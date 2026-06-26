## Description: <br>
REAL 人格测试 scans a user's logged-in social media accounts, analyzes posts, likes, saves, follows, and interactions, and classifies the user into one of 16 data-driven REAL personality types with a match score and report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent to inspect their own social media behavior and produce a data-driven personality analysis. The skill is intended for entertainment-oriented self-discovery, not psychological diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may inspect logged-in social media histories, including posts, likes, saves, follows, and other behavior that can reveal sensitive interests or relationships. <br>
Mitigation: Run the skill only on accounts the user owns or controls, use a separate browser profile where possible, and confirm the platforms and data categories before scanning. <br>
Risk: The skill stores behavioral data and generated reports locally, which may expose private information if shared or left behind. <br>
Mitigation: Review, redact, or delete generated real-data files and reports after use, and share only intentionally selected excerpts. <br>
Risk: Personality labels and match scores may be treated as more authoritative than the underlying social-media behavior supports. <br>
Mitigation: Present results as entertainment-oriented data analysis, not as psychological diagnosis or advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sophie-xin9/real-personality) <br>
- [README](artifact/README.md) <br>
- [REAL type system](artifact/types/type_system.md) <br>
- [Example REAL report](artifact/examples/xiaokai_real_report.md) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, shareable text card, local JSON data, and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include local real-data files and personality reports derived from logged-in social media account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
