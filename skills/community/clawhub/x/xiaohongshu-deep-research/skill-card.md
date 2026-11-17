## Description:

Researches Xiaohongshu topics by searching posts, ranking high-engagement results, and producing a concise analysis report with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palmpalm7](https://clawhub.ai/user/palmpalm7)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to research Xiaohongshu topics, understand trends from search-result metadata, and generate shareable Markdown summaries with links to relevant posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a local Xiaohongshu MCP service with a logged-in account and saves topic research artifacts locally, which may expose sensitive research interests on the machine.

Mitigation: Before use, confirm the local service and account are intended for this research, and review or delete ~/xiaohongshu-research/ when topics are sensitive.

Risk: Reports are based on search-result metadata and cannot include post body text or comments.

Mitigation: Treat generated findings as metadata-based trend analysis and verify important conclusions against the linked Xiaohongshu posts.

## Reference(s):

- [Detailed Workflow](references/workflow.md)
- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
- [Xiaohongshu Post Links](https://www.xiaohongshu.com/explore/{id})

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report with local JSON data files and inline shell/API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores searched post metadata, generated reports, and research metadata under ~/xiaohongshu-research/.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
