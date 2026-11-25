<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Linear API: mutation

## `linear api agent-activity-create [options]`

- What: Publishes an activity to your agent’s session and updates its lifecycle. Thoughts and actions report ongoing work; a response completes the turn unless it has the continue signal, an elicitation waits for user input, and an error records a failed turn. The session must be unarchived and owned by the authenticated app user. Use the agent app’s OAuth or workload identity token; personal API keys cannot publish agent activities.
- Call: `mutation agentActivityCreate`, effect: write
- Body: `AgentActivityCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The agent activity object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-session-create-on-comment [options]`

- What: Starts an active session for your authenticated agent app on an existing issue comment thread. Supply the UUID of an unarchived root comment; replies and threads that already have a session are rejected. The caller must have access to the issue. Use the returned session ID when publishing activities.
- Call: `mutation agentSessionCreateOnComment`, effect: write
- Body: `AgentSessionCreateOnCommentRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The agent session object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-session-create-on-issue [options]`

- What: Starts an active session for your authenticated agent app and creates its comment thread on the issue. The issue must be accessible and writable. Supply its UUID or identifier, then use the returned session ID to publish progress and results with agentActivityCreate.
- Call: `mutation agentSessionCreateOnIssue`, effect: write
- Body: `AgentSessionCreateOnIssueRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The agent session object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-session-update [options]`

- What: Updates your agent’s session title, external links, or plan. Only the app user that owns the session can change these fields. Omitted fields remain unchanged, while each supplied plan or externalUrls list replaces that value. Updates other than a title-only change acknowledge a pending or stale session by making it active; publishing an activity still determines the next turn status.
- Call: `mutation agentSessionUpdate`, effect: write
- Body: `AgentSessionUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial agent session object to update the agent session with. |
| `--id <value>` | no | The identifier of the agent session to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-session-update-external-url [options]`

- What: Updates external links on a session owned by the authenticated agent app. A pending or stale session becomes active.
- Call: `mutation agentSessionUpdateExternalUrl`, effect: write
- Body: `AgentSessionUpdateExternalUrlRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The agent session object to update. |
| `--id <value>` | no | The identifier of the agent session to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-skill-create [options]`

- What: Creates reusable Markdown instructions for the Linear Agent, owned by the authenticated user. Omit teamId for a personal skill, or provide a team UUID to share it with that team. Creating a team skill requires permission to manage the team’s agent skills. The returned skill contains the saved instructions and display details.
- Call: `mutation agentSkillCreate`, effect: write
- Body: `AgentSkillCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The agent skill object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-skill-delete [options]`

- What: Deletes an agent skill and its inherited copies. Inherited skills must be deleted from the team that owns the source skill.
- Call: `mutation agentSkillDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `AgentSkillDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the agent skill to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api agent-skill-update [options]`

- What: Updates a skill the caller can manage. Omitted fields remain unchanged, and a supplied body replaces the full instruction text. For a team skill, the caller needs agent skill management permission; moving it also requires that permission in the destination team. Inherited copies cannot be edited directly—update their source skill instead.
- Call: `mutation agentSkillUpdate`, effect: write
- Body: `AgentSkillUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Data to update the agent skill with. |
| `--id <value>` | no | The identifier of the agent skill to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api airbyte-integration-connect [options]`

- What: Registers an export key for Airbyte. Requires integration-creation and export permissions and a plan with data export. The key can read private-team data.
- Call: `mutation airbyteIntegrationConnect`, effect: write
- Body: `AirbyteIntegrationConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Airbyte integration settings. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-create [options]`

- What: Creates an attachment, or updates the existing attachment with the same URL on the same issue. This is useful for links and metadata managed by your integration. Use attachmentLinkURL or a service-specific link mutation when you want Linear to fetch integration metadata and apply its supported link behavior.
- Call: `mutation attachmentCreate`, effect: write
- Body: `AttachmentCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The attachment object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-delete [options]`

- What: Deletes the attachment record from its issue. This removes the link in Linear; it does not delete the external resource.
- Call: `mutation attachmentDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `AttachmentDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the attachment to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-discord [options]`

- What: Link a Discord message to an issue. Requires a connected Discord integration.
- Call: `mutation attachmentLinkDiscord`, effect: write
- Body: `AttachmentLinkDiscordRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The issue for which to link the Discord message. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--channel-id <value>` | no | The Discord channel ID for the message to link. |
| `--message-id <value>` | no | The Discord message ID for the message to link. |
| `--url <value>` | no | The Discord message URL for the message to link. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-front [options]`

- What: Link a Front conversation to an issue. Requires a connected Front integration.
- Call: `mutation attachmentLinkFront`, effect: write
- Body: `AttachmentLinkFrontRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--conversation-id <value>` | no | The Front conversation ID to link. |
| `--issue-id <value>` | no | The issue for which to link the Front conversation. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-git-hub-issue [options]`

- What: Link a GitHub issue to a Linear issue. Uses the matching GitHub integration and sync mapping when available; may fall back to a URL attachment.
- Call: `mutation attachmentLinkGitHubIssue`, effect: write
- Body: `AttachmentLinkGitHubIssueRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The Linear issue for which to link the GitHub issue. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--url <value>` | no | The URL of the GitHub issue to link. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-git-hub-pr [options]`

- What: Link a GitHub pull request to an issue. Uses the matching GitHub integration when available; may fall back to a URL attachment.
- Call: `mutation attachmentLinkGitHubPR`, effect: write
- Body: `AttachmentLinkGitHubPRRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The issue for which to link the GitHub pull request. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--url <value>` | no | The URL of the GitHub pull request to link. |
| `--link-kind <value>` | no | The kind of link between the issue and the pull request. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-git-lab-mr [options]`

- What: Links a GitLab merge request to an issue. Supply the merge-request URL, number, and full project path including any groups. Linear uses a matching integration when available and otherwise creates a basic URL attachment.
- Call: `mutation attachmentLinkGitLabMR`, effect: write
- Body: `AttachmentLinkGitLabMRRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The issue for which to link the GitLab merge request. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--url <value>` | no | The URL of the GitLab merge request to link. |
| `--project-path-with-namespace <value>` | no | The path name to the project including any (sub)groups. E.g. linear/main/client. |
| `--number <value>` | no | The GitLab merge request number to link. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-intercom [options]`

- What: Link an Intercom conversation to an issue. Requires a connected Intercom integration.
- Call: `mutation attachmentLinkIntercom`, effect: write
- Body: `AttachmentLinkIntercomRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--conversation-id <value>` | no | The Intercom conversation ID to link. |
| `--part-id <value>` | no | An optional Intercom conversation part ID to link to |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--issue-id <value>` | no | The issue for which to link the Intercom conversation. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-jira-issue [options]`

- What: Links a Jira issue to a Linear issue. The URL selects a connected Jira site; if it identifies no connected site, Linear uses the workspace’s sole Jira integration. With multiple Jira integrations, provide a URL for the intended site.
- Call: `mutation attachmentLinkJiraIssue`, effect: write
- Body: `AttachmentLinkJiraIssueRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The issue for which to link the Jira issue. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--jira-issue-id <value>` | no | The Jira issue key or ID to link. |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--url <value>` | no | URL used to select the connected Jira site and as a fallback if the Jira issue cannot be fetched. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-salesforce [options]`

- What: Link a Salesforce case to an issue. Requires a connected Salesforce integration and a valid case URL.
- Call: `mutation attachmentLinkSalesforce`, effect: write
- Body: `AttachmentLinkSalesforceRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The issue for which to link the Salesforce case. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--url <value>` | no | The URL of the Salesforce case to link. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-slack [options]`

- What: Link an existing Slack message to an issue. This creates a rich attachment using the workspace's Slack integration.
- Call: `mutation attachmentLinkSlack`, effect: write
- Body: `AttachmentLinkSlackRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--issue-id <value>` | no | The issue to which to link the Slack message. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--url <value>` | no | The Slack message URL for the message to link. |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--sync-to-comment-thread <value>` | no | Sync the Slack thread with issue comments and import existing replies. Defaults to false; the thread cannot already be synced elsewhere. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-url [options]`

- What: Links a URL to an issue and, when recognized, uses the workspace’s matching integration to fetch richer details. Supported integrations can add behaviors such as status updates. If no matching integration can enrich the link, Linear creates a basic URL attachment.
- Call: `mutation attachmentLinkURL`, effect: write
- Body: `AttachmentLinkURLRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--url <value>` | no | The url to link. |
| `--issue-id <value>` | no | The issue for which to link the url. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | The id for the attachment. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-link-zendesk [options]`

- What: Link a Zendesk ticket to an issue. Requires a connected Zendesk integration.
- Call: `mutation attachmentLinkZendesk`, effect: write
- Body: `AttachmentLinkZendeskRequest`, required

| Flag | Required | What |
|---|---|---|
| `--create-as-user <value>` | no | Display name credited with creating the attachment. Available only to OAuth applications using actor=app. |
| `--display-icon-url <value>` | no | Avatar URL for createAsUser. Requires createAsUser and an OAuth application using actor=app. |
| `--title <value>` | no | The title to use for the attachment. |
| `--ticket-id <value>` | no | The Zendesk ticket ID to link. |
| `--issue-id <value>` | no | The issue for which to link the Zendesk ticket. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--id <value>` | no | Optional attachment ID that may be provided through the API. |
| `--url <value>` | no | The URL of the Zendesk ticket to link. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-sync-to-slack [options]`

- What: Sync an existing Slack attachment with an issue comment thread and import existing replies. Requires a connected Slack integration whose bot can post in the channel; the Slack thread cannot already be synced elsewhere.
- Call: `mutation attachmentSyncToSlack`, effect: write
- Body: `AttachmentSyncToSlackRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The ID of the Slack attachment to begin syncing. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api attachment-update [options]`

- What: Updates an existing attachment’s title, subtitle, metadata, or icon. title is required even when changing another field, and metadata replaces the full stored object. This mutation does not move the attachment or change its URL.
- Call: `mutation attachmentUpdate`, effect: write
- Body: `AttachmentUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial attachment object to update the attachment with. |
| `--id <value>` | no | The identifier of the attachment to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api comment-create [options]`

- What: Creates a comment on one resource, or a reply when parentId is supplied. You must be allowed to comment on that resource. For issue comments, the author is subscribed to the issue unless doNotSubscribeToIssue is true.
- Call: `mutation commentCreate`, effect: write
- Body: `CommentCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The comment object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api comment-delete [options]`

- What: Deletes a comment and, for a root comment, its replies. You must be allowed to delete the comment and comment on its resource. Deleting a reply selected as the resolution reopens the parent thread.
- Call: `mutation commentDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CommentDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the comment to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api comment-resolve [options]`

- What: Marks a root comment’s thread as resolved by you. You may select one of its replies as resolvingCommentId, or resolve the thread without a specific reply. Pass the root comment ID, even when the discussion ended in a reply.
- Call: `mutation commentResolve`, effect: write
- Body: `CommentResolveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--resolving-comment-id <value>` | no | The identifier of the child comment that resolves the thread. If not provided, the thread is resolved without a specific resolving comment. |
| `--id <value>` | no | The identifier of the comment to resolve. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api comment-unresolve [options]`

- What: Reopens a resolved thread and clears its resolution time, resolving user, and selected resolving reply. Pass the root comment ID. An already unresolved thread is returned unchanged.
- Call: `mutation commentUnresolve`, effect: write
- Body: `CommentUnresolveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the comment to unresolve. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api comment-update [options]`

- What: Replaces a comment’s Markdown body and records an edit time. Content edits are restricted to an authorized author or acting user; comments originating in synced Slack messages or Intercom cannot be edited here. Omit body to keep the existing message.
- Call: `mutation commentUpdate`, effect: write
- Body: `CommentUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--skip-edited-at <value>` | no | \[INTERNAL\] Flag to prevent setting editedAt when updating bodyData (used for background uploads). |
| `--input <value>` | no | A partial comment object to update the comment with. |
| `--id <value>` | no | The identifier of the comment to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api contact-create [options]`

- What: Submits a message to Linear support on behalf of the authenticated user. Delivery happens after the request succeeds.
- Call: `mutation contactCreate`, effect: write
- Body: `ContactCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The contact entry to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api create-csv-export-report [options]`

- What: Queues a workspace CSV export and emails the requesting user a download link when it is ready. Success confirms scheduling, not completion. Private and restricted teams are excluded unless explicitly selected by their UUIDs. Requires workspace export permission, which permits selecting eligible teams even when the requester is not a member.
- Call: `mutation createCsvExportReport`, effect: write
- Body: `CreateCsvExportReportRequest`

| Flag | Required | What |
|---|---|---|
| `--include-private-team-ids <value>` | no | UUIDs of private teams to include in the export. Omit or use an empty list to exclude private teams. Restricted teams are selected separately. |
| `--include-restricted-team-ids <value>` | no | UUIDs of restricted teams to include in the export. An empty list excludes restricted teams. Omission falls back to the deprecated includeProtectedTeamIds list, or excludes them if neither list is provided. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api create-initiative-update-reminder [options]`

- What: Create a notification to remind a user about an initiative update.
- Call: `mutation createInitiativeUpdateReminder`, effect: write
- Body: `CreateInitiativeUpdateReminderRequest`, required

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | no | The user identifier to whom the notification will be sent. By default, it is set to the initiative owner. |
| `--initiative-id <value>` | no | The identifier of the initiative to remind about. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api create-project-update-reminder [options]`

- What: Create a notification to remind a user about a project update.
- Call: `mutation createProjectUpdateReminder`, effect: write
- Body: `CreateProjectUpdateReminderRequest`, required

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | no | The user identifier to whom the notification will be sent. By default, it is set to the project lead. |
| `--project-id <value>` | no | The identifier of the project to remind about. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api custom-view-create [options]`

- What: Creates a saved view owned by you. Choose an issue, project, initiative, or update filter and set shared if others in its scope should use it. Display settings can be saved separately with viewPreferencesCreate.
- Call: `mutation customViewCreate`, effect: write
- Body: `CustomViewCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the custom view to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api custom-view-delete [options]`

- What: Deletes a saved view without deleting the items it displayed. Only workspace members can delete views shared with the whole workspace; deleting a view used in a pinned tab also requires permission to edit that tab. Use customViewHasSubscribers to check whether other people receive notifications from the view.
- Call: `mutation customViewDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CustomViewDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the custom view to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api custom-view-update [options]`

- What: Updates a saved view’s metadata, scope, or filter configuration. Omitted fields are unchanged. Only workspace members can change views shared with the whole workspace; editing a view used in a pinned tab also requires permission to edit that tab.
- Call: `mutation customViewUpdate`, effect: write
- Body: `CustomViewUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the custom view to update. |
| `--id <value>` | no | The identifier of the custom view to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-create [options]`

- What: Creates a customer when the Customers feature is available and enabled in the workspace. Business domains and external IDs must not belong to another customer, including archived customers. If no status is supplied, the first customer status by position is used.
- Call: `mutation customerCreate`, effect: write
- Body: `CustomerCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The customer to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-delete [options]`

- What: Permanently deletes a customer, including an archived customer. Use customerMerge when you want to preserve its requests by transferring them to another customer.
- Call: `mutation customerDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CustomerDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the customer to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-merge [options]`

- What: Merges two customers by transferring all needs from the source customer to the target customer. The source customer is archived after the merge. Domains, external IDs, and metadata are combined on the target customer.
- Call: `mutation customerMerge`, effect: write
- Body: `CustomerMergeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--source-customer-id <value>` | no | The ID of the source customer to merge. All needs from this customer will be transferred to the target, and this customer will be archived. |
| `--target-customer-id <value>` | no | The ID of the target customer to merge into. This customer will receive all needs from the source customer and retain its own. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-need-archive [options]`

- What: Archives a customer need so it can be removed from active request lists without permanently deleting it. Use customerNeedUnarchive to restore the saved need.
- Call: `mutation customerNeedArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CustomerNeedArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the customer need to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-need-create [options]`

