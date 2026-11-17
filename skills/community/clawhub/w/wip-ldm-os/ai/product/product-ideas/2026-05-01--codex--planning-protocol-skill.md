# Product Idea: Planning Protocol Skill

**Date:** 2026-05-01
**Status:** idea
**Owner:** Parker decides whether to turn this into a plan

## Idea

We need a small planning protocol for agents.

When an agent writes a plan document, it should not only describe the work. It should also describe the collaboration shape required to execute the work.

At minimum, every serious plan should answer:

- Who is the coder?
- Who is the reviewer or partner?
- Is there a security reviewer?
- Is there a gate checker?
- Are any VPS/deploy agents needed?
- Are any hosted-auth/token agents needed?
- Which agent owns final evidence?
- Which agent is allowed to say the work is done?
- How many sessions does Parker need to create manually?

## Why

Right now Parker has to infer the agent topology from the work. That creates drift when several agents are working in parallel and a packet gets pasted to the wrong session.

The plan itself should say which sessions need to exist and what each session is allowed to do.

## Product Shape

This probably becomes a skill, something like `planning-protocol`.

The skill would activate when an agent is asked to write a plan, PRD, gate matrix, recovery packet, or implementation proposal.

It should add a short section like:

```text
Agents Needed

- <topic>--cc--coder: implementation owner
- <topic>--kay--partner: product/security review
- <topic>-security--cody--partner: gate checker, if needed

Parker creates these sessions manually for now.
```

The skill should not auto-create agents yet. For now it only tells Parker what agents are needed.

## Non-Goal

This is not a full agent-orchestration product yet.

The first version is just a planning hygiene rule: every plan names the people or agents required to execute and review it.
