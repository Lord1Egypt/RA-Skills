## Description: <br>
Search Movie helps agents search for movie and TV resources through a XiaoBenYang MCP API and validate whether candidate playback links are playable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find candidate movie or TV playback resources, validate playable links, and present the returned API results to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the user-provided API key in a local plaintext .env file. <br>
Mitigation: Use a dedicated key for this service, avoid entering unrelated credentials, and remove or rotate the key when it is no longer needed. <br>
Risk: Search and link-validation requests are sent to the remote XiaoBenYang provider. <br>
Mitigation: Install and use the skill only if the remote provider is acceptable for the user's environment and avoid submitting sensitive or unnecessary data. <br>
Risk: Initial movie or TV search results may be unverified candidate links. <br>
Mitigation: Use the validation tool before recommending a playable link and do not fabricate results when the API key or API response is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/search-movie) <br>
- [XiaoBenYang provider site](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown or plain text summarizing JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided XBY API key; candidate search results should be validated before presenting playable links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
