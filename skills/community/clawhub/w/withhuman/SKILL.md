---
name: withhuman
description: What withHuman is and how it works. withHuman is the approval layer for AI agents. It intercepts an agent's tool calls and decides, through rules and human reviewers, which run automatically, which are refused and which wait for a person to approve them. Explains agents, instances, approval requests and decisions, approval pipelines, escalation paths, the review queue, the hosted and self-hosted editions, and how to behave when your own tool call is held, denied or expired. Start here for any withHuman question; it points to the withhuman-cli and withhuman-pipelines skills for setup work. Trigger keywords - withhuman, withHuman, what is withhuman, human in the loop, human approval for AI agents, agent approval, approval request, call was denied, approval timed out, gated by approval policy, Agent Approval Protocol, AAP.
---

# withHuman

withHuman is the approval layer for AI agents. An organization decides
which of its agents' actions run automatically, which are refused, and
which need a person's approval first. withHuman then enforces that on
every tool call.

It works by **interception**. The agent is not asked to call a special
approval tool and needs no code changes. An adapter speaking the Agent
Approval Protocol (AAP) sits between the agent and its tools, sends each
tool call to withHuman, and lets the call run only once withHuman approves
it.

## What happens to a tool call

1. The agent goes to call a tool: a shell command, a file edit, an MCP
   server's tool such as a refund or a deploy.
2. An **AAP adapter** intercepts it and sends withHuman an **approval
   request** over AAP: the tool, its MCP server (if any), the exact
   arguments, and which agent and instance is asking.
3. The organization's **approval pipelines** run on the request and
   approve it, deny it, or hand it to a person.
4. If a person is needed, an **escalation path** picks the reviewers and
   notifies them (email, Slack, Discord, the phone apps and more), raising
   it to others if nobody answers.
5. A reviewer approves or denies it in the **review queue**. The agent
   waits meanwhile.
6. The AAP adapter returns the **decision** to the agent. Approved calls
   run; anything else does not.

Example: a support agent may refund up to $20 automatically, refunds up to
$500 go to the support team, and anything larger is refused.

## The Agent Approval Protocol (AAP)

AAP is the open protocol between an adapter (the client) and an approval
provider, and withHuman is one such provider. The protocol carries
approval requests and decisions, and specifies the flow between the client
and the provider. It never runs a tool or sees its result. A typical
exchange:

1. The adapter gets an instance credential, from `withhuman agent install`
   on a developer machine or from a provisioner token on a server.
2. For each tool call it creates an approval request describing the tool,
   its server and arguments, and how long it may wait. The adapter can also
   send context and the agent's own reasoning.
3. It waits for the request to reach `approved`, `denied`, `expired` or
   `cancelled` in the provider. If the request is approved, the tool call
   is run, otherwise it is not.

The `withhuman` CLI installs ready-made AAP adapters. An agent built in
house can speak AAP directly: create an instance in the app with
**Generate an API key**, then send requests to `<origin>/api/aap` (hosted:
`https://app.withhuman.ai/api/aap`) with that key as a bearer token. For
an agent that should stop while it waits and resume when a decision is
made, choose **Pause runs while waiting** instead: configure the agent's
webhook receiver with the registration ID and signing secret the app
shows once, then enter the receiver's URL and choose **Verify receiver**.
Specification: <https://agentapprovalprotocol.io>; withHuman's reference:
<https://withhuman.ai/docs/reference/agent-approval-protocol.md>.

## Concepts

