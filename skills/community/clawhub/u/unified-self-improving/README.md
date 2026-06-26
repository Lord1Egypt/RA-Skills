# Unified Self-Improving Skill

统一自我进化系统，整合 self-improving-agent、self-improving、mulch 三个技能的优势。

**ClawHub**: https://clawhub.ai/421zuoduan/unified-self-improving

## 功能

- 三层存储：HOT / WARM / COLD
- 双格式：Markdown + JSONL
- 统一 CLI 接口
- 命名空间隔离
- 自动升级规则
- 模式检测

## 安装

```bash
# 从 ClawHub 安装
clawhub install unified-self-improving

# 或从 GitHub 克隆
git clone https://github.com/421zuoduan/unified-self-improving.git
```

## 使用方法

### CLI 命令

```
unified-self-improving <command> [options]
```

| 命令 | 功能 | 示例 |
|------|------|------|
| `log` | 记录 correction/error/pattern | `log -t correction -c "用户纠正了我"` |
| `query` | 查询学习项 | `query --pattern "error"` |
| `move` | 移动层级 | `move --id learn-xxx --to warm` |
| `recall` | 从 COLD 召回 | `recall --id learn-xxx` |
| `namespace` | 命名空间管理 | `namespace create myproject` |
| `index` | 索引管理 | `index rebuild` |
| `import` | 批量导入 | `import learnings.jsonl` |
| `session` | 会话管理 | `session start` / `session end` |
| `detect-pattern` | 模式检测 | `detect-pattern` |

### 详细用法

#### 记录学习项
```bash
# 记录用户纠正
unified-self-improving log -t correction -c "用户说我不应该..."

# 记录错误
unified-self-improving log -t error -c "命令执行失败" -p high

# 指定命名空间
unified-self-improving log -t pattern -c "检测到重复行为" -n myproject
```

#### 查询
```bash
# 查询所有
unified-self-improving query

# 按关键词搜索
unified-self-improving query --pattern "correction"

# 按 ID 查询
unified-self-improving query --id learn-20260315-001

# 按优先级/层级过滤
unified-self-improving query --priority high --level hot
```

#### 层级移动
```bash
# 移动到指定层级
unified-self-improving move --id learn-xxx --to warm
```

#### 命名空间
```bash
# 创建命名空间
unified-self-improving namespace create myproject

# 列出命名空间
unified-self-improving namespace list

# 删除命名空间
unified-self-improving namespace delete myproject
```

#### 索引
```bash
# 重建索引
unified-self-improving index rebuild
```

#### 导入导出
```bash
# 批量导入
unified-self-improving import learnings.jsonl

# 指定目标层级和命名空间
unified-self-improving import -n myproject -l warm data.jsonl
```

#### 会话管理
```bash
# 开始会话
unified-self-improving session start

# 结束会话 (自动执行升级和清理)
unified-self-improving session end
```

## 存储结构

```
~/.openclaw/workspace/memory/
├── hot/                    # 最近 3 次会话
│   ├── session-*.md
│   ├── session-*.jsonl
│   ├── corrections.md
│   ├── errors.md
│   └── patterns.md
├── warm/learnings/         # 3-10 次会话
│   └── {namespace}/
├── cold/archive/           # 10+ 次会话
│   └── {namespace}/
├── namespace/              # 命名空间隔离
└── index.jsonl            # 全局索引
```

## 配置

默认配置可在 `scripts/lib/config.sh` 中修改：

- `HOT_RETENTION`: HOT 层保留会话数 (默认 3)
- `WARM_RETENTION`: WARM 层保留会话数 (默认 10)
- `AUTO_UPGRADE_THRESHOLD`: 自动升级阈值 (默认 3)
- `DEFAULT_NAMESPACE`: 默认命名空间 (default)

## 整合说明

本技能整合了以下三个原始技能的功能：

| 原始技能 | 整合功能 |
|----------|----------|
| self-improving-agent | query, detect-pattern, move |
| self-improving | namespace, move, recall |
| mulch | index, query, import |

所有接口已统一为 `unified-self-improving <command>` 格式。

## 版本

- **1.0.3**: 修复代码 bug，更新文档
- **1.0.2**: 添加 ClawHub 链接
- **1.0.1**: 统一 CLI 接口
- **1.0.0**: 初始版本
