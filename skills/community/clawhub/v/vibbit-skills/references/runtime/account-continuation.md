# Account actions and continuation

Read only when credentials are missing, the user wants their own reusable avatar, or credits are insufficient. Keep account actions within the current creative workflow; return to the same task without repeating settled questions.

## Preserve progress before handoff

Add the account step to `production` in the current [creative handoff](../contracts/creative-handoff.md). Reference existing project/run versions rather than copying the adopted script. When persistence across turns is needed, save in the user's current project, never in the Skill:

- `account_step`: `configure_key`, `create_avatar`, or `add_credits`.
- `api_base`, current workflow, and unfinished stage; use the same region and account on the website.
- References to adopted copy, constraints, selected avatars/voices/settings, input media, and successful outputs.
- Original submission_id, task_id, request_id, state_file, and actual status. Do not invent server IDs for unsubmitted steps.
- `next_action`: the step to run after setup, resources to refresh after cloning, or task to check after resolving credits.
- If avatars were already queried, keep the current ID set and the desired avatar description to identify new candidates on return.

Never store API keys, cookies, upload credentials, or the local setup session URL in creative records or task journals. Preserve existing journal redaction rules. Claim progress was saved only after successful persistence.

## Give an actionable entry and one clear instruction

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" account_links
~~~

The offline command returns this region's `api_keys`, `create_avatar`, `avatars`, `pricing` (plans/credit packs), and `billing` (account management) links. For an unknown/custom API environment without a website mapping, verify the entry instead of guessing a domain. Do not put keys or media in URLs. Open the relevant page when supported and include a clickable link; otherwise provide the link. Do not claim a nonexistent host settings window was opened.

| Action | User-facing guidance | On return |
| --- | --- | --- |
| Key setup | “Open the setup page, create a key, then paste and verify it. I will continue this production.” | Read the setup result using [authentication](authentication.md); after native settings, verify once and continue the original stage |
| Personal avatar | “Create your avatar here using the page's material requirements. Reply ‘continue’ when done; I will refresh the list and resume.” | Follow [avatar creation](../capabilities/generation/digital-human-creation.md); refresh and match without asking for an ID |
| Insufficient credits | “This step needs more credits. Your completed work is preserved. Open pricing for plans or credit packs, then reply ‘continue’ so I can pick up here.” | Check the original task and reuse successful assets; proceed only with unfinished work within authorization |

There is no account-action callback. The local setup process can directly report success; other host setup, cloning, and billing actions normally need the user's “continue” before checking. Opening a page is not completing the action. Do not poll while waiting for payment or human review. Continue independent script/storyboard work where useful without claiming blocked steps are complete.

## Continue after credit handling

Use the CLI's `account_action` when present. `1007` / `INSUFFICIENT_POINTS` routes to `/pricing` for plans or credit packs in the same account; `1008` requires checking the actual quota restriction, which buying credits may not resolve. Show balances, required credits, or shortfalls only when actually returned. The user makes purchases; the Skill does not order, pay, or repeatedly submit requests to probe the balance.

| Original state | Next action |
| --- | --- |
| Not submitted because credentials were missing | After verification, submit the original step once |
| Existing task_id, pending/running or uncertain status | GET / `resume` the original task before any new submission |
| Submission outcome unknown, with no task_id | Preserve uncertainty and investigate; topping up or changing keys does not remove duplicate-charge risk |
| Definitive rejection or terminal insufficient-credit failure | Topping up cannot revive the old task. Preserve its journal and submit only the failed step with a new journal within the original authorization; reuse successful audio/images |
| Partial success, including translation | Keep and deliver successful items. Redo failed items only where the API supports it; explain scope and additional costs if targeted recovery is unavailable |
| Completed | Reuse the result and continue the next production stage |

After account/region changes or resource ownership mismatches, query available resources again instead of using private IDs from the previous account. Persistent errors require a specific explanation and next step, not a loop of setup, billing, or regeneration requests.
