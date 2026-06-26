# QuizMe — Per-Topic Coverage Guide

This reference defines what concepts to cover at each difficulty level for every supported topic area, and provides example question ideas.

---

## Python

### Beginner
**Concepts:**
- Variable types and type casting (`int`, `str`, `float`, `bool`)
- Lists, tuples, dicts, sets — creation and basic operations
- `if`/`elif`/`else` and comparison operators
- `for`/`while` loops, `range()`
- Defining and calling functions, default arguments

**Example question ideas:**
- "What is the output of `print(type(3.0))`?"
- "Which of these creates a tuple with one element: `(1)`, `(1,)`, `[1]`, `{1}`?"
- "What does `list.append()` return?"
- Code snippet: a simple loop printing values — ask what is printed.

### Intermediate
**Concepts:**
- List comprehensions and generator expressions
- `*args` and `**kwargs`
- Exception handling (`try`/`except`/`finally`)
- Classes, `__init__`, `self`, inheritance
- Mutable vs. immutable types, default mutable argument trap

**Example question ideas:**
- Code: `def f(x=[]): x.append(1); return x` — ask what `f()` returns on the second call.
- "What does `super().__init__()` do?"
- Code: a list comprehension with a condition — ask what it produces.
- "What is the difference between `is` and `==`?"

### Advanced
**Concepts:**
- Decorators and `functools.wraps`
- `async`/`await`, `asyncio.gather`, event loop mechanics
- Generator protocol (`__iter__`, `__next__`, `yield from`)
- Context managers (`__enter__`, `__exit__`, `contextlib`)
- GIL, threading vs. multiprocessing tradeoffs

**Example question ideas:**
- Code: a decorator that times a function — spot the missing `functools.wraps`.
- "What is the difference between `asyncio.gather` and `asyncio.wait`?"
- Code: a generator with `yield from` — ask what the caller receives.
- "When does the GIL not protect you from race conditions?"

---

## JavaScript

### Beginner
**Concepts:**
- `var` vs. `let` vs. `const` — scope and hoisting
- Arrow functions vs. regular functions
- Template literals
- Array methods: `map`, `filter`, `reduce`
- `undefined` vs. `null`

**Example question ideas:**
- Code: `console.log(x); var x = 5;` — ask what is logged.
- "What does `Array.prototype.filter()` return?"
- Code: arrow function vs. regular function — ask which has its own `this`.
- "What is the output of `typeof null`?"

### Intermediate
**Concepts:**
- Closures and lexical scope
- Prototype chain and `Object.create()`
- Promises: `.then()`, `.catch()`, chaining
- Event loop, call stack, task queue, microtask queue
- Destructuring and spread/rest operators

**Example question ideas:**
- Code: classic closure-in-loop with `var` — ask what is logged.
- "In what order do microtasks and macrotasks execute?"
- Code: chained Promises — ask what value resolves.
- "What does `Object.assign({}, a, b)` do?"

### Advanced
**Concepts:**
- `async`/`await` error handling patterns
- `WeakMap`/`WeakRef` and memory management
- Generators and iterators
- Module system: CommonJS vs. ESM
- Performance: debounce vs. throttle, memory leaks

**Example question ideas:**
- Code: `async` function with a `try/catch` wrapping `await Promise.reject(...)` — does it catch?
- "What is the difference between CommonJS `require()` and ESM `import`?"
- Code: a generator function — ask what calling `.next()` twice returns.
- "What causes a memory leak with closures? Give an example."

---

## SQL

