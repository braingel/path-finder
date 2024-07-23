nlp = spacy.load("en_core_web_md")

degree_job = nlp("Business Analyst")
job1 = nlp("Accountants and Auditors")
job2 = nlp("Business Intelligence Analysts")

print(degree_job, "<->", job2, degree_job.similarity(job2))