- What: Records customer feedback, optionally linked to an issue. Unlinked requests require Customer Signals to be enabled. You can identify the customer, add Markdown feedback, or link a source attachment. Multiple requests can be recorded for the same customer and issue.
- Call: `mutation customerNeedCreate`, effect: write
- Body: `CustomerNeedCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The customer need to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-need-create-from-attachment [options]`

- What: Creates a customer need from an existing issue attachment. If that attachment already has an archived need, the need is restored and follows the attachment’s current issue. An existing active need is not duplicated.
- Call: `mutation customerNeedCreateFromAttachment`, effect: write
- Body: `CustomerNeedCreateFromAttachmentRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The customer need to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-need-delete [options]`

- What: Permanently deletes a customer need. By default, its associated issue or project attachment is also deleted. Set keepAttachment to true to retain that source attachment; the linked issue or project is kept.
- Call: `mutation customerNeedDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CustomerNeedDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--keep-attachment <value>` | no | Whether to keep the attachment associated with the customer need. |
| `--id <value>` | no | The identifier of the customer need to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-need-unarchive [options]`

- What: Restores an archived customer need. The need must currently be archived; its saved feedback and associations are kept.
- Call: `mutation customerNeedUnarchive`, effect: write
- Body: `CustomerNeedUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the customer need to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-need-update [options]`

- What: Updates a customer request, including its feedback, customer, priority, or issue association. Only manually added source attachments can be replaced or removed. Use clearAttachment to remove such a source; moving the request to another issue also moves its source attachment.
- Call: `mutation customerNeedUpdate`, effect: write
- Body: `CustomerNeedUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--clear-attachment <value>` | no | Whether to remove the manually added source attachment. Sources managed by an integration cannot be removed this way. A different, nonempty attachmentUrl takes precedence. |
| `--input <value>` | no | The properties of the customer need to update. |
| `--id <value>` | no | The identifier of the customer need to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-status-create [options]`

- What: Creates a workspace customer status. Requires permission to manage customer settings and rejects a name or display name already used by another active status.
- Call: `mutation customerStatusCreate`, effect: write
- Body: `CustomerStatusCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The CustomerStatus object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-status-delete [options]`

- What: Deletes a customer status. Cannot delete the last remaining status in a workspace, and the status must not be in use by any customers.
- Call: `mutation customerStatusDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CustomerStatusDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the customer status to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-status-update [options]`

- What: Updates a workspace customer status. Requires permission to manage customer settings. Customers using the status retain their association with it.
- Call: `mutation customerStatusUpdate`, effect: write
- Body: `CustomerStatusUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial CustomerStatus object to update the CustomerStatus with. |
| `--id <value>` | no | The identifier of the customer status to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-tier-create [options]`

- What: Creates a workspace customer tier. Requires permission to manage customer settings and rejects a name or display name already used by another active tier.
- Call: `mutation customerTierCreate`, effect: write
- Body: `CustomerTierCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The CustomerTier object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-tier-delete [options]`

- What: Deletes a customer tier. The tier must not be in use by any customers.
- Call: `mutation customerTierDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CustomerTierDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the customer tier to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-tier-update [options]`

- What: Updates a workspace customer tier. Requires permission to manage customer settings. Customers using the tier retain their association with it.
- Call: `mutation customerTierUpdate`, effect: write
- Body: `CustomerTierUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial CustomerTier object to update the CustomerTier with. |
| `--id <value>` | no | The identifier of the customer tier to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-unsync [options]`

- What: Disconnects a customer from its configured data source integration so the integration no longer updates it. External IDs belonging to that source are cleared. Requires permission to manage workspace customer settings.
- Call: `mutation customerUnsync`, effect: write
- Body: `CustomerUnsyncRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the customer to unsync. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-update [options]`

- What: Updates the supplied customer fields, leaving omitted fields unchanged. For a customer managed by an integration, only fields that are editable in Linear are applied; managed fields are ignored. The request fails if none of the supplied fields are editable.
- Call: `mutation customerUpdate`, effect: write
- Body: `CustomerUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the customer to update. |
| `--id <value>` | no | The identifier of the customer to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api customer-upsert [options]`

- What: Finds a customer using the supplied UUID, external ID, Slack channel, or domains, and updates it; otherwise creates one. A name is required when no customer matches. Unlike customerUpdate, this operation can override integration-managed fields, and a tierName can create a new customer tier.
- Call: `mutation customerUpsert`, effect: write
- Body: `CustomerUpsertRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The customer to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api cycle-archive [options]`

- What: Archives a cycle and removes its current issues from it. The issues themselves are not archived. An inherited cycle must be managed through its parent team. Requires permission to manage the team.
- Call: `mutation cycleArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `CycleArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the cycle to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api cycle-create [options]`

- What: Unsupported. This mutation always returns an error; cycles are generated from the team’s cycle settings.
- Call: `mutation cycleCreate`, effect: write, deprecated
- Body: `CycleCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The cycle object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api cycle-shift-all [options]`

- What: Shifts an upcoming cycle and every later cycle in the team by the same number of days. Local times are preserved in the team’s time zone, and the team’s cycle start day is updated. Use this when moving the schedule as a whole; it requires permission to manage the team.
- Call: `mutation cycleShiftAll`, effect: write
- Body: `CycleShiftAllRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The shift parameters specifying which cycle to start from and how many days to shift. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api cycle-start-upcoming-cycle-today [options]`

- What: Starts the upcoming cycle as of midnight today. Completes the previous cycle if it has not yet ended. Only the next upcoming (not yet started) cycle for the team can be started. Requires permission to manage the team.
- Call: `mutation cycleStartUpcomingCycleToday`, effect: write
- Body: `CycleStartUpcomingCycleTodayRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the cycle to start as of midnight today. Must be the upcoming cycle. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api cycle-update [options]`

- What: Updates a cycle’s name, description, or schedule and returns the resulting cycle. Date changes can shorten adjacent cycles to prevent overlap. You cannot change an active cycle’s start or a completed cycle’s dates, or edit inherited cycles directly. Requires permission to manage the team.
- Call: `mutation cycleUpdate`, effect: write
- Body: `CycleUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial cycle object to update the cycle with. |
| `--id <value>` | no | The identifier of the cycle to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api document-create [options]`

- What: Creates a document in a project, issue, or release, with optional initial Markdown content. The returned document includes its assigned UUID and metadata; select content to read the resulting body.
- Call: `mutation documentCreate`, effect: write
- Body: `DocumentCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The document to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api document-delete [options]`

- What: Moves a document to the trash and archives it, including the sub-documents covered by its archive cascade. It is not permanently removed by this mutation. You must be allowed to manage the document; use documentUnarchive to restore it.
- Call: `mutation documentDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `DocumentDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--if-parent-document-id <value>` | no | \[Internal\] Only trash the document if it is still a sub-document of this document. Otherwise the mutation fails and the document is left unchanged. |
| `--id <value>` | no | The identifier of the document to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api document-unarchive [options]`

- What: Restores a trashed document and its eligible sub-documents. You must be allowed to manage the restored documents. If the containing resource is archived, restore that resource first.
- Call: `mutation documentUnarchive`, effect: write
- Body: `DocumentUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the document to restore. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api document-update [options]`

- What: Updates a document’s metadata or replaces its Markdown body. You must have edit access to the document. Supplying a different container moves the document there, which can affect access; omitted fields are left unchanged.
- Call: `mutation documentUpdate`, effect: write
- Body: `DocumentUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial document object to update the document with. |
| `--id <value>` | no | The identifier of the document to update. Also the identifier from the URL is accepted. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api document-update-workspace-access [options]`

- What: \[Internal\] Changes what people outside a document's teams can do with a document in a public team or in a project with a public team: edit, comment, or view. It can't be above the document's general access. Only the owner of the document, an owner of one of its teams, or a workspace admin can change it. Comment and view need an owner who can access the document.
- Call: `mutation documentUpdateWorkspaceAccess`, effect: write
- Body: `DocumentUpdateWorkspaceAccessRequest`, required

| Flag | Required | What |
|---|---|---|
| `--previous-workspace-access <value>` | no | The workspace access level of this document when the change was confirmed. When given, the change fails if the document has another level now. |
| `--apply-to-sub-documents <value>` | no | Whether to also change the sub-documents whose levels equal the document's levels before the change. Sub-documents with other levels, without an owner who can access them, or that the user cannot loosen keep their level. |
| `--workspace-access <value>` | no | The new workspace access level: edit, comment, or view. |
| `--id <value>` | no | The identifier of the document. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-intake-address-create [options]`

- What: Creates an address that accepts email for one team or issue template. For team and template types, an existing active address for that destination is returned instead of creating another. Use the returned emailAddress as the forwarding destination in your mail provider. Asks creation requires the appropriate plan and integration management permission; team and template addresses require permission to manage their destination. Form templates cannot be used for template intake.
- Call: `mutation emailIntakeAddressCreate`, effect: write
- Body: `EmailIntakeAddressCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The email intake address object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-intake-address-delete [options]`

- What: Deletes an email intake address object.
- Call: `mutation emailIntakeAddressDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `EmailIntakeAddressDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the email intake address to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-intake-address-refresh-ses-domain-status [options]`

- What: Requests a check of the intake address’s custom sending domain after you update its DNS records. The check runs asynchronously: success means a check was requested, not that the domain passed verification. Query sesDomainIdentity.canSendFromCustomDomain and dnsRecords for the result. Returns success=false when no custom domain is configured or the domain is already fully verified.
- Call: `mutation emailIntakeAddressRefreshSesDomainStatus`, effect: write
- Body: `EmailIntakeAddressRefreshSesDomainStatusRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the email intake address to refresh the domain status for. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-intake-address-rotate [options]`

- What: Generates a new email address for an existing team or template intake configuration. The old address no longer routes incoming mail, so update any forwarding rules or places where you published it. The intake record and its settings are retained. Asks and Asks web addresses do not support rotation through this mutation.
- Call: `mutation emailIntakeAddressRotate`, effect: write
- Body: `EmailIntakeAddressRotateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the email intake address. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-intake-address-update [options]`

- What: Updates an existing email intake address.
- Call: `mutation emailIntakeAddressUpdate`, effect: write
- Body: `EmailIntakeAddressUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the email intake address to update. |
| `--id <value>` | no | The identifier of the email intake address. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-token-user-account-auth [options]`

- What: Completes email sign-in using the emailed token and the same clientAuthCode sent with emailUserAccountAuthChallenge. Successful authentication consumes the client binding and sets a session cookie. Use the returned memberships and available or locked workspaces to continue into a workspace; the deprecated token field is not populated. An expired token or a code from a different client cannot complete this flow.
- Call: `mutation emailTokenUserAccountAuth`, effect: write
- Body: `EmailTokenUserAccountAuthRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The data used for token authentication. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-unsubscribe [options]`

- What: Unsubscribes a user from the selected email category using the user ID and token from a Linear email. No sign-in is required because the token authorizes the change. An invalid token returns success=false; other email categories and notification channels are unchanged.
- Call: `mutation emailUnsubscribe`, effect: write
- Body: `EmailUnsubscribeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Unsubscription details. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api email-user-account-auth-challenge [options]`

- What: Starts email sign-in and sends a one-time token to the supplied address. Generate and retain a clientAuthCode UUID, then pass it with the emailed token to emailTokenUserAccountAuth within ten minutes. Requesting another challenge replaces the stored client binding for that email. When login challenge verification is enabled, challengeResponse is also required. Success confirms the challenge was accepted; email delivery may finish in the background.
- Call: `mutation emailUserAccountAuthChallenge`, effect: write
- Body: `EmailUserAccountAuthChallengeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The data used for email authentication. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api emoji-create [options]`

- What: Creates a custom emoji from an image already uploaded to Linear. Its name must be unique in the workspace. The current user is recorded as the creator, and the source is user.
- Call: `mutation emojiCreate`, effect: write
- Body: `EmojiCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The emoji object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api emoji-delete [options]`

- What: Deletes an emoji.
- Call: `mutation emojiDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `EmojiDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the emoji to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api entity-external-link-create [options]`

- What: Adds an external resource to an initiative, project, or release the caller can access and write to. Provide exactly one parent, a destination URL, and the label to show in Linear. Omit sortOrder to place the link last among the parent’s resources. This stores a reference to the URL; it does not upload or copy the destination content.
- Call: `mutation entityExternalLinkCreate`, effect: write
- Body: `EntityExternalLinkCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The entity link object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api entity-external-link-delete [options]`

- What: Removes a resource link from Linear and clears any team pins that refer to it. The external URL’s content is unchanged. The caller must have access to the link’s parent scope; archived links can also be deleted.
- Call: `mutation entityExternalLinkDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `EntityExternalLinkDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the entity link to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api entity-external-link-update [options]`

- What: Changes an unarchived resource link’s URL, display label, or position within its parent’s resources. Omitted fields remain unchanged, and the parent cannot be changed. The link must be writable and within the caller’s permitted scope.
- Call: `mutation entityExternalLinkUpdate`, effect: write
- Body: `EntityExternalLinkUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The entity link object to update. |
| `--id <value>` | no | The identifier of the entity link to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api favorite-create [options]`

- What: Creates a sidebar favorite for the authenticated user. If it already exists, updates its position and supplied folder instead.
- Call: `mutation favoriteCreate`, effect: write
- Body: `FavoriteCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The favorite object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api favorite-delete [options]`

- What: Removes a favorite from your sidebar. Deleting a custom folder also removes the favorites inside it; the bookmarked entities are unaffected. The mutation succeeds if the favorite no longer exists.
- Call: `mutation favoriteDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `FavoriteDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the favorite reference to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api favorite-update [options]`

- What: Changes the position, parent folder, or name of one of your favorites. Omitted fields stay unchanged. The target entity cannot be changed, and predefined live folders cannot be renamed.
- Call: `mutation favoriteUpdate`, effect: write
- Body: `FavoriteUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial favorite object to update the favorite with. |
| `--id <value>` | no | The identifier of the favorite to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api file-upload [options]`

- What: Prepares a file upload and returns a signed destination. Upload the raw bytes with HTTP PUT to uploadFile.uploadUrl, using its headers and the supplied Content-Type; start the request within one minute and send exactly size bytes. Once the PUT succeeds, reference uploadFile.assetUrl in an issue description, comment, or attachment. This mutation does not create that reference for you. Workspace file-type restrictions and plan upload limits apply.
- Call: `mutation fileUpload`, effect: write
- Body: `FileUploadRequest`, required

| Flag | Required | What |
|---|---|---|
| `--meta-data <value>` | no | Optional metadata encoded as a JSON string, such as {"issueId":"..."} or {"commentId":"..."}. These references record upload context; they do not insert the file into that issue or comment. You still need to use assetUrl when creating or updating the content. |
| `--make-public <value>` | no | Whether anyone with the asset URL can view the uploaded image without authenticating. Omit or set false for a private upload. Only non-SVG images can be public; other file types are rejected when this is true. |
| `--size <value>` | no | Exact file size in bytes. The upload request must match this size. |
| `--content-type <value>` | no | MIME type of the uploaded file. |
| `--filename <value>` | no | Filename of the uploaded file. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api file-upload-dangerously-delete [options]`

- What: Permanently delete an uploaded file by asset URL. This should be used as a last resort and will break comments and documents that reference the asset.
- Call: `mutation fileUploadDangerouslyDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `FileUploadDangerouslyDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--asset-url <value>` | no | The asset URL of the uploaded file to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api git-automation-state-create [options]`

- What: Creates a rule that maps a Git event to an issue status for a team. Requires permission to manage that team. Rules cannot be created for retired teams.
- Call: `mutation gitAutomationStateCreate`, effect: write
- Body: `GitAutomationStateCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The automation state to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api git-automation-state-delete [options]`

- What: Permanently deletes a Git automation rule. Requires permission to manage its team. Removing a branch-specific rule allows the team’s default for that event to apply again.
- Call: `mutation gitAutomationStateDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `GitAutomationStateDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the automation state to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api git-automation-state-update [options]`

