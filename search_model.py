import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

data = pd.read_csv("medquad_dataset.csv")

# remove rows with missing values
data = data.dropna()

questions = data["question"].tolist()
answers = data["answer"].tolist()

# Load embedding model
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

print("Creating embeddings...")

question_embeddings = model.encode(questions)

# Convert to numpy
embeddings = np.array(question_embeddings)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("AI Medical Search System Ready!")

while True:
    query = input("\nEnter patient question: ")

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)

    idx = I[0][0]

    print("\nSuggested Response:")
    print(answers[idx])
