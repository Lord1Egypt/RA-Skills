---
name: trello-projects
description: Manage Trello boards, lists, cards, comments, labels, checklists, and project workflows via the Trello API. Use this skill when users want to create boards, manage cards, track tasks, or automate Trello project management workflows.
---

# Trello Projects

![Trello Projects](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/trello.svg?v=2)

Manage Trello boards, lists, cards, comments, labels, checklists, members, and project workflows from chat via the Trello API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=trello-projects) for hosted connection flows and credentials so you do not need to configure Trello API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Trello |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Trello |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Trello API     │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Trello   │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Trello │
   │  File    │           │ Auth     │           │ Account │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Trello again."

## Quick Start

```bash
# List boards
clawlink_call_tool --tool "trello_get_boards" --params '{}'

# Get a board with lists and cards
clawlink_call_tool --tool "trello_get_board" --params '{"board_id": "BOARD_ID"}'

# Create a card
clawlink_call_tool --tool "trello_add_card" --params '{"id_list": "LIST_ID", "name": "New task"}'
```

## Authentication

All Trello tool calls are authenticated automatically by ClawLink using the user's connected Trello account OAuth token.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Trello API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=trello and connect Trello.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `trello` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration trello
```

**Response:** Returns the live tool catalog for Trello.

### Reconnect

If Trello tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=trello
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration trello`

## Security & Permissions

- Access is scoped to the Trello account connected during OAuth setup and the workspaces/boards accessible to that account.
- **All write operations require explicit user confirmation.** Board deletion, card deletion, and list archiving are high-impact.
- Confirm before bulk operations, member removals, or board deletions.
- Board visibility and workspace permissions affect what operations are available.

## Tool Reference

### Boards

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_boards` | List all boards the member is associated with | Read |
| `trello_get_board` | Get board details including lists, cards, and members | Read |
| `trello_add_board` | Create a new board | Write |
| `trello_update_board` | Update board name, description, or preferences | Write |
| `trello_delete_board` | Permanently delete a board and all its contents | Write |
| `trello_close_board` | Archive a board | Write |
| `trello_get_board_actions` | Get recent actions on a board | Read |
| `trello_get_board_labels` | List labels on a board | Read |
| `trello_create_board_label` | Create a new label on a board | Write |
| `trello_update_board_label` | Update a label's name or color | Write |
| `trello_delete_board_label` | Delete a label from a board | Write |

### Lists

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_lists` | List all lists on a board | Read |
| `trello_add_list` | Create a new list on a board | Write |
| `trello_update_list` | Update a list's name or position | Write |
| `trello_archive_list` | Archive a list and all its cards | Write |
| `trello_move_list` | Move a list to a different position | Write |
| `trello_archive_all_list_cards` | Archive all cards in a list | Write |

### Cards

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_cards` | List all cards on a board | Read |
| `trello_get_card` | Get card details including description, members, and checklists | Read |
| `trello_add_card` | Create a new card in a list | Write |
| `trello_update_card` | Update a card's name, description, or position | Write |
| `trello_move_card` | Move a card to a different list or position | Write |
| `trello_delete_card` | Permanently delete an archived card | Write |
| `trello_archive_card` | Archive a card | Write |
| `trello_close_card` | Archive and close a card | Write |

### Card Members & Labels

| Tool | Description | Mode |
|------|-------------|------|
| `trello_add_member_to_card` | Assign a member to a card | Write |
| `trello_remove_member_from_card` | Remove a member from a card | Write |
| `trello_add_label_to_card` | Add a label to a card | Write |
| `trello_remove_label_from_card` | Remove a label from a card | Write |
| `trello_create_card_label` | Create and add a new label to a card | Write |

### Comments & Activity

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_card_comments` | List all comments on a card | Read |
| `trello_add_comment` | Add a text comment with optional @mentions | Write |
| `trello_delete_comment` | Delete a specific comment from a card | Write |
| `trello_get_card_actions` | Get all actions on a card | Read |
| `trello_add_reaction_to_action` | Add an emoji reaction to an action | Write |
| `trello_delete_reaction_from_action` | Remove a reaction from an action | Write |

### Checklists

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_card_checklists` | List all checklists on a card | Read |
| `trello_add_checklist` | Add a checklist to a card | Write |
| `trello_add_checklist_item` | Add an item to an existing checklist | Write |
| `trello_toggle_checklist_item` | Toggle a checklist item's completion state | Write |
| `trello_delete_checklist` | Delete a checklist from a card | Write |
| `trello_delete_checklist_item` | Remove an item from a checklist | Write |
| `trello_convert_checklist_item_to_card` | Convert a checklist item to a new card | Write |

### Attachments

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_card_attachments` | List all attachments on a card | Read |
| `trello_add_attachment` | Add a file attachment or URL to a card | Write |
| `trello_delete_attachment` | Remove an attachment from a card | Write |

