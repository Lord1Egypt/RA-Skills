# Socrates Protocol

Use this protocol to improve thinking quality before acting. Prefer one round. Open a second round only when the first round still leaves a material decision unresolved.

## Decision Gate

Choose one of these entry modes before doing any real work:

- Skip: casual chat, direct translation, formatting-only edits, or fully specified micro-fixes.
- Compressed Round 1: bounded work that still matters, such as a small code change with a clear target and a modest blast radius.
- Full Round 1: planning, architecture, non-trivial coding, refactors, task decomposition, or delegation.

## Round 1

Answer these five questions in order. Keep each answer short and concrete.

1. Goal and done criteria
   - What problem am I solving?
   - What would count as a successful result?
2. Knowns, unknowns, and assumptions
   - What facts do I already have?
   - What important details are missing?
   - Which assumptions am I making for now?
3. Risks and failure modes
   - What is most likely to fail?
   - What would cause rework, wasted effort, or hidden regressions?
4. Approach selection
   - Which approach should I use?
   - Why is it better than the main alternatives for this task?
5. Next actions and delegation
   - What should happen now?
   - What should be delegated, if anything?
   - In what order should the work move?

## Round 2

Run a second round only when Round 1 still leaves a high-impact decision unresolved.

### Triggers

- The task includes an architecture-level or hard-to-reverse decision.
- Key constraints are missing and acting now is likely to cause rework.
- Multiple sub-agents are needed and ownership or interfaces are still unclear.
- Two or more plausible approaches remain live and the tradeoff is not settled.

### Round 2 rules

- Ask only the follow-up questions needed to close the decision gap.
- Do not repeat all five Round 1 questions.
- Stop after the key uncertainty is resolved or clearly surfaced to the user.

## Output Contract

Use this section order:

```md
Socratic Pass
Round 1
- Goal and done criteria: ...
- Knowns, unknowns, assumptions: ...
- Risks: ...
- Chosen approach: ...
- Next actions and delegation: ...

Round 2
- Trigger: ...
- Follow-up question(s): ...
- Resolution: ...

Action Plan
1. ...
2. ...
3. ...

Delegation Contract
- Goal: ...
- Done criteria: ...
- Constraints: ...
- Deliverable: ...
- Run Socrates first: ...
```

### Section rules

- Always include `Socratic Pass`.
- Always include `Action Plan`.
- Include `Delegation Contract` only when sub-agents are involved.
- Include `Round 2` only when a real trigger fired.
- Keep the whole response compact. Most tasks should complete with Round 1 only.

## Delegation Contract

Use this handoff shape when work moves to a sub-agent:

```md
Goal:
Done criteria:
Constraints:
Deliverable:
Run Socrates first:
- Do a concise mini Socratic pass before acting.
- Use a second round only if risk or ambiguity remains unresolved.

Report back:
- Socratic Pass
- Action taken
- Results or blockers
```

## Mini Pass For Child Agents

Require every child agent to answer these before taking action:

1. What is the goal and what counts as done?
2. What is known, unknown, and assumed?
3. What is the main risk?
4. What approach will I use?
5. What is the immediate next step?

Keep the child pass short. Default to one round.

## Anti-Patterns

- Do not turn the pass into abstract philosophy.
- Do not repeat the user request in different words.
- Do not generate a second round just to look thorough.
- Do not hide blocking uncertainty inside self-reflection; ask the user when needed.
- Do not let the pass replace real execution. It should sharpen action, not delay it.
