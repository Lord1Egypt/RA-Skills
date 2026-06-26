---
name: zion-baas
description: Instructions and authentication code for building headless BaaS applications with Zion.app (functorz.com). Use when integrating Zion backend features like GraphQL, actionflows, AI agents, binary assets, and payments.
---

# Zion.app Headless BaaS Skill

## Overview
This skill outlines how to build frontend applications utilizing Zion.app as a headless Backend-as-a-Service (BaaS). Zion exposes all backend interactions (database, actionflows, third-party APIs, and AI agents) through a single, unified GraphQL API.

- **HTTP URL**: `https://zion-app.functorz.com/zero/{projectExId}/api/graphql-v2`
- **WebSocket URL**: `wss://zion-app.functorz.com/zero/{projectExId}/api/graphql-subscription`

## Token Acquisition & Authentication (CRITICAL)
To interact with authenticated endpoints, you must obtain a JWT token by logging in or registering. Unauthenticated requests are assigned an anonymous user role. The JWT can be obtained in two ways. One is via username + password login. The other one is by querying the Meta API & fetching runtime backend token. The token return in FETCH_DATA_VISUALIZER is the runtime backend token. 

### 1. Username Registration & Login
You should ask user for username and password.
```graphql
mutation AuthenticateWithUsername($username: String!, $password: String!, $register: Boolean!) {
  authenticateWithUsername(username: $username, password: $password, register: $register) {
    account { id, permissionRoles }
    jwt { token }
  }
}
```
*Note: Both mutations return `FZ_Account` which is a subset of the full `account` type. It contains only `email`, `id`, `permissionRoles`, `phoneNumber`, `profileImageUrl`, `roles`, and `username`.*

## Developer Authentication with Zion.app (Meta API)
If you need to interact directly with the Zion platform (Meta API) to fetch project schemas, list projects, or authenticate as an admin to the runtime backend, follow these steps:

### 1. Acquire Developer JWT Token
There are two ways to acquire a developer token: via OAuth Flow or via Email/Password login.

#### Option A: OAuth Flow
Set up a local HTTP server to receive the OAuth callback. Open the Zion authentication endpoint (`https://auth.functorz.com/login`) in the browser and wait for the `token` parameter.

You can run the bundled authentication script:

```bash
cd ~/.openclaw/skills/zion_baas/scripts
npm run auth
```

#### Option B: Email/Password Login
You can directly login with an email and password using the Meta API:

```bash
cd ~/.openclaw/skills/zion_baas/scripts
npm run auth:email <email> <password>
```

### 2. Querying the Meta API & Fetching Runtime Backend Token
Use the developer JWT token as a Bearer token against the Meta API (`https://zionbackend.functorz.com/api/graphql`) to get the schema or data visualizer tokens. The data visualizer token grants administrative access to the project's runtime backend (`zeroUrl`).

You can run the bundled script to fetch the token. It requires the developer token to be present in `.zion/credentials.yaml`.

```bash
cd ~/.openclaw/skills/zion_baas/scripts
npm run fetch-token -- <projectExId>
```

You can also search for projects or fetch their schema via the Meta API using the bundled `meta` script:

```bash
cd ~/.openclaw/skills/zion_baas/scripts
# Search projects (returns project names and exIds)
npm run meta -- search-projects "optional search term"

# Fetch project schema (returns data models, actionflows, apis)
npm run meta -- fetch-schema <projectExId>
```

## Credential Management & State Persistence

All credentials and project state MUST be persisted in the `.zion` directory at the root of the user's project in YAML format, typically in a file named `.zion/credentials.yaml`.

### Required YAML Format

The credentials file must adhere to the following structure:

```yaml
# .zion/credentials.yaml
developer_token:
  token: "<your_developer_jwt_token>" # Used to communicate with zionbackend.functorz.com
  expiry: "<timestamp_or_date_of_expiry>"

project:
  exId: "<project_ex_id>"
  name: "<project_name>"
  admin_token:
    token: "<runtime_backend_admin_token>"
    expiry: "<timestamp_or_date_of_expiry>"
  other_users:
    - user_id: "<user_id>"
      user_tags: 
        - "<notable_information_about_the_user_1>"
      token:
        token: "<user_jwt_token>"
        expiry: "<timestamp_or_date_of_expiry>"
```

- **`developer_token`**: The JWT token acquired via the OAuth flow, used against the Meta API (`zionbackend.functorz.com`).
- **`project`**: Contains the core project identifiers (`exId`, `name`), the `admin_token` (data visualizer token) for the runtime backend, and `other_users`.
- **`other_users`**: A list of authenticated users (e.g., test accounts) containing their `user_id`, helpful `user_tags` to identify their purpose, and their `token`.
- **`expiry`**: All stored tokens must include an associated expiry.

## Executing GraphQL Queries & Subscriptions via CLI
You can use the bundled scripts to quickly test GraphQL queries, mutations, and subscriptions from the command line without writing frontend boilerplate. These scripts automatically read the correct token from your project's `.zion/credentials.yaml`.

### 1. Execute a Query or Mutation
Pass your GraphQL query or mutation as a string.

```bash
cd ~/.openclaw/skills/zion_baas/scripts
npm run gql -- <projectExId> <role> '<query_string>' '<optional_variables_json>'
```
- `<role>`: Can be `admin` (uses data visualizer token), `anonymous` (no token), or a specific `user_id` (fetches token from `other_users` in `.zion/credentials.yaml`).

*Example:*
```bash
npm run gql -- myProjectEx123 admin 'query GetProject($id: Int!) { project(id: $id) { name } }' '{"id": 1}'
```

