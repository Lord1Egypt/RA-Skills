---
name: twelvelabs-video-intelligence
description: Search inside videos, generate summaries, and analyze video content using TwelveLabs video understanding AI. Use when the user wants to find moments in a video, summarize video content, get chapters or highlights, or work with video embeddings.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - TWELVE_LABS_API_KEY
    primaryEnv: TWELVE_LABS_API_KEY
    emoji: "🎬"
    homepage: https://docs.twelvelabs.io
    install:
      - kind: pip
        package: twelvelabs
        label: Install TwelveLabs Python SDK (pip)
    links:
      homepage: https://twelvelabs.io
      repository: https://github.com/twelvelabs-io/twelvelabs-python
      documentation: https://docs.twelvelabs.io/reference
---

# TwelveLabs

Search inside videos, generate summaries, chapters, highlights, and analyze video content using the TwelveLabs Python SDK (v1.2.1).

## Setup

1. Get your API key: https://api.twelvelabs.io
2. Install the SDK:
   ```bash
   python3 -m pip install twelvelabs
   ```
3. Set environment variable:
   ```bash
   export TWELVE_LABS_API_KEY="your-api-key"
   ```

## Important: index before you search or analyze

Videos must be indexed before they can be searched or analyzed. Always index a video and wait for status `Ready` before running search or analysis commands.

## Initialize the client

All snippets below assume this setup:

```python
import os
from twelvelabs import TwelveLabs

client = TwelveLabs(api_key=os.environ["TWELVE_LABS_API_KEY"])
```

## List indexes

```python
for index in client.indexes.list():
    print(f"{index.id}: {index.index_name}")
```

## Create an index

```python
from twelvelabs.indexes import IndexesCreateRequestModelsItem

index = client.indexes.create(
    index_name="my-index",
    models=[
        IndexesCreateRequestModelsItem(model_name="marengo3.0", model_options=["visual", "audio"]),
        IndexesCreateRequestModelsItem(model_name="pegasus1.2", model_options=["visual", "audio"]),
    ],
    addons=["thumbnail"],
)
print(f"Created index: {index.id}")
```

Use both models: Marengo 3.0 for search/embeddings, Pegasus 1.2 for analysis.

## Upload an asset

From URL:
```python
asset = client.assets.create(method="url", url="https://example.com/video.mp4")
print(f"Asset: {asset.id}")
```

From local file:
```python
with open("/path/to/video.mp4", "rb") as f:
    asset = client.assets.create(method="direct", file=f)
print(f"Asset: {asset.id}")
```

Assets are reusable — upload once, index into multiple indexes.

## Index an asset

```python
indexed = client.indexes.indexed_assets.create(
    index_id="<index-id>",
    asset_id=asset.id,
)
print(f"Indexed asset: {indexed.id}")
```

## Check indexing status

```python
result = client.indexes.indexed_assets.retrieve(
    index_id="<index-id>",
    indexed_asset_id="<indexed-asset-id>",
)
print(f"Status: {result.status}")
```

Statuses: `pending` → `queued` → `indexing` → `ready` (or `failed`).

### Poll until ready

```python
import time

while True:
    result = client.indexes.indexed_assets.retrieve(
        index_id="<index-id>",
        indexed_asset_id=indexed.id,
    )
    if result.status == "ready":
        print(f"Ready. Indexed asset ID: {indexed.id}")
        break
    if result.status == "failed":
        raise RuntimeError("Indexing failed")
    print(f"Status: {result.status} — waiting...")
    time.sleep(5)
```

## List indexed assets

```python
for video in client.indexes.indexed_assets.list("<index-id>"):
    duration = video.system_metadata.duration if hasattr(video, "system_metadata") and video.system_metadata else ""
    filename = video.system_metadata.filename if hasattr(video, "system_metadata") and video.system_metadata else ""
    print(f"{video.id}  {filename}  {duration}s")
```

## Search

```python
results = client.search.query(
    index_id="<index-id>",
    query_text="person giving a presentation",
    search_options=["visual", "audio"],
)

for result in results:
    print(f"{result.start:.1f}s - {result.end:.1f}s  rank={result.rank}  video={result.video_id}")
```

Results include timestamps (`start`/`end` in seconds) and relevance `rank` (1 = most relevant).

### Search options

```python
results = client.search.query(
    index_id="<index-id>",
    query_text="your query",
    search_options=["visual", "audio"],  # or ["transcription"]
    threshold="medium",                   # high, medium, low (default), none
    group_by="video",                     # clip (default) or video
    sort_option="clip_count",             # score (default) or clip_count
    page_limit=20,                        # max 50
)
```

