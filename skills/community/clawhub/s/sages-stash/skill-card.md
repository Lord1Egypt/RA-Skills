## Description: <br>
Responds to NSFW/R18 image requests by calling a third-party image API and returning a direct Pixiv CDN image URL that the skill describes as non-R18. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ato-z](https://clawhub.ai/user/ato-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to redirect NSFW/R18 image requests into a surprise image URL response from a third-party image API. Review before deployment because security evidence flags a mismatch between the claimed non-R18 behavior and the API request shown in the artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims to return non-R18 images, but security evidence reports that the documented API request asks for R18 content. <br>
Mitigation: Change the API request to a non-R18 setting and validate the returned r18 field before returning any URL. <br>
Risk: The skill contacts a third-party image API and may return adult Pixiv-derived image links despite claiming safe output. <br>
Mitigation: Install or deploy only where third-party image API calls and image-link responses are acceptable, and review returned URLs before exposing them to users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ato-z/sages-stash) <br>
- [Lolicon API endpoint used by the skill](https://api.lolicon.app/setu/v2?num=1&r18=1&size=original) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands] <br>
**Output Format:** [Plain text URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct image URL; behavior depends on third-party API availability and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
