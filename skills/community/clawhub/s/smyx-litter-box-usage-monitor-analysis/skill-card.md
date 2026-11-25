## Description:

Analyzes cat litter-box videos to track visit frequency and duration, compare behavior with historical baselines, and flag changes for follow-up without diagnosing disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Cat owners and care teams in multi-cat homes, catteries, veterinary wards, and boarding centers can review litter-box visits over time and receive behavior-based alerts for unusual frequency or duration. The alerts are not a veterinary diagnosis and should be discussed with a veterinarian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports concerns about credential handling and account creation or storage.

Mitigation: Review the skill and its authentication flow with the publisher before use, and avoid supplying credentials or identity data beyond what the intended service requires.

Risk: The security assessment reports that video footage may be processed externally.

Mitigation: Confirm where footage is processed and how it is retained before uploading; avoid sharing footage until those terms are clear.

Risk: The security assessment reports a mismatch between the advertised analysis and reported implementation, and notes that a referenced local path was missing.

Mitigation: Ask the publisher to explain the implementation mismatch and restore or clarify the missing reference before relying on video-analysis results.

Risk: Behavior changes can be mistaken for a medical conclusion.

Mitigation: Treat alerts as behavior-statistics prompts only and consult a veterinarian for health concerns.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-litter-box-usage-monitor-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)
- [Analysis API error codes](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis report, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis report; Markdown summary or history table when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-cat visit frequency and duration, baseline comparisons, and behavior-based alerts; alerts are not medical diagnoses.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
