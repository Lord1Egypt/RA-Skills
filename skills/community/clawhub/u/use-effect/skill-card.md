## Description:

Refactor React code away from direct useEffect usage by replacing effect-driven state, fetching, action relays, and resets with clearer React patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyown](https://clawhub.ai/user/liyown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code review agents use this skill to review or refactor React components, custom hooks, and frontend architecture away from direct useEffect where derived render values, event handlers, data-loading abstractions, keyed remounts, or mount-only wrappers are safer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refactoring direct useEffect usage can change lifecycle timing, remount behavior, request frequency, or state ownership in React applications.

Mitigation: Run the relevant tests or targeted checks after applying changes, with attention to loops, duplicate requests, stale state, and remount semantics.

Risk: Broad adoption may introduce lint or documentation changes that affect contributor workflow.

Mitigation: Apply no-direct-useEffect policy changes incrementally unless a full migration is explicitly requested.

## Reference(s):

- [useEffect Replacement Patterns](references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/liyown/skills/use-effect)

## Skill Output:

**Output Type(s):** [Analysis, Code, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown guidance with code snippets, patch-ready recommendations, and optional shell commands or configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose lint or contributor guidance updates during broader React adoption work.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
