# Remotion

Use Remotion for a selected React video project or template. Read the installed official modules relevant to creation, markup, Studio, and rendering; older distributions may use a best-practices layout.

Official sources: [AI skills](https://www.remotion.dev/docs/ai/skills), [rendering](https://www.remotion.dev/docs/render), [render CLI](https://www.remotion.dev/docs/cli/render).

If needed and authorized, install the official skill with `npx skills add remotion-dev/skills`. The skill does not install project dependencies. Preserve the user's package manager, lockfile, and required versions. See [dependency checks](../../runtime/external-render-dependencies.md).

Discover real entry files, composition IDs, input schemas, and render scripts from the selected project. Supply actual user text and numbers. Use frame-driven timing and explicitly manage video and audio placement. Review changes to timing and layout.

Prefer the installed project CLI or scripts. An npx invocation can download software when the dependency is absent; verify availability before using it. This is an illustrative command, not a universal project entry:

~~~bash
npx remotion render src/index.tsx ActualComposition out/final.mp4 --props=inputs/props.json
~~~

Run from the project directory and use options supported by its version. Inspect the actual export and return the [artifact](../../contracts/render-artifact.md). Upload only when a downstream cloud step needs the file.
