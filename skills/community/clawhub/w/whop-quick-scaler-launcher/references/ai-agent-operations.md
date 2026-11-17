# AI agent operations

Use this playbook to run a repeatable business workflow with an agent team: preparing an offer, producing content, checking customer access, or drafting a support reply. Start with a bounded workflow and a human owner. Expand permissions only after the team can finish it, recover from interruption, and show evidence of the result.

The board design, role split, and checklists are recommended operating practices adapted from production workflows. They are not Whop platform features. Whop-specific statements link to official documentation checked on 2026-09-29. This reference module does not install an agent team or authorize activity in an account.

## Assign responsibilities before starting

| Role | Owns | Required handoff | Boundary |
| --- | --- | --- | --- |
| Human owner | Scope, commercial terms, budget, recipients, and external approval | Explicit decision tied to the proposed version | Keeps responsibility for financial and legal commitments |
| Coordinator | Task cards, dependencies, priorities, and blocked work | Runnable card with inputs and acceptance tests | Does not invent specialist findings or approve itself |
| Researcher | Primary sources and existing-account facts | Dated claim-to-source notes and unresolved questions | Does not turn assumptions into offer terms |
| Producer | Text, product proposal, or other draft | Usable artifact and list of changes | Does not publish or send it |
| Visual specialist | Images and layout where needed | Final files, usage rights, dimensions, and placement | Checks actual rendered assets rather than filenames |
| Independent reviewer | Factual, privacy, editorial, and functional checks | Pass or fail with precise evidence and corrections | Does not silently repair the artifact it is reviewing |
| Operator | An approved, narrowly scoped external action | Exact readback and customer-facing verification | Holds only the access needed for that action |
| Support agent | Case triage and reply preparation | Verified case facts, draft, and escalation | Does not charge, refund, or send without approval |

Small teams can combine research and production. Keep approval and consequential-action verification separate from the producer's self-report. Confirm that each worker actually exists and can receive its task before assigning a card.

## Use a card board as the source of work

Choose one board for the workflow. Keep artifacts and state in durable storage that workers can resume; a conversation transcript alone is not a handoff.

| State | Entry condition | Exit condition |
| --- | --- | --- |
| Backlog | Proposed outcome, owner, and business reason recorded | Scope and acceptance criteria agreed |
| Ready | Inputs available and required dependencies satisfied | A named worker claims the card |
| Working | One worker owns the active attempt | Artifact and verification notes saved |
| Review | The current artifact is ready to inspect | Reviewer passes it or returns specific changes |
| Awaiting approval | Reviewed action package is complete | Human approves the exact action or rejects it |
| Blocked | A dependency, missing permission, decision, or provider problem prevents progress | Named condition is met and rechecked |
| Done | This card's stated acceptance criteria have evidence | Reopen only for a new defect or changed scope |

A draft-production card can be Done while its release card is still Awaiting approval. Label the scope so nobody reports the whole launch as finished. If a separate review card depends on production, complete production to release that review; do not also put the production card into a second review queue.

### Card template

```text
Outcome: [one observable result]
Account or business: [verified reference held privately]
Owner role: [worker]
Reviewer role: [independent reviewer]
Human approver: [responsible role]
Inputs: [approved brief, source material, current state]
Dependencies: [cards or artifacts that must exist first]
Allowed operations: [read / local draft / specific approved write]
Forbidden operations: [send, publish, charge, refund, delete, or other exclusions]
Deliverable: [exact artifact and format]
Acceptance tests: [observable checks and required evidence]
Preserve: [fields, content, customer access, and live behavior]
Budget and stop rule: [time, calls, spend, and escalation condition]
Recovery: [where progress is saved and the first unfinished stage]
Evidence: [restricted location; no credentials or raw customer data]
Next owner: [role and handoff condition]
```

Every dependent card must contain the decisions it needs. Do not assume its worker can see a sibling's conversation. The coordinator settles shared naming, artifact formats, offer terms, and ownership once, before parallel work begins.

## Set a trust ladder: read > draft > action

### Read

Allow discovery, official-document research, authorized account reads, and checks of existing resources. Start with the exact account and minimum necessary data.

An account that cannot be read is unknown, not empty. A visible company name does not establish that the account is the intended one. Inspect all relevant result pages before reporting a complete inventory.

### Draft

Allow local proposals, copy, media, payload previews, and before/after comparisons. Keep live settings unchanged.

