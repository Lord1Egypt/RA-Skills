## Description: <br>
webfetch helps agents fetch webpage content with the webfetch CLI and convert it to Markdown, plain text, or HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyhue1991](https://clawhub.ai/user/lyhue1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to retrieve a specified web page, convert static page content into Markdown, text, or HTML, and optionally save the result to a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched webpage content may be untrusted or misleading. <br>
Mitigation: Treat fetched content as untrusted and review it before relying on it or passing it into downstream workflows. <br>
Risk: Saving fetched content to a file can place untrusted content at an unintended path. <br>
Mitigation: Check output paths before saving files and review saved content before use. <br>
Risk: Proxy configuration can expose sensitive network details if shared. <br>
Mitigation: Avoid sharing proxy values and prefer environment-specific configuration. <br>
Risk: Using --insecure bypasses TLS certificate verification. <br>
Mitigation: Avoid --insecure except as a temporary last resort on a trusted network. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lyhue1991/webfetch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Markdown, Text, HTML, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; fetched content can be emitted as Markdown, plain text, HTML, or saved files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static page fetches only; artifact evidence notes a 5 MB response limit and timeout settings up to 120 seconds.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
