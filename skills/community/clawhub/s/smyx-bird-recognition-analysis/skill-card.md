## Description: <br>
Identifies bird species in images or videos, supports recognition of at least 500 common species, and can return structured bird-recognition reports or historical report listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, birdwatchers, ecological observers, and monitoring teams use this skill to identify bird species in supplied images or videos and to review prior bird-recognition reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bird images, videos, and a user-provided username or phone-like open-id are sent to the Lifeemergence cloud service for analysis. <br>
Mitigation: Use only when users consent to cloud processing, avoid submitting sensitive media, and keep HTTPS/TLS transfer enabled. <br>
Risk: The security scan says the skill under-discloses account creation, local session-token storage, and historical report access. <br>
Mitigation: Review the publisher's disclosures and local credential storage behavior before installation, and limit use of history retrieval to expected user-owned reports. <br>
Risk: The security guidance calls out broad backend helpers, stale health-analysis documentation, and an exposed key. <br>
Mitigation: Before production use, narrow the package to bird-specific code, remove stale documentation and unused helpers, and rotate or remove exposed credentials. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-bird-recognition-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report text, with optional shell command examples and optional saved result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided open-id and an image, video, or public media URL; local uploads are documented as limited to common image/video formats up to 10 MB.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence; SKILL.md frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
