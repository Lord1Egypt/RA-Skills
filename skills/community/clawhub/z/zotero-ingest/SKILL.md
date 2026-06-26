---
name: zotero-ingest
version: 1.0.0
description: Add papers (arXiv, DOI, URL) to Zotero via the Zotero REST API. Requires
  Zotero to be open for sync. Use when ingesting research papers into the Zotero library
  for citation management.
metadata:
  openclaw:
    emoji: 📚
    primaryEnv: ZOTERO_API_KEY
    requires:
      env:
      - ZOTERO_API_KEY
    network:
      outbound: true
      reason: Calls Zotero REST API to add items to the library.
---

# Skill: Zotero Ingest

Add papers (arxiv, DOI, URL) to Zotero via the web API. Uses the Zotero REST API — requires Zotero to be open for sync but does NOT require the local connector.

## Credentials

- **API Key:** `op read "op://OpenClaw/Zotero API Credentials/credential"`
- **User ID:** `10425097`
- **Base URL:** `https://api.zotero.org/users/10425097`

## Routing Rule (mandatory)

When given an arxiv link to research:
1. **Check if a relevant collection exists** (see Known Collections below)
2. If yes → add to that collection
3. If no matching collection → add as **unfiled item** (omit `collections` field)
4. Never create a new collection without being asked — unfiled is fine

## Known Collections

| Key | Name | Use for |
|---|---|---|
| `MYPG9XG6` | LLM Routing | LLM routing, cost/quality tradeoff, model selection papers |
| `9JVUH7YZ` | AI and Deep Learning | General ML/AI papers, transformers, SSMs, foundation models |
| `FF6WRU8W` | Blockchain | Web3, DeFi, smart contracts, crypto protocols |
| `PUFVMY85` | Cryptography and Zero Knowledge Proofs | ZK proofs, cryptographic protocols |
| `XQXSE29R` | Web | Web standards, protocols |

