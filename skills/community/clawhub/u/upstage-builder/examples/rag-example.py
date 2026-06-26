"""RAG pipeline example: embeddings + retrieval + chat with Upstage APIs."""

from __future__ import annotations

import os

import numpy as np
from openai import OpenAI


api_key = os.environ.get("UPSTAGE_API_KEY")
if not api_key:
    raise RuntimeError("Set UPSTAGE_API_KEY before running this example.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.upstage.ai/v1",
)

# Sample documents to index
documents = [
    "Solar energy converts sunlight into electricity using photovoltaic cells.",
    "Wind turbines generate power by converting kinetic energy from wind.",
    "Hydroelectric power uses flowing water to spin turbines and produce electricity.",
    "Nuclear energy is produced through fission of uranium atoms in reactors.",
    "Geothermal energy harnesses heat from the Earth's interior for power generation.",
]

# Step 1: Index documents with embedding-passage
response = client.embeddings.create(model="embedding-passage", input=documents)
doc_embeddings = [item.embedding for item in response.data]


# Step 2: Search with embedding-query
def search(query: str, top_k: int = 3) -> list[str]:
    query_resp = client.embeddings.create(model="embedding-query", input=query)
    query_emb = query_resp.data[0].embedding

    scores = [float(np.dot(query_emb, emb)) for emb in doc_embeddings]
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return [documents[i] for i in top_indices]


# Step 3: Generate answer with Solar Pro3
query = "How does solar power work?"
relevant_docs = search(query)

response = client.chat.completions.create(
    model="solar-pro3",
    messages=[
        {
            "role": "system",
            "content": "Answer based on this context:\n\n"
            + "\n".join(f"- {doc}" for doc in relevant_docs),
        },
        {"role": "user", "content": query},
    ],
)

print(f"Query: {query}")
print(f"Retrieved: {relevant_docs}")
print(f"Answer: {response.choices[0].message.content}")
