# Guide 04 — Source Normalization

## Purpose

Normalization ensures that minor formatting differences in the same underlying content do not produce different chunks, hash mismatches, or misleading metadata. All hashes (`document_content_hash`, `content_hash`) must be computed from **normalized** content, never from raw source payloads.

The normalization logic must be versioned independently from the schema, and the `normalizer_version` field recorded on every chunk.

---

## Why Normalization Matters

Without consistent normalization:
- The same message edited to fix a typo produces a different hash → unnecessary re-ingestion
- Whitespace differences between source systems cause false "content changed" detections
- Emoji codes (``:thumbsup:``) and actual emoji (👍) produce different embeddings for the same meaning
- Duplicate quoted-reply content in email inflates chunk count and confuses retrieval

---

## Universal Normalization Rules

Apply these to ALL content from ALL source types, in this order:

1. **Collapse whitespace** — Replace all consecutive whitespace characters (spaces, tabs, non-breaking spaces, zero-width spaces) with a single space.

2. **Strip leading/trailing whitespace** — From the full document text and from each logical segment before chunking.

3. **Normalize Unicode** — Convert to NFC (Canonical Decomposition, Canonical Composition) form. This resolves composed vs. decomposed character variants.

4. **Strip HTML/markup** — Remove HTML tags, markdown rendering artifacts, inline CSS. Preserve only the text content. Do not strip structural markers (headings, list markers) that inform chunking hierarchy.

5. **Normalize timestamps** — Convert all timestamps to ISO 8601 UTC: `2024-04-30T18:00:00Z`.

6. **Normalize author/participant names** — Map to canonical directory names. If a user is referenced as "Jane", "Jane Smith", "jsmith", or "Jane S." in different parts of the content, normalize to their canonical display name from your directory.

```python
import unicodedata
import re

def universal_normalize(text: str) -> str:
    """Apply all universal normalization rules."""
    # Step 1: Normalize Unicode to NFC
    text = unicodedata.normalize("NFC", text)
    
    # Step 2: Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    
    # Step 3: Collapse all whitespace to single space
    text = re.sub(r"\s+", " ", text)
    
    # Step 4: Strip leading/trailing whitespace
    text = text.strip()
    
    return text
```

---

## Source-Specific Normalization Rules

Apply these AFTER the universal rules, for each source type.

### Slack

```python
def normalize_slack(text: str, user_directory: dict) -> str:
    """Normalize Slack message content."""
    # Replace user mention IDs with display names: <@U012AB3CD> → @Jane Smith
    def replace_mention(match):
        uid = match.group(1)
        return f"@{user_directory.get(uid, uid)}"
    text = re.sub(r"<@([A-Z0-9]+)>", replace_mention, text)
    
    # Replace channel links: <#C03AB|general> → #general
    text = re.sub(r"<#[A-Z0-9]+\|([^>]+)>", r"#\1", text)
    
    # Replace Slack URLs: <https://example.com|Click here> → Click here (https://example.com)
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r"\2 (\1)", text)
    
    # Strip bare URLs in angle brackets: <https://example.com> → https://example.com
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)
    
    # Replace emoji shortcodes: :thumbsup: → 👍 (or strip if emoji not desired)
    # Use emoji library for replacement, or simply strip shortcodes:
    text = re.sub(r":[a-z0-9_+-]+:", "", text)
    
    # Strip bot-generated footers (customize patterns for your workspace)
    # e.g., "Sent via Zapier", "This is an automated message"
    text = re.sub(r"(?i)(sent via|this is an automated message).*$", "", text, flags=re.MULTILINE)
    
    return universal_normalize(text)

# Handle edited messages: always use latest text, flag is_edited=True in metadata
def get_slack_message_text(message: dict) -> tuple[str, bool]:
    is_edited = "edited" in message
    text = message.get("text", "")
    return text, is_edited
```

### Email

