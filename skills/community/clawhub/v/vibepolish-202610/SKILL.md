\---  
name: vibepolish  
description: Use when opening a single-file HTML demo or unbundled static HTML/CSS/JS project in VibePolish, with a connected CDP style provider for WYSIWYG editing and export.  
\---

# VibePolish

Open an HTML demo or unbundled static project in a connected VibePolish workbench.

## Workflow

1. Determine the runtime source kind before choosing a launcher command.

- A directory is a project.
- For an HTML file, inspect its local `src`, `href`, `srcset`, CSS `url()`, script import, and similar resource references. If it depends on files beside it or under a local asset directory, treat it as a project.
- Use `--source` only when the HTML can run independently of its filesystem location, with its required CSS, JavaScript, and media embedded or remotely addressed.
- Do not classify an HTML file as single-file merely because the user named that file directly.
- Never copy local assets or create a replacement entry to make single-file mode work.

1. Run exactly one standalone launcher command from this skill directory.

For a single HTML file:

```bash
node <skill-root>/scripts/open-runtime.mjs --source <source.html>
```

For an unbundled static project:

First list existing HTML files:

```bash
rg --files <project-root> -g '*.html' -g '*.htm'
```

Inspect the plausible pages and identify the entry the user intends to open. Prefer an established entry when one exists, but do not assume `index.html`, create a new entry, or modify the project during discovery. If multiple plausible entries remain, ask the user which page to open.

Then pass the confirmed project-relative entry explicitly:

```bash
node <skill-root>/scripts/open-runtime.mjs --project <project-root> --entry <entry.html>
```

1. Keep the launcher process running and leave its Chrome window open for the user.
2. Report `CDP_PORT`, `PROJECT_PORT` when present, and the opened address.
3. Do not replace the launcher with a generic static server or open the generated wrapper directly; those paths do not install the CDP provider.
4. Do not edit or normalize the source HTML, infer semantic states, scan hidden business states, build state chips, generate previews, or rewrite the demo state machine.

## Usage Boundary

- Launching connected Chrome is a delivery step, not a runtime regression test.
- Do not exercise snapshot, delayed selection, editing, apply/cancel, or export flows unless the user asks for verification or the generated page fails to open normally.
- Runtime quality is owned by VibePolish's development tests and engineering guards, not repeated by every skill invocation.
