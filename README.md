## Information Job Posting Signal Extraction

### Intro

Our solution addresses the challenges of unstructured text data by leveraging the latest advancements in large language models utilizing SetFit, LangChain and DSPy to extract meaningful information out of a job posting.   

TLDR;

   * LangChain and LangChain Experimental is used to split the text using semantic text splitting and recursive character text splitting
     * Github: https://github.com/langchain-ai/langchain
     * Docs: https://python.langchain.com/v0.2/docs/introduction/
    
   * SetFit is then trained with a labeled dataset labeled by a human to filter out signals we don't need from a job
     * Github: https://github.com/huggingface/setfit
     * Docs: https://huggingface.co/docs/setfit/en/quickstart
    
   * DSPy program is created to do information extraction on the denoised job posting extracting certifications, pay, position_title, work_arrangement, experience, employment_type, degree and required_skills.
     * Github: https://github.com/stanfordnlp/dspy
     * Docs: https://dspy-docs.vercel.app/docs/intro 

* Here is the overall pipeline in one notebook that utilizes the utils folder. [Overall Pipeline Notebook](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/tutorial/example_pipeline.ipynb) 
  
  * In the DSPy pipeline, you can select the desired LLM suitable for your compute resource
  * If you run the more precise pipeline it is more resource intensive and might not be able to run the 4-bit quantized Qwen 2 on a 16 GB VRAM

---

### Text Preproecessing:
    
**LangChain Text Chunking Recursive Character Text Splitting and Semantic Text Splitting**
   
   To reduce computational costs and token usage in our DSPy framework, we preprocess job postings by filtering out irrelevant sentences through text chunking. Using the LangChain library, we employ recursive character text splitting, which leverages          document structure and default separators like double new lines, new lines, spaces, and characters, as it is less computationally expensive than semantic splitting. Semantic text splitting, on the other hand, requires an embedding model to infer            semantic relationships between chunks for sentence segmentation.

   How we chose between Recursive Character Text Splitting and Semantic Text Splitting is if the job post had more than 1500 words and 8000 tokens it would fall into Recursive Character Text Splitting. Anything below would go to Semantic Text Splitting. 
   
* Text Chunking Notebook that does semantic and recursive [LangChain Text Chunking](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/01_text-chunking.ipynb)
  
Data is then aggregated and a sample of 10,000 is taken.  Our team labeled a dataset of 300 and 3500. 
      
* Creating the data for labeling to be moved to excel to label for binary classification. [Data Selection for Labeling](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/02_data_creation.ipynb)

**Instructions for labeling:**

  It is often most effective to approach classification tasks, especially those involving yes or no scenarios, with binary labels. In our case, this means labeling as '0' any signals that do not relate to specific attributes like position, location, work arrangement, experience, employment type, pay/salary, degree/certifications, and required skills. Should the Adept team decide to switch to a multi-class or multi-label approach, it remains beneficial to break down the task into binary classification steps before consolidating the labels and feeding them into a machine learning or AI pipeline.

The signals are defined as follows:

  * Position: The name or title of the position.
  * Location: Where the position is located in the United States.
  * Work Arrangement: Hybrid, On-Site, Remote.
  * Experience: Years of experience or preferred experience for a job seeker.
  * Employment Type: Full-Time, Part-Time, Contractor, Internship, or Apprenticeship.
  * Pay / Salary: The hourly pay or annual salary.
  * Degree / Certifications: Educational qualifications (Bachelors, High School, GED, Masters, PhD) and special industry or other certifications.
  * Required Skills: The daily tasks expected from the employee.

  Below is an example of how the labeling might look in Excel. However, for such manual tasks, it is recommended to purchase a one-time Prodigy subscription for the Adept team. Prodigy can help labelers work faster and use the already labeled dataset to train a smaller model. This model can then create a silver labeled dataset (labeled by machine learning or AI), which can be corrected to extend the gold labeled dataset (human-evaluated and labeled dataset). More information can be found on  Prodigy: https://prodi.gy


  Overall, we reduced the text in job postings by 25%. Our team labeled the dataset leniently, aiming to retain potentially useful information. However, a more aggressive approach to reducing noisy signals might be more effective.