### Transcription search

```python
results = client.search.query(
    index_id="<index-id>",
    query_text="what the speaker said about revenue",
    search_options=["transcription"],
    transcription_options=["semantic"],  # semantic, lexical, or both (default)
)
```

### Search with filtering

```python
import json

# Filter by duration range
results = client.search.query(
    index_id="<index-id>",
    query_text="your query",
    search_options=["visual"],
    filter=json.dumps({"duration": {"gte": 60, "lte": 300}}),
)
```

Filter fields: `id` (array of video IDs), `duration`, `width`, `height`, `size`, `filename`.

## Analyze a video

Use a prompt to generate summaries, chapters, highlights, titles, topics, hashtags, action items, or any open-ended analysis:

```python
response = client.analyze(
    video_id="<video-id>",
    prompt="Generate a summary with chapters and key takeaways",
)
print(response.data)
```

Example prompts:
- `"Summarize this video in 3 paragraphs"`
- `"List the chapters with timestamps"`
- `"Extract action items from this meeting"`
- `"Generate a title, 5 topics, and 10 hashtags"`
- `"Create a table of contents"`

### Streaming analysis

```python
stream = client.analyze_stream(
    video_id="<video-id>",
    prompt="Describe this video",
)
for chunk in stream:
    if chunk.event_type == "text_generation":
        print(chunk.text, end="")
```

## Composed search (text + image)

Combine text and image for refined results. Marengo 3.0 required:

```python
with open("image.jpg", "rb") as f:
    results = client.search.query(
        index_id="<index-id>",
        query_text="red color",
        query_media_type="image",
        query_media_file=f,
        search_options=["visual"],
    )
```

## Entity search

Find specific people or objects using reference images. Marengo 3.0 required:

```python
# Create collection + entity with reference images
collection = client.entity_collections.create(name="my-team")
asset = client.assets.create(method="url", url="https://example.com/person.jpg")
entity = client.entity_collections.entities.create(
    entity_collection_id=collection.id,
    name="Person Name",
    asset_ids=[asset.id],
)

# Search for entity
results = client.search.query(
    index_id="<index-id>",
    query_text=f"<@{entity.id}> is walking",
    search_options=["visual", "audio"],
)
```

## Embeddings

### Retrieve embeddings from an indexed video

```python
video = client.indexes.videos.retrieve(
    index_id="<index-id>",
    video_id="<video-id>",
    embedding_option=["visual", "audio"],
)

for segment in video.embedding.video_embedding.segments:
    print(f"{segment.start_offset_sec}s - {segment.end_offset_sec}s  scope={segment.embedding_scope}  option={segment.embedding_option}  dims={len(segment.float_)}")
```


### Create new embeddings (Embed v2 API)

```python
from twelvelabs.types import TextInputRequest, ImageInputRequest, MediaSource

# Text embedding (512 dimensions)
res = client.embed.v_2.create(
    input_type="text",
    model_name="marengo3.0",
    text=TextInputRequest(input_text="your text here"),
)
embedding = res.data[0].embedding

# Image embedding from URL
res = client.embed.v_2.create(
    input_type="image",
    model_name="marengo3.0",
    image=ImageInputRequest(media_source=MediaSource(url="https://example.com/image.jpg")),
)
embedding = res.data[0].embedding
```

## Sample video for testing

Big Buck Bunny — 10 seconds, 1MB, free to use:
```
https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4
```

## Limitations

- **Indexing is async** — videos take time to process. Poll `client.indexes.indexed_assets.retrieve()` until status is `ready`.
- **Composed search requires Marengo 3.0** — text + image search only works with this model.
- **Entity search requires Marengo 3.0** — and additional setup (collections, assets, entities).
- **Query limit** — search queries support up to 500 tokens (Marengo 3.0) or 77 tokens (older models).
- **Page limit** — max 50 results per search page.
- **Index names must be unique** — use timestamps or UUIDs to avoid conflicts.
- **`client.summarize()` and `client.gist()` are deprecated** — use `client.analyze(prompt="...")` instead.

## Resources

- [TwelveLabs Documentation](https://docs.twelvelabs.io)
- [API Reference](https://docs.twelvelabs.io/reference)
- [Python SDK](https://github.com/twelvelabs-io/twelvelabs-python) v1.2.1 (latest)
- [Get API Key](https://api.twelvelabs.io)
