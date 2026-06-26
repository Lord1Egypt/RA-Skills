# Consolidation 脚本配置指南

## 核心功能

consolidation 脚本在每次心跳后自动运行，执行以下模块：

### [A] 观察合并
检测重复的 subject+predicate 三元组：
- 如果新版本有更新的 `valid_from` 日期，保留新版本
- 旧版本自动标记为 expired
- 避免 KG 膨胀

### [C] 访问统计
- 每次心跳查询 KG 实体时，记录访问时间戳
- 存储在 `.access_stats.json`（自动创建）
- 后续检索优先返回热点实体

### [D] 偏差检测
扫描记忆文件（MEMORY.md / HEARTBEAT.md）中的关键词：
- "忘了" / "没做" / "应该" / "忘记" 等
- 检测到后自动追加到 SHADOW.md
- 格式：`YYYY-MM-DD | 检测到关键词 | 来源文件 | 建议检查`

### [R] 路由发现
- 检测 workspace 中新增的 `.md` 文件
- 与当前路由表（`记忆路由表.md`）对比
- 新文件追加为"待确认"条目

## 运行方式

```bash
python3 scripts/mempalace_consolidation.py
```

建议在 HEARTBEAT.md 中配置为每次心跳自动执行。

## 文件位置

- 主脚本：`workspace/scripts/mempalace_consolidation.py`
- 访问统计：`workspace/scripts/.access_stats.json`（自动创建）
- SHADOW.md：`成长箱/.learnings/SHADOW.md`