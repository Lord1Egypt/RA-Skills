## Description:

tfl-cli helps agents use the tfl command for London transport status, journey planning, live arrivals, disruptions, bike docks, stop search, and targeted output projection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shan8851](https://clawhub.ai/user/shan8851)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to query London transport information through the tfl CLI and extract specific route, arrival, or bike availability values for downstream tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an external npm CLI package that is not vendored or integrity-pinned in the artifact.

Mitigation: Review or pin the npm package version before installation, especially in managed or production environments.

Risk: Providing TFL_APP_KEY can expose an API credential if it is handled like ordinary command text.

Mitigation: Set TFL_APP_KEY only when higher rate limits are needed and store it through the agent environment's secret-management path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shan8851/skills/tfl-cli)
- [Publisher profile](https://clawhub.ai/user/shan8851)
- [tfl-cli homepage](https://tfl-cli.xyz)
- [npm package @shan8851/tfl-cli](https://www.npmjs.com/package/@shan8851/tfl-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands; tfl command output may be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports targeted dot-path projection for route, arrivals, and bikes commands.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
