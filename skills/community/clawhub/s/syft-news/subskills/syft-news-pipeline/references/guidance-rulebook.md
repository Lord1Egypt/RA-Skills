# Guidance Rulebook Route

Use this route when the user expresses a durable preference that may need to persist across future runs.

## Goal

Maintain a persistent guidance file, usually:

- `profiles/user_guidance_rulebook.md`

Reuse an existing rulebook format if the workspace already uses JSON or another stable structure.

## Confirmation-First Workflow

Never persist a durable rule from one raw sentence alone.

Always do this in order:

1. summarize your understanding
2. ask whether the summary is correct
3. ask whether the user wants it persisted
4. only then write it into the rulebook

## Good Candidates

- long-term content preferences
- editorial preferences
- storyline handling preferences
- recurring search preferences
- durable dislikes or red lines

## Bad Candidates

- one-off requests for today
- temporary formatting asks
- speculative guesses that were not confirmed

## Entry Shape

Preserve these fields in each stored rule:

- `id`
- `name`
- `scope`
- `kind`
- `priority`
- `status`
- canonical guidance text
- short rationale
- source note
- confirmed date

## Scope Bands

- `all`
- `editorial`
- `storyline`
- `syft_search`
- `recommendation`

## Priority Bands

- `85-100`: identity-defining
- `65-80`: meaningful preference
- `40-60`: soft preference
- `<40`: weak or situational preference
