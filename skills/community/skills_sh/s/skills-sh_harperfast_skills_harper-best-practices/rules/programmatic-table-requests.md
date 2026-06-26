---
name: programmatic-table-requests
description: How to interact with Harper tables programmatically using the `tables` object.
metadata:
  mode: generate
  sources:
    - reference/v5/database/api.md#`tables`
    - reference/v5/resources/resource-api.md#Query Object
    - 'reference/v5/database/api.md#`transaction(context?, callback)`'
    - >-
      reference/v5/resources/resource-api.md#`update(target: RequestTarget | Id,
      updates?: object): Promise<Resource>`
    - >-
      reference/v5/resources/resource-api.md#`addTo(property: string, value:
      number)`
    - reference/v5/components/javascript-environment.md#Module Loading
  sourceCommit: be709f9978319dcdb669c05d794effc82bcda8b7
  inputHash: 3d2417fbff687c42
---

# Programmatic Table Requests

Instructions for the agent to interact with Harper tables programmatically using the `tables` object and its query API.

## When to Use

Apply this rule when writing server-side Harper code that reads from or writes to tables directly — for example, in request handlers, background jobs, or SSR entry points — instead of going through the REST API. Use it whenever you need to construct queries with `conditions`, paginate results, select specific fields, or perform CRDT-safe mutations with `addTo`.

## How It Works

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

## Examples

### Nested conditions query

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

### Chained attribute reference (relationship join)

```javascript
Product.search({ conditions: [{ attribute: ['brand', 'name'], value: 'Harper' }] });
```

### Deep nested `select`

```javascript
select: [
	'id',
	'name',
	{ name: 'segments', select: ['id', 'name', { name: 'client', select: ['id', 'name'] }] },
];
```

### SSR usage

```typescript
import { tables } from 'harper';

export async function render(url: string): Promise<string> {
	const product = await tables.Product.get(idFromUrl(url));
	return renderToString(/* <App product={product} /> */);
}
```

## Notes

### `conditions` comparator values

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

### Query object options

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

### `select` special properties

- `$id` — Returns the primary key regardless of its name
- `$updatedtime` — Returns the last-updated timestamp
- `$distance` — Returns the computed distance from the target vector when the query uses a vector index

### Relationship join behavior

- Selecting a relationship **without** filtering on it behaves as a **LEFT JOIN** — records with no related row are still returned.
- Adding a `conditions` entry on a related attribute (e.g. `attribute: ['author', 'name']`) behaves as an **INNER JOIN** — only records with a matching related row are returned.

- Keep `harper` external when bundling for SSR (e.g. `ssr: { external: ['harper'] }` in `vite.config`) so it resolves to the runtime instead of being bundled.
- `tables`, `databases`, and other Harper APIs are the same live, process-wide objects regardless of whether accessed as globals or via `import { tables } from 'harper'`.
