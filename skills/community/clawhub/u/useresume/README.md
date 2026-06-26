# @useresume/cli

CLI for AI-powered resume and cover letter generation via [useresume.ai](https://useresume.ai) — built for OpenClaw agents.

## Install

```bash
npm install -g @useresume/cli
```

## Setup

```bash
export USERESUME_API_KEY=ur_your_key_here
```

Get your API key at [useresume.ai/account/api-platform](https://useresume.ai/account/api-platform).

## Commands

All commands output JSON to stdout.

### Resume

```bash
# Create a resume (1 credit)
useresume resume:create --input resume.json

# Create a tailored resume for a specific job (5 credits)
useresume resume:create-tailored --input tailored.json

# Parse an existing resume file (4 credits)
useresume resume:parse --file-url "https://example.com/resume.pdf" --parse-to json
useresume resume:parse --file ./resume.pdf --parse-to markdown
```

### Cover Letter

```bash
# Create a cover letter (1 credit)
useresume cover-letter:create --input cover-letter.json

# Create a tailored cover letter for a specific job (5 credits)
useresume cover-letter:create-tailored --input tailored-cl.json

# Parse an existing cover letter file (4 credits)
useresume cover-letter:parse --file-url "https://example.com/cl.pdf" --parse-to json
useresume cover-letter:parse --file ./cover-letter.pdf --parse-to markdown
```

### Utility

```bash
# Check status of an async run (0 credits)
useresume run:get <run-id>

# Test your API key (0 credits)
useresume credentials:test
```

## JSON Input Format

### resume:create

```json
{
  "content": {
    "name": "Jane Doe",
    "role": "Software Engineer",
    "email": "jane@example.com",
    "summary": "Experienced software engineer...",
    "employment": [
      {
        "title": "Senior Engineer",
        "company": "Acme Corp",
        "start_date": "2020-01-01",
        "present": true,
        "responsibilities": [{ "text": "Led team of 5 engineers" }]
      }
    ],
    "education": [],
    "skills": [{ "name": "TypeScript", "proficiency": "Expert" }]
  },
  "style": {
    "template": "clean",
    "template_color": "blue",
    "font": "inter"
  }
}
```

### resume:create-tailored

```json
{
  "resume_content": {
    "content": { "...same as resume:create content..." },
    "style": { "...same as resume:create style..." }
  },
  "target_job": {
    "job_title": "Senior Frontend Engineer",
    "job_description": "We are looking for..."
  },
  "tailoring_instructions": "Emphasize React experience"
}
```

## Response Format

All commands return JSON with this structure:

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

## Output Contract

All commands output **JSON to stdout** — including errors. This is critical for agent consumption:

- Success and error JSON always goes to **stdout** (never stderr)
- Non-zero exit code on failure
- yargs parse errors are also JSON: `{ "success": false, "error": { "code": "CLI_ERROR", "message": "..." } }`
- API errors use the SDK's `UseResumeError.status` directly: `{ "code": "HTTP_401", "message": "..." }`
- `credentials:test` returns account status on success, and `{ "success": false, "data": { "valid": false, ... } }` with a non-zero exit code on invalid credentials

## OpenClaw / ClawHub

This CLI includes a `SKILL.md` for discovery by OpenClaw agents. Install via ClawHub:

```bash
openclaw skills install useresume
```

Or place the skill folder in `~/.openclaw/skills/useresume/` manually.

See [SKILL.md](./SKILL.md) for the full agent-readable spec.

## License

MIT
