## Description: <br>
Multi-agent validation framework that uses six independent AI critics to evaluate artifacts against rubrics with evidence-grounded findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dacervera](https://clawhub.ai/user/dacervera) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent teams use Sharedintellect Quorum to validate AI-generated research, configuration, code, and documentation against rubrics before relying on or shipping the outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read selected project files and send analyzed content to the configured LLM provider. <br>
Mitigation: Use it only on content you are comfortable sharing with that provider and understand where analyzed content is sent. <br>
Risk: Batch validation over broad directories can include private files or secrets by mistake. <br>
Mitigation: Avoid pointing batch mode at directories containing secrets and use --no-learning for sensitive reviews. <br>
Risk: Installation uses a cloned Python package and dependency installation flow. <br>
Mitigation: Review the cloned repository or pin a commit before use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dacervera/quorum) <br>
- [Source repository](https://github.com/SharedIntellect/quorum) <br>
- [Full architectural specification](https://github.com/SharedIntellect/quorum/blob/main/SPEC.md) <br>
- [Model requirements](https://github.com/SharedIntellect/quorum/blob/main/docs/getting-started/MODEL_REQUIREMENTS.md) <br>
- [Configuration reference](https://github.com/SharedIntellect/quorum/blob/main/docs/configuration/CONFIG_REFERENCE.md) <br>
- [Beginner guide](https://github.com/SharedIntellect/quorum/blob/main/docs/getting-started/FOR_BEGINNERS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; Quorum runs produce JSON verdict files and report.md.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, pip, and either ANTHROPIC_API_KEY or OPENAI_API_KEY; may read selected project files during validation.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata, docs/CHANGELOG.md, pyproject.toml, runtime __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
