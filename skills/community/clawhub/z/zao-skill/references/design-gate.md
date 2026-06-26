# Design Gate

## Part 1 — Init Design
Load when Phase 1 Step 1 in purpose of fully understand the user's intent and workflow

### Interview and Crystalize the workflow

1. Interview to clarify use cases, tasks and domain and propose to agree on a skill name.

2. **Grill systematically**  — Dig deeper about every aspect of this idea until a shared understanding with the user is reached. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

3. Once the picture is clear, give your **independent judgment**:
   - Is a skill even useful here, or would the agent do fine without it?
   - Is it too trivial for a skill? (If yes → stop; handle conversationally.)
   - Is it too complex for one skill?  
     If complex, propose a breakdown. Focus on the **first piece** to start.  
     Keep the remaining pieces as a todo list in `<skill-name>/.wip/`.

4. If the idea passes (skill is useful and appropriately scoped) AND no existing workflow available:
   - Suggest that the user complete a **real task** in conversation to crystallize the workflow.
   - Capture : triggers, input/output formats, example files, success criteria, edge cases, failures/corrections, tools, project‑specific facts/conventions/constraints.
   - Keep the conversation and artifacts as a **living document** under `<skill-name>/.wip/` for output later; do not clean intermediate notes.


## Part 2 —Enhance Design
Load when Phase 1 Step 2 user chooses "Enhance".

- Clarify differences between the existing skill(s) and the user's intent (from Step 1 workflow extraction).

- Recommend which skill(s) to base on, borrow from, or discard.

- **Grill systematically**  — Dig deeper about every aspect of this enhancement plan until a shared understanding with the user is reached. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

- Confirm shared understanding and append enhancement decisions to the Design Context section in `workflow-extraction.md`.

**Decision format** (append to Design Context):
```
### Enhancement Decisions
- **Base on**: [skill-name] — [why]
- **Borrow from**: [skill-name] — [what pattern]
- **Key differences from intent**: [list]
```
