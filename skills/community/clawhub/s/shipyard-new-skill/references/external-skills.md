# Good skills that already exist (point to them, do not copy)

Before building a new skill, check whether one of these already does the job. Shipyard links to them; it does not ship copies. Install sources checked on GitHub in October 2026. Each is someone else's code: read its SKILL.md before installing and tell the student what it can run.

## Find a skill first

- **find-skills** (Vercel): searches the open skills directory and installs a match. Source `github.com/vercel-labs/skills` (`skills/find-skills`). Install: `npx skills add vercel-labs/skills --skill find-skills`. Browse at skills.sh.

## Ways of working

- **superpowers** (Jesse Vincent): brainstorm > plan > test-first build > review workflows. Plugin marketplace `obra/superpowers-marketplace`, plugin `superpowers`; other agents: see its README. Source `github.com/obra/superpowers`.
- **caveman** (Julius Brussee): very short replies to save tokens, plus caveman-commit, caveman-review and caveman-compress. Plugin marketplace `JuliusBrussee/caveman`, plugin `caveman`; Cursor and other agents: see its README. Source `github.com/JuliusBrussee/caveman`. Do not use it for messages the student's users will read.
- **compound-engineering** (Every): plan > work > review > "compound" (write down what was learned so the next task is easier). Source `github.com/EveryInc/compound-engineering-plugin`; follow its README for the marketplace command.

## Official skills from the agent maker

- **skill-creator**: write and test new skills; use it alongside `/shipyard:new-skill`. Source `github.com/anthropics/skills` (`skills/skill-creator`). It is also a plugin marketplace (`anthropics/skills`). The same repo has **frontend-design** and **webapp-testing**.
- **Engineering plugin** from `github.com/anthropics/knowledge-work-plugins` (`engineering/skills`): **code-review**, **debug**, **deploy-checklist**, **testing-strategy**, **system-design**, **tech-debt**, **documentation** (also architecture, incident-response, standup). Add the marketplace `anthropics/knowledge-work-plugins`, then install its `engineering` plugin. Overlaps with Shipyard: deploy-checklist and launch's go-live check; prefer Shipyard's `launch-check.mjs` for Shipyard apps and use deploy-checklist for anything else.

## Domain skills worth knowing

- **react-best-practices** (installed as vercel-react-best-practices) and **deploy-to-vercel**: Vercel's own guidance, `github.com/vercel-labs/agent-skills` (`skills/`).
- **supabase-postgres-best-practices**: Supabase's Postgres rules, `github.com/supabase/agent-skills` (`skills/`).
- **logo-design-skill**: `github.com/kaankiziltug/logo-design-skill`; Shipyard's design skill makes icons, this one is for a full logo set.

## How to recommend

Name at most two that fit the request, say what each adds and what it overlaps with in Shipyard, and install only with the student's yes.
