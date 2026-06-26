## Description: <br>
Anti-forgetting vocabulary review using spaced repetition to select English phrases from a vocabulary bank, show Chinese translations, and track future review dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hushenglang](https://clawhub.ai/user/hushenglang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and language-study agents use this skill to run recurring vocabulary review sessions, show selected English phrases with Chinese translations, and persist spaced-repetition progress locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates a local vocabulary progress file, and evidence notes that the actual review_log.md location may differ from the documented workspace memory path. <br>
Mitigation: Check the review_log.md location after first use or set REVIEW_MEMORY_DIR explicitly before running review sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hushenglang/vocabulary-anti-forgetting) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Review CLI script](artifact/review.py) <br>
- [Vocabulary bank](artifact/asset/vocabulary_bank.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text from a local Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local review_log.md progress file; no external dependencies are documented.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
