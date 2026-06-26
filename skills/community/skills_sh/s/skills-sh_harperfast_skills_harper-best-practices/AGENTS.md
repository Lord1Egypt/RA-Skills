# Harper Best Practices

Guidelines for building scalable, secure, and performant applications on Harper. These practices cover everything from initial schema design to advanced deployment strategies.

## 1. Schema & Data Design

### 1.1 Adding Tables with Schemas

Instructions for the agent to follow when adding tables to a Harper database.

#### When to Use

Use this skill when you need to define new data structures or modify existing ones in a Harper database.

#### How It Works

1. **Create Dedicated Schema Files**: Prefer having a dedicated schema `.graphql` file for each table. Check the `config.yaml` file under `graphqlSchema.files` to see how it's configured. It typically accepts wildcards (e.g., `schemas/*.graphql`), but may be configured to point at a single file.
2. **Use Directives**: All available directives for defining your schema are defined in `node_modules/harper/schema.graphql`. Common directives include `@table`, `@export`, `@primaryKey`, `@indexed`, and `@relationship`.
3. **Define Relationships**: Link tables together using the `@relationship` directive. For more details, see the [Defining Relationships](defining-relationships.md) skill.
4. **Enable Automatic APIs**: If you add `@table @export` to a schema type, Harper automatically sets up REST and WebSocket APIs for basic CRUD operations against that table. **Important**: REST endpoints also require `rest: true` in `config.yaml` — without it, `@export`ed tables will not respond to HTTP requests. For a detailed list of available endpoints and how to use them, see the [Automatic REST APIs](automatic-apis.md) skill.
   - `GET /{TableName}`: Describes the schema itself.
   - `GET /{TableName}/`: Lists all records (supports filtering, sorting, and pagination via query parameters). See the [Querying REST APIs](querying-rest-apis.md) skill for details.
   - `GET /{TableName}/{id}`: Retrieves a single record by its ID.
   - `POST /{TableName}/`: Creates a new record.
   - `PUT /{TableName}/{id}`: Updates an existing record.
   - `PATCH /{TableName}/{id}`: Performs a partial update on a record.
   - `DELETE /{TableName}/`: Deletes all records or filtered records.
   - `DELETE /{TableName}/{id}`: Deletes a single record by its ID.
5. **Consider Table Extensions**: If you are going to [extend the table](./extending-tables.md) in your resources, then do not `@export` the table from the schema.

#### Examples

In a hypothetical `schemas/ExamplePerson.graphql`:

```graphql
type ExamplePerson @table @export {
	id: ID @primaryKey
	name: String
	tag: String @indexed
}
```

### 1.2 Schema Design and GraphQL Tooling

Instructions for the agent to follow when designing Harper schemas, applying core directives, and configuring GraphQL tooling.

#### When to Use

Apply this rule when creating or modifying Harper schema files, configuring `graphqlSchema` in `config.yaml`, or deciding which directives to apply to tables and fields. Use it any time a component needs tables, indexes, primary keys, or exported endpoints defined.

#### How It Works

1. **Create a schema file** using standard GraphQL type definitions with Harper-specific directives. Name it (e.g., `schema.graphql`) and place it in your component directory.

2. **Register the schema** in the component's `config.yaml` using the `graphqlSchema` plugin:

   ```yaml
   graphqlSchema:
     files: 'schema.graphql'
   ```

   Both plugins and applications can specify schemas.

3. **Mark types as tables** with `@table`. The type name becomes the table name by default:

   ```graphql
   type Dog @table {
   	id: Long @primaryKey
   	name: String
   	breed: String
   	age: Int
   }
   ```

4. **Designate a primary key** with `@primaryKey` on exactly one field per type. Primary keys must be unique; duplicate-key inserts are rejected. If no primary key is provided on insert, Harper auto-generates one:
   - `String` or `ID` → UUID string
   - `Int`, `Long`, or `Any` → auto-incrementing integer

   Use `Long` or `Any` for auto-generated numeric keys; `Int` is 32-bit and may be insufficient for large tables.

5. **Add secondary indexes** with `@indexed` on any field that will be used for filtering in REST queries, SQL, or NoSQL operations:

   ```graphql
   type Breed @table {
   	id: Long @primaryKey
   	name: String @indexed
   }
   ```

   If the field value is an array, each element is individually indexed. Null values are indexed by default.

6. **Expose a table as an external endpoint** with `@export`. The optional `name` parameter sets the URL path segment:

   ```graphql
   type MyTable @table @export(name: "my-table") {
   	id: Long @primaryKey
   }
   ```

   Without `name`, the type name is used as the path segment.

7. **Configure `@table` arguments** as needed for database placement, expiration, eviction, and replication:

   | Argument       | Type      | Default                       | Description                                                   |
   | -------------- | --------- | ----------------------------- | ------------------------------------------------------------- |
   | `table`        | `String`  | type name                     | Override the table name                                       |
   | `database`     | `String`  | `"data"`                      | Database to place the table in                                |
   | `expiration`   | `Int`     | —                             | Seconds until a record goes stale                             |
   | `eviction`     | `Int`     | `0`                           | Additional seconds after `expiration` before physical removal |
   | `scanInterval` | `Int`     | `(expiration + eviction) / 4` | Seconds between eviction scans                                |
   | `replicate`    | `Boolean` | `true`                        | Enable replication of this table                              |

8. **Apply additional field directives** where needed:
   - `@createdTime` — auto-assigns Unix epoch milliseconds on record creation
   - `@updatedTime` — auto-assigns Unix epoch milliseconds on each update
   - `@embed(source: "fieldName", model: "modelName")` — computes an embedding vector on write; attribute type must be `[Float]`
   - `@hidden` — suppresses the field from MCP tool descriptors and OpenAPI documents (not an access-control mechanism)

9. **Restrict extra properties** with `@sealed` if records must not include properties beyond those declared:
   ```graphql
   type StrictRecord @table @sealed {
   	id: Long @primaryKey
   	name: String
   }
   ```

#### Examples

**Minimal two-table schema:**

```graphql
type Dog @table {
	id: Long @primaryKey
	name: String
	breed: String
	age: Int
}

type Breed @table {
	id: Long @primaryKey
	name: String @indexed
}
```

**Table with expiration, eviction, and custom scan interval:**

```graphql
# Expire after 5 minutes, evict after 1 hour, scan every 10 minutes
type WeatherCache @table(expiration: 300, eviction: 3300, scanInterval: 600) {
	id: ID @primaryKey
	temperature: Float
}
```

**Exported table with timestamps and a hidden field:**

```graphql
type Customer @table @export(name: "customers") {
	id: Long @primaryKey
	name: String @indexed
	createdAt: Long @createdTime
	updatedAt: Long @updatedTime

	"""
	Internal — do not surface to external consumers.
	"""
	creditScore: Int @hidden
}
```

**Multiple `@table` argument combinations:**

```graphql
# Override table name
type Product @table(table: "products") {
	id: Long @primaryKey
}

# Place in a specific database
type Order @table(database: "commerce") {
	id: Long @primaryKey
}

# Auto-expire records after 1 hour
type Session @table(expiration: 3600) {
	id: Long @primaryKey
	userId: String
}

# Disable replication
type LocalRecord @table(replicate: false) {
	id: Long @primaryKey
	value: String
}

# Combine multiple arguments
type Event @table(database: "analytics", expiration: 86400) {
	id: Long @primaryKey
	name: String @indexed
}
```

#### Notes

- All tables default to the `"data"` database. When designing plugins or applications, use unique database names to avoid table naming collisions.
- Schemas are flexible by default — records may include properties beyond those declared. Use `@sealed` to prevent this.
- `expiration` marks a record stale; `eviction` controls how long after expiration the record is physically removed. Eviction does not remove records from secondary indexes — Harper fetches the full record on demand if an evicted record matches a query.
- `scanInterval` is clock-aligned to the server's local timezone, not startup-aligned. The eviction schedule is deterministic across restarts.
- If replication is disabled on a table and later re-enabled, writes made during the disabled period are not replicated retroactively.
- `@hidden` (on types or fields) is a metadata-visibility directive only. Use `attribute_permissions` on roles to enforce data access control.
- Disabling replication (`replicate: false`) and re-enabling it later will not catch up on writes made while replication was disabled.

### 1.3 Defining Relationships Between Tables in Harper

Instructions for the agent to follow when defining and querying relationships between tables in Harper using the `@relationship` directive.

#### When to Use

Apply this rule whenever a schema requires linking two tables via a foreign key — for example, modeling shows and networks, products and brands, or orders and items. Use it when queries need to filter or select nested related records using dot-syntax.

#### How It Works

1. **Use `@relationship(from: attribute)` for many-to-one or many-to-many**: Place this on a field in the current table when the foreign key lives in this table and references the primary key of the target table.

   ```graphql
   type RealityShow @table @export {
   	id: Long @primaryKey
   	networkId: Long @indexed
   	network: Network @relationship(from: networkId)
   	title: String @indexed
   }

   type Network @table @export {
   	id: Long @primaryKey
   	name: String @indexed
   }
   ```

   For a many-to-many relationship, make the foreign key an array:

   ```graphql
   type RealityShow @table @export {
   	id: Long @primaryKey
   	networkIds: [Long] @indexed
   	networks: [Network] @relationship(from: networkIds)
   }
   ```

2. **Use `@relationship(to: attribute)` for one-to-many or many-to-many**: Place this on a field in the current table when the foreign key lives in the target table and references the primary key of this table. The result type must be an array.

   ```graphql
   type Network @table @export {
   	id: Long @primaryKey
   	name: String @indexed
   	shows: [RealityShow] @relationship(to: networkId)
   }
   ```

3. **Use `@relationship(from: attribute, to: attribute)` for foreign key to foreign key joins**: Specify both `from` and `to` when neither side uses the primary key. This is useful for joining on non-primary-key attributes.

   ```graphql
   type OrderItem @table @export {
   	id: Long @primaryKey
   	orderId: Long @indexed
   	productSku: Long @indexed
   	product: Product @relationship(from: productSku, to: sku)
   }

   type Product @table @export {
   	id: Long @primaryKey
   	sku: Long @indexed
   	name: String
   }
   ```

4. **Query across relationships using dot-syntax**: Filter by related table attributes using chained dot notation. This behaves as an INNER JOIN.

   ```
   GET /RealityShow?network.name=Bravo
   GET /Product/?brand.name=Microsoft
   GET /Brand/?products.name=Keyboard
   ```

