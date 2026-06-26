## Description: <br>
Spin up a remote browser session via the TinyFish Browser API and get a CDP URL for driving it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bunsdev](https://clawhub.ai/user/bunsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to create a remote Chromium session for Playwright, Puppeteer, or DevTools Protocol workflows and receive the session identifiers needed to drive it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends target URLs and browser activity to TinyFish's remote browser service. <br>
Mitigation: Install only if TinyFish is trusted for the intended browsing activity and avoid sensitive internal sites unless approved. <br>
Risk: The TinyFish API key authorizes browser session creation. <br>
Mitigation: Use a dedicated, revocable API key and verify TINYFISH_API_KEY is set before making requests. <br>
Risk: Returned CDP and session URLs can provide access to the remote browser session. <br>
Mitigation: Treat returned session endpoints as sensitive and avoid logging or sharing them outside the automation workflow. <br>


## Reference(s): <br>
- [TinyFish Browser API documentation](https://docs.tinyfish.ai/browser-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TINYFISH_API_KEY and returns a session ID, CDP URL, and authenticated polling base URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
