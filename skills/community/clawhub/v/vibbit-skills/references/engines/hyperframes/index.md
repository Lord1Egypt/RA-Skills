# Hyperframes

Use Hyperframes for the user's selected HTML/CSS video project or compatible template. Read the relevant installed official core workflow and motion graphics modules. It is not restricted to short silent clips.

Official sources: [skills](https://hyperframes.heygen.com/guides/skills), [rendering](https://hyperframes.heygen.com/guides/rendering), [official skill source](https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes-core).

When needed and authorized, use `npx skills add heygen-com/hyperframes` and select the required skill. Keep engine dependencies in the project. New-project initialization can change a global CLI; inspect the current version and avoid initialization for an existing project.

Use the selected project's real composition and input schema. Do not assume Remotion's `--props` or a universal input-file flag applies. Use the installed version's documented commands; common examples, run from the actual project directory, are:

~~~bash
npx hyperframes lint
npx hyperframes check
npx hyperframes render --output renders/final.mp4
~~~

Verify that the executable is installed before npx can download it implicitly. Check exit status, logs, output existence, and the exported video itself. A browser preview does not establish render success. Verify transparent overlays in the receiving pipeline.

Respect authorization already provided. See [local rendering](../../runtime/local-rendering.md) and the [artifact contract](../../contracts/render-artifact.md).