Uni collections (read-only, don't add to these):
`U76V7JH5` COMP3820 · `R6XBKEI6` COMP7110 · `QRHSXVZ2` BISM7255 · `5DKQBA36` INFS7450 · `AM9QMQKZ` COMP7703 · `98D36WM7` Networks Crowds and Markets · `FKPD5STF` Social Media Mining · `S37P9GSW` FastAI · `UIYY355G` Turbin3 Research paper

## Add an arXiv Paper (standard method)

```python
import urllib.request, json, subprocess, time

def get_zotero_key():
    return subprocess.check_output(['op', 'read', 'op://OpenClaw/Zotero API Credentials/credential']).decode().strip()

def add_arxiv(arxiv_id: str, title: str, authors: list, date: str,
              abstract: str = "", collection_key: str = None):
    """
    authors format: [{"creatorType":"author","firstName":"John","lastName":"Doe"}]
    collection_key: None = unfiled (correct when no matching category)
    """
    key = get_zotero_key()
    base = "https://api.zotero.org/users/10425097"
    headers = {"Zotero-API-Key": key, "Content-Type": "application/json"}

    item = {
        "itemType": "preprint",
        "title": title,
        "creators": authors,
        "date": date,
        "abstractNote": abstract,
        "repository": "arXiv",
        "archiveID": f"arXiv:{arxiv_id}",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "tags": [{"tag": "auto-ingested"}],
    }
    if collection_key:
        item["collections"] = [collection_key]

    payload = json.dumps([item]).encode()
    req = urllib.request.Request(f"{base}/items", data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = json.loads(r.read())

    parent_key = list(resp["successful"].values())[0]["key"]

    # Attach PDF link as child item
    pdf = {
        "itemType": "attachment",
        "linkMode": "linked_url",
        "title": "PDF (arXiv)",
        "url": f"https://arxiv.org/pdf/{arxiv_id}",
        "parentItem": parent_key,
        "collections": [],
    }
    time.sleep(0.3)
    payload = json.dumps([pdf]).encode()
    req = urllib.request.Request(f"{base}/items", data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        json.loads(r.read())

    return parent_key
```

## Batch Ingest

```python
papers = [
    {
        "arxiv": "2406.18665",
        "title": "RouteLLM: Learning to Route LLMs with Preference Data",
        "authors": [{"creatorType":"author","firstName":"Isaac","lastName":"Ong"}],
        "date": "2024",
        "collection": "MYPG9XG6",
    },
    # ...
]

for p in papers:
    key = add_arxiv(p["arxiv"], p["title"], p["authors"], p["date"],
                    collection_key=p.get("collection"))
    print(f"✅ {p['arxiv']} → {key}")
    time.sleep(0.4)
```

## Add a Non-arXiv URL (blog post, doc, webpage)

```python
def add_url(url: str, title: str, authors: list, date: str,
            item_type: str = "blogPost", collection_key: str = None):
    key = get_zotero_key()
    base = "https://api.zotero.org/users/10425097"
    headers = {"Zotero-API-Key": key, "Content-Type": "application/json"}

    item = {
        "itemType": item_type,  # "blogPost", "webpage", "report"
        "title": title,
        "creators": authors,
        "date": date,
        "url": url,
        "tags": [{"tag": "auto-ingested"}],
    }
    if collection_key:
        item["collections"] = [collection_key]

    payload = json.dumps([item]).encode()
    req = urllib.request.Request(f"{base}/items", data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = json.loads(r.read())
    return list(resp["successful"].values())[0]["key"]
```

## List Collections (to discover new collection keys)

```python
def list_collections():
    key = get_zotero_key()
    req = urllib.request.Request(
        "https://api.zotero.org/users/10425097/collections?limit=100",
        headers={"Zotero-API-Key": key}
    )
    with urllib.request.urlopen(req) as r:
        cols = json.loads(r.read())
    for c in cols:
        print(c["key"], c["data"]["name"], "| parent:", c["data"].get("parentCollection", "root"))
```

## Move Item to Collection

```python
def move_to_collection(item_key: str, collection_key: str):
    key = get_zotero_key()
    base = "https://api.zotero.org/users/10425097"
    headers = {"Zotero-API-Key": key, "Content-Type": "application/json"}

    # Get current item + version
    req = urllib.request.Request(f"{base}/items/{item_key}", headers=headers)
    with urllib.request.urlopen(req) as r:
        item = json.loads(r.read())

    version = item["version"]
    item["data"]["collections"].append(collection_key)

    patch_headers = {**headers, "If-Unmodified-Since-Version": str(version)}
    payload = json.dumps(item["data"]).encode()
    req = urllib.request.Request(f"{base}/items/{item_key}", data=payload,
                                  headers=patch_headers, method="PATCH")
    with urllib.request.urlopen(req) as r:
        return r.status
```

## Create a Collection

```python
def create_collection(name: str, parent_key: str = None):
    key = get_zotero_key()
    headers = {"Zotero-API-Key": key, "Content-Type": "application/json"}
    col = {"name": name}
    if parent_key:
        col["parentCollection"] = parent_key
    payload = json.dumps([col]).encode()
    req = urllib.request.Request(
        "https://api.zotero.org/users/10425097/collections",
        data=payload, headers=headers, method="POST"
    )
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    return list(resp["successful"].values())[0]["key"]
```

## Delete Items

```python
def delete_item(item_key: str):
    key = get_zotero_key()
    base = "https://api.zotero.org/users/10425097"
    headers = {"Zotero-API-Key": key}
    req = urllib.request.Request(f"{base}/items/{item_key}", headers=headers)
    with urllib.request.urlopen(req) as r:
        version = json.loads(r.read())["version"]
    del_headers = {**headers, "If-Unmodified-Since-Version": str(version)}
    req = urllib.request.Request(f"{base}/items/{item_key}", headers=del_headers, method="DELETE")
    with urllib.request.urlopen(req) as r:
        return r.status
```

## Notes

- Zotero syncs automatically when open — no extra step needed after API writes
- `linked_url` PDF attachments open in browser (not downloaded locally). User can right-click → "Find Available PDF" to store locally.
- `409 SESSION_EXISTS` from the local connector = already exists (treat as success)
- API returns version numbers — always fetch current version before PATCH/DELETE
- Rate limit: ~10 req/s — add `time.sleep(0.3)` between calls in loops
- Collections are additive — an item can be in multiple collections simultaneously
