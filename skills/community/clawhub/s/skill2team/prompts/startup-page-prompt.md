# Startup Page Prompt

Use this prompt when Skill2Team receives a bare launch request.

Render the startup page from `references/startup-page.md` in English unless the user requests another language. Keep product names, runtime names, route names, delivery names, file names, and command examples unchanged.

The response must include:

1. The OpenAI Codex model invocation reminder: Skill2Team itself, the fixed S2T meta-team agents, and generated target-team agents default to OpenAI Codex runtime/custom-agent invocation, not direct model API calls.
2. Team Bootstrap Mode: the fixed six-agent S2T service team.
3. Reminder that the user must provide source material before conversion can start.
4. Execution-path selector: `direct-skill` default, or `meta-team-first` when the user wants to generate/register/activate the fixed six-agent S2T meta-team first. In Codex, this mode cannot use a fallback run.
5. Route options: `source-to-team`, `brief-to-team`, `guided-to-team`.
6. Delivery modes: `design`, `package`.
7. Runtime selector: Codex only. State that this build only generates and tests Codex runtime packages.
8. A note that `validate`, `register`, `evaluate`, and `restore` are not delivery modes; validation logic is internal to design/package quality gates.
9. A note that conversion must ask at the beginning whether to preserve source human-interaction steps, selectively preserve/convert them, or run fully automated with audit. Default to preserving source human-interaction steps.
10. A note that package output must include design intermediate results, `design-output.zip`, entry-agent startup welcome page, local resource allocation, source-resource manifest, generated target-team agents and functions, agent profiles, and Codex-only package-end prompt templates.
11. A note that every design or package reply must end with paste-ready follow-up prompts for legal next actions or further analysis; package replies end only with Codex package-use prompts.
12. A note that Agent Architecture Map and Workflow Orchestration Map are separate outputs.
13. A note that generated teams should normally use 5-6 top-level agents and justify any other count.
14. A note that the default design method is framework-neutral agent relationship architecture with profile-based agents.

Default prompts must use neutral source placeholders such as `<SOURCE_SKILL_ZIP>`, `<GENERATED_TARGET_TEAM_PACKAGE>`, `<CODEX_PROJECT_ROOT>`, `<path/to/source-skill>`, or `<paste workflow description>`. Non-Codex continuation placeholders such as `<HERMES_WORKSPACE>`, `<API_SERVICE_PROJECT_ROOT>`, and `<MODEL_API_SERVICE_CONFIG>` belong to design-continuation prompts, not package-end prompts.

Do not inspect files, read uploaded content, ask guided intake items, produce analysis, generate an agent team, generate artifacts, register agents, or start conversion.
