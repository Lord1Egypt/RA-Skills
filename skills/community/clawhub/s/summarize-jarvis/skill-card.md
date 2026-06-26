## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided files, private URLs, and extracted content may be sent to configured AI providers or optional extraction services. <br>
Mitigation: Avoid confidential, secret, or regulated data unless the configured providers and services are approved for that data. <br>
Risk: The skill depends on the external summarize CLI distributed through a Homebrew tap. <br>
Mitigation: Install only after trusting the Homebrew tap and verifying the summarize binary source. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/bingze00000/summarize-jarvis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON when the summarize CLI is run with --json; install metadata requires the summarize binary from the Homebrew formula steipete/tap/summarize.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
