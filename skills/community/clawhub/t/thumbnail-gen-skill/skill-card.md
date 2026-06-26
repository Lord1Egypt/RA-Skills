## Description: <br>
Generate ai youtube thumbnail generator images with AI via the Neta AI image generation API (free trial at neta.art/open). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sherrihidalgolt](https://clawhub.ai/user/sherrihidalgolt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to generate AI-powered YouTube thumbnail images from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The user's prompt and Neta token are sent to api.talesofai.com for image generation. <br>
Mitigation: Use a limited, revocable Neta token and review whether prompts are appropriate to send to the external image API. <br>
Risk: Passing the token inline can expose it through shared terminals, logs, screenshots, or chat transcripts. <br>
Mitigation: Avoid sharing command history or screens that include the token, and rotate the token if exposure is suspected. <br>
Risk: Installing the wrong package or listing could run a different skill than intended. <br>
Mitigation: Verify the ClawHub listing and publisher handle before installation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sherrihidalgolt/thumbnail-gen-skill) <br>
- [Neta AI token and API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL printed to stdout, with Markdown usage examples in the documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script submits an image generation request and polls until it prints a direct generated image URL or an error.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
