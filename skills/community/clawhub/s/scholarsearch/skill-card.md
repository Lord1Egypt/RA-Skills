## Description: <br>
Scholarsearch generates relevance-ranked academic literature briefings from Tavily API, PubMed, and Google Scholar results, with options to save reports to Obsidian and send summaries via Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flying-baozi](https://clawhub.ai/user/flying-baozi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search recent academic literature by keyword, rank the most relevant papers, and produce concise Top 10 research briefings for review or recurring updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local scholarsearch command or wrapper may use external services and credentials. <br>
Mitigation: Verify the command that will run before installation and configure Tavily and Feishu credentials with limited scope. <br>
Risk: Reports may be saved or delivered to an unintended Obsidian path or Feishu destination. <br>
Mitigation: Choose the Obsidian save path and Feishu destination deliberately before running the skill. <br>
Risk: Cron or heartbeat scheduling can create recurring automated reports. <br>
Mitigation: Enable recurring scheduling only when automated reports are expected and approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flying-baozi/scholarsearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing with ranked literature summaries, links, abstracts, key findings, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts comma- or space-separated keywords; may save to an Obsidian daily note and send through Feishu when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
