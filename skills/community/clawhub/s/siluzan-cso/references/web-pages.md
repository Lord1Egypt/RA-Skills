# web-pages — CSO 后台页面速查

> 当需要引导用户前往网页端查看数据或执行操作时，使用本文件中的页面链接。
> URL 格式：`https://www.siluzan.com/v3/foreign_trade/cso/{页面路径}`

---

## 页面速查表

### 账号管理

| 页面     | 完整链接                                                  | 功能说明                                             |
| -------- | --------------------------------------------------------- | ---------------------------------------------------- |
| 账号管理 | `https://www.siluzan.com/v3/foreign_trade/cso/ManageAccounts` | 绑定/授权/查看媒体账号列表、账号状态、Token 到期时间 |
| 账号分组 | `https://www.siluzan.com/v3/foreign_trade/cso/AccountGroup`   | 新建分组、管理分组内账号                             |
| 重点账号 | `https://www.siluzan.com/v3/foreign_trade/cso/KeyAccounts`    | 配置重点关注账号、数据备份                           |

---

### 内容发布

| 页面     | 完整链接                                                           | 功能说明                                                                       |
| -------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| 发布作品 | `https://www.siluzan.com/v3/foreign_trade/cso/postVideo?contentType=1` | 矩阵发布视频、图文、草稿管理、话题组 contentType=1 是视频，contentType=2是图文 |

| 发布日历 | `https://www.siluzan.com/v3/foreign_trade/cso/publishCalendar` | 日历视图规划发布任务、创建/编辑发布任务 |
| 营销日历 | `https://www.siluzan.com/v3/foreign_trade/cso/marketingCalendar` | 营销节点日历、跳转创建发布任务 |

---

### 任务与视频管理

| 页面     | 完整链接                                                | 功能说明                                  |
| -------- | ------------------------------------------------------- | ----------------------------------------- |
| 任务列表 | `https://www.siluzan.com/v3/foreign_trade/cso/task`         | 发布任务列表、状态筛选、任务详情抽屉      |
| 视频管理 | `https://www.siluzan.com/v3/foreign_trade/cso/VideoMgr`     | 已发布视频/图文列表、删除、重发、评论查看 |
| 视频搬家 | `https://www.siluzan.com/v3/foreign_trade/cso/relocation`   | 将视频搬运到其他平台                      |
| 搬家记录 | `https://www.siluzan.com/v3/foreign_trade/cso/MovingRecord` | 搬家任务列表与执行状态                    |

---

### 互动与私信

| 页面     | 完整链接                                               | 功能说明                                |
| -------- | ------------------------------------------------------ | --------------------------------------- |
| 私信管理 | `https://www.siluzan.com/v3/foreign_trade/cso/letter`      | 按渠道/时间查看与处理私信（多平台 Tab） |
| 评论管理 | `https://www.siluzan.com/v3/foreign_trade/cso/comment`     | 收到的评论列表、回复、账号组筛选        |
| 智能互动 | `https://www.siluzan.com/v3/foreign_trade/cso/interaction` | 私信欢迎语、自动回复规则配置            |

---

### 数据与报表

| 页面     | 完整链接                                               | 功能说明                                                             |
| -------- | ------------------------------------------------------ | -------------------------------------------------------------------- |
| 作品数据 | `https://www.siluzan.com/v3/foreign_trade/cso/Workdata`    | 作品维度统计、图表、明细（对应 CLI `report fetch`）                  |
| 账户数据 | `https://www.siluzan.com/v3/foreign_trade/cso/accountdata` | 账户维度汇总数据、趋势图表                                           |
| 绩效报表 | `https://www.siluzan.com/v3/foreign_trade/cso/table`       | 多维度绩效报表、PDF 导出（对应 CLI `report fetch/records/download`） |

---

### AI 与内容工具

| 页面     | 完整链接                                               | 功能说明                                                       |
| -------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| 内容规划 | `https://www.siluzan.com/v3/foreign_trade/cso/planning`    | AI 内容规划列表、生成规划、企业维度筛选（对应 CLI `planning`） |
| 营销首页 | `https://www.siluzan.com/v3/foreign_trade/cso/ContentHome` | 工作台总览：账号数、视频数、最新评论与视频                     |

| 话题组 | `https://www.siluzan.com/v3/foreign_trade/cso/TopicGroup` | 话题组维护、话题内容管理 |
| 知识库 | `https://www.siluzan.com/knowledge-base/` | 知识库管理、编辑及查询 |

---

## CLI 命令与页面对应关系

| CLI 命令                  | 对应后台页面            |
| ------------------------- | ----------------------- |
| `list-accounts`           | `ManageAccounts`        |
| `authorize`               | `ManageAccounts`        |
| `account-group`           | `AccountGroup`          |
| `publish`                 | `postVideo`、`task`     |
| `task list/detail`        | `task`                  |
| `task comment list`       | `comment`               |
| `letter`                  | `letter`                |
| `report fetch`            | `Workdata`、`table`     |
| `report records/download` | `table`（导出记录弹窗） |
| `planning`                | `planning`              |
| `upload`                  | `postVideo`（素材库）   |
