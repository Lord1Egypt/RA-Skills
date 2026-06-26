## Description: <br>
Reads public Twitter/X tweet content from a shared tweet link and returns structured tweet details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawzhang](https://clawhub.ai/user/sawzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to read a public Twitter/X status URL and return the tweet author, timestamp, engagement counts, text, and media or link notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public tweet URLs requested by the user are sent to fxtwitter or vxtwitter third-party proxy APIs. <br>
Mitigation: Use the skill for public tweet links only and avoid submitting sensitive or private URLs. <br>
Risk: Thread or long-tweet content may be incomplete when a proxy returns only the first tweet or visible body. <br>
Mitigation: Tell the user when the returned content may be partial and ask for additional thread links when needed. <br>
Risk: Fallback search or linked-article fetching can expand the task beyond reading the original tweet. <br>
Mitigation: Ask for confirmation before using search fallback or fetching external linked articles. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured tweet details and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tweet text, author metadata, engagement counts, media links, and notes about incomplete threads or long tweets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
