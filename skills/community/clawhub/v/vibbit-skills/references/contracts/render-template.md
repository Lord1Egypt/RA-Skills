# User-owned render template contract

This describes metadata needed to adapt user-provided Remotion/Hyperframes templates. It does not require changing official project formats and is not an API request. A catalog can be a local JSON file or an existing catalog service.

## Selection metadata

Include stable source-specific `template_id`/`template_version`; name, description, and tags; actual `engine`; `kind` (full_video/clip/overlay); optional real preview; output ratio/dimensions, frame rate, duration/range, format, alpha/audio conventions; and actual `project_ref`. Verify a remote distribution's supplied version checksum when available.

Local template IDs are separate from Vibbit packaging and material IDs.

## Selected template detail

Read only after selection:
- Real entry/composition in the engine's own format.
- `parameters_schema`: names/types, required fields, enums/ranges, text length, item count, and units.
- Defaults, with demonstration business data explicitly marked as examples.
- `parameter_binding`: actual Remotion props or Hyperframes variables/scripts, without assuming a shared CLI flag.
- Engine/version, package manager, lockfile, environment, fonts, and media dependencies.
- Bundled asset paths and parameterized assets such as logos.
- Verification environment/specifications/date/result, including unverified status where appropriate.

A template version identifies a fixed master and dependency specification. Change the version when the master or parameter meaning changes; instances retain their input and actual runtime versions. Use existing fields or a local catalog instead of requiring a new catalog service.

Resolve specific text/data/ratio/duration conflicts. Dynamic durations must update scene and audio timing. Do not force fixed duration by accelerating user speech or truncating content. Extending the template structure is a project change, not merely changing parameters.

For cloud packaging, determine which subtitles/titles are already baked in and whether a clean body can be exported. Do not assume every template can disable them.

When integrating a first template, verify runnable real input, parameter boundaries, output specifications, fonts/assets, rerendering after a parameter change, and the actual required delivery/cloud path. Do not label arbitrary engine/template combinations as certified.

See [template discovery](../resources/render-templates.md) and [artifact handoff](render-artifact.md).
