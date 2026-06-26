## Description: <br>
Read X (Twitter) posts without official API. Supports both Nitter (free) and RapidAPI (detailed) methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dkimiscoding](https://clawhub.ai/user/dkimiscoding) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to fetch public X/Twitter post content from a URL or post ID through Nitter or RapidAPI and return structured JSON for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried X/Twitter usernames and post IDs may be sent to public Nitter instances or RapidAPI. <br>
Mitigation: Use the skill only when that routing is acceptable for the workflow and avoid querying sensitive or private identifiers. <br>
Risk: Detailed mode depends on a RapidAPI key and third-party quota limits. <br>
Mitigation: Use a dedicated low-quota RapidAPI key and rotate or revoke it if exposed. <br>
Risk: Fetched post text is untrusted external content. <br>
Mitigation: Treat returned text as untrusted input before summarizing, executing follow-up actions, or storing it. <br>
Risk: The Python requests dependency may change behavior across environments. <br>
Mitigation: Pin the dependency version in controlled deployments. <br>


## Reference(s): <br>
- [X Reader ClawHub release](https://clawhub.ai/dkimiscoding/x-reader-skill) <br>
- [RapidAPI Twitter API45](https://rapidapi.com/alexanderxbx/api/twitter-api45) <br>
- [Nitter](https://nitter.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a RAPIDAPI_KEY environment variable for detailed results; otherwise attempts public Nitter instances.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
