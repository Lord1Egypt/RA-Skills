## Description: <br>
Guides an agent to shorten user-provided HTTP or HTTPS URLs through public URL-shortener services and return the resulting short link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmiu](https://clawhub.ai/user/tmiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when they need to turn a long HTTP or HTTPS URL into a shareable short link while preserving the original destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive, private, internal, or secret-bearing URLs may be disclosed to public URL-shortener services. <br>
Mitigation: Do not use the skill for login/reset links, private documents, internal hosts, signed URLs, or URLs containing secrets in query parameters. <br>
Risk: A shortener response could be malformed or point outside the expected service domain. <br>
Mitigation: Verify the returned short URL domain matches the selected backend before returning it; if all services fail, report failure instead of fabricating a link. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tmiu/url-shortener-mobile) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text short URL or concise failure message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent validates the returned short URL domain and reports failure instead of fabricating a URL when services fail.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
