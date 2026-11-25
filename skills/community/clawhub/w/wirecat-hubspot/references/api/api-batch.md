<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# HubSpot API: Batch

## `hubspot api associations-batch-archive [options]`

- What: Remove associations
- Call: `POST /crm/associations/2026-03/{fromObjectType}/{toObjectType}/batch/archive`, effect: destructive
- Permission keys: `associations.delete`
- Body: `BatchInputPublicAssociationMultiArchive`, required

| Flag | Required | What |
|---|---|---|
| `--from-object-type <value>` | yes | fromObjectType |
| `--to-object-type <value>` | yes | toObjectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api associations-batch-associate-default [options]`

- What: Create Default Associations
- Call: `POST /crm/associations/2026-03/{fromObjectType}/{toObjectType}/batch/associate/default`, effect: write
- Permission keys: `associations.write`
- Body: `BatchInputPublicDefaultAssociationMultiPost`, required

| Flag | Required | What |
|---|---|---|
| `--from-object-type <value>` | yes | fromObjectType |
| `--to-object-type <value>` | yes | toObjectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api associations-batch-create [options]`

- What: Associate records (labelled)
- Call: `POST /crm/associations/2026-03/{fromObjectType}/{toObjectType}/batch/create`, effect: write
- Permission keys: `associations.write`
- Body: `BatchInputPublicAssociationMultiPost`, required

| Flag | Required | What |
|---|---|---|
| `--from-object-type <value>` | yes | fromObjectType |
| `--to-object-type <value>` | yes | toObjectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api associations-batch-labels-archive [options]`

- What: Delete Specific Labels
- Call: `POST /crm/associations/2026-03/{fromObjectType}/{toObjectType}/batch/labels/archive`, effect: destructive
- Permission keys: `associations.delete`
- Body: `BatchInputPublicAssociationMultiPost`, required

| Flag | Required | What |
|---|---|---|
| `--from-object-type <value>` | yes | fromObjectType |
| `--to-object-type <value>` | yes | toObjectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api associations-batch-read [options]`

- What: Retrieve associations
- Call: `POST /crm/associations/2026-03/{fromObjectType}/{toObjectType}/batch/read`, effect: read
- Body: `BatchInputPublicFetchAssociationsBatchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--from-object-type <value>` | yes | fromObjectType |
| `--to-object-type <value>` | yes | toObjectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api associations-default-replace [options]`

- What: put-/crm/objects/2026-03/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}_/crm/objects/2026-03/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}
- Call: `PUT /crm/objects/2026-03/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}`, effect: write
- Permission keys: `associations.write`

| Flag | Required | What |
|---|---|---|
| `--from-object-id <value>` | yes | fromObjectId |
| `--from-object-type <value>` | yes | fromObjectType |
| `--to-object-id <value>` | yes | toObjectId |
| `--to-object-type <value>` | yes | toObjectType |

## `hubspot api calls-batch-archive [options]`

- What: Archive a batch of calls by ID
- Call: `POST /crm/objects/2026-03/calls/batch/archive`, effect: destructive
- Permission keys: `calls.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api calls-batch-create [options]`

- What: Create a batch of calls
- Call: `POST /crm/objects/2026-03/calls/batch/create`, effect: write
- Permission keys: `calls.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api calls-batch-read [options]`

- What: Read a batch of calls by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/calls/batch/read`, effect: read
- Permission keys: `activities.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api calls-batch-update [options]`

- What: Update a batch of calls by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/calls/batch/update`, effect: write
- Permission keys: `calls.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api calls-batch-upsert [options]`

- What: Create or update a batch of calls by unique property values
- Call: `POST /crm/objects/2026-03/calls/batch/upsert`, effect: write
- Permission keys: `calls.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-batch-archive [options]`

- What: Archive a batch of companies
- Call: `POST /crm/objects/2026-03/companies/batch/archive`, effect: destructive
- Permission keys: `organizations.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-batch-create [options]`

- What: Create a batch of companies
- Call: `POST /crm/objects/2026-03/companies/batch/create`, effect: write
- Permission keys: `organizations.create`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-batch-read [options]`

- What: Retrieve a batch of companies
- Call: `POST /crm/objects/2026-03/companies/batch/read`, effect: read
- Permission keys: `organizations.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-batch-update [options]`

