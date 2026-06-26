# Runbook Skill Kit Template Factory

This skill provides a general template for producing a reusable documentation-and-skill kit from any validated workflow.
这个 skill 提供一个通用模板，用来把任意已验证流程做成可复用的“文档 + skill”套件。

## What This Skill Is For | 适用场景

Use it when:
适用于：

- you repeatedly convert solved workflows into docs and skills
- you want a consistent file layout
- you want the result to be publishable to ClawHub
- you want a kit that works for both humans and agents

## Output Kit | 产出套件

- knowledge index
- full knowledge runbook
- knowledge FAQ
- self-contained skill bundle
- release changelog

## Included Files | 包含文件

- `SKILL.md`
- `README.md`
- `WORKFLOW.md`
- `TEMPLATES.md`
- `FAQ.md`
- `CHANGELOG.md`

## ClawHub Publish Shape | ClawHub 发布方式

```bash
clawhub publish ./skills/shared/runbook-skill-kit-template-factory \
  --slug runbook-skill-kit-template-factory \
  --name "Runbook Skill Kit Template Factory" \
  --version 1.0.0 \
  --tags latest,template,workflow,runbook,skill,bilingual
```
