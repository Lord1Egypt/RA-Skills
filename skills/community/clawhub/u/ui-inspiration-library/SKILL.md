---
name: ui-inspiration-library
description: Archive UI screenshots into a searchable inspiration library and retrieve matching references by style, page type, use case, or visual goal.
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "env": ["NOTION_API_KEY"] },
        "primaryEnv": "NOTION_API_KEY"
      },
  }
---

# UI Inspiration Library

Archive UI references in a structured library, then retrieve the right ones later when someone actually needs them.

This skill has three core promises:
1. **Save images cleanly** into a reusable inspiration library.
2. **Make them searchable** with retrieval-friendly metadata.
3. **Return matching images** during search, not just text summaries.

Treat the library as a working visual search system, not a dead archive. Retrieval quality matters as much as ingestion quality.

## Core capabilities

### 1. Archive mode

Use when the user wants to:
- save a UI screenshot,
- collect inspiration,
- archive a design reference,
- tag an image for future reuse,
- build up a team or personal UI library.

Goal:
- normalize the incoming image,
- analyze it as a reusable design reference,
- create retrieval-friendly metadata,
- store both metadata and original image in the target library.

Return:
- concise title,
- key tags,
- archive result,
- item link when useful.

### 2. Retrieval mode

Use when the user wants to:
- search the inspiration library,
- browse references for a design goal,
- compare visual directions,
- find references by keyword, style, page type, or use case,
- get actual matching images back.

Goal:
- interpret the user’s visual/design intent,
- query the backing library,
- rank strong matches,
- return the actual images whenever possible,
- explain briefly why each match fits.

If the user is clearly browsing references, prefer an **image-first response** over a text-only report.

## Mode selection rules

Choose the workflow based on the user input:
- If the user provides one or more screenshots or asks to save/archive/tag them, use **archive mode**.
- If the user asks for references, examples, inspiration, comparisons, or similar visuals, use **retrieval mode**.
- If the user provides screenshots and also asks to compare, shortlist, or find related references, archive first when needed, then run retrieval or comparison.
- If the user intent is ambiguous, ask one short clarification question instead of guessing.

## Backend configuration discovery

Assume backend identifiers and access details come from runtime configuration, environment variables, user-provided parameters, or existing project documentation.

Before writing to a backend:
- determine which backend should be used,
- determine whether archive and retrieval use the same backend,
- determine how to locate the target database or collection,
- verify read/write permission before attempting a full archive flow.

If the target backend is not specified or not discoverable:
- ask the user one short question before writing,
- explicitly ask where the target library should live,
- ask whether the user wants help creating a new library if none exists,
- do not guess private database identifiers,
- do not auto-create a new library unless the parent location is already known and the runtime is clearly allowed to create it,
- still offer image analysis and structured metadata output without persistence.

## Default workflow

### Archive workflow

1. Detect the source channel and obtain the image locally.
2. Normalize the input into a stable image source or file.
3. Analyze the image as a UI inspiration reference.
4. Generate structured metadata optimized for future retrieval.
5. Create the target library record.
6. Upload or attach the original image to that record.
7. Return a short archive confirmation.

### Retrieval workflow

1. Parse the user’s intent.
2. Map it to one or more retrieval dimensions:
   - visual goal,
   - page type,
   - style tags,
   - component tags,
   - use case,
   - keyword signals in summaries/highlights/source.
3. Query the library.
4. Rank results by real design usefulness.
5. Return 1-5 strong matches, preferring 3 when many exist.
6. Send the actual images whenever possible.
7. Add 1-2 lines of rationale per result.

## Retrieval-first rules

When a user says things like:
- "show me some references"
- "find similar examples"
- "which ones work well for a cover?"
- "find AI-style hero references"
- "pick a few dashboard references"

assume they want **usable visual references**, not only text.

Preferred retrieval output order:
1. image preview,
2. short title,
3. why it matches,
4. optional item link.

A few strong matches are better than many weak ones.

## Multi-image, duplicate, and update rules

Use these defaults unless the user says otherwise:
- create one record per image,
- analyze each image separately,
- group multiple images into one record only when the user explicitly asks for a grouped reference set,
- update an existing record only when the user clearly refers to that record,
- append images by default when adding to an existing record,
- replace existing images only when the user explicitly says replace or overwrite.

Handle possible duplicates conservatively:
- if the same image appears to have been archived already, prefer warning or asking before creating another near-identical record,
- if the title collides but the image is meaningfully different, create a new record instead of silently merging,
- if duplicate detection is weak or uncertain, preserve the new item and state the uncertainty.

## Classification rules

Optimize for future retrieval, not exhaustive critique.

Use this minimum metadata set unless the storage backend cannot support it:
- title,
- summary,
- page type,
- style tags,
- component tags,
- use-case tags,
- original image or source link.

Apply these constraints:
- Keep titles short, concrete, and searchable.
- Prefer stable reusable tags over clever one-off wording.
- Use 1-3 page types.
- Use 2-5 style tags.
- Use 2-6 component tags.
- Use 1-3 use-case tags.
- Write 2-5 short highlights in the user's language when helpful.
- Write one concise summary focused on reference value in the user's language.
- If uncertain, choose broader categories instead of hallucinating precision.

## Source and privacy rules

Use the `source` field carefully.

Preferred source order:
1. public source URL when the user provides one,
2. canonical page URL when safely derivable,
3. channel or source label such as `telegram upload` or `manual upload`,
4. user-provided source note.

Avoid storing private local filesystem paths, temporary download URLs, access tokens, or account-specific transport details in long-term records unless the user explicitly asks for that behavior.

