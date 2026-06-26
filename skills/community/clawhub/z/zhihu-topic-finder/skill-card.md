## Description: <br>
Fetches public Zhihu hot-list data and returns ranked topic suggestions for content planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agents use this skill to inspect current Zhihu hot-list topics and identify questions that may be useful for article or answer planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live HTTPS requests to Zhihu and returns public web content that may be incomplete, stale, or untrusted. <br>
Mitigation: Use it only when network access to Zhihu is acceptable, install the requests dependency deliberately, and review returned topics before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/zhihu-topic-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON array printed to stdout with ranked topic objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes public Zhihu topic titles, excerpts, heat labels, ranking indexes, and computed opportunity scores when available.] <br>

## Skill Version(s): <br>
1.2.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
