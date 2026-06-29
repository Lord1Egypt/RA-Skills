---
name: zip-unzip-file-compression-10mb
description: "Zip / Unzip - File Compression < 10MB: Compress/decompress zip and gzip. Use when an agent needs zip / unzip file compression < 10mb, zip unzip file compression 10mb, bundling multiple generated reports or documents into a single downloadable zip file, extracting uploaded zip archives to process individual files in automated workflows, compressing json or csv data exports for efficient storage and transfer, unpacking user submitted archives to validate and scan contained files, compress."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/zip-unzip-file-compression-10mb
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/zip-unzip-file-compression-10mb"}}
---
# Zip / Unzip - File Compression < 10MB

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
File compression and decompression utility that handles zip and gzip formats for archives up to 10MB in size. This function supports two primary actions: compress and decompress, allowing users to bundle multiple files into a single zip archive or compress individual files using gzip, as well as extract contents from existing archives. For zip compression, users provide an array of files with filenames and base64-encoded content, supporting up to 200 files per archive with built-in path traversal protection for security. For gzip operations, users supply a single base64-encoded input along with an optional filename. Decompression accepts archives via base64 encoding or cloud storage file ID, automatically extracting all contents and optionally returning each file's base64 data inline for immediate processing. Extracted files and generated archives are stored in cloud storage with secure signed URLs for convenient access, and users can toggle the include_contents option to receive base64 output directly in the response. With automatic size validation and budget-based access controls, the Archive Compressor provides a reliable solution for standard file bundling and extraction workflows within agent pipelines.

## Product Instructions
### Zip / Unzip - File Compression < 10MB

Compress and decompress files using ZIP or GZIP formats. Handles archives up to 10MB with up to 200 files. Output files are stored in cloud storage for 7 days by default.

#### Actions

##### compress

Create a ZIP or GZIP archive from input files.

###### ZIP Compression

**Required fields:**
- `action`: `"compress"`
- `format`: `"zip"`
- `files`: Array of file objects, each with:
  - `filename` (string) - Name/path for the file inside the archive
  - `content_base64` (string) - Base64-encoded file content

**Optional fields:**
- `filename` (string) - Name for the output ZIP file (default: `"archive.zip"`)
- `store_file` (boolean) - Store output in cloud storage (default: `true`)
- `include_contents` (boolean) - Include base64 of the archive in the response (default: `false`)

**Example:**
```json
{
  "action": "compress",
  "format": "zip",
  "files": [
    {"filename": "report.txt", "content_base64": "SGVsbG8gV29ybGQ="},
    {"filename": "data/notes.csv", "content_base64": "bmFtZSxhZ2UKQWxpY2UsMzA="}
  ],
  "filename": "my_reports.zip"
}
```

###### GZIP Compression

Compresses a single file using GZIP.

**Required fields:**
- `action`: `"compress"`
- `format`: `"gzip"`
- `input_base64` (string) - Base64-encoded content of the file to compress

**Optional fields:**
- `filename` (string) - Name for the output file (default: `"archive.gz"`)
- `store_file` (boolean) - Store output in cloud storage (default: `true`)
- `include_contents` (boolean) - Include base64 of the compressed output in the response (default: `false`)

**Example:**
```json
{
  "action": "compress",
  "format": "gzip",
  "input_base64": "TGFyZ2UgdGV4dCBmaWxlIGNvbnRlbnQgaGVyZS4u",
  "filename": "logfile.txt.gz"
}
```

---

##### decompress

Extract files from a ZIP or GZIP archive.

###### ZIP Decompression

**Required fields:**
- `action`: `"decompress"`
- `format`: `"zip"`
- One of:
  - `input_base64` (string) - Base64-encoded ZIP archive
  - `file_id` (string) - File ID of a previously stored ZIP archive

**Optional fields:**
- `store_file` (boolean) - Store each extracted file in cloud storage (default: `true`)
- `include_contents` (boolean) - Include base64 content of each extracted file in the response (default: `false`)

**Example using base64 input:**
```json
{
  "action": "decompress",
  "format": "zip",
  "input_base64": "UEsDBBQAAAAI...",
  "include_contents": true
}
```

**Example using file_id:**
```json
{
  "action": "decompress",
  "format": "zip",
  "file_id": "abc123def456"
}
```

