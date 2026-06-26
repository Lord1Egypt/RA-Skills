## Description: <br>
AI Hairstyle Try-On & Face Shape Analysis - Upload a photo to analyze face shape and instantly try recommended hairstyles. UID required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guokai-01](https://clawhub.ai/user/guokai-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit a face photo and TryHair UID for hairstyle previews or face-shape analysis through the tryhair.ai service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive face photos and a TryHair UID to tryhair.ai. <br>
Mitigation: Confirm the selected image, requested style or analysis action, and UID before each run. <br>
Risk: Image URL input could expose private or internal image locations. <br>
Mitigation: Use local files or public image URLs only, and avoid private or internal URLs. <br>
Risk: Generated hairstyle previews may remain in the local output directory. <br>
Mitigation: Delete generated files from output/ when they are no longer needed. <br>
Risk: Runs may consume TryHair credits. <br>
Mitigation: Check the requested operation and monitor remaining credits before repeated try-ons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guokai-01/tryhair-skill) <br>
- [TryHair homepage](https://tryhair.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, image files, guidance] <br>
**Output Format:** [JSON responses containing Markdown-formatted analysis text, user-facing messages, and local image paths when previews are generated] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated hairstyle previews may be saved under output/ and responses may report remaining credits.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
