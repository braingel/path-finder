import spacy 
import csv
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from sentence_transformers import SentenceTransformer


# # initalization
# aiplatform.init(
#     # your Google Cloud Project ID or number
#     # environment default used is not set
#     project='golden-pathways',

#     # the Vertex AI region you will use
#     # defaults to us-central1
#     location='us-central1',

#     # # Google Cloud Storage bucket in same region as location
#     # # used to stage artifacts
#     # staging_bucket='gs://my_staging_bucket',

#     # # custom google.auth.credentials.Credentials
#     # # environment default credentials used if not set
#     # credentials=my_credentials,

#     # # customer managed encryption key resource name
#     # # will be applied to all Vertex AI resources if set
#     # encryption_spec_key_name=my_encryption_key_name,

#     # # the name of the experiment to use to track
#     # # logged metrics and parameters
#     # experiment='my-experiment',

#     # # description of the experiment above
#     # experiment_description='my experiment description'
# )

# from typing import List, Optional

# from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


# def embed_text(
#     texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
#     task: str = "RETRIEVAL_DOCUMENT",
#     model_name: str = "text-embedding-004",
#     dimensionality: Optional[int] = 256,
# ) -> List[List[float]]:
#     """Embeds texts with a pre-trained, foundational model."""
#     model = TextEmbeddingModel.from_pretrained(model_name)
#     inputs = [TextEmbeddingInput(text, task) for text in texts]
#     kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
#     embeddings = model.get_embeddings(inputs, **kwargs)
#     return [embedding.values for embedding in embeddings]

# def main():
#     embed_text()

# if __name__ == "__main__":
#     main()


