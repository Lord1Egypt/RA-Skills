# Requirement Analysis Assistant Skill

[Simplified Chinese README](README.zh-CN.md)

A Codex and OpenClaw compatible Agent Skill for turning rough business ideas, screenshots, sketches, and existing PRDs into structured product requirement artifacts.

This skill is designed for product managers, publishing teams, game operations, growth teams, designers, QA, and business stakeholders who need repeatable PRD drafting, requirement breakdown, prototype outlines, HTML demos, visual requirement analysis, edge-case discovery, and requirement quality checks.

## What It Does

- Converts rough requirement directions into PRD drafts.
- Generates clarification questions when key information is missing.
- Produces prototype or wireframe structures.
- Generates low-fidelity HTML demo pages for quick requirement alignment.
- Analyzes screenshots, sketches, competitor pages, or admin UI images into PRD-ready feature points.
- Expands common publishing scenarios, including website campaigns, recharge centers, user acquisition, SDK integration, and admin configuration.
- Reviews existing PRDs for missing rules, risks, edge cases, and acceptance criteria.

## Repository Structure

```text
.
+-- SKILL.md
+-- README.md
+-- README.zh-CN.md
+-- LICENSE.txt
+-- agents/
|   +-- openai.yaml
+-- references/
    +-- prd-template.md
    +-- publishing-scenarios.md
    +-- quality-checklist.md
    +-- visual-prototype.md
```

## Compatibility

This repository is intentionally kept as a standalone skill folder:

- Codex can install a skill from a GitHub directory that contains `SKILL.md`.
- OpenClaw can load a skill from a folder containing `SKILL.md` with YAML frontmatter.
- The skill uses only `name` and `description` frontmatter for maximum compatibility.
- No scripts, network calls, secrets, or executable installers are included.

## Optional Tooling

The skill works with only a text-capable agent, but it becomes more useful with:

- File tools: save PRDs, HTML demos, and analysis reports.
- Browser or Playwright tools: preview generated HTML demos.
- Figma or design tools: turn prototype outlines into design screens.
- Image-capable models/tools: analyze screenshots and sketches.
- Knowledge retrieval: use organization-approved PRD templates, historical examples, and business glossaries.

## Install In Codex

Use the skill installer with your GitHub repository URL:

```text
$skill-installer install https://github.com/<owner>/<repo>
```

Or copy this folder into:

```text
$CODEX_HOME/skills/requirement-analysis-assistant
```

Restart Codex after installation so the skill is discovered.

## Install In OpenClaw

Install from Git if your OpenClaw version supports Git skill installs:

```bash
openclaw skills install git:<owner>/<repo>@main
```

Or copy this folder into one of OpenClaw's skill roots:

```text
~/.openclaw/skills/requirement-analysis-assistant
<workspace>/skills/requirement-analysis-assistant
```

Then check or refresh skills:

```bash
openclaw skills list
openclaw skills check
```

## Example Prompts

```text
Use $requirement-analysis-assistant to turn this idea into a PRD:
We want to build an official website reservation campaign. Users can reserve before launch and claim a gift pack after launch. Operations need to configure rewards and campaign time in the admin panel.
```

```text
Use $requirement-analysis-assistant to create a low-fidelity HTML demo for an official website reservation campaign with reservation, reward claim, and admin configuration states.
```

```text
Use $requirement-analysis-assistant to analyze this screenshot and turn it into visible facts, inferred requirements, admin configuration needs, edge cases, and PRD feature points.
```

```text
Use $requirement-analysis-assistant to review this PRD and list missing edge cases, admin rules, data tracking, and acceptance criteria.
```

```text
Use $requirement-analysis-assistant to generate a prototype outline for a recharge center with package configuration, payment status, and order history.
```

## Recommended Usage

For best results, provide:

- Business objective
- Target users
- Platform or channel
- Main user path
- Rules that are already confirmed
- Admin configuration needs
- Data metrics or reporting needs
- Known launch constraints
- Screenshots, sketches, or competitor references when visual analysis is needed

If some information is missing, the skill will separate facts, assumptions, and confirmation questions.

## Organization Customization

Keep the public skill generic. Add organization-specific materials only in your private copy:

```text
references/
  company-prd-template.md
  company-writing-style.md
  company-scenarios.md
  company-quality-checklist.md
  cases/
    website-campaign-001.md
    recharge-center-001.md
```

When these files exist in a private copy, you can instruct the agent to prefer those organization-specific references over generic templates.

## License

MIT-0. See `LICENSE.txt`.
