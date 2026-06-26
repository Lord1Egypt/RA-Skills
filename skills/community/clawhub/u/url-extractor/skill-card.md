## Description: <br>
Extract and validate URLs from text, presenting results in a clear format with brief descriptions and image previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract web addresses from pasted text, validate accessibility when appropriate, and return a concise results table with titles, statuses, and image preview markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL validation may contact websites found in user-provided text, including private, internal, or tracking links. <br>
Mitigation: Use extraction without validation for sensitive text, or review and exclude private, internal, and tracking URLs before asking the agent to validate them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/url-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with a summary count, status table, and optional image-preview section.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [For more than 20 extracted URLs, validation is prioritized for the first 20 and the remainder may be listed as pending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