### Beginner
**Concepts:**
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
- `INNER JOIN` vs. `LEFT JOIN`
- `GROUP BY` and `HAVING`
- Aggregate functions: `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
- `NULL` handling: `IS NULL`, `COALESCE`

**Example question ideas:**
- "What is the difference between `WHERE` and `HAVING`?"
- Code: a `LEFT JOIN` query — ask which rows appear in the result.
- "What does `COUNT(*)` vs. `COUNT(column)` count differently?"
- "What does `COALESCE(NULL, NULL, 3)` return?"

### Intermediate
**Concepts:**
- Indexes: B-tree structure, when they help, when they don't
- `EXPLAIN` / `EXPLAIN ANALYZE` output reading
- Subqueries vs. CTEs (`WITH` clause)
- `DISTINCT` and deduplication cost
- Transactions: `COMMIT`, `ROLLBACK`, isolation levels

**Example question ideas:**
- "Why does `WHERE LOWER(email) = ...` prevent index use?"
- Code: a CTE vs. subquery — ask which is more readable/reusable.
- "What isolation level prevents phantom reads?"
- "When would an index make a query slower, not faster?"

### Advanced
**Concepts:**
- Window functions: `ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `PARTITION BY`
- Query optimization: index-only scans, covering indexes, selectivity
- `LATERAL` joins
- Partial indexes and expression indexes
- Locking: row-level, table-level, deadlocks

**Example question ideas:**
- Code: window function with `PARTITION BY` — ask what the output is.
- "What is a covering index and how does it improve performance?"
- "What is the difference between `RANK()` and `DENSE_RANK()`?"
- Code: two transactions touching the same rows — identify the deadlock.

---

## System Design

### Beginner
**Concepts:**
- Client-server architecture
- What a load balancer does
- Horizontal vs. vertical scaling
- What a CDN is and when to use one
- Stateless vs. stateful services

**Example question ideas:**
- "What is the difference between horizontal and vertical scaling?"
- "What problem does a CDN solve?"
- "Why is stateless design preferred for horizontally scaled services?"
- "What does a load balancer do at a high level?"

### Intermediate
**Concepts:**
- Caching strategies: cache-aside, write-through, write-behind
- Database replication: primary-replica, read replicas
- CAP theorem: consistency, availability, partition tolerance
- Message queues and async processing
- Rate limiting algorithms: token bucket, leaky bucket

**Example question ideas:**
- "In cache-aside, who is responsible for populating the cache?"
- "Which two of CAP can a distributed system actually guarantee together?"
- "What problem does a message queue solve vs. direct service-to-service calls?"
- "How does a token bucket rate limiter work?"

### Advanced
**Concepts:**
- Consistent hashing and virtual nodes
- Saga pattern for distributed transactions
- Event sourcing and CQRS
- Database sharding strategies and hotspot avoidance
- Consensus algorithms: Raft / Paxos at a high level

**Example question ideas:**
- "What problem does consistent hashing solve compared to modulo hashing?"
- "What is the difference between the Saga orchestration and choreography patterns?"
- "How does CQRS separate reads and writes, and what is the tradeoff?"
- "What is a hotspot shard and how do you avoid it?"

---

## Algorithms & Data Structures

### Beginner
**Concepts:**
- Big-O notation: O(1), O(n), O(n²), O(log n)
- Arrays vs. linked lists: access, insert, delete cost
- Stack and queue operations
- Binary search precondition and complexity
- Hash map basics

**Example question ideas:**
- "What is the time complexity of looking up a value in a hash map?"
- "Which is faster for random access: array or linked list?"
- "What is the precondition for binary search?"
- Code: a nested loop — ask for the Big-O.

### Intermediate
**Concepts:**
- Binary trees: BFS vs. DFS traversal
- Heap / priority queue operations
- Graph representations: adjacency list vs. matrix
- Recursion and memoization
- Sorting: merge sort, quick sort — complexity and stability

**Example question ideas:**
- "What is the difference between in-order, pre-order, and post-order traversal?"
- "When would you use BFS over DFS?"
- Code: a recursive Fibonacci — ask its time complexity without memoization.
- "Is quicksort stable? Why does it matter?"

### Advanced
**Concepts:**
- Dynamic programming: overlapping subproblems, optimal substructure
- Dijkstra's vs. Bellman-Ford (negative weights)
- Trie structure and use cases
- Union-Find / disjoint sets with path compression
- Amortized analysis (e.g., dynamic array doubling)

