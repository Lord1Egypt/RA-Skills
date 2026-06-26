# SEVO Standalone 集成指南

OpenClaw（dev-01 子Agent）｜2026-04-28

这份文档只讲一件事：如果你不跑 OpenClaw，只想把 SEVO 的核心流程接到自己的项目里，当前代码库能怎么用，哪里已经有能力，哪里还没有接通。

## 先说结论

SEVO 现在有两层东西：

- `Sevo`：一层轻量 facade，用来创建 pipeline、推进阶段、读取状态
- `SevoHostAdapter`：一层宿主适配接口，用来对接你自己的任务派发、artifact 回收、门禁通知、需求分析

`StandaloneAdapter` 已经实现了 `SevoHostAdapter`，但它是一个**内存版适配器**：

- 会记录 dispatch
- 会缓存你手动注册的 artifact
- 会缓存 gate 通知
- 可以注入 `requirementAnalyzer`
- 不会真的起 agent
- 不会扫磁盘
- 不会发通知
- 进程结束后状态就没了

如果你只是想在自己项目里验证 SEVO 的核心流程，`Sevo + StandaloneAdapter` 已经够用。
如果你想把它接到自己的任务系统、对象存储、通知系统，就该自己实现一个 `SevoHostAdapter`。

## 安装

```bash
npm install sevo
```

### 当前版本的一个关键注意点

当前仓库里：

- 核心引擎的公共导出定义在 `src/index.ts`
- 包根的 `index.js` 是 OpenClaw 插件入口
- `package.json` 的 `main` 现在指向的是根目录 `index.js`

这意味着：

- `npm install sevo` 这一步是对的
- 但**如果发布包保持当前 `package.json` 结构不变**，你不能直接把它当成“包根就是 SEVO 核心 API”来用
- 下面的代码示例都以 `src/index.ts` 里真实存在的导出为准

换句话说，Standalone 集成时，你需要让自己的工程能访问 SEVO 核心入口。最直接的方式有两种：

- 在 monorepo / workspace 里直接引用当前仓库源码入口
- 在你的构建流程里把 `src/index.ts` 编译并暴露成你自己的稳定入口

下面示例里的 import 路径，都是按**当前仓库真实 API**写的。你落地时只需要把路径换成你项目里的实际入口。

## 当前公开 API 的真实入口

`src/index.ts` 现在导出了这些和 standalone 集成最相关的能力：

- `Sevo`
- `StandaloneAdapter`
- `OpenClawAdapter`
- `SevoHostAdapter`
- `TaskOrchestrator`
- `PipelineRun`
- `TaskPayload`
- `StageId`
- `ProjectConfig`
- `GateVerdict`
- `RequirementAnalysisRequest`
- `RequirementAnalysisResponse`

如果你只做最小集成，先盯住这几个就够了：

- `Sevo`
- `StandaloneAdapter`
- `SevoHostAdapter`
- `TaskPayload`
- `ProjectConfig`

## 最小可运行示例

这个示例只依赖 `Sevo` facade，做三件事：

- 创建 pipeline
- 推进阶段
- 获取状态

### 示例代码

