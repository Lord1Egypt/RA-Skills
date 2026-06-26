---
name: using-blob-datatype
description: How to use the Blob data type for efficient binary storage in Harper.
metadata:
  mode: generate
  sources:
    - reference/v5/database/schema.md#Blob Type
    - reference/v5/database/api.md#Streaming
    - reference/v5/database/api.md#`BlobOptions`
    - reference/v5/database/api.md#Blob Coercion
  sourceCommit: 4fe4c9c95e0974eaa77032f6f10e36fbd8ec64ac
  inputHash: 71a3e738ebf87fa4
---

# Using the Blob Data Type

Instructions for the agent to follow when storing and retrieving large binary content using Harper's `Blob` data type.

## When to Use

Apply this rule when a schema field needs to store large binary content such as images, video, audio, or large HTML — typically content larger than 20KB. Use `Blob` instead of `Bytes` when you need streaming support or want to avoid loading the entire value into memory. See [handling-binary-data.md](handling-binary-data.md) for broader binary data guidance.

## How It Works

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

### `BlobOptions` Reference

| Option             | Type      | Default     | Description                                                                                                              |
| ------------------ | --------- | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| `type`             | `string`  | `undefined` | MIME type to associate with the blob (e.g., `image/jpeg`). Readable via `blob.type` and used when serving HTTP.          |
| `size`             | `number`  | `undefined` | Size of the data in bytes, if known ahead of time. Otherwise inferred from a buffer or determined as a stream completes. |
| `saveBeforeCommit` | `boolean` | `false`     | Wait for the blob to be fully written before committing the transaction.                                                 |
| `compress`         | `boolean` | `false`     | Compress the stored data with deflate.                                                                                   |
| `flush`            | `boolean` | `false`     | Flush the file to disk after writing, before the `createBlob` promise chain resolves.                                    |

## Examples

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

## Notes

- `Blob` stores data separately from the record; `Bytes` does not. Prefer `Blob` for content larger than 20KB.
- All standard Web API `Blob` methods are available: `.bytes()`, `.text()`, `.arrayBuffer()`, `.stream()`, `.slice()`.
- Blobs are **not** ACID-compliant by default when created from a stream. Use `saveBeforeCommit: true` to enforce transactional consistency.
- Always attach an `error` handler on blobs returned as HTTP response bodies to handle interrupted streams.
