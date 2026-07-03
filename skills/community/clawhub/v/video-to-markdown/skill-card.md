## Description: <br>
Analyze YouTube, Facebook, or Instagram video URLs and generate comprehensive Markdown reference documents by combining extracted video frames with transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmdeep](https://clawhub.ai/user/gmdeep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, analysts, and content reviewers use this skill to turn supported video URLs into structured notes, summaries, and reference documents that capture both spoken content and important on-screen visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends video frames, transcripts, and metadata to an external AI provider. <br>
Mitigation: Use only with videos whose contents may be shared with that provider; avoid confidential or private videos unless that data transfer is approved. <br>
Risk: Cookie files and ANTHROPIC_API_KEY are sensitive credentials used by the workflow. <br>
Mitigation: Treat cookies and API keys as secrets, avoid printing or sharing them, and remove or rotate them if exposed. <br>
Risk: The security scan notes that the skill asks agents to run unbundled relative scripts. <br>
Mitigation: Verify that setup and analyzer scripts come from the intended repository before running them. <br>


## Reference(s): <br>
- [Server-resolved GitHub repository](https://github.com/GMDEEP/video-to-markdown) <br>
- [ClawHub skill page](https://clawhub.ai/gmdeep/video-to-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with YAML frontmatter and structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated documents may include source metadata, visual summaries, section breakdowns, key takeaways, terminology, and visual-narration gaps.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
