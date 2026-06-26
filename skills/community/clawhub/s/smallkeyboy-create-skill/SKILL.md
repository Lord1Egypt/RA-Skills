---
name: create-skill
description: A callable skill factory for programmatic skill creation. Use when another skill needs to create a new skill, or when automating skill generation workflows. Accepts structured parameters (name, description, instructions, resources) and generates a complete, validated skill package. Triggers on programmatic calls from other skills or automation workflows that need to spawn new skills.
---

# Create Skill

A callable skill factory designed for programmatic invocation by other skills.

## Usage

This skill is typically called by other skills with structured parameters. Call it when you need to generate a new skill programmatically.

### Parameters

When calling this skill, provide the following parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Skill name (lowercase, hyphens only, <64 chars) |
| `description` | Yes | Skill description for frontmatter (include what it does + when to use) |
| `instructions` | Yes | Markdown body content for SKILL.md |
| `scripts` | No | List of script files to create: `[{name, content, language}]` |
| `references` | No | List of reference docs: `[{name, content}]` |
| `assets` | No | List of asset files: `[{name, content}]` |
| `output_dir` | No | Output directory (default: `~/.openclaw/workspace/skills`) |
| `validate` | No | Run validation after creation (default: true) |
| `package` | No | Generate .skill file after creation (default: true) |

### Calling Convention

```
Call this skill with a structured request:

{
  "name": "my-skill",
  "description": "Brief description of what this skill does and when to use it.",
  "instructions": "## Overview\n\nDetailed instructions in markdown...",
  "scripts": [
    {"name": "main.py", "content": "#!/usr/bin/env python3\n...", "language": "python"}
  ],
  "references": [
    {"name": "api-docs.md", "content": "# API Reference\n..."}
  ]
}
```

## Workflow

1. **Validate parameters** - Check skill_name format, required fields
2. **Create directory structure** - `skill_name/` with appropriate subdirectories
3. **Generate SKILL.md** - Write frontmatter + instructions
4. **Create resources** - Write scripts, references, assets if provided
5. **Validate** - Run skill validation (optional, default: on)
6. **Package** - Generate .skill file (optional, default: on)
7. **Return result** - Report created files and location

## Output

Returns a result object:

```json
{
  "success": true,
  "skill_path": "~/.openclaw/workspace/skills/my-skill",
  "skill_file": "~/.openclaw/workspace/skills/my-skill.skill",
  "files_created": ["SKILL.md", "scripts/main.py"]
}
```

## Quick Example

A calling skill might invoke this with:

```
Create a skill named "pdf-watermarker" that:
- Description: "Add watermarks to PDF files. Use when processing PDFs for branding or security."
- Instructions: Basic watermarking workflow with pdfplumber
- Scripts: A watermark.py script using PyPDF2
```

The skill factory handles all file creation, validation, and packaging.

## Resources

### scripts/

- `create_skill.py` - Main skill creation script
- `validate_skill.py` - Validation utilities (wraps skill-creator's package_skill.py)

### references/

- `skill-spec.md` - AgentSkills specification reference
