# Fallback Copy: sessions.md excerpts

Source: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/sessions.md

Lines 356-366:
356: - **idle** — reset after N minutes of inactivity
357: - **daily** — reset at a specific hour each day
358: - **both** — reset on whichever comes first (idle or daily)
359: - **none** — never auto-reset
360: 
361: Before a session is auto-reset, the agent is given a turn to save any important memories or skills from the conversation.
362: 
363: Sessions with **active background processes** are never auto-reset, regardless of policy.
364: 
365: ## Storage Locations
366: 

---

Lines 383-393:
383: ## Session Expiry and Cleanup
384: 
385: ### Automatic Cleanup
386: 
387: - Gateway sessions auto-reset based on the configured reset policy
388: - Before reset, the agent saves memories and skills from the expiring session
389: - Ended sessions remain in the database until pruned
390: 
391: ### Manual Cleanup
392: 
393: ```bash
