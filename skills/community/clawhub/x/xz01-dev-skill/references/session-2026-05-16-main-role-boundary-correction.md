# Session note: main role boundary correction after PC visual repair

## Context

During a PC homepage visual repair, the user pointed out that the previous fix was not performed through the xz01 role architecture. Hermes main had directly edited HTML/CSS and ran screenshot/AI validation. The user asked whether, according to xz01 skill rules and architecture, all coding should have been handed to Claude.

## Durable lesson

Yes. In xz01 workflow, main is a dispatcher and final reporter, not an implementation worker.

Correct sequence for visible template defects:

```text
user feedback
  -> Hermes main triages and dispatches
  -> Claude Code dev performs HTML/CSS/JS/ThinkPHP changes
  -> independent test role screenshots + deterministic checks + AI visual QA
  -> rule role audits and captures durable guidance
  -> Hermes main summarizes
```

## Pitfall to avoid

Do not treat a small or obvious CSS/template fix as an exception. Speed does not justify role collapse. If main patches templates directly, the workflow loses the independent dev/test separation the user explicitly wants.

## Practical implication

For future xz01 requests such as “PC 端某模块排版有问题”, main should prepare a precise dev task containing:

- affected URL/domain and device;
- screenshot or user-visible symptom;
- relevant files or run directory if already known;
- constraints: do not modify `/root/.openclaw`, preserve DB-route rule, mobile no `target_blank` when applicable;
- request for changed-file summary and self-check notes.

Then main should separately route validation to test instead of self-validating.