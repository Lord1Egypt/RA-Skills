# Tamar Resume Tailor

Use the `tamar` CLI to tailor resumes for specific job applications via the Tamar AI API.

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

This shows existing experience profiles (name, role, seniority, skills, enrichment depth). If a profile exists, note its ID — it gives higher-quality tailoring when passed to `tamar tailor --profile <id>`.

If no profile exists, proceed to step 2.

### 2. Ensure user has a resume uploaded

If the user has a resume file and hasn't uploaded one yet:

```bash
tamar upload <resume-file>
```

Supported formats: PDF, DOCX, TXT.

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

Upload + tailor in one step:

```bash
tamar tailor --job /tmp/jd.txt --resume '<resume-file>'
```

### 5. Review the output

The command returns:
- `quality` — `enriched` (profile available) or `basic` (resume-only)
- `analysis` — job match analysis (mustHaves, strongMatches, gaps, transferableSkills)
- `changes` — list of changes made

Present the analysis conversationally. Highlight key matches and gaps.

### 6. Handle feedback

If the user wants changes:

Write the feedback to a temp file to avoid shell injection:

```bash
echo '<feedback text>' > /tmp/feedback.txt
tamar feedback "$(cat /tmp/feedback.txt)"
```

### 7. Download the result

```bash
tamar download                    # PDF (default)
tamar download --format json      # structured JSON
tamar download --output my.pdf    # custom filename
```

The PDF is saved to the current directory. Tell the user the file path.

## Error Handling

| Error | Action |
|-------|--------|
| `No API key configured` | Run `tamar auth --key <key>` |
| `401 Invalid or expired` | Re-run `tamar auth` with a new key from ask-tamar.com |
| `422 Could not parse URL` | Site blocks scraping (common with LinkedIn). Paste the JD text instead of the URL |
| `429 Rate limited` | Wait and retry — check plan limits |
| `402 Plan limit reached` | Direct to https://ask-tamar.com to upgrade |
| Network error / timeout | Check connection. AI calls can take 15–60s — ensure client timeout is ≥120s |

## Quality Notes

- **Enriched** quality: user has an experience profile (check via `tamar profile`) = higher quality tailoring
- **Basic** quality: resume-only, no profile = still useful but less nuanced
- If basic, suggest building a profile at https://ask-tamar.com for better results, or use the enrichment Q&A flow via the API

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
