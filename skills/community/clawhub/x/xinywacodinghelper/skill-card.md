## Description: <br>
Guides agents through safe, minimal code changes in large repositories using repo access checks, visible progress, resumable indexing, validation, and recovery steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinyue-wang](https://clawhub.ai/user/xinyue-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill for complex brownfield code changes that need repository understanding, small scoped edits, validation, and explicit progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to read and modify target repositories and run validation commands. <br>
Mitigation: Install it only where the agent is authorized to access the repository, edit files, and run tests. <br>
Risk: The skill records local progress, indexes, and failure logs that may contain private code context. <br>
Mitigation: Keep local run and index directories private, and clean retained indexes or failure logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinyue-wang/xinywacodinghelper) <br>
- [Publisher profile](https://clawhub.ai/user/xinyue-wang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured status blocks and inline code or shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce progress logs, implementation notes, test results, confidence summaries, and recovery messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
