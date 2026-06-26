# Skill Intake Checklist

Use this checklist when a user shares a new skill link or asks whether a skill is worth installing.

## 1. Clarify the need
- What concrete capability does the user want?
- Is this a real missing capability or just a different packaging of something already available?
- Is the skill capability-type or methodology-type?

## 2. Classify before touching the package
- Capability skill: adds search, extraction, file processing, automation, browser control, etc.
- Integration skill: depends on credentials, env vars, service state, runtime placement, or host process environment.
- Automation skill: controls browsers, workflows, CLIs, runtime side effects, or long-running operations.
- Workflow/methodology skill: mainly guidance, habits, prompts, or process suggestions.
- Bridge skill: mainly points to another ecosystem, package manager, or marketplace.
- Incomplete shell: docs/meta only, missing code or resources implied by docs.

Different classes need different checks. Integration and automation skills require stronger dynamic validation than workflow skills.

## 3. Security and fit review
- Check actual files in the package.
- Look for scripts, package manifests, env vars, hooks, installers, global writes.
- Check whether docs promise code that is not present.
- Check whether it introduces another tool ecosystem or package manager.
- Estimate token cost if the skill adds reminders, hooks, or long references.
- Judge whether it fits the current OpenClaw workflow and the user's boundaries.
- Check **environment landing zone**: does it need to work only in the current shell, or also in gateway / LaunchAgent / cron?
- Check **verification level** actually achieved: downloaded, installed, configured, current shell verified, gateway verified, cron verified.

## 4. Decision buckets
### Install candidate
Use when all are true:
- Adds a concrete capability
- Package is complete enough to verify
- Risks are understandable and acceptable
- Clear value for current workflow
- Required validation level is achievable

### Install, but require dynamic validation
Use when all are true:
- The package seems real and valuable
- But usefulness depends on runtime environment, credentials, binaries, proxy, browser, daemon, gateway, or cron
- Static review alone is not enough to call it ready

### Review-only / absorb ideas
Use when any are true:
- Mostly methodology or prompt guidance
- Good ideas, but not worth adding as a formal skill
- Better absorbed into SOUL.md / AGENTS.md / TOOLS.md / memory

### Reject / do not install
Use when any are true:
- Package is incomplete
- Depends on another ecosystem without clear need
- High-risk automation with weak value
- Adds token-heavy complexity without clear gain

## 5. User-facing output template
- Conclusion: install / do not install / review-only
- What it actually does
- What files/code are really present
- Risks
- Fit with current workflow
- Recommendation

## 6. Internal principle
Prefer a small number of trustworthy, capability-oriented skills over a large pile of loosely-audited workflow skills.
