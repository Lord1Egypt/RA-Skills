# Examples

Real transcripts from local OpenClaw smoke tests against this skill. Each file
captures: the user prompt, the tool call(s) the model made, the raw JSON
returned, and the assistant's final reply.

Used as documentation for what the skill is good at — and as a regression
input when the manifest changes.

## File naming

`NN-short-slug.md` where `NN` is a two-digit ordinal. Group by tool:

- `01-list-my-tasks.md` through `09-resolve-url.md` — one per tool.
- `10+` — multi-tool transcripts (e.g. "summarize this URL and then show
  related tasks").

## Capturing a new example

1. Start an OpenClaw session with the skill installed locally.
2. Run the prompt.
3. Save the full exchange — prompt, every tool call with its args and full
   JSON output, and the final reply — to a new file here.
4. Strip anything sensitive (real names, internal project slugs) and replace
   with realistic placeholders.

## Example prompts that should work

Use these as your starter checklist when smoke-testing:

| Tool | Example prompt |
|---|---|
| `whoami` | "Which Quire account am I signed in to?" |
| `list_my_tasks` | "What's on my plate across all my Quire orgs?" |
| `list_project_tasks` | "Show me everything in the marketing-launch project." |
| `get_task` | "What does task #408 say?" |
| `search_tasks` | "Find high-priority backend tasks in Acme org." |
| `get_task_tree` | "Show me the full subtree under epic #200, three levels deep." |
| `list_projects` | "Which Quire projects do I have access to in Acme org?" |
| `get_project` | "Tell me about the marketing-launch project." |
| `resolve_url` | "What is https://quire.io/w/acme/marketing-launch/t/408 ?" |

If any of these picks the *wrong* tool or fabricates a `quire` command that
doesn't exist, that's a bug in [`SKILL.md`](../SKILL.md) — fix the manifest
first, then re-capture the transcript.
