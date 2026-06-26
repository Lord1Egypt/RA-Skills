## Description: <br>
Finds valid WebCodecs strings for video and audio by researching codec support tables and detailed specifications on webcodecsfundamentals.org. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socratescli](https://clawhub.ai/user/socratescli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify suitable WebCodecs audio and video codec strings for target platforms, codec families, and media requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codec support guidance can be incomplete or change across browsers, devices, and versions. <br>
Mitigation: Verify production-critical recommendations against current browser and device support before relying on them. <br>
Risk: The skill uses web access to consult public codec reference pages. <br>
Mitigation: Treat results as compatibility guidance and review cited reference pages for high-impact decisions. <br>


## Reference(s): <br>
- [WebCodecs Fundamentals codec support table](https://webcodecsfundamentals.org/datasets/codec-support-table/) <br>
- [ClawHub release page](https://clawhub.ai/socratescli/webcodecs-string-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendation with concise rationale and browser or platform support notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns two to three recommended codec strings when enough requirement detail is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
