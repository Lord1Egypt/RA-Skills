## Description: <br>
Generates Chinese legal-themed WeChat article drafts for personal and enterprise audiences, using current public hot topics when available and fallback legal topic templates when not. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mylillo926](https://clawhub.ai/user/mylillo926) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal content creators and practitioners use this skill to draft two publish-ready article files for a WeChat public account: one aimed at individuals and one aimed at enterprise readers. It is intended to speed up routine topic selection and first-draft preparation, not to replace legal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to public Chinese hot-search and news services when optional dependencies are installed. <br>
Mitigation: Review the public sources and network behavior before running in restricted environments. <br>
Risk: Generated legal-themed article drafts may be inaccurate, incomplete, or unsuitable for publication without review. <br>
Mitigation: Manually verify legal claims, examples, and practical guidance before publishing. <br>
Risk: The default output directory is a local Windows path that may not match the user's environment. <br>
Mitigation: Review or change the configured output directory before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text article files with Markdown-style headings and lists, plus brief command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates separate personal and enterprise article drafts and progress JSON files in a configurable local output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
