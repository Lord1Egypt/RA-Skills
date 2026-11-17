## Description:

Searches Zhihu questions by keyword, ranks matching questions by answer count, and crawls answers into JSON and plain text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taiyuexiao](https://clawhub.ai/user/taiyuexiao)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to search, crawl, or analyze Zhihu Q&A content for selected keywords. It is suited to workflows where the user can provide an active Zhihu session cookie and review the saved local data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to pass a full logged-in Zhihu browser cookie on the command line.

Mitigation: Run it in a dedicated environment, avoid shared terminals and logs, clear shell history after use, and revoke or refresh the Zhihu session afterward.

Risk: The skill stores scraped answer data locally as JSON and merged plain text.

Mitigation: Choose an appropriate local output directory, limit access to generated files, and review retained data before sharing or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taiyuexiao/skills/zhihu-keyword-content-search)
- [Zhihu](https://www.zhihu.com)
- [Zhihu question search API](https://www.zhihu.com/api/v4/search_v3)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Text, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated JSON files and merged plain text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied Zhihu login cookie and writes results to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
