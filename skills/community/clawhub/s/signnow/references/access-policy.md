# SignNow access policy

An access policy limits which endpoints SignNow connections may call through Maton. SignNow doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/signnow#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for SignNow: its 111 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create signnow --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "request-logs"},
    {"method": "GET", "path": "request-logs/{id}"},
    {"method": "GET", "path": "v2/paid-request-logs"},
    {"method": "GET", "path": "v2/paid-request-logs/export"},
    {"method": "GET", "path": "v2/paid-request-monthly-totals"},
    {"method": "GET", "path": "v2/paid-request-totals"},
    {"method": "GET", "path": "api/v2/events"},
    {"method": "GET", "path": "v2/event-subscriptions/callbacks"},
    {"method": "GET", "path": "v2/event-subscriptions/{id}/callbacks"},
    {"method": "GET", "path": "v2/event-subscriptions/{id}/callbacks/{id}"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-cc-invite"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-cc-invite-completed"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-cc-invite-reassign"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-cc-invite-signed"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-cc-invite-step-completed"},
    {"method": "GET", "path": "v2/crm/contacts/{id}/groups"},
    {"method": "GET", "path": "v2/crm/groups"},
    {"method": "GET", "path": "v2/crm/groups/{id}"},
    {"method": "GET", "path": "v2/crm/groups/{id}/contacts"},
    {"method": "GET", "path": "v2/crm/contacts"},
    {"method": "GET", "path": "v2/crm/contacts/{id}"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email"},
    {"method": "GET", "path": "v2/brands/{id}/{id}"},
    {"method": "GET", "path": "team/{id}/documentgroup/templates"},
    {"method": "GET", "path": "v2/documents/{id}/free-form-invites"},
    {"method": "GET", "path": "documentgroup/{id}/groupinvite/{id}"},
    {"method": "GET", "path": "documentgroup/{id}/groupinvite/{id}/invitestep/{id}/emails"},
    {"method": "GET", "path": "documentgroup/{id}/groupinvite/{id}/pendinginvites"},
    {"method": "GET", "path": "v2/document-groups/{id}/recipients"},
    {"method": "GET", "path": "v2/document-groups/{id}/free-form-invites/{id}/documents"},
    {"method": "GET", "path": "document/{id}"},
    {"method": "GET", "path": "document/{id}/attachment/{id}/download"},
    {"method": "GET", "path": "document/{id}/download"},
    {"method": "GET", "path": "document/{id}/historyfull"},
    {"method": "GET", "path": "document/{id}/metadata"},
    {"method": "GET", "path": "v2/documents/{id}/fields"},
    {"method": "GET", "path": "v2/documents/{id}/roles"},
    {"method": "GET", "path": "v2/documents/{id}/field-invites/{id}/full-decline"},
    {"method": "GET", "path": "v2/signing-session-settings"},
    {"method": "GET", "path": "v2/document-generations/{id}/status"},
    {"method": "GET", "path": "documentgroup/{id}"},
    {"method": "GET", "path": "documentgroup/{id}/historyfull"},
    {"method": "GET", "path": "user/documentgroups"},
    {"method": "GET", "path": "v2/document-groups/{id}"},
    {"method": "GET", "path": "v2/document-groups/{id}/metadata"},
    {"method": "GET", "path": "v2/document-groups/{id}/roles"},
    {"method": "GET", "path": "user/documentgroup/templates"},
    {"method": "GET", "path": "v2/document-group-templates/{id}"},
    {"method": "GET", "path": "v2/document-group-templates/{id}/copies"},
    {"method": "GET", "path": "v2/document-group-templates/{id}/recipients"},
    {"method": "GET", "path": "v2/document-group-templates/{id}/roles"},
    {"method": "GET", "path": "v2/favorites"},
    {"method": "GET", "path": "folder/{id}"},
    {"method": "GET", "path": "user/folder"},
    {"method": "GET", "path": "v2/folders/{id}/document-templates/pinned"},
    {"method": "GET", "path": "v2/applications/{id}/brand"},
    {"method": "GET", "path": "v2/brands"},
    {"method": "GET", "path": "v2/brands/template-file"},
    {"method": "GET", "path": "v2/brands/{id}"},
    {"method": "GET", "path": "v2/brands/{id}/resources/editor"},
    {"method": "GET", "path": "v2/brands/{id}/resources/general"},
    {"method": "GET", "path": "v2/brands/{id}/resources/logo"},
    {"method": "GET", "path": "v2/brands/{id}/resources/send-invite"},
    {"method": "GET", "path": "v2/document-groups/{id}/brand"},
    {"method": "GET", "path": "v2/documents/{id}/brand"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-general"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-invite"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-invite-canceled"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-invite-completed"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-invite-reassign"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-invite-reminder"},
    {"method": "GET", "path": "v2/brands/{id}/resources/email-logo"},
    {"method": "GET", "path": "v2/teams/{id}/admins"},
    {"method": "GET", "path": "v2/event-subscriptions"},
    {"method": "GET", "path": "v2/event-subscriptions/{id}"},
    {"method": "GET", "path": "team/{id}"},
    {"method": "GET", "path": "v2/teams"},
    {"method": "GET", "path": "team/{id}/request"},
    {"method": "GET", "path": "v2/teams/{id}/members"},
    {"method": "GET", "path": "v2/organizations/{id}/email-footers"},
    {"method": "GET", "path": "v2/organizations/{id}/email-footers/{id}"},
    {"method": "GET", "path": "v2/organizations"},
    {"method": "GET", "path": "v2/organizations/{id}/activity"},
    {"method": "GET", "path": "v2/organizations/{id}/admins"},
    {"method": "GET", "path": "v2/organizations/{id}/allowed-team-admins"},
    {"method": "GET", "path": "v2/organizations/{id}/documents/search"},
    {"method": "GET", "path": "v2/organizations/{id}/members"},
    {"method": "GET", "path": "v2/organizations/{id}/members/last-logins"},
    {"method": "GET", "path": "v2/organizations/{id}/settings"},
    {"method": "GET", "path": "v2/organizations/{id}/users-activity"},
    {"method": "GET", "path": "v2/organizations/{id}/brand"},
    {"method": "GET", "path": "v2/organizations/{id}/brands"},
    {"method": "GET", "path": "v2/organizations/{id}/brands/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/brands/{id}/resources/editor"},
    {"method": "GET", "path": "v2/organizations/{id}/brands/{id}/resources/email"},
    {"method": "GET", "path": "v2/organizations/{id}/brands/{id}/resources/general"},
    {"method": "GET", "path": "v2/organizations/{id}/brands/{id}/resources/logo"},
    {"method": "GET", "path": "organizations/{id}/merchantaccount/{id}"},
    {"method": "GET", "path": "v2/merchant-accounts/{id}"},
    {"method": "GET", "path": "v2/search"},
    {"method": "GET", "path": "document/{id}/integration_objects"},
    {"method": "GET", "path": "document/{id}/template/routing/detail"},
    {"method": "GET", "path": "v2/templates/{id}/copies"},
    {"method": "GET", "path": "v2/templates/{id}/roles/{id}"},
    {"method": "GET", "path": "folder"},
    {"method": "GET", "path": "user"},
    {"method": "GET", "path": "user/documents"},
    {"method": "GET", "path": "user/documentsv2"},
    {"method": "GET", "path": "v2/crm/contacts/{id}/users"},
    {"method": "GET", "path": "v2/crm/users"},
    {"method": "GET", "path": "event_subscription"}
  ],
  "deny": []
}
```

## Endpoints

The SignNow endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | request-logs | read | api logs | Get logs. |
| GET | request-logs/{id} | read | api logs | Get request log. |
| GET | v2/paid-request-logs | read | api logs | Get paid request logs. |
| GET | v2/paid-request-logs/export | read | api logs | Export paid request logs. |
| GET | v2/paid-request-monthly-totals | read | api logs | Get monthly request totals. |
| GET | v2/paid-request-totals | read | api logs | Get paid requests. |
| GET | api/v2/events | read | basic auth | Get event subscriptions. |
| POST | api/v2/events | write | basic auth | Create event subscription. |
| PUT | api/v2/events/{id} | write | basic auth | Edit event subscription (basic auth). |
| DELETE | api/v2/events/{id} | write | basic auth | Delete event subscription (basic auth). |
| GET | v2/event-subscriptions/callbacks | read | callbacks info | Get list of callbacks. |
| GET | v2/event-subscriptions/{id}/callbacks | read | callbacks info | Get list of callbacks by event subscription. |
| GET | v2/event-subscriptions/{id}/callbacks/{id} | read | callbacks info | Get callback info by ID. |
| POST | v2/event-subscriptions/{id}/callbacks/{id}/resend | write | callbacks info | Resend callback. |
| GET | v2/brands/{id}/resources/email-cc-invite | read | cc email branding | Get invite CC email branding. |
| PUT | v2/brands/{id}/resources/email-cc-invite | write | cc email branding | Brand invite CC email. |
| DELETE | v2/brands/{id}/resources/email-cc-invite | write | cc email branding | Delete invite CC email branding. |
| GET | v2/brands/{id}/resources/email-cc-invite-completed | read | cc email branding | Get invite completed CC email branding. |
| PUT | v2/brands/{id}/resources/email-cc-invite-completed | write | cc email branding | Brand invite completed CC email. |
| DELETE | v2/brands/{id}/resources/email-cc-invite-completed | write | cc email branding | Delete invite completed CC email branding. |
| GET | v2/brands/{id}/resources/email-cc-invite-reassign | read | cc email branding | Get reassign CC email branding. |
| PUT | v2/brands/{id}/resources/email-cc-invite-reassign | write | cc email branding | Brand reassign CC email. |
| DELETE | v2/brands/{id}/resources/email-cc-invite-reassign | write | cc email branding | Delete reassign CC email branding. |
| GET | v2/brands/{id}/resources/email-cc-invite-signed | read | cc email branding | Get freeform signed CC email branding. |
| PUT | v2/brands/{id}/resources/email-cc-invite-signed | write | cc email branding | Brand freeform signed CC email. |
| DELETE | v2/brands/{id}/resources/email-cc-invite-signed | write | cc email branding | Delete freeform signed CC email branding. |
| GET | v2/brands/{id}/resources/email-cc-invite-step-completed | read | cc email branding | Get step completed CC email branding. |
| PUT | v2/brands/{id}/resources/email-cc-invite-step-completed | write | cc email branding | Brand step completed CC email. |
| DELETE | v2/brands/{id}/resources/email-cc-invite-step-completed | write | cc email branding | Delete step completed CC email branding. |
| GET | v2/crm/contacts/{id}/groups | read | contact groups | Get contact groups list by contact. |
| GET | v2/crm/groups | read | contact groups | Get the list of groups. |
| POST | v2/crm/groups | write | contact groups | Create contact group. |
| GET | v2/crm/groups/{id} | read | contact groups | Get contact group. |
| PUT | v2/crm/groups/{id} | write | contact groups | Update contact group. |
| DELETE | v2/crm/groups/{id} | write | contact groups | Remove contact group. |
| GET | v2/crm/groups/{id}/contacts | read | contact groups | Get contacts from group. |
| PUT | v2/crm/groups/{id}/contacts/{id} | write | contact groups | Add contact to group. |
| DELETE | v2/crm/groups/{id}/contacts/{id} | write | contact groups | Remove contact from group. |
| GET | v2/crm/contacts | read | contacts | Get the list of CRM contacts. |
| POST | v2/crm/contacts | write | contacts | Create CRM contact. |
| POST | v2/crm/contacts/import | write | contacts | Import CRM contacts in bulk. |
| GET | v2/crm/contacts/{id} | read | contacts | Get CRM contact info. |
| PUT | v2/crm/contacts/{id} | write | contacts | Update a CRM contact. |
| DELETE | v2/crm/contacts/{id} | write | contacts | Remove a CRM contact. |
| POST | v2/brands/{id}/assign | write | deprecated branding | Assign brand. |
| GET | v2/brands/{id}/resources/email | read | deprecated branding | Get email brand resource. |
| PUT | v2/brands/{id}/resources/email | write | deprecated branding | Create email brand resource. |
| POST | v2/brands/{id}/unassign | write | deprecated branding | Unassign brand. |
| GET | v2/brands/{id}/{id} | read | deprecated branding | Get resource details. |
| DELETE | v2/brands/{id}/{id} | write | deprecated branding | Delete resource. |
| POST | team/{id}/documentgroup/template/{id}/share | write | deprecated dgt | Share doc group template. |
| DELETE | team/{id}/documentgroup/template/{id}/share | write | deprecated dgt | Delete doc group templates for a team. |
| GET | team/{id}/documentgroup/templates | read | deprecated dgt | Get team doc group templates. |
| POST | document/{id}/invite | write | doc freeform invite | Create freeform invite. |
| PUT | invite/{id}/cancel | write | doc freeform invite | Cancel freeform invite. |
| GET | v2/documents/{id}/free-form-invites | read | doc freeform invite | Get freeform invites. |
| POST | v2/document-groups/{id}/embedded-invites | write | doc group embedded signing | Create embedded invite. |
| DELETE | v2/document-groups/{id}/embedded-invites | write | doc group embedded signing | Delete embedded invites. |
| POST | v2/document-groups/{id}/embedded-invites/{id}/link | write | doc group embedded signing | Generate embedded invite link. |
| POST | documentgroup/{id}/groupinvite | write | doc group field invite | Invite to sign doc group. |
| GET | documentgroup/{id}/groupinvite/{id} | read | doc group field invite | Get doc group invite. |
| POST | documentgroup/{id}/groupinvite/{id}/cancelinvite | write | doc group field invite | Cancel doc group invite. |
| GET | documentgroup/{id}/groupinvite/{id}/invitestep/{id}/emails | read | doc group field invite | Get emails of the invite step. |
| POST | documentgroup/{id}/groupinvite/{id}/invitestep/{id}/update | write | doc group field invite | Update doc group invite. |
| GET | documentgroup/{id}/groupinvite/{id}/pendinginvites | read | doc group field invite | Get pending group invites. |
| POST | documentgroup/{id}/groupinvite/{id}/resendinvites | write | doc group field invite | Resend doc group invite. |
| POST | v2/document-groups/{id}/invites/{id}/full-decline | write | doc group field invite | Decline group invite. |
| GET | v2/document-groups/{id}/recipients | read | doc group field invite | Get doc group recipients. |
| PUT | v2/document-groups/{id}/recipients | write | doc group field invite | Edit doc group recipients. |
| POST | v2/document-groups/{id}/send-email | write | doc group field invite | Email doc group copy. |
| POST | v2/document-groups/{id}/free-form-invites | write | doc group freeform invite | Create freeform invite. |
| POST | v2/document-groups/{id}/free-form-invites/{id}/cancel | write | doc group freeform invite | Cancel invites for all signers. |
| GET | v2/document-groups/{id}/free-form-invites/{id}/documents | read | doc group freeform invite | Get freeform invites. |
| POST | v2/document-groups/{id}/free-form-invites/{id}/users/{id}/cancel | write | doc group freeform invite | Cancel invite for one signer. |
| POST | v2/document-groups/{id}/free-form-invites/{id}/users/{id}/resend | write | doc group freeform invite | Resend freeform invite. |
| POST | document | write | document | Upload document. |
| POST | document/fieldextract | write | document | Upload document with tags. |
| POST | document/merge | write | document | Merge documents. |
| GET | document/{id} | read | document | Get document. |
| PUT | document/{id} | write | document | Edit document. |
| DELETE | document/{id} | write | document | Delete document. |
| GET | document/{id}/attachment/{id}/download | read | document | Download document attachment. |
| POST | document/{id}/custom_history_event | write | document | Add custom history event. |
| GET | document/{id}/download | read | document | Download document. |
| POST | document/{id}/download/link | write | document | Get document download link. |
| GET | document/{id}/historyfull | read | document | Get document history. |
| GET | document/{id}/metadata | read | document | Get metadata of a document. |
| PUT | document/{id}/metadata | write | document | Add metadata to a document. |
| POST | document/{id}/move | write | document | Move document. |
| PUT | folder/{id}/documents | write | document | Move documents in bulk. |
| POST | v2/documents/url | write | document | Upload document from URL. |
| GET | v2/documents/{id}/fields | read | document | Get fields data from completed document. |
| PUT | v2/documents/{id}/prefill-texts | write | document | Prefill text fields. |
| GET | v2/documents/{id}/roles | read | document | Get document users. |
| DELETE | v2/documents/{id}/roles | write | document | Unshare document from all users. |
| DELETE | v2/documents/{id}/roles/{id} | write | document | Unshare document from user. |
| POST | v2/faxes/send | write | document | Send fax. |
| POST | v2/shared-entities | write | document | Share document. |
| POST | v2/documents/{id}/embedded-invites | write | document embedded signing | Create embedded invite. |
| DELETE | v2/documents/{id}/embedded-invites | write | document embedded signing | Delete embedded invites. |
| POST | v2/documents/{id}/embedded-invites/{id}/link | write | document embedded signing | Generate embedded invite link. |
| PUT | document/{id}/fieldinvitecancel | write | document field invite | Cancel invite. |
| POST | document/{id}/trigger_fieldinvite | write | document field invite | Replace signer: Step 3 - Send. |
| POST | field_invite | write | document field invite | Replace signer: Step 2 - Replace. |
| DELETE | field_invite/{id} | write | document field invite | Replace signer: Step 1 - Delete. |
| PUT | fieldinvite/{id}/resend | write | document field invite | Resend email invite. |
| GET | v2/documents/{id}/field-invites/{id}/full-decline | read | document field invite | Get the declined invite. |
| POST | v2/documents/{id}/field-invites/{id}/full-decline | write | document field invite | Decline to sign a field invite. |
| GET | v2/signing-session-settings | read | document field invite | Get welcome message. |
| POST | v2/signing-session-settings | write | document field invite | Customize welcome message. |
| DELETE | v2/signing-session-settings | write | document field invite | Reset welcome message to default. |
| POST | v2/document-generations/upload | write | document generation | Generate document from uploaded file. |
| POST | v2/document-generations/url | write | document generation | Generate document from URL. |
| GET | v2/document-generations/{id}/status | read | document generation | Get document generation status. |
| POST | documentgroup | write | document group | Create document group. |
| GET | documentgroup/{id} | read | document group | Get document group. |
| DELETE | documentgroup/{id} | write | document group | Delete document group. |
| POST | documentgroup/{id}/downloadall | write | document group | Download document group. |
| GET | documentgroup/{id}/historyfull | read | document group | Get document group history. |
| GET | user/documentgroups | read | document group | Get document groups. |
| GET | v2/document-groups/{id} | read | document group | Get document group info (v.2). |
| PUT | v2/document-groups/{id} | write | document group | Rename document group. |
| PATCH | v2/document-groups/{id} | write | document group | Edit document group. |
| POST | v2/document-groups/{id}/copy | write | document group | Create a copy of doc group. |
| PUT | v2/document-groups/{id}/invite/{id} | write | document group | Complete DG correction. |
| POST | v2/document-groups/{id}/invite/{id}/correction | write | document group | Initiate DG correction. |
| GET | v2/document-groups/{id}/metadata | read | document group | Get metadata of doc group. |
| PUT | v2/document-groups/{id}/metadata | write | document group | Add metadata to doc group. |
| DELETE | v2/document-groups/{id}/metadata | write | document group | Remove metadata from doc group. |
| POST | v2/document-groups/{id}/move | write | document group | Move document group. |
| GET | v2/document-groups/{id}/roles | read | document group | Get document group users. |
| POST | v2/document-groups/{id}/roles | write | document group | Share document group. |
| DELETE | v2/document-groups/{id}/roles | write | document group | Unshare document group from all users. |
| PUT | v2/document-groups/{id}/roles/{id} | write | document group | Update document group role. |
| DELETE | v2/document-groups/{id}/roles/{id} | write | document group | Unshare document group from user. |
| GET | user/documentgroup/templates | read | document group template | Get doc group templates. |
| POST | v2/document-group-templates | write | document group template | Create doc group template. |
| GET | v2/document-group-templates/{id} | read | document group template | Get doc group template info. |
| PATCH | v2/document-group-templates/{id} | write | document group template | Edit doc group template. |
| GET | v2/document-group-templates/{id}/copies | read | document group template | Get doc groups created from template. |
| POST | v2/document-group-templates/{id}/copy | write | document group template | Copy doc group template. |
| POST | v2/document-group-templates/{id}/document-group | write | document group template | Create doc group from template. |
| PATCH | v2/document-group-templates/{id}/move | write | document group template | Move doc group template. |
| GET | v2/document-group-templates/{id}/recipients | read | document group template | Get doc group template recipients. |
| PUT | v2/document-group-templates/{id}/recipients | write | document group template | Edit doc group template recipients. |
| GET | v2/document-group-templates/{id}/roles | read | document group template | Get document group template roles. |
| POST | v2/document-group-templates/{id}/roles | write | document group template | Share document group template. |
| DELETE | v2/document-group-templates/{id}/roles | write | document group template | Unshare document group template from all users. |
| PUT | v2/document-group-templates/{id}/roles/{id} | write | document group template | Update document group template role. |
| DELETE | v2/document-group-templates/{id}/roles/{id} | write | document group template | Unshare document group template from user. |
| POST | v2/document-group-templates/{id}/templates | write | document group template | Add template to doc group template. |
| POST | v2/document-groups/{id}/document-group-template | write | document group template | Create doc group template from doc group. |
| POST | v2/document-groups/{id}/embedded-editor | write | embedded editor | Create link for doc group. |
| POST | v2/documents/{id}/embedded-editor | write | embedded editor | Create link for document. |
| POST | v2/document-groups/{id}/embedded-sending | write | embedded sending | Create link for doc group. |
| POST | v2/documents/{id}/embedded-sending | write | embedded sending | Create link for document. |
| POST | v2/document-groups/{id}/embedded-view | write | embedded view | Create document group embedded view link. |
| POST | v2/documents/{id}/embedded-view | write | embedded view | Create document embedded view link. |
| POST | v2/document-groups/{id}/favorites | write | favorites | Mark doc group as favorite. |
| DELETE | v2/document-groups/{id}/favorites | write | favorites | Remove doc group from favorites. |
| POST | v2/documents/{id}/favorites | write | favorites | Mark document as favorite. |
| DELETE | v2/documents/{id}/favorites | write | favorites | Remove document from favorites. |
| GET | v2/favorites | read | favorites | Retrieve all favorites. |
| GET | folder/{id} | read | folder | Get folder by id. |
| GET | user/folder | read | folder | Get all folders. |
| POST | user/folder | write | folder | Create folder. |
| PUT | user/folder/{id} | write | folder | Rename folder. |
| DELETE | user/folder/{id} | write | folder | Delete folder. |
| GET | v2/folders/{id}/document-templates/pinned | read | folder | Get pinned templates. |
| DELETE | v2/trash | write | folder | Empty trash bin folder. |
| GET | v2/applications/{id}/brand | read | general branding | Get brand of application. |
| PUT | v2/applications/{id}/brand | write | general branding | Assign brand to application. |
| DELETE | v2/applications/{id}/brand | write | general branding | Unassign brand from application. |
| GET | v2/brands | read | general branding | Get all brands. |
| POST | v2/brands | write | general branding | Create brand. |
| GET | v2/brands/template-file | read | general branding | Get brand template file. |
| POST | v2/brands/upload-file | write | general branding | Create brand from template file. |
| GET | v2/brands/{id} | read | general branding | Get brand. |
| PUT | v2/brands/{id} | write | general branding | Change brand. |
| DELETE | v2/brands/{id} | write | general branding | Delete brand. |
| GET | v2/brands/{id}/resources/editor | read | general branding | Get editor brand resource. |
| PUT | v2/brands/{id}/resources/editor | write | general branding | Create and edit editor brand resource. |
| DELETE | v2/brands/{id}/resources/editor | write | general branding | Delete editor brand resource. |
| GET | v2/brands/{id}/resources/general | read | general branding | Get general brand resource. |
| PUT | v2/brands/{id}/resources/general | write | general branding | Create and edit general brand resource. |
| DELETE | v2/brands/{id}/resources/general | write | general branding | Delete general brand resource. |
| GET | v2/brands/{id}/resources/logo | read | general branding | Get logo brand resource. |
| POST | v2/brands/{id}/resources/logo | write | general branding | Create logo brand resource. |
| PUT | v2/brands/{id}/resources/logo | write | general branding | Add and change logo from URL. |
| DELETE | v2/brands/{id}/resources/logo | write | general branding | Delete logo brand resource. |
| GET | v2/brands/{id}/resources/send-invite | read | general branding | Get send invite brand resource. |
| PUT | v2/brands/{id}/resources/send-invite | write | general branding | Create and edit send invite brand resource. |
| DELETE | v2/brands/{id}/resources/send-invite | write | general branding | Delete send invite brand resource. |
| GET | v2/document-groups/{id}/brand | read | general branding | Get brand of doc group. |
| PUT | v2/document-groups/{id}/brand | write | general branding | Assign brand to doc group. |
| DELETE | v2/document-groups/{id}/brand | write | general branding | Unassign brand from doc group. |
| GET | v2/documents/{id}/brand | read | general branding | Get brand of document. |
| PUT | v2/documents/{id}/brand | write | general branding | Assign brand to document. |
| DELETE | v2/documents/{id}/brand | write | general branding | Unassign brand from document. |
| GET | v2/brands/{id}/resources/email-general | read | general email branding | Get email general resource. |
| PUT | v2/brands/{id}/resources/email-general | write | general email branding | Add and edit email general branding. |
| DELETE | v2/brands/{id}/resources/email-general | write | general email branding | Delete email general resource. |
| GET | v2/brands/{id}/resources/email-invite | read | general email branding | Get email invite resource. |
| PUT | v2/brands/{id}/resources/email-invite | write | general email branding | Add and edit branding for email invite. |
| DELETE | v2/brands/{id}/resources/email-invite | write | general email branding | Delete email invite resource. |
| GET | v2/brands/{id}/resources/email-invite-canceled | read | general email branding | Get email canceled resource. |
| PUT | v2/brands/{id}/resources/email-invite-canceled | write | general email branding | Add and edit branding for canceled invite emails. |
| DELETE | v2/brands/{id}/resources/email-invite-canceled | write | general email branding | Delete email canceled resource. |
| GET | v2/brands/{id}/resources/email-invite-completed | read | general email branding | Get email completed resource. |
| PUT | v2/brands/{id}/resources/email-invite-completed | write | general email branding | Add and edit branding for completed emails. |
| DELETE | v2/brands/{id}/resources/email-invite-completed | write | general email branding | Delete email completed resource. |
| GET | v2/brands/{id}/resources/email-invite-reassign | read | general email branding | Get email reassign resource. |
| PUT | v2/brands/{id}/resources/email-invite-reassign | write | general email branding | Add and edit branding for reassign emails. |
| DELETE | v2/brands/{id}/resources/email-invite-reassign | write | general email branding | Delete email reassign resource. |
| GET | v2/brands/{id}/resources/email-invite-reminder | read | general email branding | Get email reminder resource. |
| PUT | v2/brands/{id}/resources/email-invite-reminder | write | general email branding | Add and edit branding for reminder emails. |
| DELETE | v2/brands/{id}/resources/email-invite-reminder | write | general email branding | Delete email reminder resource. |
| GET | v2/brands/{id}/resources/email-logo | read | general email branding | Get email logo brand resource. |
| POST | v2/brands/{id}/resources/email-logo | write | general email branding | Create email logo brand resource. |
| PUT | v2/brands/{id}/resources/email-logo | write | general email branding | Add and update email logo for brand from URL. |
| DELETE | v2/brands/{id}/resources/email-logo | write | general email branding | Delete email logo brand resource. |
| POST | team/{id}/admin | write | manage admins | Grant admin permissions. |
| DELETE | team/{id}/admin/{id} | write | manage admins | Cancel admin permissions. |
| POST | team/{id}/transferownership/{id} | write | manage admins | Change team primary admin. |
| GET | v2/teams/{id}/admins | read | manage admins | Get team admins. |
| GET | v2/event-subscriptions | read | manage event subscriptions | Get list of event subscriptions. |
| POST | v2/event-subscriptions | write | manage event subscriptions | Create event subscription. |
| GET | v2/event-subscriptions/{id} | read | manage event subscriptions | Get subscription info. |
| PUT | v2/event-subscriptions/{id} | write | manage event subscriptions | Edit event subscription. |
| DELETE | v2/event-subscriptions/{id} | write | manage event subscriptions | Delete event subscription. |
| PUT | v2/event-subscriptions/{id}/activate | write | manage event subscriptions | Activate event subscription. |
| PUT | v2/event-subscriptions/{id}/deactivate | write | manage event subscriptions | Deactivate event subscription. |
| POST | team | write | manage team | Create a team. |
| GET | team/{id} | read | manage team | Get team. |
| PUT | team/{id} | write | manage team | Rename team. |
| DELETE | team/{id} | write | manage team | Delete team. |
| GET | v2/teams | read | manage team | Get user's teams. |
| GET | team/{id}/request | read | manage users | Get team invite. |
| POST | team/{id}/request | write | manage users | Invite user to a team. |
| PUT | team/{id}/request | write | manage users | Accept or decline invitation to a team. |
| DELETE | team/{id}/user/{id} | write | manage users | Delete user from team. |
| GET | v2/teams/{id}/members | read | manage users | Get team members. |
| PATCH | v2/teams/{id}/request | write | manage users | Update team invite status. |
| POST | oauth2/terminate | write | oauth2 | Terminate access token. |
| GET | oauth2/token | write | oauth2 | Verify access token. Kept out of read: it returns details of the access token. |
| POST | oauth2/token | write | oauth2 | Generate access token. |
| GET | oauth2/userauth | write | oauth2 | Get authorization code via redirect. Kept out of read: it issues an authorization code. |
| GET | v2/organizations/{id}/email-footers | read | org email footer | Get all email footers. |
| POST | v2/organizations/{id}/email-footers | write | org email footer | Create email footer. |
| GET | v2/organizations/{id}/email-footers/{id} | read | org email footer | Get email footer text. |
| PUT | v2/organizations/{id}/email-footers/{id} | write | org email footer | Update email footer. |
| GET | v2/organizations | read | organization | Get admin's organizations. |
| POST | v2/organizations | write | organization | Create organization. |
| PUT | v2/organizations/{id} | write | organization | Rename organization. |
| DELETE | v2/organizations/{id} | write | organization | Delete organization. |
| GET | v2/organizations/{id}/activity | read | organization | Get organization activity. |
| GET | v2/organizations/{id}/admins | read | organization | Get the list of admins. |
| POST | v2/organizations/{id}/admins | write | organization | Add moderator or admin. |
| PUT | v2/organizations/{id}/admins/{id} | write | organization | Change admin/moderator role. |
| DELETE | v2/organizations/{id}/admins/{id} | write | organization | Remove admin/moderator. |
| POST | v2/organizations/{id}/admins/{id}/accept | write | organization | Accept invite to be admin. |
| POST | v2/organizations/{id}/admins/{id}/decline | write | organization | Decline invite to be admin. |
| GET | v2/organizations/{id}/allowed-team-admins | read | organization | Get allowed team admins. |
| POST | v2/organizations/{id}/allowed-team-admins | write | organization | Set an allowed team admin. |
| PUT | v2/organizations/{id}/allowed-team-admins | write | organization | Activate/deactivate allowed team admins. |
| GET | v2/organizations/{id}/documents/search | read | organization | Get user's documents. |
| POST | v2/organizations/{id}/logo | write | organization | Upload organization logo. |
| DELETE | v2/organizations/{id}/logo | write | organization | Delete organization logo. |
| GET | v2/organizations/{id}/members | read | organization | Get the list of members. |
| POST | v2/organizations/{id}/members | write | organization | Add members. |
| GET | v2/organizations/{id}/members/last-logins | read | organization | Get members' last logins. |
| POST | v2/organizations/{id}/members/last-logins/export | write | organization | Export last logins of members. |
| DELETE | v2/organizations/{id}/members/{id} | write | organization | Remove members. |
| POST | v2/organizations/{id}/members/{id}/accept | write | organization | Accept invite to organization. |
| POST | v2/organizations/{id}/members/{id}/decline | write | organization | Decline invite to organization. |
| PUT | v2/organizations/{id}/move | write | organization | Move users across organizations. |
| GET | v2/organizations/{id}/settings | read | organization | Get organization settings. |
| PUT | v2/organizations/{id}/settings | write | organization | Update organization settings. |
| GET | v2/organizations/{id}/users-activity | read | organization | Get users' activity. |
| POST | v2/organizations/{id}/users-activity/export | write | organization | Export last activity of members. |
| GET | v2/organizations/{id}/brand | read | organization branding | Get brand assigned to organization. |
| PUT | v2/organizations/{id}/brand | write | organization branding | Assign brand to organization. |
| DELETE | v2/organizations/{id}/brand | write | organization branding | Unassign brand from organization. |
| GET | v2/organizations/{id}/brands | read | organization branding | Get organization brands. |
| POST | v2/organizations/{id}/brands | write | organization branding | Create organization brand. |
| GET | v2/organizations/{id}/brands/{id} | read | organization branding | Get an organization brand. |
| PUT | v2/organizations/{id}/brands/{id} | write | organization branding | Update an organization brand. |
| DELETE | v2/organizations/{id}/brands/{id} | write | organization branding | Delete an organization brand. |
| GET | v2/organizations/{id}/brands/{id}/resources/editor | read | organization branding | Get org editor brand resource. |
| PUT | v2/organizations/{id}/brands/{id}/resources/editor | write | organization branding | Create org editor brand resource. |
| DELETE | v2/organizations/{id}/brands/{id}/resources/editor | write | organization branding | Delete org editor brand resource. |
| GET | v2/organizations/{id}/brands/{id}/resources/email | read | organization branding | Get org email brand resource. |
| PUT | v2/organizations/{id}/brands/{id}/resources/email | write | organization branding | Create org email brand resource. |
| DELETE | v2/organizations/{id}/brands/{id}/resources/email | write | organization branding | Delete org email brand resource. |
| GET | v2/organizations/{id}/brands/{id}/resources/general | read | organization branding | Get org general brand resource. |
| PUT | v2/organizations/{id}/brands/{id}/resources/general | write | organization branding | Create org general brand resource. |
| DELETE | v2/organizations/{id}/brands/{id}/resources/general | write | organization branding | Delete org general brand resource. |
| GET | v2/organizations/{id}/brands/{id}/resources/logo | read | organization branding | Get org logo brand resource. |
| POST | v2/organizations/{id}/brands/{id}/resources/logo | write | organization branding | Create org logo brand resource. |
| DELETE | v2/organizations/{id}/brands/{id}/resources/logo | write | organization branding | Delete org logo brand resource. |
| POST | organizations/{id}/merchantaccount | write | request payments | Connect to merchant account. |
| GET | organizations/{id}/merchantaccount/{id} | read | request payments | Get merchant account. |
| DELETE | organizations/{id}/merchantaccount/{id} | write | request payments | Delete merchant account. |
| POST | v2/merchant-accounts | write | request payments | Connect to personal merchant account. |
| GET | v2/merchant-accounts/{id} | read | request payments | Get personal merchant account. |
| DELETE | v2/merchant-accounts/{id} | write | request payments | Delete personal merchant account. |
| POST | documentgroup/{id}/scheduled-invite | write | scheduled doc group invite | Create scheduled invite. |
| PUT | documentgroup/{id}/scheduled-invite | write | scheduled doc group invite | Update scheduled invite. |
| DELETE | documentgroup/{id}/scheduled-invite | write | scheduled doc group invite | Cancel scheduled invite. |
| POST | documentgroup/{id}/scheduled-invite/send | write | scheduled doc group invite | Send scheduled invite. |
| POST | document/{id}/scheduled-invite | write | scheduled document invite | Create scheduled invite. |
| PUT | document/{id}/scheduled-invite | write | scheduled document invite | Update scheduled invite. |
| DELETE | document/{id}/scheduled-invite | write | scheduled document invite | Cancel scheduled invite. |
| POST | document/{id}/scheduled-invite/send | write | scheduled document invite | Send scheduled invite. |
| GET | v2/search | read | search | Search for documents, templates, and document groups. |
| POST | link | write | signing link | Create signing link. |
| GET | v2/application/signing-links | write | signing link | Get signing links. Kept out of read: it returns signing links that grant access to sign. |
| PUT | v2/application/signing-links/{id} | write | signing link | Activate/deactivate signing link. |
| POST | v2/document-groups/{id}/signing-links | write | signing link | Create/edit signing link for doc group. |
| POST | document/{id}/integration/object/smartfields | write | smart fields | Prefill smart fields. |
| GET | document/{id}/integration_objects | read | smart fields | Get smart fields from template. |
| POST | document/{id}/integration_objects | write | smart fields | Add smart fields to template. |
| DELETE | document/{id}/integration_objects | write | smart fields | Delete smart fields from template. |
| POST | team/{id}/shared/document/folder | write | team folders | Enable Documents folder. |
| DELETE | team/{id}/shared/document/folder | write | team folders | Disable Documents folder. |
| GET | document/{id}/template/routing/detail | read | template | Get template recipients. |
| PUT | document/{id}/template/routing/detail | write | template | Edit template recipients. |
| POST | import/document-templates | write | template | Import template from DocuSign. |
| POST | template | write | template | Create template. |
| POST | template/{id}/bulkinvite | write | template | Bulk invite. |
| POST | template/{id}/copy | write | template | Create document from template. |
| GET | v2/templates/{id}/copies | read | template | Get list of documents from template. |
| POST | v2/templates/{id}/copy | write | template | Duplicate a template. |
| POST | v2/templates/{id}/roles | write | template | Share template. |
| GET | v2/templates/{id}/roles/{id} | read | template | Get user role for template. |
| PUT | v2/templates/{id}/roles/{id} | write | template | Update role for template. |
| DELETE | v2/templates/{id}/roles/{id} | write | template | Remove access to template. |
| GET | folder | read | user | Get the root folders. |
| GET | user | read | user | Get user info. |
| POST | user | write | user | Create user. |
| PUT | user | write | user | Change user details. |
| GET | user/documents | read | user | Get user documents. |
| GET | user/documentsv2 | read | user | Get modified documents. |
| POST | user/forgotpassword | write | user | Reset password. |
| POST | user/verifyemail | write | user | Send verification email. |
| GET | v2/crm/contacts/{id}/users | read | users | Get users by contact. |
| PUT | v2/crm/contacts/{id}/users | write | users | Share contact with other users. |
| DELETE | v2/crm/contacts/{id}/users/{id} | write | users | Revoke access to shared contact. |
| GET | v2/crm/users | read | users | Get the list of CRM users. |
| GET | event_subscription | read | webhooks 1 | Get event subscription. |
| POST | event_subscription | write | webhooks 1 | Create event subscription. |
| DELETE | event_subscription/{id} | write | webhooks 1 | Delete event subscription. |
