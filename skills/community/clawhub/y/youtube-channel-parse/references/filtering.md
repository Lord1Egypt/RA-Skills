# Filtering

Apply channel filters in this order:

1. date window
2. metadata filters
3. topic filter
4. speaker filter

## Date Window

Use `since_date` and `until_date` to narrow the candidate set before transcript retrieval.

## Metadata Filters

Use metadata filters for structured constraints such as:

- title keywords
- description keywords
- duration range
- upload date
- playlist or section context when available

## Topic Filter

Use `topic_filter` for theme-based selection.

Start with title and description matches.

Use transcript text when the topic depends on spoken content rather than metadata.

## Speaker Filter

Use `speaker_filter` for named speakers, hosts, guests, or repeated mentions.

Use title and description first.

Use transcript text when the speaker name or role appears in spoken content only.

## Selection Behavior

Write the filtered candidate set before full transcript work when the user asks to inspect or approve the selected videos.

Transcribe the filtered subset only.
