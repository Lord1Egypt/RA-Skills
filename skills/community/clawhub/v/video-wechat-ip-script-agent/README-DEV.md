# README-DEV.md

## 目标

本开发版把“提示词型 skill”升级为“可工程化的内容生成骨架”。

你可以在现有 OpenClaw skill 基础上继续扩展：
- 结构化调用四个服务：选题、脚本、改写、合规
- 统一拼装 prompt
- 解析并校验模型输出
- 在模型输出不完整时自动补齐默认字段

## 目录说明

- `services/`：面向业务能力的入口函数
- `lib/promptBuilder.ts`：统一拼装 prompt
- `lib/skillRegistry.ts`：统一维护 action 校验与分发注册表
- `lib/outputParser.ts`：解析 AI 返回结果，清洗字段
- `lib/fallback.ts`：字段不完整时的兜底默认值
- `config/`：行业、人设、平台、风格配置
- `prompts/`：各任务 Prompt 模板
- `schemas/`：TypeScript 类型定义

## 推荐接入方式

```ts
import { generateScript } from "./services/generateScript";
import { createModelInvoker } from "./lib/modelInvoker";

const invokeModel = createModelInvoker({
  model: "gpt-4.1-mini",
});

const result = await generateScript({
  topic: "顾客不是嫌贵，是你不会讲价值",
  style: "老板表达型",
  duration: 60,
  includeShotList: true,
  includePublishCaption: true,
  includeCommentCTA: true,
}, invokeModel);
```

## 统一模型调用器

项目现在内置统一模型调用器 `lib/modelInvoker.ts`：
- 默认走 OpenAI 兼容的 `chat/completions` 接口
- 支持通过环境变量注入 `MODEL_API_KEY` / `OPENAI_API_KEY`
- 支持通过 `MODEL_BASE_URL` / `OPENAI_BASE_URL` 切换网关
- 支持通过 `MODEL_MOCK_RESPONSE` 做本地无网络测试
- 所有 `services/*` 都复用同一个 `ModelInvoker` 类型

## 动作注册表

skill 入口现在不再把 action 校验和分发硬编码在 `index.ts` 里，而是统一收敛到 `lib/skillRegistry.ts`：
- 新增 action 时，补一条注册定义即可
- 请求校验和 handler 分发在同一处维护
- CLI help 会自动读取支持的 action 列表

## 脚本结构配置

脚本结构现在已配置化到 `config/script-structures.json`：
- 默认结构：`wechat_core_v1`
- 新增示例：`boss_point_v1`
- `generateScript` 支持传入 `scriptStructure`

这意味着以后新增脚本结构时，可以优先先改配置和 prompt 变量，而不是直接改 service 主体。

## 输出包配置

脚本输出字段现在也有单独配置：
- 配置文件：`config/script-output-profiles.json`
- 默认输出包：`full_publish_pack`
- 精简输出包：`lite_publish_pack`

`generateScript` 现在支持传入 `outputProfile`，并且还会结合：
- `includeShotList`
- `includePublishCaption`
- `includeCommentCTA`

一起决定最终保留哪些字段。这样以后如果你要新增“只出脚本和标题”或“直播预热版输出包”，可以先改配置，而不是直接改解析主流程。

选题和合规结果现在也支持同样思路：
- `config/topic-output-profiles.json`
- `config/compliance-output-profiles.json`
- `config/rewrite-profiles.json`

当前内置示例：
- 选题：`default_topics`
- 合规：`full_compliance`、`issues_only`
- 改写：`default_rewrite`、`boss_only`

这意味着以后如果你要做“只看风险点”或“只保留基础选题字段”的输出形态，也可以优先走配置，而不是改 service 主流程。

改写服务 `rewriteStyle` 现在也支持 `rewriteProfile`：
- 可以控制默认风格集合
- prompt 会自动注入对应 profile 配置
- 如果没有传 `styles`，会优先取 profile 里的 styles

## OpenClaw 可调用入口

根目录新增了 `openclaw.ts` 与 `index.ts`，可以直接作为技能执行入口：

```bash
npm run build
echo '{"action":"script","payload":{"topic":"客户不是嫌贵，是你没讲清价值"}}' | node dist/openclaw.js
```

也支持拆开的 CLI 参数形式：

```bash
node dist/openclaw.js --action script --payload '{"topic":"客户不是嫌贵，是你没讲清价值"}'
node dist/openclaw.js --action script --payload-file ./tests/fixtures/script-request.json
```

支持的 `action`：
- `topics`
- `script`
- `rewrite`
- `compliance`

## 联调样例

根目录下新增了标准请求样例，便于本地联调或接 OpenClaw 时直接复用：
- `examples/requests/topics.json`
- `examples/requests/script.json`
- `examples/requests/rewrite.json`
- `examples/requests/compliance.json`

例如：

```bash
npm run build
node dist/openclaw.js --file ./examples/requests/script.json
```

如果只想验证入口链路、不想走真实网络，可以配合 `MODEL_MOCK_RESPONSE` 使用。

## 配置校验

项目新增了配置校验脚本：

```bash
npm run validate-config
```

它会检查当前所有关键配置文件的基础结构是否完整，包括：
- `persona.json`
- `platforms.json`
- `styles.json`
- `script-structures.json`
- `script-output-profiles.json`
- `topic-output-profiles.json`
- `compliance-output-profiles.json`
- `rewrite-profiles.json`

## 模型适配假设

本骨架默认不强绑某一家 SDK，而是统一走 `invokeModel`。如果你有自定义网关，只需要传入 `baseUrl/model/apiKey`，或直接替换 `createModelInvoker` 的实现即可。

期望模型返回：
1. JSON 字符串；或
2. Markdown 包裹的 JSON；或
3. 普通文本（将触发宽松解析与兜底）

## 扩展建议

### 新增平台
1. 在 `config/platforms.json` 中新增平台规则
2. 在调用时传入 `platform`
3. 必要时新增对应 prompt 模板

### 新增风格
1. 在 `config/styles.json` 中新增风格项
2. 不改 service 逻辑即可生效

### 新增行业
1. 在 `config/persona.json` 中补充行业设定
2. 如需行业差异化 prompt，可增加新模板并在 `promptBuilder` 中切换