```ts
import { Sevo, type TaskPayload } from '../src/index.js';

const DEFAULT_STAGES = [
  'spec',
  'spec-review-gate',
  'contract',
  'contract-review-gate',
  'implement',
  'review',
  'regression',
  'publish-generalization-gate',
  'deploy',
  'verify',
  'ledger',
] as const;

async function main() {
  const sevo = new Sevo({
    projectName: 'demo-project',
    stages: [...DEFAULT_STAGES],
    rules: [],
    adapter: 'standalone',
  });

  await sevo.init();

  const payload: TaskPayload = {
    taskId: 'task-001',
    title: '接入支付回调',
    initialStage: 'spec',
    stages: [...DEFAULT_STAGES],
  };

  const run = sevo.startPipeline(payload);

  console.log('runId =', run.runId);
  console.log('初始状态 =', sevo.getPipelineStatus(run.runId));

  let nextStage: string | null = run.getCurrentStage();

  while (nextStage !== null) {
    nextStage = sevo.advanceStage(run.runId);
    console.log('推进结果 =', nextStage);
    console.log('当前状态 =', sevo.getPipelineStatus(run.runId));
  }

  console.log('最终状态 =', sevo.getPipelineStatus(run.runId));
  sevo.shutdown();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

### 这个示例为什么能跑

因为它完全对应当前 `src/sevo.ts` 里的真实 API：

- `new Sevo(config)`
- `await sevo.init()`
- `sevo.startPipeline(payload)`
- `sevo.advanceStage(runId)`
- `sevo.getPipelineStatus(runId)`
- `sevo.shutdown()`

上面没有使用任何 README 里不存在于源码的方法。

### 这里有两个容易踩坑的点

第一个坑：`Sevo` 必须先 `init()`。

如果不先初始化，`startPipeline()`、`advanceStage()`、`getPipelineStatus()` 都会抛错：

```ts
throw new Error('Sevo not initialized. Call init() first.');
```

第二个坑：`Sevo` 当前默认跟着 `StageRouter` 的内置流程走，不是跟着 `payload.stages` 动态改图。

当前默认流程是：

`spec -> spec-review-gate -> contract -> contract-review-gate -> implement -> review -> regression -> publish-generalization-gate -> deploy -> verify -> ledger`

所以最稳妥的写法，就是像示例那样把完整默认阶段都传进去。否则你看到的推进结果可能和你手写的 `payload.stages` 不一致。

### 什么时候用 `evaluateGate()`

如果你想先看门禁结论，再决定要不要推进，可以单独调用：

```ts
const verdict = sevo.evaluateGate(run.runId);
console.log(verdict);
```

要注意一件事：`advanceStage(runId)` 内部已经做了“评估 gate + 推进阶段”这两个动作。你如果先调一次 `evaluateGate()`，再马上调一次 `advanceStage()`，就等于评估了两次。

## StandaloneAdapter 单独怎么用

`StandaloneAdapter` 适合做这几种事：

- 在测试里模拟宿主环境
- 在没有 OpenClaw 的项目里先把适配层接口跑通
- 先把 dispatch / artifact / gate 通知链路用内存打通，再替换成你自己的宿主实现

### 示例代码

```ts
import {
  StandaloneAdapter,
  type ProjectConfig,
  type ArtifactRef,
  type TaskPayload,
} from '../src/index.js';

const projectConfig: ProjectConfig = {
  workspaceRoot: process.cwd(),
  projectRoot: process.cwd(),
  artifactRoots: [`${process.cwd()}/artifacts`],
  defaultAgentId: 'dev-01',
  stageAgents: {
    implement: 'cc',
    review: 'audit-01',
  },
  notifications: {
    feishuEnabled: false,
  },
};

const adapter = new StandaloneAdapter(projectConfig, {
  requirementAnalyzer: async ({ prompt }) => ({
    summary: `需求摘要：${prompt}`,
    functionalRequirements: [
      {
        title: '示例需求',
        description: prompt,
        acceptanceCriteria: ['能够产出一条功能需求'],
      },
    ],
    ambiguities: [],
  }),
});

const payload: TaskPayload = {
  taskId: 'task-implement-001',
  title: '实现用户登录',
  initialStage: 'implement',
  stages: ['implement', 'review', 'verify', 'ledger'],
};

const taskId = await adapter.dispatchTask('implement', payload);

const artifacts: ArtifactRef[] = [
  {
    id: 'artifact-001',
    type: 'document',
    path: `${process.cwd()}/artifacts/task-implement-001-result.md`,
    createdAt: new Date().toISOString(),
    metadata: { size: 128 },
  },
];

adapter.registerArtifacts(taskId, artifacts);

const collected = await adapter.collectArtifacts(taskId);
console.log('taskId =', taskId);
console.log('dispatches =', adapter.getDispatches());
console.log('artifacts =', collected);

adapter.notifyGateResult('review', {
  gateId: 'review-gate',
  conclusion: 'passed',
  blockers: [],
  reviewBundles: [],
});

