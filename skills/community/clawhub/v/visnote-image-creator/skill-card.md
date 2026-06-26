## Description: <br>
Generates XiaoHongShu-style social media images by selecting VisNote templates, merging user content with template defaults, and running a Playwright-based image generation script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherine0325](https://clawhub.ai/user/katherine0325) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent users use this skill to create XiaoHongShu-style cover, content, comparison, and tutorial images from prompts, live VisNote template data, and optional local image inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a VisNote API key and image-generation content that could be exposed if config.json is printed or shared in logs, browser history, or transcripts. <br>
Mitigation: Do not ask the agent to print config.json; keep the key out of shared transcripts and rotate it if it has been exposed. <br>
Risk: Using a custom server endpoint can send the API key and generation content to a service the user does not control. <br>
Mitigation: Use the default VisNote service or only pass --server for a domain the user explicitly trusts. <br>
Risk: Image generation depends on membership status and available generation quota, so batch use can consume paid or limited credits. <br>
Mitigation: Confirm account status and quota before large batches, and space batch requests to reduce failed or repeated generations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/katherine0325/visnote-image-creator) <br>
- [VisNote homepage](https://vis-note.netlify.app) <br>
- [VisNote profile and API key page](https://vis-note.netlify.app/profile) <br>
- [VisNote template API](https://vis-note.netlify.app/api/open/templates) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a VisNote API key in config.json, Playwright with Chromium, network access to VisNote APIs, and optional local image paths for image-based templates.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter and package metadata report v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
