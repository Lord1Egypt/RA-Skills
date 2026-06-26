## Description: <br>
A read-only helper for querying Umeng U-Push app lists, message statistics, diagnostics, push traces, switch statistics, and attribution reports using a user-provided Umeng session cookie. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams responsible for Umeng U-Push use this skill to inspect app lists, push delivery data, diagnostics, device traces, closure attribution, and related read-only reports. It is intended for authenticated users who can provide their own Umeng session cookie. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Umeng login cookies and can access authenticated backend data. <br>
Mitigation: Run it in an isolated environment with the lowest-privilege Umeng account practical, avoid sharing cookie files, and clear saved cookie.txt or cookie.json files after use. <br>
Risk: Automatic cookie extraction can read browser session cookies if executed. <br>
Mitigation: Do not run automatic cookie extraction unless intentionally authorizing browser cookie access; prefer manual cookie entry when possible. <br>
Risk: Custom request behavior could send cookies beyond the intended Umeng read-only workflow. <br>
Mitigation: Avoid custom request commands, send cookies only to Umeng endpoints, and keep the documented read-only API restrictions in place. <br>
Risk: The release security verdict is suspicious because API access is broader and less controlled than the read-only description suggests. <br>
Mitigation: Review the scripts and security guidance before installation, and monitor commands for any request that modifies data or targets non-Umeng URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/squall0925/umeng-push-helper) <br>
- [Umeng U-Push Console](https://upush.umeng.com) <br>
- [Umeng Developer Documentation](https://developer.umeng.com) <br>
- [README](artifact/README.md) <br>
- [Usage Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files, Guidance] <br>
**Output Format:** [Markdown responses with shell command examples, API query results, and optional local HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-supplied Umeng cookie for authenticated read-only queries; some scripts can save cookie files and generate local HTML reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