```python
def normalize_email_body(raw_body: str) -> str:
    """Normalize email body, stripping quoted replies and signatures."""
    
    # Strip quoted reply blocks (lines starting with >)
    lines = raw_body.split("\n")
    body_lines = []
    in_quoted = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(">"):
            in_quoted = True
            continue
        # Common reply delimiters
        if any(stripped.startswith(d) for d in [
            "On ", "From:", "-----Original Message-----",
            "________________________________", "Sent from my"
        ]):
            break  # Everything after this is quoted reply
        if not in_quoted:
            body_lines.append(line)
    
    body = "\n".join(body_lines)
    
    # Strip email signatures (lines after -- on its own line)
    body = re.sub(r"\n--\s*\n.*$", "", body, flags=re.DOTALL)
    
    # Strip legal disclaimers (common patterns)
    body = re.sub(
        r"(?i)(this email and any attachments|confidentiality notice|disclaimer:).*$",
        "",
        body,
        flags=re.DOTALL,
    )
    
    return universal_normalize(body)

def normalize_email_headers(from_addr: str, to_addrs: list, subject: str) -> dict:
    """Normalize email header fields to consistent format."""
    return {
        "from": from_addr.strip().lower(),
        "to": [addr.strip().lower() for addr in to_addrs],
        "subject": subject.strip(),
    }
```

### Meeting Transcripts (Fireflies / similar)

```python
FILLER_WORDS = {
    "um", "uh", "er", "ah", "like", "you know", "sort of", "kind of",
    "basically", "literally", "actually", "right", "okay", "so"
}

def normalize_transcript_segment(
    text: str,
    speaker_name: str,
    canonical_names: dict,
    confidence_threshold: float = 0.7,
    segment_confidence: float = 1.0,
) -> str:
    """Normalize a single speaker turn in a meeting transcript."""
    
    # Normalize speaker name to canonical directory name
    canonical_speaker = canonical_names.get(speaker_name, speaker_name)
    
    # Strip filler words if confidence is below threshold
    if segment_confidence < confidence_threshold:
        words = text.split()
        words = [w for w in words if w.lower().strip(".,?!") not in FILLER_WORDS]
        text = " ".join(words)
    
    # Prepend speaker attribution
    normalized = f"[{canonical_speaker}]: {text}"
    
    return universal_normalize(normalized)

def build_transcript_context_header(meeting: dict) -> str:
    """Build the context header prepended to every transcript chunk."""
    return (
        f"Meeting: {meeting['title']} | "
        f"Date: {meeting['date']} | "
        f"Attendees: {', '.join(meeting['attendee_names'])}"
    )
```

### Google Drive Documents

```python
def normalize_gdrive_document(raw_content: str, doc_type: str) -> str:
    """Normalize Google Drive document content."""
    
    if doc_type == "doc":
        # Strip suggestion markup: {+added text+} and {-removed text-}
        raw_content = re.sub(r"\{\+[^}]*\+\}", "", raw_content)
        raw_content = re.sub(r"\{-[^}]*-\}", "", raw_content)
        
        # Strip comment anchors: [[COMMENT: ...]]
        raw_content = re.sub(r"\[\[COMMENT:[^\]]*\]\]", "", raw_content)
    
    # Export Google Docs as Markdown (use Google API export with MIME type text/markdown)
    # Preserve heading structure as structural markers for chunking:
    # ## Heading 2 → keep for hierarchical chunking boundary detection
    
    return universal_normalize(raw_content)
```

### ClickUp Tasks

```python
def normalize_clickup_task(task: dict) -> str:
    """Normalize ClickUp task into a single text block."""
    
    parts = []
    
    # Task title
    parts.append(f"Task: {task.get('name', '')}")
    
    # Task description
    if task.get("description"):
        desc = task["description"]
        # Strip ClickUp markup: @mentions, /commands, etc.
        desc = re.sub(r"@\w+", "", desc)
        desc = re.sub(r"/\w+", "", desc)
        parts.append(desc)
    
    # All comments, in chronological order
    for comment in sorted(task.get("comments", []), key=lambda c: c.get("date", "")):
        author = comment.get("user", {}).get("username", "Unknown")
        text = comment.get("comment_text", "")
        if text:
            text = re.sub(r"@\w+", "", text)  # Strip mentions
            parts.append(f"[{author}]: {text}")
    
    combined = "\n\n".join(parts)
    return universal_normalize(combined)
```

---

## Normalization Checklist

Before writing the normalization function for a new source:

- [ ] Unicode normalized to NFC
- [ ] HTML/markup stripped, structure preserved for chunking
- [ ] Source-specific user IDs replaced with display names
- [ ] Source-specific markup and noise removed
- [ ] Timestamps in ISO 8601 UTC
- [ ] Quoted/repeated content stripped (email, threaded messages)
- [ ] Signatures and disclaimers stripped
- [ ] Content verified to be deterministic: same input always produces same output
- [ ] `normalizer_version` bumped if normalization logic changes
