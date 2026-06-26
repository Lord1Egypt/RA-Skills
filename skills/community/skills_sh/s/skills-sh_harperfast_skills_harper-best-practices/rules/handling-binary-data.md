---
name: handling-binary-data
description: How to store and serve binary data like images or audio in Harper.
metadata:
  mode: generate
  sources:
    - reference/v5/database/api.md#Accepting Binary in JSON Requests
    - reference/v5/database/api.md#Serving Binary from a Resource
    - reference/v5/rest/content-types.md#Storing Arbitrary Content Types
  sourceCommit: ce0ab713d918d789bc1c9f22e461e963ccc1dff1
  inputHash: fa06480e6fae7614
---

# Handling Binary Data

Instructions for the agent to follow when storing and serving binary data (images, audio, arbitrary content types) in Harper.

## When to Use

Apply this rule when a Harper resource needs to accept, store, or serve binary payloads such as images, audio files, or calendar data. Use it when REST clients send `base64`-encoded data inside JSON, when raw binary is uploaded via `PUT`/`POST`, or when a resource must stream binary back to the client with the correct `Content-Type`.

## How It Works

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

## Examples

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

## Notes

- `createBlob` takes a `Buffer` as its first argument and an options object with a `type` property for the MIME type. See [using-blob-datatype.md](using-blob-datatype.md) for full details on the blob data type.
- Always fall back to `application/octet-stream` when no MIME type is known, both when creating and when serving blobs.
- When Harper retrieves a record that has both `contentType` and `data` properties, it automatically sets the response `Content-Type` and body — no custom `get` override is required for that case unless you need additional logic.
- Non-`text` content types cause `data` to be stored and returned as a Node.js `Buffer`.
