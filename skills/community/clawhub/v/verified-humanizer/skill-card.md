## Description:

Legacy verification-guided rewriting skill that makes AI-generated text more natural while encouraging claims to stay grounded and attributable, without performing cryptographic verification or proving rewritten text is true.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutstrut](https://clawhub.ai/user/nutstrut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to rewrite stiff or formulaic AI-assisted drafts into clearer, more natural prose while preserving meaning and documenting before-and-after evaluation metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw user text, secrets, credentials, or private data could be exposed if sent to external verification services.

Mitigation: Keep rewriting and evaluation local, and send only structured evaluation metrics if optional verification is requested.

Risk: Readers may overinterpret the skill as proving human authorship, factual truth, or cryptographic verification.

Mitigation: Present it as a writing transformation and evaluation workflow, and keep explicit boundaries that it is not an AI detector, authorship proof, receipt verifier, or truth guarantee.

## Reference(s):

- [Verified Humanizer release page](https://clawhub.ai/nutstrut/skills/verified-humanizer)
- [Verified Humanizer examples](references/examples.md)
- [OpenClaw integration notes](references/openclaw-integration.md)
- [Rewrite checklist](assets/REWRITE-CHECKLIST.md)
- [Transformation report template](assets/TRANSFORMATION-REPORT-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or JSON-style structured rewrite reports with rewritten text, change notes, evaluation metrics, and optional verification status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rewriting and evaluation are intended to run locally; optional verification should use structured metrics only, not original or rewritten text.]

## Skill Version(s):

0.0.8 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
