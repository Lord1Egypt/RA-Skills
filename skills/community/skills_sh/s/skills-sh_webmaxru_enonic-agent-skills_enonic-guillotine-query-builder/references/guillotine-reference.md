# Guillotine GraphQL API Reference

Condensed reference for composing Guillotine queries against Enonic XP.
Source: https://developer.enonic.com/docs/guillotine/stable

Guillotine 7.x is the current stable release (requires XP 7.14.0+).

## Entry Point

Every query starts with the `guillotine` root field:

```graphql
{
  guillotine {
    # HeadlessCms fields here
  }
}
```

Pass `siteKey` when working in a site context (Guillotine 7.1+):

```graphql
{
  guillotine(siteKey: "/my-site") { ... }
}
```

Or set the HTTP header `X-Guillotine-SiteKey: <IdOrPathToSite>` (6.x+).

## HeadlessCms Fields (Query Operations)

| Field | Purpose |
|---|---|
| `get(key: ID): Content` | Fetch a single content by ID or path |
| `getChildren(key: ID, offset: Int, first: Int, sort: String): [Content]` | Fetch direct children of a content |
| `getChildrenConnection(key: ID, after: String, first: Int, sort: String): ContentConnection` | Children as a Relay connection |
| `getPermissions(key: ID): Permissions` | Permissions on a content |
| `getSite: portal_Site` | Parent site of current context |
| `queryDsl(query: QueryDSLInput, offset: Int, first: Int, sort: [SortDslInput]): [Content]` | Query content with DSL |
| `queryDslConnection(query: QueryDSLInput!, after: String, first: Int, sort: [SortDslInput], aggregations: [AggregationInput], highlight: HighlightInputType): QueryDSLContentConnection` | DSL query as a connection with aggregations and highlight |
| `getType(name: String!): ContentType` | Content type metadata |
| `getTypes: [ContentType]` | All available content types |

> `query` and `queryConnection` are **deprecated** since Guillotine 6 Update 1. Use `queryDsl` / `queryDslConnection` instead.

## Common Arguments

| Argument | Description | Default |
|---|---|---|
| `key` | Content path or content ID | — |
| `offset` | Start index for paging | `0` |
| `first` | Number of items to fetch | `10` |
| `sort` | Sorting expression string | `"_score DESC"` |

## Content Interface Fields

All content types share these fields. Custom content types add a `data` field.

| Field | Type | Notes |
|---|---|---|
| `_id` | `ID!` | Content ID |
| `_name` | `String!` | Content name |
| `_path(type: ContentPathType)` | `String!` | Full or site-relative path |
| `_references` | `[Content]` | Outbound content references |
| `_score` | `Float` | Relevance score (available on search results) |
| `_project` | `String` | Project name |
| `_branch` | `String` | Branch name (`draft` or `master`) |
| `displayName` | `String` | Display name |
| `type` | `String` | Content type descriptor |
| `contentType` | `ContentType` | Typed content type metadata (name, form, icon) |
| `creator` | `PrincipalKey` | Content creator |
| `modifier` | `PrincipalKey` | Last content modifier |
| `owner` | `PrincipalKey` | Content owner |
| `createdTime` | `String` | ISO datetime |
| `modifiedTime` | `String` | ISO datetime |
| `language` | `String` | Language code |
| `valid` | `Boolean` | Content validity |
| `hasChildren` | `Boolean` | Has children |
| `dataAsJson` | `JSON` | Raw data as JSON |
| `xAsJson` | `JSON` | Extra data as JSON |
| `pageAsJson(resolveTemplate: Boolean, resolveFragment: Boolean)` | `JSON` | Page specific information |
| `parent` | `Content` | Parent content |
| `site` | `portal_Site` | Link to nearest site |
| `children(offset, first, sort)` | `[Content]` | Direct children |
| `childrenConnection(after, first, sort)` | `ContentConnection` | Children as a connection |
| `publish` | `PublishInfo` | from, to, first, time timestamps |
| `attachments` | `[Attachment]` | File attachments |
| `components(resolveTemplate: Boolean, resolveFragment: Boolean)` | `[Component]` | Page components (flattened) |
| `pageUrl(type: UrlType, params: Json)` | `String` | Generated URL for this content. `params` is `Json` type in Guillotine 7+ |
| `pageTemplate` | `Content` | Related page template content |
| `x` | `[ExtraData]` | eXtra Data |
| `permissions` | `Permissions` | Content permissions |

### Media-Specific Fields

Content types under `media:*` additionally expose:

| Field | Type | Notes |
|---|---|---|
| `mediaUrl(download: Boolean, type: UrlType, params: Json)` | `String` | URL to the media attachment |
| `imageUrl(scale: String!, quality: Int, type: UrlType, background: String, format: String, filter: String, params: Json)` | `String` | Scaled image URL (`media:image` only) |

## Inline Fragments for Custom Types

Custom content types are accessed via inline fragments. The type name is derived from the content type descriptor by replacing dots (`.`) and colons (`:`) with underscores (`_`), and removing hyphens (`-`) while capitalizing the following letter. The first letter of each segment after a colon is capitalized.

