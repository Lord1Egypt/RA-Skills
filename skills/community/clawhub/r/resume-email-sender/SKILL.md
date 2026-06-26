---
name: resume-email-sender
description: Send resume and cover letter to companies via Gmail. Activate when user wants to send, deliver, or submit a resume by email, apply to a job, or email a company about a position. Uses gog Gmail tool to compose and send professional job application emails with resume attached.
metadata: {"openclaw": {"emoji": "📨", "requires": {"bins": ["gog"]}}}
---

# Resume Email Sender

Sends professional job application emails with resume via Gmail (`gog` tool).

## Prerequisites

The `gog` skill must be installed and Gmail authenticated:
```bash
gog auth add you@gmail.com --services gmail
```

## When to Activate

- User says "发送简历"、"投递简历"、"apply to job"、"email my resume"
- User provides a company email and wants to apply
- User wants to send a cover letter + resume to a recruiter

## Required Information (ask if missing)

Before sending, collect:
1. **Recipient email** — HR or recruiter address
2. **Company name** — for personalizing the email
3. **Job title** — role they're applying for
4. **Sender name** — applicant's name
5. **Resume content** — already optimized (from resume-optimizer skill)
6. **Cover letter** — optional, generate one if not provided

## Workflow

### Step 1: Confirm details with user

Always show a preview before sending:

```
📋 Application Summary
To: hr@company.com
Subject: Application for [Job Title] — [Your Name]
Company: [Company Name]

[Email preview...]

Send this email? (yes/no)
```

### Step 2: Generate cover letter (if not provided)

Use this template, personalized to the role:

```
Subject: Application for [Job Title] — [Your Name]

Dear Hiring Manager / Dear [Name if known],

I am writing to express my interest in the [Job Title] position at [Company].
With [X] years of experience in [relevant area], I am confident I can 
[specific contribution matching job requirements].

In my current/previous role at [Company], I [key achievement relevant to role].
I am particularly drawn to [Company] because [specific reason — product, mission, 
culture — research this if possible].

I have attached my resume for your review. I would welcome the opportunity to 
discuss how my background aligns with your team's needs.

Thank you for your time and consideration.

Best regards,
[Name]
[Phone] | [LinkedIn] | [Email]
```

### Step 3: Send via gog

Write email body to temp file then send:

```bash
# Write body to temp file (avoids newline issues)
cat > /tmp/job_application_email.txt << 'EOF'
[email body here]
EOF

# Send the email
gog gmail send \
  --to "hr@company.com" \
  --subject "Application for Software Engineer — Jane Smith" \
  --body-file /tmp/job_application_email.txt \
  --account you@gmail.com
```

### Step 4: Log the application

After sending, record it in the job search tracker:

```
✅ Sent: [Company] — [Job Title]
📅 Date: [today's date]
📧 To: [recipient email]
📌 Status: Applied
```

Ask the user if they want to save this to their job search log file (`~/job-search-log.md`).

## Email Etiquette Rules

- **Subject format**: `Application for [Job Title] — [Full Name]`
- **Salutation**: Use "Dear [Name]" if known; "Dear Hiring Manager" if not
- **Length**: Cover letter ≤ 250 words; concise and specific
- **Tone**: Professional but not stiff; match company culture if known (startup vs bank)
- **Attachments note**: Mention "I have attached my resume" even if sending inline (no actual file attachment via gog — paste resume as plain text at bottom or in separate follow-up)
- **Follow-up**: Suggest following up in 5–7 business days if no response

## Batch Sending (multiple companies)

If user wants to send to multiple companies:
1. Confirm the list first (show all recipients + subjects)
2. Personalize each email (company name, role, specific reason)
3. Send one by one with confirmation between each
4. Never send bulk/identical emails — always personalize

## Error Handling

- If `gog` not found: guide user to install with `brew install steipete/tap/gogcli`
- If not authenticated: run `gog auth add [email] --services gmail`
- If send fails: save draft instead with `gog gmail drafts create ...`
