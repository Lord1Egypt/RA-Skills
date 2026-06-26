## Description: <br>
Create, edit, and manage WeChat Official Account articles via the official WeChat API, including access token handling, image uploads, draft creation and updates, publishing, and WeChat-compatible HTML formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slientrain-new](https://clawhub.ai/user/slientrain-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and developers use this skill to draft, format, validate, upload media for, and publish WeChat Official Account articles through the official API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat Official Account credentials and access tokens. <br>
Mitigation: Keep credentials scoped and private, and provide tokens only when the agent needs to perform an explicit WeChat API action. <br>
Risk: The skill can change or publish official-account content. <br>
Mitigation: Require explicit human confirmation before uploads, draft updates, publication, or deletion, and review generated article content and API payloads before submission. <br>
Risk: Bundled drafts and idea notes may be mistaken for operational instructions. <br>
Mitigation: Treat bundled drafts and notes as evidence or examples only, and base operational actions on the user's current request. <br>


## Reference(s): <br>
- [WeChat layout template](references/templates.md) <br>
- [Editorial review checklist](references/review-checklist.md) <br>
- [Prompt examples](references/prompt-examples.md) <br>
- [Image generation helper](scripts/generate_images.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, HTML article content, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WeChat API payloads, generated article assets, draft IDs, media IDs, and preflight check results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
