## Description: <br>
Generates structured Xiaohongshu posts from pdf, md, txt, and json inputs, defaulting to paper-interpretation posts with Markdown and JSON outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chen-Li-17](https://clawhub.ai/user/Chen-Li-17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, researchers, and developers use this skill to turn source documents and structured paper notes into publishable Xiaohongshu-style posts with titles, body sections, hashtags, and evidence notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes xhs-post.md and xhs-post.json into the input file directory, which can overwrite existing files. <br>
Mitigation: Check whether those files already exist, or run the skill on a copy of the input file before using it in an important folder. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Chen-Li-17/xhs-post-factory) <br>
- [Paper Interpretation Template](templates/paper-interpretation.md) <br>
- [XHS Writing Style Guide](references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown and JSON files saved as xhs-post.md and xhs-post.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default post_type is paper-interpretation; length and emoji_density can be adjusted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
