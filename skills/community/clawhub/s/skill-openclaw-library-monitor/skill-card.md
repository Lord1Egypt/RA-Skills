## Description: <br>
Monitor library book availability and get notified when books become available for borrowing. Supports Shenzhen Library and extensible for other libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yszheda](https://clawhub.ai/user/yszheda) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to track books they want to borrow, check Shenzhen Library availability, and receive console or email notifications when monitored books become available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores monitored book titles, authors, ISBNs, and availability status locally. <br>
Mitigation: Store the skill data in a protected workspace and avoid sharing book_list.json or config.yaml. <br>
Risk: Email notifications require SMTP settings and credentials. <br>
Mitigation: Use an app-specific SMTP credential, review recipient addresses, and protect config.yaml. <br>
Risk: Scheduled monitoring continues background availability checks until stopped. <br>
Mitigation: Use reasonable check intervals and stop the scheduler when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yszheda/skill-openclaw-library-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/yszheda) <br>
- [Shenzhen Library](https://www.szlib.org.cn/) <br>
- [Shenzhen Library OPAC](https://www.szlib.org.cn/opac/) <br>
- [Shenzhen Library OPAC Service API](https://www.szlib.org.cn/api/opacservice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON/configuration file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local book list data and may send console or email notifications when availability changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