### Members

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_board_members` | List members on a board | Read |
| `trello_add_member_to_board` | Invite a member to a board | Write |
| `trello_remove_member_from_board` | Remove a member from a board | Write |
| `trello_get_member` | Get a member's profile | Read |

### Organizations (Workspaces)

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_organizations` | List organizations the member belongs to | Read |
| `trello_get_organization` | Get an organization's details | Read |
| `trello_create_organization` | Create a new organization/workspace | Write |
| `trello_update_organization` | Update an organization's settings | Write |
| `trello_delete_organization` | Delete an organization | Write |

### Power-Ups

| Tool | Description | Mode |
|------|-------------|------|
| `trello_get_board_power_ups` | List enabled Power-Ups on a board | Read |
| `trello_enable_board_power_up` | Enable a Power-Up on a board | Write |
| `trello_disable_board_power_up` | Disable a Power-Up on a board | Write |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `trello_create_webhook` | Create a webhook for board/card changes | Write |
| `trello_list_webhooks` | List all webhooks for the account | Read |
| `trello_delete_webhook` | Delete a webhook | Write |

## Code Examples

### Get a board with all lists and cards

```bash
clawlink_call_tool --tool "trello_get_board" \
  --params '{
    "board_id": "BOARD_ID"
  }'
```

### Create a new card

```bash
clawlink_call_tool --tool "trello_add_card" \
  --params '{
    "id_list": "LIST_ID",
    "name": "Review Q2 budget proposal",
    "desc": "Please review and approve by Friday.",
    "pos": "bottom"
  }'
```

### Add a checklist to a card

```bash
clawlink_call_tool --tool "trello_add_checklist" \
  --params '{
    "id_card": "CARD_ID",
    "name": "Definition of Done"
  }'
```

### Add a comment with @mention

```bash
clawlink_call_tool --tool "trello_add_comment" \
  --params '{
    "id_card": "CARD_ID",
    "text": "@JaneDoe please review the updated design by EOD."
  }'
```

### Move a card to a different list

```bash
clawlink_call_tool --tool "trello_move_card" \
  --params '{
    "card_id": "CARD_ID",
    "id_list": "TARGET_LIST_ID",
    "pos": "top"
  }'
```

### Create a new board

```bash
clawlink_call_tool --tool "trello_add_board" \
  --params '{
    "name": "Project Alpha",
    "desc": "Tracking deliverables for the alpha release",
    "id_org": "ORGANIZATION_ID",
    "visibility": "org"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Trello is connected.
2. Call `clawlink_list_tools --integration trello` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `trello`.
5. If no Trello tools appear, direct the user to https://claw-link.dev/dashboard?add=trello.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → search                             │
│                                                             │
│  Example: List boards → Get board → Get card → Show details│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Preview card creation → User approves → Create   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, get, and search operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Board, list, and card IDs are required for most operations — resolve them from board/card lookups first.
- Card moves between boards require both `card_id` and `id_board` parameters.
- Checklist items converted to cards cannot be customized during conversion — the card inherits basic properties.
- Archived cards and boards can be restored via the Trello web UI but not via the API.
- Webhooks require a publicly accessible callback URL — they will not work with localhost.
- Label operations on cards require knowing the label ID, which comes from `trello_get_board_labels`.
- Organization (workspace) membership determines which boards are accessible.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration trello`. |
| Missing connection | Trello is not connected. Direct the user to https://claw-link.dev/dashboard?add=trello. |
| `board_not_found` | The board ID does not exist or is not accessible. |
| `list_not_found` | The list ID does not exist on the target board. |
| `card_not_found` | The card ID does not exist or was archived. |
| `member_not_found` | The member ID or username does not match any board member. |
| `invalid_token` | The OAuth token is invalid or expired. Reconnect Trello. |
| `webhook_not_found` | The webhook ID does not exist. |
| `model_not_found` | The target resource (card, board, etc.) was not found. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Card Operations Fail

1. Verify the list ID exists on the target board — use `trello_get_lists` to confirm.
2. Check that the card is not already archived — archived cards cannot be moved, only deleted.
3. Confirm the board's permission settings allow the operation.

## Resources

- [Trello API Documentation](https://developer.atlassian.com/cloud/trello/)
- [Trello REST API Reference](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello Power-Ups](https://trello.com/power-ups)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=trello-projects
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=trello-projects)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)