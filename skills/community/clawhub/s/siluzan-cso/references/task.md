# task — 发布任务管理

> 发布提交后，用本命令查看任务状态、处理失败项、管理任务生命周期。

---

## 常用场景速查

| 用户问                       | 命令                                                        |
| ---------------------------- | ----------------------------------------------------------- |
| 发出去了吗？/ 查看发布记录   | `siluzan-cso task list`                                     |
| 只看失败的任务               | `siluzan-cso task list --failed-only`                       |
| 查近一周的任务               | `siluzan-cso task list --date-preset week`                  |
| 查某个任务每个账号的发布结果 | `siluzan-cso task detail --publish-id <id>`                 |
| 对失败项重试                 | `siluzan-cso task item republish --item-id <id>`            |
| 立即发布某个定时项           | `siluzan-cso task item run-now --item-id <id>`              |
| 中止任务                     | `siluzan-cso task stop --publish-id <id>`                   |
| 删除任务                     | `siluzan-cso task delete --publish-id <id>`                 |
| 重命名任务                   | `siluzan-cso task rename --publish-id <id> --name <新名称>` |

---

## task list — 任务列表

```bash
# 默认：最新 10 条
siluzan-cso task list

# 只看异常任务（找失败原因）
siluzan-cso task list --failed-only

# 按时间范围筛选
siluzan-cso task list --date-preset week     # 近一周
siluzan-cso task list --date-preset month    # 近一个月
siluzan-cso task list --start-date 2026-01-01 --end-date 2026-03-31

# 按内容类型筛选
siluzan-cso task list --content-type video
siluzan-cso task list --content-type image-text

# 按状态筛选
siluzan-cso task list --status 0   # 执行中
siluzan-cso task list --status 1   # 已完成

# 按任务名搜索
siluzan-cso task list --keyword "任务名关键词"

# 落盘完整数据（适合脚本），脚本读盘见 references/core/tips.md
siluzan-cso task list --json-out ./snap-cso
```

**任务状态（`status`）：**

| 值  | 显示   | 含义               |
| --- | ------ | ------------------ |
| 0   | 执行中 | 任务正在发布       |
| 1   | 已完成 | 所有发布项处理完毕 |
| 2   | 已中止 | 任务被手动中止     |

---

## task detail — 任务详情

```bash
# 查看某个任务每个账号的发布结果（publish-id 来自 task list 输出）
siluzan-cso task detail --publish-id <任务ID>

# 按平台过滤
siluzan-cso task detail --publish-id <id> --media YouTube
```

**发布项状态：**

| 状态     | 含义             | videoStatus |
| -------- | ---------------- | ----------- |
| 发布中   | 正在发布到该平台 | 0或10       |
| 已发布   | 成功             | 1           |
| 定时发布 | 等待到达设定时间 | 9           |
| 发布失败 | 失败，可重试     | 3           |

---

## 处理发布失败

```bash
# Step 1：找出有异常的任务
siluzan-cso task list --failed-only

# Step 2：查看具体哪个账号/平台失败
siluzan-cso task detail --publish-id <任务ID>

# Step 3：重试失败的发布项（item-id 来自 task detail 输出）
siluzan-cso task item republish --item-id <发布项ID>
```

**常见失败原因：**

- Token 已失效 → 重新授权该账号（参见 `references/authorize.md`）
- 视频格式不符合平台要求 → 检查视频规格
- 标题超出平台字数限制 → 用 `platformOverrides` 给该平台定制更短的标题（参见 `references/publish.md`）
- 定时时间已过去 → 修改时间后重新提交

---

## 交叉引用

- 提交发布后查看状态 → 本文件（从 `references/publish.md` Step 8 跳转至此）
- Token 失效处理 → 参见 `references/authorize.md`
- 重新提交新任务 → 参见 `references/publish.md`
