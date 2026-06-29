## Description: <br>
SaaS Video helps an agent submit a SaaS demo or explainer request to Pexo, upload supporting media, poll progress, and return the finished video link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, marketers, and operators use this skill to turn a SaaS or software brief, app URL, or screenshot into a publish-ready demo or explainer video for landing pages, onboarding, or sales. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends product details, URLs, screenshots, or media to Pexo's hosted service. <br>
Mitigation: Submit only material approved for external processing, and avoid confidential internal URLs, secrets, customer data, or proprietary material without approval. <br>
Risk: The skill uses a Pexo API key stored in local configuration. <br>
Mitigation: Store ~/.pexo/config as a secret, keep it writable only by the user, and do not point PEXO_CONFIG at untrusted files. <br>
Risk: Creating or revising videos can consume Pexo credits or lead to credit top-up flows. <br>
Mitigation: Confirm the user's intent before starting or retrying production, and surface credit or purchase links only when the service reports they are needed. <br>


## Reference(s): <br>
- [Pexo](https://pexo.ai) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown with shell commands, JSON script results, project links, and final asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; may upload user-provided media and return signed asset URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release, target metadata, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
