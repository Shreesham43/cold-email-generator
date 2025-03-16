
from langchain_groq import ChatGroq
import chromadb
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import WebBaseLoader
import pandas as pd
import os
import uuid

from dotenv import load_dotenv
load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant", 
            temperature=0, 
            max_retries=2, 
            api_key=os.getenv("GROQ_API_KEY")  
            )
    
    def extract_job(self, job_url):
        loader = WebBaseLoader(job_url)
        page_data = loader.load().pop().page_content
        prompt = PromptTemplate.from_template("""Given a Job descritpion {page_data} from a career portal of company. 
                        Extract role name with company name, details of the experience required for the role, top few skills required with short description and description of the role.
                        Convert this to a JSON format with role, experience_required, skills_required which is always array of strings and job_description. 
                        ###NO PREAMBLE 
                        ###VALID JSON
                        """)

        extract_chain = prompt | self.llm
        extracted_data = extract_chain.invoke({"page_data": page_data})
        try:
            parser = JsonOutputParser()
            parsed_data = parser.parse(extracted_data.content)
        except:
            raise OutputParserException("Error parsing output")
        return parsed_data if isinstance(parsed_data, list) else [parsed_data]
    
    def generate_email(self, pased_job, links):
        prompt = PromptTemplate.from_template("""
                        I'm Shreesha, IT sales executive. I work for TCS which is an IT service company. 
                        Tata Consultancy Services is an IT services, consulting and business solutions organization that has been partnering with many of the world’s largest businesses in their transformation journeys for over 56 years. Its consulting-led, cognitive powered, portfolio of business, technology and engineering services and solutions is delivered through its unique Location Independent Agile™ delivery model, recognized as a benchmark of excellence in software development.
                        A part of the Tata group, India's largest multinational business group, TCS has over 601,000 of the world’s best-trained consultants in 55 countries. The company generated consolidated revenues of US $29 billion in the fiscal year ended March 31, 2024, and is listed on the BSE and the NSE in India. TCS' proactive stance on climate change and award-winning work with communities across the world have earned it a place in leading sustainability indices such as the MSCI Global Sustainability Index and the FTSE4Good Emerging Index

                        Given a Job descritpion {parsed_data}.  Now write a cold email based on job description to the company in job description. 
                        Idea here is to land the company in job description as a client to TCS. 
                        Also given the list of portfolio links. include the relevant portfolio link from following list: {links}
                        Keep the email precise and to the point.
                        Do not include PREAMBLE 
                        ### VALID EMAIL
                        ### NO PREAMBLE
                        """)

        email_chain = prompt | self.llm
        output_email = email_chain.invoke({"parsed_data": pased_job, "links": links})
        return output_email.content