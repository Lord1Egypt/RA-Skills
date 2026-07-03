# Claw Local Knowledge

A specialized skill enabling AI Agents to manage a local document knowledge base with semantic search and retrieval capabilities.

## Overview

This skill provides two core functionalities:

| Function | Description |
|----------|-------------|
| **Ingest Knowledge** | Convert user-uploaded documents (docx, pdf, xlsx, pptx) into markdown and store them in the knowledge base |
| **Retrieve Knowledge** | Search and retrieve relevant documents from the knowledge base to assist decision-making |

## Architecture

```
.openclaw/workspace/
├── memory/
│   ├── knowledge_base/              # Converted markdown documents
│   └── knowledge_base_index.json     # Knowledge base index (JSON array)
└── temp_file/                        # Staging area for uploaded files
```

### File Flow

1. User uploads documents → `.openclaw/workspace/temp_file/`
2. Agent converts to markdown → `.openclaw/workspace/memory/knowledge_base/`
3. Agent updates index → `.openclaw/workspace/memory/knowledge_base_index.json`

## Initial Setup

Before first use, initialize the required directory structure:

### Linux / macOS

```bash
# Create knowledge base directory
mkdir -p .openclaw/workspace/memory/knowledge_base

# Create temporary file directory
mkdir -p .openclaw/workspace/temp_file

# Create empty index file
echo '[]' > .openclaw/workspace/memory/knowledge_base_index.json
```

### Windows PowerShell

```powershell
# Create directories
New-Item -ItemType Directory -Path ".openclaw/workspace/memory/knowledge_base" -Force
New-Item -ItemType Directory -Path ".openclaw/workspace/temp_file" -Force

# Create empty index file
Set-Content -Path ".openclaw/workspace/memory/knowledge_base_index.json" -Value "[]"
```

### Configure SOUL.md

If the `SOUL.md` file exists in the OpenClaw workspace, inject the following instructions in the original `SOUL.md` style to enable proactive knowledge retrieval:

```plaintext
## Local Knowledge (claw-local-knowledge skill)
Please attempt to load the **claw-local-knowledge skill** when encountering uncertain or specialized knowledge, and retrieve relevant information according to the instructions.

**Retrieval Process:**
1. Read `memory/knowledge_base_index.json` to obtain the file list.
2. Match relevant files based on keywords.
3. Read the corresponding Markdown files from `memory/knowledge_base/`.
4. Integrate the information and reply to the user.

**Note:**
The knowledge base path is `workspace/memory/knowledge_base/`, and the index file is `workspace/memory/knowledge_base_index.json`.
```

This configuration ensures that the Agent can proactively query the local knowledge base when facing knowledge blind spots.

## Index File Format

The `knowledge_base_index.json` is a JSON array where each entry represents a document:

```json
{
  "name": "document_name.md",
  "description": "Brief summary of the document's content"
}
```

## Supported Input Formats

| Format | Type | Extension |
|--------|------|-----------|
| Word Document | Microsoft Word | `.docx` |
| PDF Document | Portable Document Format | `.pdf` |
| Excel Spreadsheet | Microsoft Excel | `.xlsx` |
| PowerPoint Presentation | Microsoft PowerPoint | `.pptx` |

## Usage Scenarios

- User uploads documents and requests integration into the knowledge base
- Agent requires domain knowledge to assist with user queries
- User inquires about topics covered by existing knowledge base documents
- Agent encounters uncertainty and needs to verify against stored documentation

## Workflow Reference

For detailed workflow instructions, refer to:

- **`references/add_knowledge.md`** — Document ingestion process: conversion, cleaning, indexing
- **`references/retrieval_knowledge.md`** — Knowledge retrieval process: index lookup, content retrieval, integration
