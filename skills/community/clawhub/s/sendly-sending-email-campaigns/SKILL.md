---
name: sending-email-campaigns
description: "Picks an audience, drafts a Sendly email campaign, sends a test, and sends the campaign only after the user confirms the recipient count. Use when the user asks to 'draft a September newsletter for premium members', 'write an email announcement', 'prepare a campaign', 'who is in this segment', 'send me a test email', 'send the campaign', or run an email marketing send or email blast."
---

# Draft and send a Sendly campaign

Go from an idea to a campaign in DRAFT, then to a test, then to a send. Sending reaches real inboxes, so it happens only after the user explicitly confirms the audience size.

## Connecting and calling the tools

Every tool in this skill comes from the `sendly` MCP server, the Sendly connector, and is written here as `sendly:<tool>`.

- **Tools listed by name:** call them directly, for example `sendly:list_contacts`.
- **Only `sendly:search_tools` and `sendly:execute_typescript` listed (Code Mode, the default):** call `sendly:search_tools` first, then call each tool inside `sendly:execute_typescript` as `external_<tool>` (for example `external_list_contacts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `sendly:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Sendly and approves that scope.
- **No `sendly` tools at all:** Sendly is not connected yet. Install the Sendly power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `sendly:list_segments`, `sendly:list_segment_contacts`, `sendly:list_lists`, `sendly:list_contacts`: find and size the audience.
- `sendly:list_templates`, `sendly:get_template`: reuse the copy and layout of an existing template.
- `sendly:create_campaign`: save a campaign in DRAFT. Needs `name`, `subject`, `body`, and `from`, even though the schema marks only the first two as required.
- `sendly:update_campaign`: change a draft campaign.
- `sendly:send_test_email`: send a test to the project owner's own verified address. Refuses any other recipient.
- `sendly:send_campaign`: two-step. Without `confirm: true` it returns the audience size and sends nothing. With `confirm: true` it sends to every contact in the audience.
- `sendly:check_domain`: confirm the `from` address is on a verified domain.

## Workflow

1. Settle the audience. Call `sendly:list_segments` or `sendly:list_lists`, then `sendly:list_segment_contacts` or `sendly:list_contacts` to show who is in it and how many.
2. If the user wants to start from a template, call `sendly:list_templates` and `sendly:get_template`.
3. Write the subject and body in the user's voice. Show them and ask for changes once.
4. Call `sendly:check_domain` and make sure the `from` address is on a verified domain. If not, stop and offer the `checking-email-deliverability` skill.
5. Call `sendly:create_campaign` with name, subject, body, from, and audience. Report the campaign id and that it is a DRAFT. Nothing is sent.
6. Offer a test. Call `sendly:send_test_email` only after the user says yes; it goes to their own verified address.
7. When the user asks to send, call `sendly:send_campaign` without `confirm`. Report the audience size it returned, the subject, and the from address.
8. Ask: "Send this to N contacts now?" Only after an explicit yes in this turn, call `sendly:send_campaign` again with `confirm: true`. Report the result.

## Rules

- Never call `sendly:send_campaign` with `confirm: true`, `sendly:send_email`, or `sendly:send_mailbox_email` without an explicit yes to a stated recipient count. An earlier "send it" before the count was shown is not confirmation.
- Never send to addresses that are not already contacts in the project. There is no bulk import or arbitrary-recipient send here, and a purchased list is not consent.
- If `sendly:send_test_email` refuses a recipient, explain that tests go only to the owner's own verified address.
- If the sending tools are missing, the user did not grant the sending scope. Say so; do not look for another way to send.
- Do not fabricate links, prices, or claims in the copy. Ask for them.
