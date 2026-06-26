# Data format

## `metadata_vectors.json`

List of objects:

```json
{
  "itemID": 1688,
  "key": "RZFISQTN",
  "metadata": {
    "title": "...",
    "abstractNote": "...",
    "publicationTitle": "...",
    "authors": [{"name": "...", "type": "author"}],
    "tags": ["tag-a", "tag-b"],
    "date": "...",
    "dateAdded": "...",
    "dateModified": "...",
    "DOI": "...",
    "url": "..."
  },
  "embedding_text": "Title: ...\nAbstract: ...",
  "itemType": "journalArticle",
  "vector": [0.1, 0.2],
  "vector_dimension": 384,
  "model": "paraphrase-multilingual-MiniLM-L12-v2"
}
```

## `fulltext_vectors.json`

List of objects:

```json
{
  "itemID": 1688,
  "attachmentID": 1687,
  "title": "...",
  "itemType": "journalArticle",
  "total_pages": 9,
  "pdf_file": "paper.pdf",
  "chunks": [
    {
      "chunk_id": "1688_0",
      "text": "chunk text",
      "vector": [0.1, 0.2],
      "word_count": 800,
      "page": 1
    }
  ]
}
```

## `vector_store_metadata.json`

Holds:

- latest generation timestamp
- embedding model and dimension
- chunk settings
- important paths
- counts for metadata items, fulltext items, fulltext chunks
- build/update history

## Naming rationale

Use explicit names:

- `metadata_vectors.json` is clearer than `all_vectors.json`
- `fulltext_vectors.json` is clearer than `all_fulltext_vectors.json`

These names distinguish bibliographic metadata vectors from PDF full-text vectors.
