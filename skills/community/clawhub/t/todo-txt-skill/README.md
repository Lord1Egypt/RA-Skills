# todo.txt Skill for AI Agents

![](./assets/demo.gif)

A durable and light ToDo list your agent can use across conversations.

Ask things like *"add buy milk to my groceries"*, *"what's on my list for work?"*, or *"mark the dentist task as done"* — the skill translates these into the right `todo.sh` commands, runs them, and shows you the updated list.

> **Why this exists:** the todo.txt format is a plain-text, future-proof, tool-agnostic way to track tasks. This skill teaches  how to drive the official CLI so you can manage that file conversationally — no public skill for it existed, so here it is.

## Who is it for?

People running AI agents who want to keep their task list durable, light and portable.

## Features

- 🗣️ **Natural language → CLI** — describe what you want; the skill picks the right command and flags.
- ➕ **Full task lifecycle** — add, list, filter, prioritize, edit, complete, archive, and delete tasks.
- 🏷️ **Projects & contexts** — understands `+project` and `@context` tags, plus `key:value` metadata like `due:2026-06-30`.
- 🔧 **Self-installing** — if `todo.sh` isn't installed, the skill runs a bundled script (`scripts/install_todo_cli.sh`) that sets it up on macOS or Linux.
- 📄 **Durable, plain text, yours forever** — your tasks live in a portable `todo.txt` file you fully control, readable with any text editor for as long as you need it, with no app or vendor lock-in.

## Installation

Paste the one-liner for your platform:

```
npx skills add aguilera-ee/todo.txt-skill
```

## Usage

Invoke it explicitly with a slash command, or just describe what you need and let your agent pick the skill:

```
/todo.txt-skill list all tasks
/todo.txt-skill add "buy milk +groceries @store"
/todo.txt-skill mark task 3 as done
```

Natural-language prompts work too:

> "Add a high-priority task to call the dentist tomorrow, tagged health."

> "Show me everything in the +work project."

> "I finished the report — cross it off."

After any change, the skill re-lists your tasks so you always see the current state.

## todo.txt format cheatsheet

| Element        | Syntax              | Example                              |
|----------------|---------------------|--------------------------------------|
| Priority       | `(A)` … `(Z)`       | `(A) Call dentist`                   |
| Completion     | `x ` prefix + date  | `x 2026-06-10 Buy groceries`         |
| Creation date  | `YYYY-MM-DD`        | `2026-06-01 Write report`            |
| Project tag    | `+project`          | `+health`                            |
| Context tag    | `@context`          | `@phone`                             |
| Metadata       | `key:value`         | `due:2026-06-30`                     |

Full example:
```
(A) Call dentist @phone +health due:2026-06-15
(B) 2026-06-01 Write report +work @computer
x 2026-06-10 2026-06-01 Buy groceries +errands @store
```

See the [todo.txt format spec](https://github.com/todotxt/todo.txt) for the complete definition.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to propose changes, test the skill, and open a pull request.

## Acknowledgements

- The [todo.txt CLI](https://github.com/todotxt/todo.txt-cli) and the [todo.txt format](https://github.com/todotxt/todo.txt), created by Gina Trapani and maintained by the todo.txt community.

## License

[MIT](./LICENSE) © Eduardo Aguilera. This skill is an independent project and is not affiliated with the todo.txt project or Anthropic.