- What: Updates the status, branch scope, or event of an existing rule. Requires permission to manage its team, and the team must not be retired. Omitted fields keep their values.
- Call: `mutation gitAutomationStateUpdate`, effect: write
- Body: `GitAutomationStateUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The state to update. |
| `--id <value>` | no | The identifier of the state to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api git-automation-target-branch-create [options]`

- What: Creates a team’s target-branch pattern for Git automation. Add automation rules that reference the returned definition to choose the status changes. Requires team-management permission and an active, non-retired team.
- Call: `mutation gitAutomationTargetBranchCreate`, effect: write
- Body: `GitAutomationTargetBranchCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The Git target branch automation to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api git-automation-target-branch-delete [options]`

- What: Deletes a target-branch definition and its associated automation rules. Future matching events use any remaining applicable rules, including team defaults. Requires team-management permission.
- Call: `mutation gitAutomationTargetBranchDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `GitAutomationTargetBranchDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the target branch definition to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api git-automation-target-branch-update [options]`

- What: Changes the pattern or matching mode used by every automation rule linked to this definition. Omitted fields stay unchanged. Requires team-management permission; definitions in retired teams cannot be updated.
- Call: `mutation gitAutomationTargetBranchUpdate`, effect: write
- Body: `GitAutomationTargetBranchUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The updates. |
| `--id <value>` | no | The identifier of the Git target branch automation to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api google-user-account-auth [options]`

- What: Exchanges a Google OAuth code, sets the authentication cookie, and returns workspace access details. May create an account unless disallowSignup is true.
- Call: `mutation googleUserAccountAuth`, effect: write
- Body: `GoogleUserAccountAuthRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The data used for Google authentication. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api image-upload-from-url [options]`

- What: Copies an image from an external URL into Linear’s private upload storage. The URL must let Linear download the image directly; an HTML page containing the image is not accepted. On success, the returned URL refers to the copied image and can be used in Linear content. Unlike fileUpload, this mutation performs the download and upload for you.
- Call: `mutation imageUploadFromUrl`, effect: write
- Body: `ImageUploadFromUrlRequest`, required

| Flag | Required | What |
|---|---|---|
| `--url <value>` | no | URL of the file to be uploaded to Linear. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api import-file-upload [options]`

- What: Prepares a file in Linear’s import storage. Upload the raw bytes with HTTP PUT to the returned uploadUrl, using all returned headers and the matching Content-Type. The upload must start within one minute and contain exactly the declared number of bytes. Success prepares the destination; it does not upload the bytes or start an import.
- Call: `mutation importFileUpload`, effect: write
- Body: `ImportFileUploadRequest`, required

| Flag | Required | What |
|---|---|---|
| `--meta-data <value>` | no | Optional metadata encoded as a JSON string, such as {"issueId":"..."} or {"commentId":"..."}. These references record upload context; they do not insert the file into that issue or comment. You still need to use assetUrl when creating or updating the content. |
| `--size <value>` | no | Exact file size in bytes. The upload request must match this size. |
| `--content-type <value>` | no | MIME type of the uploaded file. |
| `--filename <value>` | no | Filename of the uploaded file. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api inbox-notification-update [options]`

- What: Changes read or snooze state for the authenticated user’s group of related inbox notifications. Supply a notification UUID from the group and at least one state change. The response includes the requested notification and all notifications changed.
- Call: `mutation inboxNotificationUpdate`, effect: write
- Body: `InboxNotificationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The inbox state changes to apply. |
| `--id <value>` | no | The identifier of the inbox notification to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-add-label [options]`

- What: Adds an initiative label while keeping the other labels. Label groups themselves cannot be applied, and the group’s selection rules still apply.
- Call: `mutation initiativeAddLabel`, effect: write
- Body: `InitiativeAddLabelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--label-id <value>` | no | The identifier of the label to add. |
| `--id <value>` | no | The identifier of the initiative to add the label to. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-archive [options]`

- What: Archives an initiative.
- Call: `mutation initiativeArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `InitiativeArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiative to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-create [options]`

- What: Creates an initiative in a workspace where initiatives are enabled. You can assign an owner and lead team at creation. Add projects separately with initiativeToProjectCreate, and build a hierarchy with initiativeRelationCreate.
- Call: `mutation initiativeCreate`, effect: write
- Body: `InitiativeCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the initiative to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-delete [options]`

- What: Moves an initiative to the trash instead of immediately deleting it permanently. You can restore it with initiativeUnarchive while it remains available.
- Call: `mutation initiativeDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `InitiativeDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiative to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-label-create [options]`

- What: Creates a workspace label or label group for initiatives. Requires workspace label-management permission. Use parentId to place a label in a group.
- Call: `mutation initiativeLabelCreate`, effect: write
- Body: `InitiativeLabelCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The initiative label to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-label-delete [options]`

- What: Deletes an initiative label and its children, removing their assignments from initiatives.
- Call: `mutation initiativeLabelDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `InitiativeLabelDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-label-restore [options]`

- What: Restores a previously retired initiative label, making it available for use on new initiatives.
- Call: `mutation initiativeLabelRestore`, effect: write
- Body: `InitiativeLabelRestoreRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to restore. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-label-retire [options]`

- What: Retires an initiative label. Retired labels remain on existing initiatives but cannot be applied to new ones.
- Call: `mutation initiativeLabelRetire`, effect: write
- Body: `InitiativeLabelRetireRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to retire. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-label-update [options]`

- What: Changes the supplied label fields. Omitted fields stay unchanged. Requires workspace label-management permission.
- Call: `mutation initiativeLabelUpdate`, effect: write
- Body: `InitiativeLabelUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial label object to update. |
| `--id <value>` | no | The identifier of the label to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-relation-create [options]`

- What: Adds a child initiative to a parent. Both must be accessible and unarchived, and the workspace must support sub-initiatives. When the new parent overlaps the child’s existing hierarchy, the overlapping parent links are removed as part of the move. Cycles and excessive nesting are rejected.
- Call: `mutation initiativeRelationCreate`, effect: write
- Body: `InitiativeRelationCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The initiative relation to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-relation-delete [options]`

- What: Removes a parent-child link without deleting either initiative. Deleting a link that no longer exists succeeds without making changes; an existing link still requires access to both initiatives.
- Call: `mutation initiativeRelationDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `InitiativeRelationDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiative relation to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-relation-update [options]`

- What: Changes a child initiative’s ordering within its parent. The relation’s endpoints remain unchanged. Both initiatives must be visible to you.
- Call: `mutation initiativeRelationUpdate`, effect: write
- Body: `InitiativeRelationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the initiative relation to update. |
| `--id <value>` | no | The identifier of the initiative relation to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-remove-label [options]`

- What: Removes a label from the initiative while keeping its other labels. The label itself is not deleted.
- Call: `mutation initiativeRemoveLabel`, effect: write
- Body: `InitiativeRemoveLabelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--label-id <value>` | no | The identifier of the label to remove. |
| `--id <value>` | no | The identifier of the initiative to remove the label from. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-to-project-create [options]`

- What: Links an accessible, active project to an accessible, active initiative. Neither may be read-only. The link is rejected if the project is already in that initiative or one of its ancestors or descendants. App users need initiative:write scope.
- Call: `mutation initiativeToProjectCreate`, effect: write
- Body: `InitiativeToProjectCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the initiativeToProject to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-to-project-delete [options]`

- What: Removes an active project-to-initiative link without deleting either entity. Requires access to the association; app users need initiative:write scope.
- Call: `mutation initiativeToProjectDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `InitiativeToProjectDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiativeToProject to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-to-project-update [options]`

- What: Changes the project’s sort order within the initiative. The initiative and project endpoints cannot be changed through this mutation.
- Call: `mutation initiativeToProjectUpdate`, effect: write
- Body: `InitiativeToProjectUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the initiativeToProject to update. |
| `--id <value>` | no | The identifier of the initiativeToProject to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-unarchive [options]`

- What: Restores an archived or trashed initiative. This makes the existing initiative available again with its saved properties and associations.
- Call: `mutation initiativeUnarchive`, effect: write
- Body: `InitiativeUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiative to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-update [options]`

- What: Updates the supplied fields of an initiative you can access. Omitted fields keep their current values. Changing the lead team can change who can see the initiative, and the owner must be able to access the new team.
- Call: `mutation initiativeUpdate`, effect: write
- Body: `InitiativeUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the initiative to update. |
| `--id <value>` | no | The identifier of the initiative to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-update-archive [options]`

- What: Archives an update and recalculates the initiative’s health from the remaining updates. You must be the author or have permission to manage workspace entities. Use initiativeUpdateUnarchive to restore it.
- Call: `mutation initiativeUpdateArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `InitiativeUpdateArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiative update to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-update-create [options]`

- What: Publishes an update, records the current user as author, captures the initiative’s projects, and refreshes its health. Provide the written message in input.body.
- Call: `mutation initiativeUpdateCreate`, effect: write
- Body: `InitiativeUpdateCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The initiative update object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-update-unarchive [options]`

- What: Restores an archived update and recalculates the initiative’s health. You must be the author or have permission to manage workspace entities.
- Call: `mutation initiativeUpdateUnarchive`, effect: write
- Body: `InitiativeUpdateUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the initiative update to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api initiative-update-update [options]`

- What: Edits an update’s message or health. You must be the author or have permission to manage workspace entities. Editing the latest update while it is less than one hour old also refreshes its project snapshots.
- Call: `mutation initiativeUpdateUpdate`, effect: write
- Body: `InitiativeUpdateUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the initiative update to update. |
| `--id <value>` | no | The identifier of the initiative update to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-archive [options]`

- What: Disconnects an integration that supports archiving while retaining its record for a later reconnect. You can archive your own personal connection; workspace connections generally require integration-creation permission. GitHub installation removal and Jira webhook cleanup run in the background, so a successful response can precede the completed disconnection. Services that do not support archiving must use integrationDelete instead.
- Call: `mutation integrationArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IntegrationArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the integration to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-asks-connect-channel [options]`

- What: Connects the public or private Slack channel selected during OAuth to an existing Asks integration. The channel must be in that integration's Slack workspace and must not already be connected. Individual channel connections require full Asks access and permission to manage Asks settings. Check addBot after success and invite the bot manually when true. Direct messages work with Asks without this setup.
- Call: `mutation integrationAsksConnectChannel`, effect: write
- Body: `IntegrationAsksConnectChannelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-delete [options]`

- What: Disconnects an integration that supports deletion and removes its connection record. You can remove your own personal connection; workspace connections require integration-creation permission, and team, project, or view connections follow the permissions for that resource. Some services finish external cleanup in the background, so success does not guarantee that cleanup has finished. Services that retain a record for reconnecting must use integrationArchive instead.
- Call: `mutation integrationDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IntegrationDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--skip-installation-deletion <value>` | no | Whether to skip deleting the installation on the external service side. |
| `--id <value>` | no | The identifier of the integration to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-discord [options]`

- What: Connects a Discord server using the OAuth code and redirect URI from its authorization flow, and links the authorizing Discord user to your Linear account. A Linear workspace can have one Discord connection, and the Discord server cannot already belong to another Linear workspace's connection.
- Call: `mutation integrationDiscord`, effect: write
- Body: `IntegrationDiscordRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Discord OAuth redirect URI. |
| `--code <value>` | no | The Discord OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-figma [options]`

- What: Connects Figma using an OAuth authorization code and its redirect URI, storing the credentials needed for the workspace integration. The workspace cannot already have an active Figma connection.
- Call: `mutation integrationFigma`, effect: write
- Body: `IntegrationFigmaRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Figma OAuth redirect URI. |
| `--code <value>` | no | The Figma OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-front [options]`

- What: Connects Front using an OAuth grant. Requires the workspace's support integration plan feature and no existing Front connection. New connections initially reopen linked Front conversations when a Linear issue is completed or canceled; comments do not trigger reopening by default.
- Call: `mutation integrationFront`, effect: write
- Body: `IntegrationFrontRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Front OAuth redirect URI. |
| `--code <value>` | no | The Front OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-git-hub-enterprise-server-connect [options]`

- What: Starts a GitHub Enterprise Server connection for a GitHub organization or personal account. Open setupUrl to register the app, configure it with webhookSecret, then use installUrl to install it. Call verifyGitHubEnterpriseServerInstallation to check that the app has connected. Success here means the setup record was saved, not that installation is complete. An archived connection for the same organization is reused.
- Call: `mutation integrationGitHubEnterpriseServerConnect`, effect: write
- Body: `IntegrationGitHubEnterpriseServerConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--organization-name <value>` | no | GitHub organization login name. Use an empty string to create the app for a personal account. |
| `--github-url <value>` | no | The base URL of the GitHub Enterprise Server installation. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-git-hub-personal [options]`

- What: Links your GitHub account using an OAuth code from Linear's GitHub App authorization flow. codeAccess selects the app with repository code access and defaults to false. This is a personal account connection; connecting a workspace's GitHub App installation uses integrationGithubConnect.
- Call: `mutation integrationGitHubPersonal`, effect: write
- Body: `IntegrationGitHubPersonalRequest`, required

| Flag | Required | What |
|---|---|---|
| `--enterprise-url <value>` | no | The enterprise URL for GitHub Enterprise Cloud connections. Omit for github.com. |
| `--code-access <value>` | no | Whether to connect with code access. |
| `--code <value>` | no | The GitHub OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-github-commit-create`

- What: Creates the workspace's GitHub commit integration and returns its webhook secret. Use the secret when configuring the webhook in GitHub; creating this record alone does not configure GitHub to send events.
- Call: `mutation integrationGithubCommitCreate`, effect: write

## `linear api integration-github-connect [options]`

- What: Connects a GitHub App installation to the workspace using its installation ID and OAuth grant. If replacing a connection would make repositories used by GitHub Issues sync inaccessible, the call stops and returns gitHub.lostRepositoryNames. Review that list, then repeat with confirmReplace set to true to accept the change. GitHub Enterprise Cloud connections require the corresponding workspace plan feature.
- Call: `mutation integrationGithubConnect`, effect: write
- Body: `IntegrationGithubConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--confirm-replace <value>` | no | Confirm replacing an existing installation after a prior call reported lostRepositoryNames. Defaults to false. |
| `--github-host <value>` | no | GitHub Enterprise Cloud hostname, such as acme.ghe.com, without a URL scheme or path. Omit for github.com. |
| `--code-access <value>` | no | Whether to connect the GitHub App with repository code access. Defaults to false. |
| `--code <value>` | no | The GitHub grant code that's exchanged for OAuth tokens. |
| `--installation-id <value>` | no | GitHub App installation ID as a positive integer string. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-github-import-connect [options]`

- What: Connects the GitHub Import App installation authorized by the supplied OAuth code. This creates the connection used to discover repositories for import; it does not import issues by itself.
- Call: `mutation integrationGithubImportConnect`, effect: write
- Body: `IntegrationGithubImportConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--code <value>` | no | The GitHub grant code that's exchanged for OAuth tokens. |
| `--installation-id <value>` | no | GitHub App installation ID as a positive integer string. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-github-import-refresh [options]`

- What: Queues a refresh of repositories and labels available to a GitHub import integration. Success confirms scheduling.
- Call: `mutation integrationGithubImportRefresh`, effect: write
- Body: `IntegrationGithubImportRefreshRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The id of the integration to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-github-remove-code-access [options]`

- What: Removes repository code access from a GitHub connection. Check action in the response: Done means the change is complete, while InstallBasicApp means you need to finish installing the basic GitHub App before setup is complete.
- Call: `mutation integrationGithubRemoveCodeAccess`, effect: write
- Body: `IntegrationGithubRemoveCodeAccessRequest`, required

