## Description:

Cross-shift continuity and unresolved issue tracking system for restaurant and franchise operators. Captures wins, bottlenecks, and handoffs at end of shift, then actively tracks unresolved urgent items across shifts until they are confirmed closed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcphersonai](https://clawhub.ai/user/mcphersonai)

### License/Terms of Use:

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

## Use Case:

Restaurant operators, franchise managers, and shift leads use this skill to capture end-of-shift reflections, preserve handoff context, and track urgent unresolved issues until they are closed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reflections, issue histories, and exports can contain confidential operational details such as staffing, customer incident, maintenance, or food-safety context.

Mitigation: Treat exports as confidential and confirm that the host platform and qsr-store-memory-engine enforce expected namespace, authorization, audit, retention, and deletion controls.

Risk: Operator-authored free-text fields may include unnecessary personal or customer-identifying details.

Mitigation: Prefer roles over names, omit prohibited identifiers, and ask whether a personal detail is operationally necessary before recording it.

Risk: Persistent cross-shift tracking depends on the companion store memory engine and host controls.

Mitigation: Verify the store-scoped memory namespace before deployment; if it is unavailable, use the skill only in session-only mode without cross-conversation persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcphersonai/skills/qsr-shift-reflection)
- [Observa getting started publisher notice](https://mcphersonai.com/observa/getting-started?utm_source=clawhub&utm_medium=skill&utm_campaign=observa-getting-started&utm_content=qsr-shift-reflection)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational Markdown with structured text records, issue boards, setup confirmations, exports, and digest summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are scoped to the operator's store context and may include confidential operational information.]

## Skill Version(s):

2.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
