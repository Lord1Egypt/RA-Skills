---
name: tamar-resume-tailor
description: Tailor resumes for specific job applications using the Tamar AI API
metadata: {"openclaw":{"requires":{"bins":["tamar"],"env":["TAMAR_API_KEY"]},"primaryEnv":"TAMAR_API_KEY","install":[{"id":"npm","kind":"node","package":"tamar-cli","bins":["tamar"],"label":"Install Tamar CLI (npm)"}]}}
---

# Tamar Resume Tailoring

Use the `tamar` CLI to tailor resumes for specific job applications via the Tamar API.

## Triggers

Activate when the user says anything like:
- "tailor my resume"
- "customize my resume for"
- "help me apply for this job"
- "make a resume for this role"
- "adapt my resume"
- "target my resume at"

## Prerequisites

- The `tamar` CLI must be installed by the user before using this skill: `npm install -g tamar-cli`
- An API key must be configured. Verify by running `tamar status`. If it fails with "No API key configured", ask the user to run `tamar auth --key <their-key>` (keys are obtained from https://ask-tamar.com → Profile → API Keys)
- Do NOT read or inspect `~/.tamarrc` directly — use `tamar status` to check auth

## Pipeline

### 1. Check if the user has an experience profile

```bash
tamar profile
```

Shows existing profiles with name, role, seniority, skills, and enrichment depth. If a profile exists, use its ID with `tamar tailor --profile <id>` for higher-quality output. If none exists, proceed to step 2.

### 2. Ensure user has a resume uploaded

If the user has a resume file and hasn't uploaded one yet:

```bash
tamar upload <resume-file>
```

### 3. Get the job description

Ask the user for the job description. It can be:
- A URL (LinkedIn, company careers page, etc.)
- A file path — read the file content first
- Pasted text

### 4. Tailor the resume

**IMPORTANT — Input safety:** Never interpolate user-provided strings directly into shell commands. Always write job descriptions or multi-word arguments to a temporary file and pass the file path, or use the `--` separator and single-quote the argument. This prevents shell injection from malicious input.

```bash
# Safe: write JD to a temp file, pass the file
echo '<job description text>' > /tmp/jd.txt
tamar tailor --job /tmp/jd.txt

# Safe: single-quote the argument to prevent shell expansion
tamar tailor --job 'https://example.com/jobs/12345'
```

If the user also provides a resume file and hasn't uploaded before:

```bash
tamar tailor --job /tmp/jd.txt --resume '<resume-file>'
```

### 5. Review the output

The command returns JSON with:
- `id` — the generated resume ID (stored for later commands)
- `quality` — `"enriched"` (has profile) or `"basic"` (resume-only)
- `analysis` — job match analysis
- `changes` — list of changes made

Present the analysis summary conversationally. Highlight key matches and gaps.

### 6. Handle feedback

If the user wants changes:

Write the feedback to a temp file to avoid shell injection:

```bash
echo '<feedback text>' > /tmp/feedback.txt
tamar feedback "$(cat /tmp/feedback.txt)"
```

Or for a specific resume:

```bash
tamar feedback "$(cat /tmp/feedback.txt)" --id '<resume-id>'
```

### 7. Download the result

```bash
tamar download                    # PDF (default)
tamar download --format json      # structured JSON
```

The PDF is saved to the current directory. Tell the user the file path.

## Error Handling

| Error | Action |
|-------|--------|
| `No API key configured` | Guide user to run `tamar auth --key <key>` |
| `401 Invalid or expired` | Prompt to re-run `tamar auth` with a new key |
| `422 Could not parse URL` | Site blocks scraping (common with LinkedIn). Paste the JD text instead |
| `429 Rate limited` | Tell user to wait and retry |
| `402 Plan limit reached` | Direct to https://ask-tamar.com for upgrade |
| Network error / timeout | Check connection. AI calls can take 15–60s — ensure client timeout is ≥120s |

## Quality Notes

- **Enriched** quality (user has an experience profile — check via `tamar profile`) = higher quality tailoring
- **Basic** quality (resume-only, no profile) = still useful but less nuanced
- If user has no profile, suggest building one at https://ask-tamar.com via the interactive Q&A, or use the enrichment API flow

## Example Interaction

```
User: Can you tailor my resume for this job? https://linkedin.com/jobs/12345

Agent: Let me tailor your resume for that role.

[runs: tamar tailor --job 'https://linkedin.com/jobs/12345']

Agent: Done! Here's what I found:
- Quality: enriched (used your experience profile)
- Key alignments: Python, data pipelines, team leadership
- Adjusted: Reframed your experience to emphasize data platform work
- Gaps: Kubernetes — no production experience listed

Want me to tweak anything? I can also download the PDF for you.
```
