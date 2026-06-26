---
name: skill-router
description: "技能路由枢纽 — 解决80+技能导致OpenClaw变笨的问题。按场景分桶，每次只激活Top3相关技能，防止路由成本过高。学习历史路由记录，失败的技能自动降权。ano原创架构。"
metadata:
  {
    "openclaw": { "emoji": "🧭" }
  }
---

# 🧭 技能路由枢纽

**核心问题**：技能太多 → 路由成本高 → 选错技能 → OpenClaw变笨

**解决方案**：场景分桶 + 智能路由 + 失败学习

---

## 核心问题：为什么技能太多反而变笨

当OpenClaw有80+技能时：
- 每个请求都要在80个里选 → 决策成本高
- 路由错误率上升 → 选到不相关的技能
- 相关技能被稀释 → 真正需要的反而没被激活

---

## 架构设计

### 三步路由

```
用户请求 → 场景识别 → 桶内选Top3 → 激活技能
```

### 场景分桶

| 桶（场景）| 核心技能 | Top3 |
|-----------|---------|------|
| 学术研究 | sci-paper-three-pass / literature-review | 三刀精修 / 文献搜索 / 论文摘要 |
| AI自我进化 | self-model / idle-learning / ai-consciousness-core | 自我建模 / 持续学习 / 置信度 |
| 内容创作 | openclaw-novel-pipeline / caveman | 小说流水线 / 输出压缩 |
| 短视频运营 | douyin-operations / xiaohongshu | 抖音运营 / 小红书 |
| 代码开发 | coding-agent / cloudbase / github | 代码开发 / 建站 / GitHub |
| 图片处理 | baoyu-compress-image / baoyu-infographic | 图片压缩 / 信息图 |
| 搜索查询 | find-skills / minimax-web-search | 技能搜索 / 网页搜索 |
| 总结汇报 | summarize-pro | 总结摘要 |

**每次只激活相关桶内的Top3技能，其他技能静默。**

---

## 失败学习机制

```
路由到技能A → 执行 → 失败/不好用
     ↓
记录失败 → 下次这个场景换技能B
```

- 每个场景维护一个"历史成功列表"
- 成功过的技能优先
- 失败的技能自动降权

---

## 使用方式

### 路由API

```python
from router import route, log_routing

result = route("ano想发一篇SCI论文")
# {'scene': '学术研究', 'selected_skills': ['sci-paper-three-pass', 'literature-review', ...], 'reason': '场景「学术研究」桶内Top3'}

# 任务完成后标记结果
log_routing("ano想发一篇SCI论文", "学术研究", result['selected_skills'], outcome="success")
```

### 手动路由

```bash
python3 /root/.openclaw/workspace/skills/skill-router/router.py "ano想精修论文"
```

### 查看路由历史

```bash
python3 /root/.openclaw/workspace/skills/skill-router/router.py "查路由" --learn
```

---

## 关键文件

```
skill-router/
  router.py         # 路由核心逻辑
  routing_log.jsonl # 路由历史（成功/失败）
  skill_buckets.json # 场景桶配置
```

---

## 与skill-recommender的关系

- `skill-recommender`：基于关键词的推荐，返回Top5
- `skill-router`：基于场景桶的路由，每次只激活Top3

**两者配合**：Router确定桶和Top3 → Recommender在Top3内精确匹配

---

_技能版本: v1.0.0_  
_基于: ano原创skill-router架构_  
_创建时间: 2026-05-02_