Common elements to exclude include:

  * Mentions of equal pay, which are not signals, labeled as 0.
  * Generic skills such as "must work well with a team" that do not specify job tasks, labeled as 0.
  * Introductions or company culture descriptions, labeled as 0.

---

**Binary Classification SetFit Signal Denoising**

Model is then used to remove text that aren't signals we are looking to extract and saved as csv file for DSPy information extraction. The signals that the team looked for are related to position, location, work arragement, experience, employment type, pay, degree, certification and required skills. A binary classification model was created and data was labeled. The nomic-embed-text-v1.5 was used as the embedding model. 

SetFit model training on 3500 dataset example.  Trained on 5 epochs and 5 iterations with max sequence length of 512. 

* Fine-Tuning a SetFit Model [SetFit Model Training](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/03_setfit_model_training_3500.ipynb)

Distillation of the SetFit model that used paraphrase-mpnet-base-v2 as the teacher model and paraphrase-all-MiniLM-L6-V2 as the student model. 

* Distilling a model using a Teacher and Student model [SetFit Model Distillation](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/04_setfit_distilliation.ipynb)

Model Comparison on Accuracy Score and Custom Dataset
   
<div style="text-align:center;">


| Model                                 | Accuracy | Prediction Ratio |
|---------------------------------------|----------|------------------|
| paraphrase-all-MiniLM-L6-V2 – 3500    | 0.800    | 0.571            |
| nomic-embed-text-v1.5 – 300           | 0.700    | 0.700            |
| paraphrase-mpnet-base-v2 - 300        | 0.850    | 1.00           |
| nomic-embed-text-v1.5 – 3500          | 0.858    | 0.714           |
| paraphrase-mpnet-base-v2 - 3500       | 0.822    | 1.00           |
| paraphrase-mpnet-base-v2 - 3500 distilled | 0.555    | 0.571            |

</div>

We compared the model based off of accuracy and a custom dataset.  

* Comparing all our trained models [SetFit Model Comparison](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/05_setfit_model_compare.ipynb)
  
The mpnet model performed the best. Distillation unfortunately didn't produce good results.  Once denoising was done. The list of strings was the put together back into a single string. 

* Performing inference with the final selected model [SetFit Model Inference](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/06_setfit_model_infernece.ipynb)
  
Lastly we look at the model using a Tri-gram Frequency bar chart to see how well denoising performed. 
   
* Looking at word frequency of the denoised job posting using count vectorization [SetFit Word Frequency Model Eval](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/02_preprocess/07_setfit_perf_eval.ipynb)

---

### DSPy Information Extraction pipeline
   
This section explored information extraction utilizing DSPy.  Several models were used from Hugging Face as well as proprietary models such as GPT and Gemini.  For open source models Qwen 2 performed the best from Alibaba.  The signature and module utilizing DSPy was experinmented in two ways.  

1. Utilizing a Question and Answer format to run through the the job posting answering different questions and then returning a dictionary string.
2. Utilizing the Pydantic class and then splitting up the task into multiple information searches and then combining it together as a dictionary.

ChainOfThoughWithAHint was utilizized as well as ChainOfThought for the DSPy module.  

<img src = 'https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/c0deb837cd2ffb9b1a47c28f1251e8db259c7666/data/dspy.png'>

**Model Comparison Table**

<div align="center">

| **Model** | **Pros** | **Cons** | **When to use** |
|-----------|----------|----------|----------------|
| GPT | GPT-4 and GPT-3.5 Turbo are industry leaders producing great results for info extraction | Vendor lock-in, need to send GPT your data | If inference speed matters more than data security, and you are not worried about vendor lock-in. You want a smarter model. |
| Gemini | Good alternative to GPT, works great if you're in the Google ecosystem using Vertex AI. Cost is based on character count, potentially cheaper | Not as good as GPT overall, and you need to send your data to Google with vendor lock-in | Inference speed matters, you are a bit cost-sensitive, and don't care about vendor lock-in. |
| Ollama | Great alternative for local use on a Mac or Linux device, no data sharing | Does not work if your pipeline needs to be on the cloud | Data team uses Apple products; this is a great alternative to using a GPU as it utilizes the M1, M2, M3 chip efficiently with great inference times. |
| Hugging Face Models | Can use your own fine-tuned models and apply quantization techniques to reduce memory footprint | Greater complexity compared to using an API key. You have to host the model yourself and consider the overall infrastructure cost, especially GPU usage | If data privacy is a priority, able to do predictions in batch, higher level of knowledge of the transformers library, and access to GPUs with VRAM 24GB and up. |