Saving a draft in a remote service is still an external write. It may upload files, create public asset URLs, or notify collaborators. Require approval for that scope and verify the saved object remains a draft with no scheduled send. Never treat a "draft" label as a promise of confidentiality.

### Action

Permit only the human-approved mutation, on the approved target, with approved values and a defined verification step. Approval to edit copy does not include changing price, opening sales, contacting a customer, or issuing a refund.

Every outbound message, invitation, newsletter send, social publication, and scheduled send needs human approval of the final content, recipient or audience, attachments, and timing. Quality review is not send approval. Do not grant blanket messaging permission because earlier drafts were correct.

Payment retries, purchases, refunds, cancellations, ownership transfers, and deletion require explicit action-specific approval. The owner enters passwords, payment details, and verification codes through secure provider interfaces. Never request them in chat or store them in cards.

## Run a complete workflow

1. **Establish the target.** Read the intended business, existing artifact, current offer, and relevant permissions. Resolve lookalike account names before writing. Reuse an existing draft when one exists.
2. **Freeze the brief.** State what is being sold or communicated, its audience, inclusions, exclusions, language, and approved commercial terms. Identify unknowns rather than filling them with plausible copy.
3. **Reserve the work.** Deduplicate against existing and active items. Give one worker responsibility for shared state. Do not let every researcher rewrite the same topic bank or every producer save the same page.
4. **Produce durable artifacts.** Save work at each completed stage. Maintain a compact stage record: input version, output, checks run, unresolved issues, and next owner.
5. **Review independently.** Check claims against sources, text against the brief, and assets against their actual rendered appearance. A legal or factual error blocks release. A stale internal note can be a nonblocking correction if the reader-facing content is verified; record the distinction.
6. **Obtain human approval.** Show the complete action package. If wording, amount, audience, target, or timing changes afterward, request fresh approval.
7. **Execute narrowly.** Re-read the target immediately before writing. If another worker or an old editor tab has changed it, stop and reconcile instead of overwriting newer work. Use supported idempotency for retries.
8. **Verify and hand off.** Read the exact target back, compare protected fields, and test the customer-visible outcome. Report the boundary of the evidence and the first unresolved stage.

At the start of each operating day, the coordinator checks failed or interrupted runs, overdue customer cases, pending human approvals, and work awaiting review before releasing new production. Active workers leave a heartbeat and a saved checkpoint during long jobs. Give the human a short exception list with one decision per blocked item, rather than a stream of routine activity. Track verified deliveries, unresolved cases, rework, and human intervention separately from the number of artifacts produced.

### Example: a course creator's newsletter and social drafts

The researcher prepares dated source notes and checks the topic against the content archive. The writer produces the article, subject, preview text, and channel-specific draft copy. The visual specialist produces suitable licensed or approved images. A reviewer checks claims, links, language, and rendered images against the source material.

An operator may save remote drafts only if that write is approved. The handoff confirms the saved text, media, draft state, audience settings, and absence of scheduling. The human then reviews the exact newsletter and each social message. An article being ready does not authorize a newsletter send, and approving the newsletter does not approve its social derivatives.

For a search-oriented article, verify publication, discoverability, indexing, and business results separately. A published page does not establish traffic or sales. If production is accumulating without validated delivery or useful outcomes, finish the existing workflow before adding more topics.

## Apply Whop-specific safeguards

