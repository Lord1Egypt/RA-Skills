# Case Study: Todo Accelerator in Action

These examples demonstrate the full lifecycle using the [AutoResearch](https://github.com/karpathy/autoresearch) project as the scenario.

`<CMD>` = `python3 <skill-dir>/scripts/todo.py --config <workspace>/todo-accelerator-config.yaml`

---

## Case 1: Adding a New To-Do

**User:** I have a new task — I want to research what AutoResearch is and how to use it. Here's the repo: https://github.com/karpathy/autoresearch

**Agent:** I'd be happy to add this as a to-do. Let me collect some details:

1. What results do you expect from this research?
2. What specific requirements or questions should be addressed?
3. Should this be prioritized? (0 = normal, higher = more urgent)

**User:** I want a summary of what it does and how to set it up. Requirements: read the README, try running the demo, and write up findings. Priority 1.

**Agent:** Got it. Creating the to-do now.

```bash
<CMD> add-todo \
  --name "Research AutoResearch" \
  --targets "Summary of features and setup guide" \
  --requirements "Read the README thoroughly" "Try running the demo" "Write up findings" \
  --priority 1
```

> Created note: /path/to/TODOs/Research AutoResearch.md
> Added to-do: [[Research AutoResearch]]

*End of session.*

---

## Case 2: Heartbeat Picks Up the To-Do

During a heartbeat event, the heartbeat instruction tells the agent to call `work-on-todo`:

```bash
<CMD> work-on-todo
```

The script selects "Research AutoResearch" (highest priority), moves it from Ideas to 推进中, and returns:

```
## Working on: Research AutoResearch
Note: /path/to/TODOs/Research AutoResearch.md
Iteration: 1

### Expected Results
- Summary of features and setup guide

### Unresolved Issues
- [ ] Read the README thoroughly
- [ ] Try running the demo
- [ ] Write up findings
```

The agent follows the returned prompt and the skill's instructions — especially `references/processing-work-on-todo.md`. It reads the README, records concise findings in the "Investigation and Problems" section of the note, and writes preliminary results in the "Target" section.

When done (or when stuck), the agent calls commit with the requirements it completed:

```bash
<CMD> commit \
  --name "Research AutoResearch" \
  --completed "Read the README thoroughly" "Try running the demo"
```

> Committed: checked off 2 requirement(s).
> Moved [[Research AutoResearch]] to 审阅中.
>
> Remaining unchecked (1):
>   - [ ] Write up findings

*End of heartbeat session.*

---

## Case 3: User Requests Work on a Specific To-Do

*After review, the user moves "Research AutoResearch" back to Ideas (one requirement remains).*

**User:** Can you work on that AutoResearch task?

**Agent:** Let me check what's pending.

```bash
<CMD> list-pending
```

> Pending to-dos (Ideas):
>   - Research AutoResearch (priority: 1)
>   - Write blog post (priority: 0)

**Agent:** I see "Research AutoResearch" (priority 1) — is that the one you mean?

**User:** Yes, that's it.

**Agent:** Starting work on it now.

```bash
<CMD> work-on-todo --name "Research AutoResearch"
```

```
## Working on: Research AutoResearch
Note: /path/to/TODOs/Research AutoResearch.md
Iteration: 2

### Expected Results
- Summary of features and setup guide

### Unresolved Issues
- [ ] Write up findings

### Previous Results
Preliminary feature summary documented.

Previous findings are in the "Investigation and Problems" section of the note. Review before starting; record any new discoveries in the same section. Keep entries concise — facts and conclusions only, no filler.
```

The agent writes up the final findings, then commits:

```bash
<CMD> commit \
  --name "Research AutoResearch" \
  --completed "Write up findings"
```

> Committed: checked off 1 requirement(s).
> Moved [[Research AutoResearch]] to 审阅中.

*End of session.*
