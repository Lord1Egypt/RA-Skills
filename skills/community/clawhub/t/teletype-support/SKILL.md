---
name: teletype-support
description: "Support workflows for the Teletype MCP server: triage the unanswered inbox, draft and send replies safely, summarize clients, escalate issues, and prepare shift handovers. Use when the task mentions Teletype conversations, the support queue, operator work, or client follow-up."
---

# Teletype support workflows

Regulations for working with a Teletype support project through its MCP tools. Each tool's parameters live in its own schema. This skill covers the order of steps and the safety rules.

## Before any work

If Teletype tools are absent, read [connection instructions](references/installation.md) and help the user configure the MCP server. Installing this skill alone does not connect a project. Never request the project token in chat.

1. If the tool list looks unexpected or a call fails with a policy error, call `get_capabilities` once. It reports the project identity, read-only mode, and active toolsets.
2. Read tools (`find_conversations`, `find_messages`, `list_clients`, `lookup_client_profile`, `read_conversation_thread`, `read_client_history`, `list_workspace_metadata`, `get_project_status`) are safe to call whenever the task needs them. For old message text, continue `find_messages` through pages while `has_more` is true.
3. Write tools require both `confirm: true` in the arguments and the user's explicit approval. "Send it" approves one specific message, not a batch.
4. If the user gives a `dialog_id`, `message_id`, or `channel_id`, pass it to the relevant tool directly. Do not search that ID as message text, client name, or last-message text.

## Safety rules

- Never send, close, or edit without the user asking for it. Draft first.
- For `send_reply_to_client` and `send_whatsapp_template`: when the target is ambiguous (new conversation, client+channel instead of `recipient_dialog_id`), run `dry_run: true` first and show the resolved target. Send with `confirm: true` only after approval.
- For a phone lookup, call `list_clients(phone=...)`. `create_dialog_by_phone` changes data: it can create a dialog or assign the project owner to an existing open dialog. Preview with `dry_run: true` and require approval before `confirm: true`.
- To close a conversation with a category, first call `list_workspace_metadata(resource: "categories")` and use the exact name. Never invent or translate a category. Closing without a category needs no lookup.
- After any write, report from `structuredContent`: distinguish `accepted` from `delivery_confirmed`, and check `partial_errors` for `annotate_client_record` and `resolve_conversation`. If a write timed out or was cancelled, check the conversation state before retrying.
- In drafts and summaries, separate confirmed facts from proposed next steps. Do not promise a courier call, a changed delivery window, a refund, or a deadline unless the conversation or another verified source confirms it. If the needed fact is absent, say you will check it.
- In read-only mode every write is unregistered and `mark_seen` is declined. Say so instead of retrying.

## Presentation rules

- Show every conversation and message as a clickable Markdown link (`link_to_dialog`, `link_to_message`).
- Answer in the user's language. Customer data and API error details stay in their original language.

## Workflow: triage the inbox

1. Run `find_conversations(status: "unanswered", limit: 10)`. Add `channel` if asked.
2. For each conversation, study the client's last message and the wait time.
3. Classify urgency: 🔴 Critical (complaints, payment failures, VIP clients) / 🟡 Standard questions (delivery, consultation) / 🟢 Low priority (information requests).
4. Output a short summary table: link, client, channel, why it is urgent, recommended next action. Send nothing yet.

## Workflow: draft and send a reply

1. `read_conversation_thread(dialog_id or client)` to read recent messages.
2. `lookup_client_profile` when context is missing.
3. Draft a clear, empathetic reply in the language the client uses, and show the draft.
4. After approval: `dry_run: true` if the target was ambiguous, then send with `confirm: true`.
5. Report `accepted`, `delivery_confirmed`, and the message IDs.

## Workflow: client summary

1. `lookup_client_profile(client)`.
2. Summarize the client: name and contact details, tags and custom fields (segment, order number), operator notes, history and status of recent requests. Add a recommended next step.

## Workflow: escalation packet

1. `read_conversation_thread(dialog_id)`.
2. Produce a bug report: the component, the issue as reported by the client, reproduction steps if known, expected and actual behavior, the client environment (browser, OS, screenshots, links), a link to the Teletype conversation.

## Workflow: shift handover

1. `get_project_status(aspect: "all")` for balance, operator availability, API status, and channel issues.
2. `find_conversations(status: "unanswered", limit: 20)` for the queue.
3. Report: project status, available operators, the unanswered queue with links, and risks for the next shift.
