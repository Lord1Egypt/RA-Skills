## Description: <br>
Real-time Toronto transit: bus and streetcar arrivals, vehicle tracking, alerts, and stop search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasygu](https://clawhub.ai/user/lucasygu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent run the TTC CLI for Toronto surface transit questions, including next arrivals, live vehicles, nearby stops, service alerts, route lookup, and machine-readable status output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npm installer can modify or replace ~/.claude/skills/ttc in the user's home directory. <br>
Mitigation: Review install scripts before installation and check whether ~/.claude/skills/ttc already contains a custom skill or symlink. <br>
Risk: The nearby-stops command can request macOS device location access when coordinates are not supplied. <br>
Mitigation: Pass coordinates manually or deny macOS location permission when location sharing is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasygu/ttc) <br>
- [Project homepage](https://github.com/lucasygu/ttc-cli) <br>
- [Open Toronto TTC GTFS dataset](https://open.toronto.ca/dataset/merged-gtfs-ttc-routes-and-schedules/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summaries, with optional JSON from CLI commands that support --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public TTC transit feeds; nearby-stop lookup may use macOS location permission or manually supplied coordinates.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
