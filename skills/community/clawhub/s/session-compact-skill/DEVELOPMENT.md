# OpenClaw Session Compact - 开发指南

## ✅ 项目概览

**位置**: `<project-root>` (e.g., `~/.openclaw/workspace/skills/session-compact`)

**类型**: OpenClaw 插件 (npm 包)

**功能**: 智能会话压缩，自动管理 Token 消耗，支持无限长对话

### 项目结构
```
openclaw-session-compact/
├── src/
│   ├── index.ts              # 插件入口 (register 函数)
│   ├── compact/
│   │   ├── config.ts         # 配置管理
│   │   ├── engine.ts         # 压缩核心逻辑
│   │   └── __tests__/        # 单元测试 (94 个测试)
│   └── cli/
│       └── register.ts       # CLI 命令注册 (遗留)
├── bin/
│   └── openclaw-compact.js   # 独立 CLI 入口
├── package.json              # npm 包配置
├── openclaw.plugin.json      # OpenClaw 插件清单
├── tsconfig.json             # TypeScript 配置
├── SKILL.md                  # 技能文档 (含 YAML frontmatter)
└── README.md                 # 完整文档
```

## 🔧 核心功能实现

1. **Token 估算**: `estimateTokenCount()` — 简化版（4 字符 ≈ 1 token）
2. **摘要生成**: `generateSummary()` — 调用 OpenClaw LLM 生成结构化摘要
3. **会话压缩**: `compactSession()` — 执行压缩逻辑
4. **CLI 命令**:
   - `openclaw compact` — 手动压缩
   - `openclaw compact-status` — 查看状态
   - `openclaw compact-config` — 配置管理

## 🏗️ 插件架构

### OpenClaw 插件系统 vs 技能系统

| 方面 | 工作区技能 (Workspace Skill) | 插件 (Plugin) |
|------|------------------------------|---------------|
| 位置 | `workspace/skills/` | `~/.openclaw/extensions/` |
| 用途 | LLM 文档提示 | 可执行代码 |
| 入口 | `SKILL.md` (含 frontmatter) | `dist/index.js` (含 `register()`) |
| CLI | 不支持 | 支持 (`api.registerCli()`) |

### 插件注册流程

```typescript
// src/index.ts
export function register(api: any) {
  api.registerCli(
    async ({ program }) => {
      program.command('compact').action(...)
      program.command('compact-status').action(...)
      program.command('compact-config').action(...)
    },
    {
      commands: ['compact', 'compact-status', 'compact-config'],
      descriptors: [...]
    }
  );
}
```

### 插件发现机制

1. OpenClaw 扫描 `~/.openclaw/extensions/` 目录
2. 查找包含 `"openclaw": { "extensions": [...] }` 的 `package.json`
3. 读取 `openclaw.plugin.json` 获取 `id`、`cli`、`configSchema`
4. 加载 `dist/index.js` 并调用 `register(api)`

## 🚀 开发工作流

### 本地开发
```bash
cd <project-root>

# 安装依赖
npm install

# 构建
npm run build

# 开发模式 (监听变化)
npm run dev

# 运行测试
npm test

# 查看覆盖率
npm run test:coverage
```

### 同步到插件目录
```bash
# 构建后同步到 extensions
rsync -a --exclude node_modules --exclude src --exclude coverage \
  --exclude .qwen --exclude "*.md" --exclude tsconfig.json \
  --exclude .gitignore --exclude .npmignore \
  ./ ~/.openclaw/extensions/openclaw-session-compact/

# 安装依赖
cd ~/.openclaw/extensions/openclaw-session-compact
npm install --production
```

### 测试插件
```bash
# 查看插件状态
openclaw plugins list | grep compact

# 测试 CLI 命令
openclaw compact-status
openclaw compact
openclaw compact-config
```

## 📦 发布到 ClawHub

### 前置条件

1. **登录 ClawHub**: `clawhub login` (GitHub OAuth)
2. **验证身份**: `clawhub whoami`

### 发布为 Code Plugin