</div>
  
**Proprietary Models:**

  GPT 
  
 ```python
    # Connect OpenAI gpt3.5 turbo to DSPy
    api_key=os.getenv('openai_key')
    llm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=api_key)
    dspy.settings.configure(lm=llm)
  ```
* [DSPy with GPT3.5 Turbo](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/GPT3.5-Turbo.ipynb)

  Gemini

   ```python
    gemini_key=os.getenv('gemini_key')
    gemini = dspy.Google("gemini-1.5-flash-latest", api_key=gemini_key)
    dspy.settings.configure(lm=gemini, max_tokens=1024)
  ```
* [DSPy with Gemini1.5](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/Gemini1.5Flash.ipynb)

**Open Source Models**
  
  Ollama
  ```python
  llm = dspy.OllamaLocal(model='qwen2:latest', max_tokens = 1000, temperature=0.0)
  dspy.settings.configure(lm=llm)
  ```
* [DSPy with Ollama Qwen 2 Q&A Format](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/ollama_qwen2.ipynb)
* [DSPy with Ollama Qwen 2 Pydantic with chainofthought with a hint](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/ollama_qwen2_pydantic_v2.ipynb)
* [DSPy with Ollama Llama 3 Pydantic with chainofthought with a hint](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/ollama_llama3_pydantic_v2.ipynb)

  Post and Pre Quantized models from HuggingFace
    * Note:  Unless you want to customize the level of quantization, post-quantized version of the models uploaded by Unsloth were more efficient to use than quantizing it yourself through bitsandbytes.  The memory usage on the GPU was lower. 
  
  ```python
  # HuggingFace 4-Bit Pre-Quant
  access_token = ""
  model_name = "google/gemma-7b"
  llm = dspy.HFModel(model=model_name, hf_device_map='auto', token=access_token, model_kwargs= {'temperature': 0.0, 'do_sample': False})
  llm.model=None
  gc.collect()
  bnb_config = BitsAndBytesConfig(
      load_in_4bit=True,  # 4-bit quantization
      bnb_4bit_quant_type='nf4',  # Normalized float 4
      bnb_4bit_use_double_quant=True,  # Second quantization after the first
      bnb_4bit_compute_dtype=bfloat16  # Computation type)
  llm.model=AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
  dspy.settings.configure(lm=llm)

  # Hugging Face Post-Quant 4 Bit from Unsloth
  llm = dspy.HFModel(model="unsloth/Qwen2-7B-bnb-4bit", hf_device_map='auto', model_kwargs= {'temperature':0.0,'do_sample': False})
  dspy.settings.configure(lm = llm)

  ```
* [DSPy with Quantized HuggingFace Model Q&A ](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/Llama3_Quantized.ipynb)  
* [DSPy with Qwen 2 Unsloth Q&A format post-quantization](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/quantized_qwen2.ipynb)
* [DSPy with Qwen 2 Q&A with bitsandbytes pre-quantization](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/pre-quantized_qwen2.ipynb)
* [DSPy Q&A with quantized Qwen 2 with mlFlow](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/post-quantized_qwen2_v2_mlflow.ipynb)

<div style="text-align:center;">

For metrics we looked a combined rouge score of rouge 1 rouge 2 and rouge L.  We also did human inspection to see how well the DSPy program performed before going back and recoding the program again optimizing its performance.  Unfortuantely the compiler for some reason became really greedy and started to add more information than nececcssary.  Hence, in our experiments going back through and using llm.inspect_history() and llm.history actually helped us construct a better program than using the compiler.  

