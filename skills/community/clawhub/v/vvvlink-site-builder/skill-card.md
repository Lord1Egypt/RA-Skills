## Description: <br>
Build and publish websites on vvvlink.com by creating HTML sites, uploading them to the VVVLink API, and publishing them with unique subdomain URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vladlat](https://clawhub.ai/user/vladlat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, update, and publish static websites, landing pages, portfolios, and business pages through VVVLink. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated sites may be published publicly and may send site-related content to VVVLink. <br>
Mitigation: Review private, client, legal, and unreleased business content before publishing. <br>
Risk: The skill creates and stores a VVVLink account credential locally. <br>
Mitigation: Keep the local VVVLink config protected and do not share the API key. <br>
Risk: Delete or bulk cleanup requests can remove hosted site versions. <br>
Mitigation: Confirm the intended site and scope before deleting or cleaning up hosted sites. <br>


## Reference(s): <br>
- [VVVLink API Reference](references/api-reference.md) <br>
- [Website Development Rules](references/website-development-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/vladlat/vvvlink-site-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with generated website files, configuration steps, and bash/curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish generated static sites publicly and return hosted vvvlink.com URLs.] <br>

## Skill Version(s): <br>
1.8.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