- What: Update a batch of companies
- Call: `POST /crm/objects/2026-03/companies/batch/update`, effect: write
- Permission keys: `organizations.update`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-batch-upsert [options]`

- What: Create or update a batch of companies by unique property values
- Call: `POST /crm/objects/2026-03/companies/batch/upsert`, effect: write
- Permission keys: `organizations.create`, `organizations.update`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-batch-archive [options]`

- What: Archive a batch of contacts
- Call: `POST /crm/objects/2026-03/contacts/batch/archive`, effect: destructive
- Permission keys: `people.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-batch-create [options]`

- What: Create a batch of contacts
- Call: `POST /crm/objects/2026-03/contacts/batch/create`, effect: write
- Permission keys: `people.create`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-batch-read [options]`

- What: Retrieve a batch of contacts
- Call: `POST /crm/objects/2026-03/contacts/batch/read`, effect: read
- Permission keys: `people.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-batch-update [options]`

- What: Update a batch of contacts
- Call: `POST /crm/objects/2026-03/contacts/batch/update`, effect: write
- Permission keys: `people.update`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-batch-upsert [options]`

- What: Create or update a batch of contacts
- Call: `POST /crm/objects/2026-03/contacts/batch/upsert`, effect: write
- Permission keys: `people.create`, `people.update`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-batch-archive [options]`

- What: Archive a batch of deals by ID
- Call: `POST /crm/objects/2026-03/0-3/batch/archive`, effect: destructive
- Permission keys: `deals.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-batch-create [options]`

- What: Create a batch of deals
- Call: `POST /crm/objects/2026-03/0-3/batch/create`, effect: write
- Permission keys: `deals.create`, `crm.assign-others`, `deals.move`, `deals.close`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-batch-read [options]`

- What: Read a batch of deals by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/0-3/batch/read`, effect: read
- Permission keys: `deals.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-batch-update [options]`

- What: Update a batch of deals by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/0-3/batch/update`, effect: write
- Permission keys: `deals.update`, `crm.assign-others`, `deals.move`, `deals.close`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-batch-upsert [options]`

- What: Create or update a batch of deals by unique property values
- Call: `POST /crm/objects/2026-03/0-3/batch/upsert`, effect: write
- Permission keys: `deals.create`, `deals.update`, `crm.assign-others`, `deals.move`, `deals.close`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-batch-archive [options]`

- What: Archive a batch of emails by ID
- Call: `POST /crm/objects/2026-03/emails/batch/archive`, effect: destructive
- Permission keys: `emails.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-batch-create [options]`

- What: Create a batch of emails
- Call: `POST /crm/objects/2026-03/emails/batch/create`, effect: write
- Permission keys: `emails.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-batch-read [options]`

- What: Read a batch of emails by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/emails/batch/read`, effect: read
- Permission keys: `activities.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-batch-update [options]`

- What: Update a batch of emails by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/emails/batch/update`, effect: write
- Permission keys: `emails.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-batch-upsert [options]`

- What: Create or update a batch of emails by unique property values
- Call: `POST /crm/objects/2026-03/emails/batch/upsert`, effect: write
- Permission keys: `emails.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-batch-archive [options]`

- What: Archive a batch of leads by ID
- Call: `POST /crm/objects/2026-03/leads/batch/archive`, effect: destructive
- Permission keys: `leads.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-batch-create [options]`

- What: Create a batch of leads
- Call: `POST /crm/objects/2026-03/leads/batch/create`, effect: write
- Permission keys: `leads.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-batch-read [options]`

- What: Read a batch of leads by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/leads/batch/read`, effect: read
- Permission keys: `leads.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-batch-update [options]`

- What: Update a batch of leads by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/leads/batch/update`, effect: write
- Permission keys: `leads.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-batch-upsert [options]`

- What: Create or update a batch of leads by unique property values
- Call: `POST /crm/objects/2026-03/leads/batch/upsert`, effect: write
- Permission keys: `leads.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-batch-archive [options]`

- What: Archive a batch of meetings by ID
- Call: `POST /crm/objects/2026-03/meetings/batch/archive`, effect: destructive
- Permission keys: `meetings.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-batch-create [options]`

- What: Create a batch of meetings
- Call: `POST /crm/objects/2026-03/meetings/batch/create`, effect: write
- Permission keys: `meetings.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-batch-read [options]`

