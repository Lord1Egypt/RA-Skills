# OpenClaw Session Compact Plugin 🔄

智能会话压缩插件，自动管理 Token 消耗，支持**无限长对话**。通过自动压缩历史消息，将长对话压缩为结构化摘要，显著降低 Token 使用量（通常节省 85-95%）。

## 🚀 快速开始

### 安装

**从 ClawHub 安装**（推荐）：

```bash
clawhub install openclaw-session-compact
```

**手动安装**：

```bash
git clone https://github.com/SDC-creator/openclaw-session-compact.git \
  ~/.openclaw/extensions/openclaw-session-compact
cd ~/.openclaw/extensions/openclaw-session-compact
npm install --production
```

### 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "plugins": {
    "allow": ["openclaw-session-compact"],
    "entries": {
      "openclaw-session-compact": { "enabled": true }
    }
  },
  "skills": {
    "entries": {
      "openclaw-session-compact": {
        "enabled": true,
        "max_tokens": 10000,
        "preserve_recent": 4,
        "auto_compact": true,
        "model": "qwen/qwen3.5-122b-a10b"
      }
    }
  }
}
```

## 💡 使用场景

### 场景 1: CLI 命令

```bash
# 查看当前会话状态
openclaw compact-status

# 手动触发压缩
openclaw compact

# 强制压缩（忽略阈值）
openclaw compact --force

# 查看配置
openclaw compact-config
```

### 场景 2: 自动压缩

```bash
# 启动 OpenClaw，压缩功能自动生效
openclaw start

# 当对话历史超过阈值时，自动压缩并继续
# 用户无感知，对话无缝继续
```

### 场景 3: 长对话场景

**问题**: 对话超过 10,000 tokens，导致：
- Token 消耗过快
- 响应变慢
- 可能超出模型限制

**解决**: Session Compact 自动压缩历史，保持对话流畅：

```
原始对话：50 条消息 (1,250 tokens)
        ↓ [自动压缩]
压缩后：5 条消息 (360 tokens) - 节省 92% Token
```

## 🔧 配置项详解

| 参数 | 类型 | 默认值 | 说明 | 推荐值 |
|------|------|--------|------|--------|
| `max_tokens` | number | 10000 | 触发压缩的 Token 阈值 | 5000-20000 |
| `preserve_recent` | number | 4 | 保留最近 N 条消息 | 4-6 |
| `auto_compact` | boolean | true | 是否自动压缩 | true |
| `model` | string | '' | 用于生成摘要的模型 | 全局默认 |

### 配置示例

**保守模式**（频繁压缩，节省 Token）:
```json
{
  "max_tokens": 5000,
  "preserve_recent": 6
}
```

**激进模式**（减少压缩次数，保持更多上下文）:
```json
{
  "max_tokens": 20000,
  "preserve_recent": 3
}
```

## 📊 工作原理

### 压缩流程

```
1. 监控 Token 使用量
   ↓
2. 超过阈值 (90%)?
   ├─ 否 → 继续对话
   └─ 是 → 触发压缩
        ↓
3. 保留最近 N 条消息 (默认 4 条)
   ↓
4. 压缩旧消息为结构化摘要
   ├─ Scope: 统计信息
   ├─ Recent requests: 最近用户请求
   ├─ Pending work: 待办事项
   ├─ Key files: 关键文件
   ├─ Tools used: 使用的工具
   └─ Key timeline: 对话时间线
   ↓
5. 替换旧消息，插入 System 摘要
   ↓
6. 无缝继续对话
```

### 降级机制

当 LLM 不可用时，自动降级为**代码提取**模式：
- 从消息内容直接提取时间线
- 使用预设模板填充摘要字段
- 保证功能可用，无需依赖 LLM

## 🛠️ 故障排查

### 常见问题

#### 1. 压缩未触发

**原因**: Token 未达到阈值
**解决**:
```bash
# 检查当前 Token 使用
openclaw compact-status

# 强制压缩测试
openclaw compact --force
```

#### 2. 摘要质量差

**原因**: LLM 配置错误或不可用
**解决**:
- 检查 `model` 配置
- 确保 OpenClaw 网关已启动: `openclaw gateway start`
- 系统会自动降级为代码提取摘要

#### 3. 压缩后上下文丢失

**原因**: `preserve_recent` 设置过低
**解决**:
```json
{
  "preserve_recent": 6  // 增加到 6 或更多
}
```

#### 4. 插件未被识别

**原因**: 插件配置缺失
**解决**:
```bash
# 检查插件状态
openclaw plugins list | grep compact

# 确保 openclaw.json 中 plugins.allow 包含 openclaw-session-compact
```

## 📈 性能指标

- **测试覆盖率**: 94.65% (94 个测试通过)
- **核心功能覆盖**: 89.76%
- **平均压缩时间**: < 1 秒 (无 LLM 调用)
- **Token 节省**: 通常 85-95%
- **内存使用**: 低 (无泄漏)

## 🧪 测试

```bash
# 运行测试
npm test

# 查看覆盖率
npm run test:coverage
```

## 📚 技术文档

详细 API 文档和使用示例请查看 [README.md](README.md)。

### 核心 API

```typescript
// 压缩会话
const result = await compactSession(messages, config);

// 检查是否需要压缩
const needsCompact = shouldCompact(messages, config);

// 估算 Token 数量
const tokens = estimateTokenCount(messages);
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

## 📄 许可证

MIT License

---

**项目状态**: ✅ 稳定发布
**测试状态**: ✅ 94/94 通过
**覆盖率**: 📈 94.65%
**ClawHub**: ✅ 已发布 (openclaw-session-compact@1.2.0)
**版本**: v1.0.0
**维护者**: SDC-creator