**Example question ideas:**
- "Why can't Dijkstra's algorithm handle negative edge weights?"
- "What is the amortized cost of appending to a dynamic array?"
- "What problem does a Trie solve more efficiently than a hash map?"
- Code: a DP table fill — ask what value is at `dp[n]`.

---

## Networking

### Beginner
**Concepts:**
- HTTP request/response model, status codes (200, 404, 500, 301)
- DNS: what it does, A record vs. CNAME
- TCP vs. UDP: reliability tradeoffs
- IP address basics, ports
- What HTTPS adds over HTTP

**Example question ideas:**
- "What HTTP status code means a resource was permanently moved?"
- "What is the role of DNS in loading a webpage?"
- "Why would you choose UDP over TCP for a video stream?"
- "What does HTTPS add that plain HTTP lacks?"

### Intermediate
**Concepts:**
- TCP three-way handshake
- HTTP/1.1 vs. HTTP/2: multiplexing, header compression
- TLS handshake at a high level
- WebSockets: how the upgrade works, use cases
- Cookies vs. `Authorization` header for auth

**Example question ideas:**
- "What are the three steps in the TCP handshake?"
- "What problem does HTTP/2 multiplexing solve?"
- "How is a WebSocket connection established from an HTTP request?"
- "What is the difference between a session cookie and a JWT in the `Authorization` header?"

### Advanced
**Concepts:**
- HTTP/3 and QUIC: why UDP-based
- CDN edge caching: `Cache-Control`, `Vary`, `ETag`
- TCP congestion control (AIMD, slow start)
- mTLS and zero-trust networking
- gRPC vs. REST: when each wins

**Example question ideas:**
- "Why is HTTP/3 built on QUIC (UDP) rather than TCP?"
- "What does `Cache-Control: no-cache` actually mean?"
- "What is TCP slow start and when does it affect performance?"
- "What is the key difference between mTLS and regular TLS?"

---

## Git

### Beginner
**Concepts:**
- `git add`, `git commit`, `git status`, `git log`
- `git clone` and `git pull` vs. `git fetch`
- Branching: `git branch`, `git checkout`, `git switch`
- `git merge` basics
- Reading a diff

**Example question ideas:**
- "What is the difference between `git pull` and `git fetch`?"
- "What does `git status` show?"
- "What does `git checkout -b feature` do?"
- "How do you stage only part of a file?"

### Intermediate
**Concepts:**
- `git rebase` vs. `git merge` — when to use each
- Interactive rebase: squash, fixup, reorder
- Resolving merge conflicts
- `git stash` and `git stash pop`
- `git reset` modes: `--soft`, `--mixed`, `--hard`

**Example question ideas:**
- "What is the key difference between rebase and merge in terms of history?"
- "What does `git reset --soft HEAD~1` do?"
- "How do you squash the last 3 commits into one?"
- "When would you use `git stash` over committing?"

### Advanced
**Concepts:**
- `git reflog` and recovering lost commits
- `git bisect` for bug hunting
- Detached HEAD state
- Worktrees
- Signing commits with GPG

**Example question ideas:**
- "What is a detached HEAD state and how do you recover from it?"
- "How does `git bisect` work to find a regression?"
- "What does `git reflog` show that `git log` doesn't?"
- "What is a git worktree and when is it useful?"

---

## Docker / Kubernetes

### Beginner
**Concepts:**
- Image vs. container
- `docker run`, `docker build`, `docker ps`
- Dockerfile: `FROM`, `RUN`, `COPY`, `CMD`, `EXPOSE`
- Port mapping (`-p host:container`)
- `docker-compose` basics

**Example question ideas:**
- "What is the difference between a Docker image and a container?"
- Code: a Dockerfile — ask which instruction runs at build time vs. runtime.
- "What does `-p 8080:80` mean in `docker run`?"
- "What is the purpose of `CMD` vs. `ENTRYPOINT` in a Dockerfile?"

