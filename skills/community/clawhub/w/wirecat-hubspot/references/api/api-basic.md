<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# HubSpot API: Basic

## `hubspot api account-info-api-usage-daily-private-apps-list`

- What: Retrieve private app daily API usage
- Call: `GET /account-info/2026-03/api-usage/daily/private-apps`, effect: read

## `hubspot api account-info-details-list`

- What: Retrieve account details
- Call: `GET /account-info/2026-03/details`, effect: read

## `hubspot api associations-delete [options]`

- What: delete-/crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}_/crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}
- Call: `DELETE /crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`, effect: destructive
- Permission keys: `associations.delete`

| Flag | Required | What |
|---|---|---|
| `--object-id <value>` | yes | objectId |
| `--object-type <value>` | yes | objectType |
| `--to-object-id <value>` | yes | toObjectId |
| `--to-object-type <value>` | yes | toObjectType |

## `hubspot api associations-get [options]`

- What: Retrieve all associations by object type
- Call: `GET /crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}`, effect: read
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--object-id <value>` | yes | objectId |
| `--object-type <value>` | yes | objectType |
| `--to-object-type <value>` | yes | toObjectType |
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api associations-replace [options]`

- What: put-/crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}_/crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}
- Call: `PUT /crm/objects/2026-03/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}`, effect: write
- Permission keys: `associations.write`
- Body: `PutCrmObjects202603ObjectTypeObjectIdAssociationsToObjectTypeToObjectIdCrmObjects202603ObjectTypeObjectIdAssociationsToObjectTypeToObjectIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object-id <value>` | yes | objectId |
| `--object-type <value>` | yes | objectType |
| `--to-object-id <value>` | yes | toObjectId |
| `--to-object-type <value>` | yes | toObjectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api associations-usage-high-usage-report-update [options]`

- What: Report high usage
- Call: `POST /crm/associations/2026-03/usage/high-usage-report/{userId}`, effect: write
- Permission keys: `associations.write`

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | yes | userId |

## `hubspot api calls-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/calls`, effect: write
- Permission keys: `calls.write`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api calls-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/calls/{callId}`, effect: destructive
- Permission keys: `calls.delete`

| Flag | Required | What |
|---|---|---|
| `--call-id <value>` | yes | callId |

## `hubspot api calls-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/calls/{callId}`, effect: read
- Permission keys: `activities.list`

| Flag | Required | What |
|---|---|---|
| `--call-id <value>` | yes | callId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api calls-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/calls`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api calls-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/calls/{callId}`, effect: write
- Permission keys: `calls.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--call-id <value>` | yes | callId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-create [options]`

- What: Create a company
- Call: `POST /crm/objects/2026-03/companies`, effect: write
- Permission keys: `organizations.create`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api companies-delete [options]`

- What: Archive a company
- Call: `DELETE /crm/objects/2026-03/companies/{companyId}`, effect: destructive
- Permission keys: `organizations.delete`

| Flag | Required | What |
|---|---|---|
| `--company-id <value>` | yes | companyId |

## `hubspot api companies-get [options]`

- What: Retrieve a company
- Call: `GET /crm/objects/2026-03/companies/{companyId}`, effect: read
- Permission keys: `organizations.show`

| Flag | Required | What |
|---|---|---|
| `--company-id <value>` | yes | companyId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api companies-list [options]`

- What: Retrieve companies
- Call: `GET /crm/objects/2026-03/companies`, effect: read
- Permission keys: `organizations.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api companies-update [options]`

- What: Update a company
- Call: `PATCH /crm/objects/2026-03/companies/{companyId}`, effect: write
- Permission keys: `organizations.update`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--company-id <value>` | yes | companyId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-create [options]`

- What: Create a contact
- Call: `POST /crm/objects/2026-03/contacts`, effect: write
- Permission keys: `people.create`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api contacts-delete [options]`

- What: Archive a contact
- Call: `DELETE /crm/objects/2026-03/contacts/{contactId}`, effect: destructive
- Permission keys: `people.delete`

