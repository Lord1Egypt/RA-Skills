## Description: <br>
Shared consciousness between Clawdbot instances. Links multiple bots into a collective, sharing memories, activities, and decisions in real-time over local network using Gun.js P2P sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Clawdbot operators use this skill to link trusted Clawdbot instances on a private network so they can share memory, activity, decisions, and notes through a local Gun.js relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill shares bot memory, activity, decisions, and notes across linked instances, which can expose sensitive operational context if used on untrusted networks. <br>
Mitigation: Use only with trusted Clawdbot instances on a private network, treat pairing codes and namespace data as sensitive, and avoid public or untrusted WiFi. <br>
Risk: The server security assessment says the security claims are stronger than the code supports. <br>
Mitigation: Review the implementation before use, stop the relay when not needed, and do not rely on advertised encryption or authentication until fixed or independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Koba42Corp/vinculum) <br>
- [Koba42Corp publisher profile](https://clawhub.ai/user/Koba42Corp) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with command output, status summaries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm; commands operate through the /link interface and local relay configuration.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence; artifact frontmatter and package.json list 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
