## Description: <br>
Cross-shift continuity and unresolved issue tracking system for restaurant and franchise operators. Captures wins, bottlenecks, and handoffs at end of shift, then actively tracks unresolved urgent items across shifts until they are confirmed closed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcphersonai](https://clawhub.ai/user/mcphersonai) <br>

### License/Terms of Use: <br>
CC BY-NC 4.0 with McPherson AI commercial-use clarification <br>


## Use Case: <br>
Restaurant operators, franchise managers, and shift leads use this skill to capture end-of-shift reflections, create urgent handoff records, surface unresolved items during operator-initiated check-ins, and generate operational digests for a single store or multi-location rollout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background-tracking wording could be misread as autonomous monitoring. <br>
Mitigation: Confirm the release states that issue checks run only during operator-initiated shift check-ins or on-demand commands, with no daemon, polling, scheduled alerts, or automatic cross-session monitoring. <br>
Risk: Shift reflections and open issue records may contain confidential operational details or unnecessary personal information. <br>
Mitigation: Use operational roles instead of names when possible, omit the listed PII categories, and keep records scoped to the relevant store namespace. <br>
Risk: Persistent full-store archival depends on a companion memory skill and host-platform controls. <br>
Mitigation: Verify that the QSR Store Memory Engine is available for persistence, or run in session-only mode; rely on the host platform for authentication, authorization, encryption, audit logging, retention, and deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcphersonai/qsr-shift-reflection) <br>
- [McPherson AI publisher profile](https://clawhub.ai/user/mcphersonai) <br>
- [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and structured plain text records for shift reflections, open issue records, issue boards, exports, and weekly digests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records are intended to be scoped to a store namespace; persistence depends on the companion QSR Store Memory Engine or the host session.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