| Flag | Required | What |
|---|---|---|
| `--contact-id <value>` | yes | contactId |

## `hubspot api contacts-get [options]`

- What: Retrieve a contact
- Call: `GET /crm/objects/2026-03/contacts/{contactId}`, effect: read
- Permission keys: `people.show`

| Flag | Required | What |
|---|---|---|
| `--contact-id <value>` | yes | contactId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api contacts-list [options]`

- What: Retrieve contacts
- Call: `GET /crm/objects/2026-03/contacts`, effect: read
- Permission keys: `people.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api contacts-update [options]`

- What: Update a contact
- Call: `PATCH /crm/objects/2026-03/contacts/{contactId}`, effect: write
- Permission keys: `people.update`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--contact-id <value>` | yes | contactId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/0-3`, effect: write
- Permission keys: `deals.create`, `crm.assign-others`, `deals.move`, `deals.close`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/0-3/{dealId}`, effect: destructive
- Permission keys: `deals.delete`

| Flag | Required | What |
|---|---|---|
| `--deal-id <value>` | yes | dealId |

## `hubspot api deals-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/0-3/{dealId}`, effect: read
- Permission keys: `deals.show`

| Flag | Required | What |
|---|---|---|
| `--deal-id <value>` | yes | dealId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api deals-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/0-3`, effect: read
- Permission keys: `deals.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api deals-merge [options]`

- What: Merge two deals with same type
- Call: `POST /crm/objects/2026-03/0-3/merge`, effect: destructive
- Permission keys: `deals.delete`
- Body: `PublicMergeInput`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api deals-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/0-3/{dealId}`, effect: write
- Permission keys: `deals.update`, `crm.assign-others`, `deals.move`, `deals.close`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--deal-id <value>` | yes | dealId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/emails`, effect: write
- Permission keys: `emails.write`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api emails-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/emails/{emailId}`, effect: destructive
- Permission keys: `emails.delete`

| Flag | Required | What |
|---|---|---|
| `--email-id <value>` | yes | emailId |

## `hubspot api emails-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/emails/{emailId}`, effect: read
- Permission keys: `activities.list`

| Flag | Required | What |
|---|---|---|
| `--email-id <value>` | yes | emailId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api emails-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/emails`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api emails-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/emails/{emailId}`, effect: write
- Permission keys: `emails.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--email-id <value>` | yes | emailId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/leads`, effect: write
- Permission keys: `leads.write`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api leads-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/leads/{leadsId}`, effect: destructive
- Permission keys: `leads.delete`

| Flag | Required | What |
|---|---|---|
| `--leads-id <value>` | yes | leadsId |

## `hubspot api leads-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/leads/{leadsId}`, effect: read
- Permission keys: `leads.show`

| Flag | Required | What |
|---|---|---|
| `--leads-id <value>` | yes | leadsId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api leads-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/leads`, effect: read
- Permission keys: `leads.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api leads-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/leads/{leadsId}`, effect: write
- Permission keys: `leads.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--leads-id <value>` | yes | leadsId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/meetings`, effect: write
- Permission keys: `meetings.write`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api meetings-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/meetings/{meetingId}`, effect: destructive
- Permission keys: `meetings.delete`

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meetingId |

## `hubspot api meetings-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/meetings/{meetingId}`, effect: read
- Permission keys: `activities.list`

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meetingId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api meetings-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/meetings`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api meetings-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/meetings/{meetingId}`, effect: write
- Permission keys: `meetings.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meetingId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/notes`, effect: write
- Permission keys: `notes.write`, `activities.create`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api notes-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/notes/{noteId}`, effect: destructive
- Permission keys: `notes.delete`

| Flag | Required | What |
|---|---|---|
| `--note-id <value>` | yes | noteId |

## `hubspot api notes-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/notes/{noteId}`, effect: read
- Permission keys: `activities.list`

| Flag | Required | What |
|---|---|---|
| `--note-id <value>` | yes | noteId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api notes-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/notes`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api notes-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/notes/{noteId}`, effect: write
- Permission keys: `notes.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--note-id <value>` | yes | noteId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api owners-get [options]`

