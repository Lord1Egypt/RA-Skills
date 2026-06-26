## Description: <br>
Fetches recent clean jokes from Reddit's r/tiodopave community, filters for minimum score and adult-content indicators, and returns one joke as plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents can use this skill to retrieve a recent Portuguese joke from r/tiodopave for casual responses or entertainment workflows. It is intended for users who want real Reddit-sourced jokes rather than AI-generated joke text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit content is user-generated, so unsuitable or low-quality text can remain despite score, NSFW, and keyword filtering. <br>
Mitigation: Review returned jokes before publishing them in customer-facing or brand-sensitive contexts. <br>
Risk: The skill depends on live Reddit access and can fail when Reddit is unavailable, rate-limited, or returns no eligible posts. <br>
Mitigation: Handle command failures gracefully and provide fallback copy when no joke is returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runawaydevil/tiodopave) <br>
- [r/tiodopave subreddit](https://www.reddit.com/r/tiodopave) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a selected post title and, when present, body text after URL and Reddit formatting cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
