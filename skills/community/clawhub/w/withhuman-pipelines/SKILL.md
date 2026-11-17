---
name: withhuman-pipelines
description: Decide which AI agent tool calls need human approval in withHuman, and who approves them, by writing approval pipelines and escalation paths through the withHuman MCP server. Covers connecting the MCP server, reading the current rules and the agents' tool catalogue, drafting branch, outcome, delegate and webhook blocks, conditions on tools and arguments, escalation paths with teams, levels and working hours, team escalation policies, webhook endpoints, previewing sample requests, activating and rolling back revisions. Trigger keywords - withhuman, approval pipeline, approval rules, gate tool calls, require approval, human review, escalation path, on-call reviewers, who approves, auto-approve, deny tool call, delegate pipeline, preview pipeline, withHuman MCP server.
---

# withHuman approval pipelines

withHuman sends every intercepted agent tool call through the
organization's approval pipelines. The pipeline approves it, denies it, or
hands it to a person on an escalation path. This skill writes those rules
with the withHuman MCP server's tools.

## Connect the MCP server

Read and change rules only through the withHuman MCP server's tools
(`get_pipeline`, `read_reference` and the rest). If they are not available,
stop and tell the person the withHuman MCP server is not connected, with
the command below. Don't fall back to the web app through a browser or
computer use, the REST API, or another MCP server, even just to read,
unless the person asks you to.

Don't confuse it with the **MCP Gateway**. On hosted withHuman,
`withhuman agent install` registers the gateway as `withhuman-gateway`; its
tools reach external services (named like `<server>__<tool>`) and cannot
read or change rules.

The address is the deployment's origin plus `/api/mcp/v1` (hosted:
`https://app.withhuman.ai/api/mcp/v1`). The person runs the command for
their client, then signs in when the browser opens.

Claude Code:

```sh
claude mcp add --transport http withhuman https://app.withhuman.ai/api/mcp/v1
```

Codex:

```sh
codex mcp add withhuman --url https://app.withhuman.ai/api/mcp/v1
```

Other clients add a streamable HTTP server named `withhuman` with that
URL. The consent page decides what you may do, and every change is
recorded in the audit log under that access. Guide:
<https://withhuman.ai/docs/web-app/mcp-server.md>.

The server's own instructions explain the model. Read them, then call
`read_reference` for `pipeline_blocks`, `conditions` and, when you touch
reviewers, `escalation_paths` before writing anything. The grammar is
strict and differs between deployments, so never write blocks from memory.

## How the rules fit

- **The entry pipeline** (key `entry`) runs for every request. Blocks run
  in order; the first to decide `approve`, `deny` or `human` ends it.
- **A new organization's entry pipeline approves every call.** It holds
  one `outcome` block, `approve-every-call`. Put new rules before it, or
  nothing reaches them. A pipeline that runs out of blocks sends the call
  to a person.
- **"If this, then that" is a `branch`** with a condition and its own
  blocks, ending in an `outcome` block. Requests that match are decided
  inside the branch; the rest skip it.
- **Rules for one agent** are a branch on `/agent/slug`. Agents own no
  pipeline of their own.
- **A `delegate` block** hands matching requests to another pipeline
  (`create_pipeline`). Best practice is to make a new pipeline when its
  rules will be complicated in their own right, or when a specific person
  or team should own them (for example, Payments owning every Stripe
  call). Simple rules stay as a branch in the pipeline that matches them.
- **An escalation path** says who reviews and what happens if nobody
  answers. A human exit names one with `escalation_path`, or falls back to
  the pipeline's `default_escalation_path`. `ask_agent_owner` sends the
  request to the person who owns the agent instance instead.
- **A team's escalation policy** orders how a level that targets the team
  pages its members (`update_team_escalation_policy`). Without one, the
  whole team is paged at once.
- **A webhook endpoint** is a service of yours a `webhook` block asks for
  an outcome (`save_webhook_endpoint`). Its signing secret is shown once,
  when the endpoint is created or the secret rotated.
- **Every save is a new revision.** Earlier revisions stay available for
  rollback.

## Workflow

