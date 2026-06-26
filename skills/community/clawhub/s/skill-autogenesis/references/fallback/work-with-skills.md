# Fallback Copy: work-with-skills.md

Source: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md

Lines 266-286:
266: | **Cost** | Zero tokens until loaded | Small but constant token cost |
267: | **Examples** | "How to deploy to Kubernetes" | "User prefers dark mode, lives in PST" |
268: | **Who creates** | You, the agent, or installed from Hub | The agent, based on conversations |
269: 
270: **Rule of thumb:** If you'd put it in a reference document, it's a skill. If you'd put it on a sticky note, it's memory.
271: 
272: ---
273: 
274: ## Tips
275: 
276: **Keep skills focused.** A skill that tries to cover "all of DevOps" will be too long and too vague. A skill that covers "deploy a Python app to Fly.io" is specific enough to be genuinely useful.
277: 
278: **Let the agent create skills.** After a complex multi-step task, Hermes will often offer to save the approach as a skill. Say yes — these agent-authored skills capture the exact workflow including pitfalls that were discovered along the way.
279: 
280: **Use categories.** Organize skills into subdirectories (`~/.hermes/skills/devops/`, `~/.hermes/skills/research/`, etc.). This keeps the list manageable and helps the agent find relevant skills faster.
281: 
282: **Update skills when they go stale.** If you use a skill and hit issues not covered by it, tell Hermes to update the skill with what you learned. Skills that aren't maintained become liabilities.
283: 
284: ---
285: 
286: *For the complete skills reference — frontmatter fields, conditional activation, external directories, and more — see [Skills System](/docs/user-guide/features/skills).*