| Flag | Required | What |
|---|---|---|
| `--integration-id <value>` | no | The ID of the integration to remove code access from. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-gitlab-connect [options]`

- What: Connects a GitLab instance after checking its access token. Configure the GitLab webhook with the returned webhookSecret after a successful response. Only one GitLab connection is allowed per workspace. Token or connectivity failures return success=false and diagnostic error fields instead of creating a connection.
- Call: `mutation integrationGitlabConnect`, effect: write
- Body: `IntegrationGitlabConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--access-token <value>` | no | GitLab access token for the instance being connected. Linear validates it before saving the connection and uses its reported scopes and expiry when available. |
| `--gitlab-url <value>` | no | Base URL of the GitLab instance, including its URL scheme. Linear uses this host for token validation and subsequent API requests. |
| `--validation-project-path <value>` | no | Optional path or numeric ID of a project to use for the setup health check. Set this when the GitLab tenant blocks non-project API endpoints. |
| `--readonly <value>` | no | Whether the access token is limited to a read-only scope. Used as a fallback when \`validationProjectPath\` is set and \`personal\_access\_tokens/self\` is unreachable. |
| `--expires-at <value>` | no | ISO timestamp when the access token expires. Used as a fallback when \`validationProjectPath\` is set and \`personal\_access\_tokens/self\` is unreachable. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-gitlab-rotate [options]`

- What: Rotates the GitLab token, revoking the previous token and saving its replacement.
- Call: `mutation integrationGitlabRotate`, effect: write
- Body: `IntegrationGitlabRotateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--integration-id <value>` | no | UUID of the GitLab integration. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-gitlab-test-connection [options]`

- What: Tests the stored access token against a self-hosted GitLab instance, using the validation project when one is configured. A successful check clears the connection's authentication and transient failure state. On failure, inspect success and the error fields for provider or proxy diagnostics. This mutation does not support the GitLab.com OAuth connection.
- Call: `mutation integrationGitlabTestConnection`, effect: write
- Body: `IntegrationGitlabTestConnectionRequest`, required

| Flag | Required | What |
|---|---|---|
| `--integration-id <value>` | no | The ID of the GitLab integration to test. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-gitlab-update-rotation-settings [options]`

- What: Enables or disables automatic self-rotation of the GitLab token.
- Call: `mutation integrationGitlabUpdateRotationSettings`, effect: write
- Body: `IntegrationGitlabUpdateRotationSettingsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--enabled <value>` | no | Whether Linear should automatically rotate the GitLab token. |
| `--integration-id <value>` | no | UUID of the GitLab integration. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-gitlab-update-token [options]`

- What: Replaces a GitLab integration's access token after validating the replacement against its existing host and validation project. The connection and webhook stay in place. Supply readonly and expiresAt when the instance cannot report that token information.
- Call: `mutation integrationGitlabUpdateToken`, effect: write
- Body: `IntegrationGitlabUpdateTokenRequest`, required

| Flag | Required | What |
|---|---|---|
| `--expires-at <value>` | no | The time at which the replacement token expires. Used when GitLab cannot return its expiry. |
| `--readonly <value>` | no | Whether the replacement token has read-only access. Required when GitLab cannot return its scopes. |
| `--access-token <value>` | no | Replacement GitLab access token. Validated before it replaces the current token. |
| `--integration-id <value>` | no | UUID of the GitLab integration. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-gong [options]`

- What: Connects Gong using an OAuth authorization code and its redirect URI. Requires the workspace's Gong integration plan feature and integration-creation permission. The workspace cannot already have an active Gong connection.
- Call: `mutation integrationGong`, effect: write
- Body: `IntegrationGongRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Gong OAuth redirect URI. |
| `--code <value>` | no | The Gong OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-google-sheets [options]`

- What: Connects Google Sheets using an OAuth grant that includes both access and refresh tokens. The workspace can have one active Google Sheets connection. This call saves the connection; use refreshGoogleSheetsData to request an export refresh.
- Call: `mutation integrationGoogleSheets`, effect: write
- Body: `IntegrationGoogleSheetsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--code <value>` | no | The Google OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-intercom [options]`

- What: Connects an Intercom workspace using an OAuth code and the redirect URI used during authorization. The workspace needs access to the support integration plan feature. Reconnecting the same Intercom workspace refreshes credentials and keeps its settings; disconnect first to switch to a different Intercom workspace. An Intercom workspace cannot be connected to another Linear workspace at the same time.
- Call: `mutation integrationIntercom`, effect: write
- Body: `IntegrationIntercomRequest`, required

| Flag | Required | What |
|---|---|---|
| `--domain-url <value>` | no | The Intercom domain URL to use for the integration. Defaults to app.intercom.com if not provided. |
| `--redirect-uri <value>` | no | The Intercom OAuth redirect URI. |
| `--code <value>` | no | The Intercom OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-intercom-delete`

- What: Uninstalls the Intercom connection and removes its Linear record. It also completes local cleanup when access was already revoked in Intercom. Calling this after the Linear connection has been removed returns an error.
- Call: `mutation integrationIntercomDelete`, effect: destructive
- Permission keys: `linear.delete`

## `linear api integration-intercom-settings-update [options]`

- What: \[DEPRECATED\] Updates settings on the Intercom integration.
- Call: `mutation integrationIntercomSettingsUpdate`, effect: write, deprecated
- Body: `IntegrationIntercomSettingsUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial Intercom integration settings object to update the integration settings with. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-jira-personal [options]`

- What: Links your Jira account to an existing workspace Jira integration. Supply either the OAuth authorization code for Jira Cloud or a personal access token for Jira Server. When the workspace has more than one possible Jira connection, supply workspaceIntegrationId to choose which one to link.
- Call: `mutation integrationJiraPersonal`, effect: write
- Body: `IntegrationJiraPersonalRequest`

| Flag | Required | What |
|---|---|---|
| `--workspace-integration-id <value>` | no | The workspace Jira integration to connect to. Required when the connection would otherwise be ambiguous. |
| `--code <value>` | no | The Jira OAuth code, when connecting using OAuth. |
| `--access-token <value>` | no | The Jira personal access token, when connecting using a PAT. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-loom`

- What: Enables Loom integration for the workspace.
- Call: `mutation integrationLoom`, effect: write, deprecated

## `linear api integration-microsoft-personal-connect [options]`

- What: Links your Microsoft account to Linear. Its tenant must already be connected through a workspace Microsoft Teams integration. Reconnecting the same account refreshes credentials when the existing personal connection has an authentication error; otherwise, disconnect the existing personal connection before linking another account.
- Call: `mutation integrationMicrosoftPersonalConnect`, effect: write
- Body: `IntegrationMicrosoftPersonalConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Microsoft OAuth redirect URI. |
| `--code <value>` | no | The Microsoft OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-microsoft-teams [options]`

- What: Connects the Microsoft tenant identified by the OAuth grant to this Linear workspace. An archived connection to the same tenant is restored. Multiple tenants require the corresponding plan feature, and a tenant cannot be actively connected to another Linear workspace. Personal Microsoft accounts are linked separately with integrationMicrosoftPersonalConnect.
- Call: `mutation integrationMicrosoftTeams`, effect: write
- Body: `IntegrationMicrosoftTeamsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Microsoft OAuth redirect URI. |
| `--code <value>` | no | The Microsoft OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-request [options]`

- What: Records interest in an integration that is not currently available. No authentication is required, and this does not create an integration or start an installation. Success means the request was accepted for analytics; it does not promise that the integration will be built.
- Call: `mutation integrationRequest`, effect: write
- Body: `IntegrationRequestRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Integration request details. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-salesforce [options]`

- What: Connects Salesforce using an OAuth grant and verifies that the authorizing user can access the Linear managed package, including its required license. Requires the workspace's enterprise integration plan feature. Reconnecting an active connection to the same subdomain refreshes credentials while keeping settings and templates; restoring an archived connection runs setup again. Disconnect first to switch to a different Salesforce subdomain.
- Call: `mutation integrationSalesforce`, effect: write
- Body: `IntegrationSalesforceRequest`, required

| Flag | Required | What |
|---|---|---|
| `--code <value>` | no | The Salesforce OAuth code. |
| `--subdomain <value>` | no | Salesforce installation subdomain. Use the subdomain alone, containing letters, numbers, and dashes, rather than a complete URL. |
| `--redirect-uri <value>` | no | The Salesforce OAuth redirect URI. |
| `--code-verifier <value>` | no | The PKCE code verifier matching the code\_challenge sent on authorization. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-sentry-connect [options]`

- What: Connects a Sentry installation by exchanging its grant code and confirming installation with Sentry. The workspace can have one active Sentry connection. The new connection initially enables completing linked Linear issues when Sentry issues are resolved and reopening them when Sentry issues are unresolved.
- Call: `mutation integrationSentryConnect`, effect: write
- Body: `IntegrationSentryConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--code <value>` | no | The Sentry grant code that's exchanged for OAuth tokens. |
| `--installation-id <value>` | no | The Sentry installationId to connect with. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack [options]`

- What: Connects a Slack workspace to the main Linear Slack app using an OAuth grant. Reconnecting an archived connection restores it with fresh credentials. Connecting multiple Slack workspaces requires the corresponding plan feature; the same Slack workspace cannot have two active connections or belong to another Linear workspace's connection.
- Call: `mutation integrationSlack`, effect: write
- Body: `IntegrationSlackRequest`, required

| Flag | Required | What |
|---|---|---|
| `--requested-scopes <value>` | no | The Slack OAuth scopes the client requested. Used to warn when Slack grants fewer scopes than requested. |
| `--should-use-v2-auth <value>` | no | \[DEPRECATED\] Whether or not v2 of Slack OAuth should be used. No longer used. |
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-asks [options]`

- What: Connects a Slack workspace to the Linear Asks app for issue intake. Requires a workspace plan with Asks access. An archived connection to the same Slack workspace is restored with fresh credentials. Multiple Slack workspaces require the corresponding plan feature, and each Slack workspace can be connected to Asks in only one Linear workspace.
- Call: `mutation integrationSlackAsks`, effect: write
- Body: `IntegrationSlackAsksRequest`, required

| Flag | Required | What |
|---|---|---|
| `--requested-scopes <value>` | no | The Slack OAuth scopes the client requested. Used to warn when Slack grants fewer scopes than requested. |
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-custom-view-notifications [options]`

- What: Connects the Slack channel selected during OAuth to a custom view and creates default notification settings if needed. You must be able to edit the view, and the view cannot already have this type of Slack connection. Check the response for remaining bot or workspace setup.
- Call: `mutation integrationSlackCustomViewNotifications`, effect: write
- Body: `IntegrationSlackCustomViewNotificationsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--custom-view-id <value>` | no | UUID of the Linear custom view whose notifications should be sent to the selected Slack channel. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-customer-channel-link [options]`

- What: Links a customer to a public or private Slack channel in a connected Asks workspace. Both the customer and channel must be unlinked.
- Call: `mutation integrationSlackCustomerChannelLink`, effect: write
- Body: `IntegrationSlackCustomerChannelLinkRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--customer-id <value>` | no | The customer to link the Slack channel with |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-import-emojis [options]`

- What: Queues an import of custom emoji from Slack using the OAuth grant. Success confirms scheduling.
- Call: `mutation integrationSlackImportEmojis`, effect: write
- Body: `IntegrationSlackImportEmojisRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-or-asks-update-slack-team-name [options]`

- What: Fetches the current Slack workspace name and updates the name stored on an active Slack or Asks integration. This refreshes Linear's display name; it does not rename the workspace in Slack. A valid integration token is required.
- Call: `mutation integrationSlackOrAsksUpdateSlackTeamName`, effect: write
- Body: `IntegrationSlackOrAsksUpdateSlackTeamNameRequest`, required

| Flag | Required | What |
|---|---|---|
| `--integration-id <value>` | no | The integration ID. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-org-project-updates-post [options]`

- What: Connects the Slack channel selected during OAuth to receive project updates from across the workspace. Requires integration-management permission. Check addBot and the nudge fields in the response for any remaining Slack setup.
- Call: `mutation integrationSlackOrgProjectUpdatesPost`, effect: write
- Body: `IntegrationSlackOrgProjectUpdatesPostRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-personal [options]`

- What: Links your Slack account for personal notifications and opens a direct message with the Linear app. The Slack workspace must already have a Slack or Asks connection. You can have one active personal Slack connection, and the same Slack account cannot be linked to another user in this Linear workspace. An archived connection owned by you can be restored.
- Call: `mutation integrationSlackPersonal`, effect: write
- Body: `IntegrationSlackPersonalRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-post [options]`

- What: Connects the Slack channel selected during OAuth to a Linear team and creates its default notification settings if needed. Requires permission to manage the team, and each team can have one such connection. Direct messages are not supported. Check addBot and the nudge fields in the response for any remaining Slack setup.
- Call: `mutation integrationSlackPost`, effect: write
- Body: `IntegrationSlackPostRequest`, required

| Flag | Required | What |
|---|---|---|
| `--should-use-v2-auth <value>` | no | \[DEPRECATED\] Whether or not v2 of Slack OAuth should be used. No longer used. |
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--team-id <value>` | no | UUID of the Linear team whose notifications should be sent to the selected Slack channel. This is not a Slack workspace or channel ID. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-slack-project-post [options]`

- What: Connects the Slack channel selected during OAuth to a project you can access. Choose notifications for project notifications or updates for project updates; each service can have one connection per project. The call also links the channel to the project and creates default notification settings if needed. Check the response for remaining bot or workspace setup.
- Call: `mutation integrationSlackProjectPost`, effect: write
- Body: `IntegrationSlackProjectPostRequest`, required

| Flag | Required | What |
|---|---|---|
| `--service <value>` | no | The service to enable once connected, either 'notifications' or 'updates'. |
| `--redirect-uri <value>` | no | The Slack OAuth redirect URI. |
| `--project-id <value>` | no | UUID of the Linear project whose notifications or updates should be sent to the selected Slack channel. |
| `--code <value>` | no | The Slack OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-template-create [options]`

- What: Makes an issue template available through Slack Asks, Slack, Intercom, Zendesk, or Salesforce. Slack Asks requires permission to manage Asks, a connected intake destination, and a team template; linking the template enables triage for that team. Other supported integrations require integration-management permission and accept up to ten templates. Private-team templates are supported only by Slack Asks.
- Call: `mutation integrationTemplateCreate`, effect: write
- Body: `IntegrationTemplateCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The template, integration, and optional external resource to link. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-template-delete [options]`

- What: Removes a template's link to an integration or intake destination. The template itself and the integration remain available. Requires permission to manage the Asks integration for Slack Asks, or integration-management permission for other services.
- Call: `mutation integrationTemplateDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IntegrationTemplateDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the template-integration link to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integration-zendesk [options]`

- What: Connects Zendesk using an OAuth grant and creates or selects the user that authors internal notes. Requires the workspace's support integration plan feature. Reconnecting the same subdomain refreshes credentials and keeps existing settings; an archived connection is restored. Disconnect the current integration before switching to a different Zendesk subdomain.
- Call: `mutation integrationZendesk`, effect: write
- Body: `IntegrationZendeskRequest`, required

| Flag | Required | What |
|---|---|---|
| `--subdomain <value>` | no | Zendesk subdomain, such as acme for acme.zendesk.com. Use letters, numbers, and dashes without a scheme or domain suffix. |
| `--code <value>` | no | The Zendesk OAuth authorization code. |
| `--scope <value>` | no | The Zendesk OAuth scopes. Required when connecting with \`code\`. |
| `--redirect-uri <value>` | no | The Zendesk OAuth redirect URI. Required when connecting with \`code\`. |
| `--bot-user-role <value>` | no | Role for the Zendesk bot user Linear creates: end-user or agent. Omit to retain the role on reconnect; new connections default to end-user. Ignored when botUserId selects an existing user. |
| `--bot-user-id <value>` | no | The Zendesk user ID to use as the author of internal notes instead of creating a bot user. Omit to keep the configured user on reconnect, or pass null to create a new bot user. |
| `--custom-api-url <value>` | no | Custom base URL for Zendesk API requests, such as a proxy in front of Zendesk. OAuth requests always use the standard subdomain URL. |
| `--access-token <value>` | no | Bearer token that authenticates API requests instead of a Zendesk OAuth token. Requires \`customApiUrl\`; no OAuth exchange is performed. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integrations-settings-create [options]`

