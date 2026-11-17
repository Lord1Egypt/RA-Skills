# Deploy notes (verbatim)

Captured during prototype build. The deploy target repo is
`wipcomputer/wip-websites-private`, with the homepage going at
`wip.computer/index.html` (replacing the existing LUME dark-theme page).

## From the local agent's framing brief

> No React, no JSX, no build step, no framework runtime.
>
> If you prototype in a framework, also export a plain static version,
> and the static version is the deliverable.

## What this export is

The framework prototype. Use it as the visual + interaction reference for the
vanilla static port. See BEHAVIOR.md for the complete behavior surface.

## Repo structure (existing wip-websites-private layout)

```
wipcomputer/wip-websites-private
├── SKILL.md
├── deploy-manifest.json
├── deploy.sh
└── wip.computer/
    ├── index.html         ← REPLACE THIS (currently LUME dark theme)
    ├── agent.txt          ← already linked from footer
    ├── assets/
    ├── day-63/
    ├── install/
    ├── listen (submodule)
    ├── lume/
    └── usr/
```

## External URLs the homepage points at (must stay live)

- `https://wip.computer/login?next=/demo` — the three Demo Kaleidoscope CTAs
- `https://github.com/wipcomputer` — letter inline link + Connect col
- `https://x.com/wipcomputer` — Connect col
- `https://wip.computer/agent.txt` — footer Tools col
- `https://wip.computer/legal/privacy/en-ww/` — footer
- `https://wip.computer/legal/internet-services/terms/site.html` — footer

## Brand and copy

- Title: "WIP Computer — Every AI. One experience."
- Founder letter is verbatim. Do not paraphrase.
- The 8 architecture entries are verbatim. Do not reorder.
- The 4 typewriter groups are verbatim. Do not edit individual payoffs.
