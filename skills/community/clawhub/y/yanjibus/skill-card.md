## Description: <br>
Queries real-time Yanji bus route vehicle locations, with optional sub-route and fuzzy origin and destination station matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ham-Kris](https://clawhub.ai/user/Ham-Kris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and local agents use this skill to answer Yanji bus route questions, inspect station lists, choose a travel direction, and report live vehicle positions for a selected route. <br>

### Deployment Geography for Use: <br>
Yanji, Jilin, China <br>

## Known Risks and Mitigations: <br>
Risk: Crafted station names or tampered bus responses could cause local code execution in the helper script. <br>
Mitigation: Review before installing, patch the script to pass station names and fetched JSON as data through argv, environment variables, stdin, or files, and limit activation to explicit Yanji bus route or stop queries. <br>
Risk: The helper script fetches live route data over HTTP, so responses may be modified in transit. <br>
Mitigation: Prefer HTTPS or response validation if available, and treat returned vehicle positions as informational. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Ham-Kris/yanjibus) <br>
- [Gaode Map skill integration reference](https://github.com/kaichen/amap-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text route, station, direction, and live vehicle status results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local bash, curl, python3, and network access to Yanji bus service endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
