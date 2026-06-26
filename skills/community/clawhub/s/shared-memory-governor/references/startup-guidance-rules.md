# Startup Guidance Rules

## Quick map

- Purpose
- Startup section detection priority
- Guidance placement rules
- Recommended startup wording
- Attachment success criteria
- Detach rules

## Purpose

Use this reference when implementing, repairing, detaching, or reviewing shared-memory startup guidance in agent-local `AGENTS.md` files.

## Startup section detection priority

Use this priority order in v1:

1. `## Session Startup`
2. `## Every Session`
3. explicit fallback guidance block near the top of `AGENTS.md`

All of these commands must use the same priority order:
- `attach <agent>`
- `detach <agent>`
- `repair-attachment <agent>`
- `review-attachments`

## Guidance placement rules

- Prefer placing the guidance block into the highest-priority startup section that already exists.
- Do not append a shared-memory guidance block to the end of `AGENTS.md` when a valid startup section already exists.
- If no valid startup section exists, place a clearly marked fallback guidance block near the top of the file.
- If a startup section already contains the correct shared-memory guidance, do not duplicate it.
- If both a startup guidance block and an old trailing block exist, treat the trailing block as stale and remove it during repair.

## Recommended startup wording

Use this wording when merging into the local startup section:

```md
5. If local `SHARED_ATTACH.md` is present, read it as part of session startup.
6. Then read the shared memory files exactly as instructed by `SHARED_ATTACH.md`.
7. Treat shared memory as a general supplemental long-term context layer.
8. Use shared memory only as supplemental background.
9. Do not let shared memory override this agent's private identity guidance or assistant-specific context.
```

## Attachment success criteria

Treat local attachment as complete only when all are true:

1. local `SHARED_ATTACH.md` exists
2. local `AGENTS.md` contains the shared-memory startup guidance in the highest-priority startup section that exists
3. there is no stale old trailing guidance block left at the end of `AGENTS.md`
4. the startup guidance and `SHARED_ATTACH.md` instructions are consistent with each other

## Detach rules

During `detach <agent>`:
- archive `SHARED_ATTACH.md`
- remove the startup guidance or fallback guidance block
- remove stale old trailing guidance blocks if present
- do not delete private long-term memory files
- do not delete private daily memory files
- do not silently remove unrelated local guidance
