---
name: zip-unzip-file-compression-100mb
description: "Zip / Unzip - File Compression < 100MB: Compress/decompress large archives. Use when an agent needs zip / unzip file compression < 100mb, zip unzip file compression 100mb, bundling large datasets or machine learning model files into distributable zip archives, extracting bulk media uploads containing high resolution images or video assets, compressing extensive log file collections for long term storage and archival, unpacking large software distribution packages for automated deployment."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/zip-unzip-file-compression-100mb
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/zip-unzip-file-compression-100mb"}}
---
# Zip / Unzip - File Compression < 100MB

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
High-capacity file compression and decompression utility designed specifically for handling zip and gzip archives ranging from 10MB to 100MB in size. This function complements the standard archive compressor by accepting payloads that exceed typical size limits, supporting up to 500 files per zip archive with built-in path traversal protection for secure extraction. Users can compress multiple files into a single zip archive by providing an array of filenames with base64-encoded content, or compress individual large files using gzip format. Decompression accepts archives via cloud storage file ID or base64 encoding, automatically extracting all contents and uploading each file to cloud storage with secure signed URLs for retrieval. Unlike the standard version, this large-capacity tool always stores outputs to cloud storage rather than returning inline base64 data, ensuring efficient handling of substantial payloads without memory constraints. The function enforces strict size boundaries, rejecting inputs under 10MB (directing users to the standard tool) and over 100MB (recommending file splitting), while automatic budget-based access controls maintain proper file isolation. The Archive Compressor (Large) is essential for workflows involving sizeable datasets, media collections, or bulk file operations that exceed standard compression limits.

## Product Instructions
### Zip / Unzip - File Compression < 100MB

Compress and decompress large files (10MB–100MB) using ZIP or GZIP formats. Output files are uploaded to cloud storage and returned as downloadable signed URLs that expire after 7 days.

**Size range:** Input and output must be between 10MB and 100MB. For files under 10MB, use the standard archive compressor tool.

#### Actions

##### compress

Create a ZIP or GZIP archive from input files.

###### ZIP Compression

Bundle multiple files into a single ZIP archive.

**Required fields:**
- `action` (string): `"compress"`
- `format` (string): `"zip"`
- `files` (array): List of file objects, each containing:
  - `filename` (string): Name/path for the file inside the archive
  - `content_base64` (string): Base64-encoded file content

**Optional fields:**
- `filename` (string): Output archive filename (default: `"archive.zip"`)

**Limits:** Maximum 500 files per archive.

**Example:**
```json
{
  "action": "compress",
  "format": "zip",
  "files": [
    {
      "filename": "report.csv",
      "content_base64": "<base64-encoded content>"
    },
    {
      "filename": "data/records.json",
      "content_base64": "<base64-encoded content>"
    }
  ],
  "filename": "monthly_export.zip"
}
```

**Response includes:** `file_id`, `signed_url`, `signed_url_expires_in`, `size_bytes`

###### GZIP Compression

Compress a single file using GZIP.

**Required fields:**
- `action` (string): `"compress"`
- `format` (string): `"gzip"`
- `input_base64` (string): Base64-encoded file content to compress

**Optional fields:**
- `filename` (string): Output filename (default: `"archive.gz"`)

**Example:**
```json
{
  "action": "compress",
  "format": "gzip",
  "input_base64": "<base64-encoded content>",
  "filename": "database_dump.gz"
}
```

**Response includes:** `file_id`, `signed_url`, `signed_url_expires_in`, `size_bytes`

---

##### decompress

Extract files from a ZIP or GZIP archive. Provide the archive via `file_id` (from a previous upload or tool output) or `input_base64`.

###### ZIP Decompression

Extract all files from a ZIP archive. Each extracted file is uploaded individually.

**Required fields:**
- `action` (string): `"decompress"`
- `format` (string): `"zip"`
- One of:
  - `file_id` (string): File ID of a previously stored archive
  - `input_base64` (string): Base64-encoded ZIP archive

**Example using file_id:**
```json
{
  "action": "decompress",
  "format": "zip",
  "file_id": "abc123def456"
}
```

**Example using base64:**
```json
{
  "action": "decompress",
  "format": "zip",
  "input_base64": "<base64-encoded zip archive>"
}
```

**Response includes:** `file_count` and a `files` array, each entry with `filename`, `size_bytes`, `file_id`, `signed_url`, `signed_url_expires_in`

