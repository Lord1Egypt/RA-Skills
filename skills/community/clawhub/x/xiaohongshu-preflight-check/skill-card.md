## Description:

小红书发布前文本合规自查（4 组）：违禁词、敏感词、限流词、标题与篇幅规范、AI 声明、强制标注和导流风险；纯本地运行，不调用付费 API，并用退出码支持发布流程拦截。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

External creators, operators, and content workflow maintainers use this skill before publishing Xiaohongshu notes to check draft text against local platform-rule and wordlist checks. It helps identify blocking P0 issues, advisory P1 items, AI disclosure reminders, and text-only gaps before a human publishes the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker depends on the separately installed xiaohongshu-prohibited-words skill and its local parser.

Mitigation: Install and trust that dependency before use, and treat exit code 3 as a blocked check rather than a pass.

Risk: The skill checks text only and does not evaluate images, cover text, video, or the live publishing interface.

Mitigation: Review non-text assets and final platform disclosure controls manually before publishing.

Risk: Results depend on the current bundled platform rules and wordlist quality.

Mitigation: Keep the platform rules and wordlist dependency current, rerun the self-test after updates, and review advisory output before release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniegeng-max/skills/xiaohongshu-preflight-check)
- [Publisher profile](https://clawhub.ai/user/bonniegeng-max)
- [Xiaohongshu platform rules](references/platforms/xiaohongshu.json)
- [Wordlist bridge](references/wordlist-bridge.md)
- [Examples](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain-text or JSON CLI preflight report with process exit code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes: 0 pass, 1 P0 blocking issue, 2 P1 advisory issue only, 3 fail-closed error such as missing input, missing wordlist, or parse failure.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
