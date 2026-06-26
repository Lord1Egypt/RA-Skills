## Description: <br>
Webpage to PDF and Markdown converter that saves URLs, especially WeChat articles, as offline-readable files with images, layout, and styles preserved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinkaizhou](https://clawhub.ai/user/qinkaizhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to archive single URLs or batches of URLs as PDF and Markdown files for offline reading, review, or retention. It is especially oriented toward WeChat article capture while also supporting regular webpages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default browser mode can control a real logged-in Chrome profile and access cookies or active sessions. <br>
Mitigation: Prefer --isolated or HTTP mode for public pages, and reserve default browser mode for trusted pages that require login. <br>
Risk: The CDP proxy can open a local port and write temporary state files under cdp-proxy-<user>. <br>
Mitigation: Run as a normal user, keep browser automation limited to trusted content, and clean or stop CDP proxy state after handling private content. <br>
Risk: Broad Chrome DevTools Protocol utilities require review before installation. <br>
Mitigation: Review and scan the skill before deployment, and run browser mode in a VM or sandbox when handling sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinkaizhou/url2pdf-mk) <br>
- [Publisher profile](https://clawhub.ai/user/qinkaizhou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated agent workflow may create PDF and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser mode can produce PDF and Markdown; HTTP mode produces Markdown only.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md changelog, released 2026-04-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