| Term | Meaning |
| --- | --- |
| Organization | One company's withHuman: its members, teams, agents and rules. |
| Agent | A kind of agent the organization runs, such as `support-agent` or `devin`, identified by a permanent slug. A **service** agent belongs to the organization, like a support bot. A **personal** agent belongs to a single person and acts on their behalf, like Chris's coding agents (`chris-coding-agents`). |
| Instance | One running copy of an agent on one machine or server, with its own credential. `support-agent` might run as `support-worker-01`; Codex on Chris's laptop might be `chris-mbp-codex`, an instance of `chris-coding-agents`. |
| Adapter | An integration that lets an agent harness speak AAP. It plugs into the harness (as a hook or plugin) rather than being built into the agent, and intercepts the harness's tool calls. withHuman builds adapters for the major harnesses (Claude Code, Codex, OpenClaw, Pi, Hermes and DeepSeek), which the `withhuman` CLI installs. |
| Approval request | One intercepted tool call waiting for a decision. |
| Approval pipeline | Ordered rules (blocks) that approve, deny or send a request to a person. Every request runs the `entry` pipeline, which can hand some requests to pipelines other teams own. |
| Escalation path | Defines which specific people can review a request and what order they are contacted in. |
| Review queue | Where reviewers see requests waiting for them, with the tool, arguments and why review was needed. |
| Decision | `approved`, `denied`, `expired` (nobody decided in time) or `cancelled` (the agent withdrew it). An approval only lets the call start shortly afterwards. |
| Tool Catalogue | The tools and argument schemas each agent reported, used to write rules. |
| withHuman MCP server | Lets an agent manage the organization's rules, escalation paths, teams, agents and webhook endpoints on a person's behalf (hosted withHuman adds MCP Gateway servers and the audit log). Usually added as `withhuman`. |
| MCP Gateway | Hosted only. Holds the organization's MCP servers and credentials and gives each agent the tools it was granted. The CLI adds it as `withhuman-gateway`; its tools reach external services and cannot change withHuman's rules. |

User guide: <https://withhuman.ai/docs/concepts/how-withhuman-works.md>.

## Editions

- **Hosted** at <https://app.withhuman.ai>. Sign up there; guided setup at
  `/welcome` connects the first agent.
- **Open edition**, self-hosted from <https://github.com/withHumanAI/withHuman>:
  one `withhuman` server binary with everything embedded. It is a different
  program from the `withhuman` CLI that connects agents, despite the name.

The hosted edition adds features the open edition does not have, among
them: the MCP Gateway (central MCP servers and credentials with per-agent
tool access), AI judge blocks, the audit log and
request timeline, text message, WhatsApp and phone app notifications,
enterprise SSO and directory sync, and organization API keys. When a
feature is missing, check which edition the person uses before assuming
it is broken.

## When your own tool call is gated

If you are an agent connected to withHuman, some of your tool calls will
pause, be refused, or time out. That is the organization's policy working.

- **Waiting.** The call is held until someone decides. Don't cancel and
  retry it; tell the user it is waiting for approval if they are around.
- **Denied.** Read the reviewer's note. If it asks for a change, make
  exactly that change and send the same call again; it goes back for a
  fresh review. Otherwise, tell the user and ask how to continue. Never
  get around a denial another way: a different tool, a script, a
  rephrased command or smaller pieces.
- **Expired.** Nobody answered in time. It is not a denial, but don't retry
  on your own: tell the user so they can ask again or chase a reviewer.
- **Already attempted.** Each approval runs its call once. If the adapter
  says the approved call was already attempted, request approval again
  only if the call still needs to happen.
- **Cancelled, or withHuman unreachable.** The call did not run. Treat it
  as not approved and tell the user. The adapter fails closed on purpose.
- **Credential refused.** Every call is denied until someone acts: the
  agent was archived or disabled, or this machine's credential revoked.
  Stop retrying, tell the user, and pass on the reason's advice: ask
  whoever manages the agent, reconnect, or remove the adapter.
- **Help reviewers.** They decide from the tool and its arguments. Make
  each call do one clear thing with readable arguments, and say beforehand
  what you are about to do and why.
- **Never disable the adapter** or edit its hook settings to get unblocked,
  unless the user explicitly asks you to change their withHuman setup.

## Which skill to use next

| Task | Skill |
| --- | --- |
| Install the CLI, connect a runtime, check, update or remove it | `withhuman-cli` |
| Decide which calls wait and who approves them | `withhuman-pipelines` |
| Approve or deny a request | Neither: people decide in the app, the phone apps or their notification channels, never through an agent. |

Docs: <https://withhuman.ai/docs.md>.
