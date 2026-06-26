# Viking Memory System Ultra v1.3.0

> **Viking 记忆系统** - OpenClaw 的分层记忆基座，解决"记忆太多无法高效检索"的根本矛盾。

## 🏠 系统概述

Viking Memory System Ultra 是一个企业级的记忆管理系统，提供：
- **分层记忆**: hot → warm → cold → archive 四层架构
- **动态回流**: 语义相似度驱动的冷记忆自动晋升
- **智能权重**: 对数增长 + 上下文相关性，防止"老记忆霸权"
- **可逆归档**: 多粒度摘要 + 按需解压恢复

## 📦 安装

```bash
# 方法 1: 使用 ClawHub CLI
clawhub install viking-memory-ultra

# 方法 2: 手动安装
git clone <repo_url>
cd viking-memory-ultra
bash install.sh
```

## 🚀 快速开始

### 1. 写入记忆
```bash
sv_write "agent/memories/hot/2026-03-28-重要发现.md" "# 内容" --importance high
```

### 2. 读取记忆
```bash
sv_read "agent/memories/hot/2026-03-28-重要发现.md"
```

### 3. 搜索记忆
```bash
sv_find "关键词" --layer hot
```

### 4. 自动加载
```bash
sv_autoload.sh --limit 5 --promote
```

## 📊 版本历史

### v1.3.0 (Ultra)
- Phase 1: 动态回流机制
- Phase 2: 权重公式优化
- Phase 3: Archive 可逆性

### v1.2
- 权重公式优化（对数增长）

### v1.1
- 动态回流机制

## 📖 文档
- 完整文档：`SKILL.md`
- 示例：`examples/` 目录

## 🤝 贡献
欢迎提交 Issue 和 PR！
