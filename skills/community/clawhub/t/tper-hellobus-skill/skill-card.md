## Description: <br>
Get real-time and scheduled bus arrival times for TPER buses in Bologna and Ferrara, Italy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lore2601](https://clawhub.ai/user/lore2601) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up TPER bus arrivals for specific numeric stop codes and line numbers in Bologna and Ferrara, including real-time arrivals and scheduled times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs network access to the TPER Hellobus domain to return bus-arrival data. <br>
Mitigation: Allow only the required Hellobus domain and install the skill only where external network requests are acceptable. <br>
Risk: The skill demonstrates shell-based curl requests, which can be broader than a scoped HTTP request tool. <br>
Mitigation: Use an environment that confirms shell commands before execution or replace the shell call with a scoped HTTP request tool. <br>
Risk: Incorrect stop codes or line numbers can return no results or misleading arrival information. <br>
Mitigation: Ask users to provide numeric TPER stop codes and line numbers, and report API errors clearly when the input does not match the service. <br>


## Reference(s): <br>
- [TPER Hellobus API endpoint](https://hellobuswsweb.tper.it/web-services/hellobus.asmx/QueryHellobus) <br>
- [ClawHub skill page](https://clawhub.ai/lore2601/tper-hellobus-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with bullet lists and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires numeric TPER stop codes and line numbers; real-time lookups require network access to the TPER Hellobus domain.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
