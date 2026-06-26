# Agent Team Orchestration Skill

## Trigger
Set up multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.

**Trigger phrases:** "multi-agent team", "agent orchestration", "set up agents", "task routing", "agent handoff", "agent coordination"

## Process

1. **Define roles**: What each agent specialises in
2. **Task lifecycle**: inbox → spec → build → review → done
3. **Handoff protocol**: How agents pass work between each other
4. **Quality gates**: Review checkpoints before work moves forward
5. **Shared state**: How agents share context and artifacts

## Team Architecture Template

```markdown
# Agent Team: [Name]

## Roles
### Manager Agent
- Routes incoming tasks to specialists
- Reviews completed work before delivery
- Escalates blocked tasks to human
- Model: [recommended model for this role]

### Specialist Agent: [Role Name]
- Handles: [task types]
- Outputs: [deliverable format]
- Quality bar: [minimum criteria]
- Model: [recommended model]

## Task Lifecycle
1. **Inbox**: New task arrives → Manager triages
2. **Assigned**: Manager routes to specialist with brief
3. **In Progress**: Specialist works, updates shared state
4. **Review**: Manager (or reviewer agent) checks output
5. **Revision**: If quality gate fails → back to specialist with notes
6. **Done**: Approved → delivered to requester

## Handoff Protocol
- Include: task description, context, acceptance criteria, deadline
- Never: assume context from previous tasks — always be explicit
- Format: structured JSON or markdown brief

## Quality Gates
- [ ] Output matches acceptance criteria
- [ ] No hallucinated data
- [ ] Formatting matches specification
- [ ] All links/references verified
- [ ] Spell-checked and proofread
```

## Rules
- One task per agent at a time (focus > multitasking)
- Always include acceptance criteria in task briefs
- Shared state in files, not in agent memory (survives restarts)
- Model selection matters: use cheap models for bulk, expensive for judgment
