## Description: <br>
Estimates how likely user-provided text is to be AI-generated from language style and expression features, then provides a brief analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjiangliu9-tech](https://clawhub.ai/user/dongjiangliu9-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and reviewers use this skill to get a cautious, text-feature-based estimate of whether a submitted passage resembles AI-generated writing. It is intended for style analysis, not plagiarism checking, database comparison, or proof of authorship. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the AI probability as proof of authorship or as a professional plagiarism or AI-detection result. <br>
Mitigation: Present the percentage as a rough writing-style estimate and keep the existing caveat that it is not a database, plagiarism, or professional detection result. <br>
Risk: The fixed Chinese output format may be less convenient for non-Chinese users. <br>
Mitigation: Translate or adapt the response labels when serving users who need another language, while preserving the uncertainty caveat. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dongjiangliu9-tech/zeelin-ai-detector) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown with a probability estimate, concise bullet analysis, and a cautionary explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are qualitative estimates based only on the provided text; short inputs should be marked unstable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