- What: Creates notification preferences for a destination you can access, with edit permission required for custom views. Supply exactly one team, project, initiative, or view. Settings must not already exist for that destination and, for team settings, context view; use integrationsSettingsUpdate when they do. An app writing initiative preferences also needs initiative:write scope.
- Call: `mutation integrationsSettingsCreate`, effect: write
- Body: `IntegrationsSettingsCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The settings to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api integrations-settings-update [options]`

- What: Updates the event preferences on an existing integration settings record. Only supplied booleans change, and the destination stays the same. Custom-view settings require permission to edit the view; apps changing initiative settings need initiative:write scope. For older settings that combined update and comment notifications, the first edit preserves the previous comment preference independently.
- Call: `mutation integrationsSettingsUpdate`, effect: write
- Body: `IntegrationsSettingsUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A settings object to update the settings with. |
| `--id <value>` | no | The identifier of the settings to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-add-label [options]`

- What: Add a label without replacing the issue’s existing labels. The label must be available to the issue’s team.
- Call: `mutation issueAddLabel`, effect: write
- Body: `IssueAddLabelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--label-id <value>` | no | The identifier of the label to add. |
| `--id <value>` | no | The identifier of the issue to add the label to. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-archive [options]`

- What: Archives an issue and its sub-issues, keeping their data available for later restoration. Archived issues are excluded from normal issue lists. Pass trash only when you want the deletion grace period to apply instead.
- Call: `mutation issueArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IssueArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--trash <value>` | no | Whether to trash the issue and its sub-issues. |
| `--id <value>` | no | The identifier of the issue to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-batch-create [options]`

- What: Creates one to 50 issues in a single batch. If any creation fails, none of the issues in the batch are saved. Put parent inputs before their sub-issues and supply parent UUIDs to connect issues created in the same batch.
- Call: `mutation issueBatchCreate`, effect: write
- Body: `IssueBatchCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A list of issue objects to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-batch-update [options]`

- What: Applies the same update input to one to 50 issues. The batch runs as one transaction, so a failed update rolls back the other updates. Use the returned issues to read the resulting values.
- Call: `mutation issueBatchUpdate`, effect: write
- Body: `IssueBatchUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial issue object to update the issues with. |
| `--ids <value>` | no | One to 50 distinct issue UUIDs to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-create [options]`

- What: Creates an issue in the chosen team and returns it with its assigned identifier. You can supply a template to populate defaults and create any sub-issues it defines. Team settings and automation may set values such as the initial status, assignee, and cycle.
- Call: `mutation issueCreate`, effect: write
- Body: `IssueCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The issue object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-delete [options]`

- What: Moves an issue to the trash and trashes its unarchived sub-issues that you can access. Trashed issues can be restored during the 30-day grace period; permanentlyDelete skips that period and requires workspace entity-management permission.
- Call: `mutation issueDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IssueDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--permanently-delete <value>` | no | Delete immediately, skipping the 30-day grace period. Requires workspace permission to manage entities and access to the issue’s team. |
| `--id <value>` | no | The identifier of the issue to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-external-sync-disable [options]`

- What: Stop syncing an issue with the Jira or GitHub integration identified by its sync attachment.
- Call: `mutation issueExternalSyncDisable`, effect: write
- Body: `IssueExternalSyncDisableRequest`, required

| Flag | Required | What |
|---|---|---|
| `--attachment-id <value>` | no | The ID of the sync attachment to disable. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-create-asana [options]`

- What: Starts fetching Asana tasks into an asynchronous import job. Choose an existing destination team or a new team name. Configure the fetched data and call issueImportProcess to create Linear records.
- Call: `mutation issueImportCreateAsana`, effect: write
- Body: `IssueImportCreateAsanaRequest`, required

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | UUID of an existing destination team. Provide either teamId or teamName. |
| `--team-name <value>` | no | Name of a new destination team. Provide either teamId or teamName. |
| `--asana-token <value>` | no | Asana token to fetch information from the Asana API. |
| `--asana-team-name <value>` | no | Name of the source Asana team. |
| `--asana-project-names <value>` | no | Names of Asana projects in the team. When set, only tasks from these projects are imported. When empty, all projects are imported. |
| `--instant-process <value>` | no | Start creating Linear records after fetching source data, using default mappings. Defaults to false, allowing mappings to be reviewed first. |
| `--include-closed-issues <value>` | no | Include completed Asana tasks when fetching source data. |
| `--id <value>` | no | ID of issue import. If not provided it will be generated. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-create-clubhouse [options]`

- What: Starts fetching stories from Shortcut, whose legacy API name is clubhouse, into an asynchronous import job. Choose an existing destination team or a new team name. Configure the fetched data and call issueImportProcess to create Linear records.
- Call: `mutation issueImportCreateClubhouse`, effect: write
- Body: `IssueImportCreateClubhouseRequest`, required

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | UUID of an existing destination team. Provide either teamId or teamName. |
| `--team-name <value>` | no | Name of a new destination team. Provide either teamId or teamName. |
| `--clubhouse-token <value>` | no | Shortcut (formerly Clubhouse) token to fetch information from the Clubhouse API. |
| `--clubhouse-group-name <value>` | no | Name of the source Shortcut group. |
| `--instant-process <value>` | no | Start creating Linear records after fetching source data, using default mappings. Defaults to false, allowing mappings to be reviewed first. |
| `--include-closed-issues <value>` | no | Include completed Shortcut stories when fetching source data. |
| `--id <value>` | no | ID of issue import. If not provided it will be generated. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-create-csvjira [options]`

- What: Creates an asynchronous import from a Jira CSV already uploaded to the workspace’s import storage. Choose an existing destination team or a new team name. The response accepts the job; it does not mean the imported records are ready.
- Call: `mutation issueImportCreateCSVJira`, effect: write
- Body: `IssueImportCreateCSVJiraRequest`, required

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | UUID of an existing destination team. To create a team, omit this and provide teamName. |
| `--team-name <value>` | no | Name of a new destination team. Cannot be combined with teamId. |
| `--csv-url <value>` | no | Asset URL of a Jira CSV uploaded to this workspace’s import storage. |
| `--jira-hostname <value>` | no | Jira installation or cloud hostname. |
| `--jira-token <value>` | no | Jira personal access token to access Jira REST API. |
| `--jira-email <value>` | no | Jira user account email. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-create-github [options]`

- What: Starts fetching GitHub issues into an asynchronous import job. Choose an existing destination team or provide a name for a new one, and repositories the workspace can import from. After fetching and configuration, use issueImportProcess to create the Linear records. Requires workspace import permission.
- Call: `mutation issueImportCreateGithub`, effect: write
- Body: `IssueImportCreateGithubRequest`

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | UUID of an existing destination team. Provide either teamId or teamName. |
| `--team-name <value>` | no | Name of a new destination team. Provide either teamId or teamName. |
| `--github-repo-ids <value>` | no | Numeric GitHub repository IDs to import. The workspace must have import access to these repositories. |
| `--github-labels <value>` | no | GitHub label names to use when filtering the imported issues. Omit or send an empty list to import without a label filter. |
| `--instant-process <value>` | no | Start creating Linear records after fetching source data, using default mappings. Defaults to false, allowing mappings to be reviewed first. |
| `--include-closed-issues <value>` | no | Include closed GitHub issues when fetching source data. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-create-jira [options]`

- What: Starts fetching Jira issues into an asynchronous import job. Choose an existing destination team or a new team name and the source Jira project. After fetching and configuration, use issueImportProcess to create the Linear records. Requires workspace import permission.
- Call: `mutation issueImportCreateJira`, effect: write
- Body: `IssueImportCreateJiraRequest`, required

| Flag | Required | What |
|---|---|---|
| `--team-id <value>` | no | UUID of an existing destination team. Provide either teamId or teamName. |
| `--team-name <value>` | no | Name of a new destination team. Provide either teamId or teamName. |
| `--jira-token <value>` | no | Jira personal access token to access Jira REST API. |
| `--jira-project <value>` | no | Jira project key from which we will import data. |
| `--jira-email <value>` | no | Jira user account email. |
| `--jira-hostname <value>` | no | Jira installation or cloud hostname. |
| `--jql <value>` | no | Additional JQL conditions within jiraProject. The project restriction is always applied. |
| `--instant-process <value>` | no | Start creating Linear records after fetching source data, using default mappings. Defaults to false, allowing mappings to be reviewed first. |
| `--include-closed-issues <value>` | no | Include closed Jira issues when fetching source data. |
| `--id <value>` | no | ID of issue import. If not provided it will be generated. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-delete [options]`

- What: Schedules deletion of an import and the data it created, then returns the job with status deleting. This is available within 14 days for eligible imports awaiting configuration, completed imports, or failed imports. You must be the creator or an admin with the destination team’s deletion permission, and another import from the same service must not be processing.
- Call: `mutation issueImportDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IssueImportDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--issue-import-id <value>` | no | ID of the issue import to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-process [options]`

- What: Saves the supplied mappings and schedules creation of Linear records from the fetched source data. The import must be inProgress; otherwise the mappings are saved but success is false. A successful response means processing was accepted, not that it has finished. Linear-to-Linear migrations can only be managed from the Linear app.
- Call: `mutation issueImportProcess`, effect: write
- Body: `IssueImportProcessRequest`, required

| Flag | Required | What |
|---|---|---|
| `--mapping <value>` | no | The mapping configuration to use for processing the import. |
| `--issue-import-id <value>` | no | ID of the issue import which we're going to process. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-import-update [options]`

- What: Saves mapping choices without starting the import. For external-service imports, supply the full replacement mapping. Requires workspace import permission; Linear-to-Linear migrations can only be managed from the Linear app.
- Call: `mutation issueImportUpdate`, effect: write
- Body: `IssueImportUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the issue import to update. |
| `--id <value>` | no | The identifier of the issue import. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-label-create [options]`

- What: Create a workspace or team label. Requires permission to manage labels in its scope.
- Call: `mutation issueLabelCreate`, effect: write
- Body: `IssueLabelCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--replace-team-labels <value>` | no | Whether to replace all team-specific labels with the same name with this newly created workspace label (default: false). |
| `--input <value>` | no | The issue label to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-label-delete [options]`

- What: Deletes a label and its inherited copies. Assignments to that label are removed from issues in the background, so they may remain visible briefly after the mutation succeeds. Retire a label instead if you want to preserve its existing assignments.
- Call: `mutation issueLabelDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IssueLabelDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-label-restore [options]`

- What: Makes a retired label available for new assignments again. Existing issue assignments are preserved. Restoring a group also restores its child labels.
- Call: `mutation issueLabelRestore`, effect: write
- Body: `IssueLabelRestoreRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to restore. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-label-retire [options]`

- What: Retires a label so it cannot be newly assigned, while keeping it on issues that already use it. Retiring a group also retires its children. Use issueLabelRestore to make the label available again.
- Call: `mutation issueLabelRetire`, effect: write
- Body: `IssueLabelRetireRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to retire. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-label-update [options]`

- What: Update a label. Requires permission to manage labels in its scope; inherited labels must be edited at their source.
- Call: `mutation issueLabelUpdate`, effect: write
- Body: `IssueLabelUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--replace-team-labels <value>` | no | Whether to replace all team-specific labels with the same name with this updated workspace label (default: false). |
| `--input <value>` | no | A partial label object to update. |
| `--id <value>` | no | The identifier of the label to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-relation-create [options]`

- What: Creates a relationship between two issues, replacing any conflicting relation between the pair and reusing an identical one. A duplicate relation closes the source as a duplicate of the target and can move linked customer requests to the target. You must have access to both issues and any permissions required for the merge.
- Call: `mutation issueRelationCreate`, effect: write
- Body: `IssueRelationCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--override-created-at <value>` | no | Used by client undo operations. Should not be set directly. |
| `--input <value>` | no | The issue relation to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-relation-delete [options]`

- What: Removes a relation by its UUID. Removing a duplicate relation also runs the unmerge behavior, including moving customer requests back to the original issue when applicable.
- Call: `mutation issueRelationDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IssueRelationDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the issue relation to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-relation-update [options]`

- What: Changes a relation’s type or the issues it connects. Omitted fields are unchanged, and an issue cannot relate to itself. Changing to or from duplicate also applies the corresponding merge or unmerge behavior.
- Call: `mutation issueRelationUpdate`, effect: write
- Body: `IssueRelationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the issue relation to update. |
| `--id <value>` | no | The identifier of the issue relation to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-reminder [options]`

- What: Creates a reminder notification for you at reminderAt. The time must be in the future, and existing reminders for this issue are replaced. The payload returns success without an issue object.
- Call: `mutation issueReminder`, effect: write
- Body: `IssueReminderRequest`, required

| Flag | Required | What |
|---|---|---|
| `--reminder-at <value>` | no | Future time at which to deliver the reminder notification. |
| `--id <value>` | no | The identifier of the issue to add a reminder for. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-remove-label [options]`

- What: Remove one label while keeping the issue’s other labels.
- Call: `mutation issueRemoveLabel`, effect: write
- Body: `IssueRemoveLabelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--label-id <value>` | no | The identifier of the label to remove. |
| `--id <value>` | no | The identifier of the issue to remove the label from. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-share [options]`

- What: Shares an issue with a user who would not otherwise be able to access it. The viewer must have native access to the issue's full sub-issue tree and permission to share issues in the issue's team. Issues that inherit sharing from a parent issue cannot be shared directly.
- Call: `mutation issueShare`, effect: write
- Body: `IssueShareRequest`, required

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | no | The identifier of the user to share the issue with. |
| `--id <value>` | no | The identifier of the issue to share. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-subscribe [options]`

- What: Subscribes a user to issue updates. Omit both userId and userEmail to subscribe yourself, or provide one of them to choose another workspace user. Subscribing an existing subscriber leaves the subscription in place.
- Call: `mutation issueSubscribe`, effect: write
- Body: `IssueSubscribeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--user-email <value>` | no | Email of an active workspace user to subscribe. Cannot be combined with userId. |
| `--user-id <value>` | no | UUID of the user to subscribe. Cannot be combined with userEmail. |
| `--id <value>` | no | The identifier of the issue to subscribe to. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-to-release-create [options]`

- What: Associates an issue with a release and returns the link. The issue must be editable and both resources accessible; release management must be available in the workspace. If the association already exists, the mutation returns an error rather than reusing it.
- Call: `mutation issueToReleaseCreate`, effect: write
- Body: `IssueToReleaseCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the issueToRelease to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-to-release-delete [options]`

- What: Removes an issue-to-release association by the link’s UUID, keeping the issue and release. The issue must be editable and the release accessible. Returns an error when the link does not exist.
- Call: `mutation issueToReleaseDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `IssueToReleaseDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the issue-to-release association to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-to-release-delete-by-issue-and-release [options]`

- What: Removes the association between the specified issue and release, keeping both resources. The issue must be editable and the release accessible. Returns an error when the association does not exist.
- Call: `mutation issueToReleaseDeleteByIssueAndRelease`, effect: write
- Body: `IssueToReleaseDeleteByIssueAndReleaseRequest`, required

| Flag | Required | What |
|---|---|---|
| `--release-id <value>` | no | The identifier of the release. |
| `--issue-id <value>` | no | The identifier of the issue. Can be a UUID or issue identifier (e.g., 'LIN-123'). |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-unarchive [options]`

- What: Restores an archived issue and its sub-issues to normal issue lists. Automatic-archive markers are cleared, and a project association is removed if the project no longer includes the issue’s team.
- Call: `mutation issueUnarchive`, effect: write
- Body: `IssueUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the issue to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-unshare [options]`

- What: Stops sharing an issue with a user. The viewer must have native access to the issue's full sub-issue tree and permission to share issues in the issue's team. Issues that inherit sharing from a parent issue cannot be unshared directly.
- Call: `mutation issueUnshare`, effect: write
- Body: `IssueUnshareRequest`, required

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | no | The identifier of the user to remove from the issue share. |
| `--id <value>` | no | The identifier of the issue to stop sharing. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-unsubscribe [options]`

