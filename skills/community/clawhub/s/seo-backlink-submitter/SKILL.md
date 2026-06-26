---
name: seo-backlink-submitter
description: |
  Batch submit websites to AI tool directories and SEO directories to earn backlinks.
  Use when: user says "submit site to directories", "SEO backlinks", "submit to SEO directories",
  "submit to AI tool directories", or "directory submission".
  Automatically detects whether directories accept free submissions, with Playwright browser
  automation for form filling.
---

# SEO Backlink Submitter

Batch submits websites to AI tool directories and SEO directories to earn backlinks.

## Data Format

```json
{
  "name": "Site Name",
  "url": "https://example.com",
  "description": "Site description",
  "email": "contact@example.com",
  "category": "Developer Tools",
  "tags": ["AI", "Agents", "Automation"]
}
```

## Execution Flow

### Step 1: Prerequisites

Install Playwright:
```bash
pip install playwright && playwright install chromium
```

### Step 2: Batch Submit

Run `scripts/batch_submit.py`:

```bash
cd .agent/skills/seo-backlink-submitter
python scripts/batch_submit.py \
  --site "https://your-site.com" \
  --data '{"name":"Site Name","url":"https://your-site.com","description":"Description","email":"you@email.com","category":"Developer Tools"}' \
  --directories "references/directories.txt"
```

### Step 3: Check Single Directory

Check if a directory accepts free submissions:

```bash
python scripts/check_directory.py https://aitoolshunt.com/submit
```

### Step 4: Submit to Single Directory

Submit directly to one directory:

```bash
python scripts/quick_submit.py https://aitoolshunt.com/submit \
  --data '{"name":"Name","url":"https://site.com","description":"Desc","email":"you@email.com"}'
```

## Directory List

Located at `references/directories.txt`, includes:
- AI Skills / Agent Skills Marketplaces
- Agent Skills Directories
- AI Tool Directories (ProductHunt, Futurepedia, FutureTools, etc.)
- Developer/Tools Directories (StackShare, DevPost, etc.)
- GitHub Awesome Lists

## Output Format

Results saved as JSON:

| Field | Description |
|-------|-------------|
| directory | Directory name |
| url | Submission page URL |
| status | success / failed / paid / needs_login / error |
| timestamp | Submission time |
| error | Error reason if any |

## Status Meanings

| Status | Meaning |
|--------|---------|
| success | Submitted successfully |
| failed | Submission failed |
| paid | Directory requires payment, skipped |
| needs_login | Login required, skipped |
| error | Unexpected error |

## Notes

- Directories requiring login are marked `needs_login`
- Paid directories are marked `paid` and skipped
- Add 2-5 second delay between directories to avoid rate limits
- Check directory policies periodically as free tiers may become paid
- Submit in batches of 10 or fewer per session

## Dependencies

- Python 3.8+
- playwright (`pip install playwright && playwright install chromium`)
- aiohttp (for async HTTP requests)
