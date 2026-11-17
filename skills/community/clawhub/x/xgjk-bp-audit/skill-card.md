## Description:

XGJK BP Audit helps agents audit BP goal systems across structural quality, upward alignment, downward handoff, gap analysis, and numerical consistency, with API-backed access to BP business records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houtonghoutong](https://clawhub.ai/user/houtonghoutong)

### License/Terms of Use:

MIT-0

## Use Case:

Business planning operators, managers, and supporting agents use this skill to audit organization or individual BP goal trees for completeness, alignment, coverage gaps, and measurable outcomes. It produces evidence-backed findings, severity labels, and concrete recommendations, and can help create child KR or Action records when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create BP child KR or Action records when write actions are used.

Mitigation: Require explicit human confirmation before any add_key_result or add_action operation and verify the parent task ID before writing.

Risk: The credentialed API client can be redirected by environment configuration.

Mitigation: Lock the API base URL to the documented production host and prevent untrusted environment overrides.

Risk: The skill accesses BP business data with an appKey.

Mitigation: Use a least-privilege appKey and keep credentials in memory or environment configuration without logging or writing them to files.

## Reference(s):

- [XGJK BP Audit on ClawHub](https://clawhub.ai/houtonghoutong/skills/xgjk-bp-audit)
- [BP Audit API Index](artifact/openapi/bp-audit/api-index.md)
- [BP Audit Usage Guide](artifact/examples/bp-audit/README.md)
- [Quality Rules](artifact/references/quality-rules.md)
- [Upward Alignment Rules](artifact/references/upward-check-rules.md)
- [Downward Handoff Rules](artifact/references/downward-check-rules.md)
- [Gap Analysis Rules](artifact/references/gap-analysis-rules.md)
- [Numerical Audit Rules](artifact/references/numerical-audit-rules.md)
- [Authentication Guidance](artifact/common/auth.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown audit reports with tables, severity labels, evidence references, recommendations, and optional shell commands for BP API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query BP business data and may create child KR or Action records only when explicitly requested.]

## Skill Version(s):

3.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
