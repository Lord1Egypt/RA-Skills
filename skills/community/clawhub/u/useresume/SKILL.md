---
name: useresume
description: Generate professional PDF resumes and cover letters via the useresume.ai API. Supports creating, tailoring (AI-optimized for a job), and parsing documents.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["USERESUME_API_KEY"], "bins": ["useresume"] },
        "primaryEnv": "USERESUME_API_KEY",
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "formula": "@useresume/cli",
              "bins": ["useresume"],
              "label": "Install @useresume/cli (npm)",
            },
          ],
      },
  }
---

# useresume CLI

Generate professional PDF resumes and cover letters via the useresume.ai API.

## Setup

```bash
npm install -g @useresume/cli
export USERESUME_API_KEY=ur_your_key_here
```

Get an API key at https://useresume.ai/account/api-platform

## Verify credentials

```bash
useresume credentials:test
```

Returns account status on success, including credits and expiry. Invalid keys return JSON with `success: false` and a non-zero exit code.

---

## Commands

All commands output JSON to stdout. All `--input` flags accept a path to a JSON file.

### resume:create (1 credit)

```bash
useresume resume:create --input <path-to-json>
```

**Input JSON schema:**

```json
{
  "content": {
    "name": "string (optional, max 1000)",
    "role": "string (optional, max 1000)",
    "email": "string (optional, max 250)",
    "phone": "string (optional, max 250)",
    "address": "string (optional, max 1000)",
    "photo_url": "string (optional, valid URL, max 2000)",
    "summary": "string (optional, max 5000)",
    "date_of_birth": "string (optional)",
    "marital_status": "string (optional)",
    "nationality": "string (optional)",
    "visa_status": "string (optional)",
    "pronouns": "string (optional)",
    "employment": [
      {
        "title": "string",
        "company": "string",
        "location": "string (optional)",
        "short_description": "string (optional)",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD (optional if present=true)",
        "present": "boolean",
        "responsibilities": [{ "text": "string" }]
      }
    ],
    "education": [
      {
        "degree": "string",
        "institution": "string",
        "location": "string (optional)",
        "short_description": "string (optional)",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD (optional if present=true)",
        "present": "boolean",
        "achievements": [{ "text": "string" }]
      }
    ],
    "skills": [
      {
        "name": "string",
        "proficiency": "Beginner | Intermediate | Advanced | Expert",
        "display_proficiency": "boolean (optional)"
      }
    ],
    "certifications": [
      {
        "name": "string",
        "institution": "string (optional)",
        "start_date": "YYYY-MM-DD (optional)",
        "end_date": "YYYY-MM-DD (optional)",
        "present": "boolean (optional)"
      }
    ],
    "languages": [
      {
        "language": "string",
        "proficiency": "Beginner | Intermediate | Advanced | Fluent",
        "display_proficiency": "boolean (optional)"
      }
    ],
    "references": [
      {
        "name": "string",
        "title": "string (optional)",
        "company": "string (optional)",
        "email": "string (optional)",
        "phone": "string (optional)"
      }
    ],
    "projects": [
      {
        "name": "string",
        "short_description": "string (optional)",
        "start_date": "YYYY-MM-DD (optional)",
        "end_date": "YYYY-MM-DD (optional)",
        "present": "boolean (optional)"
      }
    ],
    "activities": [
      {
        "name": "string",
        "short_description": "string (optional)"
      }
    ],
    "summary_section_name": "string (optional, default 'Summary')",
    "employment_section_name": "string (optional, default 'Employment')",
    "skills_section_name": "string (optional, default 'Skills')",
    "education_section_name": "string (optional, default 'Education')",
    "certifications_section_name": "string (optional)",
    "languages_section_name": "string (optional)",
    "references_section_name": "string (optional)",
    "projects_section_name": "string (optional)",
    "activities_section_name": "string (optional)"
  },
  "style": {
    "template": "TEMPLATE enum (see below)",
    "template_color": "COLOR enum (see below)",
    "font": "FONT enum (see below)",
    "background_color": "BACKGROUND enum (see below, optional)",
    "page_padding": "number 0-2 (optional)",
    "gap_multiplier": "number 0.5-1.5 (optional)",
    "font_size_multiplier": "number 0.8-1.2 (optional)",
    "profile_picture_radius": "rounded-full | rounded-xl | rounded-none (optional)",
    "date_format": "LLL yyyy | LL/yyyy | dd/LL/yyyy | LL/dd/yyyy | dd.LL.yyyy | yyyy (optional)",
    "document_language": "en | es | fr | de | it | pt | nl | pl | lt (optional)",
    "page_format": "a4 | letter (optional)",
    "resume_structure": [
      { "section_id": "string", "position_index": "number 0-25" }
    ]
  }
}
```

