## Description: <br>
Opens a visible browser for manual browsing of a target site and saves same-origin raw response resources to a local Desktop folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to archive authorized same-origin HTTP and HTTPS resources while manually browsing a site in a visible browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted page URL could write outside the intended Desktop output folder because path handling is unsafe. <br>
Mitigation: Review and fix path normalization before using the skill on untrusted sites. <br>
Risk: Saved raw same-origin responses may include sensitive content from logged-in pages. <br>
Mitigation: Use only on sites you are authorized to archive, preferably in a disposable browser session or test account, and avoid sensitive logged-in pages. <br>
Risk: The skill continuously writes browser responses while the visible tab remains open. <br>
Mitigation: Run it in a controlled workspace and close the tab when collection should stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnoder-wgh/save-all-resource) <br>
- [Publisher profile](https://clawhub.ai/user/cnoder-wgh) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Local files and console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves same-origin HTTP/HTTPS responses under ~/Desktop/<domain> and exits when the browser tab closes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
