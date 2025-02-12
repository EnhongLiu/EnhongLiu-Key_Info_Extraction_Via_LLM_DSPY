import os 
import sys
import re
from dotenv import load_dotenv
load_dotenv()
pythonpath = os.getenv('PYTHONPATH')
if pythonpath:
    sys.path.extend(pythonpath.split(os.pathsep))

import dspy

from dspy.teleprompt import BootstrapFewShot, BootstrapFewShotWithRandomSearch
from collections.abc import Iterable


from dspy.evaluate.evaluate import Evaluate

from rouge_score import rouge_scorer
from pydantic import BaseModel

scorer = rouge_scorer.RougeScorer(['rouge1','rouge2', 'rougeL'], use_stemmer=True)
import json

def validate_ans(example, pred, trace = None):
    
    job_dict = {"position_title": example.position_title,
                    "location" : example.location,
                    "work_arrangement": example.work_arrangement,
                    "experience": example.experience,
                    "employment_type": example.employment_type,
                    "pay": example.pay,
                    "degree": example.degree,
                    "certifications": example.certifications,
                    "required_skills": example.required_skills,}
     

    gold = re.sub(r'\n|\s+ ', '',str(job_dict)).lower()
    print(gold)

    prediction = str(pred.info_extracted).lower()
    print(prediction)

    scores = scorer.score(gold, prediction)
    score2 = scores['rouge2'][0]
    score1 = scores['rouge1'][0]
    scoreL = scores['rougeL'][0]
    score = (0.2*score1 + 0.3*score2 + 0.5* scoreL)

    print(score)

    return score

def normalize(job_post: str) -> str:
    job_post = job_post.strip('\n')

    job_post = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', job_post, flags=re.UNICODE)

    job_post = job_post.strip('\n')

    return job_post.strip().lower()

class JobPostingExtractionCert(BaseModel):
    certifications : list[str] 
    
class JobPostingExtractionPay(BaseModel):
    certifications : str

class JobPostingExtractionPostion(BaseModel):
    position_title: str

class JobPostingExtractionLocation(BaseModel):
    location : str

class JobPostingExtractionWorkArrange(BaseModel):
    work_arrangement: str 
    
class JobPostingExtractionExp(BaseModel):
    experience : str

class JobPostingExtractionEmpType(BaseModel):
    employment_type: str
    
class JobPostingExtractionDegree(BaseModel):
    degree : str

class JobPostingExtractionSkills(BaseModel):
    required_skills : list[str]

class InfoExtractorCert(dspy.Signature):
    """Extracts single certifications and credentials from a job posting not education if nothing found put not specified. short factoids. cannot be more than 20 words or 20 characters
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_cert: JobPostingExtractionCert = dspy.OutputField(desc = "a list of strings related to certifications total should be less than 20 words or 20 characters")

class InfoExtractorPay(dspy.Signature):
    """Extracts salary or pay information from job posting if nothing found put not specified. short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_pay: JobPostingExtractionPay = dspy.OutputField(desc = "a string of salary or pay information per year or per hour has to be less than 5 words")

class InfoExtractorPostion(dspy.Signature):
    """Extracts the title or name of the position from a job posting if nothing found put not specified. short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_pos: JobPostingExtractionPostion = dspy.OutputField(desc = "3 to 5 words about the title of the job position has to be less than 5 words")


class InfoExtractorLocation(dspy.Signature):
    """Extracts where the job is located in the United States if nothing found put not specified. short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_loc: JobPostingExtractionLocation = dspy.OutputField(desc = "Where the job is located City State and ZipCode has to be less than 5 words")


class InfoExtractorWork(dspy.Signature):
    """Extracts information if the job is remote, hybrid, on-site if nothing found put not specified short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_work: JobPostingExtractionWorkArrange = dspy.OutputField(desc = "4 to 5 words on if the job is remote hybrid or onsite has to be less than 3 words")

class InfoExtractorExp(dspy.Signature):
    """Extracts information on relevant years of experience required for a job if nothing found put not specified. short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_exp: JobPostingExtractionExp = dspy.OutputField(desc = "5 to 8 words on years of experience needed has to be less than 5 words")

class InfoExtractorEmpType(dspy.Signature):
    """Extracts information if the job is full-time part-time contract internship if nothing found put not specified short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_emp: JobPostingExtractionEmpType = dspy.OutputField(desc = "5 to 8 words about the job type has to be less than 2 words")

class InfoExtractorDeg(dspy.Signature):
    """Extracts education or university information from job posting if nothing found put not specified short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_deg: JobPostingExtractionDegree = dspy.OutputField(desc = "5 to 8 words wheter its bachelors, masters, high school or PHD has to be less than 5 words")

