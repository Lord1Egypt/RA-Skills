<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: admin

## `slk api admin apps-approve [options]`

- What: admin\_apps\_approve — write (POST /admin.apps.approve)
- Call: `POST /admin.apps.approve`, effect: write
- Body: `AdminAppsApproveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin apps-approved-list [options]`

- What: admin\_apps\_approved\_list — read (GET /admin.apps.approved.list)
- Call: `GET /admin.apps.approved.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page |
| `--team-id <value>` | no | team\_id |
| `--enterprise-id <value>` | no | enterprise\_id |

## `slk api admin apps-requests-list [options]`

- What: admin\_apps\_requests\_list — read (GET /admin.apps.requests.list)
- Call: `GET /admin.apps.requests.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page |
| `--team-id <value>` | no | team\_id |

## `slk api admin apps-restrict [options]`

- What: admin\_apps\_restrict — write (POST /admin.apps.restrict)
- Call: `POST /admin.apps.restrict`, effect: write
- Body: `AdminAppsRestrictRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin apps-restricted-list [options]`

- What: admin\_apps\_restricted\_list — read (GET /admin.apps.restricted.list)
- Call: `GET /admin.apps.restricted.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page |
| `--team-id <value>` | no | team\_id |
| `--enterprise-id <value>` | no | enterprise\_id |

## `slk api admin conversations-archive [options]`

- What: admin\_conversations\_archive — destructive (POST /admin.conversations.archive)
- Call: `POST /admin.conversations.archive`, effect: destructive
- Permission keys: `slack.delete`
- Body: `AdminConversationsArchiveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-convert-to-private [options]`

- What: admin\_conversations\_convertToPrivate — write (POST…
- Call: `POST /admin.conversations.convertToPrivate`, effect: write
- Body: `AdminConversationsConvertToPrivateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-create [options]`

- What: admin\_conversations\_create — write (POST /admin.conversations.create)
- Call: `POST /admin.conversations.create`, effect: write
- Body: `AdminConversationsCreateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-delete [options]`

- What: admin\_conversations\_delete — destructive (POST /admin.conversations.delete)
- Call: `POST /admin.conversations.delete`, effect: destructive
- Permission keys: `slack.delete`
- Body: `AdminConversationsDeleteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-disconnect-shared [options]`

- What: admin\_conversations\_disconnectShared — write (POST…
- Call: `POST /admin.conversations.disconnectShared`, effect: write
- Body: `AdminConversationsDisconnectSharedRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-ekm-list-original-connected-channel-info [options]`

- What: admin\_conversations\_ekm\_listOriginalConnectedChannelInfo — read (GET…
- Call: `GET /admin.conversations.ekm.listOriginalConnectedChannelInfo`, effect: read

| Flag | Required | What |
|---|---|---|
| `--channel-ids <value>` | no | A comma-separated list of channels to filter to. |
| `--team-ids <value>` | no | A comma-separated list of the workspaces to which the channels you would like returned belong. |
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page. |

## `slk api admin conversations-get-conversation-prefs [options]`

- What: admin\_conversations\_getConversationPrefs — read (GET…
- Call: `GET /admin.conversations.getConversationPrefs`, effect: read

| Flag | Required | What |
|---|---|---|
| `--channel-id <value>` | yes | The channel to get preferences for. |

## `slk api admin conversations-get-teams [options]`

- What: admin\_conversations\_getTeams — read (GET /admin.conversations.getTeams)
- Call: `GET /admin.conversations.getTeams`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `team_ids`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--channel-id <value>` | yes | The channel to determine connected workspaces within the organization for. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page |
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |
| `--all` | no | read every page, as the API pages it |

## `slk api admin conversations-invite [options]`

- What: admin\_conversations\_invite — write (POST /admin.conversations.invite)
- Call: `POST /admin.conversations.invite`, effect: write
- Body: `AdminConversationsInviteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-rename [options]`

- What: admin\_conversations\_rename — write (POST /admin.conversations.rename)
- Call: `POST /admin.conversations.rename`, effect: write
- Body: `AdminConversationsRenameRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-restrict-access-list-groups [options]`

