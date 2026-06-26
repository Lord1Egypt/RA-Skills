## Description: <br>
Scores YouTube videos from 1-10 based on a user's learning goals and persona, with summaries, alignment analysis, feed retrieval, and usage checks through the WorthClip API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IvanStancich](https://clawhub.ai/user/IvanStancich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to evaluate YouTube videos against a WorthClip persona and learning goals, inspect a scored feed, and check API usage from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a WorthClip API key and requested YouTube video IDs or feed filters to WorthClip's API. <br>
Mitigation: Use a revocable WorthClip API key, avoid processing content the user does not intend to share with WorthClip, and rotate the key if exposure is suspected. <br>
Risk: WorthClip account-changing actions such as channel tracking or persona and goals updates could affect future scoring behavior. <br>
Mitigation: Keep account, channel, persona, and goals changes explicitly user-directed before invoking any related API behavior. <br>
Risk: Remote API limits or asynchronous scoring can delay or fail a scoring request. <br>
Mitigation: Respect rate-limit responses and surface timeout or error responses to the user instead of treating missing scores as final results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IvanStancich/worthclip-youtube-video-scorer) <br>
- [WorthClip](https://worthclip.com) <br>
- [WorthClip developer API keys](https://worthclip.com/developers) <br>
- [WorthClip API base URL](https://greedy-mallard-11.convex.site/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WORTHCLIP_API_KEY plus curl and jq; video scoring may poll for up to 60 seconds.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
