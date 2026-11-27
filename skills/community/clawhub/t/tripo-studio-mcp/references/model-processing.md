# Model processing and animation

When an operation needs a source model and the user has no model ID, use `tripo_list_model_assets` to find a suitable owned asset. If several match, confirm the intended source. With a supplied ID and required arguments, submit directly. Use `tripo_get_model_asset` first when the user requests verification or when a required fact must come from the asset, such as the part catalogue. Pass its ID as `source_model_id` where the schema calls for it. Inspect the result of each successful step before using it as the source of the next step.

| User goal | Tool and prerequisites |
| --- | --- |
| Add or change textures | `tripo_texture_model`. Supply exactly one supported reference: `prompt_text`, an accepted `image_id`, an uploaded `image_key`, or `images` with matching view fields. For a generated image, follow the [input handoff](generation.md#use-generated-images-as-model-inputs). Include the required texture quality and delight fields. |
| Improve existing texture resolution | `tripo_texture_upscale`. Use a model with texture and a supported target quality. |
| Unwrap UVs or produce PBR maps | Use `tripo_uv_unwrap` or `tripo_generate_pbr` for the requested operation. |
| Split a model into parts | Use `tripo_segment_model` when advertised. Read the resulting model and verify its part directory before a part-dependent operation. |
| Remesh a whole model | Use `tripo_remesh_model` when advertised. Use an owned model without textures or parts, with an explicit `quad` choice and `face_limit` of 500–50000. Submit the original `idempotency_key` and `source_model_id`. |
| Reduce or complete selected geometry | Use `tripo_smart_low_poly_model` or `tripo_complete_model` only with a source that meets the live tool's prerequisites. |
| Make a separate copy | Use `tripo_copy_model` when the user wants a new copy. Read the resulting asset before editing it. |
| Add a skeleton | `tripo_rig_model`. Use a successful whole model that is not already rigged. Choose `topology` for the subject and `spec` for the requested target. For example, use `topology: quadruped` and `spec: unity` for a four-legged character destined for Unity. The skeleton spec does not request file conversion. Deliver the existing model link unless the user also requests export or a different format. |
| Generate motion from text | `tripo_text_to_motion` with ordered segments, each containing a prompt and duration in seconds. After task success, read `motion_id` with `tripo_get_motion_asset`. |
| Browse available preset motions | `tripo_list_motion_presets` lists enabled presets in the connected environment. |
| Apply motion to a rigged model | Use `tripo_retarget_model` with a compatible rigged source. See the argument mapping below. |

When the user describes a preset by name or action, use
`tripo_list_motion_presets` to look it up. Supply the exact `topology` filter
when known, or omit it to browse all topologies. Match the requested action and
rig using the returned `title`, `action_type` and `topology`. If you need another
page, pass `next_page_token` back as `page_token` with the same filter. If
several presets fit, ask the user to choose when the differences matter. If the
catalogue is unavailable or has no suitable match, explain what blocked preset
selection and stop that step.

For a preset, copy `motion_id` exactly from the catalogue and submit it with
`motion_source: preset`. An explicit preset ID from the user can be submitted
directly. For an existing user-generated motion asset, pass its UUID as
`motion_id` with `motion_source: user_generated`. Pass the supplied rigged model
ID as `source_model_id`, or use the successful rigging task's new `task.model_ids`
result when chaining. The server validates compatibility. After success, copy the
model ID and clip name from `task.retarget_result`. Read the model only if the
user needs its asset or link.

When an operation requires part names, use the source model's server-provided `part_names` with `parts_known=true`. For completion of selected parts, pass their names from that catalogue. The current tool can use the full catalogue when names are omitted; a request for selected parts needs explicit names. If the required catalogue or selections are unavailable, stop that step and explain what input is needed. Geometry node labels from a downloaded file are useful for display and selection in the client. Use the server-provided directory for tool arguments.

For Smart Low Poly, check the requested face count against the triangle or quad limit. Supply explicit `quad`, `do_bake`, and valid `part_names` when required. If the requested budget cannot be represented, ask which constraint can change.

A rigged model, standalone motion, and retargeted animation are separate outcomes. If retargeting fails, report the failed step and identify any verified intermediate model or motion the user can still use.

## Part workflows and reporting

Segmentation alone does not authorize completion. Complete only when the user
requests missing geometry, using the newly segmented model when chaining steps.
A successful asset read with `parts_known: false` blocks completion and does not
establish whether parts exist. Re-reading the asset, checking an old task or
using client node labels cannot establish the authoritative catalogue.

When source inspection was requested before an edit, distinguish the edited
result from the inspected original and provide their IDs and available links.
If only the edited result was requested, omit the original.
