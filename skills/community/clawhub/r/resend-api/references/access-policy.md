# Resend access policy

An access policy limits which endpoints Resend connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/resend#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Resend: its 57 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create resend --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api-keys"},
    {"method": "GET", "path": "audiences"},
    {"method": "GET", "path": "audiences/{id}"},
    {"method": "GET", "path": "automations"},
    {"method": "GET", "path": "automations/{id}"},
    {"method": "GET", "path": "automations/{id}/runs"},
    {"method": "GET", "path": "automations/{id}/runs/{id}"},
    {"method": "GET", "path": "broadcasts"},
    {"method": "GET", "path": "broadcasts/{id}"},
    {"method": "GET", "path": "broadcasts/{id}/clicked-links"},
    {"method": "GET", "path": "broadcasts/{id}/recipients"},
    {"method": "GET", "path": "contact-properties"},
    {"method": "GET", "path": "contact-properties/{id}"},
    {"method": "GET", "path": "contacts"},
    {"method": "GET", "path": "contacts/imports"},
    {"method": "GET", "path": "contacts/imports/{id}"},
    {"method": "GET", "path": "contacts/{id}"},
    {"method": "GET", "path": "contacts/{id}/segments"},
    {"method": "GET", "path": "contacts/{id}/topics"},
    {"method": "GET", "path": "domains"},
    {"method": "GET", "path": "domains/{id}"},
    {"method": "GET", "path": "domains/{id}/claim"},
    {"method": "GET", "path": "emails"},
    {"method": "GET", "path": "emails/metrics"},
    {"method": "GET", "path": "emails/receiving"},
    {"method": "GET", "path": "emails/receiving/{id}"},
    {"method": "GET", "path": "emails/{id}"},
    {"method": "GET", "path": "events"},
    {"method": "GET", "path": "events/{id}"},
    {"method": "GET", "path": "inboxes"},
    {"method": "GET", "path": "inboxes/{id}"},
    {"method": "GET", "path": "inboxes/{id}/agent"},
    {"method": "GET", "path": "inboxes/{id}/drafts"},
    {"method": "GET", "path": "inboxes/{id}/drafts/{id}"},
    {"method": "GET", "path": "inboxes/{id}/labels"},
    {"method": "GET", "path": "inboxes/{id}/threads"},
    {"method": "GET", "path": "inboxes/{id}/threads/search"},
    {"method": "GET", "path": "inboxes/{id}/threads/{id}"},
    {"method": "GET", "path": "inboxes/{id}/threads/{id}/emails"},
    {"method": "GET", "path": "inboxes/{id}/threads/{id}/emails/{id}"},
    {"method": "GET", "path": "logs"},
    {"method": "GET", "path": "logs/{id}"},
    {"method": "GET", "path": "oauth/grants"},
    {"method": "GET", "path": "segments"},
    {"method": "GET", "path": "segments/{id}"},
    {"method": "GET", "path": "segments/{id}/contacts"},
    {"method": "GET", "path": "suppressions"},
    {"method": "GET", "path": "suppressions/{id}"},
    {"method": "GET", "path": "templates"},
    {"method": "GET", "path": "templates/{id}"},
    {"method": "GET", "path": "topics"},
    {"method": "GET", "path": "topics/{id}"},
    {"method": "GET", "path": "usage"},
    {"method": "GET", "path": "webhooks"},
    {"method": "GET", "path": "webhooks/{id}/events"},
    {"method": "GET", "path": "webhooks/{id}/events/{id}"},
    {"method": "GET", "path": "webhooks/{id}/events/{id}/attempts"}
  ],
  "deny": []
}
```

## Endpoints

The Resend endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api-keys | read | api-keys | Retrieve a list of API keys. |
| POST | api-keys | write | api-keys | Create a new API key. |
| PATCH | api-keys/{id} | write | api-keys | Update an existing API key. |
| DELETE | api-keys/{id} | write | api-keys | Remove an existing API key. |
| GET | audiences | read | audiences | Retrieve a list of audiences. |
| POST | audiences | write | audiences | Create a list of contacts. |
| GET | audiences/{id} | read | audiences | Retrieve a single audience. |
| DELETE | audiences/{id} | write | audiences | Remove an existing audience. |
| GET | automations | read | automations | Retrieve a list of automations. |
| POST | automations | write | automations | Create an automation. |
| GET | automations/{id} | read | automations | Retrieve a single automation. |
| PATCH | automations/{id} | write | automations | Update an automation. |
| DELETE | automations/{id} | write | automations | Delete an automation. |
| POST | automations/{id}/duplicate | write | automations | Duplicate an automation. |
| GET | automations/{id}/runs | read | automations | Retrieve a list of automation runs. |
| GET | automations/{id}/runs/{id} | read | automations | Retrieve a single automation run. |
| POST | automations/{id}/runs/{id}/cancel | write | automations | Cancel an automation run. |
| POST | automations/{id}/stop | write | automations | Stop an automation. |
| GET | broadcasts | read | broadcasts | Retrieve a list of broadcasts. |
| POST | broadcasts | write | broadcasts | Create a broadcast. |
| GET | broadcasts/{id} | read | broadcasts | Retrieve a single broadcast. |
| PATCH | broadcasts/{id} | write | broadcasts | Update an existing broadcast. |
| DELETE | broadcasts/{id} | write | broadcasts | Remove an existing broadcast that is in the draft status. |
| POST | broadcasts/{id}/cancel | write | broadcasts | Cancel a broadcast. |
| GET | broadcasts/{id}/clicked-links | read | broadcasts | Retrieve a broadcast's clicked links. |
| POST | broadcasts/{id}/duplicate | write | broadcasts | Duplicate a broadcast. |
| GET | broadcasts/{id}/recipients | read | broadcasts | Retrieve broadcast recipients. |
| POST | broadcasts/{id}/send | write | broadcasts | Send or schedule a broadcast. |
| GET | contact-properties | read | contact-properties | Retrieve a list of contact properties. |
| POST | contact-properties | write | contact-properties | Create a new contact property. |
| GET | contact-properties/{id} | read | contact-properties | Retrieve a single contact property. |
| PATCH | contact-properties/{id} | write | contact-properties | Update an existing contact property. |
| DELETE | contact-properties/{id} | write | contact-properties | Remove an existing contact property. |
| GET | contacts | read | contacts | Retrieve a list of contacts. |
| POST | contacts | write | contacts | Create a new contact. |
| GET | contacts/imports | read | contacts | Retrieve a list of contact imports. |
| POST | contacts/imports | write | contacts | Create a contact import. |
| GET | contacts/imports/{id} | read | contacts | Retrieve a single contact import. |
| GET | contacts/{id} | read | contacts | Retrieve a single contact by ID or email. |
| PATCH | contacts/{id} | write | contacts | Update a single contact by ID or email. |
| DELETE | contacts/{id} | write | contacts | Remove an existing contact by ID or email. |
| GET | contacts/{id}/segments | read | contacts | Retrieve a list of segments for a contact. |
| POST | contacts/{id}/segments/{id} | write | contacts | Add a contact to a segment. |
| DELETE | contacts/{id}/segments/{id} | write | contacts | Remove a contact from a segment. |
| GET | contacts/{id}/topics | read | contacts | Retrieve topics for a contact. |
| PATCH | contacts/{id}/topics | write | contacts | Update topics for a contact. |
| GET | domains | read | domains | Retrieve a list of domains. |
| POST | domains | write | domains | Create a new domain. |
| POST | domains/claim | write | domains | Claim a domain. |
| GET | domains/{id} | read | domains | Retrieve a single domain. |
| PATCH | domains/{id} | write | domains | Update an existing domain. |
| DELETE | domains/{id} | write | domains | Remove an existing domain. |
| GET | domains/{id}/claim | read | domains | Retrieve a domain claim. |
| POST | domains/{id}/claim/verify | write | domains | Verify a domain claim. |
| POST | domains/{id}/forge | write | domains | Enable Forge for a domain. |
| POST | domains/{id}/verify | write | domains | Verify an existing domain. |
| GET | emails | read | emails | Retrieve a list of emails. |
| POST | emails | write | emails | Send an email. |
| POST | emails/batch | write | emails | Trigger up to 100 batch emails at once. |
| GET | emails/metrics | read | emails | Retrieve account-level email metrics. |
| GET | emails/receiving | read | emails | Retrieve a list of received emails. |
| GET | emails/receiving/{id} | read | emails | Retrieve a single received email. |
| GET | emails/receiving/{id}/attachments | write | emails | Retrieve a list of attachments for a received email. Kept out of read: response includes pre-signed attachment download_url values. |
| GET | emails/receiving/{id}/attachments/{id} | write | emails | Retrieve a single attachment for a received email. Kept out of read: response includes a pre-signed attachment download_url. |
| GET | emails/{id} | read | emails | Retrieve a single email. |
| PATCH | emails/{id} | write | emails | Update a single email. |
| GET | emails/{id}/attachments | write | emails | Retrieve a list of attachments for a sent email. Kept out of read: response includes pre-signed attachment download_url values. |
| GET | emails/{id}/attachments/{id} | write | emails | Retrieve a single attachment for a sent email. Kept out of read: response includes a pre-signed attachment download_url. |
| POST | emails/{id}/cancel | write | emails | Cancel the schedule of the e-mail. |
| POST | emails/{id}/share | write | emails | Create a shareable link for a sent or received email. |
| GET | events | read | events | Retrieve a list of events. |
| POST | events | write | events | Create an event. |
| POST | events/send | write | events | Send an event. |
| GET | events/{id} | read | events | Retrieve a single event. |
| PATCH | events/{id} | write | events | Update an event. |
| DELETE | events/{id} | write | events | Delete an event. |
| GET | inboxes | read | inboxes | Retrieve a list of inboxes. |
| POST | inboxes | write | inboxes | Create an inbox. |
| GET | inboxes/{id} | read | inboxes | Retrieve a single inbox by ID or email address. |
| PATCH | inboxes/{id} | write | inboxes | Update an existing inbox by ID or email address. |
| DELETE | inboxes/{id} | write | inboxes | Remove an existing inbox by ID or email address. |
| GET | inboxes/{id}/agent | read | inboxes | Retrieve the agent settings for an inbox. |
| PATCH | inboxes/{id}/agent | write | inboxes | Update the agent settings for an inbox. |
| GET | inboxes/{id}/drafts | read | inboxes | Retrieve a list of drafts. |
| POST | inboxes/{id}/drafts | write | inboxes | Create a draft. |
| GET | inboxes/{id}/drafts/{id} | read | inboxes | Retrieve a single draft. |
| PATCH | inboxes/{id}/drafts/{id} | write | inboxes | Update an existing draft. |
| DELETE | inboxes/{id}/drafts/{id} | write | inboxes | Remove an existing draft. |
| POST | inboxes/{id}/drafts/{id}/send | write | inboxes | Send a draft. |
| GET | inboxes/{id}/labels | read | inboxes | Retrieve a list of inbox labels. |
| POST | inboxes/{id}/labels | write | inboxes | Create a label on an inbox. |
| PATCH | inboxes/{id}/labels/{id} | write | inboxes | Update an existing inbox label. |
| DELETE | inboxes/{id}/labels/{id} | write | inboxes | Remove an existing inbox label. |
| GET | inboxes/{id}/threads | read | inboxes | Retrieve a list of inbox threads. |
| GET | inboxes/{id}/threads/search | read | inboxes | Search the threads of an inbox. |
| GET | inboxes/{id}/threads/{id} | read | inboxes | Retrieve a single inbox thread. |
| PATCH | inboxes/{id}/threads/{id} | write | inboxes | Update an existing inbox thread. |
| DELETE | inboxes/{id}/threads/{id} | write | inboxes | Remove an existing inbox thread. |
| GET | inboxes/{id}/threads/{id}/emails | read | inboxes | Retrieve a list of thread emails. |
| GET | inboxes/{id}/threads/{id}/emails/{id} | read | inboxes | Retrieve a single thread email. |
| POST | inboxes/{id}/threads/{id}/emails/{id}/forward | write | inboxes | Forward a thread email. |
| POST | inboxes/{id}/threads/{id}/emails/{id}/reply | write | inboxes | Reply to a thread email. |
| POST | inboxes/{id}/threads/{id}/labels | write | inboxes | Add labels to an inbox thread. |
| PUT | inboxes/{id}/threads/{id}/labels | write | inboxes | Set the labels of an inbox thread. |
| DELETE | inboxes/{id}/threads/{id}/labels/{id} | write | inboxes | Remove a label from an inbox thread. |
| GET | logs | read | logs | Retrieve a list of logs. |
| GET | logs/{id} | read | logs | Retrieve a single log. |
| GET | oauth/grants | read | oauth | Retrieve a list of OAuth grants. |
| DELETE | oauth/grants/{id} | write | oauth | Revoke an OAuth grant. |
| GET | segments | read | segments | Retrieve a list of segments. |
| POST | segments | write | segments | Create a new segment. |
| GET | segments/{id} | read | segments | Retrieve a single segment. |
| PATCH | segments/{id} | write | segments | Update an existing segment. |
| DELETE | segments/{id} | write | segments | Remove an existing segment. |
| GET | segments/{id}/contacts | read | segments | Retrieve a list of contacts in a segment. |
| GET | suppressions | read | suppressions | Retrieve a list of suppressions. |
| POST | suppressions | write | suppressions | Create a suppression. |
| POST | suppressions/batch/add | write | suppressions | Add up to 100 suppressions at once. |
| POST | suppressions/batch/remove | write | suppressions | Remove up to 100 suppressions at once. |
| GET | suppressions/{id} | read | suppressions | Retrieve a single suppression by ID or email. |
| DELETE | suppressions/{id} | write | suppressions | Remove a single suppression by ID or email. |
| GET | templates | read | templates | Retrieve a list of templates. |
| POST | templates | write | templates | Create a template. |
| GET | templates/{id} | read | templates | Retrieve a single template. |
| PATCH | templates/{id} | write | templates | Update an existing template. |
| DELETE | templates/{id} | write | templates | Remove an existing template. |
| POST | templates/{id}/duplicate | write | templates | Duplicate a template. |
| POST | templates/{id}/publish | write | templates | Publish a template. |
| GET | topics | read | topics | Retrieve a list of topics. |
| POST | topics | write | topics | Create a new topic. |
| GET | topics/{id} | read | topics | Retrieve a single topic. |
| PATCH | topics/{id} | write | topics | Update an existing topic. |
| DELETE | topics/{id} | write | topics | Remove an existing topic. |
| GET | usage | read | usage | Retrieve account usage. |
| GET | webhooks | read | webhooks | Retrieve a list of webhooks. |
| POST | webhooks | write | webhooks | Create a new webhook. |
| GET | webhooks/{id} | write | webhooks | Retrieve a single webhook. Kept out of read: response includes the webhook signing_secret. |
| PATCH | webhooks/{id} | write | webhooks | Update an existing webhook. |
| DELETE | webhooks/{id} | write | webhooks | Remove an existing webhook. |
| GET | webhooks/{id}/events | read | webhooks | Retrieve a list of webhook events. |
| GET | webhooks/{id}/events/{id} | read | webhooks | Retrieve a single webhook event. |
| GET | webhooks/{id}/events/{id}/attempts | read | webhooks | Retrieve a list of webhook event attempts. |
| POST | webhooks/{id}/events/{id}/replay | write | webhooks | Replay a webhook event. |
| POST | webhooks/{id}/signing-secret/rotate | write | webhooks | Rotate a webhook signing secret. |