### 2. Listen to a Subscription
Pass your GraphQL subscription as a string.

```bash
cd ~/.openclaw/skills/zion_baas/scripts
npm run subscribe -- <projectExId> <role> '<query_string>' '<optional_variables_json>'
```
The script will establish a WebSocket connection and continuously print events as they arrive until you kill it (Ctrl+C).


## Database & GraphQL Schema Rules
- Use `zion MCP server` or `webfetch/curl` to introspect the schema before making assumptions.

The GraphQL schema is automatically generated directly from the PostgreSQL data model.

> **CRITICAL CATCH-ALL RULE:**
> If you are ever in doubt about the exact structure, available fields, Enum values (like `[Enum:ROUNDING_MODE]`), or specific arguments for an endpoint, **you must use the webfetch/curl tool to introspect the live GraphQL schema** via the provided endpoint URL before making assumptions.
 

### 1. Naming Conventions & Root Operations

Each table generates corresponding root query, mutation, and subscription fields. For a table named `[table]`:

#### Queries
*   `[table]`: Fetch lists (supports `where`, `order_by`, `distinct_on`, `limit`, `offset`).
*   `[table]_by_pk`: Fetch single record by primary key (`id`).
*   `[table]_aggregate`: Aggregate queries (`count`, `sum`, `avg`, `min`, `max`).
*   `[table]_group_by`: Group records based on specified fields.
*   `fz_[table]_by_[column]`: Auto-generated spatial proximity search if the table contains a `geo_point` column.
*   **Relay API**: If configured, generates a cursor-based pagination query returning a `Connection_[table]` object.

#### Mutations
*   `insert_[table]`, `insert_[table]_one`: Create records. Supports nested inserts and `on_conflict` (requires `constraint` and `update_columns`).
*   `update_[table]`, `update_[table]_by_pk`: Modify records. Uses `_set` (replace) and `_inc` (increment numeric). `where` is required (`!`) for bulk updates. *(Note: Hasura JSONB update operators like `_append`/`_delete_key` are not supported).*
*   `delete_[table]`, `delete_[table]_by_pk`: Remove records. `where` is required (`!`) for bulk deletes.
*   `export_[table]`: Trigger a data export task for the table.

#### Subscriptions
*   `[table]`, `[table]_by_pk`, `[table]_aggregate`: Live queries mirroring their standard query counterparts.

### 2. Column Types and Data Mappings

#### Primitive Types
*   `text` → `String`, `integer` → `Int`, `bigint`, `bigserial` → `bigint`, `float8` → `Float8`, `decimal` → `Decimal`, `boolean` → `Boolean`, `jsonb` → `jsonb`.
*   **Time/Date**: `timestamptz`, `timetz`, `date`, `interval`.
*   **Geo**: `geo_point` → `geography`.

#### Composite (Media) Types
Media columns (`image`, `file`, `video`) are structurally 1:N relations but act as fields. 
*   **Single Media**: Stored as `[column]_id` (e.g., `cover_image_id`) referencing system asset tables (`FZ_Image`, `FZ_File`, `FZ_Video`).
*   **Media Lists**: Types like `image_list`, `video_list`, `file_list` map to GraphQL Arrays and are stored as `[column]_ids` (e.g., `gallery_images_ids`).

#### System-Managed Columns
`id`, `created_at`, `updated_at` are read-only and automatically managed. They cannot be used in mutation inputs (`_set`, `_inc`, insert inputs).

### 3. Relationships

Relationships are defined by foreign keys and determine GraphQL nested fields:
*   **1:1 (One-to-One)**: Yields a single nested object (e.g., `meta: post_meta`).
*   **1:N (One-to-Many)**: Yields an array (e.g., `post_tags: [post_tag]`) and an aggregate object (e.g., `post_tags_aggregate`).

### 4. Filtering (`where` clauses)

Filters rely on `[table]_bool_exp`.

#### Logical Operators
*   `_and: [bool_exp]`, `_or: [bool_exp]`, `_not: bool_exp`