### resume:create-tailored (5 credits)

```bash
useresume resume:create-tailored --input <path-to-json>
```

**Input JSON schema:**

```json
{
  "resume_content": {
    "content": { "...same as resume:create content..." },
    "style": { "...same as resume:create style..." }
  },
  "target_job": {
    "job_title": "string (max 250)",
    "job_description": "string (max 10000)"
  },
  "tailoring_instructions": "string (optional, max 2000)"
}
```

### resume:parse (4 credits)

```bash
useresume resume:parse --file-url <url> --parse-to json
useresume resume:parse --file <local-path> --parse-to markdown
```

Provide exactly one of `--file-url` (public URL, max 20MB) or `--file` (local path, auto base64-encoded, max 4MB) — passing both is an error. `--parse-to` is required: `json` returns structured resume data, `markdown` returns text.

### cover-letter:create (1 credit)

```bash
useresume cover-letter:create --input <path-to-json>
```

**Input JSON schema:**

```json
{
  "content": {
    "name": "string (optional, max 1000)",
    "address": "string (optional, max 1000)",
    "email": "string (optional, max 250)",
    "phone": "string (optional, max 250)",
    "text": "string (optional, max 15000) — the main body",
    "hiring_manager_company": "string (optional, max 250)",
    "hiring_manager_name": "string (optional, max 250)",
    "role": "string (optional, max 1000)"
  },
  "style": {
    "template": "CL_TEMPLATE enum (see below)",
    "template_color": "COLOR enum (see below)",
    "font": "FONT enum (see below)",
    "background_color": "BACKGROUND enum (see below, optional)",
    "page_padding": "number 0-2 (optional)",
    "gap_multiplier": "number 0.5-1.5 (optional)",
    "font_size_multiplier": "number 0.8-1.2 (optional)",
    "document_language": "en | es | fr | de | it | pt | nl | pl | lt (optional)",
    "page_format": "a4 | letter (optional)"
  }
}
```

### cover-letter:create-tailored (5 credits)

```bash
useresume cover-letter:create-tailored --input <path-to-json>
```

**Input JSON schema:**

```json
{
  "cover_letter_content": {
    "content": { "...same as cover-letter:create content..." },
    "style": { "...same as cover-letter:create style..." }
  },
  "target_job": {
    "job_title": "string (max 250)",
    "job_description": "string (max 10000)"
  },
  "tailoring_instructions": "string (optional, max 2000)"
}
```

### cover-letter:parse (4 credits)

```bash
useresume cover-letter:parse --file-url <url> --parse-to json
useresume cover-letter:parse --file <local-path> --parse-to markdown
```

Same flags as `resume:parse`. Exactly one of `--file-url` or `--file` is required.

### run:get (0 credits)

```bash
useresume run:get <run-id>
```

Returns the status of a previous run. Response includes `status`: `"success"`, `"error"`, or `"in_progress"`.

### credentials:test (0 credits)

```bash
useresume credentials:test
```

Tests API key validity and returns account status including available credits and key expiry. Use this before expensive operations to check if the account can afford the call.

**Response:**

```json
{
  "success": true,
  "data": {
    "api_platform_user_id": "user_abc",
    "api_credits": 96,
    "expires_at": "2026-12-31T00:00:00Z"
  }
}
```

**Invalid key / unauthorized response:**

```json
{
  "success": false,
  "data": {
    "valid": false,
    "status": 401,
    "message": "Unauthorized"
  }
}
```

---

## Enums

### TEMPLATE (resume, 29 options)

`default`, `clean`, `classic`, `executive`, `modern-pro`, `meridian`, `horizon`, `atlas`, `prism`, `nova`, `zenith`, `vantage`, `summit`, `quantum`, `vertex`, `harvard`, `lattice`, `strata`, `cascade`, `pulse`, `folio`, `ridge`, `verso`, `ledger`, `tableau`, `apex`, `herald`, `beacon`, `onyx`

### CL_TEMPLATE (cover letter, 11 options)

