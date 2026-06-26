---
name: tc-protohub
description: 在 ProtoHub 上管理原型。当用户想要上传目录或 ZIP 文件作为原型、更新现有原型、列出原型或获取预览链接时，请使用此技能。它支持自动打包文件夹、强制校验入口文件 (index.html)，以及按名称搜索原型以便更新。
---

# Skill: ProtoHub AI Agent Integration

## Purpose
This skill allows AI Agents to manage prototypes on ProtoHub. It provides automated tools for packaging, publishing, and discovering prototypes (folders or ZIP files) in the ProtoHub Private Sandbox.

## Capabilities
- **Automated Publishing:** Package a directory or use a ZIP file to create/update prototypes.
- **Entry Point Validation:** Automatically checks for `index.html` before uploading.
- **Prototype Discovery:** List existing prototypes or search by name to find IDs.
- **Preview Management:** Retrieve public URLs for demonstration.

## Mandatory Configuration
Before performing any action, the AI Agent MUST verify that the following environment variables are set:
- `PROTOHUB_API_KEY`: Required for authentication.
- `PROTOHUB_URL`: Base URL of the ProtoHub server (default: `http://localhost:48080`).

**Strict Validation Rule:**
If either of these is missing from the environment and has not been provided by the user in the current session, the Agent **MUST NOT** attempt to run the script and **MUST NOT** retry with placeholder values. Instead, immediately ask the user to provide the missing configuration.

### How to set:
```bash
export PROTOHUB_API_KEY="your-api-key"
export PROTOHUB_URL="http://localhost:48080"
```

## Recommended Tool: publish.py

### Usage Examples

#### 1. Upload a Directory as a New Prototype
```bash
python skills/tc-protohub/scripts/publish.py publish ./my-dist-folder --name "My Prototype Name"
```

#### 2. Update an Existing Prototype
Overwrites content while maintaining the same ID and URL.
```bash
python skills/tc-protohub/scripts/publish.py publish ./my-dist-folder --id 1024
```

#### 3. List Prototypes (Search by Name)
Useful for finding the ID when the user says "Update the 'Login Page' prototype".
```bash
python skills/tc-protohub/scripts/publish.py list --name "Login Page"
```

#### 4. Get Preview Link
```bash
python skills/tc-protohub/scripts/publish.py get-link 1024
```

## Best Practices
- **Folder Structure:** Ensure `index.html` is at the root of your directory or ZIP file.
- **Intelligent Updating:** 
  - If the user asks to "update" a prototype but doesn't provide an ID, use `publish.py list --name "..."` to find a matching prototype first. 
  - If exactly one match is found, use its ID to perform the update.
  - If multiple or no matches are found, ask the user for clarification or create a new one.
- **API Base URL:** Default is `http://localhost:48080`. Override using the `PROTOHUB_URL` env var or `--url` flag.
- **Error Handling:** 
  - `401 Unauthorized`: API Key is missing or invalid.
  - `404 Not Found`: The specified `prototypeId` does not exist.
  - `Missing index.html`: The script will abort the upload to prevent broken previews.