- What: Retrieve a specific owner by ID
- Call: `GET /crm/owners/2026-03/{ownerId}`, effect: read
- Permission keys: `users.show`

| Flag | Required | What |
|---|---|---|
| `--owner-id <value>` | yes | The unique identifier of the owner to retrieve. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--id-property <value>` | no | Specifies which property to use for identifying the owner. Valid values are 'id' or 'userId'. Defaults to 'id'. |

## `hubspot api owners-list [options]`

- What: List owners
- Call: `GET /crm/owners/2026-03`, effect: read
- Permission keys: `users.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--email <value>` | no | Filter by email address (optional) |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api pipelines-audit-list [options]`

- What: Return an audit of all changes to the pipeline
- Call: `GET /crm/pipelines/2026-03/{objectType}/{pipelineId}/audit`, effect: read

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |

## `hubspot api pipelines-create [options]`

- What: Create a pipeline
- Call: `POST /crm/pipelines/2026-03/{objectType}`, effect: write
- Permission keys: `pipelines.write`
- Body: `PipelineInput`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api pipelines-delete [options]`

- What: Delete a pipeline
- Call: `DELETE /crm/pipelines/2026-03/{objectType}/{pipelineId}`, effect: destructive
- Permission keys: `pipelines.delete`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--validate-deal-stage-usages-before-delete <value>` | no | validateDealStageUsagesBeforeDelete |
| `--validate-references-before-delete <value>` | no | validateReferencesBeforeDelete |

## `hubspot api pipelines-get [options]`

- What: Return a pipeline by ID
- Call: `GET /crm/pipelines/2026-03/{objectType}/{pipelineId}`, effect: read
- Permission keys: `pipelines.show`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |

## `hubspot api pipelines-list [options]`

- What: Retrieve all pipelines
- Call: `GET /crm/pipelines/2026-03/{objectType}`, effect: read
- Permission keys: `pipelines.list`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |

## `hubspot api pipelines-replace [options]`

- What: Replace a pipeline
- Call: `PUT /crm/pipelines/2026-03/{objectType}/{pipelineId}`, effect: destructive
- Permission keys: `pipelines.delete`
- Body: `PipelineReplaceInput`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--validate-deal-stage-usages-before-delete <value>` | no | validateDealStageUsagesBeforeDelete |
| `--validate-references-before-delete <value>` | no | validateReferencesBeforeDelete |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api pipelines-stages-audit-list [options]`

- What: Retrieve a reverse chronological list of all changes made to a specific pipeline stage.
- Call: `GET /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages/{stageId}/audit`, effect: read

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--stage-id <value>` | yes | stageId |

## `hubspot api pipelines-stages-create [options]`

- What: Create a pipeline stage
- Call: `POST /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages`, effect: write
- Permission keys: `pipelines.write`
- Body: `PipelineStageInput`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api pipelines-stages-delete [options]`

- What: Delete a pipeline stage
- Call: `DELETE /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages/{stageId}`, effect: destructive
- Permission keys: `pipelines.delete`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--stage-id <value>` | yes | stageId |
| `--validate-references-before-delete <value>` | no | validateReferencesBeforeDelete |

## `hubspot api pipelines-stages-get [options]`

- What: Return a pipeline stage by ID
- Call: `GET /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages/{stageId}`, effect: read
- Permission keys: `stages.list`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--stage-id <value>` | yes | stageId |

## `hubspot api pipelines-stages-list [options]`

- What: Return all stages of a pipeline
- Call: `GET /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages`, effect: read
- Permission keys: `stages.list`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |

## `hubspot api pipelines-stages-replace [options]`

- What: Replace a pipeline stage
- Call: `PUT /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages/{stageId}`, effect: write
- Permission keys: `pipelines.write`
- Body: `PipelineStageReplaceInput`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--stage-id <value>` | yes | stageId |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api pipelines-stages-update [options]`

