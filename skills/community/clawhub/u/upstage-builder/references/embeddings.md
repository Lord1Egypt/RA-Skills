<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Embeddings API

## 2. Embeddings API

Convert text into vector embeddings for semantic search and similarity.

### Endpoint

```
POST https://api.upstage.ai/v1/embeddings
```

### Request Body (JSON)

| Parameter | Type         | Required | Description                                                            |
| --------- | ------------ | -------- | ---------------------------------------------------------------------- |
| `model`   | string       | Yes      | Use `embedding-query` for queries or `embedding-passage` for documents |
| `input`   | string/array | Yes      | Text to embed. Single string or array of strings                       |

### When to Use Which Model

| Model               | Use Case                       | Input Type                                     |
| ------------------- | ------------------------------ | ---------------------------------------------- |
| `embedding-query`   | User search queries, questions | Short, specific text (questions, search terms) |
| `embedding-passage` | Documents to be searched       | Longer text (paragraphs, document chunks)      |

**Example RAG Pipeline:**

- Index documents with `embedding-passage`
- Embed user query with `embedding-query`
- Find most similar passages using dot product

### Limitations

- **Vector dimension:** 4096
- **Max tokens per input:** 4,000
- **Max batch size:** 100 texts per request
- **Max tokens per batch:** 204,800 total tokens
- **Recommended:** Keep each text under 512 tokens for optimal results
- **Vector normalization:** Outputs normalized vectors with magnitude of 1 (dot product = cosine similarity)

### Example Request

```bash
curl -X POST https://api.upstage.ai/v1/embeddings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "embedding-query",
    "input": "What is machine learning?"
  }'
```

### Example Response

```json
{
  "object": "list",
  "data": [
    {
      "index": 0,
      "embedding": [0.0012, 0.0287, -0.0045, ...],
      "object": "embedding"
    }
  ],
  "model": "embedding-query",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}
```

### Python Example (Batch Processing)

```python
import requests

documents = [
    "Korea is a beautiful country.",
    "Machine learning is a subset of AI.",
    "Python is a great programming language."
]

response = requests.post(
    "https://api.upstage.ai/v1/embeddings",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "embedding-passage",
        "input": documents
    }
)
embeddings = [item["embedding"] for item in response.json()["data"]]
```

### OpenAI SDK Compatible

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

# Single text
response = client.embeddings.create(
    model="embedding-query",
    input="What is machine learning?"
)
embedding = response.data[0].embedding

# Batch processing
response = client.embeddings.create(
    model="embedding-passage",
    input=["Text 1", "Text 2", "Text 3"]
)
embeddings = [item.embedding for item in response.data]
```

### Similarity Measurement

Since vectors are normalized (magnitude = 1), dot product equals cosine similarity:

```python
import numpy as np

# Calculate similarity between query and passages
query_embedding = get_embedding(query, model="embedding-query")
passage_embeddings = get_embeddings(passages, model="embedding-passage")

similarity_scores = [np.dot(query_embedding, p) for p in passage_embeddings]
most_similar_idx = np.argmax(similarity_scores)
print(f"Most similar: {passages[most_similar_idx]}")
```

---