- What: Removes a user’s subscription to issue updates. Omit both userId and userEmail to unsubscribe yourself, or provide one of them to choose another workspace user.
- Call: `mutation issueUnsubscribe`, effect: write
- Body: `IssueUnsubscribeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--user-email <value>` | no | Email of an active workspace user to unsubscribe. Cannot be combined with userId. |
| `--user-id <value>` | no | UUID of the user to unsubscribe. Cannot be combined with userEmail. |
| `--id <value>` | no | The identifier of the issue to unsubscribe from. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api issue-update [options]`

- What: Updates an issue by UUID or human-readable identifier and returns its resulting values. Omitted fields keep their values; list inputs replace their existing lists unless an add/remove field is used. Changes can also trigger team workflow behavior, such as automatic cycle assignment.
- Call: `mutation issueUpdate`, effect: write
- Body: `IssueUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial issue object to update the issue with. |
| `--id <value>` | no | The identifier of the issue to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api jira-project-batch-migrate [options]`

- What: Imports or syncs up to 50 projects from one connected Jira site. When both are requested, sync starts after import. Projects are checked independently; retry failed projects only. Repeating an unchanged, running migration returns its existing records. Imports into one team run sequentially. Requires the \`admin\` scope, access to destination teams, and import permission when importing.
- Call: `mutation jiraProjectBatchMigrate`, effect: write
- Body: `JiraProjectBatchMigrateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The Jira projects to migrate. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api logout [options]`

- What: Signs out the current session and clears authentication cookies. If the token has no session ID, signs out all sessions for the account.
- Call: `mutation logout`, effect: write
- Body: `LogoutRequest`

| Flag | Required | What |
|---|---|---|
| `--reason <value>` | no | Optional reason recorded with the sign-out event. It does not change which sessions are revoked. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api logout-all-sessions [options]`

- What: Signs out all sessions for the account, including the current session, and clears authentication cookies.
- Call: `mutation logoutAllSessions`, effect: write
- Body: `LogoutAllSessionsRequest`

| Flag | Required | What |
|---|---|---|
| `--reason <value>` | no | Optional reason recorded with the sign-out event. It does not change which sessions are revoked. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api logout-other-sessions [options]`

- What: Signs out every other session for the authenticated account while keeping the current session active.
- Call: `mutation logoutOtherSessions`, effect: write
- Body: `LogoutOtherSessionsRequest`

| Flag | Required | What |
|---|---|---|
| `--reason <value>` | no | Optional reason recorded with the sign-out event. It does not change which sessions are revoked. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api logout-session [options]`

- What: Revokes one sign-in session belonging to the authenticated account. Use an ID returned by authenticationSessions; it may be the current session or another device's session. Requires session JWT authentication.
- Call: `mutation logoutSession`, effect: write
- Body: `LogoutSessionRequest`, required

| Flag | Required | What |
|---|---|---|
| `--session-id <value>` | no | ID of the session to logout. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-archive [options]`

- What: Archives one of your notifications, removing it from the active inbox. Other notifications in the same group remain unchanged. Use notificationArchiveAll to archive the group.
- Call: `mutation notificationArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `NotificationArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The id of the notification to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-archive-all [options]`

- What: Archives the authenticated user’s active notifications for the selected entity or notification group.
- Call: `mutation notificationArchiveAll`, effect: write
- Body: `NotificationArchiveAllRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The entity or notification group whose notifications to change. Supply exactly one identifier. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-category-channel-subscription-update [options]`

- What: Subscribes to or unsubscribes from a specific notification category for a given notification channel. For example, subscribe to 'issueAssignment' notifications via the 'email' channel.
- Call: `mutation notificationCategoryChannelSubscriptionUpdate`, effect: write
- Body: `NotificationCategoryChannelSubscriptionUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | no | The notification channel in which to subscribe to or unsubscribe from the category |
| `--category <value>` | no | The notification category to subscribe to or unsubscribe from |
| `--subscribe <value>` | no | True if the user wants to subscribe, false if the user wants to unsubscribe |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-mark-read-all [options]`

- What: Marks the authenticated user’s active notifications for the selected entity or notification group as read.
- Call: `mutation notificationMarkReadAll`, effect: write
- Body: `NotificationMarkReadAllRequest`, required

| Flag | Required | What |
|---|---|---|
| `--read-at <value>` | no | The time when notification was marked as read. |
| `--input <value>` | no | The entity or notification group whose notifications to change. Supply exactly one identifier. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-mark-unread-all [options]`

- What: Marks the authenticated user’s active notifications for the selected entity or notification group as unread.
- Call: `mutation notificationMarkUnreadAll`, effect: write
- Body: `NotificationMarkUnreadAllRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The entity or notification group whose notifications to change. Supply exactly one identifier. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-snooze-all [options]`

- What: Snoozes the authenticated user’s active notifications for the selected entity or notification group.
- Call: `mutation notificationSnoozeAll`, effect: write
- Body: `NotificationSnoozeAllRequest`, required

| Flag | Required | What |
|---|---|---|
| `--snoozed-until-at <value>` | no | The time until a notification will be snoozed. After that it will appear in the inbox again. |
| `--input <value>` | no | The entity or notification group whose notifications to change. Supply exactly one identifier. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-subscription-create [options]`

- What: Subscribes the authenticated user to one target and its requested notification types. Rejects an existing subscription to the same target and view.
- Call: `mutation notificationSubscriptionCreate`, effect: write
- Body: `NotificationSubscriptionCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The subscription object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-subscription-delete [options]`

- What: Deletes a notification subscription reference.
- Call: `mutation notificationSubscriptionDelete`, effect: destructive, deprecated
- Permission keys: `linear.delete`
- Body: `NotificationSubscriptionDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the notification subscription reference to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-subscription-update [options]`

- What: Updates a subscription owned by the authenticated user. Use active: false to pause it without deleting its configuration, or replace notificationSubscriptionTypes to change the events you follow. Subscriptions to read-only projects cannot be changed.
- Call: `mutation notificationSubscriptionUpdate`, effect: write
- Body: `NotificationSubscriptionUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial notification subscription object to update the notification subscription with. |
| `--id <value>` | no | The identifier of the notification subscription to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-unarchive [options]`

- What: Restores one of your archived notifications. Its read and snooze states are preserved, so a snoozed notification may still be absent from the visible inbox.
- Call: `mutation notificationUnarchive`, effect: write
- Body: `NotificationUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The id of the notification to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-unsnooze-all [options]`

- What: Unsnoozes the authenticated user’s active notifications for the selected entity or notification group.
- Call: `mutation notificationUnsnoozeAll`, effect: write
- Body: `NotificationUnsnoozeAllRequest`, required

| Flag | Required | What |
|---|---|---|
| `--unsnoozed-at <value>` | no | The time when the notification was unsnoozed. |
| `--input <value>` | no | The entity or notification group whose notifications to change. Supply exactly one identifier. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api notification-update [options]`

- What: Updates one of the authenticated user’s notifications. Related notifications are unchanged.
- Call: `mutation notificationUpdate`, effect: write
- Body: `NotificationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial notification object to update the notification with. |
| `--id <value>` | no | The identifier of the notification to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api oauth-application-archive [options]`

- What: \[ALPHA\] Archives an OAuth application created by the calling OAuth application.
- Call: `mutation oauthApplicationArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `OauthApplicationArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the OAuth application to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api oauth-application-create [options]`

- What: \[ALPHA\] Creates an OAuth application private to the current workspace and managed by the calling OAuth application. The caller needs workspace API management permission. Save clientSecret and any webhookSecret from the first successful response. Retrying with the same idempotency key returns the existing unarchived application without updating it and with secrets omitted. Use the application’s id for later management operations and clientId for OAuth flows.
- Call: `mutation oauthApplicationCreate`, effect: write
- Body: `OauthApplicationCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The OAuth application object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api oauth-application-rotate-secret [options]`

- What: \[ALPHA\] Replaces the client secret for an application created by the caller and returns the new secret. Store it before discarding the response; it cannot be retrieved later. Tokens issued through client\_credentials are revoked, while tokens from the authorization-code flow remain valid. The caller must be able to manage the application’s credentials, including its private-team access, as well as have workspace API management permission.
- Call: `mutation oauthApplicationRotateSecret`, effect: write
- Body: `OauthApplicationRotateSecretRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the OAuth application for which to rotate the secret. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api oauth-application-rotate-webhook-secret [options]`

- What: \[ALPHA\] Rotates the webhook signing secret for an OAuth application created by the calling OAuth application.
- Call: `mutation oauthApplicationRotateWebhookSecret`, effect: write
- Body: `OauthApplicationRotateWebhookSecretRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the OAuth application for which to rotate the webhook secret. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api oauth-application-update [options]`

- What: \[ALPHA\] Updates an unarchived application created by the calling OAuth application in this workspace. Omitted fields keep their current values. Enabling client\_credentials or changing the webhook destination requires access to every private team available to the app, or workspace owner permission; an app with access to all private teams requires an owner. Workspace API management permission is required for every update.
- Call: `mutation oauthApplicationUpdate`, effect: write
- Body: `OauthApplicationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial OAuth application object to update. |
| `--id <value>` | no | The identifier of the OAuth application to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-cancel-delete`

- What: Cancels a scheduled workspace deletion while the deletion process still permits cancellation. Requires workspace-settings permission.
- Call: `mutation organizationCancelDelete`, effect: destructive
- Permission keys: `linear.delete`

## `linear api organization-delete [options]`

- What: Schedules deletion of the workspace and its data after validating the code from organizationDeleteChallenge. This does not finish the deletion during the request. Use organizationCancelDelete while cancellation is still available.
- Call: `mutation organizationDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `OrganizationDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Information required to delete the workspace. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-delete-challenge`

- What: Requests a deletion confirmation code for the workspace. The code is sent to the requesting user's email and must be used with the organizationDelete mutation to confirm deletion.
- Call: `mutation organizationDeleteChallenge`, effect: write

## `linear api organization-domain-delete [options]`

- What: Removes a domain configuration from the workspace and its authentication settings. Requires workspace-settings permission. Other domain configurations for the workspace are unchanged.
- Call: `mutation organizationDomainDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `OrganizationDomainDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the domain to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-invite-create [options]`

- What: Invites an email address to the workspace and sends an invitation email. Your role and workspace invitation settings must allow the requested role and teams. Guest invitations require teams; an existing user or unexpired invitation for the address causes an error.
- Call: `mutation organizationInviteCreate`, effect: write
- Body: `OrganizationInviteCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The organization invite object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-invite-delete [options]`

- What: Deletes (archives) a workspace invite, preventing it from being accepted.
- Call: `mutation organizationInviteDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `OrganizationInviteDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the organization invite to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-invite-update [options]`

- What: Replaces the teams an invitee will join on acceptance. Requires permission to manage invitations, and the selected teams must be valid for the invite’s role. This does not change the invitee’s email or role.
- Call: `mutation organizationInviteUpdate`, effect: write
- Body: `OrganizationInviteUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The updates to make to the organization invite object. |
| `--id <value>` | no | The identifier of the organization invite to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-start-trial`

- What: \[DEPRECATED\] Starts a trial for the workspace.
- Call: `mutation organizationStartTrial`, effect: write, deprecated

## `linear api organization-start-trial-for-plan [options]`

- What: Starts a trial for the workspace on the specified plan type. The workspace must not already be on a paid plan or in an active trial.
- Call: `mutation organizationStartTrialForPlan`, effect: write
- Body: `OrganizationStartTrialForPlanRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Plan details for trial |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api organization-update [options]`

- What: Updates the workspace associated with your credentials. Omitted fields keep their current values. Most changes require workspace-settings permission; project and initiative reminder schedules require schedule-management permission. Some settings also depend on the workspace’s plan.
- Call: `mutation organizationUpdate`, effect: write
- Body: `OrganizationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial workspace object to update the workspace with. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-add-label [options]`

- What: Adds a project label while keeping the project’s other labels. The label must be available to the project; label-group and team-scoping rules still apply.
- Call: `mutation projectAddLabel`, effect: write
- Body: `ProjectAddLabelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--label-id <value>` | no | The identifier of the label to add. |
| `--id <value>` | no | The identifier of the project to add the label to. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-archive [options]`

- What: Archives a project.
- Call: `mutation projectArchive`, effect: destructive, deprecated
- Permission keys: `linear.delete`
- Body: `ProjectArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--trash <value>` | no | Whether to trash the project. |
| `--id <value>` | no | The identifier of the project to archive. Also the identifier from the URL is accepted. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-create [options]`

- What: Creates a project in the supplied teams. You can apply a project template to fill in defaults and create its milestones, initial issues, and initiative associations. The new project must have at least one accessible team.
- Call: `mutation projectCreate`, effect: write
- Body: `ProjectCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--ai-conversation-id <value>` | no | \[Internal\] The identifier of the project draft conversation to attach to this project. |
| `--project-draft-id <value>` | no | \[Internal\] The identifier of the project draft that produced this project. |
| `--slack-channel-name <value>` | no | The full name for the Slack channel to create (including prefix). When provided, a Slack channel will be created and connected to the project. |
| `--input <value>` | no | The project properties to set on the new project. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-delete [options]`

- What: Moves a project to the trash. This archives the project rather than immediately deleting it permanently. You can restore it with projectUnarchive while it remains available in the trash.
- Call: `mutation projectDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ProjectDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-external-sync-disable [options]`

- What: Disables external sync on a project.
- Call: `mutation projectExternalSyncDisable`, effect: write
- Body: `ProjectExternalSyncDisableRequest`, required

| Flag | Required | What |
|---|---|---|
| `--sync-source <value>` | no | The source of the external sync to disable. |
| `--project-id <value>` | no | The ID of the project to disable external sync for. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-label-create [options]`

- What: Creates a label or label group for projects. Workspace labels require workspace label-management permission; team labels require label-management permission in that team and a plan that supports team project labels. replaceTeamLabels can migrate matching labels into the new scope.
- Call: `mutation projectLabelCreate`, effect: write
- Body: `ProjectLabelCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--replace-team-labels <value>` | no | Whether to replace all team-specific labels with the same name with this newly created workspace label (default: false). |
| `--input <value>` | no | The project label to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-label-delete [options]`

- What: Deletes a project label, its children, and inherited copies, removing their assignments from projects.
- Call: `mutation projectLabelDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ProjectLabelDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-label-restore [options]`

- What: Restores a previously retired project label, making it available for use on new projects.
- Call: `mutation projectLabelRestore`, effect: write
- Body: `ProjectLabelRestoreRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to restore. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-label-retire [options]`

- What: Retires a project label. Retired labels remain on existing projects but cannot be applied to new ones.
- Call: `mutation projectLabelRetire`, effect: write
- Body: `ProjectLabelRetireRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the label to retire. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-label-update [options]`

