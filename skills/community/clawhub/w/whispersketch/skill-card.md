## Description: <br>
Musecard turns a phrase, mood, or scene into a 9:16 illustrated quote-card prompt for WeChat, Xiaohongshu, and similar social publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, social media editors, and creative agents use Musecard to select visual styles, draft card copy options, and produce image-generation prompts for vertical emotional quote illustrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad file-write access can create or overwrite files when file creation is not required. <br>
Mitigation: Remove or limit Write access unless the workflow explicitly needs files, and review target paths before allowing writes. <br>
Risk: Anime styling features can steer vague requests toward suggestive or age-ambiguous character prompts. <br>
Mitigation: Require anime characters to be clearly adult and non-sexualized, and avoid youth-coded sexualized clothing, poses, or framing. <br>


## Reference(s): <br>
- [Musecard ClawHub release page](https://clawhub.ai/fslong520/whispersketch) <br>
- [Musecard skill definition](artifact/SKILL.md) <br>
- [Example Musecard prompt](artifact/output/musecard_prompt.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with image-prompt text blocks; may request image generation when the host agent supports it.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optimized for 9:16 vertical illustration-card prompts.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