console.log('gateNotifications =', adapter.getGateNotifications());
console.log('projectConfig =', adapter.getProjectConfig());
```

### 这个 adapter 实际做了什么

按 `src/adapter/standalone-adapter.ts` 的实现，它会：

- 生成一个形如 `implement:task-implement-001:1` 的 taskId
- 把每次 dispatch 记到内存数组里
- 通过 `registerArtifacts(taskId, artifacts)` 手动登记 artifact
- 通过 `collectArtifacts(taskId)` 取回登记过的 artifact
- 通过 `notifyGateResult(stage, verdict)` 把 gate 结果记到内存里
- 通过 `getProjectConfig()` 返回一份防御性拷贝
- 如果提供了 `requirementAnalyzer`，支持 `analyzeRequirements()`

### 它不会做什么

它不会：

- 派发真实 agent
- 根据 `stageAgents` 自动找执行者
- 读写数据库
- 扫描 artifact 目录
- 自动发现文件
- 发飞书或任何外部通知
- 跨进程保存状态

所以 `StandaloneAdapter` 更像一个**开发态 / 测试态宿主壳子**，不是生产宿主。

## StandaloneAdapter 和 OpenClawAdapter 的差别

两者都实现了 `SevoHostAdapter`，但方向完全不一样。

### StandaloneAdapter

重点是“先把接口跑通”：

- 纯内存
- 无外部依赖
- 无真实派发
- artifact 只能靠 `registerArtifacts()` 手动登记
- gate 通知只保存在内存列表里
- 适合测试、PoC、非 OpenClaw 项目里的本地集成

### OpenClawAdapter

重点是“接 OpenClaw 运行时”：

- 可以接 `spawnClient` 做真实任务派发
- 会按 `stageAgents` / `defaultAgentId` 解析 agent
- 可以扫描 `artifactRoots` 目录，把匹配 `taskId` 的文件收回来
- 可以接 `eventBus` 发 gate 事件
- 可以接 `notifier` 发通知
- 可以从 `projectConfigPath` 加载项目配置

### 一句话判断怎么选

- 你只是想把核心流程在自己项目里先跑起来：用 `StandaloneAdapter`
- 你已经在 OpenClaw 里，想接它的 spawn / event / 通知：用 `OpenClawAdapter`
- 你有自己的任务系统、对象存储、通知中心：自己实现一个 `SevoHostAdapter`

## 自定义 adapter 的接口说明

SEVO 当前的宿主接口非常小，核心就是这个：

```ts
export interface SevoHostAdapter {
  dispatchTask(stage: StageId, payload: TaskPayload): Promise<string>;
  collectArtifacts(taskId: string): Promise<ArtifactRef[]>;
  notifyGateResult(stage: StageId, verdict: GateVerdict): void;
  getProjectConfig(): ProjectConfig;
  analyzeRequirements?(
    input: RequirementAnalysisRequest,
  ): Promise<RequirementAnalysisResponse>;
}
```

### 每个方法应该负责什么

`dispatchTask(stage, payload)`

- 把某个 stage 的任务发给你的宿主系统
- 返回一个宿主侧 taskId
- 这个 taskId 后面会用来回收 artifact

`collectArtifacts(taskId)`

- 根据 taskId 找回这个任务产出的 artifact
- 返回值是 `ArtifactRef[]`
- 你可以从本地文件、对象存储、数据库、HTTP 接口里取

`notifyGateResult(stage, verdict)`

- 当 gate 有结论时，把结果通知给宿主系统
- 这里适合接 IM、事件总线、Webhook、审计日志

`getProjectConfig()`

- 返回当前项目配置
- 至少要把 `workspaceRoot`、`projectRoot` 带出来
- 如果你有 stage 级 agent 路由，也可以放进 `stageAgents`

`analyzeRequirements?(input)`

- 这是可选方法
- 但如果你要跑 `SpecStage`，它就很重要
- 当前 `StandaloneAdapter` 和 `OpenClawAdapter` 在没有配置 `requirementAnalyzer` 时，都会在调用时直接抛错

## 一个最小的自定义 adapter 骨架

```ts
import type {
  SevoHostAdapter,
  StageId,
  TaskPayload,
  ArtifactRef,
  GateVerdict,
  ProjectConfig,
  RequirementAnalysisRequest,
  RequirementAnalysisResponse,
} from '../src/index.js';