5. **Select nested relationship fields with `select()`**: Relationship attributes are not included by default. Use `select()` to include them in results. When selecting without a filter on the related table, this acts as a LEFT JOIN — the relationship property is omitted if the foreign key is null or references a non-existent record.

   ```
   GET /Product/?brand.name=Microsoft&select(name,brand)
   GET /Product/?brand.name=Microsoft&select(name,brand{name})
   GET /Product/?name=Keyboard&select(name,brand{name,id})
   ```

#### Examples

**Many-to-one relationship** — a show belongs to a network:

```graphql
type RealityShow @table @export {
	id: Long @primaryKey
	networkId: Long @indexed
	network: Network @relationship(from: networkId)
	title: String @indexed
}

type Network @table @export {
	id: Long @primaryKey
	name: String @indexed
}
```

Query:

```
GET /RealityShow?network.name=Bravo
```

**One-to-many relationship** — a network has many shows:

```graphql
type Network @table @export {
	id: Long @primaryKey
	name: String @indexed
	shows: [RealityShow] @relationship(to: networkId)
}
```

**Many-to-many with array foreign keys** — a product has multiple resellers:

```graphql
type Product @table @export {
	id: Long @primaryKey
	name: String
	resellerIds: [Long] @indexed
	resellers: [Reseller] @relationship(from: resellerIds)
}
```

Query with nested select:

```
GET /Product/?resellers.name=Cool Shop&select(id,name,resellers{name,id})
```

**Foreign key to foreign key join** — order item joined on SKU:

```graphql
type OrderItem @table @export {
	id: Long @primaryKey
	orderId: Long @indexed
	productSku: Long @indexed
	product: Product @relationship(from: productSku, to: sku)
}

type Product @table @export {
	id: Long @primaryKey
	sku: Long @indexed
	name: String
}
```

#### Notes

- The `@relationship` directive requires the referenced attribute to be `@indexed` on the foreign key side.
- Self-referential relationships are supported, enabling parent-child hierarchies within a single table.
- The array order of foreign key values (e.g., `resellerIds`) is preserved when resolving many-to-many relationships.
- When using `select()` without a filter on the related table, the join behaves as a LEFT JOIN — missing or null foreign keys result in the relationship property being omitted rather than causing an error.

### 1.4 Vector Indexing

Instructions for the agent to enable HNSW vector indexes on table fields and query them for similarity search in Harper.

#### When to Use

Apply this rule when adding a vector similarity search capability to a Harper table — for example, storing text embeddings and querying for nearest neighbors, filtering by distance threshold, or tuning index construction and search parameters. Use it alongside [adding-tables-with-schemas.md](adding-tables-with-schemas.md) when defining the schema that hosts the vector field.

#### How It Works

1. **Declare the vector index on a field**: Add `@indexed(type: "HNSW")` to a `[Float]` field inside a `@table` type. This creates an HNSW (Hierarchical Navigable Small World) index for approximate nearest-neighbor search.

   ```graphql
   type Document @table {
   	id: Long @primaryKey
   	textEmbeddings: [Float] @indexed(type: "HNSW")
   }
   ```

2. **Query by nearest neighbors using `sort`**: Call `.search()` with a `sort` descriptor that specifies the indexed `attribute` and a `target` vector. Use `limit` to cap results.

   ```javascript
   let results = Document.search({
   	sort: { attribute: 'textEmbeddings', target: searchVector },
   	limit: 5,
   });
   ```

3. **Combine with filter conditions**: Add a `conditions` array alongside `sort` to pre-filter records before ranking by similarity.

   ```javascript
   let results = Document.search({
   	conditions: [{ attribute: 'price', comparator: 'lt', value: 50 }],
   	sort: { attribute: 'textEmbeddings', target: searchVector },
   	limit: 5,
   });
   ```

4. **Filter by distance threshold**: To return only records within a similarity cutoff (without ranking), place `target` directly on the condition alongside `comparator` and `value`. This bounds result quality rather than ranking by similarity.

   ```javascript
   let results = Document.search({
   	conditions: {
   		attribute: 'textEmbeddings',
   		comparator: 'lt',
   		value: 0.1,
   		target: searchVector,
   	},
   });
   ```

5. **Include computed distance in results**: Use the special `$distance` field in `select` to return the distance from the target vector. Available in both `sort`-based and threshold-based queries.

   ```javascript
   let results = Document.search({
   	select: ['name', '$distance'],
   	sort: { attribute: 'textEmbeddings', target: searchVector },
   	limit: 5,
   });
   ```

6. **Tune per-query search options**: Pass `distance` and `ef` directly on the `sort` descriptor to override index defaults for a single query.

   ```javascript
   let results = Document.search({
   	sort: { attribute: 'textEmbeddings', target: searchVector, distance: 'dotProduct', ef: 200 },
   	limit: 5,
   });
   ```

   - `distance` — overrides the distance function for this query: `"cosine"`, `"euclidean"`, or `"dotProduct"`.
   - `ef` — overrides the search exploration budget. Higher values improve recall at the cost of latency.

7. **Configure HNSW index parameters**: Pass parameters directly in the `@indexed` directive. Structural parameters (`distance`, `M`, `efConstruction`, `quantization`) trigger an index rebuild when changed; `efConstructionSearch` does not.

   ```graphql
   type Document @table {
   	id: Long @primaryKey
   	textEmbeddings: [Float]
   		@indexed(type: "HNSW", distance: "euclidean", optimizeRouting: 0, efConstructionSearch: 100)
   }
   ```

8. **Enable vector quantization**: Use `quantization: "int8"` to store vectors as 8-bit integers, reducing index size and memory usage. Harper re-ranks nearest-neighbor `sort` results against full-precision vectors automatically.

   ```graphql
   type Document @table {
   	id: Long @primaryKey
   	textEmbeddings: [Float] @indexed(type: "HNSW", quantization: "int8")
   }
   ```

#### Examples

Full schema with custom HNSW parameters and a nearest-neighbor query with distance output:

```graphql
type Document @table {
	id: Long @primaryKey
	textEmbeddings: [Float]
		@indexed(type: "HNSW", distance: "euclidean", optimizeRouting: 0, efConstructionSearch: 100)
}
```

```javascript
// Nearest-neighbor search with distance scores
let results = Document.search({
	select: ['name', '$distance'],
	sort: { attribute: 'textEmbeddings', target: searchVector },
	limit: 5,
});

// Distance-threshold query (no ranking)
let closeMatches = Document.search({
	conditions: {
		attribute: 'textEmbeddings',
		comparator: 'lt',
		value: 0.1,
		target: searchVector,
	},
});
```

#### Notes

##### HNSW Parameters

| Parameter              | Default           | Description                                                                                            |
| ---------------------- | ----------------- | ------------------------------------------------------------------------------------------------------ |
| `distance`             | `"cosine"`        | Distance function: `"cosine"`, `"euclidean"`, or `"dotProduct"`                                        |
| `efConstruction`       | `100`             | Max nodes explored during index construction. Higher = better recall, lower = better performance       |
| `M`                    | `16`              | Preferred connections per graph layer. Higher = more space, better recall for high-dimensional data    |
| `optimizeRouting`      | `0.5`             | Heuristic aggressiveness for omitting redundant connections (0 = off, 1 = most aggressive)             |
| `mL`                   | computed from `M` | Normalization factor for level generation                                                              |
| `efConstructionSearch` | auto-scaled       | Max nodes explored during search. When unset, auto-scales with index size; setting it fixes the budget |
| `quantization`         | —                 | `"int8"` stores vectors quantized to int8                                                              |

- The `distance` option on a per-query `sort` descriptor accepts `"cosine"`, `"euclidean"`, or `"dotProduct"`.
- When no `ef` is passed and `efConstructionSearch` (or `efConstruction`) is not explicitly set on the index, the search budget auto-scales with index size.
- `efConstruction` seeds the initial value of `efConstructionSearch`; setting either one fixes the search budget.
- The correct parameter name is `efConstructionSearch` (not `efSearchConstruction`).
- `$distance` is available in both `sort`-based ranking and `conditions`-based threshold queries.
- For `quantization: "int8"`, distance-threshold (`lt`/`le`) queries filter on approximate distance; `sort` queries re-rank against full-precision vectors.

### 1.5 Using the Blob Data Type

Instructions for the agent to follow when storing and retrieving large binary content using Harper's `Blob` data type.

#### When to Use

Apply this rule when a schema field needs to store large binary content such as images, video, audio, or large HTML — typically content larger than 20KB. Use `Blob` instead of `Bytes` when you need streaming support or want to avoid loading the entire value into memory. See [handling-binary-data.md](handling-binary-data.md) for broader binary data guidance.

#### How It Works

1. **Declare a `Blob` field in your schema**: Add a field typed as `Blob` to a `@table` type.

   ```graphql
   type MyTable @table {
   	id: Any! @primaryKey
   	data: Blob
   }
   ```

2. **Create a blob with `createBlob()`**: Pass a buffer, string, or stream as the first argument. Pass a `BlobOptions` object as the second argument to configure behavior.

   ```javascript
   let blob = createBlob(largeBuffer);
   await MyTable.put({ id: 'my-record', data: blob });
   ```

3. **Read blob data using standard Web API methods**: The `Blob` type implements the Web API `Blob` interface. Use `.bytes()`, `.text()`, `.arrayBuffer()`, `.stream()`, or `.slice()` to access content.

   ```javascript
   let record = await MyTable.get('my-record');
   let buffer = await record.data.bytes(); // ArrayBuffer
   let text = await record.data.text(); // string
   let stream = record.data.stream(); // ReadableStream
   ```

4. **Use `saveBeforeCommit` for ACID-compliant writes**: By default, blobs are not ACID-compliant — a record can reference a blob before it is fully written. Set `saveBeforeCommit: true` to wait for the full write before the transaction commits.

   ```javascript
   let blob = createBlob(stream, { saveBeforeCommit: true });
   await MyTable.put({ id: 'my-record', data: blob });
   // put() resolves only after blob is fully written and record is committed
   ```

5. **Register an error handler when returning a blob via REST**: Interrupted streams must be handled explicitly to avoid stale records.

   ```javascript
   export class MyEndpoint extends MyTable {
   	static async get(target) {
   		const record = super.get(target);
   		let blob = record.data;
   		blob.on('error', () => {
   			MyTable.invalidate(target);
   		});
   		return { status: 200, headers: {}, body: blob };
   	}
   }
   ```

6. **Rely on automatic coercion where applicable**: When a field is typed as `Blob` in the schema, any string or buffer assigned via `put`, `patch`, or `publish` is automatically coerced to a `Blob`. Manual `createBlob()` calls are not required for plain JSON HTTP bodies or MQTT messages in most cases.

##### `BlobOptions` Reference

