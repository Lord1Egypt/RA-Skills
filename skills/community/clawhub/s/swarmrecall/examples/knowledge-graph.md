# Knowledge graph — entities, relations, traversal

Use the knowledge module to store structured information about people, projects, tools, and concepts, then traverse the graph to reason about connections.

## 1. Create entities

```bash
swarmrecall knowledge create --type person --name "Alice" \
  --props '{"role":"engineer","team":"ingest"}'

swarmrecall knowledge create --type project --name "Ingest Pipeline" \
  --props '{"status":"active","stack":["typescript","postgres"]}'
```

*(MCP: `knowledge_entity_create`.)*

## 2. Link them

The SDK and MCP both expose `knowledge_relation_create`. From the CLI, go through the SDK or use the MCP tool directly:

```ts
await client.knowledge.relations.create({
  fromEntityId: alice.id,
  toEntityId: ingest.id,
  relation: 'works_on',
  properties: { since: '2024-11-01' },
});
```

*(MCP: `knowledge_relation_create`.)*

## 3. Search

```bash
swarmrecall knowledge search "pipeline"
```

Returns entities ranked by semantic similarity.

*(MCP: `knowledge_search`.)*

## 4. Traverse

Walk the graph from a starting entity:

```bash
swarmrecall knowledge traverse --from <alice-id> --rel works_on --depth 2
```

Returns both entities visited and relations traversed.

*(MCP: `knowledge_traverse`.)*

## 5. Validate

After a batch of writes, sanity-check the graph:

```ts
const { valid, errors } = await client.knowledge.validate();
```

*(MCP: `knowledge_validate`.)*

## Typical reasoning loop

When the user asks "what do I know about X?":

1. `knowledge_search` with X — get top candidate entities.
2. `knowledge_entity_get` the top result — returns the entity plus its outgoing relations with pool context.
3. `knowledge_traverse` from the entity with `depth: 2` — surface related concepts.
4. Summarize the returned subgraph in natural language.

## Pools

Pass `poolId` to any create call to write into a shared pool. Pool members will see your writes in their `knowledge_search` and `knowledge_traverse` results scoped by their pool access level.
