---
name: defining-relationships
description: How to define and use relationships between tables in Harper using GraphQL.
metadata:
  mode: generate
  sources:
    - reference/v5/database/schema.md#Relationships
    - reference/v5/rest/querying.md#Relationships and Joins
  sourceCommit: 4fe4c9c95e0974eaa77032f6f10e36fbd8ec64ac
  inputHash: 6953f507f0cde0f7
---

# Defining Relationships Between Tables in Harper

Instructions for the agent to follow when defining and querying relationships between tables in Harper using the `@relationship` directive.

## When to Use

Apply this rule whenever a schema requires linking two tables via a foreign key — for example, modeling shows and networks, products and brands, or orders and items. Use it when queries need to filter or select nested related records using dot-syntax.

## How It Works

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

## Examples

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

## Notes

- The `@relationship` directive requires the referenced attribute to be `@indexed` on the foreign key side.
- Self-referential relationships are supported, enabling parent-child hierarchies within a single table.
- The array order of foreign key values (e.g., `resellerIds`) is preserved when resolving many-to-many relationships.
- When using `select()` without a filter on the related table, the join behaves as a LEFT JOIN — missing or null foreign keys result in the relationship property being omitted rather than causing an error.
