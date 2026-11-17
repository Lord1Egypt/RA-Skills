---
name: checking-email-deliverability
description: "Diagnoses why Sendly mail is not landing and fixes the sending setup: domain health, DKIM, SPF, and DMARC records, sending-domain verification, suppressions, and address validation or list cleaning. Use when the user asks 'why is mail from my domain not landing', 'why do my emails go to spam', 'why are emails bouncing', 'what DNS records do I need for DKIM', 'verify my sending domain', 'who is suppressed', or 'clean this list before I send'. Changes are confirmed first."
---

# Sendly deliverability check

Find out why mail from a domain is not landing, walk the user through the fix, and check address quality. Changes to domains and suppressions happen only after the user confirms.

## Connecting and calling the tools

Every tool in this skill comes from the `sendly` MCP server, the Sendly connector, and is written here as `sendly:<tool>`.

- **Tools listed by name:** call them directly, for example `sendly:list_contacts`.
- **Only `sendly:search_tools` and `sendly:execute_typescript` listed (Code Mode, the default):** call `sendly:search_tools` first, then call each tool inside `sendly:execute_typescript` as `external_<tool>` (for example `external_list_contacts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `sendly:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Sendly and approves that scope.
- **No `sendly` tools at all:** Sendly is not connected yet. Install the Sendly power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `sendly:check_domain`: the project's sending domains with DKIM, SPF, and DMARC status.
- `sendly:diagnose_delivery`: an explanation of a domain's delivery health from its DNS state plus recent bounces and suppressions.
- `sendly:add_domain`, `sendly:start_domain_setup`, `sendly:verify_domain`: add a sending domain, get the DNS records to publish, and check them.
- `sendly:list_suppressions`, `sendly:add_suppression`, `sendly:remove_suppression`: the addresses mail will not go to, and changes to that list.
- `sendly:validate_emails`, `sendly:get_validation_run`, `sendly:list_validation_results`, `sendly:clean_list`: check addresses before sending. Metered per address on the Sendly plan.

## Workflow

1. Call `sendly:check_domain` and report each domain's DKIM, SPF, and DMARC state.
2. For the domain the user cares about, call `sendly:diagnose_delivery` and summarize the cause it found.
3. If DNS records are missing, say which domain you will set up, get a yes, then call `sendly:start_domain_setup` (or `sendly:add_domain` first for a new domain). List the records to publish, one per line with type, name, and value.
4. After the user says the records are published, call `sendly:verify_domain` and report the result. DNS can take time to propagate; if it fails, name the records still missing.
5. If bounces are the issue, call `sendly:list_suppressions` and show how many addresses are suppressed and why.
6. For a list the user wants to check before sending, state the number of addresses and that validation is metered, get a yes, then call `sendly:validate_emails` or `sendly:clean_list`. Read results with `sendly:get_validation_run` and `sendly:list_validation_results`.

## Rules

- Call `sendly:add_domain`, `sendly:start_domain_setup`, or `sendly:add_suppression` only after the user confirms the exact domain or address.
- Suppressions are the consent record. Call `sendly:remove_suppression` only when the user says the address owner asked to receive mail again, and confirm the exact address first.
- Confirm the address count before any validation or list cleaning, because it is billed per address.
- Do not tell the user a domain is fixed until `sendly:verify_domain` or `sendly:check_domain` says so.
- Do not send email from this skill: never call `sendly:send_email`, `sendly:send_test_email`, `sendly:send_campaign`, or `sendly:send_mailbox_email`.
