from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
from tqdm import tqdm
import torch
import pandas as pd
import gc

import pickle
import itertools

from collections import ChainMap

def process_texts(input_dict, text_splitter):
    
    output_dict = {}

    for key, text in tqdm(input_dict.items()):

        chunks = text_splitter.create_documents([text])

        split_text = [chunk.page_content for chunk in chunks]
        
        output_dict[key] = split_text
        
        torch.cuda.empty_cache()
        
        gc.collect()

    return output_dict

def filter_dict_by_value_length(data_dict, threshold):
    
    filtered_keys = [key for key, value in data_dict.items() if len(value) > threshold]

    remaining_dict = {key: value for key, value in data_dict.items() if len(value) <= threshold}

    return filtered_keys, remaining_dict

def create_extended_long_postings(filtered_keys, df):

    long_posting_list = list(itertools.chain(filtered_keys))

    df2 = df[df['id'].isin(long_posting_list)].copy()

    text_dict_long_extend = {key: value for key, value in zip(df2['id'], df2['body'])}

    #extended_long_postings = ChainMap(text_dict_long, text_dict_long_extend)

    return text_dict_long_extend

def count_words(text):

    words = text.split()

    return len(words)

def create_dataframe(data):

    data_list = [(k, v) for k, vals in data.items() for v in vals]

    df = pd.DataFrame(data_list, columns=['uuid', 'text'])

    return df

def filter_and_merge_data(data1, labels, original_data, count_words):

    data1['pred_label'] = labels

    data1['preds'] = data1['pred_label'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)

    filtered_data = data1[data1['preds'] != 0]
    non_signal_data = data1[data1['preds'] == 0]


    data1_filtered = filtered_data.groupby('uuid')['text'].apply(' '.join).reset_index()
    data1_filtered_no_signal = non_signal_data.groupby('uuid')['text'].apply(' '.join).reset_index()


    uuid_list = data1_filtered['uuid'].tolist()

    filtered_original_data = original_data[original_data['id'].isin(uuid_list)]

    filtered_original_data['word_count_original'] = filtered_original_data['body'].apply(count_words)
    data1_filtered['word_count_signals'] = data1_filtered['text'].apply(count_words)
    data1_filtered = data1_filtered.rename(columns = {'text': 'signals_text'})
    data1_filtered_no_signal['word_count_no_signal'] = data1_filtered_no_signal['text'].apply(count_words)
    data1_filtered_no_signal = data1_filtered_no_signal.rename(columns = {'text': 'no_signals_text'})

    new_data = data1_filtered.merge(filtered_original_data, left_on = 'uuid', right_on = 'id', how = 'left')
    new_data1 = new_data.merge(data1_filtered_no_signal, left_on = 'uuid', right_on = 'uuid', how = 'left')

    
    return filtered_original_data, new_data1, data1_filtered