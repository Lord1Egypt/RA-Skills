# 📚 摇摇记忆系统 - 高级配置指南

> 面向进阶用户的技术配置参考

---

## 📁 目录结构

```
~/.openclaw/
├── memory-tdai/              # 记忆数据库
│   ├── vectors.db           # SQLite 数据库
│   └── .cache/              # 缓存目录
│       ├── embeddings/      # Embedding 缓存
│       └── precomputed.json # 预计算向量
├── workspace/
│   ├── skills/yaoyao-memory-v2/
│   │   ├── scripts/        # 功能脚本 (101个)
│   │   ├── core/           # 核心模块
│   │   └── config/         # 配置文件
│   └── memory/             # 记忆文件
│       └── *.md            # 每日记忆
└── credentials/
    └── secrets.env         # 敏感凭证
```

---

## 🔧 配置管理

### 查看配置

```bash
# 查看所有配置
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/config_manager.py list

# 查看特定配置
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/config_manager.py get memory.vector_search
```

### 修改配置

```bash
# 启用/禁用功能
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/config_manager.py enable memory.vector_search
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/config_manager.py disable memory.vector_search
```

---

## 🧪 健康检测

### 运行健康检查

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/health_check.py
```

### 自动修复

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/auto_fixer.py fix
```

---

## ⚡ 性能优化

### 缓存预热（首次查询加速）

```bash
# 预热常用查询
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/warmup.py

# 仅查看计划
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/warmup.py --dry-run
```

### 性能基准测试

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/benchmark.py
```

### 向量系统优化

```bash
# 检查向量扩展
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/vector_extension_manager.py status

# 查找扩展
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/vector_extension_manager.py find
```

---

## 🔐 安全扩展加载

### 检查扩展哈希

```bash
# 列出可用扩展
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/safe_extension_loader.py --list

# 验证扩展
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/safe_extension_loader.py --check vec0
```

---

## 🗄️ 数据管理

### 导出记忆

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/memory_exporter.py export --format json
```

### 清理过期数据

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/cleanup.py --dry-run
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/cleanup.py  # 确认后执行
```

---

## ☁️ 云同步

### IMA 同步

```bash
# 手动同步
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/sync_ima.py sync

# 查看同步状态
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/sync_ima.py status
```

### Samba 同步

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/sync_samba.py sync
```

---

## 📊 统计分析

### 记忆统计

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/memory_stats.py
```

### 可视化面板

```bash
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/stats_dashboard.py
```

---

## 🔄 开发流程

### 版本结构

| 目录 | 用途 |
|------|------|
| `yaoyao-memory-v2` | 开发版 |
| `yaoyao-memory-homo` | 生产版 |

### 同步命令

```bash
# 开发版 → 生产版
rsync -av --exclude=__pycache__ \
  ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/ \
  ~/.openclaw/workspace/skills/yaoyao-memory-homo/scripts/

rsync -av --exclude=__pycache__ \
  ~/.openclaw/workspace/skills/yaoyao-memory-v2/core/ \
  ~/.openclaw/workspace/skills/yaoyao-memory-homo/core/
```

---

## 🐛 故障排查

### Embedding API 失败

1. 检查 API Key 配置
   ```bash
   grep -i "embedding" ~/.openclaw/workspace/skills/yaoyao-memory-v2/config/llm_config.json
   ```

2. 测试 API 连通性
   ```bash
   curl -X POST "https://ai.gitee.com/v1/embeddings" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '{"input":"test","model":"Qwen3-Embedding-8B"}'
   ```

3. 重启 Gateway
   ```bash
   openclaw gateway restart
   ```

### 数据库损坏

```bash
# 运行自修复
python3 ~/.openclaw/workspace/skills/yaoyao-memory-v2/scripts/auto_fixer.py fix --all
```

---

## 📋 功能清单

完整功能清单请查看 [FUNCTIONS.md](./FUNCTIONS.md)

---

*最后更新：2026-04-12*