1. **Ask what should happen.** Pin down, in the person's words: which calls
   must wait (tools, arguments, agents), which are always refused, who
   reviews and how fast, and whether everything else runs automatically.
   Ask as many clarifying questions as needed until the flow is clear and
   unambiguous. Don't guess thresholds or reviewers.
   When the person is not sure what should wait, read the agents' tools
   (`list_tool_catalog` with `agent_slug`, or `list_tool_definitions`) and
   suggest the consequential calls, each with a short reason: calls that
   delete or overwrite data, change things outside the machine (git
   pushes, deploys, cloud resources), send messages, or spend money. For
   a tool that can do both safe and risky things, such as the shell,
   suggest conditions on its arguments (for example `git push` or
   `rm -rf`) rather than gating the whole tool. Reading, searching and
   running tests usually run without a person. Let the person confirm or
   change the list before you write anything.
2. **Read what exists.** `list_agents` for slugs, `list_pipelines` and
   `get_pipeline` for `entry` (and any delegated pipeline you will change),
   `list_escalation_paths`, `list_members` and `list_teams` for reviewers,
   and `list_tool_definitions` for the exact tool names and arguments the
   agents use.
3. **Read the reference** topics you need with `read_reference`.
4. **Reviewers first.** Create or update the escalation path
   (`create_escalation_path`, `update_escalation_path`) before a pipeline
   names it. A pipeline cannot be activated while a path it names is
   inactive.
5. **Draft the whole block list.** `update_pipeline` replaces every block,
   so start from the blocks `get_pipeline` returned and change only what
   was asked. Keep blocks you do not understand, including the per-runtime
   branches guided setup created (ids such as `claude-code` or `codex`).
6. **Preview.** Run `preview_pipeline` with the draft blocks and several
   samples: one call that must wait, one that must run, one that must be
   refused, and one for another agent that must be unaffected. Check the
   outcome, the deciding block and the escalation path. Note that webhook
   blocks and model-based kinds really call their service during a preview.
7. **Save.** Show the person the change and the preview results. Save with
   `activate: false` for a draft they activate in the app, or activate at
   once when they asked for that. New requests use the active revision
   immediately.
8. **Roll back** with `list_pipeline_revisions` and
   `activate_pipeline_revision` if something is wrong. Escalation paths,
   team escalation policies and webhook endpoints roll back the same way
   with their own `activate_*_revision` tools.

## Matching tool calls

- `/request/tool` is the tool's own name: the runtime's name for a built-in
  tool (Claude Code uses `Bash`, `Edit`, `Write`), or the name the MCP
  server gives its tool.
- `/request/server` is the MCP server's alias as the runtime configured it.
  Built-in tools have no server. Never match on `mcp__server__tool`
  spellings.
- `/request/arguments/...` reaches any argument, for example
  `/request/arguments/command` for a shell command or
  `/request/arguments/amount` for a refund.
- Exact tool names and argument schemas come from `list_tool_definitions`
  (or `list_tool_catalog` for one agent). A tool nobody has reported yet is
  not there; ask the person to run `withhuman agent refresh-tools` or check
  the agent's **Tool Catalogue** tab, because a condition on a misspelled
  tool silently never matches.

## Pitfalls

- **Condition and escalation node ids are UUIDs you generate**, unique
  within the revision or path. Block ids are key-shaped
  (`^[a-z0-9][a-z0-9._-]{0,62}$`) and unique across the revision,
  including blocks inside branches.
- **Unknown fields are refused.** Copy shapes from `read_reference`, not
  from other products' policy formats.
- **User targets carry a membership id** from `list_members`, never a user
  id or email. Team targets carry a team id from `list_teams`.
- **Keys are permanent.** Pipeline and escalation path keys are never
  reused, even after archiving; choose them with the person.
- **Block kinds differ by deployment.** Hosted withHuman adds kinds such as
  AI judge blocks; `read_reference` lists every kind this deployment
  accepts after the core grammar. Use only those.
- **A refusal explains itself.** Tool errors carry the same reason the app
  shows, such as a path still in use or a permission you were not granted.
  Fix the cause rather than retrying. `list_escalation_path_uses`,
  `list_pipeline_uses`, `list_webhook_endpoint_uses` and
  `get_pipeline_revision_references` explain an archive or activation
  refusal before you try.

## Out of scope

Deciding requests, inviting people and granting roles or permissions are
not available through the MCP server: a person does them in the app. Use
the `withhuman-cli` skill to connect a coding agent; people approve or deny
requests in the app, the phone apps or their notification channels. The
server also manages agents, their instances and credentials, and members'
status; on hosted withHuman it adds MCP Gateway servers and the audit log.
Use those tools only when the person asks for that.

User guides: <https://withhuman.ai/docs/web-app/approval-pipelines.md>,
<https://withhuman.ai/docs/web-app/escalation-paths.md>.
