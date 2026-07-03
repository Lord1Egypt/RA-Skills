## Description: <br>
Create, publish, share, and verify Tunly artifacts with privacy and versioned links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seaguest](https://clawhub.ai/user/seaguest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and review stakeholders use this skill to publish agent-created artifacts as durable Tunly links with explicit access mode, versioning, and verification evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Artifacts may contain secrets, private paths, customer data, screenshots, or other sensitive content before publishing. <br>
Mitigation: Review and redact artifacts before publishing, choose the intended access mode, and treat binary media as manual privacy review items. <br>
Risk: A published link may not enforce the intended privacy or durability contract. <br>
Mitigation: Verify the latest link, immutable version or revision link, content identity, Tunly serving path, and access behavior before reporting success. <br>


## Reference(s): <br>
- [Tunly Artifact Share](https://clawhub.ai/seaguest/skills/tunly-artifact-share) <br>
- [Example Prompts](references/example-prompts.md) <br>
- [Tunly Artifact Share Feature Showcase](references/feature-showcase.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final responses include the latest URL, immutable version URL or revision id, access mode, verified checks, and exact unverified gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
