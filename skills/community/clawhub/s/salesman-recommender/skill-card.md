## Description: <br>
Automatically filters livestream creators in the Jinritemai selected alliance creator square using dynamic criteria and exports matching results to an Excel file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncrowned-king](https://clawhub.ai/user/uncrowned-king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, merchant operations, and creator-partnership teams use this skill to search the Jinritemai creator marketplace by category, audience, follower, level, and gender filters, then export matching creator records for outreach or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle third-party account credentials and keep browser sessions on disk. <br>
Mitigation: Use it only on a trusted machine and account, prefer manual login when possible, avoid passing passwords through parameters unless necessary, and clear the created browser profile after use. <br>
Risk: The automation uses browser controls that may conflict with the target platform's permitted usage. <br>
Mitigation: Confirm the target platform permits this automation before running it and stop if the workflow violates account or marketplace rules. <br>
Risk: Exported spreadsheets and debug files may contain private business or creator data. <br>
Mitigation: Store exports in an approved location, limit sharing, and delete exported or debug files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uncrowned-king/salesman-recommender) <br>
- [Jinritemai creator square](https://buyin.jinritemai.com/dashboard/servicehall/daren-square) <br>
- [Jinritemai role selection](https://buyin.jinritemai.com/mpa/account/institution-role-select) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Python script execution with console status messages and Excel .xlsx export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Selenium browser automation with optional email and password inputs, persistent browser session storage, dynamic creator filters, and desktop spreadsheet output.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
