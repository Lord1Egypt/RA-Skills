## Description:

Analyzes rose leaf, shoot, and bud images or videos for common pests and diseases, grades severity, and offers general care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Home gardeners, rose growers, and garden or cut-flower teams can use the skill to review rose images or videos for common pest and disease symptoms, understand their severity, and get general care suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious due to undeclared account and identity handling and possible API-secret exposure.

Mitigation: Review identity and API-secret handling before use, and do not share credentials or identity values in prompts, logs, or reports.

Risk: The security review reports that media may be submitted externally and remote requests may occur despite an environment-only option.

Mitigation: Only submit media you are comfortable sending to the configured service, and do not rely on the environment-only option as a guarantee that no network requests occur.

Risk: The security review was partial because one referenced local path was missing.

Mitigation: Review the complete installed package and all referenced local files before deployment.

## Reference(s):

- [API documentation](artifact/skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-rose-pest-disease-detection-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report; history results can be formatted as a Markdown list.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected issues and severity with general care suggestions and, when available, a report link. Detail options are basic, standard, or JSON.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
