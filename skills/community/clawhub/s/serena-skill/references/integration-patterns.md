# Integration patterns

## Plugin + skill split

Keep these concerns separate:

- plugin: mechanics, process lifecycle, config, tool exposure
- skill: workflow judgment, heuristics, fallback rules

Do not overload the skill with installation details that belong in plugin docs. Use the skill to teach another agent **how** to use Serena well after the capability already exists.

## Good prompts that should trigger the skill

- "Trace where this service is used in the repo"
- "Update the retry logic in the worker"
- "Find the auth middleware and adjust token validation"
- "Figure out which symbols reference this class"
- "Make a targeted change in this existing codebase"
- "Use Serena on this repo and tell me where X is defined"
- "Rename this symbol safely across the codebase"

## Cases where the skill may not be needed

- "Create a new hello-world script"
- "Add a one-line print statement in this file I already opened"
- "Draft a brand-new module from scratch with no repo context"
- "Write a brand-new README from scratch"

## Good integration instructions for another agent

These prompting patterns usually produce good Serena behavior.

### General repo inspection

> Use Serena on the target repo. Activate the project first, then find the relevant symbols, inspect references, and read only the code needed to answer.

### Targeted code edit

> Use Serena for this existing codebase. Activate the project, locate the exact symbol, inspect references if behavior may ripple outward, then make the narrowest semantic edit possible.

### Safe rename flow

> Use Serena to rename the symbol semantically. Confirm the symbol identity first, inspect references if needed, then use the rename tool instead of manual text replacement.

## Anti-patterns

Avoid these behaviors when Serena is available:

- reading many whole files before trying symbol lookup
- making multi-file text edits before checking references
- using passthrough tools first when normalized tools already exist
- rewriting an entire file for a small symbol-level change
- guessing the symbol identity when multiple matches are plausible

## Suggested decision tree

1. Is this an existing repo with non-trivial structure?
   - yes → Serena is likely a good fit
   - no → normal file tools may be simpler
2. Is the user asking about references, structure, or a targeted existing edit?
   - yes → prefer Serena
3. Is the exact file and line already obvious and tiny?
   - yes → Serena may be unnecessary overhead
4. Do you only need to inspect active Serena sessions or debug session state?
   - yes → use `serena_session_status`
5. Do you genuinely need project-context shell execution rather than semantic tools?
   - yes → consider `serena_execute_shell_command` sparingly
6. Is the needed Serena capability missing from normalized tools?
   - yes → consider passthrough if available
7. Did Serena fail or return ambiguous results?
   - yes → explain briefly and fall back carefully