export class MyHostAdapter implements SevoHostAdapter {
  constructor(private readonly config: ProjectConfig) {}

  async dispatchTask(stage: StageId, payload: TaskPayload): Promise<string> {
    const response = await myQueue.enqueue({ stage, payload });
    return response.taskId;
  }

  async collectArtifacts(taskId: string): Promise<ArtifactRef[]> {
    const files = await myArtifactStore.findByTaskId(taskId);
    return files.map((file) => ({
      id: file.id,
      type: file.type,
      path: file.path,
      createdAt: file.createdAt,
      metadata: file.metadata,
    }));
  }

  notifyGateResult(stage: StageId, verdict: GateVerdict): void {
    myNotifier.send({ stage, verdict });
  }

  getProjectConfig(): ProjectConfig {
    return {
      ...this.config,
      artifactRoots: this.config.artifactRoots
        ? [...this.config.artifactRoots]
        : undefined,
      stageAgents: this.config.stageAgents
        ? { ...this.config.stageAgents }
        : undefined,
      notifications: this.config.notifications
        ? { ...this.config.notifications }
        : undefined,
    };
  }

  async analyzeRequirements(
    input: RequirementAnalysisRequest,
  ): Promise<RequirementAnalysisResponse> {
    return myRequirementAnalyzer(input);
  }
}
```

这个骨架背后的原则很简单：

- SEVO 核心负责阶段语义
- 你的 adapter 负责接宿主能力
- 核心不应该知道你的队列、数据库、通知系统长什么样

## 当前 standalone 接入时最该知道的限制

这是基于当前源码得到的事实，不是建议性的猜测。

### 1. `Sevo` facade 现在不会接收 adapter 实例

`src/sevo.ts` 当前只接 `SevoConfig`，不会在构造时注入 `StandaloneAdapter` 或 `OpenClawAdapter` 实例。

现在的 `adapter: 'standalone' | 'openclaw'` 更像是配置元数据，而不是实际把某个 adapter 接进 facade 内部。

如果你需要把“真实任务派发 / artifact 回收 / 通知”接到运行时，当前更适合：

- 直接使用 adapter 类
- 或下探到 `TaskOrchestrator`、stage 实现、你自己的宿主编排层

### 2. `StandaloneAdapter` 的状态全在内存里

重启进程后，这些内容都会丢：

- dispatch 记录
- 已登记 artifact
- gate 通知记录

如果你要持久化，得自己实现 adapter，把这些东西写到文件、数据库或对象存储。

### 3. artifact 不是自动发现的

`StandaloneAdapter.collectArtifacts(taskId)` 只能拿到你之前 `registerArtifacts()` 进去的东西。

如果你的任务已经产出了文件，但你没登记，SEVO 看不到。

### 4. 需求分析器默认没有内建实现

如果你调用 `analyzeRequirements()`，却没有在构造 `StandaloneAdapter` 时传 `requirementAnalyzer`，会直接报错：

```ts
throw new Error('StandaloneAdapter requirementAnalyzer is not configured');
```

也就是说：

- 只跑 pipeline facade，可以不管这个
- 一旦你要接 `SpecStage`，就要自己提供需求分析能力

## 推荐的接入顺序

如果你想少踩坑，按这个顺序来最稳：

先做第一步：

- 用 `Sevo` 跑通创建、推进、读状态

再做第二步：

- 用 `StandaloneAdapter` 跑通 dispatch / artifact / gate 通知这三个动作

最后做第三步：

- 按你的宿主环境实现 `SevoHostAdapter`
- 把内存逻辑替换成真实队列、真实 artifact 存储、真实通知

这样做的好处很直接：

- 先验证 SEVO 核心 API 没有理解错
- 再验证宿主边界
- 最后再接生产级能力

## 你最少需要记住的几件事

- 真实公共 API 入口在 `src/index.ts`
- `Sevo` 能直接做：初始化、建 run、推进阶段、读状态
- `StandaloneAdapter` 是内存版宿主，不会做真实派发
- `OpenClawAdapter` 才是 OpenClaw 运行时适配器
- 想接自己的系统，实现 `SevoHostAdapter` 就行
- 如果要跑需求分析，记得提供 `requirementAnalyzer`