with open('occupation_data.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    next(csv_reader)
    job_titles = []
    for row in csv_reader:
        # maybe do some logic here where you can delete the whatever

        # we will also need to grab the id of the job to use as an id for sql
        job_titles.append(row[1])
# print(job_titles)

# get links from sql database
links = ['https://www.ualberta.ca/undergraduate-programs/bachelor-of-commerce-accounting.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-kinesiology-adapted-physical-activity.html', 'https://www.ualberta.ca/undergraduate-programs/bilingual-bachelor-of-commerce-affaires-internationales.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-in-agriculture-agricultural-and-resource-economics.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-in-agricultural-agricultural-business-management.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-arts-ancient-and-medieval-studies.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-in-agriculture-animal-science.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-arts-anthropology.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-with-honors-applied-mathematics.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-education-in-secondary-education-art.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-arts-art-and-design.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-with-honors-astrophysics.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-with-major-biochemistry.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-with-major-biological-sciences.html', 'https://www.ualberta.ca/undergraduate-programs/bachelor-of-science-in-mechanical-engineering-biomedical-option-co-operative-biomedical-engineering.html']

# for each link, go into the page and scrape the career imformation
URL = links[0]  # TODO: iterate through links
session = HTMLSession()
r = session.get(URL)
r.html.render(timeout=24)
html_doc = r.html.search('Why study at the University of Alberta?{}Program Requirements')[0]
soup = BeautifulSoup(html_doc, "html.parser")
# print(soup)
prospective_careers_children = soup.find('ul', id='careers-list').stripped_strings
prospective_careers = []
for career in prospective_careers_children:
    prospective_careers.append(career)
# print(prospective_careers)

""" nlp = spacy.load("en_core_web_lg")
for i in range(len(prospective_careers)):
    ua_career = prospective_careers[i]
    max = []
    for j in range(len(job_titles)):
        onet_occupation = job_titles[j]
        ua_career_nlp = nlp(ua_career)
        onet_occupation_nlp = nlp(onet_occupation)
        if (ua_career_nlp and ua_career_nlp.vector_norm):
            if (onet_occupation_nlp and onet_occupation_nlp.vector_norm):
                simiarity_index = ua_career_nlp.similarity(onet_occupation_nlp )
                if len(max) == 0:
                    max = [simiarity_index, onet_occupation]
                elif simiarity_index > max[0]:
                    max = [simiarity_index, onet_occupation]
    print("For %s the highest match is %s at %f" % (ua_career, max[1], max[0]))

# function to match the job titles and prospective careers
# filter out jobs that are lower than 0.6
# filter out duplicates

# nlp = spacy.load("en_core_web_md")

degree_job = nlp("Accountant")
job1 = nlp("Accountants and Auditors")
# job2 = nlp("Business Intelligence Analysts")

print(degree_job, "<->", job1, degree_job.similarity(job1))

# higher is more similar 
# Accountant <-> Accountants and Auditors 0.6069359874445123
# 
 """

model = SentenceTransformer("dunzhang/stella_en_1.5B_v5")# from google.cloud import aiplatform

# prospective careers
# job_titles
embeddings = model.encode(prospective_careers)
print(embeddings.shape)

# import spacy
# from itertools import combinations


# # Set globals
# nlp = spacy.load("en_core_web_md")

# def pre_process(titles):
#     """
#     Pre-processes titles by removing stopwords and lemmatizing text.
#     :param titles: list of strings, contains target titles,.
#     :return: preprocessed_title_docs, list containing pre-processed titles.
#     """

#     # Preprocess all the titles
#     title_docs = [nlp(x) for x in titles]
#     preprocessed_title_docs = []
#     lemmatized_tokens = []
#     for title_doc in title_docs:
#         for token in title_doc:
#             if not token.is_stop:
#                 lemmatized_tokens.append(token.lemma_)
#         preprocessed_title_docs.append(" ".join(lemmatized_tokens))
#         del lemmatized_tokens[
#             :
#             ]  # empty the lemmatized tokens list as the code moves onto a new title

#     return preprocessed_title_docs

# def similarity_filter(titles):
#     """
#     Recursively check if titles pass a similarity filter.
#     :param titles: list of strings, contains titles.
#     If the function finds titles that fail the similarity test, the above param will be the function output.
#     :return: this method upon itself unless there are no similar titles; in that case the feed that was passed
#     in is returned.
#     """

#     # Preprocess titles
#     preprocessed_title_docs = pre_process(titles)

#     # Remove similar titles
#     all_summary_pairs = list(combinations(preprocessed_title_docs, 2))
#     similar_titles = []
#     for pair in all_summary_pairs:
#         title1 = nlp(pair[0])
#         title2 = nlp(pair[1])
#         similarity = title1.similarity(title2)
#         if similarity > 0.8:
#             similar_titles.append(pair)

#     titles_to_remove = []
#     for a_title in similar_titles:
#         # Get the index of the first title in the pair
#         index_for_removal = preprocessed_title_docs.index(a_title[0])
#         titles_to_remove.append(index_for_removal)

#     # Get indices of similar titles and remove them
#     similar_title_counts = set(titles_to_remove)
#     similar_titles = [
#         x[1] for x in enumerate(titles) if x[0] in similar_title_counts
#     ]

#     # Exit the recursion if there are no longer any similar titles
#     if len(similar_title_counts) == 0:
#         return titles

#     # Continue the recursion if there are still titles to remove
#     else:
#         # Remove similar titles from the next input
#         for title in similar_titles:
#             idx = titles.index(title)
#             titles.pop(idx)
            
#         # return similarity_filter(titles)
#         print(similarity_filter(titles))

# if __name__ == "__main__":
#     your_title_list = ["Accountant",
# "Accounting Manager",
# "Articling Student",
# "Auditor",
# "Business Analyst",
# "Financial Analyst",
# "Human Resources Professional",
# "Internal Audit Analyst",
# "International Trade Specialist",
# "Junior Accountant",
# "Marketing Manager",
# "Operations Manager",
# "Project Manager",
# "Public Accountant",
# "Staff Accountant",
# "Staff Auditor"]
#     print(similarity_filter(your_title_list))
#     # print(len(your_title_list))