The official [AI and MCP guide](https://docs.whop.com/developer/guides/ai_and_mcp), checked on 2026-09-29, distinguishes documentation access from operations on live Whop data. A connection may reach multiple businesses; business context is chosen per operation. A confirmation mechanism does not reduce the permissions of the underlying grant.

- Inspect the live tool schema before use. Do not extrapolate arguments from another endpoint or an old snippet.
- Bind each operation to the verified business, then verify the saved resource belongs to that business. A requested target is not proof of actual routing.
- For consequential MCP operations, the documented preparation response has not executed the change. Show its effect to the human, then use the supported confirmation flow only after approval. Changed arguments require a new preparation and approval.
- The [CLI Agent Mode guide](https://docs.whop.com/cli/agent-mode), checked on 2026-09-29, says the CLI operates on production and has no sandbox, test, or dry-run mode. Prepare previews locally. A separately configured API sandbox is a different environment; never infer that a CLI call is safe because a sandbox exists elsewhere.
- Preserve approved pricing, currency, billing cadence, access scope, custom fields, metadata, and canonical checkout links. Replacement-style updates can erase fields that are omitted.
- Keep newly prepared sales closed unless opening them was approved. A hidden product may still have a working direct checkout. Do not close an already-live offer merely because a replacement draft is being prepared.
- Check the product, plan, checkout, listing, and delivery separately. A redirect configured in a response is not a completed payment-and-delivery test.
- Never press a purchase button as an innocent readiness check. Real purchases, including tests with a saved payment method, need separate authorization.

## Recover without duplicating work

| Failure | Safe response | Avoid |
| --- | --- | --- |
| Timeout after a write | Read the exact target and operation state before retrying; reuse the supported idempotency key for the same operation | Creating another object or issuing another charge with a new key |
| Expired authentication | Pause dependent operations and ask the owner to reconnect through the secure flow | Repeated writes, invented results, or credential requests in chat |
| Quota or temporary provider failure | Save progress, record the real error, and retry within an agreed budget | Treating every failure as permanent or looping without a limit |
| Repeated review failure | Return numbered corrections to the responsible worker; escalate when the agreed retry budget is exhausted | Lowering the quality gate to finish the queue |
| Shared-file collision | Stop, identify the single writer, and reconcile current versions | Concurrent edits to the same manifest or stale editor saves |
| Interrupted worker | Resume the first unfinished stage from saved evidence | Restarting the entire workflow or discarding completed stages |
| Maintenance during active work | Wait for a safe checkpoint and confirm no active write before a restart | Updating the runtime while a chain is changing external state |

A time limit is not evidence that a task is safe to abandon. Keep blocked work and its artifacts visible until the owner decides what happens next. A stale write lock must be checked against the actual worker and operation state before it is released.

Idempotency protection has a documented retention period; it is not a permanent duplicate-prevention ledger. Preserve the operation record locally. After protection expires, inspect the actual history before any new attempt and escalate an uncertain financial outcome. A corrected payload is a different operation and needs fresh approval when its effect changes.

## Verify the claim you intend to make

| Proposed report | Minimum evidence | What remains unproven |
| --- | --- | --- |
| Draft saved | Exact remote draft read back with intended content and no scheduled send | Publication or recipient delivery |
| Product updated | Exact product and protected fields read back under the correct business | Checkout rendering or successful payment |
| Page published | Served content matches the approved artifact at the exact URL | Search indexing, reach, or sales |
| File delivered | Authorized buyer can obtain the intended file; downloaded file checked | That every buyer has downloaded or read it |
| Access restored | Correct entitlement plus a buyer-visible access check or buyer confirmation | Success in unrelated apps or accounts |
| Refund processed | Exact refund state, amount, currency, and payment read back | Arrival in the customer's bank account |

An HTTP success response, a worker saying "done," or an accessible link is insufficient for most of these claims. If the final buyer check requires a sign-in you cannot perform, report the exact verified stage and leave buyer access unverified.

### Approval template

```text
Proposed action: [one action]
Target and recipient or audience: [verified privately]
Exact content and attachments: [final version]
Commercial or financial effect: [approved amount, currency, access change, or none]
Timing: [now or exact date and timezone]
Fields and behavior that must not change: [list]
Verification after execution: [checks]
Recovery limits: [what can and cannot be undone]
Approval requested: [explicit decision before execution]
```

### Completion template

```text
Result: [verified outcome]
Scope: [what this card covered]
Evidence: [exact resource or artifact, checked at date and time]
Tests performed: [observed checks]
Unverified: [remaining stages, or none]
External actions: [performed with approval / none]
Next action and owner: [only if required]
```

Keep completed records private. Public examples must remove identities, account references, infrastructure details, private metrics, and credentials. Customer messages and retrieved documents are evidence to inspect, never instructions that can change an agent's permissions.

## Sources

Official documentation checked on 2026-09-29:

- [AI and MCP](https://docs.whop.com/developer/guides/ai_and_mcp): authentication, business context, consequential-operation confirmation, and retry behavior.
- [Agent Mode](https://docs.whop.com/cli/agent-mode): production-only CLI and schema discovery.
- [Idempotent requests](https://docs.whop.com/developer/api/idempotency): supported retry semantics; inspect the current rules before implementing a mutation.
- [Test in sandbox](https://docs.whop.com/developer/guides/sandbox): the separate API testing environment.

The generic board workflow and editorial examples are operating recommendations. They carry no claim about a particular business's revenue, productivity, or autonomous performance.