- What: Update specific properties of an existing pipeline stage.
- Call: `PATCH /crm/pipelines/2026-03/{objectType}/{pipelineId}/stages/{stageId}`, effect: write
- Permission keys: `pipelines.write`
- Body: `PipelineStagePatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--stage-id <value>` | yes | stageId |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api pipelines-update [options]`

- What: Perform a partial update of the pipeline identified by pipelineId.
- Call: `PATCH /crm/pipelines/2026-03/{objectType}/{pipelineId}`, effect: write
- Permission keys: `pipelines.write`
- Body: `PipelinePatchInput`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | objectType |
| `--pipeline-id <value>` | yes | pipelineId |
| `--validate-deal-stage-usages-before-delete <value>` | no | validateDealStageUsagesBeforeDelete |
| `--validate-references-before-delete <value>` | no | validateReferencesBeforeDelete |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-create [options]`

- What: Create a property
- Call: `POST /crm/properties/2026-03/{objectType}`, effect: write
- Permission keys: `fields.write`
- Body: `PropertyCreate`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of object for which the property is being created, such as contacts, companies, or deals. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-delete [options]`

- What: Archive a property
- Call: `DELETE /crm/properties/2026-03/{objectType}/{propertyName}`, effect: destructive
- Permission keys: `fields.delete`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of CRM object that the property belongs to, such as contacts, companies, or deals. |
| `--property-name <value>` | yes | The unique name of the property to delete. |

## `hubspot api properties-get [options]`

- What: Read a property
- Call: `GET /crm/properties/2026-03/{objectType}/{propertyName}`, effect: read
- Permission keys: `fields.list`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of object the property belongs to, such as 'contacts' or 'deals'. |
| `--property-name <value>` | yes | The name of the property to retrieve. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--data-sensitivity <value>` | no | The level of data sensitivity to filter properties by. Valid values are 'non\_sensitive', 'sensitive', and 'highly\_sensitive'. Defaults to 'non\_sensitive'. |
| `--locale <value>` | no | The locale to use for property labels and descriptions. |
| `--properties <value>` | no | A comma-separated list of property names to include in the response. |

## `hubspot api properties-groups-create [options]`

- What: Create a property group
- Call: `POST /crm/properties/2026-03/{objectType}/groups`, effect: write
- Permission keys: `fields.write`
- Body: `PropertyGroupCreate`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of object for which the property group is being created, such as contacts, companies, or deals. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-groups-delete [options]`

- What: Archive a property group
- Call: `DELETE /crm/properties/2026-03/{objectType}/groups/{groupName}`, effect: destructive
- Permission keys: `fields.delete`

| Flag | Required | What |
|---|---|---|
| `--group-name <value>` | yes | The unique name of the property group to be deleted. |
| `--object-type <value>` | yes | The type of object for which the property group is defined, such as contacts, companies, or deals. |

## `hubspot api properties-groups-get [options]`

- What: Read a property group
- Call: `GET /crm/properties/2026-03/{objectType}/groups/{groupName}`, effect: read
- Permission keys: `fields.list`

| Flag | Required | What |
|---|---|---|
| `--group-name <value>` | yes | The name of the property group to retrieve details for. |
| `--object-type <value>` | yes | The type of CRM object for which the property group is being retrieved, such as contacts or deals. |
| `--locale <value>` | no | The language locale to use for the response. This can affect the language of the labels and descriptions returned. |

## `hubspot api properties-groups-list [options]`

- What: Read all property groups
- Call: `GET /crm/properties/2026-03/{objectType}/groups`, effect: read
- Permission keys: `fields.list`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of CRM object for which to retrieve property groups, such as 'contacts' or 'deals'. |
| `--locale <value>` | no | The language locale to use for property group labels. This can help in displaying labels in the preferred language. |

## `hubspot api properties-groups-update [options]`

- What: Update a property group
- Call: `PATCH /crm/properties/2026-03/{objectType}/groups/{groupName}`, effect: write
- Permission keys: `fields.write`
- Body: `PropertyGroupUpdate`, required

| Flag | Required | What |
|---|---|---|
| `--group-name <value>` | yes | The name of the property group to update. |
| `--object-type <value>` | yes | The type of object for which the property group is being updated, such as contacts, companies, or deals. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api properties-list [options]`

