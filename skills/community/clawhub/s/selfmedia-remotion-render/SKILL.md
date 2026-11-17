---
name: selfmedia-remotion-render
description: Render an existing Remotion composition from a user-selected project using that project's installed toolchain, then verify the output against the requested render settings.
license: MIT-0
metadata:
  version: "1.0.0"
---

# Remotion Render

Use this skill when the user wants to render a video from an existing Remotion project. Ask for or infer the project workspace from the task, then use that path; never require a fixed home-directory or repository path. This package supplies instructions and an input preflight helper, not a video template, project service, or renderer binary.

## Inputs and dependencies

Before rendering, identify the project workspace, Remotion entry point, composition ID, output path, composition dimensions/FPS, codec, audio mode, and any props or media inputs. Read the project's `package.json`, lockfile, Remotion configuration, and composition registration to confirm the installed package manager and actual values. Do not alter project facts, composition, or timeline during rendering.

The selected workspace must already contain a usable Remotion project and its installed JavaScript dependencies. Rendering also requires a compatible local browser/runtime and FFmpeg capability supported by that project's Remotion version. Do not silently install dependencies or fetch a browser; if the environment is missing a dependency, report it and ask for the intended setup path.

The bundled `scripts/validate_render_request.py` checks that a request names existing project inputs, declares Remotion in `package.json`, and selects a new output path. It does not launch Remotion or claim that a render succeeded.

## Render and inspect

1. Inspect the requested composition registration and confirm its ID, width, height, FPS, duration, and props match the task and any source timeline.
2. Check that the output file does not already exist. Preserve previous successful outputs and failed render artifacts.
3. Use the project's configured CLI and package manager. The basic Remotion CLI shape is `remotion render <entry-point> <composition-id> <output-location>`; specify the requested codec and disable overwrite where the installed CLI supports it. See the official [render guide](https://www.remotion.dev/docs/render) and [CLI reference](https://convert.remotion.dev/docs/cli/render) for current flags.
4. Keep the render process observable and retain its exit status/log. If it fails or stops making progress, report the failure; do not label an incomplete file as ready.
5. Inspect the finished file with `ffprobe` for decodeability, dimensions, frame rate, video/audio streams, duration, and codec. Compare those values to the user-provided contract. Review representative frames or the full video for visible defects.
6. Save the render only at the user-selected output path. Do not upload, promote, publish, or move the result into another product's managed directory unless a separate task explicitly requests that integration.

For an FFmpeg-only fallback, use it only when the user requests a stage preview or explicitly approves a compatible alternate renderer. Record that the output did not come from Remotion and preserve the same input timing and visuals. An FFmpeg preview is not a substitute for the requested final Remotion render.

## Example

See [examples/render-request.json](examples/render-request.json) and the tiny sample project. Validate the request with:

```bash
python3 scripts/validate_render_request.py examples/render-request.json
```

Then render only after installing the sample project's dependencies in an environment selected by the user. The example does not vendor node modules or a browser.