- What: Updates the supplied project-label fields and propagates changes to inherited copies. Requires label-management permission for the label’s workspace or team. Update the source label rather than an inherited copy.
- Call: `mutation projectLabelUpdate`, effect: write
- Body: `ProjectLabelUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--replace-team-labels <value>` | no | Whether to replace all team-specific labels with the same name with this updated workspace label (default: false). |
| `--input <value>` | no | A partial label object to update. |
| `--id <value>` | no | The identifier of the label to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-milestone-create [options]`

- What: Creates a milestone in a project you can edit. Its name must be unique among the project’s active milestones. A milestone starts without issues; assign issues to it separately.
- Call: `mutation projectMilestoneCreate`, effect: write
- Body: `ProjectMilestoneCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The project milestone to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-milestone-delete [options]`

- What: Permanently deletes a milestone from a project you can edit. The issues are kept in the project, but their milestone association is removed.
- Call: `mutation projectMilestoneDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ProjectMilestoneDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project milestone to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-milestone-move [options]`

- What: Moves a milestone and its issues to another project, including archived issues. The caller must have access to every issue in the milestone, and the milestone and destination project must be writable. If an issue's team is not part of the destination project, provide newIssueTeamId or addIssueTeamToProject. The returned team snapshots can be passed to the undo inputs when moving the milestone back to its original project.
- Call: `mutation projectMilestoneMove`, effect: write
- Body: `ProjectMilestoneMoveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The project to move the milestone to, as well as any additional options need to make a successful move, or undo a previous move. |
| `--id <value>` | no | The identifier of the project milestone to move. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-milestone-update [options]`

- What: Updates a milestone in a project you can edit, including an archived milestone. Omitted fields keep their current values. Changing projectId moves the milestone and clears its links from issue drafts in the previous project.
- Call: `mutation projectMilestoneUpdate`, effect: write
- Body: `ProjectMilestoneUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial object to update the project milestone with. |
| `--id <value>` | no | The identifier of the project milestone to update. Also the identifier from the URL is accepted. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-relation-create [options]`

- What: Creates a dependency between two different projects using date or milestone anchors.
- Call: `mutation projectRelationCreate`, effect: write
- Body: `ProjectRelationCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The project relation to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-relation-delete [options]`

- What: Deletes the dependency without deleting either project or milestone.
- Call: `mutation projectRelationDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ProjectRelationDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project relation to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-relation-update [options]`

- What: Updates the supplied dependency fields and validates both project endpoints.
- Call: `mutation projectRelationUpdate`, effect: write
- Body: `ProjectRelationUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the project relation to update. |
| `--id <value>` | no | The identifier of the project relation to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-remove-label [options]`

- What: Removes a project label while keeping the project’s other labels. The label itself is not deleted.
- Call: `mutation projectRemoveLabel`, effect: write
- Body: `ProjectRemoveLabelRequest`, required

| Flag | Required | What |
|---|---|---|
| `--label-id <value>` | no | The identifier of the label to remove. |
| `--id <value>` | no | The identifier of the project to remove the label from. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-status-archive [options]`

- What: Archives a project status. The status must not have any active projects assigned to it and must not be the last status of its type.
- Call: `mutation projectStatusArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ProjectStatusArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project status to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-status-create [options]`

- What: Creates a new project status.
- Call: `mutation projectStatusCreate`, effect: write
- Body: `ProjectStatusCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The ProjectStatus object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-status-unarchive [options]`

- What: Unarchives a project status.
- Call: `mutation projectStatusUnarchive`, effect: write
- Body: `ProjectStatusUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project status to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-status-update [options]`

- What: Updates a project status.
- Call: `mutation projectStatusUpdate`, effect: write
- Body: `ProjectStatusUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial ProjectStatus object to update the ProjectStatus with. |
| `--id <value>` | no | The identifier of the project status to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-unarchive [options]`

- What: Restores an archived or trashed project. The operation checks the project quota of each associated team before restoring it.
- Call: `mutation projectUnarchive`, effect: write
- Body: `ProjectUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project to restore. Also the identifier from the URL is accepted. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-update [options]`

- What: Updates the supplied fields of a project you can edit. Omitted fields keep their current values. List inputs such as memberIds and labelIds replace the corresponding lists; see each input for clearing rules and team-access behavior.
- Call: `mutation projectUpdate`, effect: write
- Body: `ProjectUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial project object to update the project with. |
| `--id <value>` | no | The identifier of the project to update. Also the identifier from the URL is accepted. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-update-archive [options]`

- What: Archives an update and recalculates the project’s health from the remaining updates. You must be the author or have permission to manage workspace entities. Use projectUpdateUnarchive to restore it.
- Call: `mutation projectUpdateArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ProjectUpdateArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project update to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-update-create [options]`

- What: Publishes a status update for a project you can edit. The update records the current user as author, captures project progress, and refreshes the project’s health. Provide the message in input.body.
- Call: `mutation projectUpdateCreate`, effect: write
- Body: `ProjectUpdateCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Data for the project update to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-update-delete [options]`

- What: Archives a project update and recalculates project health. Use projectUpdateUnarchive to restore it.
- Call: `mutation projectUpdateDelete`, effect: destructive, deprecated
- Permission keys: `linear.delete`
- Body: `ProjectUpdateDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project update to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-update-unarchive [options]`

- What: Restores an archived update and recalculates the project’s health. The update must currently be archived, and you must be its author or have permission to manage workspace entities.
- Call: `mutation projectUpdateUnarchive`, effect: write
- Body: `ProjectUpdateUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the project update to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api project-update-update [options]`

- What: Edits an update’s message or health. You must be its author or have permission to manage workspace entities. Editing the latest update while it is less than one hour old also refreshes its progress snapshot.
- Call: `mutation projectUpdateUpdate`, effect: write
- Body: `ProjectUpdateUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the project update to update. |
| `--id <value>` | no | The identifier of the project update to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api push-subscription-create [options]`

- What: Registers a browser or device to receive push notifications for the authenticated user. If the same subscription data is already registered, returns that record; otherwise replaces the subscription associated with the current sign-in session. userId in the input is ignored. Successful registration does not guarantee notification delivery; use pushSubscriptionTest to request a test notification.
- Call: `mutation pushSubscriptionCreate`, effect: write
- Body: `PushSubscriptionCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The push subscription to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api push-subscription-delete [options]`

- What: Deletes a push subscription to stop sending notifications through it. Select success to confirm deletion. This operation does not populate entity, so selecting that field produces a GraphQL error.
- Call: `mutation pushSubscriptionDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `PushSubscriptionDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the push subscription to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api reaction-create [options]`

- What: Adds an emoji reaction as you to one issue, comment, or update. If you already used that emoji on the same resource, the existing reaction is returned. You must be allowed to comment on the target.
- Call: `mutation reactionCreate`, effect: write
- Body: `ReactionCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The reaction object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api reaction-delete [options]`

- What: Removes a reaction by its UUID and updates the target’s reaction summary. You must be its creator or have workspace permission to manage entities, and you must be allowed to comment on the target.
- Call: `mutation reactionDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReactionDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the reaction to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api refresh-google-sheets-data [options]`

- What: Queues a Google Sheets export refresh. Success confirms scheduling; the returned integration may still contain the previous export state.
- Call: `mutation refreshGoogleSheetsData`, effect: write
- Body: `RefreshGoogleSheetsDataRequest`, required

| Flag | Required | What |
|---|---|---|
| `--type <value>` | no | Export type: issue, project, or initiative. Defaults to issue. |
| `--id <value>` | no | The identifier of the Google Sheets integration to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-archive [options]`

- What: Archives a release.
- Call: `mutation releaseArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReleaseArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-complete [options]`

- What: Completes the release identified by pipeline and version, or the latest started release when version is omitted. Completing a scheduled release may move its open issues to the next release, according to the pipeline’s rollover setting.
- Call: `mutation releaseComplete`, effect: write
- Body: `ReleaseCompleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The input containing the pipeline ID and optional version. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-complete-by-access-key [options]`

- What: Marks a release as completed using an access key. If version is provided, completes that specific release; otherwise completes the most recent started release. The pipeline is inferred from the access key.
- Call: `mutation releaseCompleteByAccessKey`, effect: write
- Body: `ReleaseCompleteByAccessKeyRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The input containing the optional version. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-create [options]`

- What: Creates a new release in a pipeline. If no stage is specified, defaults to the first completed stage for continuous pipelines or the first started stage for scheduled pipelines.
- Call: `mutation releaseCreate`, effect: write
- Body: `ReleaseCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The release to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-delete [options]`

- What: Moves a release to trash for permanent deletion after the retention period. Use releaseUnarchive to restore it before deletion.
- Call: `mutation releaseDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReleaseDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-note-create [options]`

- What: Creates a note covering releases from one pipeline. Supply explicit release IDs or an inclusive range, plus an optional title and Markdown body. A scheduled pipeline’s note must cover exactly one release.
- Call: `mutation releaseNoteCreate`, effect: write
- Body: `ReleaseNoteCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The release note fields. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-note-delete [options]`

- What: Permanently deletes a release note and its body. The covered releases remain.
- Call: `mutation releaseNoteDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReleaseNoteDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release note to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-note-update [options]`

- What: Updates a release note’s title, body, or covered releases. Omitted fields remain unchanged, and a new release selection replaces the old one. The note stays in its original pipeline.
- Call: `mutation releaseNoteUpdate`, effect: write
- Body: `ReleaseNoteUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The fields to update. |
| `--id <value>` | no | The identifier of the release note to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-pipeline-archive [options]`

- What: Archives a pipeline and schedules archival of its releases. The release changes run in the background, so they may not be complete when this mutation returns. Requires workspace team-management permission or ownership of every associated team.
- Call: `mutation releasePipelineArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReleasePipelineArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release pipeline to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-pipeline-create [options]`

- What: Creates a release pipeline with default stages, subject to your workspace’s plan and quota. Requires workspace team-management permission or ownership of every team associated with the pipeline.
- Call: `mutation releasePipelineCreate`, effect: write
- Body: `ReleasePipelineCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The ReleasePipeline object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-pipeline-delete [options]`

- What: Moves a pipeline and its releases to the trash for permanent deletion after the retention period. Repeating the operation does not extend that period. Requires workspace team-management permission or ownership of every associated team.
- Call: `mutation releasePipelineDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReleasePipelineDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release pipeline to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-pipeline-unarchive [options]`

- What: Restores a pipeline and schedules restoration of its archived releases. Individually trashed releases are left in the trash. The release changes run in the background, and the same pipeline administration permissions apply.
- Call: `mutation releasePipelineUnarchive`, effect: write
- Body: `ReleasePipelineUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release pipeline to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-pipeline-update [options]`

- What: Updates an existing release pipeline. Supports updating name, slug, type, production flag, path patterns, and team associations. Private teams that the current user cannot access are preserved in the team list.
- Call: `mutation releasePipelineUpdate`, effect: write
- Body: `ReleasePipelineUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial ReleasePipeline object to update the ReleasePipeline with. |
| `--id <value>` | no | The identifier of the release pipeline to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-stage-archive [options]`

- What: Archives a release stage. Only started-type stages can be archived, and only if they have no active releases and at least one other stage of the same type remains. Cannot archive the last non-frozen started stage.
- Call: `mutation releaseStageArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ReleaseStageArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release stage to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-stage-create [options]`

- What: Creates a new release stage in a pipeline. Non-started stages must use default names and colors and are unique by type; creating a canonical duplicate returns the existing stage. Started stages can optionally be frozen, but at least one non-frozen started stage must remain.
- Call: `mutation releaseStageCreate`, effect: write
- Body: `ReleaseStageCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The ReleaseStage object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-stage-unarchive [options]`

- What: Unarchives a release stage.
- Call: `mutation releaseStageUnarchive`, effect: write
- Body: `ReleaseStageUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release stage to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-stage-update [options]`

- What: Updates an existing release stage. Only started-type stages can be edited. Supports updating name, color, position, and frozen status.
- Call: `mutation releaseStageUpdate`, effect: write
- Body: `ReleaseStageUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial ReleaseStage object to update the ReleaseStage with. |
| `--id <value>` | no | The identifier of the release stage to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-sync [options]`

- What: Associates issues found in issue or pull request references with a release. Continuous pipelines create completed releases and reuse an existing version only when its commit SHA matches. Scheduled pipelines accumulate issues in an open release or use the supplied version. Existing issue associations are kept unless explicitly reverted in a scheduled pipeline.
- Call: `mutation releaseSync`, effect: write
- Body: `ReleaseSyncRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The release data to sync. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-sync-by-access-key [options]`

- What: Syncs release data using an access key for CI/CD integration. The pipeline is automatically inferred from the access key's configured resources, so no pipeline ID is needed in the input.
- Call: `mutation releaseSyncByAccessKey`, effect: write
- Body: `ReleaseSyncByAccessKeyRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The release data to sync. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-unarchive [options]`

- What: Restores an archived or trashed release before it is permanently deleted. The release keeps its pipeline and saved issue associations.
- Call: `mutation releaseUnarchive`, effect: write
- Body: `ReleaseUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the release to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-update [options]`

- What: Updates a release by ID. Omitted fields remain unchanged. A release cannot move to another pipeline.
- Call: `mutation releaseUpdate`, effect: write
- Body: `ReleaseUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial Release object to update the Release with. |
| `--id <value>` | no | The identifier of the release to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-update-by-pipeline [options]`

- What: Updates a release by pipeline identifier. Finds the release by version, otherwise the latest started release or else the planned release with the earliest target date, and optionally transitions it to a new stage by name.
- Call: `mutation releaseUpdateByPipeline`, effect: write
- Body: `ReleaseUpdateByPipelineRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The input containing the pipeline ID, optional version, and optional stage name. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api release-update-by-pipeline-by-access-key [options]`

- What: Updates a release by pipeline using an access key.
- Call: `mutation releaseUpdateByPipelineByAccessKey`, effect: write
- Body: `ReleaseUpdateByPipelineByAccessKeyRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The input containing the optional version and optional stage name. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api resend-organization-invite [options]`

- What: Re-sends a workspace invitation email for the specified invite ID.
- Call: `mutation resendOrganizationInvite`, effect: write
- Body: `ResendOrganizationInviteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the organization invite to re-send. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api resend-organization-invite-by-email [options]`

- What: Re-sends a workspace invitation email to the specified email address, if an outstanding invite exists for that address.
- Call: `mutation resendOrganizationInviteByEmail`, effect: write
- Body: `ResendOrganizationInviteByEmailRequest`, required

| Flag | Required | What |
|---|---|---|
| `--email <value>` | no | The email address tied to the organization invite to re-send. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-archive [options]`

- What: No longer supported and returns an error. Use initiativeArchive.
- Call: `mutation roadmapArchive`, effect: destructive, deprecated
- Permission keys: `linear.delete`
- Body: `RoadmapArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the roadmap to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-create [options]`

- What: No longer supported and returns an error. Use initiativeCreate.
- Call: `mutation roadmapCreate`, effect: write, deprecated
- Body: `RoadmapCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the roadmap to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-delete [options]`

- What: No longer supported and returns an error. Use initiativeDelete.
- Call: `mutation roadmapDelete`, effect: destructive, deprecated
- Permission keys: `linear.delete`
- Body: `RoadmapDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the roadmap to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-to-project-create [options]`

- What: No longer supported and returns an error. Use initiativeToProjectCreate.
- Call: `mutation roadmapToProjectCreate`, effect: write
- Body: `RoadmapToProjectCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the roadmapToProject to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-to-project-delete [options]`

- What: No longer supported and returns an error. Use initiativeToProjectDelete.
- Call: `mutation roadmapToProjectDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `RoadmapToProjectDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the roadmapToProject to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-to-project-update [options]`

- What: No longer supported and returns an error. Use initiativeToProjectUpdate.
- Call: `mutation roadmapToProjectUpdate`, effect: write
- Body: `RoadmapToProjectUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the roadmapToProject to update. |
| `--id <value>` | no | The identifier of the roadmapToProject to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-unarchive [options]`

- What: No longer supported and returns an error. Use initiativeUnarchive.
- Call: `mutation roadmapUnarchive`, effect: write, deprecated
- Body: `RoadmapUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the roadmap to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api roadmap-update [options]`

- What: No longer supported and returns an error. Use initiativeUpdate.
- Call: `mutation roadmapUpdate`, effect: write, deprecated
- Body: `RoadmapUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the roadmap to update. |
| `--id <value>` | no | The identifier of the roadmap to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api saml-token-user-account-auth [options]`

