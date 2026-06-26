## Description: <br>
Use the SeggWat CLI to manage feedback, projects, and ratings from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hauju](https://clawhub.ai/user/hauju) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and CI operators use this skill to install, authenticate, and run SeggWat CLI commands for feedback triage, project lookup, rating analysis, JSON scripting, and CI/CD feedback automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and cached OAuth tokens can grant access to SeggWat data if exposed. <br>
Mitigation: Prefer secret-manager or CI-secret injection for API keys, avoid inline tokens when possible, and protect cached OAuth token files. <br>
Risk: Feedback and rating update or delete/archive commands can modify or hide project data. <br>
Mitigation: Review project IDs, feedback IDs, rating IDs, statuses, and resolution notes before running mutating commands or automation. <br>
Risk: Installing a CLI or running a shell installer can introduce supply-chain risk. <br>
Mitigation: Verify the SeggWat CLI package or installer before running it, especially in automated or privileged environments. <br>


## Reference(s): <br>
- [SeggWat website](https://seggwat.com) <br>
- [SeggWat shell installer](https://seggwat.com/static/install.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/hauju/seggwat-cli) <br>
- [Publisher profile](https://clawhub.ai/user/hauju) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks, command examples, and occasional JSON or shell-script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI flags, environment variables, authentication setup, project or feedback IDs supplied by the user, and jq-based scripting examples.] <br>

## Skill Version(s): <br>
0.17.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
