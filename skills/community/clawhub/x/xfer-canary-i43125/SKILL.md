---
name: Xfer Canary i43125
description: Authorized ownership-transfer state-machine canary used during a sanctioned security assessment of ClawHub.
version: 0.0.1
---

# Xfer Canary i43125

This skill is a controlled canary created for an authorized application security assessment of the ClawHub platform. Its sole purpose is to exercise the skill ownership-transfer state machine (request, outgoing listing, incoming listing, accept, reject, cancel) so that the assessment team can verify whether transfer decisions are correctly scoped to the authenticated party.

## What this skill does

This skill performs no network calls, runs no code, stores no credentials, and has no side effects. It contains a single Markdown document. It exists only as a database row that can be moved between two test accounts during the assessment.

## Transfer state machine under test

The transfer flow is expected to behave as follows:

1. The owner requests a transfer by calling the transfer endpoint with the recipient handle. A pending transfer record is created that references the source skill, the sender user id, and the recipient user id.
2. The sender can list outgoing pending transfers and the recipient can list incoming pending transfers, each scoped to the authenticated user.
3. The recipient may accept or reject the pending transfer. Accepting reassigns the skill owner to the recipient personal publisher and rewrites related embeddings, aliases, and audit logs.
4. The sender may cancel the pending transfer while it is still pending.
5. A third party who is neither the sender nor the recipient must not be able to accept, reject, or cancel the transfer.

## Safety notes

Everything here is inert documentation used to validate authorization boundaries. After the assessment the skill is deleted or transferred back so that no residual state remains on the production deployment.
