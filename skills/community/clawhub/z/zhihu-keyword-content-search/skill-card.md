## Description: <br>
Searches Zhihu questions by keyword, sorts high-answer-count questions, crawls related answers, and saves the results as JSON and plain text. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[taiyuexiao](https://clawhub.ai/user/taiyuexiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to collect Zhihu question-and-answer content for keyword-focused review, local analysis, or downstream summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A full Zhihu login cookie is required and could expose the user's account session if shared or logged. <br>
Mitigation: Treat the cookie like a password, avoid putting it in shared logs, screenshots, shell history, or saved scripts, and rotate or log out the session if it is exposed. <br>
Risk: Crawled Zhihu content is saved locally as JSON and plain text and may contain sensitive or copyrighted material. <br>
Mitigation: Use a dedicated output folder and review saved files before sharing, publishing, or reusing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/taiyuexiao/zhihu-keyword-content-search) <br>
- [Zhihu](https://www.zhihu.com) <br>
- [Zhihu Search API](https://www.zhihu.com/api/v4/search_v3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands; crawler output is JSON files and merged plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied Zhihu login cookie and writes results to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
