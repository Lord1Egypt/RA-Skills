## Description: <br>
Scaffolds a full-stack project with Next.js App Router, Supabase, Firebase Auth, Vercel, and Cloudflare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create a new Next.js full-stack project scaffold with Supabase, Firebase Auth, Vercel configuration, Cloudflare deployment guidance, tests, and environment templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project scaffolding can create files, initialize git, install packages, and run npx/npm commands in the target directory. <br>
Mitigation: Use a new or empty directory, review planned commands before execution, and confirm the project name and target path before files are created. <br>
Risk: The generated project requires Supabase and Firebase environment values, including server-side Firebase credentials. <br>
Mitigation: Add real secrets only after confirming .env files are ignored by git, and keep .env.local and credential files out of source control. <br>


## Reference(s): <br>
- [Stack Scaffold on ClawHub](https://clawhub.ai/guifav/stack-scaffold) <br>
- [OpenClaw Skills Repository](https://github.com/guifav/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a new project scaffold and prompts for configuration of Supabase, Firebase, Vercel, and Cloudflare settings.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
