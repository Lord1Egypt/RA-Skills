<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Common Patterns, Errors, and Limits

## Error Handling

All APIs return standard HTTP status codes:

| Code            | Cause                                   | Solutions                                                                                                                                                    |
| --------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 200             | Success                                 | -                                                                                                                                                            |
| 400             | Wrong format or data in request body    | **Solar APIs:** Check JSON syntax, required keys, correct types and values. **Document APIs:** Verify file path, format (JPEG/PNG/PDF/etc), and size (<50MB) |
| 401             | Invalid API key                         | Check `Authorization: Bearer YOUR_API_KEY` header format. Verify API key is not deleted in Console                                                           |
| 403             | Insufficient credit                     | [Register a payment method](https://console.upstage.ai/billing) or check credit balance                                                                      |
| 404             | Wrong URL path                          | Verify the request path is correct                                                                                                                           |
| 405             | Using `http://` instead of `https://`   | Use `https://` for all requests                                                                                                                              |
| 415             | Unsupported file format                 | Use supported formats: JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX                                                                          |
| 422             | Document is corrupted or damaged        | Re-save or re-export the file                                                                                                                                |
| 429             | Too many requests (rate limit exceeded) | Implement retry with exponential backoff. See [rate limits guide](https://console.upstage.ai/docs/guides/rate-limits)                                        |
| 500/502/503/504 | Server error during processing          | Retry after a short delay. If persistent, contact support                                                                                                    |

### Error Response Format

```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "code": "error_code"
  }
}
```

---


---

## Rate Limits

Rate limits vary by API and commitment tier:

| Metric  | Description         | Applies to                     |
| ------- | ------------------- | ------------------------------ |
| **RPS** | Requests per second | Document processing APIs       |
| **RPM** | Requests per minute | Chat and embedding APIs        |
| **TPM** | Tokens per minute   | Text-based models (Solar LLMs) |
| **PPM** | Pages per minute    | Document processing            |

### Default Rate Limits (Tier 0)

| API                         | RPM/RPS | TPM/PPM     |
| --------------------------- | ------- | ----------- |
| Solar Pro 3 / Pro 2         | 100 RPM | 50,000 TPM  |
| Solar Mini                  | 100 RPM | 50,000 TPM  |
| Embeddings                  | 100 RPM | 300,000 TPM |
| Document OCR                | 1 RPS   | 300 PPM     |
| Document Parse (Sync)       | 1 RPS   | 300 PPM     |
| Document Parse (Async)      | 2 RPS   | 1,200 PPM   |
| Information Extract (Sync)  | 1 RPS   | 300 PPM     |
| Information Extract (Async) | 2 RPS   | 1,200 PPM   |
| Document Classify           | 1 RPS   | 300 PPM     |

**Note:** Sync and Async APIs have different rate limits. Async APIs generally allow higher throughput.

For higher rate limits, upgrade your commitment tier or [contact support](https://get.support.upstage.ai/servicedesk/customer/portal/22/create/10367).

### Handling Rate Limits

#### Exponential Backoff

```python
import time
import openai
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

def call_with_retry(messages, max_retries=3):
    """Call API with exponential backoff on rate limit errors"""
    wait_time = 1

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="solar-pro3",
                messages=messages
            )
            return response
        except openai.RateLimitError:
            if attempt == max_retries - 1:
                raise
            print(f"Rate limit hit, waiting {wait_time}s...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff: 1s, 2s, 4s

    return None

# Usage
response = call_with_retry([{"role": "user", "content": "Hello!"}])
```

#### Batch Processing for Embeddings

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

documents = [
    "Document 1 text...",
    "Document 2 text...",
    # ... many documents
]

# Process in batches to avoid rate limits
batch_size = 32  # Max 100, but smaller batches are safer
all_embeddings = []

for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    response = client.embeddings.create(
        model="embedding-passage",
        input=batch
    )
    all_embeddings.extend([item.embedding for item in response.data])
    print(f"Processed {min(i + batch_size, len(documents))}/{len(documents)}")
```

#### Caching Strategy

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

# Simple in-memory cache
embedding_cache = {}

def get_embedding_cached(text):
    """Get embedding with caching to reduce API calls"""
    if text in embedding_cache:
        return embedding_cache[text]

    response = client.embeddings.create(
        model="embedding-query",
        input=text
    )
    embedding = response.data[0].embedding
    embedding_cache[text] = embedding
    return embedding
```

---


---

## Supported Languages

### Solar LLM Models

| Model       | Languages                                   |
| ----------- | ------------------------------------------- |
| Solar Pro 3 | English, Korean, Japanese (fully supported) |
| Solar Pro 2 | English, Korean, Japanese (fully supported) |
| Solar Mini  | English, Korean, Japanese (fully supported) |

### Document Processing (OCR)

| Character Set                       | Support Level |
| ----------------------------------- | ------------- |
| Alphanumeric (Latin)                | Full          |
| Hangul (Korean)                     | Full          |
| Hanja (Korean Chinese characters)   | Full          |
| Katakana (Japanese)                 | Full          |
| Hiragana (Japanese)                 | Full          |
| Hanzi (Simplified Chinese)          | Beta          |
| Kanji (Japanese Chinese characters) | Beta          |

**Note:** Hanja, Hanzi, and Kanji are writing systems based on Chinese characters used in Korean, Chinese, and Japanese respectively.

---


---

## Common Patterns

### Pattern 1: Document to Structured Data Pipeline

```python
# 1. Parse document to get structured content
parse_response = requests.post(
    "https://api.upstage.ai/v1/document-digitization",
    headers={"Authorization": f"Bearer {api_key}"},
    files={"document": open("document.pdf", "rb")},
    data={"model": "document-parse", "output_formats": '["markdown"]'}
)
markdown_content = parse_response.json()["content"]["markdown"]

# 2. Extract specific fields using Information Extraction
# (Or use the parsed markdown directly with Chat API for Q&A)
```

### Pattern 2: RAG Document Ingestion

```python
# 1. Parse documents
parsed = parse_document(file_path)  # Document Parse API

# 2. Split into chunks
chunks = split_into_chunks(parsed["content"]["markdown"])

# 3. Generate embeddings
embeddings = []
for chunk in chunks:
    response = client.embeddings.create(
        model="embedding-passage",
        input=chunk
    )
    embeddings.append(response.data[0].embedding)

# 4. Store in vector database
vector_db.insert(chunks, embeddings)
```

### Pattern 3: Document Routing with Classification

```python
# 1. Classify document type
classification = classify_document(file_path)  # Document Classification API

# 2. Route to appropriate schema based on document type
schema_map = {
    "invoice": invoice_schema,
    "receipt": receipt_schema,
    "contract": contract_schema
}

# 3. Extract with appropriate schema using Information Extraction API
schema = schema_map.get(classification, default_schema)
result = extract_information(file_path, schema)
```

### Pattern 4: Batch Document Processing

```python
# For large batches, use async APIs to avoid rate limits
import asyncio

async def process_documents(files):
    # Submit all jobs
    job_ids = []
    for file in files:
        job_id = submit_async_job(file)
        job_ids.append(job_id)

    # Poll for results
    results = []
    for job_id in job_ids:
        result = await poll_until_complete(job_id)
        results.append(result)

    return results
```

---


---

## Additional Resources

- [Full API Documentation](https://console.upstage.ai/docs)
- [Cookbook Examples](https://github.com/UpstageAI/cookbook)
- [Pricing](https://www.upstage.ai/pricing)
- [Support](https://support.upstage.ai)

