## Description: <br>
Where We Meet helps agents recommend up to five fair meeting places for a group based on each person's starting location, city, travel mode, and food or entertainment preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gggggyyyyy000](https://clawhub.ai/user/gggggyyyyy000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to turn a group meeting request into candidate restaurants or activity areas with commute comparisons, nearby similar-place counts, and map handoff details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged artifact does not include the local Node script that the skill instructs the agent to run. <br>
Mitigation: Install only when the script source is known and independently verified before execution. <br>
Risk: The skill processes people's addresses, map API keys, and generated local request, QR, or HTML files. <br>
Mitigation: Use appropriate local containment, protect Amap credentials, and confirm that generated files and map handoff artifacts are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/GggggYyyyy000/where-we-meet) <br>
- [ClawHub skill page](https://clawhub.ai/gggggyyyyy000/skills/where-we-meet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown text with map links, optional MEDIA attachment line, and local HTML file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a QR-code PNG attachment and a PC HTML comparison page; output should be forwarded as generated.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
