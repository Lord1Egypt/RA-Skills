## Description: <br>
Whale Shark helps agents run local Node.js commands that display simulated crypto whale wallet lists, holdings, transfer activity, smart money rankings, and alert records. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[gztanht](https://clawhub.ai/user/gztanht) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents assisting crypto researchers or individual users can run CLI commands to inspect presented whale wallet examples, compare holdings and transfer summaries, rank smart-money wallets, and manage local alert records. The supplied data should be treated as simulated demonstration output, not verified live market intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release markets live whale tracking and smart-money insights, while the reviewed implementation uses simulated static data. <br>
Mitigation: Treat outputs as demonstration examples and verify any wallet, transfer, or trading signal against trusted live data sources before acting. <br>
Risk: The documentation advertises paid crypto unlocks, but the reviewed implementation does not include a verifiable payment or access mechanism. <br>
Mitigation: Do not send funds for access unless the publisher provides clear, working payment terms and an auditable unlock process. <br>
Risk: Alert records store watched wallet identifiers and thresholds locally. <br>
Mitigation: Remove local alert records when they are no longer needed and avoid storing sensitive watchlists on shared systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gztanht/whale-shark) <br>
- [Publisher Profile](https://clawhub.ai/user/gztanht) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Console text and Markdown guidance with Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alert commands persist watched wallet and threshold records in a local JSON file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
