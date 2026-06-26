# Relationship Chat Analysis Implementation Instructions

You are running the Relationship Chat Analysis skill. The goal is to turn messy chat history into an evidence-grounded relationship dynamics report.

## Constants

```text
CONFIG_FILE = config.json
CLEANING_PROMPT = references/cleaning-prompt.md
EXTRACTION_PROMPT = references/extraction-prompt.md
SYNTHESIS_PROMPT = references/synthesis-prompt.md
BLINDSPOT_PROMPT = references/blindspot-prompt.md
OUTPUT_FOLDER = relationship-analysis
```

## Operating Principles

- Preserve both participants' messages unless the user explicitly asks to analyze only one side.
- Process only chat records the user explicitly provides, attaches, pastes, or names.
- Do not scan broad folders, the whole workspace, downloads, home directories, or unrelated file trees looking for possible chat logs.
- Before writing reports or manifests to disk, disclose the output paths and get consent unless the user already requested file output.
- Minimize retention: do not store raw full chat logs in generated artifacts by default.
- Do not diagnose, label, or claim hidden motives as fact.
- Every major conclusion should cite repeated evidence or clearly state that it is tentative.
- Treat missing messages, deleted messages, screenshots without timestamps, and one-sided exports as data quality issues.
- Redact unnecessary private identifiers in final output and generated manifests.
- If safety concerns appear, name the observable behavior and evidence without exaggeration.

## Step 0: Understand Request And Load Config

Infer the user's analysis intent from natural language. Common request types include:

- A full relationship chat analysis.
- A corpus-quality check before full analysis.
- A date-limited analysis, such as "January to March 2026".
- A focused analysis of conflict repair, coldness, mixed signals, breakup, reconciliation, emotional needs, boundaries, or effort balance.

Read `config.json`.

Tell the user when local configuration is being used. Treat `config.json` as non-secret settings; if it appears to contain credentials or unrelated private data, stop and ask before using it.

Ask for clarification only if:

- No specific chat file or pasted content has been provided.
- Speaker attribution is impossible.
- The user asks for a conclusion that requires missing context.
- The data may include immediate danger and the user's intent is unclear.

## Stage 1: Corpus Discovery

Use only user-provided file paths, attached files, or pasted chat content. Include likely text formats such as `.txt`, `.md`, `.csv`, `.json`, `.html`, and exported chat text only when the user explicitly identifies them as chat records. If the user pasted chat content directly, treat the pasted text as the corpus.

Do not recursively search the workspace for chat files. If the user says "analyze my chats" but does not name or provide the files, ask them to provide the export or exact path.

For each source, record:

```json
{
  "source_file": "path or pasted-input",
  "source_type": "line|whatsapp|telegram|imessage|messenger|instagram_dm|discord|sms|plain_text|unknown",
  "date_range_observed": "YYYY-MM-DD to YYYY-MM-DD or unknown",
  "participants_observed": ["name_or_alias"],
  "line_count": 0,
  "estimated_message_count": 0,
  "quality_notes": []
}
```

## Stage 2: Normalize And Clean

Read `references/cleaning-prompt.md`.

Normalize chat records into this schema:

```json
{
  "message_id": "stable-id",
  "source_file": "path or pasted-input",
  "timestamp": "ISO-8601 or null",
  "date": "YYYY-MM-DD or null",
  "speaker": "person_a|person_b|third_party|system|unknown",
  "speaker_label_original": "raw label",
  "text": "message text",
  "message_type": "text|media|sticker|call|system|deleted|unknown",
  "is_low_signal": false,
  "noise_reason": null,
  "confidence": "high|medium|low"
}
```

Cleaning rules:

