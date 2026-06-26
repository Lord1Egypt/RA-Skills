# Memory Manager — 完整技术参考

> 本文档包含完整的技术细节、API 参数、脚本命令。
> 日常使用请参考 `README.md`。

---

## 脚本命令详解

### memory_embed.py — 向量生成

```bash
python scripts/memory_embed.py --uid <用户ID> [选项]

选项:
  --rebuild          # 重建整个向量库
  --list-backends    # 列出支持的 Embedding 后端
  --batch-size <N>   # 批次大小（默认 50）
  --force            # 强制重新生成
```

### memory_search.py — 语义搜索

```bash
python scripts/memory_search.py --uid <用户ID> --query <查询内容> [选项]

选项:
  --method semantic|keyword  # 搜索方法（默认 semantic）
  --top-k <N>                # 返回数量（默认 3）
  --scope private|shared|all # 搜索范围
  --semantic-weight <0-1>   # 语义权重（默认 0.6）
  --rebuild-index            # 重建索引
  --cache-stats              # 显示缓存统计
```

### memory_sync.py — GitHub 同步

```bash
python scripts/memory_sync.py --uid <用户ID> [选项]

选项:
  --strategy rebase|merge  # 同步策略（默认 rebase）
  --push                   # 推送到远程
  --pull                   # 从远程拉取
```

### memory_compress.py — 智能压缩

```bash
python scripts/memory_compress.py --uid <用户ID> [选项]

选项:
  --upgrade    # 升级记忆到更高层级
  --downgrade  # 降级记忆到更低层级
  --aggressive # 激进压缩模式
  --rollback   # 回滚到上一个快照
```

### memory_insight.py — AI 洞察

```bash
python scripts/memory_insight.py --uid <用户ID> [选项]

选项:
  --daily    # 每日洞察
  --weekly   # 每周洞察
  --find-gaps # 发现知识盲点
```

---

## 向量搜索原理

```
用户查询: "我上周学了什么"
       ↓
  Embedding 后端（BGE-M3 / ada-002 / GLM）
       ↓
  生成向量
       ↓
  向量库余弦相似度搜索
       ↓
  综合评分 = 语义相似度 × 0.6 + 重要性评分/100 × 0.4
       ↓
  返回 top-k 最相关记忆 + 关联记忆
```

**Fallback 机制**：向量搜索失败时自动降级到关键词搜索。

---

## GitHub 同步策略

```
rebase 策略（默认）:  拉取远程 → 合并本地 → 推回远程（线性历史）
merge 策略:          拉取远程 → 创建合并提交 → 推回远程（保留分支历史）

建议：
- 单人使用：rebase（历史干净）
- 多人协作：merge（保留分支信息）
```

---

## 安全机制

| 机制 | 说明 |
|------|------|
| Token 安全 | GitHub token 通过 Git Credential Helper 存储 |
| 路径隔离 | `--base-dir` 有安全检查，禁止访问系统关键路径 |
| 向量一致性 | 使用 `content_hash + mtime` 双条件判断增量 |
| 隐私隔离 | 私有记忆严格隔离，仅用户本人可访问 |

---

## 环境变量

```bash
# Embedding 后端
export EMBED_BACKEND=siliconflow   # openai / siliconflow / zhipu

# API Keys
export OPENAI_API_KEY=sk-xxx
export SILICONFLOW_KEY=sk-xxx
export ZHIPU_API_KEY=xxx

# GitHub
export GITHUB_TOKEN=ghp_xxx

# 用户
export MEMORY_USER_ID=用户名
```

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v3.4.0 | 2026-04-04 | 多用户适配：安装脚本、首次引导、依赖管理、OpenClaw 专用安装向导 |
| v3.3.0 | 2026-04-04 | 性能优化：LanceDB HNSW 索引、并行 Embedding、查询缓存 |
| v3.1.0 | 2026-04-03 | Bug 修复、单元测试、OpenClaw 集成说明 |
| v3.0.0 | 2026-04-03 | 关联记忆网络、重要性评分、快照回滚、访问日志 |
| v2.3.0 | 2026-04-03 | 多后端支持、安全修复、增量逻辑修复、WAL 模式 |
| v2.0.0 | 2026-04-03 | 三层记忆架构重构 |