```bash
# 先构建
npm run build

# 发布到 ClawHub
clawhub package publish . \
  --family code-plugin \
  --source-repo SDC-creator/openclaw-session-compact \
  --source-commit $(git rev-parse HEAD) \
  --version 1.0.0 \
  --changelog "更新说明" \
  --tags latest
```

### 必需的 `package.json` 字段

```json
{
  "name": "openclaw-session-compact",
  "version": "1.0.0",
  "openclaw": {
    "extensions": ["./dist/index.js"],
    "compat": {
      "pluginApi": ">=2026.4.2"
    },
    "build": {
      "openclawVersion": "2026.4.5"
    }
  }
}
```

### 验证发布

```bash
clawhub package inspect openclaw-session-compact
```

### 更新已有版本

```bash
clawhub package publish . \
  --family code-plugin \
  --source-repo SDC-creator/openclaw-session-compact \
  --source-commit $(git rev-parse HEAD) \
  --version 1.0.1 \
  --changelog "修复 xxx 问题" \
  --tags latest
```

## 📋 配置要求

### package.json
```json
{
  "name": "openclaw-session-compact",
  "version": "1.0.0",
  "main": "dist/index.js",
  "openclaw": {
    "extensions": ["./dist/index.js"],
    "compat": {
      "pluginApi": ">=2026.4.2"
    },
    "build": {
      "openclawVersion": "2026.4.5"
    }
  }
}
```

### openclaw.plugin.json
```json
{
  "id": "openclaw-session-compact",
  "cli": ["compact", "compact-status", "compact-config"],
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

### openclaw.json
```json
{
  "plugins": {
    "allow": ["openclaw-session-compact"],
    "entries": {
      "openclaw-session-compact": { "enabled": true }
    }
  }
}
```

## 🧪 测试

### 运行测试
```bash
npm test
```

### 查看覆盖率
```bash
npm run test:coverage
```

### 当前覆盖率
- **总覆盖率**: 94.65% (94 个测试通过)
- **核心功能覆盖**: 89.76%
- **测试文件**: 6 个

### 测试文件
- `src/compact/__tests__/config.test.ts` — 配置测试
- `src/compact/__tests__/engine.test.ts` — 引擎单元测试
- `src/compact/__tests__/engine-integration.test.ts` — 集成测试
- `src/compact/__tests__/engine-mock.test.ts` — Mock 测试
- `src/__tests__/index.test.ts` — 插件入口测试
- `src/__tests__/cli-register.test.ts` — CLI 注册测试

## 📝 添加新功能

1. 在 `src/compact/engine.ts` 中添加新函数
2. 在 `src/compact/__tests__/` 或 `src/__tests__/` 中添加对应测试
3. 运行 `npm run test:coverage` 确保覆盖率不下降
4. 更新 `README.md` 和 `SKILL.md` 文档
5. 重新构建: `npm run build`
6. 同步到 extensions 目录
7. 测试: `openclaw compact-status`

## ⚠️ 注意事项

1. **SKILL.md 必须有 YAML frontmatter** — 包含 `name` 和 `description` 字段，否则技能会被静默跳过
2. **插件需要 `openclaw.plugin.json`** — 包含 `id`、`cli`、`configSchema`
3. **`package.json` 使用 `openclaw.extensions`** — 不是 `openclaw.entry`
4. **插件 ID 必须在 `plugins.allow` 中** — 否则 CLI 命令不可用
5. **构建后需要同步到 extensions** — workspace 的修改不会自动同步
6. **Code Plugin 需要 `openclaw.compat.pluginApi` 和 `openclaw.build.openclawVersion`** — ClawHub 发布必需

## 🔮 待完成事项

- [ ] 对接真实 OpenClaw 会话存储 (替换 mock 数据)
- [ ] 优化 LLM 调用 (使用直接 API 而非 CLI)
- [ ] 支持递归压缩 (多次压缩)
- [ ] 添加进度指示器 (Spinner)

---

**项目状态**: ✅ 稳定版本
**测试**: ✅ 94/94 通过
**覆盖率**: 📈 94.65%
**ClawHub**: ✅ 已发布 (openclaw-session-compact@1.2.0)
**版本**: v1.0.0
