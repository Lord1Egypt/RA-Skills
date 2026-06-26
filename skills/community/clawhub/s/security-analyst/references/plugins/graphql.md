---
name: GraphQL
detect:
  files: ["schema.graphql", "schema.gql"]
  dependencies: ["graphql", "apollo-server", "apollo-server-express", "apollo-server-core", "@apollo/server", "graphql-yoga", "mercurius", "graphql-go", "gqlgen", "strawberry-graphql", "ariadne", "type-graphql", "nexus"]
  keywords: ["GraphQL", "Apollo"]
---

## recon-agent

**GraphQL Discovery:**
1. Glob for `**/*.graphql`, `**/*.gql`, `**/schema.*`, `**/typeDefs*`, `**/resolvers*`
2. Grep for `typeDefs`, `makeExecutableSchema`, `buildSchema`, `type Query`, `type Mutation`
3. Check for GraphQL playground/explorer endpoints: `/graphql`, `/graphiql`, `/playground`, `/altair`
4. Identify the GraphQL server library (Apollo, Yoga, Mercurius, etc.)

## attack-surface-http

**GraphQL Endpoint Security:**
1. **Introspection in Production:**
   - Can the `__schema` or `__type` introspection query be executed in production?
   - Run: `curl -X POST -H "Content-Type: application/json" -d '{"query":"{ __schema { types { name } } }"}' <graphql-endpoint>`
   - If introspection is enabled: the entire API schema is exposed to attackers (all types, fields, mutations, subscriptions)
   - Check for `introspection: false` in server configuration
2. **Query Depth / Complexity Attacks:**
   - Is there a query depth limit? (without one, nested queries like `{ user { friends { friends { friends { ... } } } } }` cause exponential DB joins)
   - Is there a query complexity/cost analysis plugin? (`graphql-query-complexity`, `graphql-validation-complexity`)
   - Can an attacker construct a query that joins millions of records?
3. **Batching Abuse:**
   - Does the endpoint accept query batching? (array of operations in a single request: `[{query: "..."}, {query: "..."}]`)
   - Can an attacker bypass rate limiting by batching 1000 queries in a single HTTP request?
   - Is there a limit on the number of operations per batch?
4. **Alias-Based Attacks:**
   - Can field aliases be used to request the same expensive field multiple times?
   - `{ a: users { id } b: users { id } c: users { id } ... }` — is there a limit?
5. **Persisted Queries:**
   - Are persisted/allowlisted queries enforced? (only pre-approved queries can execute)
   - If automatic persisted queries (APQ) are used: can an attacker register arbitrary queries?
6. **Input Validation on Mutations:**
   - Are mutation arguments validated with custom scalars, input types, or directives?
   - Can an attacker send `null` for required fields? Overly long strings? Negative numbers?
   - Are file upload mutations (multipart requests) size-limited?

## attack-surface-authz

**GraphQL Authorization:**
1. **Field-Level Authorization:**
   - Are sensitive fields protected with `@auth` directives, resolver-level checks, or middleware?
   - Can an unauthenticated user query sensitive fields? (e.g., `user { email ssn }`)
   - Is authorization enforced at the resolver level, not just the schema level?
2. **Nested Authorization:**
   - If `User.orders` is protected, is `Order.user.orders` also protected? (authorization on nested resolvers)
   - Can an attacker traverse relationships to reach data their role doesn't permit?
3. **Mutation Authorization:**
   - Are all mutations checking the caller's permissions?
   - Can a regular user execute admin mutations?
   - Is the authorization check before or after input validation? (timing matters for information leakage)
4. **Subscription Authorization:**
   - If GraphQL subscriptions are used: is the WebSocket connection authenticated?
   - Can an unauthenticated client subscribe to sensitive data streams?
   - Is authorization re-checked on each subscription event or only at connection time?

## config-infrastructure

**GraphQL Server Configuration:**
1. **Error Masking:**
   - Does the GraphQL server expose internal error details in production? (stack traces, database errors, file paths)
   - Is `formatError` / `maskErrors` configured to strip internal details?
   - Are validation errors revealing schema information?
2. **CORS on GraphQL Endpoint:**
   - Is the GraphQL endpoint's CORS configuration restrictive?
   - Since GraphQL uses POST with `application/json`, CORS preflight is required — is it properly configured?
3. **Request Size Limits:**
   - Is there a maximum query string length? (prevent excessively large queries)
   - Is the POST body size limited?

## data-flow-tracer

**GraphQL Data Flow Patterns:**
1. Trace data from GraphQL query → resolver → data source → response
2. Are N+1 query patterns present? (resolver fetching per-item instead of batching — DataLoader pattern)
3. Is sensitive data filtered at the resolver level before returning? Or does the resolver return full database records?
4. Do resolvers share database connections/contexts that could leak data between requests?

## logic-dos

**GraphQL DoS Vectors:**
1. Deeply nested query exhaustion (exponential joins)
2. Alias multiplication (same field requested thousands of times)
3. Batch query flooding (thousands of operations in one request)
4. Fragment spread cycles (circular fragment references — most servers reject these, but check)
5. Subscription flooding (opening thousands of subscription connections)
