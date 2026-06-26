## Description: <br>
Take a blog post URL or text and generate social media posts for Twitter, LinkedIn, and promotional use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content marketers, founders, and social media operators use this skill to repurpose article URLs or text files into copy-ready Twitter or LinkedIn posts, Twitter threads, and hook variations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL inputs are fetched with curl, so private, localhost, internal, or credential-bearing URLs could expose sensitive content. <br>
Mitigation: Use public article URLs or non-sensitive text files, and avoid credential-bearing links or internal network targets. <br>
Risk: Generated posts, threads, and hooks are drafts that may be inaccurate, off-brand, or unsuitable to publish as-is. <br>
Mitigation: Review and edit all generated content before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/strd-social-post-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted social post drafts and shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a URL, text file, or inline text; supports PLATFORM, TONE, BRAND_NAME, and HASHTAGS environment variables; URL inputs require curl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
