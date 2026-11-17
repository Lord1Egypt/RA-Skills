# Build on Shipyard or from scratch

Look before you recommend (with a yes): the repo's file list and README, its instruction files, any skills it already has, and summaries of recent agent chats (what they asked for more than once, what went wrong). Then pick one and say why in one line.

| Choose | When |
|---|---|
| **A skill inside Shipyard** | It is about building, designing, launching, filming or running a web app on Next.js, Supabase and Vercel, and other Shipyard students would want it too. |
| **A plugin on Shipyard's shape** | It is their own product or team workflow, but they want what Shipyard has: plain-English rules, scripts that accept `--json` and `--help`, a key guard, tests that pin every lesson, and one install for every agent Shipyard supports. Copy the shape, not the app skills. |
| **From scratch** | It has nothing to do with apps (writing, research, data, a different stack) or they want something tiny. `skill-scaffold.mjs create --plugin` gives a clean start with the manifests. |

Signals from their code and chats:
- They repeat the same instructions in many chats: a skill.
- The same mistake keeps coming back: a rule plus a test, maybe a hook.
- They work in one app only: put it in that app's `AGENTS.md` or `.agents/skills/`, not a public plugin.
- They use several agents: keep the skill to `name` and `description` front matter and plain Markdown so every agent reads it.
