## Description: <br>
A WeChat Official Account benchmarking skill that uses RedFox data to recommend peer benchmark accounts and higher-performing aspirational accounts from account name, account ID, category, or sync requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat Official Account creators, content teams, MCN operators, and brand marketers use this skill to compare an account with similar accounts, inspect recent article performance, and find growth or placement benchmarks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and may read it from persistent shell or user environment configuration. <br>
Mitigation: Use a revocable RedFox API key, prefer temporary environment-variable setup, and do not paste the key into prompts, logs, or output files. <br>
Risk: Submitting a WeChat ID for synchronization sends that identifier to RedFox and may trigger follow-up reporting. <br>
Mitigation: Submit WeChat IDs only with user consent and only when the user is comfortable sharing the identifier with RedFox. <br>
Risk: The security review marked the release as suspicious because consent around synchronization and success messaging may be weak. <br>
Mitigation: Review the workflow before installing and confirm synchronization status and user expectations clearly before relying on the generated report timing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/wechat-similar-account) <br>
- [RedFox publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [README.en.md](README.en.md) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?souce=github) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and prose, with optional shell commands for the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends account lookup or sync inputs to RedFox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
