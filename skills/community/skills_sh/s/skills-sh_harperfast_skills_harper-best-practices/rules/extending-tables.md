---
name: extending-tables
description: How to add custom logic to automatically generated table resources in Harper.
metadata:
  mode: generate
  sources:
    - reference/v5/resources/overview.md#Extending a Table
    - reference/v5/resources/resource-api.md#Throwing Errors
  sourceCommit: ce0ab713d918d789bc1c9f22e461e963ccc1dff1
  inputHash: 19738fbc732e0a1a
---

# Extending Tables

Instructions for the agent to follow when adding custom logic to automatically generated table resources in Harper.

## When to Use

Apply this rule when you need to add computed properties, intercept writes, enforce validation, or otherwise customize the behavior of a Harper table resource beyond what the default generated endpoints provide. Use it any time a `@table` type needs server-side logic attached to its REST handlers.

## How It Works

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

## Examples

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

## Notes

- Always omit `@export` from the schema type when a JavaScript subclass is exporting the same name. The two registrations conflict.
- `super` must be called with the correct arguments for each operation type — mismatched arguments will not behave as expected.
- `statusCode` is the only recognized property for controlling HTTP status on thrown errors; `.status` is ignored.