- What: admin\_conversations\_restrictAccess\_listGroups — read (GET…
- Call: `GET /admin.conversations.restrictAccess.listGroups`, effect: read

| Flag | Required | What |
|---|---|---|
| `--channel-id <value>` | yes | channel\_id |
| `--team-id <value>` | no | The workspace where the channel exists. This argument is required for channels only tied to one workspace, and optional for channels that are shared across an organization. |

## `slk api admin conversations-search [options]`

- What: admin\_conversations\_search — read (GET /admin.conversations.search)
- Call: `GET /admin.conversations.search`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `next_cursor`; items in `channels`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--team-ids <value>` | no | Comma separated string of team IDs, signifying the workspaces to search through. |
| `--query <value>` | no | Name of the the channel to query by. |
| `--limit <value>` | no | Maximum number of items to be returned. Must be between 1 - 20 both inclusive. Default is 10. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page. |
| `--search-channel-types <value>` | no | The type of channel to include or exclude in the search. For example \`private\` will search private channels, while \`private\_exclude\` will exclude them. For a full list of types, check the Types section. |
| `--sort <value>` | no | Possible values are \`relevant\` (search ranking based on what we think is closest), \`name\` (alphabetical), \`member\_count\` (number of users in the channel), and \`created\` (date channel was created). You can optionally pair this with the \`sort\_dir\` arg to change how it is sorted |
| `--sort-dir <value>` | no | Sort direction. Possible values are \`asc\` for ascending order like (1, 2, 3) or (a, b, c), and \`desc\` for descending order like (3, 2, 1) or (c, b, a) |
| `--all` | no | read every page, as the API pages it |

## `slk api admin conversations-set-conversation-prefs [options]`

- What: admin\_conversations\_setConversationPrefs — write (POST…
- Call: `POST /admin.conversations.setConversationPrefs`, effect: write
- Body: `AdminConversationsSetConversationPrefsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-set-teams [options]`

- What: admin\_conversations\_setTeams — write (POST /admin.conversations.setTeams)
- Call: `POST /admin.conversations.setTeams`, effect: write
- Body: `AdminConversationsSetTeamsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin conversations-unarchive [options]`

- What: admin\_conversations\_unarchive — write (POST /admin.conversations.unarchive)
- Call: `POST /admin.conversations.unarchive`, effect: write
- Body: `AdminConversationsUnarchiveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin emoji-list [options]`

- What: admin\_emoji\_list — read (GET /admin.emoji.list)
- Call: `GET /admin.emoji.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page |
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |

## `slk api admin invite-requests-approve [options]`

- What: admin\_inviteRequests\_approve — write (POST /admin.inviteRequests.approve)
- Call: `POST /admin.inviteRequests.approve`, effect: write
- Body: `AdminInviteRequestsApproveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin invite-requests-approved-list [options]`

- What: admin\_inviteRequests\_approved\_list — read (GET…
- Call: `GET /admin.inviteRequests.approved.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | ID for the workspace where the invite requests were made. |
| `--cursor <value>` | no | Value of the \`next\_cursor\` field sent as part of the previous API response |
| `--limit <value>` | no | The number of results that will be returned by the API on each invocation. Must be between 1 - 1000, both inclusive |

## `slk api admin invite-requests-denied-list [options]`

- What: admin\_inviteRequests\_denied\_list — read (GET /admin.inviteRequests.denied.list)
- Call: `GET /admin.inviteRequests.denied.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | ID for the workspace where the invite requests were made. |
| `--cursor <value>` | no | Value of the \`next\_cursor\` field sent as part of the previous api response |
| `--limit <value>` | no | The number of results that will be returned by the API on each invocation. Must be between 1 - 1000 both inclusive |

## `slk api admin invite-requests-deny [options]`

- What: admin\_inviteRequests\_deny — write (POST /admin.inviteRequests.deny)
- Call: `POST /admin.inviteRequests.deny`, effect: write
- Body: `AdminInviteRequestsDenyRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin invite-requests-list [options]`

- What: admin\_inviteRequests\_list — read (GET /admin.inviteRequests.list)
- Call: `GET /admin.inviteRequests.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | ID for the workspace where the invite requests were made. |
| `--cursor <value>` | no | Value of the \`next\_cursor\` field sent as part of the previous API response |
| `--limit <value>` | no | The number of results that will be returned by the API on each invocation. Must be between 1 - 1000, both inclusive |

## `slk api admin teams-admins-list [options]`

- What: admin\_teams\_admins\_list — read (GET /admin.teams.admins.list)
- Call: `GET /admin.teams.admins.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | The maximum number of items to return. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page. |
| `--team-id <value>` | yes | team\_id |

## `slk api admin teams-create [options]`

- What: admin\_teams\_create — write (POST /admin.teams.create)
- Call: `POST /admin.teams.create`, effect: write
- Body: `AdminTeamsCreateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin teams-list [options]`

- What: admin\_teams\_list — read (GET /admin.teams.list)
- Call: `GET /admin.teams.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 100 both inclusive. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page. |

## `slk api admin teams-owners-list [options]`

- What: admin\_teams\_owners\_list — read (GET /admin.teams.owners.list)
- Call: `GET /admin.teams.owners.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | yes | team\_id |
| `--limit <value>` | no | The maximum number of items to return. Must be between 1 - 1000 both inclusive. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page. |

## `slk api admin teams-settings-info [options]`

- What: admin\_teams\_settings\_info — read (GET /admin.teams.settings.info)
- Call: `GET /admin.teams.settings.info`, effect: read

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | yes | team\_id |

## `slk api admin teams-settings-set-description [options]`

- What: admin\_teams\_settings\_setDescription — write (POST…
- Call: `POST /admin.teams.settings.setDescription`, effect: write
- Body: `AdminTeamsSettingsSetDescriptionRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin teams-settings-set-discoverability [options]`

- What: admin\_teams\_settings\_setDiscoverability — write (POST…
- Call: `POST /admin.teams.settings.setDiscoverability`, effect: write
- Body: `AdminTeamsSettingsSetDiscoverabilityRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin teams-settings-set-name [options]`

- What: admin\_teams\_settings\_setName — write (POST /admin.teams.settings.setName)
- Call: `POST /admin.teams.settings.setName`, effect: write
- Body: `AdminTeamsSettingsSetNameRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin usergroups-add-channels [options]`

- What: admin\_usergroups\_addChannels — write (POST /admin.usergroups.addChannels)
- Call: `POST /admin.usergroups.addChannels`, effect: write
- Body: `AdminUsergroupsAddChannelsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin usergroups-add-teams [options]`

- What: admin\_usergroups\_addTeams — write (POST /admin.usergroups.addTeams)
- Call: `POST /admin.usergroups.addTeams`, effect: write
- Body: `AdminUsergroupsAddTeamsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin usergroups-list-channels [options]`

- What: admin\_usergroups\_listChannels — read (GET /admin.usergroups.listChannels)
- Call: `GET /admin.usergroups.listChannels`, effect: read

| Flag | Required | What |
|---|---|---|
| `--usergroup-id <value>` | yes | ID of the IDP group to list default channels for. |
| `--team-id <value>` | no | ID of the the workspace. |
| `--include-num-members <value>` | no | Flag to include or exclude the count of members per channel. |

## `slk api admin usergroups-remove-channels [options]`

- What: admin\_usergroups\_removeChannels — destructive (POST…
- Call: `POST /admin.usergroups.removeChannels`, effect: destructive
- Permission keys: `slack.delete`
- Body: `AdminUsergroupsRemoveChannelsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-assign [options]`

- What: admin\_users\_assign — write (POST /admin.users.assign)
- Call: `POST /admin.users.assign`, effect: write
- Body: `AdminUsersAssignRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-invite [options]`

- What: admin\_users\_invite — write (POST /admin.users.invite)
- Call: `POST /admin.users.invite`, effect: write
- Body: `AdminUsersInviteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-list [options]`

- What: admin\_users\_list — read (GET /admin.users.list)
- Call: `GET /admin.users.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | yes | The ID (\`T1234\`) of the workspace. |
| `--cursor <value>` | no | Set \`cursor\` to \`next\_cursor\` returned by the previous call to list items in the next page. |
| `--limit <value>` | no | Limit for how many users to be retrieved per page |

## `slk api admin users-remove [options]`

- What: admin\_users\_remove — destructive (POST /admin.users.remove)
- Call: `POST /admin.users.remove`, effect: destructive
- Permission keys: `slack.delete`
- Body: `AdminUsersRemoveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-session-invalidate [options]`

- What: admin\_users\_session\_invalidate — destructive (POST…
- Call: `POST /admin.users.session.invalidate`, effect: destructive
- Permission keys: `slack.delete`
- Body: `AdminUsersSessionInvalidateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-session-reset [options]`

- What: admin\_users\_session\_reset — destructive (POST /admin.users.session.reset)
- Call: `POST /admin.users.session.reset`, effect: destructive
- Permission keys: `slack.delete`
- Body: `AdminUsersSessionResetRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-set-admin [options]`

- What: admin\_users\_setAdmin — write (POST /admin.users.setAdmin)
- Call: `POST /admin.users.setAdmin`, effect: write
- Body: `AdminUsersSetAdminRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-set-expiration [options]`

- What: admin\_users\_setExpiration — write (POST /admin.users.setExpiration)
- Call: `POST /admin.users.setExpiration`, effect: write
- Body: `AdminUsersSetExpirationRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-set-owner [options]`

- What: admin\_users\_setOwner — write (POST /admin.users.setOwner)
- Call: `POST /admin.users.setOwner`, effect: write
- Body: `AdminUsersSetOwnerRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api admin users-set-regular [options]`

- What: admin\_users\_setRegular — write (POST /admin.users.setRegular)
- Call: `POST /admin.users.setRegular`, effect: write
- Body: `AdminUsersSetRegularRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
