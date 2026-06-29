# Package-End Codex Register/Start Prompt

```text
You are working inside <CODEX_PROJECT_ROOT> with OpenAI Codex available.
Register and start the shared target-team package at <GENERATED_TARGET_TEAM_PACKAGE>.

Requirements:
1. Inspect the package manifest and identify the entry agent.
2. Copy or merge .codex/agents/*.toml into the current project's .codex/agents/ directory.
3. Merge any required .codex/config.toml settings without overwriting unrelated local configuration.
4. Copy .codex/s2t-agent-registrations/<team_id>.json into the project's .codex/s2t-agent-registrations/ directory.
5. Confirm [features] multi_agent = true and enable_fanout = true when required by the package.
6. Run smoke tests for entry-agent discovery and specialist handoff readiness.
7. Start the registered entry agent with the user's source task.

Do not hard-code source-specific names. Use the package manifest, profile files, and registry files as the source of truth.
```
