# Subagent Distiller v3.0 - 生产级记忆蒸馏系统

**一句话介绍**：自动增量提取对话中的结构化知识，过滤垃圾，动态聚类，专注长期价值。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **增量扫描** | Cursor 机制，只处理新增对话，99% 节省 |
| **实时结构化** | 边提取边整理，直接输出精炼格式 |
| **智能过滤** | 体育分析、市场预测、临时新闻 → 直接丢弃 |
| **动态聚类** | 自动发现域（Polymarket/OpenClaw/...），非固定分类 |
| **状态追踪** | RESOLVED/PENDING/ABANDONED，待办自动提醒 |

---

## 安装

```bash
# 通过 ClawHub 安装
clawhub install subagent-distiller

# 或手动安装
git clone https://github.com/yourname/subagent-distiller.git ~/.openclaw/workspace/skills/subagent-distiller
```

---

## 快速开始

### 1. 初始化（首次运行）
```bash
cd ~/.openclaw/workspace/skills/subagent-distiller
python3 incremental_slice.py    # 扫描历史对话
python3 realtime_distill.py     # 提取结构化知识
```

### 2. 每日自动运行（推荐）
```bash
# 添加到 crontab
crontab -e

# 凌晨 3:00 增量提取
0 3 * * * cd ~/.openclaw/workspace/skills/subagent-distiller && python3 incremental_slice.py && python3 realtime_distill.py

# 早上 9:00 待办提醒
0 9 * * * cd ~/.openclaw/workspace/skills/subagent-distiller && python3 lifecycle_manager.py
```

### 3. 每周域聚合（手动）
```bash
python3 domain_consolidate.py   # 自动发现域，生成专书
```

---

## 文件结构

```
subagent-distiller/
├── SKILL.md                          # 本文档
├── incremental_slice.py              # 增量扫描器（cursor 机制）
├── realtime_distill.py               # 实时结构化提取
├── domain_consolidate.py             # 动态域聚合
├── lifecycle_manager.py              # 生命周期管理（待办提醒）
├── bulk_cleanup.py                   # 批量清理工具
├── chunks/                           # 切片缓存（自动生成）
├── cursors/                          # 游标记录（自动生成）
└── state.json                        # 处理状态（自动生成）
```

---

## 配置

### 过滤规则（可自定义）

编辑 `realtime_distill.py` 中的 `get_prompt()` 函数：

```python
# 默认丢弃：
- 体育比赛分析（球队胜率、比分预测）
- 具体市场预测（"X市场胜率62%"、当日赔率）
- 临时新闻解读（时效性<7天）
- 无结论探索（只有"试试"没有结果）
- 寒暄废话（"在吗"、"测试"）
- 内容污染（"我看到..."等内部思考）

# 默认保留：
- 架构设计、系统方案
- 避坑指南、故障解决
- 配置沉淀、环境搭建
- 原则/铁律、SOP流程
```

### 域聚类规则（自动）

```python
# 自动从卡片名提取前缀作为域
polymarket_trading_logic.md → Polymarket/
openclaw_config_setup.md    → Openclaw/
bitcoin_wallet_security.md  → Bitcoin/  # 自动创建新域
```

---

## 输出格式

### 知识卡片（自动生成的 .md 文件）

```markdown
---
topic: "主题名称"
status: RESOLVED | PENDING | ABANDONED
created: 2026-03-05
updated: 2026-03-06
source: session_id.jsonl Line 100-200
---

# 🏷️ 主题：xxx

## 核心摘要
一句话总结

## 最新结论 / 成功方案
- 最终方案
- 关键决策

## 避坑指南
- ❌ 废弃尝试及原因
- ⚠️ 关键陷阱

## 待办事项（仅 PENDING）
- [ ] 待验证...
- [ ] 待决策...

## 历史溯源
- session_id.jsonl Line 100-200
```

### 域专书（每周聚合生成）

```
memory/domains/
├── Polymarket.md      # 交易代码、架构设计
├── Openclaw.md        # 配置、子代理模式
├── Research.md        # 科研相关
└── System.md          # 通用知识
```

---

## 工作原理

```
对话会话 (.jsonl)
    │
    ▼
incremental_slice.py    ← 只读新增行（cursor 记录位置）
    │
    ▼
realtime_distill.py     ← 子代理提取，垃圾直接丢弃
    │                        ├── 状态标记
    │                        └── 精炼格式输出
    │
    ▼
lifecycle_manager.py    ← 每日检查 PENDING 超时
    │
    ▼
domain_consolidate.py   ← 每周聚合，动态发现域
```

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `python3 incremental_slice.py` | 增量扫描，生成切片 |
| `python3 realtime_distill.py` | 生成提取任务清单 |
| `python3 lifecycle_manager.py` | 检查待办，生成提醒报告 |
| `python3 domain_consolidate.py` | 域聚合，生成专书 |
| `python3 bulk_cleanup.py` | 批量清理现有卡片 |
| `python3 lifecycle_manager.py --list-pending` | 列出所有待办 |

---

## 故障排查

### Q: 切片为空？
```bash
# 检查 cursor 文件
ls cursors/
# 删除后重新扫描
rm cursors/*.cursor && python3 incremental_slice.py
```

### Q: 提取结果不理想？
```bash
# 调整提示词
vim realtime_distill.py  # 修改 get_prompt() 函数
```

### Q: 如何彻底重置？
```bash
# 清空所有状态
rm -rf chunks/* cursors/* state.json slice_summary.json
python3 incremental_slice.py
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.0 | 2026-03-06 | 增量扫描、实时结构化、动态域、智能过滤 |
| v2.0 | 2026-03-05 | 夜间自动蒸馏、hook 拦截器 |
| v1.0 | 2026-03-04 | 基础切片提取 |

---

## 作者

- **作者**: OpenClaw Community
- **许可证**: MIT
- **仓库**: https://github.com/openclaw/subagent-distiller

---

**一句话**: 让 AI 助手拥有真正的长期记忆，只记住有价值的东西。