---
name: sharepoint-sites
description: Microsoft SharePoint and OneDrive integration with managed OAuth. Manage sites, lists, libraries, files, folders, permissions, content types, and SharePoint operations via Microsoft Graph API.
---

# SharePoint

![SharePoint](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/sharepoint.svg)

Connect to SharePoint and OneDrive to manage sites, lists, document libraries, files, folders, permissions, content types, and SharePoint operations via Microsoft Graph API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=sharepoint-sites) for hosted connection flows and credentials so you do not need to configure Microsoft SharePoint API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect SharePoint |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect SharePoint |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Microsoft Graph  │
│   (User Chat)   │     │   (OAuth)    │     │  (SharePoint,    │
│                 │     │              │     │   OneDrive)       │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                    │                      │
         │  1. Install Plugin │                      │
         │  2. Pair Device    │                      │
         │  3. Connect SharePoint │                  │
         │                    │  4. OAuth Proxy     │
         │                    │  5. Request Forward  │
         │                    │                     │
         ▼                    ▼                     ▼
   ┌──────────┐        ┌──────────┐         ┌──────────┐
   │   SKILL  │        │ Dashboard│         │ SharePoint│
   │   File   │        │   Auth   │         │   Online  │
   └──────────┘        └──────────┘         └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for SharePoint again."

## Quick Start

```bash
# List all sites accessible to the user
clawlink_call_tool --tool "share_point_list_sites"

# List all lists in a SharePoint site
clawlink_call_tool --tool "share_point_list_all_lists" --params '{"site_id": "YOUR_SITE_ID"}'

# Get current user info
clawlink_call_tool --tool "share_point_get_current_user"
```

## Authentication

All SharePoint tool calls are authenticated automatically by ClawLink using the user's connected Microsoft account via OAuth.

**No OAuth setup is required in chat.** ClawLink manages the OAuth flow and token refresh automatically.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=sharepoint and connect SharePoint via OAuth.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `sharepoint` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration sharepoint
```

**Response:** Returns the live tool catalog for SharePoint.

### Reconnect

If SharePoint tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=sharepoint
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration sharepoint`

## Security & Permissions

- Access is scoped to sites, lists, and files accessible to the connected Microsoft account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete list, delete item, recycle file) are marked as high-impact and must be confirmed.
- Permission operations (break inheritance, add role assignments) permanently alter access control — confirm before proceeding.
- Role definition IDs are scoped per site/web — always resolve current values via `share_point_get_role_definitions` rather than hard-coding.

## Tool Reference

### Site Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_sites` | Retrieve all SharePoint sites accessible to the user | Read |
| `share_point_get_site_collection_info` | Fetch site collection metadata (URL, ID, root web URI) — not item-level details | Read |
| `share_point_get_web_info` | Retrieve current SharePoint web metadata (title, URL, language, template) | Read |
| `share_point_get_current_user` | Retrieve the current user for the site (confirms authentication) | Read |

### List Operations

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_all_lists` | Retrieve all lists and document libraries in the current SharePoint web | Read |
| `share_point_get_list_by_title` | Fetch list metadata by title | Read |
| `share_point_get_list_by_guid` | Fetch list metadata by its unique identifier (prefer GUID over title) | Read |
| `share_point_get_list_items` | Retrieve items from a SharePoint list with optional OData parameters | Read |
| `share_point_get_list_items_by_guid` | Retrieve items from a SharePoint list using its GUID | Read |
| `share_point_list_list_columns` | List all column definitions in a SharePoint list (names, types, properties) | Read |
| `share_point_render_list_data_as_stream` | Retrieve list items with rich metadata and formatting via CAML queries | Read |
| `share_point_get_changes` | Retrieve changes from the SharePoint list change log (for webhook processing) | Read |

### List Item Management

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_list_item_by_id` | Fetch a specific list item by ID | Read |
| `share_point_get_list_item_version` | Access historical versions of a list item | Read |
| `share_point_sharepoint_create_list_item` | Create a new item in a SharePoint list (returns item_id and timestamps) | Write |
| `share_point_create_list_item_by_id` | Create a new item in a list using the list's GUID | Write |
| `share_point_create_list_item_in_folder` | Create a list item in a specific folder within a SharePoint list | Write |
| `share_point_update_list_item` | Update fields on an existing list item with ETag concurrency control | Write |
| `share_point_delete_list_item` | Permanently delete a list item by its ID | Write |
| `share_point_recycle_list_item` | Move a list item to the Recycle Bin (soft-delete, restorable) | Write |
| `share_point_restore_recycle_bin_item` | Restore a deleted item by its GUID | Write |

### List Management

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_sharepoint_create_list` | Create a new list in SharePoint (custom columns require separate calls) | Write |
| `share_point_update_list` | Update list metadata (title, description, versioning settings) | Write |
| `share_point_delete_list` | Permanently delete a SharePoint list by its GUID | Write |
| `share_point_delete_list_by_title` | Permanently delete a SharePoint list by title | Write |

### Document Libraries & Files

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_drive_children` | List children (files and folders) in a drive root or folder | Read |
| `share_point_list_files_in_folder` | Enumerate all files in a folder by server-relative URL (non-recursive) | Read |
| `share_point_list_drives_rest_api` | Retrieve document libraries and drives from a SharePoint site | Read |
| `share_point_get_site_drive_item_by_path` | Get metadata for a file or folder by its server-relative path | Read |
| `share_point_download_file_by_server_relative_url` | Fetch raw bytes of a SharePoint file by its server-relative path | Read |
| `share_point_list_drive_recent_items` | List recently modified items in a SharePoint drive | Read |

