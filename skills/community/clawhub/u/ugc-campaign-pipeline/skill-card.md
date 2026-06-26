## Description: <br>
Complete UGC video campaign pipeline: product to hero image, image variations, UGC videos, and an edited final video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and campaign operators use this skill to turn a product image or product URL into a short UGC-style promotional video with scene selection, dialogue, subtitles, transitions, and logo placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images, scripts, branding, and campaign materials may be sent to configured generation providers. <br>
Mitigation: Confirm the materials are approved for use with the configured providers before running the pipeline. <br>
Risk: Generated campaign assets and intermediate files are retained under ~/clawd/outputs/{project}/. <br>
Mitigation: Review the generated files after completion and remove anything that should not be retained locally. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local campaign output structure under ~/clawd/outputs/{project}/, including generated images, scene videos, assets, and a final MP4.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
