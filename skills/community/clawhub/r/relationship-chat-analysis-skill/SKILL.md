---
name: relationship-chat-analysis
description: Use this skill only when the user explicitly provides, uploads, pastes, or identifies specific relationship chat records and asks for evidence-based analysis of those records. It handles long, messy exports from LINE, WhatsApp, Telegram, iMessage, Messenger, Discord, SMS, or similar platforms by cleaning noise, segmenting episodes, and analyzing communication patterns, conflict cycles, emotional bids, repair attempts, avoidance, boundaries, effort balance, intimacy signals, safety concerns, and blind spots. Do not trigger for ordinary relationship advice, short sentiment checks, or broad questions unless the user has intentionally supplied chat data for analysis.
---

# Relationship Chat Analysis

Analyze long, noisy relationship chat histories to identify interaction patterns, emotional dynamics, conflict cycles, repair attempts, effort balance, and blind spots. The output is an evidence-grounded report that distinguishes observable facts from cautious interpretation.

## Privacy And Consent

Relationship chats can contain intimate content, abuse disclosures, sexual content, phone numbers, addresses, third-party details, and other sensitive identifiers. Before processing, confirm that the user intended to provide the specific chat records being analyzed.

Do not scan the workspace, home directory, downloads folder, or broad file trees looking for chat logs. Use only files the user explicitly names, attaches, pastes, or asks you to inspect.

Before writing any report or manifest to disk, tell the user the planned output paths and that local files may persist in backups, sync services, search indexes, or later processes. Write files only after the user agrees, unless they already explicitly requested file output.

Default to data minimization:

- Do not include raw full chat logs in generated artifacts.
- Redact unnecessary phone numbers, handles, addresses, third-party names, and other identifiers.
- Quote only short excerpts needed to support findings.
- Prefer a redacted manifest with metadata and quality notes over storing all normalized messages.

## When To Use

Use this skill for:

- Long romantic, dating, breakup, reconciliation, or ambiguous relationship chat histories
- LINE, WhatsApp, Telegram, iMessage, Messenger, Discord, Instagram DM, SMS, or exported text logs
- Messy chat records containing system messages, media placeholders, stickers, duplicated content, deleted messages, or unrelated material
- Requests to understand patterns across weeks or months, not just summarize one exchange
- Analysis of conflict escalation, coldness, distance, mixed signals, emotional needs, repair attempts, boundaries, control, validation, invalidation, or effort imbalance

Do not use this skill for ordinary sentiment classification of short text, legal conclusions, clinical diagnosis, or deciding whether someone "definitely" has a disorder. If the chat contains threats, coercion, stalking, physical danger, self-harm, or sexual pressure, flag the safety concern and keep the analysis grounded in the text.

## Inputs

Expected inputs can include:

- One or more explicitly identified exported chat files
- Manually pasted chat logs
- Screenshots that have already been transcribed into text
- Optional context from the user, such as relationship status, date range, participant names, or what question they want answered

If the export format is unknown, infer the structure conservatively and ask for clarification only when speaker/date attribution would be too unreliable.

## Workflow

1. Read `config.json`.
2. Confirm the user has intentionally supplied or identified the chat records to analyze.
3. Read `references/instructions.md` for the full orchestration procedure.
4. Use `references/cleaning-prompt.md` to normalize and filter noisy chat records with data minimization.
5. Use `references/extraction-prompt.md` for episode-level relationship pattern extraction.
6. Use `references/synthesis-prompt.md` for cross-episode relationship synthesis.
7. Use `references/blindspot-prompt.md` for blind spots, unsupported claims, and safety concerns.
8. Produce file output only with user consent or an explicit file-output request.

## Core Behavior

- Preserve both participants' messages. Do not reduce the analysis to only one person's perspective.
- Ground every major claim in dated examples or message quotes when available.
- Separate `observation`, `interpretation`, and `uncertainty`.
- Avoid diagnosis, mind-reading, moral verdicts, or manipulative certainty.
- Treat missing context as missing context. Do not fill gaps with a story that the messages do not support.
- Identify patterns across repeated episodes rather than over-weighting one heated message.
- Keep original-language quotes when useful and translate only for clarity.
- Protect privacy: do not expose unnecessary third-party names, phone numbers, addresses, handles, or sensitive identifiers in the final report.

## Output

Default file output, when the user consents:

- Analysis document: `relationship-analysis/YYYYMMDD-relationship-chat-analysis.md`
- Optional redacted corpus manifest: `relationship-analysis/YYYYMMDD-chat-corpus-manifest.json`

The final report should include a timeline, communication pattern analysis, conflict and repair cycles, emotional needs, effort balance, blind spots for each side, safety concerns if present, and a section listing what the evidence does not support. The report should not contain full raw chat history.

## Bundled References

- `references/instructions.md`: detailed implementation guide
- `references/cleaning-prompt.md`: chat normalization and noise filtering
- `references/extraction-prompt.md`: episode-level relationship pattern extraction
- `references/synthesis-prompt.md`: cross-episode synthesis
- `references/blindspot-prompt.md`: blind spots, unsupported claims, and safety review
