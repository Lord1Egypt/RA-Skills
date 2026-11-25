# Local rendering engines

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Render engine selection](#engine-selection)
- [Hyperframes](#hyperframes)
- [Remotion](#remotion)

<a id="engine-selection"></a>

## Render engine selection

Use an existing FFmpeg installation for simple trimming, joining, cropping, subtitles, and mixing. API resource queries do not require a render engine.

For programmatic video, preserve the user's selected engine or the existing template's engine and version. Otherwise, React compositions suit [Remotion](#remotion); HTML/CSS compositions suit [Hyperframes](#hyperframes). Both can produce full videos, clips, or overlays when the actual project supports them.

Official engine skills are external dependencies. Keep project packages in the video project, not in Vibbit Skills. Read [dependency checks](../runtime/external-render-dependencies.md) and only the selected engine's relevant official modules.

Cloud `MEDIA_PRODUCTION` composes media; it does not execute either local engine or deploy a third-party render service. Follow the [render artifact contract](../contracts/render-artifact.md).

<a id="hyperframes"></a>

## Hyperframes

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

Respect authorization already provided. See [local rendering](../runtime/local-rendering.md) and the [artifact contract](../contracts/render-artifact.md).

<a id="remotion"></a>

## Remotion

Use Remotion for a selected React video project or template. Read the installed official modules relevant to creation, markup, Studio, and rendering; older distributions may use a best-practices layout.

Official sources: [AI skills](https://www.remotion.dev/docs/ai/skills), [rendering](https://www.remotion.dev/docs/render), [render CLI](https://www.remotion.dev/docs/cli/render).

If needed and authorized, install the official skill with `npx skills add remotion-dev/skills`. The skill does not install project dependencies. Preserve the user's package manager, lockfile, and required versions. See [dependency checks](../runtime/external-render-dependencies.md).

Discover real entry files, composition IDs, input schemas, and render scripts from the selected project. Supply actual user text and numbers. Use frame-driven timing and explicitly manage video and audio placement. Review changes to timing and layout.

Prefer the installed project CLI or scripts. An npx invocation can download software when the dependency is absent; verify availability before using it. This is an illustrative command, not a universal project entry:

~~~bash
npx remotion render src/index.tsx ActualComposition out/final.mp4 --props=inputs/props.json
~~~

Run from the project directory and use options supported by its version. Inspect the actual export and return the [artifact](../contracts/render-artifact.md). Upload only when a downstream cloud step needs the file.
