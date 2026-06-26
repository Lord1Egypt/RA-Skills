## Description: <br>
Scrapes comments from all notes on a Xiaohongshu profile URL, saves them as local JSON files, and can generate an optional HTML analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liteli1987gmail](https://clawhub.ai/user/liteli1987gmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect Xiaohongshu profile note comments into local JSON files and, when requested, generate a local HTML analysis report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping profile comments can collect personal or sensitive commenter data. <br>
Mitigation: Confirm the exact Xiaohongshu profile before running, respect platform rules and privacy laws, and delete generated JSON or HTML files when no longer needed. <br>
Risk: The skill uses a logged-in browser session and writes local files. <br>
Mitigation: Use a dedicated browser profile when possible, avoid elevated privileges, and clear the browser session and downloaded files after use. <br>
Risk: High-frequency access may trigger Xiaohongshu captcha or anti-bot controls. <br>
Mitigation: Pause and ask the user to complete any captcha manually in the browser; do not attempt to bypass platform controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liteli1987gmail/xhs-comment) <br>
- [Publisher profile](https://clawhub.ai/user/liteli1987gmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, JSON, HTML] <br>
**Output Format:** [Markdown guidance with browser actions, Python snippets, local JSON files, and optional HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one JSON file per note to the user's Downloads xhs_comments folder and optional analysis files to Downloads xhs_comments_analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
