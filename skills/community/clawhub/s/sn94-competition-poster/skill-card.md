## Description: <br>
Helps create, review, and package SN94 BitSota competition proposals and replayable task repository skeletons for measurable research competitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alveuslabs](https://clawhub.ai/user/alveuslabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to turn measurable research competition ideas into SN94 BitSota proposals, implementation prompts, launch checklists, and replayable starter task repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated starter repositories or benchmark commands may be published or run before they are reviewed. <br>
Mitigation: Review generated repositories before publishing and run setup or benchmark commands only in an appropriate sandbox. <br>
Risk: Competition packaging can accidentally include secrets, wallet material, or sensitive credentials. <br>
Mitigation: Keep secrets, wallet files, API tokens, and production environment files out of generated task repositories and release archives. <br>


## Reference(s): <br>
- [SN94 Replay Contract](artifact/references/replay-contract.md) <br>
- [SN94 Task Repo Spec](artifact/references/task-repo-spec.md) <br>
- [Marketplace Packaging](artifact/references/marketplace-packaging.md) <br>
- [SN94 BitSota Competition Proposal Issue Template](https://github.com/AlveusLabs/SN94-BitSota/issues/new?template=competition_proposal.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/alveuslabs/sn94-competition-poster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional generated repository files, YAML/JSON configuration, Python code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May scaffold a local starter task repository when the user requests it.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
