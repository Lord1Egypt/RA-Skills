# 契约测试（Contract Testing）

> 在微服务/前后端分离架构中，用**消费者驱动契约（CDC）**保证接口提供方与调用方一致：消费者定义期望，提供方验证自己满足契约。避免「联调才发现接口对不上」。

## 何时使用

- 用户说「加契约测试」「前后端接口对不上」「微服务接口兼容」「防止破坏性变更」
- 多团队/多服务依赖同一 API，或前端与后端独立发布

## 核心概念（Pact）

- **Consumer（消费者）**：调用方，定义「我期望请求这样、响应那样」。
- **Provider（提供方）**：被调用方，验证自己满足所有消费者的契约。
- **Contract（契约）**：由消费者生成的 JSON，存于 Pact Broker 或本地。
- **CDC 流程**：消费者写测试生成契约 → 提供方拉契约验证。

## 消费者侧（生成契约）

```ts
import { Pact } from '@pact-foundation/pact';
import { like } from '@pact-foundation/pact';

const provider = new Pact({ consumer: 'web-app', provider: 'user-api', port: 8080 });

await provider.setup();
await provider.addInteraction({
  uponReceiving: '获取用户',
  withRequest: { method: 'GET', path: '/users/1' },
  willRespondWith: {
    status: 200,
    body: like({ id: 1, name: 'hope' }),  // like = 匹配类型
  },
});
// 调真实 client 指向 localhost:8080，断言后
await provider.verify();  // 生成契约
await provider.finalize();
```

## 提供方侧（验证契约）

```ts
import { Verifier } from '@pact-foundation/pact';

await new Verifier({
  providerBaseUrl: 'http://localhost:3000',
  pactUrls: ['./pacts/web-app-user-api.json'],
}).verifyProvider();
```

## 价值

- 消费者侧测试**不依赖提供方在线**，速度快、可本地跑。
- 提供方改接口前先验证契约，破坏兼容会**立即失败**，而非联调才爆。
- 适合前后端独立发版、多消费者共用一个 API。

## 与 E2E/API 测试关系

- API 测试（见 [references/api-testing.md](api-testing.md)）验证功能；契约测试验证**双方约定不被破坏**。
- 契约测试不等价于 E2E，不验证完整业务流程。

## 相关子技能（L3）

- 落地为契约测试动作（消费者侧生成 / 提供方侧验证）→ [skills/api-testing/SKILL.md](../skills/api-testing/SKILL.md)（契约测试属 API 测试范畴）

## 限制

- 引入额外工具链（Pact + Broker），小项目可能过度。
- 只覆盖接口形状与字段，不验证业务逻辑正确性。
- 需要消费者/提供方都采纳同一契约生态才能闭环。
