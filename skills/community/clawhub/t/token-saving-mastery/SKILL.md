---
name: token-saving-mastery
description: 节省 Token 的实战技巧 — 优化 AI 对话成本，提升性价比
category: productivity
---

# Token 节省大师 | Token-Saving Mastery

通过 4 大策略显著降低 AI 对话 Token 消耗，节省 30-70% 成本。

## 技能列表

### 1. 用 session_search 控制上下文 | session_search Context Control
**难度：** ⭐ 低

**原理：** AI 历史越长，消耗越多。只加载相关的记忆片段而非全部历史。

**操作步骤：**
```
1. 对话开始时，先调用 session_search 搜索关键词
2. 找到相关上下文后，整理成摘要注入对话
3. 让 AI 基于摘要继续，而非完整历史
```

**适用场景：** 多项目并行、长期开发、跨 session 协作

---

### 2. 减少技能文件体积 | Trim Skill File Bloat
**难度：** ⭐⭐ 中

**原理：** 每个 skill 的 system prompt 都会被加载，太大浪费。

**操作步骤：**
```
1. 用 skills_list 列出所有技能
2. 检查每个 skill 的 SKILL.md 体积
3. 删除以下内容：
   - 冗余的示例代码（保留 1-2 个即可）
   - 过时的 API 版本说明
   - 重复的步骤描述
   - 不常用的参考资料
4. 用 skill_view(name) 检查实际使用的行数
5. 用 skill_manage patch 精简
```

**参考体积：** 一个精简的 skill 应在 2-5KB 之间

---

### 3. 定期清理 session | Periodic Session Cleanup
**难度：** ⭐ 低

**原理：** session_history 无限累计，每次新建都会加载。

**操作步骤：**
```
1. 每周/每月运行一次 session 清理
2. 用 session_search 搜索关键项目名
3. 导出重要对话到外部笔记（Obsidian/Notion）
4. 标记不重要 session 为归档
5. 设置 cron 任务自动归档超过 30 天的 session
```

**Cron 示例：**
```
hermes cron create \
  --name "Session Cleanup" \
  --prompt "归档 30 天前的 session，保留最近 10 个" \
  --schedule "0 2 * * 0" \
  --skills "session_search"
```

---

### 4. Cron 任务用轻量 prompt | Lightweight Cron Prompts
**难度：** ⭐ 低

**原理：** Cron 任务在后台运行，不需要花哨的引导语和示例。

**操作步骤：**
```
1. 写 cron prompt 时遵守：
   - 直接说任务，不写"你是一个专业的..."
   - 不要示例，一个都不要
   - 结论导向："输出 X，返回 Y"
   - 限制输出长度："不超过 100 字"
2. 关联 skills 而非把知识写进 prompt
3. 避免多轮对话，用单次完成的任务
```

**对比：**

❌ 浪费写法：
```
你是一个专业的数据分析师，请帮我分析销售数据...
（200字引导 + 3个示例 + 200字总结要求）
```

✅ 节省写法：
```
分析附件 sales.csv，按地区统计月销售额，输出 TOP3 地区。
```

---

## 效果预估

| 策略 | 节省比例 | 实施难度 |
|------|---------|---------|
| session_search 控制 | 20-40% | ⭐ |
| 精简技能文件 | 10-20% | ⭐⭐ |
| 定期清理 session | 15-30% | ⭐ |
| 轻量 cron prompt | 10-25% | ⭐ |

**综合节省：30-70%**

---

## 变现路径

1. **ClawHub 技能市场** — 上传本技能，设置付费下载
2. **定制优化服务** — 按小时收费帮用户优化 Token 使用
3. **企业内部培训** — 打包成教程卖给团队
4. **API 成本顾问** — 帮开发者分析并优化 AI 调用成本

---

## 验证步骤

完成设置后，运行：
```
hermes session list | wc -l  # 查看 session 数量
hermes skills list | wc -l   # 查看技能数量
```

对比优化前后的 API 调用账单，验证节省效果。