###### GZIP Decompression

Decompress a single GZIP file.

**Required fields:**
- `action` (string): `"decompress"`
- `format` (string): `"gzip"`
- One of:
  - `file_id` (string): File ID of a previously stored archive
  - `input_base64` (string): Base64-encoded GZIP archive

**Optional fields:**
- `filename` (string): Output filename for the decompressed file (default: `"decompressed"`)

**Example:**
```json
{
  "action": "decompress",
  "format": "gzip",
  "file_id": "abc123def456",
  "filename": "restored_backup.sql"
}
```

**Response includes:** `file_id`, `signed_url`, `signed_url_expires_in`, `size_bytes`

---

#### Common Workflows

1. **Archive and share large datasets:** Compress multiple CSV/JSON files into a single ZIP, then share the signed URL.
2. **Process uploaded archives:** Decompress a ZIP received via `file_id`, process individual files, then re-compress results.
3. **Compress database exports:** GZIP a single large SQL dump or log file for efficient storage.

#### Important Notes

- **Size enforcement:** Both input and output must be between 10MB and 100MB. Files under 10MB should use the standard archive compressor. Files over 100MB must be split first.
- **File limit:** ZIP archives support up to 500 files.
- **Output storage:** Compressed/decompressed files are stored in cloud storage. Signed download URLs expire after 7 days.
- **Path safety:** Filenames in ZIP archives cannot use absolute paths or contain `..` traversal segments.
- **Format default:** If `format` is not specified, it defaults to `"zip"`.

## When To Use
- Use this skill for `Zip / Unzip - File Compression < 100MB` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: zip / unzip   file compression < 100mb, zip unzip file compression 100mb, bundling large datasets or machine learning model files into distributable zip archives, extracting bulk media uploads containing high resolution images or video assets, compressing extensive log file collections for long term storage and archival, unpacking large software distribution packages for automated deployment pipelines, compress, archive format.
- Supported action names: `compress`, `decompress`.

## Use Cases
- Bundling large datasets or machine learning model files into distributable zip archives
- extracting bulk media uploads containing high-resolution images or video assets
- compressing extensive log file collections for long-term storage and archival
- unpacking large software distribution packages for automated deployment pipelines
- creating consolidated backups of sizeable document libraries or project directories
- decompressing substantial data exports from enterprise systems or databases
- packaging large audio file collections or podcast episodes for delivery
- extracting research datasets distributed as compressed archives for analysis workflows
- bundling multiple high-fidelity design assets or CAD files for client handoff
- compressing batch exports of user-generated content for platform migration or backup operations

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `2`.
x402 availability: not enabled for this product.

- `compress` (action slug: `compress`): Create a ZIP or GZIP archive from input files. ZIP supports up to 500 files; GZIP compresses a single file. Input and output must be between 10MB and 100MB. Price: `20` credits. Parameters: `archive_format`, `filename`, `files`, `input_base64`.
- `decompress` (action slug: `decompress`): Extract files from a ZIP or GZIP archive (10-100MB). Provide via file_id or input_base64. All extracted files are uploaded to cloud storage. Price: `20` credits. Parameters: `archive_format`, `file_id`, `filename`, `input_base64`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "zip-unzip-file-compression-100mb"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "zip-unzip-file-compression-100mb"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "zip-unzip-file-compression-100mb"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "zip-unzip-file-compression-100mb"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "zip-unzip-file-compression-100mb"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "zip-unzip-file-compression-100mb"
  }
}
```

## Call This Tool
Product slug: `zip-unzip-file-compression-100mb`

Marketplace page: https://www.agentpmt.com/marketplace/zip-unzip-file-compression-100mb

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Zip--Unzip---File-Compression--100MB",
    "arguments": {
      "action": "compress",
      "archive_format": "zip",
      "filename": "example filename",
      "files": [
        {
          "content_base64": "Draft marketing copy to check for banned phrases.",
          "filename": "example filename"
        }
      ],
      "input_base64": "example input base64"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "zip-unzip-file-compression-100mb",
  "parameters": {
    "action": "compress",
    "archive_format": "zip",
    "filename": "example filename",
    "files": [
      {
        "content_base64": "Draft marketing copy to check for banned phrases.",
        "filename": "example filename"
      }
    ],
    "input_base64": "example input base64"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `compress` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/zip-unzip-file-compression-100mb
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