- What: Read all properties
- Call: `GET /crm/properties/2026-03/{objectType}`, effect: read
- Permission keys: `fields.list`

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of CRM object for which properties are being retrieved, such as 'contacts', 'companies', etc. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--data-sensitivity <value>` | no | Filter properties based on data sensitivity level. Valid values are 'non\_sensitive', 'sensitive', and 'highly\_sensitive'. Defaults to 'non\_sensitive'. |
| `--locale <value>` | no | Specify the locale to retrieve properties in a particular language or regional format. |
| `--properties <value>` | no | A comma-separated list of property names to include in the response. |

## `hubspot api properties-update [options]`

- What: Update a property
- Call: `PATCH /crm/properties/2026-03/{objectType}/{propertyName}`, effect: write
- Permission keys: `fields.write`
- Body: `PropertyUpdate`, required

| Flag | Required | What |
|---|---|---|
| `--object-type <value>` | yes | The type of object for which the property is being updated, such as contacts, companies, or deals. |
| `--property-name <value>` | yes | The unique name of the property to update. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/tasks`, effect: write
- Permission keys: `tasks.write`, `activities.create`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tasks-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/tasks/{taskId}`, effect: destructive
- Permission keys: `tasks.delete`

| Flag | Required | What |
|---|---|---|
| `--task-id <value>` | yes | taskId |

## `hubspot api tasks-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/tasks/{taskId}`, effect: read
- Permission keys: `activities.list`

| Flag | Required | What |
|---|---|---|
| `--task-id <value>` | yes | taskId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api tasks-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/tasks`, effect: read
- Permission keys: `activities.list`
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api tasks-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/tasks/{taskId}`, effect: write
- Permission keys: `tasks.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--task-id <value>` | yes | taskId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-create [options]`

- What: Create
- Call: `POST /crm/objects/2026-03/tickets`, effect: write
- Permission keys: `tickets.write`, `crm.assign-others`
- Body: `SimplePublicObjectInputForCreate`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `hubspot api tickets-delete [options]`

- What: Archive
- Call: `DELETE /crm/objects/2026-03/tickets/{ticketId}`, effect: destructive
- Permission keys: `tickets.delete`

| Flag | Required | What |
|---|---|---|
| `--ticket-id <value>` | yes | ticketId |

## `hubspot api tickets-get [options]`

- What: Read
- Call: `GET /crm/objects/2026-03/tickets/{ticketId}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--ticket-id <value>` | yes | ticketId |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. |

## `hubspot api tickets-list [options]`

- What: List
- Call: `GET /crm/objects/2026-03/tickets`, effect: read
- Pages: cursor: send `after` (query), read the next one from `paging.next.after`; items in `results`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | The paging cursor token of the last successfully read resource will be returned as the \`paging.next.after\` JSON property of a paged response containing more results. |
| `--archived <value>` | no | Whether to return only results that have been archived. |
| `--associations <value>` | no | A comma separated list of object types to retrieve associated IDs for. If any of the specified associations do not exist, they will be ignored. |
| `--limit <value>` | no | The maximum number of results to display per page. |
| `--properties <value>` | no | A comma separated list of the properties to be returned in the response. If any of the specified properties are not present on the requested object(s), they will be ignored. |
| `--properties-with-history <value>` | no | A comma separated list of the properties to be returned along with their history of previous values. If any of the specified properties are not present on the requested object(s), they will be ignored. Usage of this parameter will reduce the maximum number of objects that can be read by a single request. |
| `--all` | no | read every page, as the API pages it |

## `hubspot api tickets-update [options]`

- What: Update
- Call: `PATCH /crm/objects/2026-03/tickets/{ticketId}`, effect: write
- Permission keys: `tickets.write`, `crm.assign-others`
- Body: `SimplePublicObjectInput`, required

| Flag | Required | What |
|---|---|---|
| `--ticket-id <value>` | yes | ticketId |
| `--id-property <value>` | no | The name of a property whose values are unique for this object type |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
