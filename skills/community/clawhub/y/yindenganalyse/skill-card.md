## Description:

Automatically crawls Yindeng non-performing loan transfer announcements and result notices, downloads public PDFs, and can extract key financial data with OCR and optional LLM analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiyoubug](https://clawhub.ai/user/aiyoubug)

### License/Terms of Use:


## Use Case:

Developers and financial operations users use this skill to automate collection of public Yindeng announcements and result notices, then produce local crawl logs, OCR summaries, and optional LLM-generated analysis spreadsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM analysis can send extracted PDF text and an API key to the configured LLM provider.

Mitigation: Keep analysis disabled for confidential workloads unless the endpoint is trusted, restrict LLM_API_BASE to approved HTTPS provider domains, and use a scoped API key.

Risk: The skill downloads public Yindeng PDFs and retains local financial-report files.

Mitigation: Run it only in approved workspaces and review local storage and retention requirements before production use.

Risk: Runtime dependencies are not pinned in the artifact requirements.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiyoubug/skills/yindenganalyse)
- [Publisher profile](https://clawhub.ai/user/aiyoubug)
- [Yindeng transfer announcements](https://www.yindeng.com.cn/xxpl/xxpl_bldkzr/bldkzr_zrgg/index.html)
- [Yindeng transfer result notices](https://www.yindeng.com.cn/xxpl/xxpl_bldkzr/bldkzr_zrjggg/index.html)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Plain-text execution summary plus downloaded PDF files and Excel spreadsheets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes date-stamped local folders containing crawl records, OCR summary spreadsheets, and optional LLM analysis reports.]

## Skill Version(s):

1.0.0 (source: server release and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
