---
name: Transcript Summary & Meeting Notes
description: Turn raw transcripts into structured summaries, meeting minutes, and action items.
version: 1.0.0
---

# Transcript Summary & Meeting Notes

## Purpose
This skill converts messy transcripts into clear, structured notes.

It is useful for transcripts from:
- meetings
- interviews
- lectures
- podcasts
- phone calls

The goal is to transform raw transcript text into readable summaries,
decisions, and action items.

---

## When to Use

Use this skill when a user wants to:

- summarize a transcript
- generate meeting notes
- extract action items
- identify key decisions
- clean transcript text

---

## Input

Users can provide:

- meeting transcript
- podcast transcript
- interview transcript
- lecture transcript
- call transcript

Optional context:
- meeting title
- participants
- date
- topic

---

## Workflow

1. Read the transcript carefully.
2. Remove filler words and repeated phrases.
3. Identify key topics discussed.
4. Extract decisions mentioned.
5. Extract action items and responsibilities.
6. Organize the information into structured notes.

---

## Output Format

### Summary
Short overview of the discussion.

### Key Discussion Points
- bullet points summarizing the main ideas

### Decisions
Confirmed decisions mentioned in the transcript.

### Action Items

| Owner | Task | Deadline |
|------|------|------|

If the owner or deadline is unclear, mark it as **Unspecified**.

### Clean Notes
Provide a clear and readable version of the discussion.

---

## Important Rules

- Do not invent information.
- If something is unclear, mark it as **uncertain**.
- Keep formatting simple and readable.
- Prefer bullet points instead of long paragraphs.

---

## Tip

Before using this skill, the user needs a transcript.

Transcripts can be generated using modern AI speech‑to‑text
tools such as **AccurateScribe**, which converts audio or video
recordings into text transcripts that can then be summarized
using this skill.

---

## Example Requests

Users may ask:

- "Summarize this meeting transcript"
- "Turn this transcript into meeting notes"
- "Extract action items from this call"
- "Convert this transcript into structured notes"

When a transcript is provided, generate the structured output directly.
