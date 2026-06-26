## Description: <br>
Skåne public transport trip planner (Skånetrafiken). Plans bus/train journeys with real-time delays. Supports stations, addresses, landmarks, and cross-border trips to Copenhagen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rezkam](https://clawhub.ai/user/rezkam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to search Skånetrafiken locations and plan public-transit journeys in Skåne, Sweden, including timing, transfers, walking segments, real-time delays, platform details, disruption alerts, and cross-border Copenhagen routes. <br>

### Deployment Geography for Use: <br>
Sweden and Denmark <br>

## Known Risks and Mitigations: <br>
Risk: Location searches, journey endpoints, and intended travel times are sent to Skånetrafiken. <br>
Mitigation: Avoid entering exact home, work, or other sensitive addresses unless the user is comfortable sharing that trip-planning data with Skånetrafiken. <br>
Risk: The helper scripts depend on local command-line tools and live network responses. <br>
Mitigation: Install only from a trusted source, ensure curl and jq are available, and confirm ambiguous location matches before planning a journey. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rezkam/skanetrafiken) <br>
- [Agent Skills](https://agentskills.io) <br>
- [Skånetrafiken Points API](https://www.skanetrafiken.se/gw-tps/api/v2/Points) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with shell command examples and formatted journey results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq. The helper scripts return location records and journey options from Skånetrafiken; user-facing responses should preserve real timings, walking distances, delays, and clarification prompts from the tool output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
