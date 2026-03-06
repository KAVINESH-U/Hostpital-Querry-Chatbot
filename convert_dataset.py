import os
import xml.etree.ElementTree as ET
import pandas as pd

base_path = "."   # current MedQuAD folder
questions = []
answers = []

for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)

    if os.path.isdir(folder_path):   # check if it is a folder
        for file in os.listdir(folder_path):
            if file.endswith(".xml"):
                file_path = os.path.join(folder_path, file)

                tree = ET.parse(file_path)
                root = tree.getroot()

                for qa in root.findall(".//QAPair"):
                    q = qa.find("Question")
                    a = qa.find("Answer")

                    if q is not None and a is not None:
                        questions.append(q.text)
                        answers.append(a.text)

df = pd.DataFrame({
    "question": questions,
    "answer": answers
})

df.to_csv("medquad_dataset.csv", index=False)

print("Dataset converted successfully!")
print("Total Q&A pairs:", len(df))