###### GZIP Decompression

**Required fields:**
- `action`: `"decompress"`
- `format`: `"gzip"`
- One of:
  - `input_base64` (string) - Base64-encoded GZIP file
  - `file_id` (string) - File ID of a previously stored GZIP file

**Optional fields:**
- `filename` (string) - Name for the decompressed output file (default: `"decompressed"`)
- `store_file` (boolean) - Store the decompressed file in cloud storage (default: `true`)
- `include_contents` (boolean) - Include base64 of the decompressed content in the response (default: `false`)

**Example:**
```json
{
  "action": "decompress",
  "format": "gzip",
  "file_id": "abc123def456",
  "filename": "restored_log.txt"
}
```

---

#### Common Workflows

##### Bundle multiple files for download
1. Call `compress` with `format: "zip"` and an array of files.
2. Use the returned `signed_url` to share or download the archive.

##### Extract and inspect an uploaded archive
1. Call `decompress` with the `file_id` of the uploaded archive.
2. Each extracted file gets its own `file_id` and `signed_url` for individual access.

##### Compress and retrieve inline
1. Call `compress` with `include_contents: true` and `store_file: false` to get the archive as base64 in the response without storing it.

---

#### Important Notes

- **Size limit:** Total input and output must each be under 10MB. For larger files, use the large archive tool.
- **File count limit:** ZIP archives support up to 200 files.
- **Storage:** Output files are stored in cloud storage for 7 days by default when `store_file` is `true`.
- **ZIP format** supports multiple files; **GZIP format** compresses a single file.
- The response includes `file_id` and `signed_url` for each stored file.
- When decompressing a ZIP, the response includes a `files` array with details for each extracted file.

## When To Use
- Use this skill for `Zip / Unzip - File Compression < 10MB` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: zip / unzip   file compression < 10mb, zip unzip file compression 10mb, bundling multiple generated reports or documents into a single downloadable zip file, extracting uploaded zip archives to process individual files in automated workflows, compressing json or csv data exports for efficient storage and transfer, unpacking user submitted archives to validate and scan contained files, compress, archive format.
- Supported action names: `compress`, `decompress`.

## Use Cases
- Bundling multiple generated reports or documents into a single downloadable zip file
- extracting uploaded zip archives to process individual files in automated workflows
- compressing JSON or CSV data exports for efficient storage and transfer
- unpacking user-submitted archives to validate and scan contained files
- creating backup bundles of configuration files or logs for archival
- decompressing gzipped API responses or data feeds for parsing
- packaging multi-file code outputs or assets for delivery to end users
- reducing payload sizes for base64 data transfers between pipeline stages
- extracting email attachments from compressed formats for content analysis
- preparing batched file uploads by compressing multiple assets into a single archive for downstream systems

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `2`.
x402 availability: not enabled for this product.

- `compress` (action slug: `compress`): Create a ZIP or GZIP archive from input files. ZIP supports up to 200 files; GZIP compresses a single file. Maximum total size is 10MB. Price: `10` credits. Parameters: `archive_format`, `filename`, `files`, `include_contents`, `input_base64`, `store_file`.
- `decompress` (action slug: `decompress`): Extract files from a ZIP or GZIP archive provided via base64 or file ID. Extracted files are stored in cloud storage. Price: `10` credits. Parameters: `archive_format`, `file_id`, `filename`, `include_contents`, `input_base64`, `store_file`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "zip-unzip-file-compression-10mb"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "zip-unzip-file-compression-10mb"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "zip-unzip-file-compression-10mb"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "zip-unzip-file-compression-10mb"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "zip-unzip-file-compression-10mb"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "zip-unzip-file-compression-10mb"
  }
}
```

## Call This Tool
Product slug: `zip-unzip-file-compression-10mb`

Marketplace page: https://www.agentpmt.com/marketplace/zip-unzip-file-compression-10mb

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
    "name": "Zip--Unzip---File-Compression--10MB",
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
      "include_contents": false,
      "input_base64": "example input base64",
      "store_file": true
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "zip-unzip-file-compression-10mb",
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
    "include_contents": false,
    "input_base64": "example input base64",
    "store_file": true
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
- Marketplace product: https://www.agentpmt.com/marketplace/zip-unzip-file-compression-10mb
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