Before archiving, watch for low-value or sensitive images:
- unreadable, heavily cropped, or extremely low-resolution screenshots,
- screenshots dominated by personal data,
- screenshots containing private internal dashboards, customer data, or secrets,
- images whose reference value is too weak to justify storage.

Default behavior:
- warn before storing obviously sensitive screenshots,
- do not archive sensitive internal or personal screenshots by default unless the user explicitly confirms they want them stored,
- ask before archiving low-value or ambiguous material when the user intent is unclear,
- if the user clearly wants it archived anyway, proceed and record the limitations concisely.

## Output requirements

### Minimum archive output

Return at least:
- title,
- 3-8 important tags or category labels,
- archive status,
- item link or identifier when available.

Clearly separate:
- metadata write success,
- image upload success,
- partial success.

### Minimum retrieval output

Return at least:
- 1-3 strong matches by default,
- short title for each match,
- 1-2 lines of rationale,
- image preview when supported, otherwise item link.

Do not dump raw database records unless explicitly asked.

## Storage model guidance

This skill is storage-backend aware but should stay backend-neutral at the top level.

## Prerequisites and backend requirements

Use this skill only when the runtime already has access to a suitable storage backend.

This skill may require backend-specific credentials depending on the chosen storage backend.
For Notion-backed archive or retrieval flows that read or write a Notion database, `NOTION_API_KEY` should already be configured in the runtime.
Metadata-only analysis can still proceed without backend write access.

## Requirements for Notion-backed use

To use this skill with Notion as the storage backend, the user should already have:
- a Notion account,
- a Notion integration or API key,
- a target Notion database, or a parent page where a new database can be created,
- permission to connect that database or page to the integration.

Without these prerequisites, the skill can still analyze images and produce structured metadata, but it cannot complete Notion-backed archiving.

Minimum requirements:
- the runtime can read the source image from the current channel or local path,
- the runtime can analyze images or at least preserve them with low-confidence metadata,
- the runtime can create, update, and query records in the target backend,
- the runtime can attach or reference the original image in that backend,
- the runtime can return image previews or links back to the user.

If using **Notion** as the backing store:
- the runtime must already have working Notion integration or API access,
- the target database must already exist or be creatable by the runtime,
- the runtime must have permission to read and write the target database,
- database IDs, page IDs, and similar identifiers must remain configurable,
- if no target database can be found, ask the user where the library should live and whether a new database should be created there,
- only auto-create a Notion database when the parent page/location is already known and unambiguous,
- this public skill does not include personal credentials or private workspace configuration.

In OpenClaw-based setups, assume backend integrations must be configured outside the skill itself.
If backend access is missing, do not pretend archive or retrieval succeeded. Fall back to image analysis, broad tagging, and structured metadata output when possible.

A good backing store should support:
- a title field,
- an image/file field,
- structured metadata fields,
- text search,
- filtering by select/multi-select style properties,
- stable item links.

If using **Notion** as the backing store:
- keep the database ID and related identifiers configurable,
- store original images in a dedicated file/image property,
- separate database/page creation from file upload if the API path requires it,
- document any API version split in implementation notes rather than hardcoding personal IDs into the public skill.

## Capability and fallback rules

Prefer this execution order:
1. obtain image,
2. analyze image,
3. write structured metadata,
4. attach original image,
5. deliver preview or result links.

If a capability is unavailable, degrade gracefully:
- If image analysis is unavailable, store the image with a broad title and broad tags, and clearly mark metadata as low-confidence.
- If direct image attachment is unavailable, store a source link or local-path reference when safe and supported.
- If image preview delivery is unavailable, return title, rationale, tags, and item link instead.
- If the backend supports only partial structured fields, preserve the most retrieval-critical fields first: title, summary, page type, style tags, and image/source.

## Result quality rules

### Good archive result
- confirms success or partial success,
- shows the generated title,
- shows the most important tags,
- clearly separates metadata-write success from image-upload success.

### Good retrieval result
- returns images directly when possible,
- includes concise rationale,
- helps the user decide quickly,
- avoids dumping raw database records.

## Failure handling

For archive flows, separate failures into:
- image retrieval failure,
- analysis failure,
- record creation failure,
- image upload/attachment failure,
- final patch/update failure.

For retrieval flows, separate failures into:
- query interpretation failure,
- database query failure,
- image download failure,
- result-delivery failure.

Partial success is acceptable when the user still receives a usable result.

If image return fails but text retrieval succeeds, still return:
- title,
- rationale,
- key tags,
- item link,
- and clearly state that preview delivery failed.

## Public packaging rules

When publishing this skill publicly:
- remove private workspace IDs, URLs, and account-specific paths,
- keep channel handling generic,
- keep the backing store configurable,
- document both archive and retrieval as first-class capabilities,
- explicitly state that retrieval should return matching images whenever possible,
- avoid embedding personal workflows or private credentials.

## Read these references when needed

- Read `references/analysis-schema.md` when generating structured metadata for new images.
- Read `references/channel-flow.md` when adapting image intake from chat channels.
- Read `references/notion-database-schema.md` when creating or reviewing the target Notion schema.
- Read `references/notion-mapping-spec.md` when implementing field mapping and normalized writes.
- Read `references/notion-file-upload.md` when attaching original images to Notion records.
- Read `references/query-flow.md` when implementing retrieval, ranking, and image-first result delivery.
- Read `references/tag-vocabulary-v1.md` when selecting or extending bilingual tags.

## Scope

Use this skill for:
- inspiration archiving,
- design-reference retrieval,
- visual shortlist generation,
- inspiration-library workflows.

Do not use this skill as the primary tool for:
- formal UX audits,
- accessibility review,
- redesign critique,
- production UI specification writing.
