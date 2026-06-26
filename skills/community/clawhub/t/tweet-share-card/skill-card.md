## Description: <br>
Convert an X/Twitter post URL into a polished share card image by capturing the tweet content and compositing it on a styled background. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Efficiency97](https://clawhub.ai/user/Efficiency97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People creating social posts use this skill to turn X/Twitter URLs into square share-card images with preset background styles while preserving a real tweet screenshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Chrome/X session and captures screen content. <br>
Mitigation: Use an isolated dedicated browser profile with no unrelated tabs or sensitive visible content. <br>
Risk: User-provided X/Twitter URLs are passed into browser automation without enough containment. <br>
Mitigation: Provide only trusted X/Twitter URLs and prefer an updated version that validates and escapes URLs before automation. <br>
Risk: Intermediate screenshots may contain tweet or session-adjacent content. <br>
Mitigation: Store outputs in a controlled workspace and delete intermediate screenshots after the final card is created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Efficiency97/tweet-share-card) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image file with a short chat response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Square share-card image; color presets include peach, pink, blue-purple, purple-blue, and mint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
