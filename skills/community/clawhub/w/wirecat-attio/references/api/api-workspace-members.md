<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Workspace members

## `attio api workspace-members-get [options]`

- What: Get a workspace member
- Call: `GET /v2/workspace_members/{workspace_member_id}`, effect: read
- Sign-in: oauth2 (user\_management:read)

| Flag | Required | What |
|---|---|---|
| `--workspace-member-id <value>` | yes | workspace\_member\_id |

## `attio api workspace-members-list`

- What: List workspace members
- Call: `GET /v2/workspace_members`, effect: read
- Sign-in: oauth2 (user\_management:read)