- What: Read a batch of meetings by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/meetings/batch/read`, effect: read
- Permission keys: `activities.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-batch-update [options]`

- What: Update a batch of meetings by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/meetings/batch/update`, effect: write
- Permission keys: `meetings.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-batch-upsert [options]`

- What: Create or update a batch of meetings by unique property values
- Call: `POST /crm/objects/2026-03/meetings/batch/upsert`, effect: write
- Permission keys: `meetings.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-batch-archive [options]`

- What: Archive a batch of notes by ID
- Call: `POST /crm/objects/2026-03/notes/batch/archive`, effect: destructive
- Permission keys: `notes.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-batch-create [options]`

- What: Create a batch of notes
- Call: `POST /crm/objects/2026-03/notes/batch/create`, effect: write
- Permission keys: `notes.write`, `activities.create`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-batch-read [options]`

- What: Read a batch of notes by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/notes/batch/read`, effect: read
- Permission keys: `activities.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-batch-update [options]`

- What: Update a batch of notes by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/notes/batch/update`, effect: write
- Permission keys: `notes.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-batch-upsert [options]`

- What: Create or update a batch of notes by unique property values
- Call: `POST /crm/objects/2026-03/notes/batch/upsert`, effect: write
- Permission keys: `notes.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-batch-archive [options]`

- What: Archive a batch of properties
- Call: `POST /crm/properties/2026-03/{objectType}/batch/archive`, effect: destructive
- Permission keys: `fields.delete`
- Body: `BatchInputPropertyName`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of object whose properties are to be archived. This is a required parameter and identifies the specific object type within HubSpot. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-batch-create [options]`

- What: Create a batch of properties
- Call: `POST /crm/properties/2026-03/{objectType}/batch/create`, effect: write
- Permission keys: `fields.write`
- Body: `BatchInputPropertyCreate`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of CRM object for which the properties are being created, such as contacts, companies, or deals. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-batch-read [options]`

- What: Read a batch of properties
- Call: `POST /crm/properties/2026-03/{objectType}/batch/read`, effect: read
- Permission keys: `fields.list`
- Body: `BatchReadInputPropertyName`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of CRM object for which properties are being retrieved. This is a required path parameter. |
| `--locale <value>` | no | A string specifying the locale to use for the response. This can be used to tailor the response to a specific language or region. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-batch-archive [options]`

- What: Archive a batch of tasks by ID
- Call: `POST /crm/objects/2026-03/tasks/batch/archive`, effect: destructive
- Permission keys: `tasks.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-batch-create [options]`

- What: Create a batch of tasks
- Call: `POST /crm/objects/2026-03/tasks/batch/create`, effect: write
- Permission keys: `tasks.write`, `activities.create`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-batch-read [options]`

- What: Read a batch of tasks by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/tasks/batch/read`, effect: read
- Permission keys: `activities.list`
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-batch-update [options]`

- What: Update a batch of tasks by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/tasks/batch/update`, effect: write
- Permission keys: `tasks.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-batch-upsert [options]`

- What: Create or update a batch of tasks by unique property values
- Call: `POST /crm/objects/2026-03/tasks/batch/upsert`, effect: write
- Permission keys: `tasks.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-batch-archive [options]`

- What: Archive a batch of tickets by ID
- Call: `POST /crm/objects/2026-03/tickets/batch/archive`, effect: destructive
- Permission keys: `tickets.delete`
- Body: `BatchInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-batch-create [options]`

- What: Create a batch of tickets
- Call: `POST /crm/objects/2026-03/tickets/batch/create`, effect: write
- Permission keys: `tickets.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-batch-read [options]`

- What: Read a batch of tickets by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/tickets/batch/read`, effect: read
- Body: `BatchReadInputSimplePublicObjectId`, required

| Flag | Required | What |
|---|---|---|
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-batch-update [options]`

- What: Update a batch of tickets by internal ID, or unique property values
- Call: `POST /crm/objects/2026-03/tickets/batch/update`, effect: write
- Permission keys: `tickets.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-batch-upsert [options]`

- What: Create or update a batch of tickets by unique property values
- Call: `POST /crm/objects/2026-03/tickets/batch/upsert`, effect: write
- Permission keys: `tickets.write`, `crm.assign-others`
- Body: `BatchInputSimplePublicObjectBatchInputUpsert`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
