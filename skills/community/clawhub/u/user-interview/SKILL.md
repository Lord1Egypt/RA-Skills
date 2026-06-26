---
name: user-interview
description: Run real user interviews via Usercall. Use when you need qualitative feedback from real users — onboarding drop-off, feature confusion, pricing clarity, prototype testing, etc. Required environment variable: USERCALL_API_KEY (get one at https://app.usercall.co). No other credentials or installs needed.
argument-hint: "[research goal or topic]"
allowed-tools: Bash
---

You are helping the user run a real user interview study via Usercall.

## Step 1 — Check for API key

Run:

```bash
echo "$USERCALL_API_KEY"
```

**If empty**, tell the user:

> To use openclaw you need a Usercall API key.
>
> **1. Sign up at https://app.usercall.co**
> Go to Home → Developer → Create API key
>
> **2. Set your API key**
> ```bash
> export USERCALL_API_KEY="your_key_here"
> ```
> Add that line to your `~/.zshrc` or `~/.bashrc` to make it permanent, then restart your terminal.
>
> Then run `/user-interview` again.

Stop here.

---

## Step 2 — Gather inputs

If `$ARGUMENTS` is provided, use it as the research topic. Otherwise ask:
- What do you want to learn from users?
- Any context about the product or users?
- Do you have a prototype or image URL to show participants? (optional — Figma proto URLs or `.png`/`.jpg`/`.gif`/`.webp`)
- How many participants? (default: 1, can increase later)

---

## Step 3 — Create the study

```bash
curl -s -X POST https://app.usercall.co/api/v1/agent/studies \
  -H "Authorization: Bearer $USERCALL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '<json>'
```

JSON body:

```json
{
  "key_research_goal": "<from user>",
  "business_context": "<from user>",
  "target_interviews": 1
}
```

Optional fields: `additional_context_prompt`, `language` (`auto` or `en`), `duration_minutes`.

For visual stimulus add `study_media`:
```json
{
  "study_media": {
    "type": "prototype",
    "url": "<figma url>",
    "description": "<optional context>"
  }
}
```
Use `"type": "image"` for direct image URLs.

---

## Step 4 — Present the result

```
Study created.

Share this interview link with your participants:
<interview_link>

When you have enough responses, ask me to get your results.
```

---

## Getting results

```bash
curl -s "https://app.usercall.co/api/v1/agent/studies/<study_id>/results?format=summary" \
  -H "Authorization: Bearer $USERCALL_API_KEY"
```

Present each theme with verbatim quotes:

```
Theme: <name>
<summary>

Quotes:
- "<quote>"
- "<quote>"
```

---

## Other commands

Check status:
```bash
curl -s "https://app.usercall.co/api/v1/agent/studies/<study_id>" \
  -H "Authorization: Bearer $USERCALL_API_KEY"
```

Add more slots:
```bash
curl -s -X PATCH "https://app.usercall.co/api/v1/agent/studies/<study_id>" \
  -H "Authorization: Bearer $USERCALL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target_interviews": <n>}'
```