| Option             | Type      | Default     | Description                                                                                                              |
| ------------------ | --------- | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| `type`             | `string`  | `undefined` | MIME type to associate with the blob (e.g., `image/jpeg`). Readable via `blob.type` and used when serving HTTP.          |
| `size`             | `number`  | `undefined` | Size of the data in bytes, if known ahead of time. Otherwise inferred from a buffer or determined as a stream completes. |
| `saveBeforeCommit` | `boolean` | `false`     | Wait for the blob to be fully written before committing the transaction.                                                 |
| `compress`         | `boolean` | `false`     | Compress the stored data with deflate.                                                                                   |
| `flush`            | `boolean` | `false`     | Flush the file to disk after writing, before the `createBlob` promise chain resolves.                                    |

#### Examples

**Store an image with a MIME type:**

```javascript
let blob = createBlob(imageBuffer, { type: 'image/jpeg' });
await Photo.put({ id, data: blob });
```

**Stream large media with low latency:**

```javascript
let blob = createBlob(incomingStream);
// blob exists, but data is still streaming to storage
await MyTable.put({ id: 'my-record', data: blob });

let record = await MyTable.get('my-record');
// blob data is accessible as it arrives
let outgoingStream = record.data.stream();
```

**Guaranteed write before commit:**

```javascript
let blob = createBlob(stream, { saveBeforeCommit: true });
await MyTable.put({ id: 'my-record', data: blob });
```

#### Notes

- `Blob` stores data separately from the record; `Bytes` does not. Prefer `Blob` for content larger than 20KB.
- All standard Web API `Blob` methods are available: `.bytes()`, `.text()`, `.arrayBuffer()`, `.stream()`, `.slice()`.
- Blobs are **not** ACID-compliant by default when created from a stream. Use `saveBeforeCommit: true` to enforce transactional consistency.
- Always attach an `error` handler on blobs returned as HTTP response bodies to handle interrupted streams.

### 1.6 Handling Binary Data

Instructions for the agent to follow when storing and serving binary data (images, audio, arbitrary content types) in Harper.

#### When to Use

Apply this rule when a Harper resource needs to accept, store, or serve binary payloads such as images, audio files, or calendar data. Use it when REST clients send `base64`-encoded data inside JSON, when raw binary is uploaded via `PUT`/`POST`, or when a resource must stream binary back to the client with the correct `Content-Type`.

#### How It Works

1. **Accept base64-encoded binary from JSON clients**: Decode the incoming `base64` string with `Buffer.from` and wrap it using `createBlob`, recording the MIME type. Override `post` in your resource class:

   ```typescript
   import { type RequestTargetOrId, tables, createBlob } from 'harper';

   export class Photo extends tables.Photo {
   	static async post(target: RequestTargetOrId, record: any) {
   		if (record.data) {
   			record.data = createBlob(Buffer.from(record.data, record.encoding || 'base64'), {
   				type: record.contentType || 'application/octet-stream',
   			});
   		}
   		return super.post(target, record);
   	}
   }
   ```

2. **Serve binary from a resource**: Override `get` to return a response object with the blob's MIME type in the `Content-Type` header and the blob as the body. Harper streams it to the client:

   ```typescript
   export class Photo extends tables.Photo {
   	static async get(target: RequestTargetOrId) {
   		const record = await super.get(target);
   		if (record?.data) {
   			return {
   				status: 200,
   				headers: { 'Content-Type': record.data.type || 'application/octet-stream' },
   				body: record.data,
   			};
   		}
   		return record;
   	}
   }
   ```

3. **Upload raw binary with a non-standard content type**: Make a `PUT` or `POST` with any non-standard `Content-Type` header. Harper automatically stores the body as a record with `contentType` and `data` properties:

   ```http
   PUT /my-resource/33
   Content-Type: text/calendar

   BEGIN:VCALENDAR
   VERSION:2.0
   ...
   ```

   Harper stores this as:

   ```json
   { "contentType": "text/calendar", "data": "BEGIN:VCALENDAR\nVERSION:2.0\n..." }
   ```

   Retrieving that record returns the response with the stored `Content-Type` and body. If the content type is not from the `text` family, the data is treated as binary (a Node.js `Buffer`).

4. **Upload binary to a specific property**: Use `application/octet-stream` (or any image/binary MIME type) and target a sub-path to store binary directly on a property:

   ```http
   PUT /my-resource/33/image
   Content-Type: image/gif

   ...image data...
   ```

#### Examples

**End-to-end: accept base64 JSON, store as blob, serve as binary**

```typescript
import { type RequestTargetOrId, tables, createBlob } from 'harper';

export class Photo extends tables.Photo {
	// Accept base64-encoded uploads in JSON
	static async post(target: RequestTargetOrId, record: any) {
		if (record.data) {
			record.data = createBlob(Buffer.from(record.data, record.encoding || 'base64'), {
				type: record.contentType || 'application/octet-stream',
			});
		}
		return super.post(target, record);
	}

	// Stream the blob back with the correct Content-Type
	static async get(target: RequestTargetOrId) {
		const record = await super.get(target);
		if (record?.data) {
			return {
				status: 200,
				headers: { 'Content-Type': record.data.type || 'application/octet-stream' },
				body: record.data,
			};
		}
		return record;
	}
}
```

#### Notes

- `createBlob` takes a `Buffer` as its first argument and an options object with a `type` property for the MIME type. See [using-blob-datatype.md](using-blob-datatype.md) for full details on the blob data type.
- Always fall back to `application/octet-stream` when no MIME type is known, both when creating and when serving blobs.
- When Harper retrieves a record that has both `contentType` and `data` properties, it automatically sets the response `Content-Type` and body — no custom `get` override is required for that case unless you need additional logic.
- Non-`text` content types cause `data` to be stored and returned as a Node.js `Buffer`.

## 2. API & Communication

### 2.1 Automatic APIs

Instructions for the agent to follow when enabling and using Harper's automatically generated REST and WebSocket APIs.

#### When to Use

Apply this rule when adding REST or WebSocket API access to Harper tables or custom resources. Use it when configuring `config.yaml` to expose endpoints, mapping HTTP methods to resource operations, or implementing real-time WebSocket connections on a resource class.

#### How It Works

1. **Enable the REST plugin**: Add `rest: true` to your application's `config.yaml`. This activates the HTTP REST interface and enables WebSocket support by default.

   ```yaml
   rest: true
   ```

   To configure optional behavior:

   ```yaml
   rest:
     lastModified: true # enables Last-Modified response header support
     webSocket: false # disables automatic WebSocket support (enabled by default)
   ```

2. **Export your resource in the schema**: Tables are not exposed by default. Use the `@export` directive in your schema definition to make a table available as a REST endpoint. The exported name defines the base URL path, served on the application HTTP server port (default `9926`).

3. **Use the correct URL structure**: The REST interface follows a consistent path convention.

   | Path                                         | Description                                                                        |
   | -------------------------------------------- | ---------------------------------------------------------------------------------- |
   | `/my-resource`                               | Returns a description of the resource (e.g., table metadata)                       |
   | `/my-resource/`                              | Trailing slash — represents the full collection; append query parameters to search |
   | `/my-resource/record-id`                     | A specific record identified by its primary key                                    |
   | `/my-resource/record-id/`                    | Trailing slash — collection of records with the given id prefix                    |
   | `/my-resource/record-id/with/multiple/parts` | Record id with multiple path segments                                              |

4. **Map HTTP methods to operations**: Each HTTP method maps to a resource method and operation.
   - **GET** — Retrieve a record or search. Calls `get()`.

     ```
     GET /MyTable/123
     GET /MyTable/?name=Harper
     GET /MyTable/123.propertyName
     ```

     Responses include an `ETag` header. Clients may send `If-None-Match` to receive `304 Not Modified` when the record is unchanged.

   - **PUT** — Create or replace a record (upsert). Calls `put(record)`. Properties not in the body are removed.

     ```
     PUT /MyTable/123
     Content-Type: application/json

     { "name": "some data" }
     ```

   - **POST** — Create a new record without specifying a primary key. Calls `post(data)`. The assigned key is returned in the `Location` response header.

     ```
     POST /MyTable/
     Content-Type: application/json

     { "name": "some data" }
     ```

   - **PATCH** — Partially update a record, merging only provided properties. Unspecified properties are preserved.

     ```
     PATCH /MyTable/123
     Content-Type: application/json

     { "status": "active" }
     ```

   - **DELETE** — Delete a record or all records matching a query.
     ```
     DELETE /MyTable/123
     DELETE /MyTable/?status=archived
     ```

5. **Access the auto-generated OpenAPI spec**: Harper generates an OpenAPI specification for all exported resources. Retrieve it at:

   ```
   GET /openapi
   ```

6. **Connect via WebSocket**: When `rest` is enabled, WebSocket support is on by default. Connect to a resource URL to subscribe to change events for that resource.

   ```javascript
   let ws = new WebSocket('wss://server/my-resource/341');
   ws.onmessage = (event) => {
   	let data = JSON.parse(event.data);
   };
   ```

   Connecting to `wss://server/my-resource/341` accesses the `my-resource` resource with record id `341` and subscribes to it. When the record changes or a message is published to it, the WebSocket connection receives the update.

7. **Implement a custom `connect()` handler**: Override `connect(incomingMessages)` on a resource class to control WebSocket behavior. The method must return an async iterable or generator that produces messages to send to the client.

#### Examples

**Simple echo server using an async generator**:

```javascript
export class Echo extends Resource {
	async *connect(incomingMessages) {
		for await (let message of incomingMessages) {
			yield message; // echo each message back
		}
	}
}
```

**Using the default `connect()` with event-style access and a timer**:

```javascript
export class Example extends Resource {
	connect(incomingMessages) {
		let outgoingMessages = super.connect();

		let timer = setInterval(() => {
			outgoingMessages.send({ greeting: 'hi again!' });
		}, 1000);

		incomingMessages.on('data', (message) => {
			outgoingMessages.send(message); // echo incoming messages
		});

		outgoingMessages.on('close', () => {
			clearInterval(timer);
		});

		return outgoingMessages;
	}
}
```

**Minimal `config.yaml` enabling REST with WebSocket disabled**:

```yaml
rest:
  webSocket: false
```

#### Notes

- Tables must be explicitly exported using `@export` in the schema — they are not exposed by default.
- `rest: true` is the minimal configuration to enable both REST and WebSocket support. See [real-time-apps.md](real-time-apps.md) for patterns around real-time WebSocket usage.
- For full query syntax on `GET` and `DELETE` with query parameters, see [querying-rest-apis.md](querying-rest-apis.md).
- The default `connect()` returns an iterable with a `send(message)` method and a `close` event for cleanup on disconnect.
- For MQTT over WebSockets, set the sub-protocol header `Sec-WebSocket-Protocol: mqtt`.
- In distributed environments, non-retained messages are delivered in the order received per node; retained messages (PUT/updated records) keep only the latest-timestamp version as the winning record across the cluster.
- Use the `Content-Type` request header to specify body format and the `Accept` header to request a specific response format.