- Keep message order even when timestamps are missing.
- Preserve low-signal items in the manifest but exclude them from relationship interpretation unless they matter.
- Label deleted messages and media placeholders; do not infer their content.
- Merge multi-line messages only when they clearly belong to the same speaker and timestamp.
- Deduplicate repeated export blocks.
- Standardize participant aliases to `person_a` and `person_b`; keep a mapping in the manifest.
- Redact unnecessary identifiers before writing any manifest.
- Keep full normalized messages in memory only as needed for analysis. Do not persist them by default.

## Stage 3: Segment Into Episodes

Create episodes based on time gaps, topic shifts, conflict windows, repair attempts, and relationship milestones.

Episode types:

- `ordinary_contact`
- `planning_or_logistics`
- `affection_or_intimacy`
- `emotional_bid`
- `conflict`
- `repair_or_reconnection`
- `distance_or_coldness`
- `boundary_or_pressure`
- `breakup_or_reconciliation`
- `third_party_or_external_stress`
- `unclear`

Episode schema:

```json
{
  "episode_id": "episode-001",
  "date_range": "YYYY-MM-DD to YYYY-MM-DD",
  "episode_type": "conflict",
  "participants": ["person_a", "person_b"],
  "message_count": 0,
  "summary": "brief factual summary",
  "data_quality": "high|medium|low",
  "messages": []
}
```

Dry-run output should include corpus size, participants, date coverage, noise ratio, episode counts by type, and any major attribution or missing-context problems.

## Stage 4: Episode-Level Extraction

Read `references/extraction-prompt.md`.

Process episodes in batches. For each episode, extract relationship dynamics using the schema defined in the extraction prompt. If using parallel agents, each agent should process a disjoint batch and return valid JSON only.

If JSON is malformed:

- Try to salvage by removing markdown fences and locating the outer JSON object or array.
- If still unparseable, log the failed episode and continue.

## Stage 5: Aggregation

Aggregate extraction results by:

- Participant
- Episode type
- Timeline period
- Repeated loop
- Evidence strength
- Safety relevance

Do not count repeated messages from duplicated exports as separate evidence.

Pattern confidence:

- `high`: repeated in 3+ episodes, clear message evidence, low missing-context risk
- `medium`: repeated in 2+ episodes or strong single episode with clear context
- `low`: plausible but limited, ambiguous, or context-dependent

## Stage 6: Cross-Episode Synthesis

Read `references/synthesis-prompt.md`.

Synthesize the final relationship dynamics across configured output sections. Include data quality notes before interpretation so the reader can calibrate trust.

## Stage 7: Blind Spots, Unsupported Claims, And Safety Review

Read `references/blindspot-prompt.md`.

Identify:

- Blind spots for each participant
- Repeating loops neither side seems to resolve
- Claims the user may want to make that the evidence does not support
- Safety concerns requiring caution
- Alternative interpretations that remain plausible

## Stage 8: Final Output

Before writing output files, tell the user:

- The exact output paths.
- That the files may contain sensitive relationship analysis and short quoted excerpts.
- That local files can persist in backups, sync services, search indexes, or later processes.

Proceed with file output only if the user agrees or explicitly asked for saved files.

Write to:

```text
relationship-analysis/{TODAY}-relationship-chat-analysis.md
relationship-analysis/{TODAY}-chat-corpus-manifest.json
```

Final report structure:

```markdown
# Relationship Chat Analysis

## Scope And Data Quality
## Relationship Timeline
## Communication Pattern
## Emotional Needs And Bids
## Conflict Escalation Pattern
## Repair And Reconnection Pattern
## Distance, Avoidance, And Coldness
## Boundaries, Pressure, And Safety
## Effort Balance And Power Dynamics
## Repeating Loops
## Blind Spots For Each Person
## What The Evidence Does Not Support
## Practical Reflection Questions
```

Use short quotes with dates. Avoid dumping long private chat excerpts.

The corpus manifest should contain source metadata, participant alias mapping, data quality notes, episode summaries, and counts. It should not contain raw full message text unless the user explicitly requests that and acknowledges the retention risk.
