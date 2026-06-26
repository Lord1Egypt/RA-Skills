## Description: <br>
Generates Word Jumble puzzles with scrambled clue words, circled letters that spell a final idiom, a cartoon hint image, and a printable puzzle PNG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robin-marv](https://clawhub.ai/user/robin-marv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create daily or ad hoc word-jumble puzzles, validate puzzle invariants, generate a cartoon hint, and return local puzzle assets for separate publishing or scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cartoon image prompts are sent to the configured external image-generation service. <br>
Mitigation: Do not include private, sensitive, or confidential information in image prompts. <br>
Risk: The generated HTML includes the answer key and should not be treated as a secure way to hide puzzle answers. <br>
Mitigation: Use the answer key only as a visual puzzle aid and review generated outputs before publishing. <br>
Risk: The skill writes local output files and briefly runs a local preview server while rendering the printable image. <br>
Mitigation: Review output paths before use, keep the preview server bound to localhost, and stop it after rendering. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robin-marv/word-jumble) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local file paths, JSON puzzle data, shell commands, and generated image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a puzzle JSON file, a cartoon JPG, and a printable PNG in a local output directory; publishing remains the caller's responsibility.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
