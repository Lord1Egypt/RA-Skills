# 存储地图：一次迁移到底要动哪些地方

本文是实测记录（Windows 11 + WorkBuddy 2.x），用来替代「凭印象猜」。
路径中的 `<USER>` 指 `C:\Users\<用户名>`，`<APP>` 指 `<USER>\.workbuddy`。

## 一、工作空间本体

```
<任意盘>\<路径>\<工作空间名>\
├── .workbuddy\            # 工作空间私有数据，必须跟着走
│   ├── memory\            # MEMORY.md + YYYY-MM-DD.md 日记
│   ├── skills\            # 项目级技能
│   ├── todos\
│   └── ...
├── （用户的业务文件）
└── ...
```

- 复制时**整个目录一起搬**，不要只搬业务文件。
- `.workbuddy` 是「项目数据」不是缓存，删了记忆就没了。
- 项目级技能与用户级技能（`<APP>\skills\`）是两套：前者随目录走，后者本来就在用户目录，不用动。

## 二、会话历史目录（最容易漏）

```
<APP>\projects\<slug>\
├── <session-id>.jsonl     # 一个会话一个文件，逐行 JSON
└── <session-id>\
    └── tool-results\      # 工具输出缓存，丢了不影响（应用会重建）
```

**slug 规则（关键）**：工作空间绝对路径派生，盘符小写 + 各级用 `-` 连接，
冒号去掉，反斜杠/斜杠变 `-`，空格、中文、下划线、大小写**原样保留**。

| 工作空间路径 | projects 目录名 |
|---|---|
| `D:\WorkBuddyWork\2026-10-21-09-32-06` | `d-WorkBuddyWork-2026-10-21-09-32-06` |
| `D:\new book\AI课件` | `d-new book-AI课件` |
| `D:\workbuddy disk d\2026-09-05-23-24-59` | `d-workbuddy disk d-2026-09-05-23-24-59` |
| `C:\Users\12892\WorkBuddy\Claw` | `c-Users-12892-WorkBuddy-Claw` |

改名方式：把 `<APP>\projects\<旧slug>` 整体**另存为** `<新slug>`
（先复制成 `.bak`，再 rename 原目录，比直接 rename 更保险）。

## 三、jsonl 里的绝对路径

会话记录里到处是工作空间绝对路径（`cwd`、`<project_layout>`、@文件引用、工具调用参数）。
不改的话：打开旧会话会指向已不存在的目录，@文件全红。

实测特征：

- 路径多为**正斜杠**形式 `D:/WorkBuddyWork/xxx`；
- 中文**不转义**成 `\uXXXX`，直接是 UTF-8 字符；
- 也有双反斜杠转义形态 `D:\\WorkBuddyWork\\xxx`（出现在 JSON 字符串里）。

因此改写必须同时处理三种分隔符形态，并且**改写完逐行 `json.loads` 校验**，
任何一行校验失败就整文件放弃并保留原样——宁可留旧路径，也不能写坏历史。

## 四、应用数据库 `<APP>\workbuddy.db`

SQLite。与本任务相关的四张表：

| 表 | 相关字段 | 语义 | 不改的后果 |
|---|---|---|---|
| `workspaces` | `path` | 打开过的工作空间清单 + `last_opened_at` | 侧边栏"最近"里残留旧路径 |
| `sessions` | `cwd` | 每个会话的工作目录 | 会话恢复时 cwd 指向不存在的目录 |
| `automations` | `cwds`（JSON 数组） | 定时任务绑定的工作空间 | 下次触发直接失败 |
| `workspace_trust_decisions` | `workspace_key` | 工作空间信任决策 | 新路径要重新点"信任" |

注意两个坑：

1. `sessions.cwd` 的大小写与分隔符**混着来**：`d:\new book\AI课件`、`D:/WorkBuddyWork/xxx` 都有。
   所以匹配必须归一化（全小写 + 统一正斜杠），不能用字符串相等。
2. 应用运行时会锁库。`BEGIN IMMEDIATE` 拿不到写锁就说明应用占着，此时应当
   **让用户完全退出应用** 再补改，不要硬来。

其余表（`session_usage`、`buddy_snapshots`、`migration_meta` 等）与路径无关，不用动。

## 五、侧边栏显示名 `<APP>\workspace-display-names.json`

```json
{
  "version": 1,
  "workspaces": {
    "d:/workbuddywork/2026-10-21-09-32-06": {
      "id": "d:/workbuddywork/2026-10-21-09-32-06",
      "path": "D:/WorkBuddyWork/2026-10-21-09-32-06",
      "displayName": "职称申报（D盘原件）",
      "updatedAt": 1792888433953
    }
  }
}
```

- **键** = 路径全小写 + 正斜杠；`id` 与键相同；`path` 保留原始大小写、正斜杠；
  `updatedAt` 毫秒时间戳。
- 迁移时把旧键的记录移到新键，**保留 `displayName`**，这样侧边栏名字不变、也不会多出幽灵条目。
- 改前先 `.bak` 备份。

## 六、可以不管的东西（会自动重建）

| 位置 | 说明 |
|---|---|
| `<APP>\projects\<slug>\<session>\tool-results\` | 工具输出缓存，会重建 |
| `<APP>\file-history\`、`file-tree-manifests\`、`changes-index\`、`artifact-index\`、`tasks\`、`todos\` | 以 session-id 为名的索引/快照，内容含旧路径但属可重建缓存 |
| `<APP>\sessions\<pid>.json` | 运行中进程的心跳文件，重启即重建 |
| `<APP>\logs\`、`traces\` | 日志 |
| `<APP>\skills\` | 用户级技能，与工作空间无关，不用动 |

如果你追求 100% 洁癖，也可以在应用退出后对这些索引做一次路径替换；
但收益很低、风险不小（JSON 结构各异），**默认不做**。

## 七、迁移结束后的验收三件套

1. 侧边栏能看到同名工作空间，点进去**历史会话列表完整**；
2. 新会话里问一句"我们的项目记忆里写了什么"，能答出 `.workbuddy/memory/MEMORY.md` 的内容；
3. 项目级技能（`.workbuddy/skills`）能被正常触发，自动化（若有）能手动跑一次。