#### Relation Filters
Navigate relationships using the relationship field name directly. The value is a nested `[related_table]_bool_exp` object.
*   **To-One Relationships (1:1, N:1)**: Filters the parent record based on the single related record's fields.
    *(e.g., Find posts where the author's name is "John": `author: { name: { _eq: ... } }`)*
*   **To-Many Relationships (1:N, N:M)**: Uses `EXISTS` semantics. The parent record is returned if **any** related record in the array matches the nested condition.
    *(e.g., Find posts that have at least one tag named "Tech": `post_tags: { tag: { name: { _eq: ... } } }`)*

#### Comparison Predicates (Strict Pattern)
Zion uses a strict **Operator-First Pattern**. A predicate must start with the operator. If it's a generic operator, the operand wrapper type must match the *final evaluated type*, not necessarily the column type.

**Structure:**
```json
{
  "_operator": {
    "operand_type": {
      "left_operand": { ... },
      "right_operand": { ... }
    }
  }
}
```

*   **Operators:** 
    *   **Comparison (Generic):** `_eq`, `_neq`, `_gt`, `_lt`, `_gte`, `_lte`
    *   **Array (Generic):** `_in`, `_nin`
    *   **Nullity (Generic, Unary):** `_is_null`, `_is_not_null`
    *   **Text (String Pattern):** `_like`, `_nlike`, `_ilike`, `_nilike`, `_similar`, `_nsimilar`
    *   **JSONB:** `_contains`, `_contained_in`, `_has_key`, `_has_keys_any`, `_has_keys_all`
    *   **Boolean:** `_is_true`, `_is_false`
    *   **Collection:** `_is_empty`, `_is_not_empty`
*   **Operand Definitions (`left_operand` / `right_operand`):**
    *   **Literal**: `{"literal": value}`
    *   **Column**: `{"column": "field_name"}`
    *   **Function**: `{"function_name": { ...args }}`
*   **Operand Types (Determined by Final Value):** `bigint_operand`, `text_operand`, `boolean_operand`, `timestamptz_operand`, etc.

**Example Predicate (Extract Month from Timestamp and check if = 12):**
```json
{
  "_eq": {
    "bigint_operand": {
      "left_operand": {
        "extract_timestamptz": { "time": { "column": "created_at" }, "unit": "MONTH" }
      },
      "right_operand": { "literal": "12" }
    }
  }
}
```

### 5. Aggregations, Window Functions, and Order By

#### Aggregation (`[table]_aggregate`)
Returns an aggregate query object containing two main fields:
*   `nodes`: An array of the actual table objects (`[table!]!`) containing the raw data rows that match the query's `where`, `limit`, `offset`, and `order_by` criteria.
*   `aggregate`: An object containing statistical calculations over the matched rows:
    *   `count(columns: [Enum], distinct: Boolean)`: 
        *   If no columns are provided, it counts all rows (`COUNT(*)`).
        *   If `distinct: true` and 1+ columns are provided, it counts unique values or unique combinations of the specified columns.
        *   If `distinct: false` and multiple columns are provided, the system restricts the count to only evaluate the *first* column in the array.
    *   `sum`, `avg`: Only available for **numeric** columns.
    *   `max`, `min`: Available for **comparable** columns (numeric, time, text).

#### Window Functions
Advanced analytical operations like `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTH_VALUE` are supported in specific formula and window frame inputs.

#### Sorting (`order_by`)
Supports sorting by:
1.  Direct columns: `{ title: asc }`
2.  Related 1:1 records: `{ author: { name: desc } }`
3.  Aggregates of N:1 records: `{ post_tags_aggregate: { count: desc } }`
4.  Vector Search: Text columns may support similarity sorting if the `TEXT_COLUMN_VECTOR_SORT` extension is applied.

### 6. Formula Functions (Operands)
Functions are used inside operand wrappers by wrapping the uppercase function name around its arguments (e.g., `{"EXTRACT_TIMESTAMPTZ": { "time": ..., "unit": ... }}`).

#### Input Constraints & Semantics
*   **[TYPE]**: Indicates a required column or scalar operand of that exact type.
*   **[TYPE?]**: Indicates an optional operand (usually defaults to `0` or `null`).
*   **[ANY]**: Accepts any column or scalar operand of any type.
*   **[NUMERIC]**: Accepts `BIGINT`, `INTEGER`, `DECIMAL`, `FLOAT8`, or `BIGSERIAL`.
*   **[COMPARABLE]**: Accepts `NUMERIC` types, `TEXT`, `DATE`, `TIMESTAMPTZ`, `TIMETZ`, or `INTERVAL`.
*   **[ANY[]]**: Accepts an array operand of any type.
*   **[Enum:NAME]**: Requires an explicit Enum value matching the `[NAME]` definition (e.g., `[Enum:DATE_UNIT]` requires `YEAR`, `MONTH`, etc.).
*   **Nested Functions**: Arguments can often be the output of other functions, provided the output type matches the expected input type.

#### Manipulation
*   `CONCAT(items: [TEXT[]])`
*   `SUBSTRING(source_text: [TEXT], start_index: [BIGINT], end_index: [BIGINT])`
*   `LEFT(source_text: [TEXT], length: [BIGINT])`
*   `RIGHT(source_text: [TEXT], length: [BIGINT])`
*   `LOWER(source_text: [TEXT])`
*   `UPPER(source_text: [TEXT])`
*   `TRIM(text: [TEXT])`
*   `TRIM_TRAILING_ZERO(source_text: [TEXT])`
*   `REPEAT(text: [TEXT], times: [BIGINT])`
*   `ENCODE_URL(text: [TEXT])`
*   `DECODE_URL(text: [TEXT])`
*   `ARRAY_CONCAT(first_array: [ANY[]], second_array: [ANY[]])`
*   `SLICE(array: [ANY[]], start_index: [BIGINT], length: [BIGINT])`
*   `UNIQUE(array: [ANY[]])`
*   `COALESCE(array: [ANY[]])`

#### Search & Replace
*   `REPLACE_OCCURRENCES(source_text: [TEXT], search_text: [TEXT], replace_text: [TEXT], max_replacements: [BIGINT])`
*   `REPLACE_AT_POSITION(source_text: [TEXT], start_index: [BIGINT], length: [BIGINT], replace_text: [TEXT])`
*   `POSITION(source_text: [TEXT], search_text: [TEXT])`
*   `CONTAINS(source_text: [TEXT], search_text: [TEXT])`

#### Regex
*   `REGEX_EXTRACT(text: [TEXT], regex: [TEXT])`
*   `REGEX_REPLACE(text: [TEXT], regex: [TEXT], replacement: [TEXT])`
*   `REGEX_EXTRACT_ALL(text: [TEXT], regex: [TEXT])`
*   `REGEX_MATCH(text: [TEXT], regex: [TEXT])`

#### Formatting & Utils
*   `TEXT_DECIMAL_FORMAT(number: [DECIMAL], fraction_digits: [BIGINT], rounding_mode: [Enum:ROUNDING_MODE], clear_trailing_zeros: [BOOLEAN])`
*   `NUMBER_FORMAT(number: [DECIMAL], fraction_digits: [BIGINT], format: [Enum:NUMBER_FORMAT])`
*   `STRING_LEN(source_text: [TEXT])`
*   `RANDOM_TEXT(min_length: [BIGINT], max_length: [BIGINT], include_numbers: [BOOLEAN], include_lower_case: [BOOLEAN], include_upper_case: [BOOLEAN])`
*   `UUID()`
*   `JOIN(array: [TEXT[]], separator: [TEXT])`
*   `SPLIT(source_text: [TEXT], delimiter: [TEXT])`
*   `ARRAY_LEN(array: [ANY[]])`

#### Arithmetic
*   `ADD(value0: [NUMERIC], value1: [NUMERIC])`
*   `SUBTRACT(minuend: [NUMERIC], subtrahend: [NUMERIC])`
*   `MULTIPLY(value0: [NUMERIC], value1: [NUMERIC])`
*   `DIVIDE(dividend: [DECIMAL], divisor: [DECIMAL])`
*   `MODULO(dividend: [NUMERIC], divisor: [NUMERIC])`
*   `ABS(number: [NUMERIC])`
*   `POW(base: [NUMERIC], exponent: [NUMERIC])`
*   `LOG(base: [DECIMAL], argument: [DECIMAL])`

#### Rounding & Formats
*   `ROUND_UP(number: [DECIMAL])`
*   `ROUND_DOWN(number: [DECIMAL])`
*   `DECIMAL_FORMAT(number: [DECIMAL], fraction_digits: [BIGINT], rounding_mode: [Enum:ROUNDING_MODE])`

#### Generators
*   `RANDOM_BIGINT(min_length: [BIGINT], max_length: [BIGINT])`
*   `SEQUENCE(start: [BIGINT], end: [BIGINT], step: [BIGINT])`

#### Current Time
*   `CURRENT_DATE()`
*   `CURRENT_TIMETZ()`
*   `CURRENT_TIMESTAMPTZ()`

#### Constructors
*   `MAKE_DATE(years: [BIGINT], months: [BIGINT], days: [BIGINT])`
*   `MAKE_TIMETZ(hours: [BIGINT?], minutes: [BIGINT?], seconds: [BIGINT?], milliseconds: [BIGINT?])`
*   `MAKE_TIMESTAMPTZ(years: [BIGINT], months: [BIGINT], days: [BIGINT], hours: [BIGINT?], minutes: [BIGINT?], seconds: [BIGINT?], milliseconds: [BIGINT?])`
*   `MAKE_INTERVAL(years: [BIGINT], months: [BIGINT], weeks: [BIGINT], days: [BIGINT], hours: [BIGINT], minutes: [BIGINT], seconds: [BIGINT], milliseconds: [BIGINT])`
*   `FROM_DATE_AND_TIMETZ(date: [DATE], timetz: [TIMETZ])`

#### Extraction & Formatting
*   `EXTRACT_DATE(time: [DATE], unit: [Enum:DATE_UNIT])`
*   `EXTRACT_TIMETZ(time: [TIMETZ], unit: [Enum:TIME_UNIT])`
*   `EXTRACT_TIMESTAMPTZ(time: [TIMESTAMPTZ], unit: [Enum:TIMESTAMP_UNIT])`
*   `DATE_FORMAT(time: [DATE], format: [TEXT], language: [Enum:LANGUAGE])`
*   `TIMETZ_FORMAT(time: [TIMETZ], format: [TEXT], language: [Enum:LANGUAGE])`
*   `TIMESTAMPTZ_FORMAT(time: [TIMESTAMPTZ], format: [TEXT], language: [Enum:LANGUAGE])`
*   `DURATION_FORMAT(duration: [DECIMAL], unit: [Enum:DURATION_UNIT], format: [TEXT])`
*   `RELATIVE_DATE(time: [DATE], language: [Enum:LANGUAGE], hide_suffix: [BOOLEAN])`
*   `RELATIVE_TIMESTAMPTZ(time: [TIMESTAMPTZ], language: [Enum:LANGUAGE], hide_suffix: [BOOLEAN])`

#### Calculations & Deltas
*   `DELTA_DATE(date: [DATE], increase: [BOOLEAN], years: [BIGINT?], months: [BIGINT?], days: [BIGINT?])`
*   `DELTA_TIMETZ(timetz: [TIMETZ], increase: [BOOLEAN], hours: [BIGINT?], minutes: [BIGINT?], seconds: [BIGINT?], milliseconds: [BIGINT?])`
*   `DELTA_TIMESTAMPTZ(timestamptz: [TIMESTAMPTZ], increase: [BOOLEAN], years: [BIGINT?], months: [BIGINT?], days: [BIGINT?], hours: [BIGINT?], minutes: [BIGINT?], seconds: [BIGINT?], milliseconds: [BIGINT?])`
*   `EXTRACT_DATE_DURATION(start_time: [DATE], end_time: [DATE], unit: [Enum:DATE_UNIT])`
*   `EXTRACT_TIMETZ_DURATION(start_time: [TIMETZ], end_time: [TIMETZ], unit: [Enum:TIME_UNIT])`
*   `EXTRACT_TIMESTAMPTZ_DURATION(start_time: [TIMESTAMPTZ], end_time: [TIMESTAMPTZ], unit: [Enum:TIMESTAMP_UNIT])`

#### Conversions
*   `FROM_TIMESTAMPTZ_TO_DATE(timestamptz: [TIMESTAMPTZ])`
*   `FROM_TIMESTAMPTZ_TO_TIMETZ(timestamptz: [TIMESTAMPTZ])`

#### Geography
*   `FROM_COORDINATES(latitude: [DECIMAL], longitude: [DECIMAL])`
*   `GEO_DISTANCE(point0: [GEO_POINT], point1: [GEO_POINT], unit: [Enum:GEO_DISTANCE_UNIT])`
*   `GEO_LONGITUDE(geo: [GEO_POINT])`
*   `GEO_LATITUDE(geo: [GEO_POINT])`

#### Aggregates
*   `SUM(array: [NUMERIC[]])`
*   `AVG(array: [NUMERIC[]])`
*   `MAX(value0: [COMPARABLE], value1: [COMPARABLE])`
*   `MIN(value0: [COMPARABLE], value1: [COMPARABLE])`
*   `GREATEST(array: [COMPARABLE[]])`
*   `LEAST(array: [COMPARABLE[]])`

#### Element Access
*   `ITEM(array: [ANY[]], index: [BIGINT])`
*   `FIRST_ITEM(array: [ANY[]])`
*   `LAST_ITEM(array: [ANY[]])`
*   `RANDOM_ITEM(array: [ANY[]])`
*   `ARRAY_POSITION(array: [ANY[]], item: [ANY])`

#### JSONB
*   `JSON_EXTRACT_BY_DOT_NOTATION_JSONPATH(json: [JSONB], path: [TEXT])`

#### Casting
*   `CAST_FROM_TEXT(value: [TEXT])`
*   `CAST_COLUMN_TO_TEXT(value: [ANY])`
*   `CAST_ARRAY_TO_TEXT(value: [ANY[]])`
*   `CAST_TO_BIGINT(value: [ANY])`
*   `CAST_TO_DECIMAL(value: [ANY])`

#### Vector Search
*   `EMBEDDING_VECTOR_DISTANCE(embedded_text_column: [Enum:EMBEDDING_COLUMN], text: [TEXT], distance_function: [Enum:VECTOR_DISTANCE])`

#### System
*   `NULL_VALUE()`

#### Explicit Enum Definitions
When an argument requires an `[Enum:NAME]`, you must use one of the following exact string values:
*   **[Enum:DATE_UNIT]**: `YEAR, MONTH, DAY, WEEK`
*   **[Enum:DURATION_UNIT]**: `DAY, HOUR, MINUTE, SECOND, MILLISECOND`
*   **[Enum:EMBEDDING_COLUMN]**: `(Dynamically generated based on columns with TEXT_COLUMN_VECTOR_SORT extension)`
*   **[Enum:GEO_DISTANCE_UNIT]**: `METER, KILOMETER, MILE`
*   **[Enum:LANGUAGE]**: `EN, ZH`
*   **[Enum:NUMBER_FORMAT]**: `THOUSANDS_SEPARATOR, PERCENT`
*   **[Enum:ROUNDING_MODE]**: `HALF_EVEN, HALF_UP, HALF_DOWN, UP, DOWN, CEILING, FLOOR`
*   **[Enum:TIMESTAMP_UNIT]**: `YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, MILLISECOND, WEEK`
*   **[Enum:TIME_UNIT]**: `HOUR, MINUTE, SECOND, MILLISECOND`
*   **[Enum:VECTOR_DISTANCE]**: `EUCLIDEAN, COSINE`

## Actionflow Protocol

### Overview
Although zion-app.functorz.com already support direct CRUD operations that can be initiated from the frontend, many backend operations are multi-step, can be long-running and sometimes have to be asynchronous. Therefore zion-app.functorz.com also supports actionflows for these scenarios. An actionflow is a directed acyclic graph made up of actionflow nodes. These nodes represent either operations (e.g. insert into databsae, invoke another actionflow) or control flow changes (condition and loop). Actionflows also have two special nodes, input and output, where the arguments and return values of the entire actionflow are defined. 

Actionflows have two modes of operation, sync or async. A synchronous actionflow is executed within a single database transaction, and therefore when an unexpected error is encountered, will rollback all database changes. Synchronous actionflows have runtime limits to avoid hogging database connection. Asynchronous actionflows run each node inside a new database transaction, so they do not have rollback mechanism, but are more suited for long running tasks, like long http calls, especially those made to LLM APIs as they can take minutes. Within actionflows, all nodes of invoking AI agents built in zion-app.functorz.com natively can only be added inside async ones. 

### Actionflow invocation process
In order to invoke an actionflow, one needs to obtain its id, a list of arguments and optionally its version. They are found inside the project schema. 
Actionflow invocation differ based on their type. 

#### Sync actionflows
Sync actionflows can be invoked via a regular GraphQL mutation. The results will be returned in the response of the same HTTP request. 
Request:
```gql
mutation someOperationName ($args: Json!) {
 fz_invoke_action_flow(actionFlowId: "d3ea4f95-5d34-46e1-b940-91c4028caff5", versionId: 3, args: $args)
}
```

```json
{
  "args": {
    "yaml": "post_link:\n  url: \"https://zion-app.functorz.com\"\n",
    "img_id": 1020000000000111
  }
}
```
Within this query, $args corresponds to the arguments listed in the actionflow's input node. 
Response:
```json
{
  "data": {
    "fz_invoke_action_flow": {
      "img": {
        "id": 1020000000000090,
        "url": "https://fz-zion-static.functorz.com/202510252359/a64a7eb4793728a1977d3ea9e7b7e4e8/project/2000000000521152/import/1110000000000001/image/636.jpg"
      },
      "url": "https://zion-app.functorz.com"
    }
  }
}
```

#### Async actionflows
Async actionflows are triggered via a GraphQL mutation but the results are not returned in the response of the same HTTP request. Instead, a fz_create_action_flow_task is returned, containing the id of the corresponding task, which is then used for subscribing to the result in a separate GraphQL subscription. 
Mutation request:
```gql
mutation mh49tgie($args: Json!) {
 fz_create_action_flow_task(actionFlowId: "2a9068c5-8ee3-4dad-b3a4-5f3a6d365a2f", versionId: 4, args: $args)
}
```

```json
{
  "args": {
    "int": 123,
    "img_id": 1020000000000116,
    "some_text": "Dreamer",
    "datetime_with_timezone": "2025-10-23T20:13:00-07:00"
  }
}
```
Mutation response:
{
  "data": {
    "fz_create_action_flow_task": 1150000000000148
  }
}

Subscription request: 
```gql
subscription fz_listen_action_flow_result($taskId: Long!) {
  fz_listen_action_flow_result(taskId: $taskId) {
    __typename"
    output
    status
  }
}
```
```json
{ "taskId" : 1150000000000148 }
```
Subscription response:
```json
{
  "data": {
    "fz_listen_action_flow_result": {
      "__typename": "ActionFlowTaskResult",
      "output": {
        "img": {
          "id": 1020000000000089,
          "url": "https://fz-zion-static.functorz.com/202510262359/3a5f04371bf68d6c94bb890879101f0a/project/2000000000521152/import/1110000000000001/image/637.jpg"
        },
        "xyz": {
          "type": "Point",
          "coordinates": [
            131,
            22
          ]
        }
      },
      "status": "COMPLETED"
    }
  }
}
```
There might be multiple messages sent by the GraphQL subscription before the final result (inside "output") is returned, and each may contain different status values. 
The status field has the following transition rules:
```java
switch (status) {
  case CREATED -> Set.of(PROCESSING);
  case PROCESSING -> Set.of(COMPLETED, FAILED);
  default -> Set.of();
};
```

## AI Agent Protocol

### Overview
Zion.app has an integrated AI agent builder, which supports multi-modal (text, video, image) inputs and outputs, prompt templating, context fetching (via database and third-party APIs), tool use (actionflows, third-party APIs and other AI agents) and structured output (JSON according corresponding JSONSchema).  
AI Agents' results are delivered differently by the GraphQL service depending on the configuration of its output, namely, whether it is streaming and whether it is structured. A structured output can not be streamed but plain text can be either streamed or not. A structured output must be accompanied by a JSONSchema that describes the JSON's type.  
In order to invoke an AI agent, the id and the input arguments must be obtained from the project schema. An AI agent built in Zion.app's agent builder can only be invoked via the GraphQL API asynchronously. 


### Invocation process for streaming output
An example AI Agent configuration whose output is a streaming plain text will be used to illustrate this process. Its configuration is: 
```json
{
    "id": "mgzzu8jp",
    "summary": "An example summary of what the agent does",
    "inputs": {
      "mgzzufo2": {
        "type": "VIDEO",
        "displayName": "the_video",
      },
      "mh4cjjcf": {
        "type": "TEXT",
        "displayName": "text",
      },
      "mh4cjkyv": {
        "type": "BIGINT",
        "displayName": "some_int",
      },
      "mh4cjoof": {
        "type": "array",
        "itemType": "IMAGE",
        "displayName": "images",
      }
    },
    "output": "Unstructured Text"
}
```
1.  A mutation is sent to start the AI agent, supplying the arguments as inputArgs and the id as zAIConfigId. The response value only contains the id of the corresponding conversation. The keys of inputArgs should be the same keys in the inputs object from the schema. Input parameters of Image / video or other binary assets types, or arrays of such types are handled slightly differently. Their key names wihtin the inputArgs object have `_id` suffix. e.g. the following configuration  
```json
{ 
  "inputs": {
    "mgzzufo2": {
      "type": "VIDEO",
      "displayName": "the_video",
    }
  }
}
```
Corresponds to:
```json
{
  "inputArgs": {
    "mgzzufo2_id": 1030000000000002,
  }
}
```  

    Mutation request:  
    Query:
    ```gql
    mutation ZAICreateConversation($inputArgs: Map_String_ObjectScalar!, $zaiConfigId: String!) {
     fz_zai_create_conversation(inputArgs: $inputArgs, zaiConfigId: $zaiConfigId)
    }
    ```
    Variables:
    ```json
    {
      "inputArgs": {
        "mgzzufo2_id": 1030000000000002,
        "mh4cjjcf": "Just some text",
        "mh4cjkyv": 23,
        "mh4cjoof_id": [
          1020000000000097,
          1020000000000111,
          1020000000000120
        ]
      },
      "zaiConfigId": "mgzzu8jp"
    }
    ```
    Mutation response:
    ```json
    {
      "data": {
        "fz_zai_create_conversation": 1480
      }
    }
    ```
2.  Using the obtained conversation id to subscribe to the result of the previous invocation of the AI Agent. Multiple messages may be received. The messages' status may transition from IN_PROGRESS to STREAMING to eventually COMPLETED. The last message always gives you COMPLETED status and its data field will contain the consolidated output from all the previous STEAMING messages' data field. 
For models that have reasoning content output, it works similarly as the actual output. i.e. Partial reasoning content will be emitted first in multiple messages in the reasoningContent field, and then when everything is ready, the entirety of reasoningContent will be emitted again the COMPLETED message. 
    Subscription request:  
    Query: 
    ```gql
    subscription ZaiListenConversationResult($conversationId: Long!) {
      fz_zai_listen_conversation_result(conversationId: $conversationId) {
        conversationId
        status
        reasoningContent
        images {
          id
          __typename
        }
        data
        __typename
      }
    }
    ```
    Variables: 
    ```json
    {
      "conversationId": 1480
    }
    ```
    Subscription response messages:
    ```json
    {
      "data": {
        "fz_zai_listen_conversation_result": {
          "__typename": "ConversationResult",
          "conversationId": 1480,
          "data": null,
          "images": null,
          "reasoningContent": null,
          "status": "IN_PROGRESS"
        }
      }
    }
    ```
    ```json
    {
      "data":{
        "fz_zai_listen_conversation_result": {
          "__typename": "ConversationResult",
          "conversationId": 1480,
          "data": "This collection features three images and a short video. Two photos show the famous Chinese comedian and actor, Zhao Benshan. A third",
          "images": null,
          "reasoningContent": null,
          "status": "STREAMING"
        }
      }
    }
    ```
    ```json
    {
      "data":{
        "fz_zai_listen_conversation_result": {
          "__typename": "ConversationResult",
          "conversationId": 1480,
          "data": " image is an anime illustration of a young woman in a \"SHOHOKU\" basketball jersey, resembling the character Haruko Akagi from the series *Slam Dunk*.",
          "images": null,
          "reasoningContent": null,
          "status": "STREAMING"
        }
      }
    }
    ```
    ```json
    {
      "data":{
        "fz_zai_listen_conversation_result": {
          "__typename": "ConversationResult",
          "conversationId": 1480,
          "data": "This collection features three images and a short video. Two photos show the famous Chinese comedian and actor, Zhao Benshan. A third image is an anime illustration of a young woman in a \"SHOHOKU\" basketball jersey, resembling the character Haruko Akagi from the series *Slam Dunk*.",
          "images": null,
          "reasoningContent": null,
          "status": "COMPLETED"
        }
      }
    }
    ```
### Invocation process for non streaming plain text output
1. The mutation step is identical to the one inside the invocation process for streaming output. I.e. send mutation fz_zai_create_conversation(inputArgs: $inputArgs, zaiConfigId: $zaiConfigId) to obtain the conversation id. 

2. There will be no messages in the STREAMING state. i.e. A message of IN_PROGRESS status will be sent by the server, followed directly by the COMPLETED message with the final result. 

### Invocation process for AI agents that use models with image output
Certain model support image output, like gemini-2.5-flash-image.  
Their invocation process is the same as the plain text ones. Except that in the COMPLETED message, the field images will be filled with content. The images
Their output will be no different from plain-text only outputs, regardless of the streaming setting. Their COMPLETED message looks like:
```json
{
  "data": {
    "fz_zai_listen_conversation_result": {
      "__typename": "ConversationResult",
      "conversationId": 1494,
      "data": "I merged the three images into one, combining elements from each to create a new, unique image.\n",
      "images": [
        {
          "__typename": "FZ_Image",
          "id": 1020000000000164
        }
      ],
      "reasoningContent": null,
      "status": "COMPLETED"
    }
  }
}
```
The ids for FZ_Image in images represent the ids in Zion's file / asset system. Refer to zion-binary-asset-upload-rules


### Invocation process for structured output
AI agents with structured output cannot be streaming. They also always come with a JSONSchema in their configuration. 
```json
{
  "output": {
      "type": "object",
      "properties": {
        "httpLink": {
          "type": "string"
        },
        "reasoning": {
          "type": "string"
        }
      },
      "required": [
        "httpLink",
        "reasoning"
      ]
    }
}
```
There will be no messages from the GraphQL server that are in the "STREAMING" state. There will be one "COMPLETED" message where the data field is a JSON that satisfies the JSONSchema. 
e.g. 
```json
{
  "httplink": "https://www.google.com/calendar/event?eid=MTcxN2U3cHAzaDFtYTdxYzd0bGV0aHNvYmsgamlhbmd5YW9rYWlqb2huQG0",
  "explanation": "No existing events were found on 2025-10-24 in America/Los_Angeles, so there are no conflicts. Preference is mornings; scheduled 08:00–08:10 at Los Altos High school. With no adjacent events, transit checks to previous and next events are trivially satisfied."
}
```

### Continuing conversation
After AI Agent returns result (status = COMPLETED), the conversation can be continued by calling fz_zai_send_ai_message. 
The subscription of fz_zai_listen_conversation_result on the same conversationId will continue to receive messages.  
e.g.  
  mutation request:  
  ```gql
  mutation continue($conversationId: Long!, $text: String) {
    fz_zai_send_ai_message(conversationId: $conversationId, text: $text)
  }
  ```
  Variables: 
  ```json
  {
    "conversationId": 1480,
    "text": "make it about the sun"
  }
  ```
The response from the corresponding fz_zai_listen_conversation_result will then continue. Similar to what happens after one initiates a converation with an AI agent, going through the same IN_PROGRESS -> (STREAMING) -> COMPLETED status transition. 

### Stopping conversation
For converations still in "IN_PROGRESS" or "STREAMING" states, they can be stopped by calling fz_zai_stop_responding, which always returns true. 
When called on conversations with "COMPLETED" state, a 400 error will be thrown inside the `errors` field of the GraphQL response. 
e.g.  
  mutation request:  
  ```gql
  mutation continue($conversationId: Long!) {
    fz_zai_stop_responding(conversationId: $conversationId)
  }
  ```
  Variables: 
  ```json
  {
    "conversationId": 1480
  }
  ```

## Binary Asset Upload
All binary assets (images, videos, files) are stored on object storage services (e.g., S3). Their storage path is recorded in Zion's database. **When referencing these assets in other tables, you must store only the asset's Zion ID, not its path or URL.**

### Upload Workflow
To upload a binary asset and obtain its Zion ID, you must follow a strict two-step process:

#### Step 1: Obtain a Presigned Upload URL
1. **Calculate the MD5 hash** of the file (raw 128-bit hash), then Base64-encode it.
2. **Call the appropriate GraphQL mutation** to request a presigned upload URL. Use the mutation that matches your asset type:

   - `imagePresignedUrl` for images
   - `videoPresignedUrl` for videos
   - `filePresignedUrl` for other files

   Provide:
   - The Base64-encoded MD5 hash
   - The file format/suffix (see `MediaFormat` below)
   - (Optional) Access control (see `CannedAccessControlList` below)

   ##### Example GraphQL Mutations
   ```graphql
   mutation GetImageUploadUrl($md5: String!, $suffix: MediaFormat!, $acl: CannedAccessControlList) {
     imagePresignedUrl(imgMd5Base64: $md5, imageSuffix: $suffix, acl: $acl) {
       imageId
       uploadUrl
       uploadHeaders
     }
   }

   mutation GetVideoUploadUrl($md5: String!, $format: MediaFormat!, $acl: CannedAccessControlList) {
     videoPresignedUrl(videoMd5Base64: $md5, videoFormat: $format, acl: $acl) {
       videoId
       uploadUrl
       uploadHeaders
     }
   }

   mutation GetFileUploadUrl($md5: String!, $format: MediaFormat!, $name: String, $suffix: String, $sizeBytes: Int, $acl: CannedAccessControlList) {
     filePresignedUrl(
       md5Base64: $md5
       format: $format
       name: $name
       suffix: $suffix
       sizeBytes: $sizeBytes
       acl: $acl
     ) {
       fileId
       uploadHeaders
       uploadUrl
     }
   }
   ```

   - **`CannedAccessControlList`** (recommended: `PRIVATE`):
     - AUTHENTICATE_READ, AWS_EXEC_READ, BUCKET_OWNER_FULL_CONTROL, BUCKET_OWNER_READ, DEFAULT, LOG_DELIVERY_WRITE, PRIVATE, PUBLIC_READ, PUBLIC_READ_WRITE
   - **`MediaFormat`**:
     - CSS, CSV, DOC, DOCX, GIF, HTML, ICO, JPEG, JPG, JSON, MOV, MP3, MP4, OTHER, PDF, PNG, PPT, PPTX, SVG, TXT, WAV, WEBP, XLS, XLSX, XML

#### Step 2: Upload the File and Use the Returned ID
1. The mutation response includes:
   - The asset's unique ID (`imageId`, `videoId`, or `fileId`)
   - A presigned `uploadUrl`
   - Any required `uploadHeaders`
2. **Upload the file**:
   - Perform an HTTP `PUT` request to the `uploadUrl` with the raw file data
   - Include any `uploadHeaders` from the mutation response
3. **Reference the asset**:
   - Use the returned ID as the value for the corresponding `*_id` field in your Zion data mutation (e.g., `cover_image_id: returnedImageId`)

> **Note:** This two-step process is **mandatory** for all media uploads in Zion.app.

## Third-Party APIs

A project built on Zion.app can have many third-party HTTP APIs imported. These are separated into two categories: query or mutation, roughly (though not always the case) corresponding to the semantics of HTTP GET vs POST.  
Each API is stored in the following data structure:
```typescript
type ScalarType = 'string' | 'boolean' | 'number' | 'integer';
type TypeDefinition =
  | ScalarType
  | { [key: string]: TypeDefinition | TypeDefinition[] };

interface ThirdPartyApiConfig {
  id: string;
  name: string;
  operation: 'query' | 'mutation';
  inputs: { [key: string]: TypeDefinition };
  outputs: { [key: string]: TypeDefinition };
}
```
N.B. The value of the operation field within ThirdPartyApiConfig determines the root GraphQL field. i.e. query -> query operation_${id}, and mutation -> mutation operation_${id}.

### Invocation process
Each input should be provided unless the user asks to remove it.  
e.g. 
Given TPA configuration as follows:
```json
      {
        "id": "lzb3ownk",
        "inputs": {
          "body": {
            "summary": "string",
            "location": "string",
            "description": "string",
            "start": {
              "dateTime": "string",
              "timeZone": "string"
            },
            "end": {
              "dateTime": "string",
              "timeZone": "string"
            },
            "attendees": [
              "string"
            ]
          },
          "Authorization": "string"
        },
        "outputs": {
          "body": {
            "kind": "string",
            "etag": "string",
            "id": "string",
            "status": "string",
            "htmlLink": "string",
            "created": "string",
            "updated": "string",
            "summary": "string",
            "description": "string",
            "location": "string",
            "creator": {
              "email": "string",
              "self": "boolean"
            },
            "organizer": {
              "email": "string",
              "self": "boolean"
            },
            "start": {
              "dateTime": "string",
              "timeZone": "string"
            },
            "end": {
              "dateTime": "string",
              "timeZone": "string"
            },
            "iCalUID": "string",
            "sequence": "number",
            "reminders": {
              "useDefault": "boolean"
            },
            "eventType": "string"
          }
        },
        "operation": "mutation"
      }
```
The corresponding GraphQL query should be
```gql
mutation request_${nonce}($summary: String, $location: String, $description: String, $start_dateTime: String, $start_timeZone: String, $end_dateTime: String, $end_timeZone: String, $attendees:[String], $Authorization: String) {
  operation_lzb3ownk(fz_body: {}, arg1: $_1, arg2: $_2) {
    responseCode
    field_200_json {
      {subFieldSelections}
    }
 }
}
```
field_200_json is a fixed fields for all third-party API derived GraphQL operation. It means the response that's valid for all 2xx response codes. 

The responseCode subfield should always be checked, in case 5xx or 4xx codes are returned, which means field_200_json would be empty. 