### Intermediate
**Concepts:**
- Layer caching and ordering `COPY`/`RUN` instructions
- Volumes vs. bind mounts
- Multi-stage builds
- Kubernetes: Pod, Deployment, Service, Namespace
- `kubectl get`, `kubectl describe`, `kubectl logs`

**Example question ideas:**
- "Why should you `COPY requirements.txt` before `COPY . .` for better caching?"
- "What is the difference between a Kubernetes Pod and a Deployment?"
- "What does a Kubernetes Service do?"
- "When would you use a volume vs. a bind mount?"

### Advanced
**Concepts:**
- Kubernetes: liveness vs. readiness probes
- Resource requests vs. limits
- ConfigMaps and Secrets
- Horizontal Pod Autoscaler
- Rolling updates and rollback strategy

**Example question ideas:**
- "What is the difference between a liveness probe and a readiness probe?"
- "What happens when a container exceeds its memory limit in Kubernetes?"
- "How does a rolling update prevent downtime?"
- "What is the difference between a ConfigMap and a Secret?"

---

## APIs

### Beginner
**Concepts:**
- REST conventions: HTTP verbs (GET, POST, PUT, DELETE, PATCH)
- Status codes for APIs: 200, 201, 400, 401, 403, 404, 422, 500
- JSON request/response structure
- Query parameters vs. path parameters vs. request body
- API keys: basic usage

**Example question ideas:**
- "Which HTTP method should be used to partially update a resource?"
- "What is the difference between a 401 and a 403 response?"
- "When would you use a path parameter vs. a query parameter?"
- "What does a 201 status code indicate?"

### Intermediate
**Concepts:**
- REST vs. GraphQL tradeoffs
- Pagination: offset vs. cursor-based
- Idempotency and safe methods
- OAuth 2.0 flow: authorization code, client credentials
- Rate limiting and `Retry-After` header

**Example question ideas:**
- "What makes a REST endpoint idempotent? Give an example."
- "What is the main advantage of cursor-based pagination over offset?"
- "In OAuth 2.0, what is the difference between the authorization code flow and client credentials?"
- "What does GraphQL solve that REST doesn't handle well?"

### Advanced
**Concepts:**
- JWT structure and validation (header, payload, signature)
- API versioning strategies: URL path, header, query param
- gRPC vs. REST for internal services
- Webhooks: delivery guarantees, retry logic, signature verification
- HATEOAS and REST maturity levels

**Example question ideas:**
- "What is in a JWT and what should you NOT put in the payload?"
- "What are the tradeoffs of URL-based vs. header-based API versioning?"
- "How do you verify that a webhook payload came from the expected sender?"
- "What is the Richardson Maturity Model for REST?"

---

## General CS Concepts

### Beginner
**Concepts:**
- Stack vs. heap memory
- Compiled vs. interpreted languages
- Process vs. thread
- Binary, hexadecimal number representation
- What an OS kernel does

**Example question ideas:**
- "What is stored on the stack vs. the heap?"
- "What is the difference between a process and a thread?"
- "What does `0xFF` equal in decimal?"
- "What is the difference between a compiled and an interpreted language?"

### Intermediate
**Concepts:**
- Race conditions and mutex/lock
- Deadlock: conditions and prevention
- Virtual memory and paging
- Garbage collection: reference counting vs. mark-and-sweep
- Context switching cost

**Example question ideas:**
- "What are the four conditions required for a deadlock?"
- "How does reference counting garbage collection fail?"
- "What is virtual memory and why does it exist?"
- "What makes a context switch expensive?"

### Advanced
**Concepts:**
- Memory ordering and CPU cache coherence
- Lock-free data structures (CAS operations)
- JIT compilation
- ACID properties in databases
- Flynn's taxonomy (SIMD, MIMD)

**Example question ideas:**
- "What is a compare-and-swap (CAS) operation and why is it used?"
- "What does the ACID 'Atomicity' property guarantee?"
- "What is the difference between SIMD and MIMD parallelism?"
- "How does JIT compilation differ from ahead-of-time compilation?"
