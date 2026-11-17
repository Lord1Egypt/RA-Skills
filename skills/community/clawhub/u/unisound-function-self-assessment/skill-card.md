## Description:

Provides postoperative rehabilitation patient self-assessment by collecting survey answers, calculating basic scores, and generating a structured assessment summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and healthcare application developers can use this skill to collect patient postoperative rehabilitation self-assessment answers, compute simple scores, and return a Markdown interpretation with structured JSON data. It is for self-assessment support and does not provide diagnosis or replace professional clinical evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patient assessment contents are sent to a fixed external medical-model API.

Mitigation: Use the skill only when that endpoint is approved for the health data being processed, users consent to external processing, and retention and compliance terms are acceptable.

Risk: Document and image inputs may contain sensitive identifiers or unnecessary clinical details.

Mitigation: Prefer JSON input with minimal identifiers and avoid uploading sensitive documents unless they are necessary for the assessment.

Risk: The runtime can fall back to preprocessing code loaded from a shared directory outside the package.

Mitigation: Ensure any shared preprocessing directory is trusted and not writable by unprivileged users before installation.

Risk: Users may mistake self-assessment interpretation for clinical diagnosis.

Mitigation: Present outputs as self-assessment support only and require professional clinical review for diagnosis or treatment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-function-self-assessment)
- [ResearchKit](https://github.com/ResearchKit/ResearchKit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [UTF-8 JSON with structured assessment data and a Markdown text field]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an appkey and sends assessment content to a fixed external medical-model API for Markdown interpretation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
