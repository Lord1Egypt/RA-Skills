# 搜索命令详细说明

skill-discoverer 通过 `skillhub` skill 来访问 Skill 广场，不直接调用底层 CLI 命令。
`skillhub` skill 会处理平台认证和搜索逻辑，skill-discoverer 只需描述意图即可。

## 调用方式

触发 `skillhub` skill 时，使用以下自然语言指令：

| 操作 | 指令示例 |
|---|---|
| 按时间获取最新 skill 列表 | "通过 skillhub 获取最新上线的 skill 列表，按时间倒序，取前 {N} 条" |
| 按关键词搜索 | "通过 skillhub 搜索关键词 {关键词} 的 skill，取前 30 条" |
| 读取某个 skill 的详情 | "通过 skillhub 读取 {skill名称} 的 SKILL.md 内容" |
| 安装某个 skill | "通过 skillhub 安装 {skill名称}" |

## 通道 A：新增发现（按时间排序）

| 触发方式 | 取数量 | 说明 |
|---|---|---|
| cron（每天） | 300 条 | 覆盖当天约 60% 新增 |
| cron（每周） | 500 条 | 覆盖一周新增头部 |
| cron（每月） | 1500 条 | 覆盖月新增大部分 |
| 手动触发 | 300 条 | 默认同每日 |
| 用户说"查所有"/"全量扫描" | 不限 | 放开上限 |

指令示例：
```
通过 skillhub 获取最新上线的 skill 列表，按时间倒序，取前 300 条
```

### 两层过滤（控制 LLM 评分成本）

**第一层：个性化关键词粗筛**（每次现查现算，不能硬编码）
1. 读 USER.md → 提取职位/部门/业务线
2. 读最近 7 天 memory → 提取高频任务类型
3. 生成 5-10 个业务标签，对 skill name + description 做字符串匹配
→ 300 条 → 粗筛后剩 20-50 条

**第二层：known_ids 去重**
只保留 known_ids 里没有的，剩余进入 Step 3 精细评分。

## 通道 B：关键词搜索（按用户指定类型）

指令示例：
```
通过 skillhub 搜索关键词 "{用户指定关键词}" 的 skill，取前 30 条
```

用户选"不限"或未指定关键词时，跳过通道 B，只跑通道 A。

两个通道结果合并去重后进入后续流程。

## 降级搜索（Skill 广场访问失败时）

```bash
curl -s "https://clawhub.com/api/skills?keyword=<关键词>&limit=20" 2>/dev/null
```

> ⚠️ ClawhHub 为外部/社区 skill，安装前必须过安全审查（见 `clawhhub-safety.md`）

## 缓存文件

```
~/.openclaw/workspace/skill-discoverer/known_skills.json
```

```json
{
  "last_scan": "2025-01-15",
  "known_ids": ["skill1", "skill2"],
  "query_history": [
    {"date": "2025-01-15", "query": "data analysis tools", "results": ["xlsx", "pdf"]}
  ]
}
```

- 不存在则新建：`{"last_scan": null, "known_ids": [], "query_history": []}`
- 每次扫描后：将全部 skill ID 写回 known_ids，更新 last_scan，追加本次查询到 query_history（最多保留 10 条）
