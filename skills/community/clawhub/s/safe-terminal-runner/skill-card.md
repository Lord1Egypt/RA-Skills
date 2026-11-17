## Description:

Guides agents to run complex Node.js and Python terminal tasks through temporary script files with explicit environment loading, execution, cleanup, and hang recovery steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaynzhu](https://clawhub.ai/user/zaynzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run complex one-off terminal scripts without fragile inline command quoting, especially for Node.js, Python, database operations, and environment-variable-heavy tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned npx example can download packages on demand during TypeScript script execution.

Mitigation: Prefer a project-local pinned tsx dependency or an already-installed binary before running TypeScript tasks.

Risk: Loading full .env contents can expose unnecessary secrets to temporary scripts.

Mitigation: Load only the environment variables the task requires.

Risk: Temporary scripts can remain in the workspace or be committed if cleanup is missed.

Mitigation: Prefix temporary scripts with temp_, keep temp_* ignored by version control, and delete temporary scripts after confirming results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaynzhu/skills/safe-terminal-runner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to create temp_ files, load environment variables explicitly, execute the files, and remove them after confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