```
com.enonic.app.myapp:BlogPost → com_enonic_app_myapp_BlogPost
portal:template-folder        → portal_TemplateFolder
base:unstructured              → base_Unstructured
```

Example:

```graphql
{
  guillotine {
    get(key: "/blog/first-post") {
      displayName
      ... on com_enonic_app_myapp_BlogPost {
        data {
          title
          body {
            processedHtml
          }
          author {
            displayName
          }
        }
      }
    }
  }
}
```

## Connection Types (Pagination)

### ContentConnection / QueryDSLContentConnection

| Field | Type |
|---|---|
| `totalCount` | `Int!` |
| `edges` | `[ContentEdge]` |
| `pageInfo` | `PageInfo` |
| `aggregationsAsJson` | `JSON` (QueryDSLContentConnection only) |
| `highlightAsJson` | `JSON` (QueryDSLContentConnection only) |

### ContentEdge

| Field | Type |
|---|---|
| `node` | `Content!` |
| `cursor` | `String!` |

### PageInfo

| Field | Type |
|---|---|
| `startCursor` | `String!` |
| `endCursor` | `String!` |
| `hasNext` | `Boolean!` |

## Query DSL Input Types

`QueryDSLInput` accepts exactly one expression field:

| Field | Type | Purpose |
|---|---|---|
| `boolean` | `BooleanDSLExpressionInput` | Compound boolean (must, should, mustNot, filter) |
| `term` | `TermDSLExpressionInput` | Exact-value match |
| `like` | `LikeDSLExpressionInput` | Wildcard match (`*`) |
| `in` | `InDSLExpressionInput` | Match any value in a list |
| `range` | `RangeDSLExpressionInput` | lt, lte, gt, gte comparisons |
| `exists` | `ExistsDSLExpressionInput` | Field exists check |
| `fulltext` | `FulltextDSLExpressionInput` | Full-text search |
| `ngram` | `NgramDSLExpressionInput` | Ngram search (partial match) |
| `stemmed` | `StemmedDSLExpressionInput` | Stemmed search with language |
| `matchAll` | `MatchAllDSLExpressionInput` | Match everything |
| `pathMatch` | `PathMatchDSLExpressionInput` | Match by path prefix |

### BooleanDSLExpressionInput

| Field | Description |
|---|---|
| `must` | All sub-queries must match, contributes to score |
| `should` | At least one should match |
| `mustNot` | Must not match |
| `filter` | Must match, does not affect score |
| `boost` | Score multiplier |

### TermDSLExpressionInput

```graphql
term: { field: "type", value: { string: "com.enonic.app.myapp:Post" }, boost: 2.0 }
```

Supports `boost` for relevance scoring.

### RangeDSLExpressionInput

```graphql
range: {
  field: "data.publishDate",
  gte: { localDateTime: "2024-01-01T00:00:00" },
  lt: { localDateTime: "2025-01-01T00:00:00" }
}
```

Supports `boost` for relevance scoring.

### DSLExpressionValueInput

Exactly one type field:
`string`, `double`, `long`, `boolean`, `localDate`, `localDateTime`, `localTime`, `instant`

### InDSLExpressionInput

Matches content where the field contains any of the listed values. Uses separate typed value arrays — only one array field should be provided per expression:

| Field | Type | Description |
|---|---|---|
| `field` | `String!` | Property name to search |
| `boost` | `Float` | Score multiplier |
| `stringValues` | `[String]` | String values |
| `doubleValues` | `[Float]` | Float values |
| `longValues` | `[Int]` | Integer values |
| `booleanValues` | `[Boolean]` | Boolean values |
| `localDateValues` | `[Date]` | Date values (e.g. `2015-03-16`) |
| `localDateTimeValues` | `[LocalDateTime]` | DateTime values without timezone (e.g. `2015-03-16T10:00:02`) |
| `localTimeValues` | `[LocalTime]` | Time values without date (e.g. `10:00:03`) |
| `instantValues` | `[DateTime]` | Point-on-timeline values (e.g. `2015-03-16T10:00:02Z`) |

### Other DSL Expression Inputs

Most DSL expression types (`like`, `in`, `exists`, `stemmed`, `matchAll`, `pathMatch`) support the `boost` parameter for relevance scoring. `fulltext` and `ngram` do **not** support `boost`. `fulltext`, `ngram`, and `stemmed` accept `fields`, `query`, and `operator` (`OR` or `AND`). `stemmed` also requires `language`.

## SortDslInput

| Field | Type | Description |
|---|---|---|
| `field` | `String!` | Property path to sort on |
| `direction` | `DslSortDirectionType` | `ASC` or `DESC` |
| `location` | `GeoPointSortDslInput` | Optional geo-sort origin |
| `unit` | `DslGeoPointDistanceType` | Distance unit for geo-sort |

## Aggregation Input Types

Pass via `aggregations` on `queryDslConnection`. Each `AggregationInput` takes a `name`, exactly one aggregation type, and an optional `subAggregations` array for nested aggregations:

