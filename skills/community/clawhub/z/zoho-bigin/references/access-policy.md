# Zoho Bigin access policy

An access policy limits which endpoints Zoho Bigin connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-bigin#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho Bigin: its 29 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-bigin --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "bigin/v2/{id}/{id}/Attachments"},
    {"method": "GET", "path": "bigin/v2/{id}/{id}/Attachments/{id}"},
    {"method": "GET", "path": "bigin/bulk/v2/read/{id}"},
    {"method": "GET", "path": "bigin/bulk/v2/read/{id}/result"},
    {"method": "POST", "path": "bigin/v2/coql"},
    {"method": "GET", "path": "bigin/v2/settings/emails/actions/from_addresses"},
    {"method": "GET", "path": "bigin/v2/files"},
    {"method": "GET", "path": "bigin/v2/settings/custom_views"},
    {"method": "GET", "path": "bigin/v2/settings/custom_views/{id}"},
    {"method": "GET", "path": "bigin/v2/settings/fields"},
    {"method": "GET", "path": "bigin/v2/settings/layouts"},
    {"method": "GET", "path": "bigin/v2/settings/modules"},
    {"method": "GET", "path": "bigin/v2/settings/modules/{id}"},
    {"method": "GET", "path": "bigin/v2/settings/related_lists"},
    {"method": "GET", "path": "bigin/v2/Notes"},
    {"method": "GET", "path": "bigin/v2/{id}/{id}/Notes"},
    {"method": "GET", "path": "bigin/v2/actions/watch"},
    {"method": "GET", "path": "bigin/v2/org"},
    {"method": "GET", "path": "bigin/v2/settings/profiles"},
    {"method": "GET", "path": "bigin/v2/{id}"},
    {"method": "GET", "path": "bigin/v2/{id}/actions/count"},
    {"method": "GET", "path": "bigin/v2/{id}/deleted"},
    {"method": "GET", "path": "bigin/v2/{id}/search"},
    {"method": "GET", "path": "bigin/v2/{id}/{id}"},
    {"method": "GET", "path": "bigin/v2/{id}/{id}/{id}"},
    {"method": "GET", "path": "bigin/v2/settings/roles"},
    {"method": "GET", "path": "bigin/v2/settings/tags"},
    {"method": "GET", "path": "bigin/v2/users"},
    {"method": "GET", "path": "bigin/v2/users/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho Bigin endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | bigin/v2/{id}/{id}/Attachments | read | attachments | Get the list of attachments of a record. |
| POST | bigin/v2/{id}/{id}/Attachments | write | attachments | Upload an attachment to a record. |
| GET | bigin/v2/{id}/{id}/Attachments/{id} | read | attachments | Download an attachment of a record. |
| DELETE | bigin/v2/{id}/{id}/Attachments/{id} | write | attachments | Delete an attachment of a record. |
| POST | bigin/bulk/v2/read | write | bulk-read | Create a bulk read job to export records. Kept out of read: creates a bulk export job. |
| GET | bigin/bulk/v2/read/{id} | read | bulk-read | Get the details of a bulk read job. |
| GET | bigin/bulk/v2/read/{id}/result | read | bulk-read | Download the result of a bulk read job. |
| POST | bigin/v2/coql | read | coql | Query records with a COQL SELECT statement. |
| GET | bigin/v2/settings/emails/actions/from_addresses | read | emails | Get the configured from-addresses. |
| POST | bigin/v2/{id}/{id}/actions/send_mail | write | emails | Send an email to a record. |
| GET | bigin/v2/files | read | files | Get a file using its encrypted ID. |
| POST | bigin/v2/files | write | files | Upload a file. |
| GET | bigin/v2/settings/custom_views | read | metadata | Get the custom views of a module. |
| GET | bigin/v2/settings/custom_views/{id} | read | metadata | Get a specific custom view of a module. |
| GET | bigin/v2/settings/fields | read | metadata | Get the metadata of the fields in a module. |
| GET | bigin/v2/settings/layouts | read | metadata | Get the metadata of the layouts of a module. |
| GET | bigin/v2/settings/modules | read | metadata | Get the metadata of all modules. |
| GET | bigin/v2/settings/modules/{id} | read | metadata | Get the metadata of a specific module. |
| GET | bigin/v2/settings/related_lists | read | metadata | Get the related lists of a module. |
| GET | bigin/v2/Notes | read | notes | Get the notes of all records. |
| POST | bigin/v2/Notes | write | notes | Add notes to records. |
| DELETE | bigin/v2/Notes | write | notes | Delete notes. |
| GET | bigin/v2/{id}/{id}/Notes | read | notes | Get the notes of a specific record. |
| POST | bigin/v2/{id}/{id}/Notes | write | notes | Add notes to a specific record. |
| PUT | bigin/v2/{id}/{id}/Notes/{id} | write | notes | Update a note of a record. |
| DELETE | bigin/v2/{id}/{id}/Notes/{id} | write | notes | Delete a note of a record. |
| GET | bigin/v2/actions/watch | read | notifications | Get the notification channel details. |
| POST | bigin/v2/actions/watch | write | notifications | Enable notifications. |
| PUT | bigin/v2/actions/watch | write | notifications | Update notification channel details. |
| PATCH | bigin/v2/actions/watch | write | notifications | Update or disable specific notification events. |
| DELETE | bigin/v2/actions/watch | write | notifications | Disable notifications. |
| GET | bigin/v2/org | read | org | Get the organization details. |
| GET | bigin/v2/settings/profiles | read | profiles | Get the list of profiles. |
| GET | bigin/v2/{id} | read | records | Get the list of records from a module. |
| POST | bigin/v2/{id} | write | records | Add records to a module. |
| PUT | bigin/v2/{id} | write | records | Update records in a module. |
| DELETE | bigin/v2/{id} | write | records | Delete records from a module. |
| GET | bigin/v2/{id}/actions/count | read | records | Returns the record count of a module. |
| GET | bigin/v2/{id}/deleted | read | records | Get the list of deleted records of a module. |
| GET | bigin/v2/{id}/search | read | records | Search records in a module by criteria, email, phone or word. |
| POST | bigin/v2/{id}/upsert | write | records | Insert or update records by duplicate-check fields. |
| GET | bigin/v2/{id}/{id} | read | records | Get a record from a module by ID. |
| PUT | bigin/v2/{id}/{id} | write | records | Update a specific record. |
| DELETE | bigin/v2/{id}/{id} | write | records | Delete a specific record. |
| GET | bigin/v2/{id}/{id}/{id} | read | related-records | Get the records in a related list of a record. |
| PUT | bigin/v2/{id}/{id}/{id} | write | related-records | Update the records in a related list of a record. |
| GET | bigin/v2/settings/roles | read | roles | Get the list of roles. |
| GET | bigin/v2/settings/tags | read | tags | Get the tags of a module. |
| POST | bigin/v2/settings/tags | write | tags | Add new tags to a module. |
| PUT | bigin/v2/settings/tags | write | tags | Update multiple tags. |
| PUT | bigin/v2/settings/tags/{id} | write | tags | Update a specific tag. |
| DELETE | bigin/v2/settings/tags/{id} | write | tags | Delete a tag. |
| POST | bigin/v2/{id}/actions/remove_tags | write | tags | Remove tags from multiple records. |
| POST | bigin/v2/{id}/{id}/actions/remove_tags | write | tags | Remove tags from a specific record. |
| GET | bigin/v2/users | read | users | Get the list of users. |
| GET | bigin/v2/users/{id} | read | users | Get a specific user. |
