## Description: <br>
Автоматический поиск клиентов (родителей) для репетитора по математике в группах ВКонтакте с умной фильтрацией и приоритизацией онлайн-запросов. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Danil4091](https://clawhub.ai/user/Danil4091) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Math tutors use this skill to monitor selected VK communities for parent requests, filter out tutor advertising, prioritize online tutoring leads, and save structured leads for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a VK service token and recurring scans, so token exposure or unintended long-running monitoring could create account and privacy risk. <br>
Mitigation: Use a dedicated VK service token, keep it private, and confirm how to pause or remove the recurring 3-hour task before deployment. <br>
Risk: The skill saves lead information from VK communities to CSV or an optional Google Sheet. <br>
Mitigation: Monitor only groups you are allowed to process, keep generated lead files private, define a retention and deletion practice, and enable Google Sheets export only when intentionally copying lead data there. <br>


## Reference(s): <br>
- [VK Developers](https://vk.com/apps?act=manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown report plus structured CSV lead records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a VK service token, target VK group list, and output path; can run on a recurring 3-hour schedule.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
