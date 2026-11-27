# Slack access policy

An access policy limits which endpoints Slack connections may call through Maton. Slack doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/slack#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Slack: its 150 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create slack --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/api.test"},
    {"method": "POST", "path": "api/api.test"},
    {"method": "GET", "path": "api/auth.teams.list"},
    {"method": "POST", "path": "api/auth.teams.list"},
    {"method": "GET", "path": "api/auth.test"},
    {"method": "POST", "path": "api/auth.test"},
    {"method": "GET", "path": "api/conversations.history"},
    {"method": "POST", "path": "api/conversations.history"},
    {"method": "GET", "path": "api/conversations.info"},
    {"method": "POST", "path": "api/conversations.info"},
    {"method": "GET", "path": "api/conversations.list"},
    {"method": "POST", "path": "api/conversations.list"},
    {"method": "GET", "path": "api/conversations.listConnectInvites"},
    {"method": "POST", "path": "api/conversations.listConnectInvites"},
    {"method": "GET", "path": "api/conversations.members"},
    {"method": "POST", "path": "api/conversations.members"},
    {"method": "GET", "path": "api/conversations.replies"},
    {"method": "POST", "path": "api/conversations.replies"},
    {"method": "GET", "path": "api/conversations.requestSharedInvite.list"},
    {"method": "POST", "path": "api/conversations.requestSharedInvite.list"},
    {"method": "GET", "path": "api/chat.getPermalink"},
    {"method": "POST", "path": "api/chat.getPermalink"},
    {"method": "GET", "path": "api/chat.scheduledMessages.list"},
    {"method": "POST", "path": "api/chat.scheduledMessages.list"},
    {"method": "GET", "path": "api/migration.exchange"},
    {"method": "POST", "path": "api/migration.exchange"},
    {"method": "GET", "path": "api/openid.connect.userInfo"},
    {"method": "POST", "path": "api/openid.connect.userInfo"},
    {"method": "GET", "path": "api/users.conversations"},
    {"method": "POST", "path": "api/users.conversations"},
    {"method": "GET", "path": "api/users.discoverableContacts.lookup"},
    {"method": "POST", "path": "api/users.discoverableContacts.lookup"},
    {"method": "GET", "path": "api/users.getPresence"},
    {"method": "POST", "path": "api/users.getPresence"},
    {"method": "GET", "path": "api/users.identity"},
    {"method": "POST", "path": "api/users.identity"},
    {"method": "GET", "path": "api/users.info"},
    {"method": "POST", "path": "api/users.info"},
    {"method": "GET", "path": "api/users.list"},
    {"method": "POST", "path": "api/users.list"},
    {"method": "GET", "path": "api/users.lookupByEmail"},
    {"method": "POST", "path": "api/users.lookupByEmail"},
    {"method": "GET", "path": "api/users.profile.get"},
    {"method": "POST", "path": "api/users.profile.get"},
    {"method": "GET", "path": "api/usergroups.list"},
    {"method": "POST", "path": "api/usergroups.list"},
    {"method": "GET", "path": "api/usergroups.users.list"},
    {"method": "POST", "path": "api/usergroups.users.list"},
    {"method": "GET", "path": "api/files.info"},
    {"method": "POST", "path": "api/files.info"},
    {"method": "GET", "path": "api/files.list"},
    {"method": "POST", "path": "api/files.list"},
    {"method": "GET", "path": "api/files.remote.info"},
    {"method": "POST", "path": "api/files.remote.info"},
    {"method": "GET", "path": "api/files.remote.list"},
    {"method": "POST", "path": "api/files.remote.list"},
    {"method": "GET", "path": "api/reactions.get"},
    {"method": "POST", "path": "api/reactions.get"},
    {"method": "GET", "path": "api/reactions.list"},
    {"method": "POST", "path": "api/reactions.list"},
    {"method": "GET", "path": "api/pins.list"},
    {"method": "POST", "path": "api/pins.list"},
    {"method": "GET", "path": "api/stars.list"},
    {"method": "POST", "path": "api/stars.list"},
    {"method": "GET", "path": "api/bookmarks.list"},
    {"method": "POST", "path": "api/bookmarks.list"},
    {"method": "GET", "path": "api/search.all"},
    {"method": "POST", "path": "api/search.all"},
    {"method": "GET", "path": "api/search.files"},
    {"method": "POST", "path": "api/search.files"},
    {"method": "GET", "path": "api/search.messages"},
    {"method": "POST", "path": "api/search.messages"},
    {"method": "GET", "path": "api/assistant.search.context"},
    {"method": "POST", "path": "api/assistant.search.context"},
    {"method": "GET", "path": "api/assistant.search.info"},
    {"method": "POST", "path": "api/assistant.search.info"},
    {"method": "GET", "path": "api/reminders.info"},
    {"method": "POST", "path": "api/reminders.info"},
    {"method": "GET", "path": "api/reminders.list"},
    {"method": "POST", "path": "api/reminders.list"},
    {"method": "GET", "path": "api/dnd.info"},
    {"method": "POST", "path": "api/dnd.info"},
    {"method": "GET", "path": "api/dnd.teamInfo"},
    {"method": "POST", "path": "api/dnd.teamInfo"},
    {"method": "GET", "path": "api/team.accessLogs"},
    {"method": "POST", "path": "api/team.accessLogs"},
    {"method": "GET", "path": "api/team.billableInfo"},
    {"method": "POST", "path": "api/team.billableInfo"},
    {"method": "GET", "path": "api/team.billing.info"},
    {"method": "POST", "path": "api/team.billing.info"},
    {"method": "GET", "path": "api/team.externalTeams.list"},
    {"method": "POST", "path": "api/team.externalTeams.list"},
    {"method": "GET", "path": "api/team.info"},
    {"method": "POST", "path": "api/team.info"},
    {"method": "GET", "path": "api/team.integrationLogs"},
    {"method": "POST", "path": "api/team.integrationLogs"},
    {"method": "GET", "path": "api/team.preferences.list"},
    {"method": "POST", "path": "api/team.preferences.list"},
    {"method": "GET", "path": "api/team.profile.get"},
    {"method": "POST", "path": "api/team.profile.get"},
    {"method": "GET", "path": "api/emoji.list"},
    {"method": "POST", "path": "api/emoji.list"},
    {"method": "GET", "path": "api/bots.info"},
    {"method": "POST", "path": "api/bots.info"},
    {"method": "GET", "path": "api/canvases.getContent"},
    {"method": "POST", "path": "api/canvases.getContent"},
    {"method": "GET", "path": "api/canvases.sections.lookup"},
    {"method": "POST", "path": "api/canvases.sections.lookup"},
    {"method": "GET", "path": "api/slackLists.download.get"},
    {"method": "POST", "path": "api/slackLists.download.get"},
    {"method": "GET", "path": "api/slackLists.items.info"},
    {"method": "POST", "path": "api/slackLists.items.info"},
    {"method": "GET", "path": "api/slackLists.items.list"},
    {"method": "POST", "path": "api/slackLists.items.list"},
    {"method": "GET", "path": "api/calls.info"},
    {"method": "POST", "path": "api/calls.info"},
    {"method": "GET", "path": "api/blocks.validate"},
    {"method": "POST", "path": "api/blocks.validate"},
    {"method": "GET", "path": "api/workflows.featured.list"},
    {"method": "POST", "path": "api/workflows.featured.list"},
    {"method": "GET", "path": "api/workflows.triggers.permissions.list"},
    {"method": "POST", "path": "api/workflows.triggers.permissions.list"},
    {"method": "GET", "path": "api/functions.distributions.permissions.list"},
    {"method": "POST", "path": "api/functions.distributions.permissions.list"},
    {"method": "GET", "path": "api/functions.workflows.steps.list"},
    {"method": "POST", "path": "api/functions.workflows.steps.list"},
    {"method": "GET", "path": "api/apps.activities.list"},
    {"method": "POST", "path": "api/apps.activities.list"},
    {"method": "GET", "path": "api/apps.datastore.bulkGet"},
    {"method": "POST", "path": "api/apps.datastore.bulkGet"},
    {"method": "GET", "path": "api/apps.datastore.count"},
    {"method": "POST", "path": "api/apps.datastore.count"},
    {"method": "GET", "path": "api/apps.datastore.get"},
    {"method": "POST", "path": "api/apps.datastore.get"},
    {"method": "GET", "path": "api/apps.datastore.query"},
    {"method": "POST", "path": "api/apps.datastore.query"},
    {"method": "GET", "path": "api/apps.event.authorizations.list"},
    {"method": "POST", "path": "api/apps.event.authorizations.list"},
    {"method": "GET", "path": "api/apps.manifest.export"},
    {"method": "POST", "path": "api/apps.manifest.export"},
    {"method": "GET", "path": "api/apps.manifest.validate"},
    {"method": "POST", "path": "api/apps.manifest.validate"},
    {"method": "GET", "path": "api/agents.conversations.getCanvas"},
    {"method": "POST", "path": "api/agents.conversations.getCanvas"},
    {"method": "GET", "path": "api/agents.conversations.listViews"},
    {"method": "POST", "path": "api/agents.conversations.listViews"},
    {"method": "GET", "path": "api/slackbot.skills.info"},
    {"method": "POST", "path": "api/slackbot.skills.info"},
    {"method": "GET", "path": "api/slackbot.skills.list"},
    {"method": "POST", "path": "api/slackbot.skills.list"}
  ],
  "deny": []
}
```

## Endpoints

The Slack endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/api.test | read | auth | Checks API calling code. |
| POST | api/api.test | read | auth | Checks API calling code. |
| GET | api/auth.revoke | write | auth | Revokes the calling token, which breaks the connection. |
| POST | api/auth.revoke | write | auth | Revokes the calling token, which breaks the connection. |
| GET | api/auth.teams.list | read | auth | Obtain a full list of workspaces your org-wide app has been approved for. |
| POST | api/auth.teams.list | read | auth | Obtain a full list of workspaces your org-wide app has been approved for. |
| GET | api/auth.test | read | auth | Checks authentication & identity. |
| POST | api/auth.test | read | auth | Checks authentication & identity. |
| GET | api/conversations.acceptSharedInvite | write | conversations | Accepts an invitation to a Slack Connect channel. |
| POST | api/conversations.acceptSharedInvite | write | conversations | Accepts an invitation to a Slack Connect channel. |
| GET | api/conversations.approveSharedInvite | write | conversations | Approves an invitation to a Slack Connect channel. |
| POST | api/conversations.approveSharedInvite | write | conversations | Approves an invitation to a Slack Connect channel. |
| GET | api/conversations.archive | write | conversations | Archives a conversation. |
| POST | api/conversations.archive | write | conversations | Archives a conversation. |
| GET | api/conversations.canvases.create | write | conversations | Create a channel canvas for a channel. |
| POST | api/conversations.canvases.create | write | conversations | Create a channel canvas for a channel. |
| GET | api/conversations.close | write | conversations | Closes a direct message or multi-person direct message. |
| POST | api/conversations.close | write | conversations | Closes a direct message or multi-person direct message. |
| GET | api/conversations.create | write | conversations | Initiates a public or private channel-based conversation. |
| POST | api/conversations.create | write | conversations | Initiates a public or private channel-based conversation. |
| GET | api/conversations.declineSharedInvite | write | conversations | Declines a Slack Connect channel invite. |
| POST | api/conversations.declineSharedInvite | write | conversations | Declines a Slack Connect channel invite. |
| GET | api/conversations.externalInvitePermissions.set | write | conversations | Changes a Slack Connect channel's permissions between post-only and post-and-invite. |
| POST | api/conversations.externalInvitePermissions.set | write | conversations | Changes a Slack Connect channel's permissions between post-only and post-and-invite. |
| GET | api/conversations.history | read | conversations | Fetches a conversation's history of messages and events. |
| POST | api/conversations.history | read | conversations | Fetches a conversation's history of messages and events. |
| GET | api/conversations.info | read | conversations | Retrieve information about a conversation. |
| POST | api/conversations.info | read | conversations | Retrieve information about a conversation. |
| GET | api/conversations.invite | write | conversations | Invites users to a channel. |
| POST | api/conversations.invite | write | conversations | Invites users to a channel. |
| GET | api/conversations.inviteShared | write | conversations | Sends an invitation to a Slack Connect channel. |
| POST | api/conversations.inviteShared | write | conversations | Sends an invitation to a Slack Connect channel. |
| GET | api/conversations.join | write | conversations | Joins an existing conversation. |
| POST | api/conversations.join | write | conversations | Joins an existing conversation. |
| GET | api/conversations.kick | write | conversations | Removes a user from a conversation. |
| POST | api/conversations.kick | write | conversations | Removes a user from a conversation. |
| GET | api/conversations.leave | write | conversations | Leaves a conversation. |
| POST | api/conversations.leave | write | conversations | Leaves a conversation. |
| GET | api/conversations.list | read | conversations | Lists all channels in a Slack team. |
| POST | api/conversations.list | read | conversations | Lists all channels in a Slack team. |
| GET | api/conversations.listConnectInvites | read | conversations | Lists Slack Connect invites generated or received that are not yet approved by all parties. |
| POST | api/conversations.listConnectInvites | read | conversations | Lists Slack Connect invites generated or received that are not yet approved by all parties. |
| GET | api/conversations.mark | write | conversations | Sets the read cursor in a channel, changing the user's unread state. |
| POST | api/conversations.mark | write | conversations | Sets the read cursor in a channel, changing the user's unread state. |
| GET | api/conversations.members | read | conversations | Retrieve members of a conversation. |
| POST | api/conversations.members | read | conversations | Retrieve members of a conversation. |
| GET | api/conversations.open | write | conversations | Opens or resumes a direct message or multi-person direct message; can create a new DM. |
| POST | api/conversations.open | write | conversations | Opens or resumes a direct message or multi-person direct message; can create a new DM. |
| GET | api/conversations.rename | write | conversations | Renames a conversation. |
| POST | api/conversations.rename | write | conversations | Renames a conversation. |
| GET | api/conversations.replies | read | conversations | Retrieve a thread of messages posted to a conversation. |
| POST | api/conversations.replies | read | conversations | Retrieve a thread of messages posted to a conversation. |
| GET | api/conversations.requestSharedInvite.approve | write | conversations | Approves a request to add an external user to a channel and sends them a Slack Connect invite. |
| POST | api/conversations.requestSharedInvite.approve | write | conversations | Approves a request to add an external user to a channel and sends them a Slack Connect invite. |
| GET | api/conversations.requestSharedInvite.deny | write | conversations | Denies a request to invite an external user to a channel. |
| POST | api/conversations.requestSharedInvite.deny | write | conversations | Denies a request to invite an external user to a channel. |
| GET | api/conversations.requestSharedInvite.list | read | conversations | Lists requests to add external users to channels with ability to filter. |
| POST | api/conversations.requestSharedInvite.list | read | conversations | Lists requests to add external users to channels with ability to filter. |
| GET | api/conversations.setPurpose | write | conversations | Sets the channel description. |
| POST | api/conversations.setPurpose | write | conversations | Sets the channel description. |
| GET | api/conversations.setTopic | write | conversations | Sets the topic for a conversation. |
| POST | api/conversations.setTopic | write | conversations | Sets the topic for a conversation. |
| GET | api/conversations.unarchive | write | conversations | Reverses conversation archival. |
| POST | api/conversations.unarchive | write | conversations | Reverses conversation archival. |
| GET | api/chat.appendStream | write | messages | Append text to an existing streaming conversation. |
| POST | api/chat.appendStream | write | messages | Append text to an existing streaming conversation. |
| GET | api/chat.delete | write | messages | Deletes a message. |
| POST | api/chat.delete | write | messages | Deletes a message. |
| GET | api/chat.deleteScheduledMessage | write | messages | Deletes a pending scheduled message from the queue. |
| POST | api/chat.deleteScheduledMessage | write | messages | Deletes a pending scheduled message from the queue. |
| GET | api/chat.getPermalink | read | messages | Retrieve a permalink URL for a specific extant message. |
| POST | api/chat.getPermalink | read | messages | Retrieve a permalink URL for a specific extant message. |
| GET | api/chat.meMessage | write | messages | Share a me message into a channel. |
| POST | api/chat.meMessage | write | messages | Share a me message into a channel. |
| GET | api/chat.postEphemeral | write | messages | Sends an ephemeral message to a user in a channel. |
| POST | api/chat.postEphemeral | write | messages | Sends an ephemeral message to a user in a channel. |
| GET | api/chat.postMessage | write | messages | Sends a message to a channel. |
| POST | api/chat.postMessage | write | messages | Sends a message to a channel. |
| GET | api/chat.scheduleMessage | write | messages | Schedules a message to be sent to a channel. |
| POST | api/chat.scheduleMessage | write | messages | Schedules a message to be sent to a channel. |
| GET | api/chat.scheduledMessages.list | read | messages | Returns a list of scheduled messages. |
| POST | api/chat.scheduledMessages.list | read | messages | Returns a list of scheduled messages. |
| GET | api/chat.startStream | write | messages | Start a new streaming conversation. |
| POST | api/chat.startStream | write | messages | Start a new streaming conversation. |
| GET | api/chat.stopStream | write | messages | Stop a streaming conversation. |
| POST | api/chat.stopStream | write | messages | Stop a streaming conversation. |
| GET | api/chat.unfurl | write | messages | Provide custom unfurl behavior for user-posted URLs. |
| POST | api/chat.unfurl | write | messages | Provide custom unfurl behavior for user-posted URLs. |
| GET | api/chat.update | write | messages | Updates a message. |
| POST | api/chat.update | write | messages | Updates a message. |
| GET | api/migration.exchange | read | users | For Enterprise organization workspaces, map local user IDs to global user IDs. |
| POST | api/migration.exchange | read | users | For Enterprise organization workspaces, map local user IDs to global user IDs. |
| GET | api/openid.connect.userInfo | read | users | Get the identity of a user who has authorized Sign in with Slack. |
| POST | api/openid.connect.userInfo | read | users | Get the identity of a user who has authorized Sign in with Slack. |
| GET | api/users.conversations | read | users | List conversations the calling user is a member of. |
| POST | api/users.conversations | read | users | List conversations the calling user is a member of. |
| GET | api/users.deletePhoto | write | users | Deletes the user's profile photo. |
| POST | api/users.deletePhoto | write | users | Deletes the user's profile photo. |
| GET | api/users.discoverableContacts.lookup | read | users | Look up an email address to see if someone is discoverable on Slack. |
| POST | api/users.discoverableContacts.lookup | read | users | Look up an email address to see if someone is discoverable on Slack. |
| GET | api/users.getPresence | read | users | Gets user presence information. |
| POST | api/users.getPresence | read | users | Gets user presence information. |
| GET | api/users.identity | read | users | Get a user's identity. |
| POST | api/users.identity | read | users | Get a user's identity. |
| GET | api/users.info | read | users | Gets information about a user. |
| POST | api/users.info | read | users | Gets information about a user. |
| GET | api/users.list | read | users | Lists all users in a Slack team. |
| POST | api/users.list | read | users | Lists all users in a Slack team. |
| GET | api/users.lookupByEmail | read | users | Find a user with an email address. |
| POST | api/users.lookupByEmail | read | users | Find a user with an email address. |
| GET | api/users.profile.get | read | users | Retrieve a user's profile information, including their custom status. |
| POST | api/users.profile.get | read | users | Retrieve a user's profile information, including their custom status. |
| GET | api/users.profile.set | write | users | Set a user's profile information, including custom status. |
| POST | api/users.profile.set | write | users | Set a user's profile information, including custom status. |
| GET | api/users.setActive | write | users | Marks the user as active (deprecated and non-functional). |
| POST | api/users.setActive | write | users | Marks the user as active (deprecated and non-functional). |
| GET | api/users.setPhoto | write | users | Set the user profile photo. |
| POST | api/users.setPhoto | write | users | Set the user profile photo. |
| GET | api/users.setPresence | write | users | Manually sets the user's presence to auto or away. |
| POST | api/users.setPresence | write | users | Manually sets the user's presence to auto or away. |
| GET | api/usergroups.create | write | usergroups | Create a User Group. |
| POST | api/usergroups.create | write | usergroups | Create a User Group. |
| GET | api/usergroups.disable | write | usergroups | Disable an existing User Group. |
| POST | api/usergroups.disable | write | usergroups | Disable an existing User Group. |
| GET | api/usergroups.enable | write | usergroups | Enable a User Group. |
| POST | api/usergroups.enable | write | usergroups | Enable a User Group. |
| GET | api/usergroups.list | read | usergroups | List all User Groups for a team. |
| POST | api/usergroups.list | read | usergroups | List all User Groups for a team. |
| GET | api/usergroups.update | write | usergroups | Update an existing User Group. |
| POST | api/usergroups.update | write | usergroups | Update an existing User Group. |
| GET | api/usergroups.users.list | read | usergroups | List all users in a User Group. |
| POST | api/usergroups.users.list | read | usergroups | List all users in a User Group. |
| GET | api/usergroups.users.update | write | usergroups | Update the list of users for a user group. |
| POST | api/usergroups.users.update | write | usergroups | Update the list of users for a user group. |
| GET | api/files.comments.delete | write | files | Deletes an existing comment on a file. |
| POST | api/files.comments.delete | write | files | Deletes an existing comment on a file. |
| GET | api/files.completeUploadExternal | write | files | Finishes an upload started with files.getUploadURLExternal. |
| POST | api/files.completeUploadExternal | write | files | Finishes an upload started with files.getUploadURLExternal. |
| GET | api/files.delete | write | files | Deletes a file. |
| POST | api/files.delete | write | files | Deletes a file. |
| GET | api/files.getUploadURLExternal | write | files | Starts a file upload and returns the URL to upload to; creates an upload session. |
| POST | api/files.getUploadURLExternal | write | files | Starts a file upload and returns the URL to upload to; creates an upload session. |
| GET | api/files.info | read | files | Gets information about a file. |
| POST | api/files.info | read | files | Gets information about a file. |
| GET | api/files.list | read | files | Lists files for a team, in a channel, or from a user, with filters. |
| POST | api/files.list | read | files | Lists files for a team, in a channel, or from a user, with filters. |
| GET | api/files.remote.add | write | files | Adds a file from a remote service. |
| POST | api/files.remote.add | write | files | Adds a file from a remote service. |
| GET | api/files.remote.info | read | files | Retrieve information about a remote file added to Slack. |
| POST | api/files.remote.info | read | files | Retrieve information about a remote file added to Slack. |
| GET | api/files.remote.list | read | files | Lists remote files added to Slack. |
| POST | api/files.remote.list | read | files | Lists remote files added to Slack. |
| GET | api/files.remote.remove | write | files | Remove a remote file. |
| POST | api/files.remote.remove | write | files | Remove a remote file. |
| GET | api/files.remote.share | write | files | Shares a remote file into a channel. |
| POST | api/files.remote.share | write | files | Shares a remote file into a channel. |
| GET | api/files.remote.update | write | files | Updates an existing remote file. |
| POST | api/files.remote.update | write | files | Updates an existing remote file. |
| GET | api/files.revokePublicURL | write | files | Revokes public/external sharing access for a file. |
| POST | api/files.revokePublicURL | write | files | Revokes public/external sharing access for a file. |
| GET | api/files.sharedPublicURL | write | files | Enables a file for public/external sharing. |
| POST | api/files.sharedPublicURL | write | files | Enables a file for public/external sharing. |
| GET | api/files.upload | write | files | Uploads or creates a file. |
| POST | api/files.upload | write | files | Uploads or creates a file. |
| GET | api/reactions.add | write | reactions | Adds a reaction to an item. |
| POST | api/reactions.add | write | reactions | Adds a reaction to an item. |
| GET | api/reactions.get | read | reactions | Gets reactions for an item. |
| POST | api/reactions.get | read | reactions | Gets reactions for an item. |
| GET | api/reactions.list | read | reactions | Lists reactions made by a user. |
| POST | api/reactions.list | read | reactions | Lists reactions made by a user. |
| GET | api/reactions.remove | write | reactions | Removes a reaction from an item. |
| POST | api/reactions.remove | write | reactions | Removes a reaction from an item. |
| GET | api/pins.add | write | pins | Pins an item to a channel. |
| POST | api/pins.add | write | pins | Pins an item to a channel. |
| GET | api/pins.list | read | pins | Lists items pinned to a channel. |
| POST | api/pins.list | read | pins | Lists items pinned to a channel. |
| GET | api/pins.remove | write | pins | Un-pins an item from a channel. |
| POST | api/pins.remove | write | pins | Un-pins an item from a channel. |
| GET | api/stars.add | write | stars | Save an item for later. Formerly known as adding a star. |
| POST | api/stars.add | write | stars | Save an item for later. Formerly known as adding a star. |
| GET | api/stars.list | read | stars | Lists the user's saved items, formerly known as stars. |
| POST | api/stars.list | read | stars | Lists the user's saved items, formerly known as stars. |
| GET | api/stars.remove | write | stars | Removes a saved item (star) from an item. |
| POST | api/stars.remove | write | stars | Removes a saved item (star) from an item. |
| GET | api/bookmarks.add | write | bookmarks | Add bookmark to a channel. |
| POST | api/bookmarks.add | write | bookmarks | Add bookmark to a channel. |
| GET | api/bookmarks.edit | write | bookmarks | Edit bookmark. |
| POST | api/bookmarks.edit | write | bookmarks | Edit bookmark. |
| GET | api/bookmarks.list | read | bookmarks | List bookmark for the channel. |
| POST | api/bookmarks.list | read | bookmarks | List bookmark for the channel. |
| GET | api/bookmarks.remove | write | bookmarks | Remove bookmark from the channel. |
| POST | api/bookmarks.remove | write | bookmarks | Remove bookmark from the channel. |
| GET | api/search.all | read | search | Searches for messages and files matching a query. |
| POST | api/search.all | read | search | Searches for messages and files matching a query. |
| GET | api/search.files | read | search | Searches for files matching a query. |
| POST | api/search.files | read | search | Searches for files matching a query. |
| GET | api/search.messages | read | search | Searches for messages matching a query. |
| POST | api/search.messages | read | search | Searches for messages matching a query. |
| GET | api/assistant.search.context | read | assistant | Searches messages, files, channels and users across your Slack organization. |
| POST | api/assistant.search.context | read | assistant | Searches messages, files, channels and users across your Slack organization. |
| GET | api/assistant.search.info | read | assistant | Returns search capabilities on a given team. |
| POST | api/assistant.search.info | read | assistant | Returns search capabilities on a given team. |
| GET | api/assistant.threads.setStatus | write | assistant | Set the status for an AI assistant thread. |
| POST | api/assistant.threads.setStatus | write | assistant | Set the status for an AI assistant thread. |
| GET | api/assistant.threads.setSuggestedPrompts | write | assistant | Set suggested prompts for the given assistant thread. |
| POST | api/assistant.threads.setSuggestedPrompts | write | assistant | Set suggested prompts for the given assistant thread. |
| GET | api/assistant.threads.setTitle | write | assistant | Set the title for the given assistant thread. |
| POST | api/assistant.threads.setTitle | write | assistant | Set the title for the given assistant thread. |
| GET | api/reminders.add | write | reminders | Creates a reminder. |
| POST | api/reminders.add | write | reminders | Creates a reminder. |
| GET | api/reminders.complete | write | reminders | Marks a reminder as complete. |
| POST | api/reminders.complete | write | reminders | Marks a reminder as complete. |
| GET | api/reminders.delete | write | reminders | Deletes a reminder. |
| POST | api/reminders.delete | write | reminders | Deletes a reminder. |
| GET | api/reminders.info | read | reminders | Gets information about a reminder. |
| POST | api/reminders.info | read | reminders | Gets information about a reminder. |
| GET | api/reminders.list | read | reminders | Lists all reminders created by or for a given user. |
| POST | api/reminders.list | read | reminders | Lists all reminders created by or for a given user. |
| GET | api/dnd.endDnd | write | dnd | Ends the current user's Do Not Disturb session immediately. |
| POST | api/dnd.endDnd | write | dnd | Ends the current user's Do Not Disturb session immediately. |
| GET | api/dnd.endSnooze | write | dnd | Ends the current user's snooze mode immediately. |
| POST | api/dnd.endSnooze | write | dnd | Ends the current user's snooze mode immediately. |
| GET | api/dnd.info | read | dnd | Retrieves a user's current Do Not Disturb status. |
| POST | api/dnd.info | read | dnd | Retrieves a user's current Do Not Disturb status. |
| GET | api/dnd.setSnooze | write | dnd | Turns on Do Not Disturb mode for the current user, or changes its duration. |
| POST | api/dnd.setSnooze | write | dnd | Turns on Do Not Disturb mode for the current user, or changes its duration. |
| GET | api/dnd.teamInfo | read | dnd | Retrieves the Do Not Disturb status for up to 50 users on a team. |
| POST | api/dnd.teamInfo | read | dnd | Retrieves the Do Not Disturb status for up to 50 users on a team. |
| GET | api/team.accessLogs | read | team | Gets the workspace's access logs (admin only). |
| POST | api/team.accessLogs | read | team | Gets the workspace's access logs (admin only). |
| GET | api/team.billableInfo | read | team | Gets billable-user information for the workspace (admin only). |
| POST | api/team.billableInfo | read | team | Gets billable-user information for the workspace (admin only). |
| GET | api/team.billing.info | read | team | Reads a workspace's billing plan information. |
| POST | api/team.billing.info | read | team | Reads a workspace's billing plan information. |
| GET | api/team.externalTeams.disconnect | write | team | Disconnect an external organization. |
| POST | api/team.externalTeams.disconnect | write | team | Disconnect an external organization. |
| GET | api/team.externalTeams.list | read | team | Returns a list of all the external teams connected and details about the connection. |
| POST | api/team.externalTeams.list | read | team | Returns a list of all the external teams connected and details about the connection. |
| GET | api/team.info | read | team | Gets information about the current team. |
| POST | api/team.info | read | team | Gets information about the current team. |
| GET | api/team.integrationLogs | read | team | Gets the workspace's integration logs (admin only). |
| POST | api/team.integrationLogs | read | team | Gets the workspace's integration logs (admin only). |
| GET | api/team.preferences.list | read | team | Retrieve a list of a workspace's team preferences. |
| POST | api/team.preferences.list | read | team | Retrieve a list of a workspace's team preferences. |
| GET | api/team.profile.get | read | team | Retrieve a team's profile. |
| POST | api/team.profile.get | read | team | Retrieve a team's profile. |
| GET | api/emoji.list | read | emoji | Lists custom emoji for a team. |
| POST | api/emoji.list | read | emoji | Lists custom emoji for a team. |
| GET | api/bots.info | read | bots | Gets information about a bot user. |
| POST | api/bots.info | read | bots | Gets information about a bot user. |
| GET | api/canvases.access.delete | write | canvases | Remove access to a canvas for specified entities. |
| POST | api/canvases.access.delete | write | canvases | Remove access to a canvas for specified entities. |
| GET | api/canvases.access.set | write | canvases | Sets the access level to a canvas for specified entities. |
| POST | api/canvases.access.set | write | canvases | Sets the access level to a canvas for specified entities. |
| GET | api/canvases.create | write | canvases | Create canvas for a user. |
| POST | api/canvases.create | write | canvases | Create canvas for a user. |
| GET | api/canvases.delete | write | canvases | Deletes a canvas. |
| POST | api/canvases.delete | write | canvases | Deletes a canvas. |
| GET | api/canvases.edit | write | canvases | Update an existing canvas. |
| POST | api/canvases.edit | write | canvases | Update an existing canvas. |
| GET | api/canvases.getContent | read | canvases | Get the content of a canvas as markdown (default) or HTML. |
| POST | api/canvases.getContent | read | canvases | Get the content of a canvas as markdown (default) or HTML. |
| GET | api/canvases.sections.lookup | read | canvases | Find sections matching the provided criteria. |
| POST | api/canvases.sections.lookup | read | canvases | Find sections matching the provided criteria. |
| GET | api/slackLists.access.delete | write | lists | Revoke access to a List for specified entities. |
| POST | api/slackLists.access.delete | write | lists | Revoke access to a List for specified entities. |
| GET | api/slackLists.access.set | write | lists | Set the access level to a List for specified entities. |
| POST | api/slackLists.access.set | write | lists | Set the access level to a List for specified entities. |
| GET | api/slackLists.create | write | lists | Create a List. |
| POST | api/slackLists.create | write | lists | Create a List. |
| GET | api/slackLists.download.get | read | lists | Gets the status and download URL of a List export job that was already started. |
| POST | api/slackLists.download.get | read | lists | Gets the status and download URL of a List export job that was already started. |
| GET | api/slackLists.download.start | write | lists | Starts a job that exports a List's contents; creates an export job. |
| POST | api/slackLists.download.start | write | lists | Starts a job that exports a List's contents; creates an export job. |
| GET | api/slackLists.items.create | write | lists | Add a new item to an existing List. |
| POST | api/slackLists.items.create | write | lists | Add a new item to an existing List. |
| GET | api/slackLists.items.delete | write | lists | Deletes an item from an existing List. |
| POST | api/slackLists.items.delete | write | lists | Deletes an item from an existing List. |
| GET | api/slackLists.items.deleteMultiple | write | lists | Deletes multiple items from an existing List. |
| POST | api/slackLists.items.deleteMultiple | write | lists | Deletes multiple items from an existing List. |
| GET | api/slackLists.items.info | read | lists | Get a row from a List. |
| POST | api/slackLists.items.info | read | lists | Get a row from a List. |
| GET | api/slackLists.items.list | read | lists | Get records from a List. |
| POST | api/slackLists.items.list | read | lists | Get records from a List. |
| GET | api/slackLists.items.update | write | lists | Updates cells in a List. |
| POST | api/slackLists.items.update | write | lists | Updates cells in a List. |
| GET | api/slackLists.update | write | lists | Update a List. |
| POST | api/slackLists.update | write | lists | Update a List. |
| GET | api/calls.add | write | calls | Registers a new Call. |
| POST | api/calls.add | write | calls | Registers a new Call. |
| GET | api/calls.end | write | calls | Ends a Call. |
| POST | api/calls.end | write | calls | Ends a Call. |
| GET | api/calls.info | read | calls | Returns information about a Call. |
| POST | api/calls.info | read | calls | Returns information about a Call. |
| GET | api/calls.participants.add | write | calls | Registers new participants added to a Call. |
| POST | api/calls.participants.add | write | calls | Registers new participants added to a Call. |
| GET | api/calls.participants.remove | write | calls | Registers participants removed from a Call. |
| POST | api/calls.participants.remove | write | calls | Registers participants removed from a Call. |
| GET | api/calls.update | write | calls | Updates information about a Call. |
| POST | api/calls.update | write | calls | Updates information about a Call. |
| GET | api/blocks.validate | read | views | Validates blocks, messages, and views Block Kit JSON payloads. |
| POST | api/blocks.validate | read | views | Validates blocks, messages, and views Block Kit JSON payloads. |
| GET | api/dialog.open | write | views | Open a dialog with a user. |
| POST | api/dialog.open | write | views | Open a dialog with a user. |
| GET | api/views.open | write | views | Open a view for a user. |
| POST | api/views.open | write | views | Open a view for a user. |
| GET | api/views.publish | write | views | Publish a static view for a User. |
| POST | api/views.publish | write | views | Publish a static view for a User. |
| GET | api/views.push | write | views | Push a view onto the stack of a root view. |
| POST | api/views.push | write | views | Push a view onto the stack of a root view. |
| GET | api/views.update | write | views | Update an existing view. |
| POST | api/views.update | write | views | Update an existing view. |
| GET | api/workflows.featured.add | write | workflows | Add featured workflows to a channel. |
| POST | api/workflows.featured.add | write | workflows | Add featured workflows to a channel. |
| GET | api/workflows.featured.list | read | workflows | List the featured workflows for specified channels. |
| POST | api/workflows.featured.list | read | workflows | List the featured workflows for specified channels. |
| GET | api/workflows.featured.remove | write | workflows | Remove featured workflows from a channel. |
| POST | api/workflows.featured.remove | write | workflows | Remove featured workflows from a channel. |
| GET | api/workflows.featured.set | write | workflows | Set featured workflows for a channel. |
| POST | api/workflows.featured.set | write | workflows | Set featured workflows for a channel. |
| GET | api/workflows.triggers.permissions.add | write | workflows | Allows users to run a trigger that has its permission type set to named_entities. |
| POST | api/workflows.triggers.permissions.add | write | workflows | Allows users to run a trigger that has its permission type set to named_entities. |
| GET | api/workflows.triggers.permissions.list | read | workflows | Returns a trigger's permission type and the entities that have been granted access. |
| POST | api/workflows.triggers.permissions.list | read | workflows | Returns a trigger's permission type and the entities that have been granted access. |
| GET | api/workflows.triggers.permissions.remove | write | workflows | Revoke an entity's access to a trigger that has its permission type set to named_entities. |
| POST | api/workflows.triggers.permissions.remove | write | workflows | Revoke an entity's access to a trigger that has its permission type set to named_entities. |
| GET | api/workflows.triggers.permissions.set | write | workflows | Set the permission type for who can run a trigger. |
| POST | api/workflows.triggers.permissions.set | write | workflows | Set the permission type for who can run a trigger. |
| GET | api/functions.completeError | write | functions | Signal that a function failed to complete. |
| POST | api/functions.completeError | write | functions | Signal that a function failed to complete. |
| GET | api/functions.completeSuccess | write | functions | Signal the successful completion of a function. |
| POST | api/functions.completeSuccess | write | functions | Signal the successful completion of a function. |
| GET | api/functions.distributions.permissions.add | write | functions | Grants users access to a custom function. |
| POST | api/functions.distributions.permissions.add | write | functions | Grants users access to a custom function. |
| GET | api/functions.distributions.permissions.list | read | functions | Lists the access type of a custom function and the users, teams or orgs that have access. |
| POST | api/functions.distributions.permissions.list | read | functions | Lists the access type of a custom function and the users, teams or orgs that have access. |
| GET | api/functions.distributions.permissions.remove | write | functions | Revokes user access to a custom function. |
| POST | api/functions.distributions.permissions.remove | write | functions | Revokes user access to a custom function. |
| GET | api/functions.distributions.permissions.set | write | functions | Sets the access type of a custom function and who is granted access. |
| POST | api/functions.distributions.permissions.set | write | functions | Sets the access type of a custom function and who is granted access. |
| GET | api/functions.workflows.steps.list | read | functions | List the steps of a specific function of a workflow's versions. |
| POST | api/functions.workflows.steps.list | read | functions | List the steps of a specific function of a workflow's versions. |
| GET | api/functions.workflows.steps.responses.export | write | functions | Exports a workflow's form responses; starts an export, so not a read. |
| POST | api/functions.workflows.steps.responses.export | write | functions | Exports a workflow's form responses; starts an export, so not a read. |
| GET | api/apps.activities.list | read | apps | Get logs for a specified app. |
| POST | api/apps.activities.list | read | apps | Get logs for a specified app. |
| GET | api/apps.auth.external.delete | write | apps | Delete external auth tokens only on the Slack side. |
| POST | api/apps.auth.external.delete | write | apps | Delete external auth tokens only on the Slack side. |
| GET | api/apps.auth.external.get | write | apps | Returns a stored external-provider access token; kept out of read because it exposes a credential. |
| POST | api/apps.auth.external.get | write | apps | Returns a stored external-provider access token; kept out of read because it exposes a credential. |
| GET | api/apps.connections.open | write | apps | Opens a Socket Mode session and returns its WebSocket URL; creates a live connection, so not a read. |
| POST | api/apps.connections.open | write | apps | Opens a Socket Mode session and returns its WebSocket URL; creates a live connection, so not a read. |
| GET | api/apps.datastore.bulkDelete | write | apps | Delete items from a datastore in bulk. |
| POST | api/apps.datastore.bulkDelete | write | apps | Delete items from a datastore in bulk. |
| GET | api/apps.datastore.bulkGet | read | apps | Get items from a datastore in bulk. |
| POST | api/apps.datastore.bulkGet | read | apps | Get items from a datastore in bulk. |
| GET | api/apps.datastore.bulkPut | write | apps | Creates or replaces existing items in bulk. |
| POST | api/apps.datastore.bulkPut | write | apps | Creates or replaces existing items in bulk. |
| GET | api/apps.datastore.count | read | apps | Count the number of items in a datastore that match a query. |
| POST | api/apps.datastore.count | read | apps | Count the number of items in a datastore that match a query. |
| GET | api/apps.datastore.delete | write | apps | Delete an item from a datastore. |
| POST | api/apps.datastore.delete | write | apps | Delete an item from a datastore. |
| GET | api/apps.datastore.get | read | apps | Get an item from a datastore. |
| POST | api/apps.datastore.get | read | apps | Get an item from a datastore. |
| GET | api/apps.datastore.put | write | apps | Creates a new item, or replaces an old item with a new item. |
| POST | api/apps.datastore.put | write | apps | Creates a new item, or replaces an old item with a new item. |
| GET | api/apps.datastore.query | read | apps | Query a datastore for items. |
| POST | api/apps.datastore.query | read | apps | Query a datastore for items. |
| GET | api/apps.datastore.update | write | apps | Edits an existing item's attributes, or adds a new item if it does not already exist. |
| POST | api/apps.datastore.update | write | apps | Edits an existing item's attributes, or adds a new item if it does not already exist. |
| GET | api/apps.event.authorizations.list | read | apps | Lists the app installations that a given event is visible to. |
| POST | api/apps.event.authorizations.list | read | apps | Lists the app installations that a given event is visible to. |
| GET | api/apps.icon.set | write | apps | Sets the app icon. |
| POST | api/apps.icon.set | write | apps | Sets the app icon. |
| GET | api/apps.managed.permissions.set | write | apps | Set who can interact with a managed app. |
| POST | api/apps.managed.permissions.set | write | apps | Set who can interact with a managed app. |
| GET | api/apps.manifest.create | write | apps | Create an app from an app manifest. |
| POST | api/apps.manifest.create | write | apps | Create an app from an app manifest. |
| GET | api/apps.manifest.delete | write | apps | Permanently deletes an app created through app manifests. |
| POST | api/apps.manifest.delete | write | apps | Permanently deletes an app created through app manifests. |
| GET | api/apps.manifest.export | read | apps | Export an app manifest from an existing app. |
| POST | api/apps.manifest.export | read | apps | Export an app manifest from an existing app. |
| GET | api/apps.manifest.update | write | apps | Update an app from an app manifest. |
| POST | api/apps.manifest.update | write | apps | Update an app from an app manifest. |
| GET | api/apps.manifest.validate | read | apps | Validate an app manifest. |
| POST | api/apps.manifest.validate | read | apps | Validate an app manifest. |
| GET | api/apps.uninstall | write | apps | Uninstalls your app from a workspace. |
| POST | api/apps.uninstall | write | apps | Uninstalls your app from a workspace. |
| GET | api/apps.user.connection.update | write | apps | Updates the connection status between a user and an app. |
| POST | api/apps.user.connection.update | write | apps | Updates the connection status between a user and an app. |
| GET | api/agents.conversations.archive | write | agents | Archives a code channel, optionally recording a summary message on the channel. |
| POST | api/agents.conversations.archive | write | agents | Archives a code channel, optionally recording a summary message on the channel. |
| GET | api/agents.conversations.create | write | agents | Creates a dedicated code channel for an agent session. |
| POST | api/agents.conversations.create | write | agents | Creates a dedicated code channel for an agent session. |
| GET | api/agents.conversations.getCanvas | read | agents | Fetches a canvas attached to an agent session channel in a single round-trip. |
| POST | api/agents.conversations.getCanvas | read | agents | Fetches a canvas attached to an agent session channel in a single round-trip. |
| GET | api/agents.conversations.listViews | read | agents | Lists the views currently attached to a code channel. |
| POST | api/agents.conversations.listViews | read | agents | Lists the views currently attached to a code channel. |
| GET | api/agents.conversations.removeView | write | agents | Removes a view from a code channel. |
| POST | api/agents.conversations.removeView | write | agents | Removes a view from a code channel. |
| GET | api/agents.conversations.setCanvasContent | write | agents | Replaces the full markdown content of a canvas attached to a code channel. |
| POST | api/agents.conversations.setCanvasContent | write | agents | Replaces the full markdown content of a canvas attached to a code channel. |
| GET | api/agents.conversations.setCommands | write | agents | Registers the set of slash commands your agent offers in a code channel. |
| POST | api/agents.conversations.setCommands | write | agents | Registers the set of slash commands your agent offers in a code channel. |
| GET | api/agents.conversations.setProperties | write | agents | Sets properties on a code channel: context bar items and external resource details. |
| POST | api/agents.conversations.setProperties | write | agents | Sets properties on a code channel: context bar items and external resource details. |
| GET | api/agents.conversations.setView | write | agents | Creates or updates a view (HTML, diff, Block Kit or canvas tab) in a code channel. |
| POST | api/agents.conversations.setView | write | agents | Creates or updates a view (HTML, diff, Block Kit or canvas tab) in a code channel. |
| GET | api/agents.sessions.rename | write | agents | Rename an agent session. |
| POST | api/agents.sessions.rename | write | agents | Rename an agent session. |
| GET | api/agents.sessions.setStatus | write | agents | Set an agent session's lifecycle status, creating the session if needed. |
| POST | api/agents.sessions.setStatus | write | agents | Set an agent session's lifecycle status, creating the session if needed. |
| GET | api/slackbot.skills.create | write | slackbot skills | Creates a skill from markdown instructions, or turns an existing canvas the caller owns into a skill. |
| POST | api/slackbot.skills.create | write | slackbot skills | Creates a skill from markdown instructions, or turns an existing canvas the caller owns into a skill. |
| GET | api/slackbot.skills.delete | write | slackbot skills | Deletes a Slackbot skill and its canvas, and removes it from every library, skill set, and the org catalog. |
| POST | api/slackbot.skills.delete | write | slackbot skills | Deletes a Slackbot skill and its canvas, and removes it from every library, skill set, and the org catalog. |
| GET | api/slackbot.skills.info | read | slackbot skills | Returns one Slackbot skill, including its instructions. |
| POST | api/slackbot.skills.info | read | slackbot skills | Returns one Slackbot skill, including its instructions. |
| GET | api/slackbot.skills.library.add | write | slackbot skills | Turns a skill on in the caller's Slackbot library. |
| POST | api/slackbot.skills.library.add | write | slackbot skills | Turns a skill on in the caller's Slackbot library. |
| GET | api/slackbot.skills.library.remove | write | slackbot skills | Turns a skill off in the caller's Slackbot library. |
| POST | api/slackbot.skills.library.remove | write | slackbot skills | Turns a skill off in the caller's Slackbot library. |
| GET | api/slackbot.skills.list | read | slackbot skills | Lists Slackbot skills from the caller's point of view. Instructions are not included. |
| POST | api/slackbot.skills.list | read | slackbot skills | Lists Slackbot skills from the caller's point of view. Instructions are not included. |
| GET | api/slackbot.skills.update | write | slackbot skills | Changes a Slackbot skill's instructions or metadata. |
| POST | api/slackbot.skills.update | write | slackbot skills | Changes a Slackbot skill's instructions or metadata. |
| GET | api/entity.acknowledgeCommentAction | write | work objects | Acknowledges a comment post, edit, or delete on a Work Object. |
| POST | api/entity.acknowledgeCommentAction | write | work objects | Acknowledges a comment post, edit, or delete on a Work Object. |
| GET | api/entity.presentComments | write | work objects | Sends per-user flexpane comment data for a Work Object to the client. |
| POST | api/entity.presentComments | write | work objects | Sends per-user flexpane comment data for a Work Object to the client. |
| GET | api/entity.presentDetails | write | work objects | Sends per-user flexpane metadata for a Work Object to the client. |
| POST | api/entity.presentDetails | write | work objects | Sends per-user flexpane metadata for a Work Object to the client. |
| GET | api/rtm.connect | write | rtm | Starts a Real Time Messaging session and returns its WebSocket URL; the session can send messages. |
| POST | api/rtm.connect | write | rtm | Starts a Real Time Messaging session and returns its WebSocket URL; the session can send messages. |
| GET | api/rtm.start | write | rtm | Deprecated: starts a Real Time Messaging session and returns its WebSocket URL; the session can send messages. |
| POST | api/rtm.start | write | rtm | Deprecated: starts a Real Time Messaging session and returns its WebSocket URL; the session can send messages. |
| GET | api/oauth.access | write | oauth | Exchanges an OAuth code for an access token (legacy); issues a credential. |
| POST | api/oauth.access | write | oauth | Exchanges an OAuth code for an access token (legacy); issues a credential. |
| GET | api/oauth.v2.access | write | oauth | Exchanges an OAuth code or refresh token for an access token; issues a credential. |
| POST | api/oauth.v2.access | write | oauth | Exchanges an OAuth code or refresh token for an access token; issues a credential. |
| GET | api/oauth.v2.beginShortTokenRotation | write | oauth | Begins rotating the secret on an API token with a short secret. |
| POST | api/oauth.v2.beginShortTokenRotation | write | oauth | Begins rotating the secret on an API token with a short secret. |
| GET | api/oauth.v2.completeShortTokenRotation | write | oauth | Finishes rotating the secret on an API token with a short secret. |
| POST | api/oauth.v2.completeShortTokenRotation | write | oauth | Finishes rotating the secret on an API token with a short secret. |
| GET | api/oauth.v2.exchange | write | oauth | Exchanges a legacy access token for an expiring token and refresh token; replaces the credential. |
| POST | api/oauth.v2.exchange | write | oauth | Exchanges a legacy access token for an expiring token and refresh token; replaces the credential. |
| GET | api/oauth.v2.user.access | write | oauth | Exchanges an OAuth code for a user access token; issues a credential. |
| POST | api/oauth.v2.user.access | write | oauth | Exchanges an OAuth code for a user access token; issues a credential. |
| GET | api/openid.connect.token | write | oauth | Exchanges an OAuth code for a Sign in with Slack token; issues a credential. |
| POST | api/openid.connect.token | write | oauth | Exchanges an OAuth code for a Sign in with Slack token; issues a credential. |
| GET | api/tooling.tokens.rotate | write | oauth | Exchanges a refresh token for a new app configuration token; replaces the credential. |
| POST | api/tooling.tokens.rotate | write | oauth | Exchanges a refresh token for a new app configuration token; replaces the credential. |
