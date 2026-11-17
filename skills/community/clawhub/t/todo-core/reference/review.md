# Independent reviews (optional, never a required stage)

Loaded by `/todo-plan` and `/todo-continue` only for a root that qualifies. Part of the `todo` core skill.

A root **qualifies** when its complexity is `high` or it touches security, data migration, concurrency or a public interface (a command, flag, endpoint, config key or exported symbol). It is never offered for a `low` or `mid` root that touches none of these. Each review is offered once per root, and the user can also ask for one ("review this plan", "review this root", `--review`, or a line under the plan doc's **Open questions**). Neither review is required, and declining one changes nothing else.

**Reviewer.** With a subagent tool, a new agent gets only the inputs listed below. It reads and comments, returning spec compliance findings first, then quality findings. It never edits files or runs tests. Without a subagent tool, say so and offer a review in a new session started from those same inputs.

**External tool.** If the project already uses a design-review skill or tool (for example EGM), run it on the same inputs instead. This repository neither bundles nor requires one.

## Design review (before the first build node)

- **When:** `/todo-plan` offers it once for a qualifying root, and must never block a plan on it.
- **Inputs:** the plan doc, the root and its children as written in `TODO.md`, and the `Ref` path.
- **Outcome:** findings the user accepts go through `/todo-plan --revise`, so they land in **Revisions** with the reason. Declined or unresolved findings become a bullet under **Open questions**. With no review, the plan simply proceeds.

## Root review (before the drain)

- **When:** `/todo-continue`, after a qualifying root's refresh from the base (step 10.4.1) and before the last gate, asks once "review the whole root before it drains? (yes / no)". A recorded answer is not asked again: a plan doc line under **Open questions**, or an earlier reply in this conversation.
- **Inputs:** the whole root diff (`git diff <base>...<root branch>`; no git: the root's `files:`), the plan doc it links, the root's `Ref`, and the tree's task lines.
- **Outcome:** a valid finding inside the root's task line is fixed on the root branch. Commit it as `fix(<scope>): <title>` with `Refs: <ROOT-ID>`, then rerun the root's `Done when` and the regression before the last gate. A finding outside the root's task line goes to the report as a `/todo-add "<description>" --from <ROOT-ID>` command. A declined finding becomes a bullet under the plan doc's **Open questions** (no plan doc: the report). Fixing findings is not an attempt, and the root is not blocked unless a fix makes `Done when` or the regression fail ("Test failures").
