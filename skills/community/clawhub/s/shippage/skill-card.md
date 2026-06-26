## Description: <br>
Publish HTML or Markdown to a public URL instantly, with zero configuration and first-use auto-registration for generated pages, reports, dashboards, prototypes, documentation, and product listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncle-jacky](https://clawhub.ai/user/uncle-jacky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Shippage to publish generated HTML, Markdown, JSX, and web content as shareable public pages for previews, reports, dashboards, prototypes, documentation, landing pages, and product listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish provided content to shippage.ai, making content externally accessible. <br>
Mitigation: Use it only for content approved for upload to shippage.ai and public sharing; use password protection or avoid publishing sensitive material. <br>
Risk: The bundled behavior includes a remote self-update path that can replace local skill instructions. <br>
Mitigation: Remove or disable the self-update step before installation, or require explicit human approval before downloading and replacing skill files. <br>
Risk: First-use registration may store credentials locally under ~/.shippage. <br>
Mitigation: Require clear user consent before credential storage and review local credential handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uncle-jacky/shippage) <br>
- [Shippage homepage](https://shippage.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Code, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes supplied HTML or Markdown to shippage.ai and returns a public URL; may save credentials under ~/.shippage.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
