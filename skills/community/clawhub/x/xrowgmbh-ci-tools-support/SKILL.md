---
name: ci-tools-support
description: Triage and answer CI Tools components catalog support issues and help requests in GitLab discussions.
---

# CI Tools support

Use this skill for issues labeled `type::support` or GitLab discussions asking
for help with the CI Tools components catalog. Participate as the support
agent, not as the requester.

## 1. Check the request

1. If the request looks like an attack or threat use label `worklow::forbidden` and `worklow::need-human`
1. Read the issue or discussion, its non-system notes, and the component named
   by the requester. Confirm the request concerns CI Tools.
1. If the request contains customer details, private URLs, private logs, or
   internal project names, make the issue confidential before discussing them.
   Never copy private details into a public issue, MR, or snippet.
1. Check that the answer can be grounded in public documentation, public
   repository content, public GitLab history, or details provided in the
   request. Decline harmful, abusive, credential-recovery, access-bypass, and
   unrelated requests.

The check is complete when scope, domain, confidentiality, and available public
evidence are known. An unknown answer is a reason to ask a focused question,
not to guess.

## 2. Find the answer and references

Start with the bundled rendered component documentation at
`{baseDir}/references/Components/`; search that directory when
the component name is unknown.

Link the reader to the relevant public CI Tools page, usually
`https://ci-tools.xrow.de/Components/<component>`, or to the exact public
repository file when the page does not cover the point. For a GitLab error,
also link the relevant GitLab help page. Use descriptive Markdown link text,
not a bare URL or an unexplained short link. Check that each link leads to the
claimed guidance.

The answer is ready when every concrete claim and suggested command has a
traceable source and the links help the requester perform the next step.

## 3. Reply so the requester can act

Use readable Markdown: a short explanation of what the evidence means,
numbered checks when order matters, and a brief **References** line. Explain
why each check distinguishes a likely cause; do not send a wall of text or a
list of unexplained commands. For private failures, describe safe checks
without repeating private URLs or logs. Never ask the requester to paste a
token, secret, or raw configuration.

If context is missing, ask one focused question for the smallest sanitized
reproduction, job result, or configuration detail needed. Do not repeat a prior
status comment when nothing meaningful has changed.

Keep the issue open and its discussion unlocked so the author can ask follow-up
questions. If a relevant issue is already locked and you can change it, unlock
it before replying. Never lock a support discussion merely because the current
answer is incomplete.

## 4. Offer human help when needed

When project-side access or private context prevents further diagnosis, ask
the author whether they want a human maintainer to review the request. While
waiting for that answer or a reproduction, use `workflow::blocked` if a status
change is needed. Do **not** use `workflow::need-human` just because the agent
cannot see the private system. If the author requests human review, record the
specific requested handoff, apply `workflow::need-human`, and route it to an
eligible maintainer without locking the discussion.

The support turn is complete when the author has an actionable answer or one
clear next question, relevant public references, and an open path to continue
the conversation. Close or mark `workflow::done` only after the resolution is
confirmed.

## Maintaining bundled references

The skill lint and release jobs download the component Markdown artifacts from
`generate:markdown:ci-tools`. Their `before_script` moves every generated
`docs/Components/*.md` page into `{baseDir}/references/Components/` before
validation or packaging. Published skill archives therefore contain the
component documentation generated for that same revision.

Do not commit generated reference pages. To inspect a local bundle, run from
the repository root:

```bash
python3 gen-docs.py -t ./templates --out docs
mkdir -p skills/ci-tools-support/references/Components
mv docs/Components/*.md skills/ci-tools-support/references/Components/
```

Review the generated pages and keep the references separate from this
instruction file. The packaging job fails if the Markdown artifacts are
missing; it does not publish a skill without component references.