### 2.2 Querying REST APIs

Instructions for the agent to filter, sort, select, and paginate Harper REST API collections using URL query parameters.

#### When to Use

Apply this rule when building or modifying code that queries Harper REST endpoints with filtering, sorting, field selection, or pagination. Use it whenever constructing URLs against collection paths exposed by Harper's automatic REST interface (see [automatic-apis.md](automatic-apis.md)).

#### How It Works

1. **Filter by attribute**: Add query parameters matching attribute names and values. The queried attribute must be indexed.

   ```
   GET /Product/?category=software
   GET /Product/?category=software&inStock=true
   ```

2. **Apply comparison operators (FIQL syntax)**: Use FIQL operators directly in query parameter values.

   | Operator     | Meaning                                |
   | ------------ | -------------------------------------- |
   | `==`         | Equal                                  |
   | `=lt=`       | Less than                              |
   | `=le=`       | Less than or equal                     |
   | `=gt=`       | Greater than                           |
   | `=ge=`       | Greater than or equal                  |
   | `=ne=`, `!=` | Not equal                              |
   | `=ct=`       | Contains (strings)                     |
   | `=sw=`       | Starts with (strings)                  |
   | `=ew=`       | Ends with (strings)                    |
   | `=`, `===`   | Strict equality (no type conversion)   |
   | `!==`        | Strict inequality (no type conversion) |

   ```
   GET /Product/?price=gt=100
   GET /Product/?price=le=20
   GET /Product/?name==Keyboard*
   GET /Product/?category=software&price=gt=100&price=lt=200
   ```

   For date fields, URL-encode colons as `%3A`:

   ```
   GET /Product/?listDate=gt=2017-03-08T09%3A30%3A00.000Z
   ```

3. **Chain conditions for range queries**: Omit the attribute name on the second condition to apply it to the same attribute. Only `gt`/`ge` combined with `lt`/`le` is supported.

   ```
   GET /Product/?price=gt=100&lt=200
   ```

4. **Combine conditions with OR logic**: Use `|` instead of `&`.

   ```
   GET /Product/?rating=5|featured=true
   ```

5. **Group conditions**: Use parentheses or square brackets to control order of operations. Prefer square brackets when constructing queries from user input, since standard URI encoding safely encodes `[` and `]`.

   ```
   GET /Product/?rating=5|(price=gt=100&price=lt=200)
   GET /Product/?rating=5&[tag=fast|tag=scalable|tag=efficient]
   ```

   Construct grouped queries from JavaScript:

   ```javascript
   let url = `/Product/?rating=5&[${tags.map(encodeURIComponent).join('|')}]`;
   ```

6. **Select specific properties with `select(`**: Use `select()` to control which fields are returned.

   | Syntax                                 | Returns                                     |
   | -------------------------------------- | ------------------------------------------- |
   | `?select(property)`                    | Values of a single property directly        |
   | `?select(property1,property2)`         | Objects with only the specified properties  |
   | `?select([property1,property2])`       | Arrays of property values                   |
   | `?select(property1,)`                  | Objects with a single specified property    |
   | `?select(property{subProp1,subProp2})` | Nested objects with specific sub-properties |

   ```
   GET /Product/?category=software&select(name)
   GET /Product/?brand.name=Microsoft&select(name,brand{name})
   ```

7. **Limit results with `limit(`**: Use `limit(end)` or `limit(start,end)` to paginate.

   ```
   GET /Product/?rating=gt=3&inStock=true&select(rating,name)&limit(20)
   GET /Product/?rating=gt=3&limit(10,30)
   ```

8. **Sort results with `sort(`**: Use `sort(property)` or `sort(+property,-property,...)`. Prefix `+` or no prefix = ascending; `-` = descending.

   ```
   GET /Product/?rating=gt=3&sort(+name)
   GET /Product/?sort(+rating,-price)
   ```

9. **Query across relationships**: Use dot-syntax to filter by related table attributes. Relationships must be defined in the schema using `@relation`.

   ```
   GET /Product/?brand.name=Microsoft
   GET /Brand/?products.name=Keyboard
   ```

   Use `select()` to include relationship attributes in the response (they are not included by default):

   ```
   GET /Product/?brand.name=Microsoft&select(name,brand{name})
   ```

10. **Access a specific property by URL**: Append the property name with dot syntax to the record ID. Only works for properties declared in the schema.
    ```
    GET /MyTable/123.propertyName
    ```

#### Examples

**Range filter with select and limit:**

```
GET /Product/?category=software&price=gt=100&price=lt=200&select(name,price)&limit(20)
```

**Sort descending with multiple fields:**

```
GET /Product/?sort(+rating,-price)
```

**OR logic with grouping:**

```
GET /Product/?price=lt=100|[rating=5&[tag=fast|tag=scalable|tag=efficient]&inStock=true]
```

**Relationship join with nested select:**

```
GET /Product/?brand.name=Microsoft&select(name,brand{name,id})
```

**Schema defining a relationship for join queries:**

```graphql
type Product @table @export {
	id: Long @primaryKey
	name: String
	brandId: Long @indexed
	brand: Brand @relation(from: "brandId")
}
type Brand @table @export {
	id: Long @primaryKey
	name: String
	products: [Product] @relation(to: "brandId")
}
```

**Many-to-many relationship query:**

```graphql
type Product @table @export {
	id: Long @primaryKey
	name: String
	resellerIds: [Long] @indexed
	resellers: [Reseller] @relation(from: "resellerId")
}
```

```
GET /Product/?resellers.name=Cool Shop&select(id,name,resellers{name,id})
```

**Type conversion with explicit prefix:**

```
GET /Product/?price==number:123
GET /Product/?active==boolean:true
GET /Product/?listDate==date:2024-01-05T20%3A07%3A27.955Z
```

#### Notes

- Only indexed attributes can be used as the primary filter; additional unindexed attributes can be combined with `&` once at least one indexed attribute is present.
- For null value queries, use `?attribute=null`. Indexes must have been created with null indexing support; existing indexes must be removed and re-added to support null queries.
- FIQL comparators (`==`, `!=`, `=gt=`, etc.) apply automatic type conversion based on value syntax or schema-declared type. Strict operators (`=`, `===`, `!==`) skip automatic type conversion.
- Filtering by a related attribute produces INNER JOIN behavior (only records with a matching related record are returned). Using `select()` on a relationship without a filter produces LEFT JOIN behavior.
- The array order of foreign key values in many-to-many relationships is preserved when resolving the relationship.
- See [automatic-apis.md](automatic-apis.md) for how Harper tables are automatically exposed as REST endpoints.

### 2.3 Real-Time Apps with WebSockets and Pub/Sub

Instructions for the agent to follow when building real-time features in Harper using WebSockets and Pub/Sub.

#### When to Use

Apply this rule when implementing any feature that requires real-time bidirectional communication, live data streaming, or push-based updates in a Harper application. This includes chat, live dashboards, sensor feeds, and any scenario where clients must receive resource changes as they happen.

#### How It Works

1. **Enable WebSocket support**: WebSocket support is enabled automatically when the `rest` plugin is enabled. To explicitly disable it, set the following in your config:

   ```yaml
   rest:
     webSocket: false
   ```

2. **Connect a client to a resource**: A WebSocket connection to a resource URL automatically subscribes to that resource. When the record changes or a message is published to it, the connection receives the update.

   ```javascript
   let ws = new WebSocket('wss://server/my-resource/341');
   ws.onmessage = (event) => {
   	let data = JSON.parse(event.data);
   };
   ```

   `new WebSocket('wss://server/my-resource/341')` accesses the resource defined for `my-resource` with record id `341` and subscribes to it.

3. **Implement a custom `connect()` handler**: Override the `connect(incomingMessages)` method on a resource class to control WebSocket behavior. The method must return an async iterable (or generator) that produces messages to send to the client. See [automatic-apis.md](automatic-apis.md) for more on defining resource classes.

4. **Use the default `connect()` for event-style access**: Call `super.connect()` to get a streaming iterable that provides:
   - A `send(message)` method for pushing outgoing messages
   - A `close` event for cleanup on disconnect

5. **Handle message ordering in distributed environments**: Harper delivers messages to local subscribers immediately without inter-node coordination delay.

   | Message Type                                             | Behavior                                                                |
   | -------------------------------------------------------- | ----------------------------------------------------------------------- |
   | Non-retained (no `retain` flag)                          | Every message delivered in order received; suitable for chat            |
   | Retained (published with `retain`, or PUT/updated in DB) | Only the latest-timestamp message is kept; suitable for sensor readings |

6. **Use MQTT over WebSockets** when needed by setting the sub-protocol header:
   ```
   Sec-WebSocket-Protocol: mqtt
   ```

#### Examples

**Simple echo server** — override `connect(incomingMessages)` to yield each incoming message back to the client:

```javascript
export class Echo extends Resource {
	async *connect(incomingMessages) {
		for await (let message of incomingMessages) {
			yield message; // echo each message back
		}
	}
}
```

**Custom connect with timer and event-style access** — use `super.connect()` to get the outgoing stream, push periodic messages, echo incoming messages, and clean up on disconnect:

```javascript
export class Example extends Resource {
	connect(incomingMessages) {
		let outgoingMessages = super.connect();

		let timer = setInterval(() => {
			outgoingMessages.send({ greeting: 'hi again!' });
		}, 1000);

		incomingMessages.on('data', (message) => {
			outgoingMessages.send(message); // echo incoming messages
		});

		outgoingMessages.on('close', () => {
			clearInterval(timer);
		});

		return outgoingMessages;
	}
}
```

#### Notes

- WebSocket connections target a resource URL path. By default, connecting to a resource subscribes to changes for that resource.
- The `connect(incomingMessages)` method **must** return an async iterable or generator; returning a plain value will not work.
- `super.connect()` returns a streaming iterable with `send(message)` and a `close` event — use this when you need to push messages outside of the incoming message loop.
- For one-way real-time streaming without bidirectional communication, consider Server-Sent Events instead.
- For full pub/sub capabilities, Harper also supports MQTT; set `Sec-WebSocket-Protocol: mqtt` to use MQTT over WebSockets.

### 2.4 Checking Authentication

Instructions for the agent to follow when handling user authentication and session management inside Harper Resources.

#### When to Use

