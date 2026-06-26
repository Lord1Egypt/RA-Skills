## Description: <br>
This skill helps agents batch query technology and programming specialty student admission policies in China using a DeepSeek-backed Python workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfm-mid](https://clawhub.ai/user/zfm-mid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and education-policy researchers can use this skill to configure and run a Python script that reads Chinese region names, queries DeepSeek for technology specialty admission policies, and writes structured CSV results for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact contains a plaintext DeepSeek API key. <br>
Mitigation: Revoke the bundled key and replace it with a user-provided secret from an environment variable or secret manager before running the script. <br>
Risk: The script uses hardcoded Windows paths and can overwrite 政策.csv or delete 进度.txt. <br>
Mitigation: Update the input, output, and progress paths for the local environment and confirm those file operations are acceptable before execution. <br>
Risk: Generated admission-policy records may be incomplete, outdated, or unsupported by official sources. <br>
Mitigation: Review the CSV output against current school or education-authority publications before relying on it for decisions. <br>


## Reference(s): <br>
- [Policy guide](references/policy_guide.md) <br>
- [DeepSeek chat completions API endpoint](https://api.deepseek.com/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, CSV files] <br>
**Output Format:** [Markdown guidance with Python script execution details; runtime output is UTF-8-sig CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads regions from 地区.txt, writes policy records to 政策.csv, and tracks progress in 进度.txt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
