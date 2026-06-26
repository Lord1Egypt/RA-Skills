# Deepening

给定依赖关系，如何安全地 deepen 一组 shallow modules。假设你使用 [LANGUAGE.md](LANGUAGE.md) 中的词汇：**module**、**interface**、**seam**、**adapter**。

## Dependency categories

评估 deepening candidate 时，先分类它的 dependencies。类别决定 deepened module 如何跨 seam 测试。

### 1. In-process

纯计算、in-memory state、无 I/O。总是可以 deepen：合并 modules，并直接通过新 interface 测试。不需要 adapter。

### 2. Local-substitutable

存在本地 test stand-ins 的 dependencies（Postgres 用 PGLite、in-memory filesystem）。如果 stand-in 存在，就可以 deepen。deepened module 在 test suite 中用 stand-in 测试。seam 是内部的；module 外部 interface 上不需要 port。

### 3. Remote but owned (Ports & Adapters)

你自己控制的跨 network boundary 服务（microservices、internal APIs）。在 seam 处定义 **port**（interface）。deep module 拥有逻辑；transport 作为 **adapter** 注入。tests 使用 in-memory adapter。production 使用 HTTP/gRPC/queue adapter。

推荐表达：_"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."_

### 4. True external (Mock)

你不控制的第三方服务（Stripe、Twilio 等）。deepened module 把外部 dependency 作为 injected port；tests 提供 mock adapter。

## Seam discipline

- **One adapter means a hypothetical seam. Two adapters means a real one.** 除非至少有两个 adapters 有正当理由（通常 production + test），否则不要引入 port。单 adapter seam 只是 indirection。
- **Internal seams vs external seams.** deep module 可以有 internal seams（implementation 私有，由自己的 tests 使用），也可以有 interface 上的 external seam。不要因为 tests 使用 internal seams，就把它们暴露到 interface 上。

## Testing strategy: replace, don't layer

- 一旦 deepened module interface 上有 tests，旧的 shallow modules unit tests 就变成浪费，删除它们。
- 在 deepened module 的 interface 上写新 tests。**interface is the test surface**。
- Tests 通过 interface 断言 observable outcomes，而不是 internal state。
- Tests 应经受 internal refactors；它们描述 behaviour，不描述 implementation。如果 implementation 改变时 test 也必须改变，那它测过了 interface。
