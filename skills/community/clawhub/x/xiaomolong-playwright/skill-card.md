## Description: <br>
Browser automation via Playwright MCP for navigating websites, clicking elements, filling forms, taking screenshots, extracting rendered data, debugging browser workflows, and authoring Playwright tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to decide when to use Playwright MCP, direct Playwright scripts, or Playwright tests for real-browser workflows such as forms, screenshots, downloads, rendered-page extraction, debugging, and CI automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags a bundled review helper that can grant a nested reviewer broad local access. <br>
Mitigation: Review that helper before installation or use, run it without yolo mode unless broad access is intentional, and require confirmation before moderation or write actions. <br>
Risk: Browser automation can send requests, cookies, form input, uploads, and page interactions to user-requested websites. <br>
Mitigation: Limit automation to the user's requested targets, use staging or local environments for sensitive flows, and get explicit confirmation before destructive, financial, medical, production, or other high-stakes actions. <br>
Risk: Optional Playwright or Playwright MCP installation downloads packages from npm. <br>
Mitigation: Install only in environments where npm package traffic is acceptable and the packages are trusted for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/xiaomolong-playwright) <br>
- [Publisher profile](https://clawhub.ai/user/linbo405) <br>
- [Skill homepage](https://clawic.com/skills/playwright) <br>
- [npm package registry](https://registry.npmjs.org) <br>
- [Selector strategy and frame handling](artifact/selectors.md) <br>
- [Failure analysis, traces, logs, and headed runs](artifact/debugging.md) <br>
- [Test architecture, mocks, auth, and assertions](artifact/testing.md) <br>
- [CI defaults, retries, workers, and failure artifacts](artifact/ci-cd.md) <br>
- [Rendered-page extraction, pagination, and respectful throttling](artifact/scraping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript or TypeScript code examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser actions that create screenshots, PDFs, downloads, traces, and temporary browser state in the workspace or system temp directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