### File Operations

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_sharepoint_check_out_file` | Check out a file in a document library to lock it for editing | Write |
| `share_point_check_in_file` | Check in a file to finalize changes and release the lock | Write |
| `share_point_undo_checkout_file` | Undo a file checkout, discarding any changes made while checked out | Write |
| `share_point_upload_file` | Upload a file to a SharePoint document library or folder | Write |
| `share_point_upload_from_url` | Fetch a file from a URL and upload it to SharePoint (with conflict behavior) | Write |
| `share_point_update_drive_item` | Update properties of a drive item (rename file/folder) | Write |
| `share_point_recycle_file` | Move a file to the Recycle Bin | Write |
| `share_point_restore_drive_item_version` | Revert a file to an earlier version | Write |
| `share_point_delete_drive_item_version_content` | Delete binary content of a specific version of a drive item | Write |

### Folder Operations

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_subfolders_in_folder` | List immediate child folders within a SharePoint folder | Read |
| `share_point_get_all_folders` | Retrieve all folders across the SharePoint site | Read |
| `share_point_sharepoint_create_folder` | Create a new folder in SharePoint (returns server_relative_url) | Write |
| `share_point_delete_folder` | Delete a folder from a document library (moves to Recycle Bin) | Write |
| `share_point_rename_folder` | Rename a folder by updating its list item metadata | Write |

### Permissions & Roles

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_role_definitions` | List role definitions at the web level (IDs are scoped per site — resolve dynamically) | Read |
| `share_point_break_role_inheritance_on_list` | Break permission inheritance on a SharePoint list (must precede add_role_assignment_to_list) | Write |
| `share_point_break_role_inheritance_on_item` | Break permission inheritance on a list item | Write |
| `share_point_add_role_assignment_to_list` | Grant permissions to a user or group on a SharePoint list | Write |
| `share_point_add_role_assignment_to_item` | Grant permissions to a user or group on a list item | Write |
| `share_point_ensure_user` | Ensure a user exists in a SharePoint site by login name (returns Id for permissions) | Write |
| `share_point_get_user_effective_permissions_on_web` | Get a user's effective permissions on the current site | Read |

### Content Types

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_content_types` | Retrieve all content types from the current SharePoint site | Read |
| `share_point_get_content_type` | Retrieve a specific content type by its ID | Read |
| `share_point_get_content_types_for_list` | Retrieve all content types for a specific SharePoint list by GUID | Read |
| `share_point_get_list_content_type_by_id` | Retrieve a specific content type from a list by ID | Read |
| `share_point_add_field_link_to_content_type` | Associate an existing list field with a content type | Write |
| `share_point_create_content_type` | Create a new content type in SharePoint | Write |
| `share_point_update_content_type` | Update a content type's properties (name, description, group, hidden status) | Write |

### List Fields (Columns)

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_create_list_field` | Create a new field (column) in a SharePoint list | Write |

### Attachments

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_item_attachments` | List all attachments for a SharePoint list item | Read |
| `share_point_get_item_attachment_content` | Download the binary contents of a specific attachment | Read |
| `share_point_add_attachment_to_list_item` | Upload a binary file as an attachment to a list item | Write |

### Sharing & Links

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_create_drive_item_sharing_link` | Create a sharing link for a drive item with specific permissions (view/edit/embed) and scope | Write |

### Users & Groups

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_site_users` | List users in the site collection | Read |
| `share_point_list_site_groups` | List SharePoint site groups for a site collection | Read |
| `share_point_get_group_users` | Retrieve all users who are members of a specified SharePoint group | Read |
| `share_point_get_group_users_by_id` | Retrieve all users in a specific SharePoint site group by group ID | Read |
| `share_point_sharepoint_find_user` | Search for a user by email address in the SharePoint site | Read |
| `share_point_sharepoint_remove_user` | Remove a user from SharePoint (idempotent — returns success even if not a member) | Write |

### Following & Social

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_my_followed` | Get entities the current user is following | Read |
| `share_point_get_my_followers` | Get the list of users who are following the authenticated user | Read |
| `share_point_is_followed` | Check if the current user is following a specified actor | Read |
| `share_point_follow` | Follow a SharePoint user, document, site, or tag | Write |

### Search

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_search_query` | Search SharePoint content using Keyword Query Language (KQL) | Read |
| `share_point_search_suggest` | Get search query suggestions for autocomplete | Read |

### Site Pages

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_site_page_content` | Retrieve modern SharePoint Site Pages content (CanvasContent1, LayoutWebpartsContent) | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_webhook_subscription` | Retrieve a specific webhook subscription by ID | Read |
| `share_point_get_webhook_subscriptions` | Retrieve all webhook subscriptions on a SharePoint list | Read |

