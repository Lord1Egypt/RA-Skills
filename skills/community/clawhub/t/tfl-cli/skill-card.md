## Description: <br>
London transport CLI for checking TfL line status, journey planning, live arrivals, disruptions, bike docks, stop search, and agent-friendly output projection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan8851](https://clawhub.ai/user/shan8851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to run or compose `tfl` commands for London transport status, routes, arrivals, disruptions, bike availability, and stop lookup. It is also useful when an agent needs a single value or subtree from route, arrivals, or bike results instead of a full response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an installed `tfl` binary and may call external TfL services for live transport data. <br>
Mitigation: Install from the declared npm package, review commands before running them, and use the optional `TFL_APP_KEY` only in an appropriate local environment. <br>
Risk: Live journey, arrival, disruption, and bike data can be unavailable, ambiguous, or rate limited. <br>
Mitigation: Check structured error envelopes and documented exit codes before relying on results in automated workflows. <br>


## Reference(s): <br>
- [tfl-cli homepage](https://tfl-cli.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/shan8851/tfl-cli) <br>
- [npm package @shan8851/tfl-cli](https://www.npmjs.com/package/@shan8851/tfl-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON envelope descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can return text or JSON; `--output <path>` projects selected route, arrivals, and bike fields.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
