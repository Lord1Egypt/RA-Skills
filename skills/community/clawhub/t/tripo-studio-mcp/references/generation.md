# Image and model generation

| Starting input and goal | Tool and prerequisites |
| --- | --- |
| Text description for a new model | `tripo_text_to_model` with `prompt_text`. Preserve the subject, style, and explicit constraints. |
| One existing image asset | Use its supplied `image_id` for the first call unless it is known to be generated. If the adapter says it needs an uploaded input, use the handoff below. |
| One local reference image | Follow [image upload](delivery.md), then pass the grant's `object_key` as `image_key` to `tripo_image_to_model`. |
| Multiple views of the same subject | `tripo_multiview_to_model`. Supply `front` plus at least one of `left`, `right`, or `back`. Each field takes an image asset ID or an uploaded object key when supported. |
| Local model file | Follow [model upload and import](delivery.md). |

For single-image tools use exactly one of the supported image ID and upload-key fields. A view label, task ID, local path, or URL cannot substitute for either.

Product aliases use Smart Mesh P1 for Nexus v1 and P2 for Nexus v2.
When the connected schema advertises them, map P1 to
`Nexus-v1.0-20260214` and P2 to `Nexus-v2.0-20260801`, with
`family: smart_mesh`. Keep the user's explicit topology and face count.
Consult the schema if an advertised version differs.

The three modeling tools require explicit `family`, `model_version`, and `texture`. Choose a family and version that meet the request. The current contract pairs HD with releases such as `v3.1-20260211` and Smart Mesh with releases such as `Nexus-v2.0-20260801`. Confirm the connected schema and version-specific constraints. In particular:

- Use the live `face_limit` guidance for the chosen family, version, topology and quality. The minimum is 500. If omitted, MCP requests the applicable HD maximum; Smart Mesh uses the downstream default of 500. For a low-poly asset or a downstream topology budget, set an explicit supported limit. A requested limit does not guarantee a particular output face count. HD allows 50,000 quad, 1,000,000 standard triangle, or 2,000,000 detailed triangle faces (v3.1). Smart Mesh Nexus v1 allows 20,000 triangle faces. Nexus v2 allows 25,000 quad or 50,000 triangle faces. Set `quad` explicitly when topology matters. Ask which constraint can change if the requested count is outside the allowed range.
- Send an explicitly requested `symmetry: true` or `false` only for Smart Mesh Nexus v2. Omit it for HD and Nexus v1. If symmetry is required for an unsupported version, ask whether switching to Nexus v2 is acceptable.
- With `texture: false`, omit `pbr`, `texture_quality`, and `delight`. Passing `false` for a boolean field still counts as supplying it. HD generation with `generate_parts: true` requires `texture: false` and an explicit `segmentation_granularity`. Ask whether to prioritize parts or texture if the user requests both in one generation.
- Map a requested texture resolution onto the `texture_quality` enum: `standard` is 2K, `detailed` is 4K, and `extreme` is 8K. A named resolution is not a request for the highest tier. Higher tiers need plan entitlement, so an unentitled tier is rejected before a task exists. Report the enum value actually sent, not the user's wording, so the rejected tier is identifiable. If the request names a resolution the enum cannot express, ask which supported tier to use.
- Do not infer that every field in a shared schema works for every family. HD-only options include negative text prompts and geometry quality. If the connected tool cannot represent a user requirement, explain it or ask about an acceptable alternative.

For example, an untextured HD model from a prompt on a connection advertising this version:

```json
{
  "prompt_text": "A chunky toy-style lighthouse with a wide circular base",
  "family": "hd",
  "model_version": "v3.1-20260211",
  "texture": false,
  "idempotency_key": "<stable key for this operation>"
}
```

Call `tripo_text_to_model` with those arguments after substituting the actual key. For other modeling inputs, use the appropriate tool and input field instead. Poll `tripo_get_model_task` by `task_id`. Once it succeeds, use each needed `model_id` from `model_ids` with `tripo_get_model_asset`.

## Image preprocessing and four-view handoff

- `tripo_generate_multiview_images` produces views from one source image. Use `image_id` or the upload's `image_key`, as supported.
- `tripo_upscale_image` and `tripo_split_image` use `image_id` or the upload's `resource_key`, as supported.
- Follow each image task with `tripo_get_image_task`. After success, read its `image_ids` with `tripo_get_image_asset`.
- Match each view by `result_key`. Slot numbers, file order and filenames do not establish direction. If the images visibly contradict their labels, ask the user to verify the mapping before submitting. Keep the image task ID and affected labels for troubleshooting.

### Use generated images as model inputs

An existing or delivered image ID alone does not establish its origin. If
the source is unknown, use the supplied ID and let the adapter validate it
before submitting work. If the source is known to be generated or the
adapter requests re-upload, follow the upload handoff.

Check the destination tool's description. If it requires images backed by
uploads, use `tripo_get_image_asset` to obtain each generated image's
`download_url`. Download the bytes, follow [image upload](delivery.md), and
pass the grant's `object_key` as `image_key` or the corresponding view
field. An `image_id` field may accept only uploaded inputs. If the connected
tool accepts generated IDs, pass the verified IDs directly. Image
preprocessing has its own input contract.

If the host cannot download and PUT the bytes, ask for uploaded keys or
files and pause the dependent step. If a model tool already returned a
definite `invalid_asset` with re-upload guidance, re-upload the input before
submitting the corrected request. If acceptance is unclear, recover the
original request first.

Use [Recovery](recovery.md) for pending or uncertain tasks.

For an advice-only request about already contradictory view labels, explain the
mismatch using the supplied labels and task ID and ask for corrected inputs or
a verified mapping without calling tools.

If the user says the front view or every additional view is unavailable,
multiview modeling is blocked. Ask for the missing required view and stop;
do not search for unrelated assets or substitute another input workflow unless
requested. A missing prerequisite is not permission to discover replacements.

Check whether required view inputs exist before any asset discovery. A declared
missing front or additional view ends that branch; listing assets does not cure
a missing input or authorize substitutes. Advice about a reported label mismatch
uses the supplied evidence without querying tasks or assets. Request a corrected
mapping only when needed to continue a separately authorized modeling step.

Task and asset metadata describe labels, not image pixels. A user-reported
contradiction already blocks modeling; do not re-read metadata to reconfirm it.
Ask for corrected inputs or mapping. Perform visual inspection only when
explicitly requested and supported by the host's viewer.

Before a generated-image upload handoff, establish that the host can download
bytes and PUT them to an upload grant. If these capabilities are absent, briefly
ask for an uploaded key or file and pause before asset fetches or grants. Do not
speculate about unavailable transfer tools. An explicit self-upload request may
instead use the private grant handoff described in Delivery.
