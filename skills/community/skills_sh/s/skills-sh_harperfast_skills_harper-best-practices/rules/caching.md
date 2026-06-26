---
name: caching
description: How to implement integrated data caching in Harper from external sources.
metadata:
  mode: generate
  sources:
    - learn/developers/caching-with-harper.md
  sourceCommit: 4fe4c9c95e0974eaa77032f6f10e36fbd8ec64ac
  inputHash: 60ad55fa37b5eec5
---

# Caching External Data Sources in Harper

Instructions for the agent to implement integrated data caching from external sources using Harper's cache table directives and `sourcedFrom` API.

## When to Use

Apply this rule when an application needs to wrap an external API, microservice, or database with a fast local cache. Use it when you need to define TTL-based cache expiration, connect an upstream data source to a Harper table, or implement on-demand cache invalidation.

## How It Works

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

## Examples

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

## Notes

- `expiration` is measured in seconds. Harper also supports separate `eviction` and `scanInterval` arguments on `@table` for fine-grained control over physical record removal.
- ETags are automatically computed from a record's last-modified timestamp. Include the double quotes when passing an ETag back in `If-None-Match` — they are part of the value.
- Exporting a class with the same name as a table (e.g., `export class JokeCache extends tables.JokeCache`) registers it as the HTTP endpoint for that table; `@export` in the schema is not required separately.
- For defining custom upstream source behavior beyond a simple `get`, see [custom-resources.md](custom-resources.md).
- For details on how `@table` and `@export` expose REST endpoints automatically, see [automatic-apis.md](automatic-apis.md).
