## Description:

Browser automation via Playwright MCP for navigating sites, filling forms, taking screenshots, extracting data, writing tests, and debugging real browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and apply Playwright, Playwright MCP, and related testing patterns for browser automation, UI debugging, screenshots, downloads, CI test runs, and rendered-page extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional npm installs can introduce supply-chain drift if package versions are not controlled.

Mitigation: Use pinned Playwright and Playwright MCP versions or a reviewed lockfile before installation.

Risk: Browser automation can send cookies, form input, uploads, and page interactions to user-requested web origins.

Mitigation: Run only against intended targets, prefer staging or local environments for sensitive flows, and avoid entering secrets unless required and approved.

Risk: Screenshots, traces, videos, PDFs, downloads, and CI artifacts can expose authenticated or confidential page content.

Mitigation: Keep browser artifacts scoped, temporary, and access-controlled; avoid broad uploads for confidential workflows.

Risk: Saved browser sessions can preserve credentials or privileged state across tasks.

Mitigation: Keep saved browser state temporary unless session reuse is intentional and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbo405/skills/xiaomolong-playwright)
- [Skill homepage](https://clawic.com/skills/playwright)
- [Playwright npm package](https://registry.npmjs.org/playwright)
- [Playwright MCP npm package](https://registry.npmjs.org/@playwright%2fmcp)
- [Selector strategy reference](artifact/selectors.md)
- [Debugging guide](artifact/debugging.md)
- [Testing patterns](artifact/testing.md)
- [CI/CD defaults](artifact/ci-cd.md)
- [Rendered-page extraction patterns](artifact/scraping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JavaScript, TypeScript, YAML, and Dockerfile examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; may propose Playwright commands, MCP browser actions, test code, CI configuration, screenshots, traces, PDFs, or extraction steps depending on the user's task.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