class InfoExtractorSkills(dspy.Signature):
    """Extracts relevant skills needed to perform job should not be more than 20 words or 20 characters if nothing found put not specified short factoids. 
    """
    job_posting: str = dspy.InputField(desc = "contains job information")
    info_extracted_skills: JobPostingExtractionSkills = dspy.OutputField(desc = "total should not be more than 20 words or 20 characters")

class JobPostingModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.info_extraction_modules = {
            "position_title": dspy.ChainOfThoughtWithHint(InfoExtractorPostion, max_tokens=15,),
            "location": dspy.ChainOfThoughtWithHint(InfoExtractorLocation, max_tokens=15),
            "work_arrangement": dspy.ChainOfThoughtWithHint(InfoExtractorWork, max_tokens=30),
            "experience": dspy.ChainOfThoughtWithHint(InfoExtractorExp, max_tokens=15),
            "employment_type": dspy.ChainOfThoughtWithHint(InfoExtractorEmpType, max_tokens=15),
            "pay": dspy.ChainOfThoughtWithHint(InfoExtractorPay, max_tokens=15),
            "degree": dspy.ChainOfThoughtWithHint(InfoExtractorDeg, max_tokens=15),
            "certifications": dspy.ChainOfThoughtWithHint(InfoExtractorCert, max_tokens=30),
            "required_skills": dspy.ChainOfThoughtWithHint(InfoExtractorSkills, max_tokens=30)
        }

        self.attribute_names = {
            "position_title": "info_extracted_pos",
            "location": "info_extracted_loc",
            "work_arrangement": "info_extracted_work",
            "experience": "info_extracted_exp",
            "employment_type": "info_extracted_emp",
            "pay": "info_extracted_pay",
            "degree": "info_extracted_deg",
            "certifications": "info_extracted_cert",
            "required_skills": "info_extracted_skills"
        }

        self.hints = {
            "certifications": "Usually 3 or 4 letters capitalized, not an academic degree like BS, Masters or PHD but something you obtain professionally or through job experience or relevant technologies or certificates",
            "pay": "The dollars per hour or salary for the year or pay",
            "position_title": "The title of the job or position of the job",
            "location": "Where the job is located in the United States",
            "work_arrangement": "If the job is hybrid, remote on-site or where the job is located to go into the office",
            "experience": "Number of years of experience that a job posting is asking for",
            "employment_type": "full time, part time, contract or internship or apprenticeship",
            "degree": "Education level such as GED, High School, Bachelors, Masters, Doctorate, PHD",
            "required_skills": "The required skills to do the job"
        }

    def forward(self, job_posting):
        job_posting = job_posting.replace('\n', ' ').replace('“', '"').replace('”', '"')
        job_posting = normalize(job_posting)

        job_dict = {}
        for key in ["position_title", "location", "work_arrangement", "experience", "employment_type", "pay", "degree", "certifications", "required_skills"]:
            extraction_module = self.info_extraction_modules[key]
            hint_value = self.hints[key]
            extracted_info = getattr(extraction_module(job_posting=job_posting, hint=hint_value), self.attribute_names[key]).replace("```\n", "").replace("```", "")
            #dspy.Suggest(len(extracted_info) <= 400,f"info extract should be short and less than 400 characters right now its {len(extracted_info)} for {key}",)
            job_dict[key] = extracted_info

        return dspy.Prediction(job_posting=job_posting, info_extracted=job_dict)
    
class GenerateAnswer(dspy.Signature):
    """Extract information from a job posting and return the output in a json format if you don't know answer Not Specified. Should be key-value with output as dictionary."""

    context = dspy.InputField(desc="contain relevant facts")
    question = dspy.InputField(desc="unique possible questions")
    answer = dspy.OutputField(desc="key-value pairs of position_title, location, work_arrangement, experience, employment_type, pay, degree, certifications, required_skills each with less than 20 words")

class QUESTIONANSWER(dspy.Module):
    def __init__(self,question):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer, max_tokens=400)
        self.question=question

    def forward(self, context):
        context = context.replace('\n', ' ').replace('“', '"').replace('”', '"')
        context = normalize(context)
        question=self.question
        pred = self.generate_answer(context=context, question=question)
        pred = re.sub(r"```\n|```", "",pred.answer)
        return dspy.Prediction(context=context,answer=pred)