| Model and Method                      | Combined Rouge |
|---------------------------------------|----------|
| Qwen 2 Q&A   | 0.648   | 
| Llama 3 Q&A          | 0.494    |
| Qwen 2 Pydnatic      | 0.523    | 
| Qwen 2 Pydnatic      | 0.599    | 


</div>

**Other Exploration Outside DSPy Info Extract**

During the last two weeks of the practicum, a model was released that utilized Qwen1.5-0.5B and phi-3-mini-4k, known as NuExtract (https://huggingface.co/numind/NuExtract). NuExtract is a purely information extraction model. In our brief experiments, we found that it performed quite well; however, it struggled with extracting certifications, recognizing employment types, and fully retrieving salary information.

* [NuExtract with Qwen1.5-0.5B](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/nuextract_tiny.ipynb)
* [NuExtract with Phi-3-3.8B](https://github.com/EnhongLiu/Key_Info_Extraction_Via_LLM_DSPY/blob/7cf96f3a88b1439961ba05b74654a66b6e04b9b6/03_ml/nuextract_base.ipynb)

---

### Main Library Dependencies 

<div align="center">

| pypi library | version |
|----------|----------|
| accelerate  | 0.30.1   |
| beautifulsoup4  | 4.12.3  |
| bitsandbytes  | 0.42.0  |
| chromadb   | 0.5.0   |
| faiss-cpu  | 1.8.0  |
| langchain | 0.2.5  |
| langchain-community | 0.2.5 |
| langchain-experimental | 0.0.59 |
| langchain-core  | 0.2.9  |
| langchain-text-splitters | 0.2.0 |
| langchain-openai | 0.1.9 |
| safetensors | 0.4.3 |
| sentence-transformers | 2.7.0 |
| tokenizers | 0.19.1 |
| transformers | 4.41.1 |
| umap-learn | 0.5.6 |
| dspy-ai | 2.4.10 |
| setfit | 1.0.3 |

</div>

---

### Reference Notebooks 

<div align="center">

| **Resource** | **Code** | **Video/Article** | **Description** |
| --- | ------------- | ------------- | ------------- | 
| 5 Levels of Text Splitting | [Link](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb) | [YouTube](https://www.youtube.com/watch?v=8OJC21T2SL4&t=2189s) | Greg Kamradt on text splitting methods |
| Efficient Few-Shot Learning | [Link](https://github.com/huggingface/setfit/blob/main/notebooks/text-classification.ipynb) | [YouTube](https://www.youtube.com/watch?v=8h27lV8v8BU&t=3s) | Lewis Tunstall and Moshe Wasserblat on SetFit |
| Few-Shot Learning In Production | [Link](https://github.com/huggingface/workshops/blob/main/fewshot-learning-in-production/setfit-optimisation.ipynb) | [YouTube](https://www.youtube.com/watch?v=FKsARHV3ZTI&t=56s) | Lewis Tunstall on model distillation |
| NLP with Transformers | [Link](https://github.com/nlp-with-transformers/notebooks/blob/main/08_model-compression.ipynb) | [O'Reilly](https://www.oreilly.com/library/view/natural-language-processing/9781098136789/) | HuggingFace Library, model compression |
| DSPy Learning Series | [Link](https://github.com/insightbuilder/python_de_learners_data/blob/main/code_script_notebooks/projects/exploring_dspy/playlist_assy.ipynb) | [YouTube](https://www.youtube.com/watch?v=zBb8XQZ4ksI&list=PLbzjzOKeYPCqoCjk_rTuZA1Qobq5_D_hX&index=1) | Kamalraj M M on DSPy |
| Info Extraction with DSPy | [Link](https://colab.research.google.com/drive/1CpsOiLiLYKeGrhmq579_FmtGsD5uZ3Qe#scrollTo=hVrLgbZvbJ97) | [Docs](https://dspy-docs.vercel.app/docs/tutorials/other_tutorial) | DSPy extraction for biomedical research |
| Resume Extraction | [Link](https://github.com/PhiBrandon/resume_extraction_dspy/blob/main/start.py) | [YouTube](https://www.youtube.com/watch?v=iAPfIZ-gAGc) | Brandon Phillip on Pydantic with DSPy |

</div>