Apply this rule when implementing authentication checks, login/logout flows, or token issuance inside a custom Resource. Use it any time a Resource needs to identify the current user, establish a session, or issue JWTs to clients. See [custom-resources.md](custom-resources.md) for the general Resource authoring pattern.

#### How It Works

1. **Check the current user** with `getCurrentUser()`. Call it inside any Resource method to retrieve the authenticated user or `undefined` if no user is authenticated. Guard protected endpoints by returning a `401` when the result is `undefined`.

   ```javascript
   async get(target) {
     const user = this.getCurrentUser();
     if (!user) return new Response(null, { status: 401 });
     return { username: user.username, role: user.role };
   }
   ```

   The returned object exposes `username`, `role`, and `role.permission` flags.

2. **Enable sessions** before using session-based login. Set `authentication.enableSessions: true` in `harperdb-config.yaml`:

   ```yaml
   authentication:
     enableSessions: true
   ```

3. **Access login and session helpers** via `getContext()`. The context object exposes `context.login` and `context.session` for sign-in/out flows.
   - Call `context.login(username, password)` to verify credentials and establish a session cookie on success.
   - To end a session, delete it via `context.session.delete(context.session.id)`.

4. **Implement sign-in and sign-out Resources** using the context helpers:

   ```javascript
   export class SignIn extends Resource {
   	async post(_target, data) {
   		const context = this.getContext();
   		try {
   			await context.login(data.username, data.password);
   		} catch {
   			return new Response('Invalid credentials', { status: 403 });
   		}
   		return new Response('Logged in', { status: 200 });
   	}
   }

   export class SignOut extends Resource {
   	async post() {
   		const context = this.getContext();
   		if (!context.session) return new Response(null, { status: 401 });
   		await context.session.delete(context.session.id);
   		return new Response('Logged out', { status: 200 });
   	}
   }
   ```

5. **Issue JWTs for non-browser clients** (CLI tools, mobile apps, service-to-service). Cookie-based sessions are intended for browser clients. For other clients, mint tokens programmatically using `server.operation()`:

   ```javascript
   import { Resource, server } from 'harper';

   export class IssueTokens extends Resource {
   	static async get(_target, context) {
   		const { operation_token, refresh_token } = await server.operation(
   			{ operation: 'create_authentication_tokens' },
   			context,
   			true,
   		);
   		return { operation_token, refresh_token };
   	}

   	static async post(_target, data) {
   		const { username, password } = await data;
   		if (!username || !password) {
   			return new Response('username and password required', { status: 400 });
   		}
   		const { operation_token, refresh_token } = await server.operation({
   			operation: 'create_authentication_tokens',
   			username,
   			password,
   		});
   		return { operation_token, refresh_token };
   	}
   }

   export class RefreshJWT extends Resource {
   	static async post(_target, data) {
   		const { refresh_token } = await data;
   		if (!refresh_token) {
   			return new Response('refresh_token required', { status: 400 });
   		}
   		const { operation_token } = await server.operation({
   			operation: 'refresh_operation_token',
   			refresh_token,
   		});
   		return { operation_token };
   	}
   }
   ```

   Pass `true` as the third argument to `server.operation()` when the operation should run as the current authenticated user. Omit it or pass `false` when the operation supplies its own credentials.

6. **Configure JWT token expiry** in `harperdb-config.yaml` under the `authentication` section:

   ```yaml
   authentication:
     operationTokenTimeout: 1d
     refreshTokenTimeout: 30d
   ```

   Duration strings follow the `jsonwebtoken` package format (e.g., `1d`, `12h`, `60m`).

#### Examples

**Protecting a resource endpoint and returning user info:**

```javascript
async get(target) {
  const user = this.getCurrentUser();
  if (!user) return new Response(null, { status: 401 });
  return { username: user.username, role: user.role };
}
```

**Full session-based sign-in/sign-out flow:**

```javascript
export class SignIn extends Resource {
	async post(_target, data) {
		const context = this.getContext();
		try {
			await context.login(data.username, data.password);
		} catch {
			return new Response('Invalid credentials', { status: 403 });
		}
		return new Response('Logged in', { status: 200 });
	}
}

export class SignOut extends Resource {
	async post() {
		const context = this.getContext();
		if (!context.session) return new Response(null, { status: 401 });
		await context.session.delete(context.session.id);
		return new Response('Logged out', { status: 200 });
	}
}
```

**JWT token refresh endpoint:**

```javascript
export class RefreshJWT extends Resource {
	static async post(_target, data) {
		const { refresh_token } = await data;
		if (!refresh_token) {
			return new Response('refresh_token required', { status: 400 });
		}
		const { operation_token } = await server.operation({
			operation: 'refresh_operation_token',
			refresh_token,
		});
		return { operation_token };
	}
}
```

#### Notes

- `getCurrentUser()` and `getContext()` are instance methods; call them with `this` inside non-static Resource methods.
- `enableSessions` must be `true` in config before `context.login` or `context.session` will function.
- Cookie-based sessions target browser clients. Use JWT issuance via `server.operation()` for all other client types.
- When both `operation_token` and `refresh_token` have expired, the client must call `create_authentication_tokens` again with credentials.

## 3. Logic & Extension

### 3.1 Custom Resources

Instructions for the agent to follow when defining custom REST endpoints with JavaScript or TypeScript in Harper.

#### When to Use

Apply this rule when creating custom HTTP endpoints, wrapping external APIs, or registering programmatic routes in a Harper application. Use it any time business logic needs to live outside a standard table-backed resource.

#### How It Works

1. **Import `Resource` from the `harper` package**: Always import explicitly rather than relying on globals.

   ```javascript
   import { tables, Resource } from 'harper';
   ```

2. **Define a class that `extends Resource`**: Use `export class` so Harper can expose it as an endpoint. Implement HTTP methods as `static` methods on the class.

   ```javascript
   export class CustomEndpoint extends Resource {
   	static get(target) {
   		return {
   			data: doSomething(),
   		};
   	}
   }
   ```

