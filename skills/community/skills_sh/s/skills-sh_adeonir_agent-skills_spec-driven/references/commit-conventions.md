# Commit Conventions

Conventional commit message format for a commit that closes a boundary.

## When to Use

When building the message for a commit that closes a boundary — the auto-commit
path in [implement.md](implement.md) and the commit step in
[quick-mode.md](quick-mode.md) both compose this format. It defines the message
only; staging, branching, pushing, and pull requests are out of scope.

## Sourcing

The message summarizes the boundary just closed. The agent making the commit
already implemented and verified the work, so it builds the message from:

- the boundary's tasks (their `Done when` and intent), and
- the actual changes made during implementation.

There is no separate diff-reading pass — the implementing agent holds the
context. Reproduce facts from what was actually written, never invented.

## Commit Types

| Type | Use when |
|------|----------|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `refactor` | Restructuring code without changing behavior |
| `chore` | Maintenance tasks, dependencies, configs |
| `docs` | Documentation changes |
| `test` | Adding or updating tests |
| `style` | Code style changes |
| `perf` | Performance improvements |
| `ci` | CI/CD configuration changes |
| `build` | Build system or external dependencies |

## Format Rules

1. **Imperative mood** — "add", "fix", "implement" (not "added", "fixes").
2. **Concise subject** — ~72 characters, a soft ceiling, not a hard limit.
3. **What and why, never where or how** — carry the user-observable effect and
   the why; keep file names, paths, mechanics, and specific values out (they
   live in the diff and the code). One exception: when the file *is* the change
   (`docs: update README`), naming it is clearer than abstracting it.
4. **Match project style** — follow the project log's scope usage
   (`type(scope):` vs `type:`); do not add or strip scope against the
   established style. A prompt directive overrides (e.g. "add scope `auth`").
5. **No attribution, no future references** — never add Co-Authored-By or
   mention upcoming work.

## Template

ALWAYS use this exact template structure:

```text
type(scope): subject

- body bullet 1
- body bullet 2
```

Omit the blank line and body when the subject already says everything. Omit
`(scope)` when the project style is scopeless.

## Body Guidelines

The body makes the commit self-sufficient — a reader understands the change from
the message alone. Write it as a **curated mini-changelog**, not a hunk-by-hunk
transcript of the diff:

- 1 to 5 bullets — the *meaningful* changes, grouped; drop incidental edits.
- Start each bullet with a lowercase imperative verb ("- add", "- remove").
- Fold in the *why* where the changes alone don't carry it.

A trivial change needs no body. When the subject already says everything
(`fix: resolve token refresh race condition`), stop there.

## Anti-Pattern: AI-slop subject

AI-slop has two opposite shapes, and "just be concrete" pushes out of the first
and straight into the second. Watch for both.

**Shape 1 — empty abstraction.** The subject names a filler word instead of the
thing that moved: filler verbs (*enhance, streamline, leverage, optimize* when
nothing was measured), filler adjectives (*robust, comprehensive, seamless*),
abstract nouns standing in for the real object (*logic, functionality, handling,
behavior*).

**Shape 2 — fake concreteness.** Over-correcting yields a subject that sounds
specific but reads like a release note: specific values are *how* not *what*
(`retry failed uploads three times` → `retry failed uploads`; the count stays in
the code), and prose locators are *where* (`... in CI` → drop it; the `ci:`
scope already carries it).

A human subject is terse and structural — it names what moved, in the
developer's own shorthand, at topic altitude. Exact values and locations stay in
the diff.

| AI-slop | Human |
|---------|-------|
| `feat: enhance error handling` | `feat: retry failed uploads` |
| `refactor: streamline auth logic` | `refactor: move token refresh into the request interceptor` |
| `chore: pin node to 20 in CI` | `ci: pin node version` |

## Examples

```text
feat: add user authentication flow

- support email/password login
- add session management
- include remember me option
```

```text
fix: resolve token refresh race condition
```

```text
refactor: extract validation logic into shared utilities
```

## Scope

This reference carries the message format only. It does **not** cover staging
strategy, branch handling, pushing, pull requests, or verification — those
belong to the workflow that composes it. The commit runs hooks normally: never
`--no-verify` or `--amend`.
