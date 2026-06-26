## Description: <br>
Shorten URLs via tinyurl or bitly API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other ClawHub users use this skill to generate shortened URLs through TinyURL or Bitly from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shortening a URL sends the submitted URL to TinyURL or Bitly, which can expose sensitive internal links or secrets embedded in query parameters. <br>
Mitigation: Do not shorten sensitive internal links, password-reset links, pre-signed URLs, invite links, or URLs with secrets in query parameters. <br>
Risk: Setting BITLY_TOKEN causes the skill to use the user's Bitly account for URL shortening. <br>
Mitigation: Set BITLY_TOKEN only when the user intends to use Bitly for the request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/url-shorten) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; optionally uses BITLY_TOKEN for Bitly and otherwise falls back to TinyURL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
