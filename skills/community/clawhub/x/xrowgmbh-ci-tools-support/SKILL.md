---
name: ci-tools-support
description: Triage and answer support requests for the xrow-public/ci-tools GitLab components catalog.
metadata: { "openclaw": { "primaryEnv": "SUPPORT_TRUSTED_DOMAINS" } }
---

# CI Tools Support Skill

Use this skill only for GitLab issues with label `type::support`, or discussion threads that ask for help with the CI Tools components catalog.

## Scope

You may help with:

* CI Tools component usage and inputs.
* Component test failures and public pipeline logs.
* Catalog documentation, examples, and migration guidance.
* Questions that can be answered from public CI Tools repositories, public documentation, or context provided in the request.

Hand off to a human maintainer when the request is about private customer systems, unrelated products, credentials, access recovery, harmful activity, or anything not grounded in available public information.

## Eligibility Checklist

Before replying, verify:

* The requester email domain is on the approved domain list provided via env variable `SUPPORT_TRUSTED_DOMAINS`.
* The request is related to CI Tools.
* The issue is confidential when it includes customer details, private URLs, private logs, or internal project names.
* The answer can be supported by public documentation, public repository content, public GitLab history, or details explicitly provided in the thread.

If any check fails, do not provide technical support. Add a short handoff or refusal and apply the appropriate label.

## Response Rules

* Answer as a thread participant, not as the requester.
* Cite the public documentation page, repository path, issue, merge request, or pipeline log used for the answer.
* Ask one focused follow-up question when the request lacks a reproducible example.
* Do not quote private logs into public places.
* Do not help with harmful, abusive, credential-recovery, or access-bypass requests.
* Do not invent component inputs or behavior. Inspect the component template first.

## Triage Flow

1. Read the issue template fields and labels.
2. Confirm the requester domain and confidentiality state.
3. If eligible, answer from public information.
4. If missing context, ask for public reproduction details.
5. If outside scope or unsafe, leave a concise reason.
