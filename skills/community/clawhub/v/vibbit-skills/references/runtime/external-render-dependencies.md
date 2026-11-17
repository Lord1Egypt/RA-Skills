# External rendering dependencies

Read this only for local programmatic rendering. Official engine skills and project dependencies are separate from this package. Simple cutting, joining, resizing, mixing, or subtitles can use an existing FFmpeg installation without an animation framework.

If the user declines local installation, choose a cloud or hybrid route appropriate to the requested result. Do not substitute another installer or use an implicit download through npx. Existing tools may be used when that is within the user's stated permission.

## Check the actual execution host

Identify the machine that will run the renderer; an available cloud shell is not evidence that software exists on the user's computer. Inspect the selected official skill, the actual project manifest and lockfile, installed versions, and the project's preview/render entry points.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/render-doctor.js" --engine remotion --project /absolute/path/video-project
node "$VIBBIT_SKILL_DIR/scripts/render-doctor.js" --engine hyperframes --skill-root /absolute/path/skills
~~~

The engine can be `remotion`, `hyperframes`, or `all`. The project is optional. Repeat `--skill-root` for directories containing skill folders; explicit roots limit the search. Default roots cover common host locations, so a missing result does not establish that the skill is absent everywhere.

The doctor only reads files and PATH. It does not run package executables, access the network, install dependencies, or render anything. It always reports `render_verified: false`. Missing dependencies are a discovery result; invalid arguments and execution errors return a nonzero status. A declared version range is not an installed version.

## Install only when needed and authorized

Respect permission already given for the current task. Install only the selected engine and necessary project dependencies. Keep official skills in the host's skill location and dependencies in the video project, outside this package. Follow the selected engine's current instructions: initialization may change a global CLI, and an existing project may require a specific version. Do not perform unrelated global upgrades.

Read only the relevant official modules. Report the host and actual installation/render result accurately; do not claim a host has reloaded a skill merely because files were written.

See [engine selection](../engines/index.md) and [local rendering](local-rendering.md).
