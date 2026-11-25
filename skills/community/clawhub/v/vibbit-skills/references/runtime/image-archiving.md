# Generated image archiving

Use the same policy for reusable generated comic pages/panels, character/environment/prop references, ecommerce and marketing images, video keyframes, and retained candidates/revisions. Preserve actual outputs without regenerating, reuploading or requesting per-image confirmation to resolve archive problems. Honor explicit no-archive requests. Exclude temporary masks, caches and debug images. Supplying a reference image does not authorize registering it.

## Available behavior

Public endpoints support image generation, file upload and queries for existing image materials, but no general image registration operation. OSS upload transfers bytes; it does not prove library registration. Never pass images to video import, call website-internal endpoints, or invent an endpoint.

Completed `gen_image` results report an independent `image_archive` and attempt to save a private record. Pending registration does not prevent delivery of a successfully generated image.

| Status | Meaning |
| --- | --- |
| `pending_registration` | Real image URL retained without a verifiable material ID |
| `pending_verification` | An explicitly associated material ID has not been verified; do not register again |
| `registered` | Public detail confirms the same material ID and `media_type=IMAGE`; reuse it |
| `partially_registered` | Only some outputs are verified; retain each outcome |
| `skipped` | User requested no Skill archiving; existing cloud materials are not deleted |
| `unrecognized_result` | No supported image output was identified; retain the result for inspection |

Use IDs explicitly associated with the image in a real generation result or a private record of the same task. Task/product IDs, filenames and approximate name matches are not material IDs. Do not assign an ambiguous batch ID to every image. Verification uses read-only `GET /materials/{materialId}`. An unavailable detail query leaves verification pending without import, upload or generation calls.

## Names, groups and continuation

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" gen_image --input /absolute/path/image.json --state /absolute/private/page-001.json --archive-name 'Chapter 1 page 001 v1' --archive-group 'Comic references' --wait
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" resume --state /absolute/private/page-001.json
```

`--archive-name` and `--archive-group` record local intent, not generation API fields or successful cloud metadata changes. Defaults use task and image numbers; workflows should add meaningful work/product, purpose and version names. Omit an unspecified group without asking or creating one. Keep actual registered names/groups separate from requested values; this client does not update them.

The record is normally `STATE.images.json`, identified by `image_archive.record_file`, in a private directory with file mode 0600. It stores task/site, actual URLs, requested metadata, verified material IDs and per-image states. The submission journal continues to exclude result URLs, full prompts and credentials. Records belong in the user's private persistent production directory, never the Skill or a public repository. Signed URLs may expire; refresh through real material detail when an ID is available, never through regeneration.

When `record_saved=false`, retain the actual output in another writable private production location and report the pending work. Do not discard the image, charge for another generation, or claim registration because record retention failed. Resume the original task to refresh the same record. No analysis is requested by default. Local fields do not implement image content search, tagging, categories, product binding or cloud group updates.

`gen_image`, `status`, `wait` and `resume` accept `--no-archive`, retained in the generation journal. This skips Skill records and verification; it does not prevent server retention or delete existing materials. Do not combine it with `--archive-name`/`--archive-group`. Dry-run displays local policy without querying or writing records.

## Comics and versions

The production manifest links work, chapter, page/panel, revision, adoption state, generation task, actual source file/URL, archive record and verified material ID. Keep stable character/environment/prop references. A revised page adds a version linked to the original without regenerating other pages.

Track generated originals and compressed delivery images separately, including source revision, actual dimensions, bytes and file location. A source material ID does not prove the compressed variant was registered. Reuse identical files; register genuinely different files separately once a public operation exists. Every delivered comic image must remain strictly below `1,500,000` bytes, with existing 1K specifications unchanged. Pending registration does not block delivery of checked pages; a local manifest is not a cloud comic project.

Video service registration and external video imports follow [material import and reuse](../resources/materials.md).
