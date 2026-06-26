---
name: enonic-guillotine-query-builder
description: Composes, debugs, and optimizes Guillotine GraphQL queries for Enonic XP headless content delivery. Covers query construction, variable usage, filtering, aggregation, pagination, sorting, and TypeScript type generation from the auto-generated Guillotine schema. Use when writing or troubleshooting Guillotine queries, querying custom content types through GraphQL, or generating typed interfaces from Guillotine responses. Don't use for content type XML definitions, non-Enonic GraphQL APIs (Apollo, Hasura), server-side lib-content queries, or Guillotine deployment and CORS configuration.
license: MIT
metadata:
  author: webmaxru
  version: "1.5"
---

# Enonic Guillotine Query Builder

## Procedures

**Step 1: Scan the workspace for existing Guillotine usage**
1. Execute `node scripts/find-guillotine-targets.mjs .` to inventory files containing Guillotine markers (query strings, library imports, endpoint references).
2. If a Node runtime is unavailable, search the workspace manually for `guillotine`, `queryDsl`, `queryDslConnection`, or `/lib/guillotine` in `.ts`, `.js`, `.graphql`, and `.gql` files.
3. Note the Guillotine version in use: if `query(query: "...")` string-based fields are found, the project uses the deprecated 5.x-style API; if `queryDsl` / `queryDslConnection` are found, the project uses 6.x+ DSL. Check for `exports.extensions` in `guillotine/guillotine.js` to detect Guillotine 7 Extensions API usage.
4. If both styles coexist, flag the deprecated usage for migration.

**Step 2: Load the Guillotine API reference**
1. Read `references/guillotine-reference.md` before composing any query.
2. Read `references/compatibility.md` when the workspace targets or migrates between Guillotine versions.

**Step 3: Determine the query shape**
1. Identify the operation the user needs:
   - **Single content fetch**: Use `get(key)`.
   - **Direct children**: Use `getChildren(key)` or `getChildrenConnection(key)` for pagination.
   - **Filtered search**: Use `queryDsl(query)` for a flat list or `queryDslConnection(query)` for pagination, aggregations, or highlighting.
   - **Content type metadata**: Use `getType(name)` or `getTypes`.
2. If pagination is needed, prefer connection variants (`queryDslConnection`, `getChildrenConnection`) and guide the caller to pass `after` / `first`.
3. If aggregations or highlighting are needed, require `queryDslConnection` — these features are not available on `queryDsl`.

**Step 4: Construct the content type fragment**
1. Derive the GraphQL type name from the content type descriptor by replacing dots (`.`) and colons (`:`) with underscores (`_`), and removing hyphens (`-`) while capitalizing the following letter. The first letter of each segment after a colon is capitalized. Example: `com.enonic.app.myapp:BlogPost` → `com_enonic_app_myapp_BlogPost`. For built-in types: `portal:template-folder` → `portal_TemplateFolder`.
2. Use an inline fragment to access the type-specific `data` field: `... on <GraphQLTypeName> { data { ... } }`.
3. For content references (ContentSelector, ImageSelector, MediaSelector), follow the reference with a nested inline fragment on the target type.
4. For RichText / HtmlArea fields, include `processedHtml` and optionally `links`, `images`, `macros` sub-fields. Use the `processHtml` input argument for absolute URLs, srcset widths (`imageWidths`), or responsive sizes (`imageSizes`).

**Step 5: Build query filters and sorting**
1. Use Query DSL input types. Each `QueryDSLInput` must contain exactly one expression field.
2. Combine multiple conditions using `boolean` with `must`, `should`, `mustNot`, and `filter` arrays.
3. For date or numeric ranges, use the `range` expression with `gt`/`gte`/`lt`/`lte` and the correct `DSLExpressionValueInput` type (`localDate`, `localDateTime`, `instant`, `long`, `double`).
4. For sorting, use `SortDslInput` with `field` and `direction` (`ASC` / `DESC`).
5. Read `references/examples.md` when the query pattern matches a documented example.

**Step 6: Add aggregations and highlighting (if needed)**
1. Pass `aggregations` as an array of `AggregationInput` objects on `queryDslConnection`.
2. Each aggregation requires a unique `name` and exactly one aggregation type field (`terms`, `dateRange`, `stats`, etc.).
3. For highlighting, pass `highlight` with a `properties` array specifying `propertyName` for each field to highlight.
4. Read aggregation and highlight results from `aggregationsAsJson` and `highlightAsJson` on the connection result.

**Step 7: Generate TypeScript types (if requested)**
1. Read `assets/guillotine-query.template.ts` as the starting template.
2. Replace `__APP_KEY__`, `__CONTENT_TYPE__`, `__GRAPHQL_TYPE__`, and `__FIELDS__` placeholders with the actual content type values.
3. Add typed fields to the `Data` interface matching the content type schema fields requested in the query.
4. For connection queries, use the `ContentConnection<T>` generic with the specific content type.

**Step 8: Set site context (if applicable)**
1. If the query targets a specific site, set `siteKey` on the `guillotine` field or instruct the caller to set the `X-Guillotine-SiteKey` HTTP header.
2. Use `${site}` placeholder in path arguments for site-relative queries.
3. Use `_path(type: siteRelative)` to return site-relative paths.

**Step 9: Validate the query**
1. Verify all inline fragment type names use underscores, not the original descriptor format.
2. Confirm `queryDsl` / `queryDslConnection` are used instead of the deprecated `query` / `queryConnection`.
3. Ensure `QueryDSLInput` objects contain exactly one expression field.
4. Verify `DSLExpressionValueInput` objects contain exactly one value type field.
5. Check that aggregation and highlight are only used on connection variants.
6. For Guillotine 7+ projects, verify `pageUrl` / `mediaUrl` / `imageUrl` / `attachmentUrl` use `Json` type for `params` argument, not `String`.
7. Read `references/troubleshooting.md` if the query returns unexpected nulls, empty results, or type errors.

## Error Handling
* If `get` returns null, verify the key is a valid content path or ID and that the correct branch (draft vs master) is targeted.
* If inline fragment fields are null, confirm the GraphQL type name uses underscores and matches the content type descriptor exactly.
* If `queryDsl` returns empty results, simplify to `matchAll: {}` to confirm data exists, then re-add filters one at a time.
* If aggregation or highlight results are null, verify the query uses `queryDslConnection`, not `queryDsl`.
* If the deprecated `query` field is used, read `references/compatibility.md` to migrate to `queryDsl` with DSL syntax.
* If `scripts/find-guillotine-targets.mjs` cannot run, scan the workspace manually for Guillotine markers and continue.