3. **Add async `static` methods for each HTTP verb you need**: Methods receive `target` (contains `target.id`, etc.) and, for write operations, `data`.

   ```javascript
   export class MyExternalData extends Resource {
   	static async get(target) {
   		const response = await fetch(`https://api.example.com/${target.id}`);
   		return response.json();
   	}

   	static async put(target, data) {
   		return fetch(`https://api.example.com/${target.id}`, {
   			method: 'PUT',
   			body: JSON.stringify(await data),
   		});
   	}
   }
   ```

4. **Control the URL by choosing the export form**: The shape of the export determines the resulting URL path. Path matching is case-sensitive.

   | Export form                              | URL             | Notes                                                           |
   | ---------------------------------------- | --------------- | --------------------------------------------------------------- |
   | `export class Foo extends Resource {}`   | `/Foo/`         | Class name becomes the path segment.                            |
   | `export const Bar = { Foo };`            | `/Bar/Foo/`     | Nest under an object to add a path prefix.                      |
   | `export const bar = { 'foo-baz': Foo };` | `/bar/foo-baz/` | Use object keys for lowercase, hyphens, or non-identifier URLs. |
   | `server.resources.set('my-path', Foo);`  | `/my-path/`     | Programmatic registration; useful when the path is dynamic.     |

5. **Register programmatically when the path is dynamic**: Use `server.resources.set(` with a path string and the class.

   ```javascript
   server.resources.set('my-path', Foo);
   ```

6. **Optionally use the resource as a cache source for a local table**: Pass the class to `sourcedFrom`.
   ```javascript
   tables.MyCache.sourcedFrom(MyExternalData);
   ```

#### Examples

Wrap an external API and expose it as an endpoint, then back a local cache table with it:

```javascript
import { tables, Resource } from 'harper';

export class MyExternalData extends Resource {
	static async get(target) {
		const response = await fetch(`https://api.example.com/${target.id}`);
		return response.json();
	}

	static async put(target, data) {
		return fetch(`https://api.example.com/${target.id}`, {
			method: 'PUT',
			body: JSON.stringify(await data),
		});
	}
}

// Use as a cache source for a local table
tables.MyCache.sourcedFrom(MyExternalData);
```

Programmatic registration with a custom path:

```javascript
import { Resource } from 'harper';

export class CustomEndpoint extends Resource {
	static get(target) {
		return {
			data: doSomething(),
		};
	}
}

server.resources.set('my-path', CustomEndpoint);
```

#### Notes

- `export class` directly produces a URL from the class name (e.g., `export class Foo extends Resource {}` → `/Foo/`). Do not export the same resource from both a schema file and a JavaScript file — this creates conflicting exports.
- URL path segments are case-sensitive: `/Foo/` and `/foo/` are different endpoints.
- For CommonJS modules, use `const { tables, Resource } = require('harper');` instead of the ESM import.
- When developing a component in its own directory, run `npm link harper` to ensure typings match your installed version. All installed components have `harper` automatically linked.
- The `static` keyword is required on all HTTP verb methods — Harper dispatches requests through static class methods, not instance methods.

### 3.2 Extending Tables

Instructions for the agent to follow when adding custom logic to automatically generated table resources in Harper.

#### When to Use

Apply this rule when you need to add computed properties, intercept writes, enforce validation, or otherwise customize the behavior of a Harper table resource beyond what the default generated endpoints provide. Use it any time a `@table` type needs server-side logic attached to its REST handlers.

#### How It Works

1. **Define the schema without `@export`**: Declare the table type in `schema.graphql` and omit the `@export` directive. Leaving `@export` on the schema while also exporting a subclass with the same name produces conflicting endpoints. Let the JavaScript class own the URL instead.

   ```graphql
   # Omit the `@export` directive
   type MyTable @table {
   	id: Long @primaryKey
   	# ...
   }
   ```

2. **Extend the generated table class**: In `resources.js`, extend from the `tables.<TypeName>` global. The class name you export becomes the URL path. The exported class extends tables.

   ```javascript
   export class MyTable extends tables.MyTable {
   	static async get(target) {
   		const record = await super.get(target);
   		return { ...record, computedField: 'value' };
   	}

   	static async post(target, data) {
   		this.create({ ...(await data), status: 'pending' });
   	}
   }
   ```

3. **Call `super` to preserve default behavior**: When delegating to `super`, match the argument form to the operation:
   - Reads/deletes: `super.get(target)` / `super.delete(target)`
   - Collection create: `super.post(target, record)` — target carries no id
   - Updates: `super.put(target, data)` / `super.patch(target, data)`

   Omit the `super` call only if you intend to replace the default behavior entirely.

4. **Set `statusCode` on thrown errors to control HTTP responses**: Uncaught errors are caught by the protocol handler and produce error responses for REST. Use `.statusCode` — a plain `.status` property is ignored.

   ```javascript
   const error = new Error('Name is required');
   error.statusCode = 400; // use statusCode, NOT status
   throw error;
   ```

5. **Configure Harper to load both files**: Ensure your configuration references the schema and resource files.

   ```yaml
   rest: true
   graphqlSchema:
     files: schema.graphql
   jsResource:
     files: resources.js
   ```

#### Examples

Full end-to-end example — schema, resource class, and error handling:

```graphql
# schema.graphql — omit @export so the JS class owns the endpoint
type MyTable @table {
	id: Long @primaryKey
}
```

```javascript
// resources.js
export class MyTable extends tables.MyTable {
	static async get(target) {
		// get the record from the database
		const record = await super.get(target);
		// add a computed property before returning
		return { ...record, computedField: 'value' };
	}

	static async post(target, data) {
		// custom action on POST
		this.create({ ...(await data), status: 'pending' });
	}
}
```

Throwing a controlled HTTP error:

```javascript
if (!authorized) {
	const error = new Error('Forbidden');
	error.statusCode = 403;
	throw error;
}
```

#### Notes

- Always omit `@export` from the schema type when a JavaScript subclass is exporting the same name. The two registrations conflict.
- `super` must be called with the correct arguments for each operation type — mismatched arguments will not behave as expected.
- `statusCode` is the only recognized property for controlling HTTP status on thrown errors; `.status` is ignored.

### 3.3 Programmatic Table Requests

Instructions for the agent to interact with Harper tables programmatically using the `tables` object and its query API.

#### When to Use

Apply this rule when writing server-side Harper code that reads from or writes to tables directly — for example, in request handlers, background jobs, or SSR entry points — instead of going through the REST API. Use it whenever you need to construct queries with `conditions`, paginate results, select specific fields, or perform CRDT-safe mutations with `addTo`.

#### How It Works

1. **Import `tables`**: Import from the `harper` package. Each table defined in `schema.graphql` with `@table` is available as a named property.

   ```javascript
   import { tables } from 'harper';
   const { Product } = tables;
   // same as: databases.data.Product
   ```

2. **Define your schema**: Declare tables in `schema.graphql` using `@table` and `@primaryKey`.

   ```graphql
   # schema.graphql
   type Product @table {
   	id: Long @primaryKey
   	name: String
   	price: Float
   }
   ```

3. **Create and mutate records**: Use `create`, `patch`, `get`, and `update` on the table class.

   ```javascript
   // Create a new record (id auto-generated)
   const created = await Product.create({ name: 'Shirt', price: 9.5 });

   // Modify the record
   await Product.patch(created.id, { price: Math.round(created.price * 0.8 * 100) / 100 });

   // Retrieve by primary key
   const record = await Product.get(created.id);
   ```

4. **Query with `search(` and `conditions`**: Pass a query object to `search()` to filter records. Iterate the async result.

   ```javascript
   const query = {
   	conditions: [{ attribute: 'price', comparator: 'less_than', value: 8.0 }],
   };
   for await (const record of Product.search(query)) {
   	// ...
   }
   ```

5. **Use `select` to shape results**: Pass a `select` array to return only specific properties, including nested relationship fields.

   ```javascript
   const book = await Book.get({ id: 42, select: ['id', 'title', 'author'] });
   book.author.name; // full related Author record

   // Partial related record
   const book = await Book.get({
   	id: 42,
   	select: ['id', 'title', { name: 'author', select: ['name'] }],
   });
   ```

6. **Use `addTo` for concurrent-safe increments**: Call `addTo` on a mutable resource instance obtained via `update()`. This uses CRDT incrementation, safe across threads and nodes.

   ```javascript
   static async post(target, data) {
     const record = await this.update(target.id);
     record.addTo('quantity', -1); // decrement safely across nodes
   }
   ```

7. **Scope destructive operations carefully**: `update`, `patch`, and `delete` operate directly on stored data. Always use specific `conditions`, validate the affected set before writing, and gate behind authorization controls.

#### Examples

##### Nested conditions query

```javascript
Product.search({
	conditions: [
		{ attribute: 'price', comparator: 'less_than', value: 100 },
		{
			operator: 'or',
			conditions: [
				{ attribute: 'rating', comparator: 'greater_than', value: 4 },
				{ attribute: 'featured', value: true },
			],
		},
	],
});
```

##### Chained attribute reference (relationship join)

```javascript
Product.search({ conditions: [{ attribute: ['brand', 'name'], value: 'Harper' }] });
```

##### Deep nested `select`

```javascript
select: [
	'id',
	'name',
	{ name: 'segments', select: ['id', 'name', { name: 'client', select: ['id', 'name'] }] },
];
```

##### SSR usage

```typescript
import { tables } from 'harper';

export async function render(url: string): Promise<string> {
	const product = await tables.Product.get(idFromUrl(url));
	return renderToString(/* <App product={product} /> */);
}
```

#### Notes

##### `conditions` comparator values

| Comparator           | Description            |
| -------------------- | ---------------------- |
| `equals`             | Default equality match |
| `greater_than`       | Strictly greater       |
| `greater_than_equal` | Greater than or equal  |
| `less_than`          | Strictly less          |
| `less_than_equal`    | Less than or equal     |
| `starts_with`        | String prefix match    |
| `contains`           | String contains        |
| `ends_with`          | String suffix match    |
| `between`            | Range match            |
| `not_equal`          | Inequality match       |

##### Query object options

| Property                | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `conditions`            | Array of condition objects to filter records                            |
| `operator`              | Top-level `and` (default) or `or` for the `conditions` array            |
| `limit`                 | Maximum number of records to return                                     |
| `offset`                | Number of records to skip (for pagination)                              |
| `select`                | Properties to include in each returned record                           |
| `sort`                  | Sort order object with `attribute`, `descending`, and `next` properties |
| `explain`               | If `true`, returns conditions reordered as Harper will execute them     |
| `enforceExecutionOrder` | If `true`, forces conditions to execute in the order supplied           |

##### `select` special properties

- `$id` — Returns the primary key regardless of its name
- `$updatedtime` — Returns the last-updated timestamp
- `$distance` — Returns the computed distance from the target vector when the query uses a vector index

##### Relationship join behavior

- Selecting a relationship **without** filtering on it behaves as a **LEFT JOIN** — records with no related row are still returned.
- Adding a `conditions` entry on a related attribute (e.g. `attribute: ['author', 'name']`) behaves as an **INNER JOIN** — only records with a matching related row are returned.

- Keep `harper` external when bundling for SSR (e.g. `ssr: { external: ['harper'] }` in `vite.config`) so it resolves to the runtime instead of being bundled.
- `tables`, `databases`, and other Harper APIs are the same live, process-wide objects regardless of whether accessed as globals or via `import { tables } from 'harper'`.

### 3.4 TypeScript Type Stripping in Harper

Instructions for the agent to run `.ts` files directly in Harper without a build step using Node.js's built-in type stripping.

#### When to Use

Apply this rule when writing Harper resource files in TypeScript. Use it any time you need to reference `.ts` source files from `config.yaml` or import between local TypeScript modules in a Harper project.

#### How It Works

1. **Ensure Node.js version**: Require Node.js 22.6 or later. Type stripping is unavailable on earlier versions.

2. **Point `jsResource` at `.ts` files**: The `jsResource` plugin loads both `.js` and `.ts` files. Set its `files` glob in `config.yaml` to target your `.ts` source files:

   ```yaml
   jsResource:
     files: 'resources/*.ts'
   ```

3. **Use explicit `.ts` extensions in local imports**: Node's loader does not resolve `'./helper'` to `'./helper.ts'`, so always include the full extension:

   ```typescript
   import { helper } from './helper.ts';
   ```

4. **Stay within type-stripping limits**: Only type annotations and declarations are removed. Do not use enums with runtime values, namespaces with runtime semantics, or any other features that require code transformation beyond type stripping.

#### Examples

A complete Harper resource written in TypeScript, using imports from the `harper` package:

```typescript
import { type RequestTargetOrId, Resource, tables } from 'harper';

export class MyResource extends Resource {
	async get(target?: RequestTargetOrId): Promise<{ message: string }> {
		return { message: 'Hello from TS' };
	}
}
```

Paired `config.yaml` entry loading the file via `jsResource`:

```yaml
jsResource:
  files: 'resources/*.ts'
```

#### Notes

- No build step or transpiler is required — Harper runs `.ts` files directly.
- Type imports (e.g., `import { type RequestTargetOrId }`) from the `harper` package work as usual.
- Unsupported TypeScript features include: enums with runtime values, namespaces with runtime semantics, and anything requiring code transformation beyond simple type stripping.

### 3.5 Caching External Data Sources in Harper

Instructions for the agent to implement integrated data caching from external sources using Harper's cache table directives and `sourcedFrom` API.

#### When to Use

Apply this rule when an application needs to wrap an external API, microservice, or database with a fast local cache. Use it when you need to define TTL-based cache expiration, connect an upstream data source to a Harper table, or implement on-demand cache invalidation.

#### How It Works

1. **Define a cache table with `expiration`**: Add the `expiration` argument to the `@table` directive in `schema.graphql`. The value is in seconds. When a record becomes stale, the next request fetches a fresh copy from the upstream source.

   ```graphql
   type JokeCache @table(expiration: 60) @export {
   	id: ID @primaryKey
   	setup: String
   	punchline: String
   }
   ```

2. **Implement an upstream source object**: In `resources.js`, create an object with a `get(id)` method that fetches data from the external API.

   ```javascript
   const jokeAPI = {
   	async get(id) {
   		const response = await fetch(`https://official-joke-api.appspot.com/jokes/${id}`);
   		return response.json();
   	},
   };
   ```

3. **Connect the source with `sourcedFrom`**: Call `sourcedFrom` on the table to register the upstream source. Harper will call `jokeAPI.get()` automatically when a record is missing or stale.

   ```javascript
   tables.JokeCache.sourcedFrom(jokeAPI);
   ```

   Harper's request flow after `sourcedFrom` is registered:
   - Request arrives for `/JokeCache/1`.
   - Harper checks if the record exists and is not stale.
   - If fresh, Harper returns it immediately.
   - If missing or stale, Harper calls `jokeAPI.get()`, stores the result in `JokeCache`, and returns it.
   - Multiple simultaneous requests for the same missing or stale record wait on a single upstream call — Harper prevents cache stampedes automatically.

4. **Configure plugins in `config.yaml`**: Enable `graphqlSchema`, `rest`, and `jsResource`.

   ```yaml
   graphqlSchema:
     files: 'schema.graphql'
   rest: true
   jsResource:
     files: 'resources.js'
   ```

5. **Implement on-demand invalidation**: To invalidate a cache entry before its TTL expires, export a class extending the table and call `this.invalidate(target)` in a `post` handler. Remove `@export` from the schema when using this pattern — the exported class provides the endpoint.

   ```javascript
   export class JokeCache extends tables.JokeCache {
   	static async post(target, data) {
   		const body = await data;
   		if (body?.action === 'invalidate') {
   			this.invalidate(target);
   			return { status: 200, data: { message: 'invalidated' } };
   		}
   	}
   }
   ```

   Update the schema to remove `@export`:

   ```graphql
   type JokeCache @table(expiration: 60) {
   	id: ID @primaryKey
   	setup: String
   	punchline: String
   }
   ```

#### Examples

**Complete `resources.js`**:

```javascript
// resources.js

const jokeAPI = {
	async get(id) {
		const response = await fetch(`https://official-joke-api.appspot.com/jokes/${id}`);
		return response.json();
	},
};

tables.JokeCache.sourcedFrom(jokeAPI);

export class JokeCache extends tables.JokeCache {
	static async post(target, data) {
		const body = await data;
		if (body?.action === 'invalidate') {
			this.invalidate(target);
			return { status: 200, data: { message: 'invalidated' } };
		}
	}
}
```

**Complete `schema.graphql`**:

```graphql
type JokeCache @table(expiration: 60) {
	id: ID @primaryKey
	setup: String
	punchline: String
}
```

**Fetch a cached record**:

```javascript
const response = await fetch('http://localhost:9926/JokeCache/1');
console.log(response.status); // 200
const etag = response.headers.get('etag'); // e.g. "abCDefGHij"
const joke = await response.json();
```

**Use ETag for conditional requests** (returns `304 Not Modified` if unchanged):

```javascript
const second = await fetch('http://localhost:9926/JokeCache/1', {
	headers: { 'If-None-Match': etag },
});
console.log(second.status); // 304
```

**Bypass the cache with `Cache-Control: no-cache`**:

```javascript
const response = await fetch('http://localhost:9926/JokeCache/1', {
	headers: { 'Cache-Control': 'no-cache' },
});
```

**Trigger invalidation via POST**:

```javascript
await fetch('http://localhost:9926/JokeCache/1', {
	method: 'POST',
	headers: { 'Content-Type': 'application/json' },
	body: JSON.stringify({ action: 'invalidate' }),
});
```

#### Notes

- `expiration` is measured in seconds. Harper also supports separate `eviction` and `scanInterval` arguments on `@table` for fine-grained control over physical record removal.
- ETags are automatically computed from a record's last-modified timestamp. Include the double quotes when passing an ETag back in `If-None-Match` — they are part of the value.
- Exporting a class with the same name as a table (e.g., `export class JokeCache extends tables.JokeCache`) registers it as the HTTP endpoint for that table; `@export` in the schema is not required separately.
- For defining custom upstream source behavior beyond a simple `get`, see [custom-resources.md](custom-resources.md).
- For details on how `@table` and `@export` expose REST endpoints automatically, see [automatic-apis.md](automatic-apis.md).

## 4. Infrastructure & Ops

### 4.1 Deploying to Harper Fabric

Instructions for the agent to follow when deploying a Harper application to the Harper Fabric cloud using the Harper CLI.

#### When to Use

Apply this rule when deploying a Harper application to a remote Harper instance or Harper Fabric cluster. This covers interactive deployments, CI/CD pipelines, and any scenario where the agent must push a local or remote package to a target environment.

#### How It Works

1. **Authenticate with the remote target**: Run `harper login` once to store an authentication token. The CLI writes `HARPER_CLI_TARGET` to a local `.env` so subsequent commands do not need credentials repeated. Find the **Application URL** on the cluster's **Config → Overview** page (see [creating-a-fabric-account-and-cluster.md](creating-a-fabric-account-and-cluster.md)).

   ```bash
   harper login <Application URL>
   # Provide cluster username and password when prompted
   ```

2. **Deploy the application**: Run `harper deploy` with the required parameters. After logging in, no credentials are needed inline.

   ```bash
   harper deploy \
     project=<name> \
     package=<package> \
     target=<remote> \
     restart=true \
     replicated=true
   ```

3. **Choose a package source**: Set the `package` parameter to any valid npm dependency value, or omit it to package and deploy the current local directory.

   | Value                                                | Effect                                           |
   | ---------------------------------------------------- | ------------------------------------------------ |
   | _(omitted)_                                          | Packages and deploys the current local directory |
   | `"@harperdb/status-check"`                           | npm package                                      |
   | `"HarperDB/status-check"`                            | GitHub repo (short form)                         |
   | `"https://github.com/HarperDB/status-check"`         | GitHub repo (full URL)                           |
   | `"git+ssh://git@github.com:HarperDB/secret-app.git"` | Private repo via SSH                             |
   | `"https://example.com/application.tar.gz"`           | Remote tarball                                   |

   For git tags, use the `semver` directive for reliable versioning:

   ```
   HarperDB/application-template#semver:v1.0.0
   ```

4. **Authenticate for CI/CD pipelines**: Use environment variables instead of interactive login. Set credentials before running `harper deploy`.

   ```bash
   export HARPER_CLI_USERNAME=<username>
   export HARPER_CLI_PASSWORD=<password>
   harper deploy \
     project=<name> \
     package=<package> \
     target=<remote> \
     restart=true \
     replicated=true
   ```

5. **Register SSH keys for private repos**: Before deploying from an SSH-based private repository, use the Add SSH Key operation to register the key with the remote instance.

#### Examples

**Interactive login then deploy (recommended):**

```bash
# Log in once
harper login <remote>
# Provide your username and password when prompted

# Subsequently deploy without credentials
harper deploy \
  project=<name> \
  package=<package> \
  target=<remote> \
  restart=true \
  replicated=true
```

**Deploy with inline credentials (not recommended for production):**

```bash
harper deploy \
  project=<name> \
  package=<package> \
  username=<username> \
  password=<password> \
  target=<remote> \
  restart=true \
  replicated=true
```

**Deploy a specific GitHub release by semver tag:**

```bash
harper deploy \
  project=my-app \
  package="HarperDB/application-template#semver:v1.0.0" \
  target=<remote> \
  restart=true \
  replicated=true
```

#### Notes

- Always prefer `harper login` for interactive use and environment variables (`HARPER_CLI_USERNAME`, `HARPER_CLI_PASSWORD`) for CI/CD. Avoid inline `username`/`password` parameters in production.
- Omitting `package` causes the CLI to package the current local directory. Specifying a local file path creates a symlink, so changes are picked up between restarts without redeploying.
- Harper generates a `package.json` from component configurations and resolves dependencies using a form of `npm install`.
- For SSH-based private repos, register keys with the Add SSH Key operation before deploying.

### 4.2 Creating a Harper Fabric Account and Cluster

Follow these steps to set up your Harper Fabric environment for deployment.

#### How It Works

1. **Sign Up/In**: Go to [https://fabric.harper.fast/](https://fabric.harper.fast/) and sign up or sign in.
2. **Create an Organization**: Create an organization (org) to manage your projects.
3. **Create a Cluster**: Create a new cluster. This can be on the free tier, no credit card required.
4. **Set Credentials**: During setup, set the cluster username and password to finish configuring it.
5. **Get Application URL**: Navigate to the **Config** tab and copy the **Application URL**.
6. **Configure Environment**: Update your `.env` file or GitHub Actions secrets with cluster-specific credentials.
7. **Next Steps**: See the [deploying-to-harper-fabric](deploying-to-harper-fabric.md) rule for detailed instructions on deploying your application successfully.

#### Examples

##### Environment Configuration

```bash
CLI_TARGET_USERNAME='YOUR_CLUSTER_USERNAME'
CLI_TARGET_PASSWORD='YOUR_CLUSTER_PASSWORD'
CLI_TARGET='YOUR_CLUSTER_URL'
```

### 4.3 Creating Harper Applications

The fastest way to start a new Harper project is using the `create-harper` CLI tool. This command
initializes a project with a standard folder structure, essential configuration files, and basic
schema definitions.

#### When to Use

Use this command when starting a new Harper application or adding a new Harper microservice to an
existing architecture.

#### Commands

Initialize a project using your preferred package manager:

##### NPM

```bash
npm create harper@latest
```

##### PNPM

```bash
pnpm create harper@latest
```

##### Bun

```bash
bun create harper@latest
```

#### Options

You can specify the project name and template directly:

```bash
npm create harper@latest my-app --template default
```

#### Next Steps

1. **Configure Environment**: Set up your `.env` file with local or cloud credentials.
2. **Define Schema**: Modify `schema.graphql` to fit your application's data model.
3. **Start Development**: Run `npm run dev` to start the local Harper instance.
4. **Deploy**: Use `npm run deploy` to push your application to Harper Fabric.

### 4.4 Serving Web Content

Instructions for the agent to follow when serving web content from Harper.

#### When to Use

Use this skill when you need to serve a frontend (HTML, CSS, JS, or a React/Vue app) directly from your Harper instance — either plain static files or an integrated Vite app with hot module replacement (HMR) in development and a real production build when deployed.

#### How It Works

There are two building blocks. Harper's built-in `static` plugin **serves** files; the `@harperfast/vite` plugin **builds** (and, for SSR, **renders**) a Vite app. For a Vite app they work **together** — the plugin builds into a directory and `static` serves that same directory.

##### Option A: Static plugin only (simple, pre-built assets)

For a plain static site or already-built assets, use `static` on its own:

```yaml
static:
  files: 'web/*'
```

- Place files in a `web/` folder in the project root; they are served from the root URL (e.g. `http://localhost:9926/index.html`).
- Static files are matched first; if none matches, Harper falls through to your resource and table APIs.

##### Option B: Vite plugin + static plugin (integrated Vite app)

> **Renamed in v1:** the plugin was previously `@harperfast/vite-plugin`. From `1.0.0` on it is **`@harperfast/vite`** (same key and `package`). It now pairs with the `static` plugin instead of building into `web/` itself.

`@harperfast/vite` **builds** your app — in `harper dev` it runs Vite in middleware mode with HMR; in `harper run` it runs `vite build` and rebuilds when watched files change (and renders HTML for SSR). The `static` plugin **serves** the built output. Point both at the same directory (`output`, default `dist`) — that shared directory is the only contract between them.

**SPA `config.yaml`** — list the plugin first so its dev server wins in `harper dev`; `notFound` + `fallthrough: false` makes client-side routing work:

```yaml
'@harperfast/vite':
  package: '@harperfast/vite'
  files: 'src/**/*'
  output: 'dist'

static:
  files: 'dist/**'
  notFound:
    file: 'index.html'
    statusCode: 200
  fallthrough: false
```

**SSR `config.yaml`** — add an `ssr` entry so the plugin renders `index.html`, and set `index: false` on `static` so it serves assets only:

```yaml
'@harperfast/vite':
  package: '@harperfast/vite'
  files: 'src/**/*'
  output: 'dist'
  ssr: 'src/entry-server.tsx'

static:
  files: 'dist/**'
  index: false
```

- Install dependencies: `npm install --save-dev vite @harperfast/vite @vitejs/plugin-react` (swap in your framework's Vite plugin, e.g. `@vitejs/plugin-vue`).
- Then `harper dev .` runs the app with HMR and `harper run .` runs the production build. Vite does _not_ need to be executed separately.

#### Reading Harper Data During SSR

The render entry (`src/entry-server.tsx`) runs **inside Harper**, so it can read straight from the database and render the data into the HTML — no client-side fetch/XHR. `tables` is the same live, process-wide registry available everywhere (see [Programmatic Table Requests](programmatic-table-requests.md)); import it and query a table in an async `render`:

```tsx
import { tables } from 'harper';

export async function render(url: string): Promise<string> {
	const product = await tables.Product.get(idFromUrl(url));
	return renderToString(
		<StrictMode>
			<App product={product} />
		</StrictMode>,
	);
}
```

Keep `harper` external in `vite.config.ts` so this import resolves to Harper's running runtime instead of being bundled. `node_modules/harper` is symlinked to the running install, and symlinked deps aren't reliably auto-externalized for SSR:

```typescript
export default defineConfig({
	ssr: { external: ['harper'] },
	// ...plugins, resolve, build
});
```

To hydrate on the client without re-fetching, embed the rendered data in the HTML (e.g. an inline `<script type="application/json">`) and read it back before hydration — so the page needs no XHR at all.

#### Deploying to Production

Because `@harperfast/vite` builds on the node and `static` serves the output, deploy the component as-is — no manual build-and-move step is needed:

```json
{
	"scripts": {
		"dev": "harper dev .",
		"start": "harper run .",
		"deploy": "harper deploy_component . restart=true replicated=true"
	}
}
```

On deploy the plugin runs `vite build` at startup (and rebuilds when `files` change) while `static` serves the result. If you prefer to build in CI, commit the build output, point `static` at it, and omit `files` so the plugin stays idle while `static` serves the prebuilt assets. Either way, `npm create harper@latest` scaffolds a working setup for you.

### 4.5 Harper Logging

Instructions for the agent to follow when implementing logging in Harper applications, including direct logger usage, tagged loggers, and console capture behavior.

#### When to Use

Apply this rule when writing any JavaScript component, plugin, or resource that needs to emit structured log entries, filter logs by component, or capture existing `console.log` output into Harper's log system. Use it whenever you need to understand log levels, log entry format, or the `logger` global API.

#### How It Works

1. **Use the `logger` global directly** — `logger` is available in all JavaScript components without any imports. Call the method matching the desired severity level:

   ```javascript
   logger.trace('detailed trace message');
   logger.debug('debug info', { someContext: 'value' });
   logger.info('informational message');
   logger.warn('potential issue');
   logger.error('error occurred', error);
   logger.fatal('fatal error');
   logger.notify('server is ready');
   ```

   Only entries at or above the configured `logging.level` (or `logging.external.level`) are written to `hdb.log`.

2. **Create a tagged logger with `withTag(`** — Call `logger.withTag(tag)` once per module or class to get a `TaggedLogger` scoped to that tag. This prefixes every log entry with the tag, making log output filterable by component.

   ```javascript
   const log = logger.withTag('my-resource');
   ```

   Because `TaggedLogger` methods for disabled levels are `null`, always use optional chaining (`?.`) when calling them:

   ```javascript
   log.debug?.('Fetching record', { id });
   log.warn?.('Record not found', { id });
   log.error?.('Failed to update record', err);
   ```

   `TaggedLogger` does not have a `withTag()` method.

3. **Understand the interface contracts** — `MainLogger` always has all methods defined:

   ```typescript
   interface MainLogger {
   	trace(...messages: any[]): void;
   	debug(...messages: any[]): void;
   	info(...messages: any[]): void;
   	warn(...messages: any[]): void;
   	error(...messages: any[]): void;
   	fatal(...messages: any[]): void;
   	notify(...messages: any[]): void;
   	withTag(tag: string): TaggedLogger;
   }
   ```

   `TaggedLogger` methods may be `null`:

   ```typescript
   interface TaggedLogger {
   	trace: ((...messages: any[]) => void) | null;
   	debug: ((...messages: any[]) => void) | null;
   	info: ((...messages: any[]) => void) | null;
   	warn: ((...messages: any[]) => void) | null;
   	error: ((...messages: any[]) => void) | null;
   	fatal: ((...messages: any[]) => void) | null;
   	notify: ((...messages: any[]) => void) | null;
   }
   ```

4. **Know the log levels** — From least to most severe:

   | Level    | Description                                                          |
   | -------- | -------------------------------------------------------------------- |
   | `trace`  | Highly detailed internal execution tracing.                          |
   | `debug`  | Diagnostic information useful during development.                    |
   | `info`   | General operational events.                                          |
   | `warn`   | Potential issues that don't prevent normal operation.                |
   | `error`  | Errors that affect specific operations.                              |
   | `fatal`  | Critical errors causing process termination.                         |
   | `notify` | Important operational milestones. Always logged regardless of level. |

   The default log level is `warn`. Setting a level includes that level and all more-severe levels.

5. **Enable console capture when porting existing code** — When `logging.console: true` is set, writes via `console.log`, `console.warn`, `console.error`, etc. are appended verbatim to `hdb.log`. Captured lines do **not** pass through `logger`'s level filter. Prefer `logger` directly in production code so that level filtering and tagging apply. Console capture is intended as a convenience for porting existing code and for debugging.

6. **Know where logs are written** — All standard log output goes to `<ROOTPATH>/log/hdb.log` (default: `~/hdb/log/hdb.log`). To also log to `stdout`/`stderr`, set `logging.stdStreams: true`.

#### Examples

##### Basic logging in a resource

```javascript
export class MyResource extends Resource {
	async get(id) {
		logger.debug('Fetching record', { id });
		const record = await super.get(id);
		if (!record) {
			logger.warn('Record not found', { id });
		}
		return record;
	}

	async put(record) {
		logger.info('Updating record', { id: record.id });
		try {
			return await super.put(record);
		} catch (err) {
			logger.error('Failed to update record', err);
			throw err;
		}
	}
}
```

##### Tagged logging with `withTag()`

```javascript
const log = logger.withTag('my-resource');

export class MyResource extends Resource {
	async get(id) {
		log.debug?.('Fetching record', { id });
		const record = await super.get(id);
		if (!record) {
			log.warn?.('Record not found', { id });
		}
		return record;
	}

	async put(record) {
		log.info?.('Updating record', { id: record.id });
		try {
			return await super.put(record);
		} catch (err) {
			log.error?.('Failed to update record', err);
			throw err;
		}
	}
}
```

Tagged entries appear in `hdb.log` with the tag in the header:

```
2023-03-09T14:25:05.269Z [info] [my-resource]: Updating record
```

#### Notes

- All log output is written to `<ROOTPATH>/log/hdb.log`. The `logger` global writes to this file at the configured `logging.external` level.
- Log entry format for `logger`: `<timestamp> [<level>] [<thread>/<id>]: <message>`
- Log entry format for `TaggedLogger`: `<timestamp> [<level>] [<tag>]: <message>`
- `console.log` output is only forwarded to `hdb.log` when `logging.console: true` is explicitly set; it is not forwarded by default.
- When logging to standard streams, run Harper in the foreground (`harper`, not `harper start`).
- `TaggedLogger` is bound to the configured log level at creation time — always use `?.` on its methods.

### 4.6 Load Environment Variables with loadEnv

Instructions for the agent to follow when loading environment variables from `.env` files into a Harper application using the `loadEnv` plugin.

#### When to Use

Apply this rule when a Harper application needs to load secrets or configuration values from `.env` files into `process.env` at startup. Use it whenever hardcoding values must be avoided and environment-specific configuration must be supplied to Harper components.

#### How It Works

1. **Declare `loadEnv` in `config.yaml`**: Add `loadEnv` as a top-level key. It is built into Harper and requires no installation.

   ```yaml
   loadEnv:
     files: '.env'
   ```

2. **Place `loadEnv` first**: Always list `loadEnv` before any other components in `config.yaml` so that environment variables are available on `process.env` before dependent components start.

   ```yaml
   # config.yaml — loadEnv must come first
   loadEnv:
     files: '.env'

   rest: true

   myApp:
     files: './src/*.js'
   ```

3. **Configure the `files` option**: Provide one or more paths or glob patterns pointing to the env files to load. This option is required.

4. **Set `override` if needed**: By default, existing environment variables take precedence over values in `.env` files. Set `override: true` to reverse this and have loaded values win.

   ```yaml
   loadEnv:
     files: '.env'
     override: true
   ```

5. **Load multiple files when required**: Supply a list of files or a glob pattern. Files are loaded in the order specified.
   ```yaml
   loadEnv:
     files:
       - '.env'
       - '.env.local'
   ```
   or
   ```yaml
   loadEnv:
     files: 'env-vars/*'
   ```

##### Configuration Options

| Option     | Type                 | Required | Description                                                                            |
| ---------- | -------------------- | -------- | -------------------------------------------------------------------------------------- |
| `files`    | `string \| string[]` | **Yes**  | Path(s) or glob pattern(s) to the env file(s) to load.                                 |
| `override` | `boolean`            | No       | If `true`, loaded values override existing environment variables. Defaults to `false`. |

#### Examples

**Minimal setup — single `.env` file:**

```yaml
loadEnv:
  files: '.env'
```

**Full `config.yaml` with load order, multiple files, and override:**

```yaml
# config.yaml — loadEnv must come first
loadEnv:
  files:
    - '.env'
    - '.env.local'
  override: true

rest: true

myApp:
  files: './src/*.js'
```

**Glob pattern:**

```yaml
loadEnv:
  files: 'env-vars/*'
```

#### Notes

- `loadEnv` is built into Harper — do not install it separately; only declare it in `config.yaml`.
- Because Harper is a single-process application, variables loaded onto `process.env` are shared across all components.
- Without `override: true`, variables already set in the shell or container environment will not be overwritten by values in `.env` files.
- `files` is the only required option; omitting it will produce an invalid configuration.
