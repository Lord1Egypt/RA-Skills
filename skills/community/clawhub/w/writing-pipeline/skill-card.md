## Description: <br>
Writing Pipeline guides an agent through a Chinese content-recreation workflow from reference intake and AI drafting through human review, preference learning, and multi-platform publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and publishing teams use this skill to turn reference material into Chinese drafts, preserve human review feedback, learn style preferences from edits, and prepare platform-specific outputs for blogs, WeChat, Xiaohongshu, Jike, and Twitter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish stage can upload article assets to R2 and WeChat and rewrite local article files. <br>
Mitigation: Review the article directory, images, and target platforms before publishing; avoid confidential, licensed, or unpublished-sensitive material unless external upload is acceptable. <br>
Risk: The review stage can propose updates to writing-style skills based on draft-to-final differences. <br>
Mitigation: Approve writing-style skill updates only after checking that the proposed rules reflect the user's preferences, then review and scan changed skills before deployment. <br>


## Reference(s): <br>
- [Diff-and-Learn workflow](references/diff-learn.md) <br>
- [ClawHub skill page](https://clawhub.ai/shing19/writing-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, YAML metadata, JSON mappings, shell commands, and platform-specific article text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update article directories, drafts, final copy, diff analysis, platform output files, and image assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
