## Description: <br>
Install and run the published SuperPowers desktop streamer npm package for login, account verification, streamer startup, control-link opening, and common npm or runtime recovery without requiring source-code access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohanarun](https://clawhub.ai/user/rohanarun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install the third-party SuperPowers desktop streamer npm package locally, run its CLI, complete email or phone verification, start or stop the streamer, and troubleshoot common install, login, and streaming issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an unpinned third-party desktop streaming package that may expose screen or control access. <br>
Mitigation: Verify the npm package and publisher before installation, install only when the desktop streamer is intended, and use the documented stop and logout commands when finished. <br>
Risk: Screen Recording or Accessibility permissions can expose sensitive desktop activity if granted to an untrusted streamer. <br>
Mitigation: Approve those permissions only when the service and session are trusted, and revoke them after use if access is no longer needed. <br>


## Reference(s): <br>
- [Super Powers AI ClawHub Release](https://clawhub.ai/rohanarun/super-powers) <br>
- [superpowers-ai npm Package](https://www.npmjs.com/package/superpowers-ai) <br>
- [Install And Run](references/install.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs through a local .superpowers state directory and does not perform a global npm install.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
