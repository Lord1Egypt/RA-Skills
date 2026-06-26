# 📎 zotero-pdf-upload

[中文版](README_CN.md) | [GitHub](https://github.com/chenhaox/zotero-pdf-upload)

> 🤖 AI Skill — Let your LLM manage your [Zotero Web Library](https://www.zotero.org) directly: upload PDFs, create items, and match collections.

## ⚙️ Configure

You need two things: a **Zotero API Key** and your **Zotero Library URL**.

### Step 1 — Create a Zotero API Key

1. Log in to [zotero.org](https://www.zotero.org) and click **"Settings"** in the top-right corner.

2. In the Settings page, click **"Security"** in the left sidebar, then scroll down to the **Applications** section and click **"Create new private key"**.

3. Configure the key permissions:
   - **Personal Library**: ✅ Allow library access, ✅ Allow notes access, ✅ Allow write access
   - **Default Group Permissions**: Set to **Read/Write** (if you use group libraries)
   - Click **"Save Key"** to generate your `Zotero_API_Key`

4. **Copy the generated key** — you'll need it below.

### Step 2 — Get your Zotero Library URL

Open your Zotero library in a browser and copy the URL from the address bar:

- **Personal library**: `https://www.zotero.org/<your-username>/library`
- **Group library**: `https://www.zotero.org/groups/<group-id>/<group-name>/library`

For example:
```
# Personal
https://www.zotero.org/chenhaox/library

# Group
https://www.zotero.org/groups/6320165/fafu_robot/library
```

### Step 3 — Run setup

```bash
python scripts/setup.py "<YOUR_LIBRARY_URL>" "<YOUR_API_KEY>"
```

✅ **Done!** Restart your conversation and the LLM will automatically detect and use this skill.

> 💡 Just tell the AI: _"Upload this PDF to my Zotero collection X"_ — it will handle the rest.

---

## 🔧 What it does

- 🔗 Parse Zotero group/user URLs into `libraryType` + `libraryId`
- 📂 List and inspect existing collections
- 🎯 Heuristically match an item to an existing collection
- ✋ Require explicit approval before creating collections/items
- 📝 Create Zotero item metadata
- 📤 Optionally upload/attach a PDF when enabled
- 🔐 Load API key safely from env/path/config precedence

---

## 🛠 For Advanced Users

### 📁 Main scripts

| Script | Description |
|--------|-------------|
| `scripts/setup.py` | ⚡ One-line config generator |
| `scripts/zotero_workflow.py` | 🚀 CLI entrypoint |
| `scripts/zotero_client.py` | 🔌 Zotero API client/utilities |
| `tests/smoke_test_zotero_pdf_upload.py` | 🧪 No-network smoke tests |

### 📖 Detailed Usage

#### 1️⃣ Parse URL

```bash
python scripts/zotero_workflow.py parse-url --url "https://www.zotero.org/groups/123456/my-group/library"
```

#### 2️⃣ List collections (read-only)

```bash
python scripts/zotero_workflow.py list-collections --config config.json
```

#### 3️⃣ Choose collection (read-only)

```bash
python scripts/zotero_workflow.py choose-collection --config config.json --item-json references/item.example.json
```

#### 4️⃣ Create collection (explicit write)

```bash
python scripts/zotero_workflow.py create-collection --config config.json --name "LLM Safety" --approve-create
```

#### 5️⃣ Create item + attach PDF (explicit write)

```bash
python scripts/zotero_workflow.py create-item \
  --config config.json \
  --item-json references/item.example.json \
  --auto-match-collection \
  --attach-pdf /path/to/paper.pdf \
  --approve-write
```

### 🧪 Tests

```bash
python tests/smoke_test_zotero_pdf_upload.py
```

## 📄 License

MIT
