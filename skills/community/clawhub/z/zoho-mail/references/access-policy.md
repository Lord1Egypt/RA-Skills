# Zoho Mail access policy

An access policy limits which endpoints Zoho Mail connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-mail#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho Mail: its 97 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-mail --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/accounts"},
    {"method": "GET", "path": "api/accounts/{id}"},
    {"method": "GET", "path": "api/organization/{id}/antispam/options"},
    {"method": "GET", "path": "api/links"},
    {"method": "GET", "path": "api/links/favorites"},
    {"method": "GET", "path": "api/links/groups"},
    {"method": "GET", "path": "api/links/groups/collections"},
    {"method": "GET", "path": "api/links/groups/{id}"},
    {"method": "GET", "path": "api/links/groups/{id}/collections"},
    {"method": "GET", "path": "api/links/groups/{id}/collections/{id}"},
    {"method": "GET", "path": "api/links/groups/{id}/trash"},
    {"method": "GET", "path": "api/links/groups/{id}/{id}"},
    {"method": "GET", "path": "api/links/me"},
    {"method": "GET", "path": "api/links/me/collections"},
    {"method": "GET", "path": "api/links/me/collections/{id}"},
    {"method": "GET", "path": "api/links/me/trash"},
    {"method": "GET", "path": "api/links/me/{id}"},
    {"method": "GET", "path": "api/organization/{id}/domains"},
    {"method": "GET", "path": "api/organization/{id}/domains/{id}"},
    {"method": "GET", "path": "api/accounts/{id}/folders"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}"},
    {"method": "GET", "path": "api/organization/{id}/groups"},
    {"method": "GET", "path": "api/organization/{id}/groups/{id}"},
    {"method": "GET", "path": "api/organization/{id}/groups/{id}/messages"},
    {"method": "GET", "path": "api/organization/{id}/groups/{id}/messages/{id}"},
    {"method": "GET", "path": "api/accounts/{id}/labels"},
    {"method": "GET", "path": "api/accounts/{id}/labels/{id}"},
    {"method": "GET", "path": "api/organization/{id}/accounts/reports/loginHistory"},
    {"method": "GET", "path": "api/organization/{id}/activity"},
    {"method": "GET", "path": "api/organization/{id}/smtplogs"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}/messages/{id}/attachmentinfo"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}/messages/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}/messages/{id}/content"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}/messages/{id}/details"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}/messages/{id}/header"},
    {"method": "GET", "path": "api/accounts/{id}/folders/{id}/messages/{id}/inline"},
    {"method": "GET", "path": "api/accounts/{id}/messages/search"},
    {"method": "GET", "path": "api/accounts/{id}/messages/view"},
    {"method": "GET", "path": "api/accounts/{id}/messages/{id}/originalmessage"},
    {"method": "GET", "path": "api/notes/favorites"},
    {"method": "GET", "path": "api/notes/groups"},
    {"method": "GET", "path": "api/notes/groups/{id}"},
    {"method": "GET", "path": "api/notes/groups/{id}/books"},
    {"method": "GET", "path": "api/notes/groups/{id}/books/{id}"},
    {"method": "GET", "path": "api/notes/groups/{id}/{id}"},
    {"method": "GET", "path": "api/notes/groups/{id}/{id}/attachments"},
    {"method": "GET", "path": "api/notes/groups/{id}/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/notes/me"},
    {"method": "GET", "path": "api/notes/me/books"},
    {"method": "GET", "path": "api/notes/me/books/{id}"},
    {"method": "GET", "path": "api/notes/me/{id}"},
    {"method": "GET", "path": "api/notes/me/{id}/attachments"},
    {"method": "GET", "path": "api/notes/me/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/notes/sharedtome"},
    {"method": "GET", "path": "api/organization/{id}"},
    {"method": "GET", "path": "api/organization/{id}/allowedIps"},
    {"method": "GET", "path": "api/organization/{id}/antispam/data"},
    {"method": "GET", "path": "api/organization/{id}/storage"},
    {"method": "GET", "path": "api/organization/{id}/storage/{id}"},
    {"method": "GET", "path": "api/organization/{id}/subscriptionInfo"},
    {"method": "GET", "path": "api/organization/{id}/policy"},
    {"method": "GET", "path": "api/organization/{id}/policy/accessRestriction"},
    {"method": "GET", "path": "api/organization/{id}/policy/accountRestriction"},
    {"method": "GET", "path": "api/organization/{id}/policy/mailForwardPolicy"},
    {"method": "GET", "path": "api/organization/{id}/policy/mailRestriction"},
    {"method": "GET", "path": "api/organization/{id}/policy/{id}/getGroups"},
    {"method": "GET", "path": "api/organization/{id}/policy/{id}/getUsers"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/assigned/{id}/messages"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/counts"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/messages/{id}"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/messages/{id}/comments"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/messages/{id}/comments/{id}"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/messages/{id}/invitees"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/tags"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/tags/{id}"},
    {"method": "GET", "path": "api/v2/sharedmailbox/{id}/tags/{id}/messages"},
    {"method": "GET", "path": "api/accounts/signature"},
    {"method": "GET", "path": "api/organization/{id}/accounts/{id}/signature"},
    {"method": "GET", "path": "api/tasks"},
    {"method": "GET", "path": "api/tasks/groups"},
    {"method": "GET", "path": "api/tasks/groups/{id}"},
    {"method": "GET", "path": "api/tasks/groups/{id}/customStatus"},
    {"method": "GET", "path": "api/tasks/groups/{id}/members"},
    {"method": "GET", "path": "api/tasks/groups/{id}/projects"},
    {"method": "GET", "path": "api/tasks/groups/{id}/projects/{id}"},
    {"method": "GET", "path": "api/tasks/groups/{id}/{id}"},
    {"method": "GET", "path": "api/tasks/groups/{id}/{id}/attachments"},
    {"method": "GET", "path": "api/tasks/groups/{id}/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/tasks/groups/{id}/{id}/subtasks"},
    {"method": "GET", "path": "api/tasks/me"},
    {"method": "GET", "path": "api/tasks/me/customStatus"},
    {"method": "GET", "path": "api/tasks/me/{id}"},
    {"method": "GET", "path": "api/tasks/me/{id}/attachments"},
    {"method": "GET", "path": "api/tasks/me/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/tasks/me/{id}/subtasks"},
    {"method": "GET", "path": "api/organization/{id}/accounts"},
    {"method": "GET", "path": "api/organization/{id}/accounts/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho Mail endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/accounts | read | accounts | Get all accounts of the user. |
| GET | api/accounts/{id} | read | accounts | Get details of a specific account. |
| PUT | api/accounts/{id} | write | accounts | Update an account (sequence, reply-to, display name, forwarding, vacation reply, IMAP/POP). |
| GET | api/organization/{id}/antispam/options | read | antispam | Get SPF, DKIM or DMARC fail options. |
| PUT | api/organization/{id}/antispam/options | write | antispam | Update SPF, DKIM or DMARC fail options. |
| GET | api/links | read | bookmarks | Get all shared bookmarks. |
| GET | api/links/favorites | read | bookmarks | Get all favourite bookmarks. |
| GET | api/links/groups | read | bookmarks | Get all bookmark groups. |
| GET | api/links/groups/collections | read | bookmarks | Get all collections in groups. |
| GET | api/links/groups/{id} | read | bookmarks | Get all bookmarks in a group. |
| POST | api/links/groups/{id} | write | bookmarks | Create a group bookmark. |
| GET | api/links/groups/{id}/collections | read | bookmarks | Get all group collections. |
| POST | api/links/groups/{id}/collections | write | bookmarks | Create a group bookmark collection. |
| GET | api/links/groups/{id}/collections/{id} | read | bookmarks | Get bookmarks in a group collection. |
| PUT | api/links/groups/{id}/collections/{id} | write | bookmarks | Edit a group collection. |
| DELETE | api/links/groups/{id}/collections/{id} | write | bookmarks | Delete a group collection. |
| GET | api/links/groups/{id}/trash | read | bookmarks | Get group bookmarks in trash. |
| GET | api/links/groups/{id}/{id} | read | bookmarks | Get a group bookmark. |
| PUT | api/links/groups/{id}/{id} | write | bookmarks | Edit a group bookmark. |
| DELETE | api/links/groups/{id}/{id} | write | bookmarks | Delete a group bookmark. |
| PUT | api/links/groups/{id}/{id}/favorite | write | bookmarks | Mark a group bookmark as favorite. |
| DELETE | api/links/groups/{id}/{id}/favorite | write | bookmarks | Unmark a group bookmark as favorite. |
| PUT | api/links/groups/{id}/{id}/restore | write | bookmarks | Restore a group bookmark. |
| GET | api/links/me | read | bookmarks | Get all personal bookmarks. |
| POST | api/links/me | write | bookmarks | Create a personal bookmark. |
| GET | api/links/me/collections | read | bookmarks | Get all personal collections. |
| POST | api/links/me/collections | write | bookmarks | Create a personal bookmark collection. |
| GET | api/links/me/collections/{id} | read | bookmarks | Get bookmarks in a personal collection. |
| PUT | api/links/me/collections/{id} | write | bookmarks | Edit a personal collection. |
| DELETE | api/links/me/collections/{id} | write | bookmarks | Delete a personal collection. |
| GET | api/links/me/trash | read | bookmarks | Get personal bookmarks in trash. |
| GET | api/links/me/{id} | read | bookmarks | Get a personal bookmark. |
| PUT | api/links/me/{id} | write | bookmarks | Edit a personal bookmark. |
| DELETE | api/links/me/{id} | write | bookmarks | Delete a personal bookmark. |
| PUT | api/links/me/{id}/favorite | write | bookmarks | Mark a personal bookmark as favorite. |
| DELETE | api/links/me/{id}/favorite | write | bookmarks | Unmark a personal bookmark as favorite. |
| GET | api/organization/{id}/domains | read | domains | Get all domain details. |
| POST | api/organization/{id}/domains | write | domains | Add a domain to the organization. |
| GET | api/organization/{id}/domains/{id} | read | domains | Get details of a specific domain. |
| PUT | api/organization/{id}/domains/{id} | write | domains | Update a domain (verify, primary, alias, DKIM, catch-all, notification address, and similar actions). |
| DELETE | api/organization/{id}/domains/{id} | write | domains | Delete a domain from the organization. |
| GET | api/accounts/{id}/folders | read | folders | Get all folders. |
| POST | api/accounts/{id}/folders | write | folders | Create a folder. |
| GET | api/accounts/{id}/folders/{id} | read | folders | Get a specific folder. |
| PUT | api/accounts/{id}/folders/{id} | write | folders | Update a folder (rename, move, IMAP view, mark read, empty). |
| DELETE | api/accounts/{id}/folders/{id} | write | folders | Delete a folder. |
| GET | api/organization/{id}/groups | read | groups | Get all group details. |
| POST | api/organization/{id}/groups | write | groups | Create a group. |
| DELETE | api/organization/{id}/groups | write | groups | Delete groups. |
| GET | api/organization/{id}/groups/{id} | read | groups | Get specific group details. |
| PUT | api/organization/{id}/groups/{id} | write | groups | Update a group (name, members, roles, settings, aliases). |
| DELETE | api/organization/{id}/groups/{id} | write | groups | Delete a group. |
| GET | api/organization/{id}/groups/{id}/messages | read | groups | Get emails held for moderation in a group. |
| PUT | api/organization/{id}/groups/{id}/messages | write | groups | Moderate emails in a group. |
| GET | api/organization/{id}/groups/{id}/messages/{id} | read | groups | Get the content of a moderation email. |
| GET | api/accounts/{id}/labels | read | labels | Get all labels. |
| POST | api/accounts/{id}/labels | write | labels | Create a label. |
| GET | api/accounts/{id}/labels/{id} | read | labels | Get a specific label. |
| PUT | api/accounts/{id}/labels/{id} | write | labels | Update a label. |
| DELETE | api/accounts/{id}/labels/{id} | write | labels | Delete a label. |
| GET | api/organization/{id}/accounts/reports/loginHistory | read | logs | Get login history. |
| GET | api/organization/{id}/activity | read | logs | Get audit records. |
| GET | api/organization/{id}/smtplogs | read | logs | Get SMTP logs. |
| DELETE | api/accounts/{id}/folders/{id}/messages/{id} | write | messages | Delete an email. |
| GET | api/accounts/{id}/folders/{id}/messages/{id}/attachmentinfo | read | messages | Get attachment info of an email. |
| GET | api/accounts/{id}/folders/{id}/messages/{id}/attachments/{id} | read | messages | Download an attachment. |
| GET | api/accounts/{id}/folders/{id}/messages/{id}/content | read | messages | Get email content. |
| GET | api/accounts/{id}/folders/{id}/messages/{id}/details | read | messages | Get email metadata. |
| GET | api/accounts/{id}/folders/{id}/messages/{id}/header | read | messages | Get email headers. |
| GET | api/accounts/{id}/folders/{id}/messages/{id}/inline | read | messages | Download an inline image. |
| POST | api/accounts/{id}/messages | write | messages | Send an email or save a draft or template. |
| POST | api/accounts/{id}/messages/attachments | write | messages | Upload an attachment. |
| GET | api/accounts/{id}/messages/search | read | messages | Search emails. |
| GET | api/accounts/{id}/messages/view | read | messages | List emails in a folder. |
| POST | api/accounts/{id}/messages/{id} | write | messages | Reply to an email. |
| GET | api/accounts/{id}/messages/{id}/originalmessage | read | messages | Get the original MIME message. |
| PUT | api/accounts/{id}/updatemessage | write | messages | Update emails (read state, move, flag, labels, archive, spam). |
| GET | api/notes/favorites | read | notes | Get all favourite notes. |
| GET | api/notes/groups | read | notes | Get all note groups. |
| GET | api/notes/groups/{id} | read | notes | Get all notes in a group. |
| POST | api/notes/groups/{id} | write | notes | Create a group note. |
| GET | api/notes/groups/{id}/books | read | notes | Get all group books. |
| POST | api/notes/groups/{id}/books | write | notes | Create a group book. |
| GET | api/notes/groups/{id}/books/{id} | read | notes | Get all notes in a group book. |
| PUT | api/notes/groups/{id}/books/{id} | write | notes | Edit a group book. |
| DELETE | api/notes/groups/{id}/books/{id} | write | notes | Delete a group book. |
| GET | api/notes/groups/{id}/{id} | read | notes | Get a group note. |
| PUT | api/notes/groups/{id}/{id} | write | notes | Edit a group note. |
| DELETE | api/notes/groups/{id}/{id} | write | notes | Delete a group note. |
| GET | api/notes/groups/{id}/{id}/attachments | read | notes | Get all attachments of a group note. |
| POST | api/notes/groups/{id}/{id}/attachments | write | notes | Add an attachment to a group note. |
| GET | api/notes/groups/{id}/{id}/attachments/{id} | read | notes | Get an attachment of a group note. |
| DELETE | api/notes/groups/{id}/{id}/attachments/{id} | write | notes | Delete an attachment of a group note. |
| PUT | api/notes/groups/{id}/{id}/favorite | write | notes | Mark a group note as favorite. |
| DELETE | api/notes/groups/{id}/{id}/favorite | write | notes | Unmark a group note as favorite. |
| GET | api/notes/me | read | notes | Get all personal notes. |
| POST | api/notes/me | write | notes | Create a personal note. |
| GET | api/notes/me/books | read | notes | Get all personal books. |
| POST | api/notes/me/books | write | notes | Create a personal book. |
| GET | api/notes/me/books/{id} | read | notes | Get all notes in a personal book. |
| PUT | api/notes/me/books/{id} | write | notes | Edit a personal book. |
| DELETE | api/notes/me/books/{id} | write | notes | Delete a personal book. |
| GET | api/notes/me/{id} | read | notes | Get a personal note. |
| PUT | api/notes/me/{id} | write | notes | Edit a personal note. |
| DELETE | api/notes/me/{id} | write | notes | Delete a personal note. |
| GET | api/notes/me/{id}/attachments | read | notes | Get all attachments of a personal note. |
| POST | api/notes/me/{id}/attachments | write | notes | Add an attachment to a personal note. |
| GET | api/notes/me/{id}/attachments/{id} | read | notes | Get an attachment of a personal note. |
| DELETE | api/notes/me/{id}/attachments/{id} | write | notes | Delete an attachment of a personal note. |
| PUT | api/notes/me/{id}/favorite | write | notes | Mark a personal note as favorite. |
| DELETE | api/notes/me/{id}/favorite | write | notes | Unmark a personal note as favorite. |
| GET | api/notes/sharedtome | read | notes | Get all notes shared with you. |
| POST | api/organization | write | organization | Add a child organization. |
| GET | api/organization/{id} | read | organization | Get organization details. |
| PUT | api/organization/{id} | write | organization | Update the organization spam process type. |
| GET | api/organization/{id}/allowedIps | read | organization | Get the allowed IPs list. |
| POST | api/organization/{id}/allowedIps | write | organization | Add allowed IPs for the organization. |
| DELETE | api/organization/{id}/allowedIps | write | organization | Delete allowed IPs. |
| GET | api/organization/{id}/antispam/data | read | organization | Get the organization spam listing. |
| PUT | api/organization/{id}/antispam/data | write | organization | Update the organization spam listing. |
| DELETE | api/organization/{id}/antispam/data | write | organization | Remove entries from the organization spam listing. |
| GET | api/organization/{id}/storage | read | organization | Get organization subscription and storage details. |
| GET | api/organization/{id}/storage/{id} | read | organization | Get storage details of a user. |
| PUT | api/organization/{id}/storage/{id} | write | organization | Update a user's storage. |
| GET | api/organization/{id}/subscriptionInfo | read | organization | Get organization subscription info. |
| GET | api/organization/{id}/policy | read | policies | Get all policies. |
| POST | api/organization/{id}/policy | write | policies | Create an organization policy. |
| GET | api/organization/{id}/policy/accessRestriction | read | policies | Get all access restrictions. |
| POST | api/organization/{id}/policy/accessRestriction | write | policies | Create an access restriction. |
| PUT | api/organization/{id}/policy/accessRestriction/{id} | write | policies | Add allowed IPs to an access restriction. |
| GET | api/organization/{id}/policy/accountRestriction | read | policies | Get all account restrictions. |
| POST | api/organization/{id}/policy/accountRestriction | write | policies | Create an account restriction. |
| GET | api/organization/{id}/policy/mailForwardPolicy | read | policies | Get all forward restrictions. |
| POST | api/organization/{id}/policy/mailForwardPolicy | write | policies | Create a forward restriction. |
| GET | api/organization/{id}/policy/mailRestriction | read | policies | Get all email restrictions. |
| POST | api/organization/{id}/policy/mailRestriction | write | policies | Create an email restriction. |
| PUT | api/organization/{id}/policy/{id} | write | policies | Apply a policy to users or groups or assign restrictions to it. |
| GET | api/organization/{id}/policy/{id}/getGroups | read | policies | Get groups a policy applies to. |
| GET | api/organization/{id}/policy/{id}/getUsers | read | policies | Get users a policy applies to. |
| GET | api/v2/sharedmailbox/{id}/assigned/{id}/messages | read | sharedmailbox | List messages assigned to a user. |
| GET | api/v2/sharedmailbox/{id}/counts | read | sharedmailbox | Get message counts. |
| PUT | api/v2/sharedmailbox/{id}/messages/read-all | write | sharedmailbox | Mark all messages as read. |
| GET | api/v2/sharedmailbox/{id}/messages/{id} | read | sharedmailbox | Get a shared mailbox message or list messages by view. |
| DELETE | api/v2/sharedmailbox/{id}/messages/{id} | write | sharedmailbox | Delete a message in trash or spam view. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/archive | write | sharedmailbox | Archive a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/assign | write | sharedmailbox | Assign a message. |
| GET | api/v2/sharedmailbox/{id}/messages/{id}/comments | read | sharedmailbox | List comments on a message. |
| POST | api/v2/sharedmailbox/{id}/messages/{id}/comments | write | sharedmailbox | Add a comment to a message. |
| GET | api/v2/sharedmailbox/{id}/messages/{id}/comments/{id} | read | sharedmailbox | Get a comment. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/comments/{id} | write | sharedmailbox | Edit a comment. |
| DELETE | api/v2/sharedmailbox/{id}/messages/{id}/comments/{id} | write | sharedmailbox | Delete a comment. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/comments/{id}/like | write | sharedmailbox | Like a comment. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/comments/{id}/unlike | write | sharedmailbox | Unlike a comment. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/follow | write | sharedmailbox | Follow a message. |
| GET | api/v2/sharedmailbox/{id}/messages/{id}/invitees | read | sharedmailbox | List invitees on a message. |
| POST | api/v2/sharedmailbox/{id}/messages/{id}/invitees | write | sharedmailbox | Add invitees to a message. |
| DELETE | api/v2/sharedmailbox/{id}/messages/{id}/invitees | write | sharedmailbox | Remove invitees from a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/invitees/disable | write | sharedmailbox | Disable invite access on a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/invitees/enable | write | sharedmailbox | Enable invite access on a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/like | write | sharedmailbox | Like a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/notspam | write | sharedmailbox | Mark a message as not spam. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/read | write | sharedmailbox | Mark a message as read. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/spam | write | sharedmailbox | Mark a message as spam. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/tags/add | write | sharedmailbox | Add tags to a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/tags/remove | write | sharedmailbox | Remove tags from a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/trash | write | sharedmailbox | Trash a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/trash/restore | write | sharedmailbox | Restore a message from trash. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/unarchive | write | sharedmailbox | Unarchive a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/unassign | write | sharedmailbox | Unassign a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/unfollow | write | sharedmailbox | Unfollow a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/unlike | write | sharedmailbox | Unlike a message. |
| PUT | api/v2/sharedmailbox/{id}/messages/{id}/unread | write | sharedmailbox | Mark a message as unread. |
| GET | api/v2/sharedmailbox/{id}/tags | read | sharedmailbox | List tags. |
| POST | api/v2/sharedmailbox/{id}/tags | write | sharedmailbox | Create a tag. |
| GET | api/v2/sharedmailbox/{id}/tags/{id} | read | sharedmailbox | Get a tag. |
| PUT | api/v2/sharedmailbox/{id}/tags/{id} | write | sharedmailbox | Update a tag. |
| DELETE | api/v2/sharedmailbox/{id}/tags/{id} | write | sharedmailbox | Delete a tag. |
| GET | api/v2/sharedmailbox/{id}/tags/{id}/messages | read | sharedmailbox | List messages by tag. |
| GET | api/accounts/signature | read | signatures | Get the user signature. |
| POST | api/accounts/signature | write | signatures | Add a user signature. |
| PUT | api/accounts/signature | write | signatures | Update the user signature. |
| DELETE | api/accounts/signature | write | signatures | Delete the user signature. |
| GET | api/organization/{id}/accounts/{id}/signature | read | signatures | Get an admin-added user signature. |
| POST | api/organization/{id}/accounts/{id}/signature | write | signatures | Add an admin-added user signature. |
| PUT | api/organization/{id}/accounts/{id}/signature | write | signatures | Update an admin-added user signature. |
| DELETE | api/organization/{id}/accounts/{id}/signature | write | signatures | Delete an admin-added user signature. |
| GET | api/tasks | read | tasks | Get tasks assigned to or created by you. |
| GET | api/tasks/groups | read | tasks | Get all task groups. |
| GET | api/tasks/groups/{id} | read | tasks | Get all tasks in a group. |
| POST | api/tasks/groups/{id} | write | tasks | Add a group task. |
| GET | api/tasks/groups/{id}/customStatus | read | tasks | Get custom statuses of group tasks. |
| POST | api/tasks/groups/{id}/customStatus | write | tasks | Add a custom status to group tasks. |
| PUT | api/tasks/groups/{id}/customStatus | write | tasks | Edit a custom status of group tasks. |
| DELETE | api/tasks/groups/{id}/customStatus | write | tasks | Delete a custom status of group tasks. |
| GET | api/tasks/groups/{id}/members | read | tasks | Get member details of a group. |
| GET | api/tasks/groups/{id}/projects | read | tasks | Get all projects in a group. |
| POST | api/tasks/groups/{id}/projects | write | tasks | Add a project to a group. |
| GET | api/tasks/groups/{id}/projects/{id} | read | tasks | Get all tasks in a project. |
| PUT | api/tasks/groups/{id}/projects/{id} | write | tasks | Edit a project. |
| DELETE | api/tasks/groups/{id}/projects/{id} | write | tasks | Delete a project. |
| GET | api/tasks/groups/{id}/{id} | read | tasks | Get a specific group task. |
| PUT | api/tasks/groups/{id}/{id} | write | tasks | Update a group task. |
| DELETE | api/tasks/groups/{id}/{id} | write | tasks | Delete a group task. |
| GET | api/tasks/groups/{id}/{id}/attachments | read | tasks | Get attachment details of a group task. |
| POST | api/tasks/groups/{id}/{id}/attachments | write | tasks | Add an attachment to a group task. |
| DELETE | api/tasks/groups/{id}/{id}/attachments | write | tasks | Delete attachments from a group task. |
| GET | api/tasks/groups/{id}/{id}/attachments/{id} | read | tasks | Download an attachment of a group task. |
| PUT | api/tasks/groups/{id}/{id}/restore | write | tasks | Restore a deleted group task. |
| GET | api/tasks/groups/{id}/{id}/subtasks | read | tasks | Get subtasks of a group task. |
| GET | api/tasks/me | read | tasks | Get all personal tasks. |
| POST | api/tasks/me | write | tasks | Add a personal task. |
| GET | api/tasks/me/customStatus | read | tasks | Get custom statuses of personal tasks. |
| POST | api/tasks/me/customStatus | write | tasks | Add a custom status to personal tasks. |
| PUT | api/tasks/me/customStatus | write | tasks | Edit a custom status of personal tasks. |
| DELETE | api/tasks/me/customStatus | write | tasks | Delete a custom status of personal tasks. |
| GET | api/tasks/me/{id} | read | tasks | Get a specific personal task. |
| PUT | api/tasks/me/{id} | write | tasks | Update a personal task. |
| DELETE | api/tasks/me/{id} | write | tasks | Delete a personal task. |
| GET | api/tasks/me/{id}/attachments | read | tasks | Get attachment details of a personal task. |
| POST | api/tasks/me/{id}/attachments | write | tasks | Add an attachment to a personal task. |
| DELETE | api/tasks/me/{id}/attachments | write | tasks | Delete attachments from a personal task. |
| GET | api/tasks/me/{id}/attachments/{id} | read | tasks | Download an attachment of a personal task. |
| PUT | api/tasks/me/{id}/restore | write | tasks | Restore a deleted personal task. |
| GET | api/tasks/me/{id}/subtasks | read | tasks | Get subtasks of a personal task. |
| PUT | api/accounts/{id}/updatethread | write | threads | Update threads (flag, move, labels, read state, spam). |
| GET | api/organization/{id}/accounts | read | users | Fetch details of all organization users. |
| POST | api/organization/{id}/accounts | write | users | Add a user to the organization. |
| PUT | api/organization/{id}/accounts | write | users | Change the role of a user. |
| DELETE | api/organization/{id}/accounts | write | users | Delete a user account. |
| GET | api/organization/{id}/accounts/{id} | read | users | Fetch a single user's details by ZUID or email address. |
| PUT | api/organization/{id}/accounts/{id} | write | users | Update a user (password reset, TFA, aliases, enable/disable, protocol status). |
