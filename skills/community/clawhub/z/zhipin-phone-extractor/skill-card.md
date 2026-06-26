## Description: <br>
Automatically extracts phone numbers from BOSS直聘 (zhipin.com) chat messages and saves deduplicated recruiter contact records locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libaoming](https://clawhub.ai/user/libaoming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a Playwright-based extractor against a logged-in BOSS直聘 web session, collect phone numbers from recruiter chat messages, and save deduplicated contacts to a local file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates access to private recruiting chats and collects personal phone numbers. <br>
Mitigation: Install and run it only when that collection is intentional, start with a small message limit, and confirm the target account and chat scope before use. <br>
Risk: Extracted contact data is saved to a local file and may persist longer than needed. <br>
Mitigation: Choose a protected output path, restrict access to the saved file, and delete or secure the file when it is no longer needed. <br>
Risk: Headless or scheduled use can collect chat data without immediate user review. <br>
Mitigation: Prefer manual runs; avoid cron or headless background use unless the operator has reviewed the scope and storage location. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [BOSS直聘](https://www.zhipin.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/libaoming/zhipin-phone-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with bash command examples and local text-file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends timestamped contact records containing name, phone number, and company when matching phone numbers are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
