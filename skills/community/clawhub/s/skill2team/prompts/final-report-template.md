# Final Report Template

Write the report in the user's language unless explicitly overridden. Keep machine-readable identifiers, file names, runtime names, and code blocks in their original form.

# Skill2Team Report

## 1. Executive summary
## 2. OpenAI Codex model invocation policy
## 3. Execution-path log
## 4. Route and delivery log
## 5. Original workflow extraction
## 6. Asset diagnosis
## 7. Decomposition lens analysis
## 8. Design intermediate results
## 9. Recommended target-team agents and functions
## 10. Agent Architecture Map
## 11. Workflow Orchestration Map
## 12. Control-Flow & Resume Contract
## 13. Human-interaction preservation and required user input nodes
## 14. Entry-agent startup welcome page
## 15. Skill allocation matrix
## 16. Handoff and gate contracts
## 17. Codex package artifact plan
## 18. Package release gate and post-package readiness contract
## 19. Runtime invocation and prompt rewrite policy
## 20. Local resource allocation and source-resource manifest (`local-resource-allocation.map.json`, `source-resource-manifest.json`)
## 21. Follow-up prompts for use and further analysis
## 22. Design-continuation prompts when delivery is `design`
## 23. Package-end Codex package-use prompts when delivery is `package`
## 24. Unresolved questions and risks

End every design report and every package report with paste-ready prompt templates for legal next actions outside Skill2Team delivery. For design, include at least package generation, further design/resource-gate analysis, Codex/OpenAI registration guidance, API-service runner construction, API-run role simulation, Hermes profile conversion, and OpenClaw profile conversion. For package, include only Codex package-use prompts: artifact-only inspection, package release/resource-gate analysis that reads `local-resource-allocation.map.json` and `source-resource-manifest.json`, Codex post-package registration/use guidance, registered entry-agent use after real Codex smoke tests pass, and current-session target-team fan-out when registered agent types are unavailable.

Do not end with post-package delivery commands. Skill2Team exposes only `design` and `package`; registration, evaluation, restore, and external conversion are documented as user-run follow-up prompts outside the Skill2Team delivery set.
