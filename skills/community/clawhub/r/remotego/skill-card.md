## Description: <br>
Expose local command-line tools as browser-accessible public web terminal sessions through a tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topcheer](https://clawhub.ai/user/topcheer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to share, access, or collaborate on local CLI sessions from a browser when they intentionally need remote terminal access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a local interactive terminal through a public web link, which can grant high-impact access if shared unintentionally or run from a privileged environment. <br>
Mitigation: Treat the session URL like a password, avoid privileged shells or secret-bearing directories, prefer a restricted working directory or disposable VM/container, and stop the tunnel immediately when finished. <br>
Risk: The remote terminal package is installed or run from npm before use. <br>
Mitigation: Verify the npm package and command source before running it, then install only in environments where remote interactive access is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/topcheer/remotego) <br>
- [Project Homepage](https://github.com/topcheer/claude-remoting) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes npm and npx commands, tunnel options, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
