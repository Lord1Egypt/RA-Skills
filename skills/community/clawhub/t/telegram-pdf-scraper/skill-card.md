## Description: <br>
A browser automation skill that downloads PDF files from a named Telegram channel and organizes them into folders based on message headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koppakanagaharsha-lang](https://clawhub.ai/user/koppakanagaharsha-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators with access to Telegram Web use this skill to collect PDF study materials from a specified Telegram channel and save them into locally organized folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains a logged-in Telegram Web browser profile on disk. <br>
Mitigation: Use a dedicated Telegram session when possible, and delete or log out of ./openclaw_chrome_profile when session persistence is not desired. <br>
Risk: The skill automatically clicks and downloads files from the selected Telegram channel. <br>
Mitigation: Run it only on trusted channels, confirm the selected chat before scanning, and inspect or scan downloaded PDFs before opening them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/koppakanagaharsha-lang/telegram-pdf-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/koppakanagaharsha-lang) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, configuration, guidance] <br>
**Output Format:** [Local PDF files organized into folders plus status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local browser profile directory and writes downloaded files under the configured download directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
