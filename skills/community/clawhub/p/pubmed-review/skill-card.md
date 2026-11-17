## Description:

PubMed Review processes Feishu or OpenClaw natural-language requests into PubMed searches, retrieves article metadata and abstracts, generates brief and full AI-assisted literature reviews, sends notifications, and answers follow-up questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crayfish-ai](https://clawhub.ai/user/crayfish-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Feishu/OpenClaw use this skill to turn natural-language medical literature requests into PubMed retrieval tasks, AI-assisted summaries, local Markdown review files, and follow-up answers grounded in saved PMID context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe configuration and execution paths may affect installation security.

Mitigation: Install in a controlled environment only after fixes or compensating controls are applied.

Risk: MINIMAX_API_URL is configurable and sends prompts containing user queries and article abstracts to an external service.

Mitigation: Pin MINIMAX_API_URL to an approved HTTPS host and disclose that query and abstract content may leave the local environment.

Risk: Shell-based environment loading and configurable notification paths can execute or invoke unexpected local content.

Mitigation: Parse environment files as data, restrict NOTIFY_PATH to a trusted binary, and run cron or dispatcher processes as a dedicated unprivileged user.

Risk: Task IDs and article file paths drive local reads and writes for task queues and review outputs.

Mitigation: Validate task IDs and article paths before execution and restrict filesystem permissions to the skill, task, log, and result directories.

Risk: Generated medical literature reviews and follow-up answers may be incomplete, outdated, or unsuitable for clinical decisions.

Mitigation: Require qualified human review before using generated summaries in medical, research, or publication workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crayfish-ai/skills/pubmed-review)
- [NCBI PubMed ESearch API endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [NCBI PubMed EFetch API endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi)
- [MiniMax chat completion API endpoint](https://api.minimax.chat/v1/text/chatcompletion_v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Feishu notification text, local Markdown review files, JSON task and article files, and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include PubMed identifiers, titles, abstracts, DOI metadata, brief summaries, full structured reviews, and follow-up answers.]

## Skill Version(s):

1.0.1 (source: evidence.release.version, target metadata, artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
