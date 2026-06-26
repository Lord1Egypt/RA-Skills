## Description: <br>
Analyzes a YouTube channel's recent upload history to identify high-performing posting days and hours for scheduling content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, channel operators, and content teams use this skill to inspect recent YouTube upload performance and choose posting windows based on historical views. Agents can use it to run the analyzer script, summarize the report, and provide scheduling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install commands fetch mutable files into a persistent agent skills folder. <br>
Mitigation: Review the fetched files before use, prefer pinning to a commit or verifying checksums, and remove ~/.agents/skills/youtube-scheduler when the skill is no longer needed. <br>
Risk: Scheduling recommendations are statistical estimates from historical videos and may not predict future performance. <br>
Mitigation: Treat the recommended posting windows as decision support and validate them against current audience analytics and channel goals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/youtube-scheduler) <br>
- [Publisher Profile](https://clawhub.ai/user/mcbaivn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style report text with shell command examples and a saved .txt report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The analyzer writes reports under Youtube_Schedule/ and bases recommendations on the requested number of recent videos.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
