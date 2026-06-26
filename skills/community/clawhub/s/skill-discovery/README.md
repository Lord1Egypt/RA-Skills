# Skill Discovery

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](LICENSE)

基于用户意图自动发现并安装 skills 的 OpenClaw 技能。当用户表达某类需求时，自动从 skills.sh 搜索、验证并安装最匹配的 skill。

## 安装

在 OpenClaw 中直接对话：

```
> 帮我安装这个 skill：https://github.com/caocong1/skill-discovery
```

或通过命令行：

```bash
npx skills add https://github.com/caocong1/skill-discovery -g
```

## 它能做什么

安装后，当你在 OpenClaw 中输入类似以下内容时，skill-discovery 会自动介入：

```
> 帮我部署到 Vercel
✅ 已自动安装 vercel-labs/agent-skills@vercel-deploy
📊 安装量: 262,000
🔗 https://skills.sh/vercel-labs/agent-skills/vercel-deploy

> 怎么写测试
✅ 已自动安装 vercel-labs/agent-skills@testing-best-practices
```

**不会触发的情况：**
- "今天天气怎么样" — 非技能需求
- "什么是 React" — 知识类提问
- "为什么报错" — 调试类问题

## 工作原理

1. **意图分析** — 通过触发词 + 领域关键词 + 置信度评分判断是否需要搜索 skill
2. **搜索** — 调用 `npx skills find` 从 skills.sh 查找匹配结果（带 10 分钟缓存）
3. **质量验证** — 安装量 >= 1000 且来源可信（vercel-labs、anthropics、openai 等）
4. **自动安装** — 选择评分最高的 skill 并安装

## 触发词

| 语言 | 示例 |
|------|------|
| 中文 | "帮我..."、"怎么..."、"有什么工具..."、"推荐一个..."、"找个...工具" |
| 英文 | "find a skill for..."、"help me with..."、"is there a skill that..."、"I need..." |

## 覆盖领域

DevOps、测试、设计、文档、代码质量、数据处理、图片处理、视频处理、性能优化、API/网络、数据库、AI/ML、安全、移动端、游戏

## 安全机制

- **Shell 转义** — CLI 参数转义防止命令注入
- **日志脱敏** — token、密钥等敏感信息自动遮蔽
- **卸载备份** — 卸载的 skill 备份到 `.trash/`，保留 7 天
- **来源验证** — 校验 skill 来源是否在可信 owner 列表中

## 编程接口

如果需要在自己的代码中调用：

```javascript
const { autoDiscover, onUserInput } = require('skill-discovery');

// 方式一：直接发现
const result = await autoDiscover('帮我部署到 Vercel', { dryRun: true });
// { success, stage, outcome, skill, message, ... }

// 方式二：OpenClaw 钩子
const hookResult = await onUserInput('写个测试');
if (hookResult.handled) {
  console.log(hookResult.response);
}
```

## 返回结构

```javascript
{
  success: boolean,
  stage: 'analyze' | 'search' | 'select' | 'install',
  outcome: 'installed' | 'already_installed' | 'dry_run' | 'skipped' | 'failed',
  errorCode: string | null,
  skill: object | null,
  candidates: array,
  message: string
}
```

## 规划中

- 配置文件支持（`config.json` 用户级覆盖）
- 交互式确认/审批流程（针对非可信来源）
- 安装前内容预审扫描
- Skill 评分集成
- 用户反馈循环优化推荐

---

## 开发

面向贡献者的信息：

```bash
npm install               # 安装依赖
npm test                  # 运行全部测试（80 个用例）
npm run test:unit         # 仅单元测试
npm run test:coverage     # 含覆盖率
npm run lint              # ESLint 检查
node index.js --help      # CLI 模式帮助
```

### 项目结构

```
constants.js          # 统一常量（MAGIC、CONFIG、ERROR_CODES）
skills-cli.js         # npx skills CLI 封装（Phase 1）
auto-discover.js      # 核心发现逻辑（Phase 2）
openclaw-hook.js      # OpenClaw 集成（Phase 3）
index.js              # 主入口 + CLI
```

## 依赖

- Node.js >= 18
- `npx skills` CLI（来自 skills.sh）
- OpenClaw（可选，用于钩子集成）

## 许可证

MIT-0