| Type | Purpose |
|---|---|
| `terms` | Bucket by field value |
| `stats` | Min, max, avg, sum, count |
| `range` | Numeric range buckets |
| `dateRange` | Date range buckets |
| `dateHistogram` | Date interval buckets |
| `getDistance` | Geo-distance buckets |
| `min` / `max` / `count` | Simple single-value aggregations |

Each aggregation also accepts `subAggregations: [AggregationInput]` for nesting.

Results are returned in `aggregationsAsJson`.

## Highlight Input Types

Pass via `highlight` on `queryDslConnection`:

| Field | Default |
|---|---|
| `encoder` | `default` (no encoding). Use `html` for HTML encoding |
| `tagsSchema` | Unset. Set to `styled` for built-in tag schema |
| `fragmenter` | `span`. Alternative: `simple` |
| `fragmentSize` | `100` |
| `noMatchSize` | `0` (nothing returned if no match) |
| `numberOfFragments` | `5` |
| `order` | `none`. Set to `score` to sort by relevance |
| `preTag` / `postTag` | `<em>` / `</em>` |
| `requireFieldMatch` | `true` |
| `properties` | Array of `HighlightPropertiesInputType` with `propertyName` |

Each `HighlightPropertiesInputType` accepts per-property overrides: `propertyName` (required), `fragmenter`, `fragmentSize`, `noMatchSize`, `numberOfFragments`, `order`, `preTag`, `postTag`, `requireFieldMatch`.

Results are returned in `highlightAsJson`.

## RichText Type

Returned for HtmlArea fields:

| Field | Description |
|---|---|
| `raw` | Unprocessed HTML |
| `processedHtml` | Processed HTML with resolved links, images, macros |
| `macrosAsJson` | Detected macros as JSON array (alternative to `macros` field) |
| `macros` | Detected macros with ref, name, descriptor, config |
| `images` | Detected images with ref, content, style (name, aspectRatio, filter) |
| `links` | Detected links with ref, uri, media (intent, content), content |

The `links` field distinguishes between media and content links:
- `media` — non-null for media links; includes `intent` (`download` or `inline`) and `content`
- `content` — non-null for content links; null for media links

Use `processHtml` input argument for image processing:

```graphql
body(processHtml: { imageWidths: [600, 992], imageSizes: "(max-width: 600px) 100vw, 50vw", type: absolute }) {
  processedHtml
  images { ref }
}
```

`imageSizes` specifies image widths for specific browser resolutions in the format `(media-condition) width`, comma-separated.

## Attachment Type

| Field | Type | Description |
|---|---|---|
| `name` | `String` | Attachment name |
| `label` | `String` | Attachment label |
| `size` | `Int` | Attachment size |
| `mimeType` | `String` | Attachment MIME type |
| `attachmentUrl(download: Boolean, type: UrlType, params: Json)` | `String` | Attachment URL. `params` is `Json` type in Guillotine 7+ |

## ContentType Utility Fields

The `ContentType` type returned by `getType` and `getTypes` includes utility fields for fetching content instances directly:

| Field | Type | Description |
|---|---|---|
| `getInstances(offset, first, query, sort)` | `[Content]` | Contents of this type |
| `getInstanceConnection(after, first, query, sort)` | `ContentConnection` | Contents of this type as a connection |
| `formAsJson` | `JSON` | Content type form schema as JSON |

## Media Type URL Fields

Media content types (`media_Image`, `media_Vector`, etc.) expose additional URL fields not present on the base `Content` interface:

| Field | Type | Description |
|---|---|---|
| `imageUrl(scale: String!, quality: Int, type: UrlType, params: Json)` | `String` | Scaled image URL. `scale` controls dimensions (e.g. `"block(800,200)"`, `"width(600)"`). `params` is `Json` type in Guillotine 7+ |
| `mediaUrl(download: Boolean, type: UrlType, params: Json)` | `String` | Media download/inline URL. `params` is `Json` type in Guillotine 7+ |

These fields are accessed via inline fragments on the specific media type:

```graphql
... on media_Image {
  imageUrl(scale: "block(800,200)", type: absolute)
}
```

## Key Enum Types

| Enum | Values |
|---|---|
| `UrlType` | `server`, `absolute` |
| `ContentPathType` | `siteRelative` |
| `MediaIntentType` | `download`, `inline` |
| `DslOperatorType` | `OR`, `AND` |
| `DslSortDirectionType` | `ASC`, `DESC` |
| `DslGeoPointDistanceType` | `m`, `meters`, `in`, `inch`, `yd`, `yards`, `ft`, `feet`, `km`, `kilometers`, `NM`, `nmi`, `nauticalmiles`, `mm`, `millimeters`, `cm`, `centimeters`, `mi`, `miles` |
| `ComponentType` | `page`, `layout`, `image`, `part`, `text`, `fragment` |
| `HighlightEncoderType` | `default`, `html` |
| `HighlightFragmenterType` | `simple`, `span` |
| `HighlightOrderType` | `score`, `none` |
| `HighlightTagsSchemaType` | `styled` |