- What: Completes SAML sign-in with the email and token issued by the SAML flow, then sets the authentication cookie. The response identifies workspace memberships and any workspaces that require a different sign-in method. Unlike email token sign-in, this operation does not require clientAuthCode.
- Call: `mutation samlTokenUserAccountAuth`, effect: write
- Body: `SamlTokenUserAccountAuthRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The data used for token authentication. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-create [options]`

- What: Creates a team with workflow states, labels, and other initial resources. You become a member and, for private teams or plans that support team owners, an owner. copySettingsFromTeamId copies settings and related resources from an existing team; copied settings take precedence over input values except an explicit private value.
- Call: `mutation teamCreate`, effect: write
- Body: `TeamCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--copy-settings-from-team-id <value>` | no | The team id to copy settings from, if any. |
| `--input <value>` | no | The team object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-cycles-delete [options]`

- What: Permanently deletes all cycles for a team and disables cycles. Issues are kept, but their cycle associations are removed. Requires permission to manage the team.
- Call: `mutation teamCyclesDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TeamCyclesDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the team, which cycles will be deleted. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-delete [options]`

- What: Archives a team and schedules permanent deletion after a 30-day grace period. You cannot delete the workspace’s final active team. Requires a workspace administrator or team owner; use teamUnarchive before deletion begins to restore it.
- Call: `mutation teamDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TeamDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the team to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-key-delete [options]`

- What: Deletes a previously used team key. The active team key (the team's current key) cannot be deleted.
- Call: `mutation teamKeyDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TeamKeyDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the team key to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-membership-create [options]`

- What: Adds a user to an active team after checking permission and membership limits. Regular workspace members also join ancestor teams. The operation fails if the user is already a member or if the team is archived, retired, or managed through SCIM.
- Call: `mutation teamMembershipCreate`, effect: write
- Body: `TeamMembershipCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The team membership object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-membership-delete [options]`

- What: Removes a user from a team after checking removal permissions and membership restrictions. Leaving cannot remove the user’s last active team, and SCIM-managed memberships must be managed through the identity provider. alsoLeaveParentTeams can extend the removal to parent teams.
- Call: `mutation teamMembershipDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TeamMembershipDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--also-leave-parent-teams <value>` | no | Whether to leave the parent teams. |
| `--id <value>` | no | The identifier of the team membership to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-membership-update [options]`

- What: Updates the team’s position in the member’s team list.
- Call: `mutation teamMembershipUpdate`, effect: write
- Body: `TeamMembershipUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial team membership object to update the team membership with. |
| `--id <value>` | no | The identifier of the team membership to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-unarchive [options]`

- What: Restores an archived team and cancels its scheduled deletion while the grace period still permits cancellation. Requires workspace team-management permission, access to the team, and capacity for another active team on the workspace’s plan.
- Call: `mutation teamUnarchive`, effect: write
- Body: `TeamUnarchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the team to unarchive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api team-update [options]`

- What: Updates the supplied team fields. Changes require the relevant team-management permissions.
- Call: `mutation teamUpdate`, effect: write
- Body: `TeamUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--mapping <value>` | no | \[INTERNAL\] Mapping of existing team entities to those inherited from the parent team |
| `--input <value>` | no | A partial team object to update the team with. |
| `--id <value>` | no | The identifier of the team to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api template-create [options]`

- What: Create a template. Requires permission to manage templates in the workspace, team, or release pipeline that owns it.
- Call: `mutation templateCreate`, effect: write
- Body: `TemplateCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The template object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api template-delete [options]`

- What: Deletes a template and its inherited copies. Requires permission to manage templates in its scope; inherited copies must be deleted at their source. Resources already created from the template remain.
- Call: `mutation templateDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TemplateDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the template to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api template-update [options]`

- What: Changes a template’s metadata, saved defaults, or team scope. Update an inherited template at its source, and supply the full templateData when replacing its configuration. Changing a template does not rewrite resources already created from it.
- Call: `mutation templateUpdate`, effect: write
- Body: `TemplateUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the template to update. |
| `--id <value>` | no | The identifier of the template. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api time-schedule-create [options]`

- What: Creates an API-managed on-call schedule in the workspace. Provide a name and the complete list of shifts, then reference the returned schedule ID from a triage responsibility to use it for a team. An OAuth-created schedule is owned by that application for later updates and deletion. Duplicate IDs or external IDs are rejected.
- Call: `mutation timeScheduleCreate`, effect: write
- Body: `TimeScheduleCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the time schedule to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api time-schedule-delete [options]`

- What: Deletes an API-managed schedule and replaces linked triage responsibilities with available fallback users. The same ownership and team-management requirements as timeScheduleUpdate apply. Integration-synced schedules cannot be deleted here.
- Call: `mutation timeScheduleDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TimeScheduleDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the time schedule to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api time-schedule-refresh-integration-schedule [options]`

- What: Requests a refresh of a schedule managed by an integration. The schedule must have an associated integration. Success means the refresh was queued; the returned timeSchedule may still contain its previous shifts. Query the schedule again to read the refreshed entries.
- Call: `mutation timeScheduleRefreshIntegrationSchedule`, effect: write
- Body: `TimeScheduleRefreshIntegrationScheduleRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the time schedule to refresh. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api time-schedule-update [options]`

- What: Updates an unarchived, API-managed schedule. Omitted fields remain unchanged; entries replaces every existing shift. OAuth callers can update only schedules created by the same application. Other callers need management permission for every team using the schedule, or workspace team management permission if no team uses it. Integration-synced schedules cannot be edited here.
- Call: `mutation timeScheduleUpdate`, effect: write
- Body: `TimeScheduleUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the time schedule to update. |
| `--id <value>` | no | The identifier of the time schedule to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api time-schedule-upsert-external [options]`

- What: Finds an unarchived schedule by its workspace-unique externalId and updates it, or creates one if none exists. For a new schedule, include name and the same externalId inside input; the lookup argument is not copied into input automatically. A supplied entries list replaces the old shifts. Email references without userId are matched to workspace users when possible; unmatched references remain external. The same ownership rules as timeScheduleUpdate apply to an existing schedule.
- Call: `mutation timeScheduleUpsertExternal`, effect: write
- Body: `TimeScheduleUpsertExternalRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the time schedule to insert or update. |
| `--external-id <value>` | no | Schedule identifier in the external service, unique within the workspace. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api track-anonymous-event [options]`

- What: Submits an anonymous $pageview or $pageleave analytics event, with optional properties and session correlation. Unsupported event names return success=false. A successful response means tracking accepted the event, not that analytics delivery has completed. Limited to 30 requests per hour.
- Call: `mutation trackAnonymousEvent`, effect: write
- Body: `TrackAnonymousEventRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | Event tracking details. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api triage-responsibility-create [options]`

- What: Creates the team’s triage responsibility using a manual user selection or an on-call schedule. The team must be writable, the workspace plan must support triage responsibility, and the caller needs team management permission. A team can have only one rule. Selecting an integration-managed schedule also queues a refresh of its shifts.
- Call: `mutation triageResponsibilityCreate`, effect: write
- Body: `TriageResponsibilityCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the triage responsibility to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api triage-responsibility-delete [options]`

- What: Deletes a triage responsibility.
- Call: `mutation triageResponsibilityDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `TriageResponsibilityDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the triage responsibility to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api triage-responsibility-update [options]`

- What: Updates the action or responsible users for a writable team’s existing rule. Changing to a manual selection clears its schedule, and changing to a schedule clears its manual selection. Omitted fields remain unchanged. Requires team management permission; selecting a different integration-managed schedule queues a refresh.
- Call: `mutation triageResponsibilityUpdate`, effect: write
- Body: `TriageResponsibilityUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the triage responsibility to update. |
| `--id <value>` | no | The identifier of the triage responsibility to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-change-role [options]`

- What: Changes the workspace role of a user. The requesting user must have a role equal to or higher than the target role. Requires workspace admin permissions.
- Call: `mutation userChangeRole`, effect: write
- Body: `UserChangeRoleRequest`, required

| Flag | Required | What |
|---|---|---|
| `--role <value>` | no | The new role for the user. |
| `--id <value>` | no | The identifier of the user |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-discord-connect [options]`

- What: Connects the Discord user to this Linear account via OAuth2.
- Call: `mutation userDiscordConnect`, effect: write
- Body: `UserDiscordConnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--redirect-uri <value>` | no | The Discord OAuth redirect URI. |
| `--code <value>` | no | The Discord OAuth code. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-external-user-disconnect [options]`

- What: Disconnects the external user from this Linear account.
- Call: `mutation userExternalUserDisconnect`, effect: write
- Body: `UserExternalUserDisconnectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--workspace-integration-id <value>` | no | The workspace Jira integration whose account mapping to remove. If omitted, removes all Jira mappings without a personal connection. |
| `--service <value>` | no | The external service to disconnect. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-flag-update [options]`

- What: Updates a specific user settings flag by performing an operation (e.g., increment or clear) on it.
- Call: `mutation userFlagUpdate`, effect: write
- Body: `UserFlagUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--operation <value>` | no | Flag operation to perform. |
| `--flag <value>` | no | Settings flag to increment. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-revoke-all-sessions [options]`

- What: Revokes all active sessions for a user, forcing them to re-authenticate. Can only be called by a workspace admin or owner.
- Call: `mutation userRevokeAllSessions`, effect: write
- Body: `UserRevokeAllSessionsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the user to logout all sessions of. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-revoke-session [options]`

- What: Revokes a specific authentication session for a user. The admin cannot revoke their own sessions with this mutation. Can only be called by a workspace admin or owner.
- Call: `mutation userRevokeSession`, effect: write
- Body: `UserRevokeSessionRequest`, required

| Flag | Required | What |
|---|---|---|
| `--session-id <value>` | no | The identifier of the session to revoke. |
| `--id <value>` | no | The identifier of the user whose session to revoke. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-settings-flags-reset [options]`

- What: Resets one or more of the user's setting flags. If no specific flags are provided, all flags are reset.
- Call: `mutation userSettingsFlagsReset`, effect: write
- Body: `UserSettingsFlagsResetRequest`

| Flag | Required | What |
|---|---|---|
| `--flags <value>` | no | The flags to reset. If not provided all flags will be reset. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-settings-update [options]`

- What: Updates the settings record identified by id. You must own that record or have permission to manage workspace entities. General settings and notification category or channel preferences merge with existing values. See notificationDeliveryPreferences for its schedule replacement and mobile-channel effects.
- Call: `mutation userSettingsUpdate`, effect: write
- Body: `UserSettingsUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial notification object to update the settings with. |
| `--id <value>` | no | The identifier of the userSettings to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-suspend [options]`

- What: Suspends a user, deactivating their account and revoking access to the workspace. The suspended user's sessions are invalidated. Can only be called by a workspace admin or owner.
- Call: `mutation userSuspend`, effect: write
- Body: `UserSuspendRequest`, required

| Flag | Required | What |
|---|---|---|
| `--force-bypass-scim-restrictions <value>` | no | \[INTERNAL\] Whether to bypass SCIM restrictions when suspending. Use with caution — this overrides identity provider management. |
| `--id <value>` | no | The identifier of the user to suspend. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-unlink-from-identity-provider [options]`

- What: Unlinks a guest user from their identity provider. Can only be called by an admin when SCIM is enabled.
- Call: `mutation userUnlinkFromIdentityProvider`, effect: write
- Body: `UserUnlinkFromIdentityProviderRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the guest user to unlink from their identity provider. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-unsuspend [options]`

- What: Re-activates a suspended user, restoring their access to the workspace. Can only be called by a workspace admin or owner.
- Call: `mutation userUnsuspend`, effect: write
- Body: `UserUnsuspendRequest`, required

| Flag | Required | What |
|---|---|---|
| `--force-bypass-scim-restrictions <value>` | no | \[INTERNAL\] Whether to bypass SCIM restrictions when unsuspending. Use with caution — this overrides identity provider management. |
| `--id <value>` | no | The identifier of the user to unsuspend. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api user-update [options]`

- What: Updates a user’s profile. Use the user UUID or me for your own account. Updating another user requires member-management permission; identity-provider rules may block name changes, and application accounts only accept name and displayName.
- Call: `mutation userUpdate`, effect: write
- Body: `UserUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial user object to update the user with. |
| `--id <value>` | no | The identifier of the user to update. Use \`me\` to reference currently authenticated user. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api view-preferences-create [options]`

- What: Saves display settings for a view and scope. Existing records that conflict with the supplied type, view type, and scope are deleted and replaced, so supply the settings you want to retain. Personal preferences are owned by the current user.
- Call: `mutation viewPreferencesCreate`, effect: write
- Body: `ViewPreferencesCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The ViewPreferences object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api view-preferences-delete [options]`

- What: Deletes a saved preferences record, allowing the view to use its fallback defaults. You can delete only your own user-type preferences. If the record is already absent, the mutation still succeeds.
- Call: `mutation viewPreferencesDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `ViewPreferencesDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the ViewPreferences to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api view-preferences-update [options]`

- What: Replaces the supplied settings objects on a saved preferences record. You can update only your own user-type preferences; changing workspace defaults for a custom view also requires permission to edit that view.
- Call: `mutation viewPreferencesUpdate`, effect: write
- Body: `ViewPreferencesUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the view preferences. |
| `--id <value>` | no | The identifier of the ViewPreferences object. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api webhook-create [options]`

- What: Creates a webhook subscription and returns its configuration, including the signing secret. Choose one team or all public teams, and provide a public HTTPS destination with the resource types you want to receive. The destination must not already be registered for the same team scope. Requires workspace API management permission; a team-specific webhook also requires that team’s management permission. AuditEntry subscriptions have separate audit log access requirements.
- Call: `mutation webhookCreate`, effect: write
- Body: `WebhookCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The webhook object to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api webhook-delete [options]`

- What: Deletes a webhook subscription and stops future deliveries.
- Call: `mutation webhookDelete`, effect: destructive
- Permission keys: `linear.delete`
- Body: `WebhookDeleteRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the Webhook to delete. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api webhook-rotate-secret [options]`

- What: Generates and returns a new HMAC-SHA256 signing secret for the webhook. Update your receiver to verify later deliveries with the returned key; the previous key is replaced rather than kept as a second active key. This changes webhook signatures, not the endpoint or subscribed event streams.
- Call: `mutation webhookRotateSecret`, effect: write
- Body: `WebhookRotateSecretRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the Webhook to rotate the secret for. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api webhook-update [options]`

- What: Updates an existing webhook without changing its team scope. Omitted properties remain unchanged, and resourceTypes replaces the complete list of event streams. Setting enabled to false pauses delivery while retaining the subscription. Changing secret changes the key your receiver must use for later deliveries. Requires workspace API management permission and access to the subscribed resource types.
- Call: `mutation webhookUpdate`, effect: write
- Body: `WebhookUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The properties of the Webhook. |
| `--id <value>` | no | The identifier of the Webhook. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api workflow-state-archive [options]`

- What: Archives an unused status so it is no longer available for new issues. First move or archive every active issue in that status. You must be able to manage the team, and cannot archive reserved or inherited statuses or the last active status of a type.
- Call: `mutation workflowStateArchive`, effect: destructive
- Permission keys: `linear.delete`
- Body: `WorkflowStateArchiveRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | no | The identifier of the state to archive. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api workflow-state-create [options]`

- What: Add an issue status to a team. Requires permission to manage the team; inherited workflows cannot be edited directly.
- Call: `mutation workflowStateCreate`, effect: write
- Body: `WorkflowStateCreateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | The state to create. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `linear api workflow-state-update [options]`

- What: Update a status’s name, color, description, or position. Requires permission to manage the team. Reserved and inherited statuses cannot be changed.
- Call: `mutation workflowStateUpdate`, effect: write
- Body: `WorkflowStateUpdateRequest`, required

| Flag | Required | What |
|---|---|---|
| `--input <value>` | no | A partial state object to update. |
| `--id <value>` | no | The identifier of the state to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
