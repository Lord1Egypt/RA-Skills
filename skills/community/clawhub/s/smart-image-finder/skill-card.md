## Description: <br>
Smart Image Finder helps agents find and download images for articles, dashboards, and content using news-site extraction, Brave image search, and AI image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinbao19](https://clawhub.ai/user/justinbao19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to locate, generate, download, and verify images for article illustrations, news thumbnails, dashboards, and social posts through CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, image URLs, and generation prompts may be sent to external websites or third-party services. <br>
Mitigation: Avoid private or secret terms in searches and prompts, and review external service use before running commands. <br>
Risk: Downloaded files are written locally and may be mislabeled or unexpected content. <br>
Mitigation: Use a dedicated download folder and verify content type, file size, and source before opening files. <br>
Risk: The Brave API key can be exposed if handled carelessly in shell history, logs, or shared environments. <br>
Mitigation: Protect the Brave API key, avoid committing it, and prefer scoped environment handling for searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justinbao19/smart-image-finder) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash snippets and helper shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write downloaded image files locally and use a Brave API key when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
