## Description: <br>
Stremio CLI automates Stremio web with Torrentio on a Mac Mini by searching for shows or movies, selecting high-seeded streams, and starting playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BEARLY-HODLING](https://clawhub.ai/user/BEARLY-HODLING) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to drive a saved Stremio browser session on a Mac Mini, choose a requested title or episode, and begin playback through the Torrentio-enabled Stremio web app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a saved Stremio account and browser session on the target Mac Mini. <br>
Mitigation: Install and run it only on the intended Mac Mini and account, and confirm the user is comfortable with the agent using that saved session. <br>
Risk: The artifact includes an unused legacy casting script with stream-extraction and Chromecast/catt behavior. <br>
Mitigation: Audit or remove scripts/stremio_cast.py before deployment if legacy casting capability is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BEARLY-HODLING/stremio-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, browser actions] <br>
**Output Format:** [Markdown guidance with browser automation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a saved Stremio login/browser session and may rely on the Torrentio addon being active.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