`atlas`, `classic`, `clean`, `default`, `executive`, `horizon`, `meridian`, `modern-pro`, `nova`, `prism`, `zenith`

### COLOR (32 options)

`blue`, `black`, `emerald`, `purple`, `rose`, `amber`, `slate`, `indigo`, `teal`, `burgundy`, `forest`, `navy`, `charcoal`, `plum`, `olive`, `maroon`, `steel`, `sapphire`, `pine`, `violet`, `mahogany`, `sienna`, `moss`, `midnight`, `copper`, `cobalt`, `crimson`, `sage`, `aqua`, `coral`, `graphite`, `turquoise`

### FONT (9 options)

`geist`, `inter`, `merryweather`, `roboto`, `playfair`, `lora`, `jost`, `manrope`, `ibm-plex-sans`

### BACKGROUND (16 options)

`white`, `cream`, `pearl`, `mist`, `smoke`, `ash`, `frost`, `sage`, `mint`, `blush`, `lavender`, `sky`, `sand`, `stone`, `linen`, `ivory`

### SECTION_ID (for resume_structure)

`summary`, `employment`, `skills`, `education`, `certifications`, `languages`, `references`, `projects`, `activities`, or a custom string for any custom sections

---

## Response Formats

### Create response

```json
{
  "success": true,
  "data": {
    "file_url": "https://...",
    "file_url_expires_at": 1234567890,
    "file_expires_at": 1234567890,
    "file_size_bytes": 54321
  },
  "meta": {
    "run_id": "run_abc123",
    "credits_used": 1,
    "credits_remaining": 95
  }
}
```

### Parse response (json)

```json
{
  "success": true,
  "data": { "...structured resume/cover letter object..." },
  "meta": { "run_id": "...", "credits_used": 4, "credits_remaining": 91 }
}
```

### Parse response (markdown)

```json
{
  "success": true,
  "data": "# Jane Doe\n\n## Summary\n...",
  "meta": { "run_id": "...", "credits_used": 4, "credits_remaining": 91 }
}
```

### Run status response

```json
{
  "success": true,
  "data": {
    "id": "run_abc123",
    "status": "success | error | in_progress",
    "endpoint": "/resume/create",
    "credits_used": 1,
    "file_url": "https://...",
    "file_url_expires_at": 1234567890,
    "file_expires_at": 1234567890,
    "file_size_bytes": 54321,
    "created_at": 1234567890
  }
}
```

### Error response

```json
{
  "success": false,
  "error": {
    "code": "HTTP_401",
    "message": "useResume API Error: ..."
  }
}
```

---

## Common Agent Workflows

### 0. Check budget before calling

```bash
useresume credentials:test
# Read .data.api_credits — compare against the cost of your next command
# If credits < cost, tell the user to top up at https://useresume.ai/account/api-platform
```

### 1. Create a resume from user data

```bash
# 1. Write the JSON input to a temp file
cat > /tmp/resume.json << 'EOF'
{ "content": { "name": "...", ... }, "style": { "template": "clean", "template_color": "blue", "font": "inter" } }
EOF

# 2. Generate the PDF
useresume resume:create --input /tmp/resume.json
# Returns JSON with file_url to the PDF
```

### 2. Parse an existing resume, tailor it for a job

```bash
# 1. Parse to get structured data
useresume resume:parse --file ./existing-resume.pdf --parse-to json
# Save the returned data.content

# 2. Use parsed data + job description to create a tailored version
cat > /tmp/tailored.json << 'EOF'
{
  "resume_content": { "content": { ...parsed data... }, "style": { "template": "clean", "template_color": "navy", "font": "inter" } },
  "target_job": { "job_title": "Senior Engineer", "job_description": "..." }
}
EOF
useresume resume:create-tailored --input /tmp/tailored.json
```

### 3. Poll for async completion

Some operations may return `in_progress`. Poll with:

```bash
useresume run:get <run-id>
# Check .data.status — repeat until "success" or "error"
```

---

## Credit Costs

| Command                        | Credits |
| ------------------------------ | ------- |
| `resume:create`                | 1       |
| `resume:create-tailored`       | 5       |
| `resume:parse`                 | 4       |
| `cover-letter:create`          | 1       |
| `cover-letter:create-tailored` | 5       |
| `cover-letter:parse`           | 4       |
| `run:get`                      | 0       |
| `credentials:test`             | 0       |
