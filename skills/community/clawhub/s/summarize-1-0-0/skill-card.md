## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garrisongg](https://clawhub.ai/user/garrisongg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and other agent users can use this skill to ask an agent for concise summaries of URLs, local documents, media files, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files, URLs, or extracted page content may be sent to configured AI or extraction providers. <br>
Mitigation: Use only approved providers for confidential, regulated, or internal data, and avoid submitting secret-bearing inputs unless the provider is authorized for that use. <br>
Risk: The skill depends on the external summarize CLI installed from a Homebrew tap. <br>
Mitigation: Install only after trusting the Homebrew package source and verifying the summarize CLI in the target environment. <br>
Risk: Configured provider API keys can create billing or access exposure. <br>
Mitigation: Store provider keys securely, scope them where possible, and monitor usage and billing for the configured services. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/garrisongg/summarize-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request JSON output from the summarize CLI when the --json flag is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