### Recycle Bin

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_list_recycle_bin_items` | List items in the SharePoint Recycle Bin | Read |
| `share_point_delete_recycle_bin_item_permanent` | Permanently delete a Recycle Bin item by its GUID | Write |

### Site Management

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_create_web` | Create a new SharePoint subsite under the current site | Write |
| `share_point_update_site` | Update properties of the current SharePoint site (web) | Write |

### Context & Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `share_point_get_context_info` | Retrieve SharePoint context information including form digest value | Read |
| `share_point_get_drive_item_analytics` | Get access statistics (view counts, unique viewers) for files or folders | Read |
| `share_point_log_event` | Log custom usage analytics events for tracking user activities | Write |

## Code Examples

### List all sites

```bash
clawlink_call_tool --tool "share_point_list_sites"
```

### Get a list by title and its items

```bash
clawlink_call_tool --tool "share_point_get_list_by_title" \
  --params '{"title": "Project Tasks"}'

clawlink_call_tool --tool "share_point_get_list_items" \
  --params '{"list_name": "Project Tasks"}'
```

### Create a new list item

```bash
clawlink_call_tool --tool "share_point_sharepoint_create_list_item" \
  --params '{
    "list_name": "Project Tasks",
    "item": {
      "Title": "Complete Q4 Report",
      "Priority": "High",
      "DueDate": "2024-12-31"
    }
  }'
```

### Upload a file

```bash
clawlink_call_tool --tool "share_point_upload_file" \
  --params '{
    "file_name": "report.xlsx",
    "folder_url": "/Shared Documents/Reports",
    "file_content": "BASE64_ENCODED_CONTENT"
  }'
```

### Create a sharing link

```bash
clawlink_call_tool --tool "share_point_create_drive_item_sharing_link" \
  --params '{
    "item_id": "YOUR_FILE_ID",
    "link_type": "view",
    "scope": "organization"
  }'
```

### Break inheritance and add permissions

```bash
clawlink_call_tool --tool "share_point_break_role_inheritance_on_list" \
  --params '{"list_id": "YOUR_LIST_ID", "copy_role_assignments": true}'

clawlink_call_tool --tool "share_point_ensure_user" \
  --params '{"login_name": "i:0#.f|membership|user@domain.com"}'

clawlink_call_tool --tool "share_point_add_role_assignment_to_list" \
  --params '{"list_id": "YOUR_LIST_ID", "principal_id": "USER_ID_FROM_ENSURE_USER", "role_definition_id": 1}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm SharePoint is connected.
2. Call `clawlink_list_tools --integration sharepoint` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `sharepoint`.
5. If no SharePoint tools appear, direct the user to https://claw-link.dev/dashboard?add=sharepoint.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List sites → List lists → Get items → Show results │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Server-relative URLs for folders use the format `/Shared Documents/FolderName` or `/Lists/ListName`.
- List GUIDs are preferred over titles for reliable lookups — names may collide across similarly named lists.
- Role definition IDs are scoped per site/web — never hard-code them; always resolve via `share_point_get_role_definitions`.
- Permission operations require breaking inheritance first (`break_role_inheritance_on_list`) before adding unique role assignments.
- `ensure_user` is a write operation with provisioning side effects — it registers the user in the site collection but does not grant permissions.
- SharePoint search results are security-trimmed — inaccessible content never appears even if it exists.
- `upload_from_url` with `conflict_behavior: 'rename'` bypasses file locks on existing files.
- Custom columns cannot be added at list creation time — use `create_list_field` after creating the list.
- Site pages (`get_site_page_content`) read structured content from modern pages — `.aspx` files may need different handling.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration sharepoint`. |
| Missing connection | SharePoint is not connected. Direct the user to https://claw-link.dev/dashboard?add=sharepoint. |
| `ItemNotFound` | The file, list, or site does not exist. Check the ID or path. |
| `accessDenied` | The connected account lacks permissions to access this site, list, or item. |
| `invalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `resourceModified` | The item has been modified (ETag mismatch). Re-fetch and retry with updated ETag. |
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

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `sharepoint`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.
4. Verify site_id/list_id exist before using them — use `list_sites` and `list_all_lists` to discover IDs.

## Resources

- [Microsoft Graph SharePoint API](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint)
- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-in/set-up-a-sharepoint-add-in-development-environment)
- [SharePoint Permissions](https://learn.microsoft.com/en-us/sharepoint/how-to-set-up-and-configure-sharepoint-add-ins)
- [Working with Lists and List Items](https://learn.microsoft.com/en-us/graph/api/resources/list)
- [Sharing and Permissions in SharePoint](https://learn.microsoft.com/en-us/graph/api/resources/permission)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=sharepoint-sites
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Microsoft OneDrive](https://clawhub.ai/hith3sh/onedrive-files) — For OneDrive file management
- [Microsoft Excel](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) — For Excel workbook operations in SharePoint/OneDrive
- [Microsoft Teams](https://clawhub.ai/hith3sh/microsoft-teams) — For Teams collaboration and channel management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=sharepoint-sites)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)