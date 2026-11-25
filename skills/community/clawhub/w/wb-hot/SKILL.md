---
name: wb-hot
slug: wb-hot-list
displayName: 微博热榜采集
version: 1.0.0
description: 微博实时热榜采集工具。当用户需要获取当前微博热搜/热榜、热搜排名、热度值、话题链接，或导出微博热榜 CSV，或提到"微博热榜/微博热搜/热搜榜单/热点采集/热榜导出"时使用本 skill。服务端直接通过 HTTP 请求采集公开热榜，不需要微博登录态、微博 Cookie 或内网浏览器节点；每次采集 1 点数，失败全额返还。
---

# 微博热榜采集 Skill（wb-hot）

封装「社媒采集平台」（FastAPI，`/api/v1`）的零依赖 Node CLI。提交任务后，**服务端直接通过 HTTP** 请求微博公开热榜接口，返回实时榜单；无需用户打开浏览器，也无需微博登录。

- **能采什么**：排名（`rank`）、热搜标题（`title`）、关键词（`keyword`）、热度值（`hot_value`）、标签（`label`）、分类（`category`）、微博搜索链接（`url`）。
- **采集范围**：一次返回接口当前提供的完整实时热榜（通常约 50 条），不是只取前 5 条；广告项会过滤。
- **收费**：**每次采集 = 1 点数**，注册送 10 点；失败或零结果全额返还。
- **无需微博登录态**：不读取、不保存微博 Cookie，不依赖内网采集节点。
- 客户端零 npm 依赖，Node.js ≥ 18；stdout 纯 JSON，进度走 stderr。

## 收费价格

- **点数换算：0.1 元 = 1 点数。**

## 客服支持

- 客服微信（扫码添加）：http://st.aidata366.com/assets/concat.png
- 客服电话：**18722121663**

## 前置条件

采集本身不需要微博账号，但平台任务接口需要平台账号和点数：

1. 首次使用执行 `node cli.js register --link`（新用户）或 `node cli.js login --link`（已有账号）。
2. 把 stderr 中的注册/登录引导**原样发给用户**；用户完成后执行对应的 `--check --access-token "<串>"`。
3. token 保存于 `~/.xhs-platform/config.json`，与其他社媒 skill 共用账号体系；不要泄露或提交 git。
4. 默认后端为 `http://st.aidata366.com`，可执行 `node cli.js config set base-url <url>` 修改。默认地址为明文 HTTP，token 会明文传输；条件允许时切换 HTTPS。

## 命令

### version / quota / logout / config

```bash
node cli.js version
node cli.js quota
node cli.js logout
node cli.js config show
node cli.js config set base-url http://127.0.0.1:8084
```

`version` 输出：

```json
{"ok":true,"data":{"name":"wb-hot","version":"1.0.0","capability":"wb_hot"}}
```

### submit — 采集当前热榜

```bash
node cli.js submit --wait
node cli.js submit --wait --force   # 24h 内已采过，也要重新获取最新榜单
```

- 不需要关键词、链接或条数参数。
- 每次预扣 1 点；`--wait` 默认最多等待 120 秒。
- 同一空参数任务 24h 内默认去重；需要再次获取最新榜单时使用 `--force`。
- 可选 `--interval <秒>`、`--timeout <秒>` 调整轮询。

成功结果示例（数组仅示意一条，实际返回完整热榜）：

```json
{"ok":true,"data":{"task_id":"t_20261029_67c73013","status":"done","success_count":1,
 "items":[{"id":"1","status":"success","result":{"collected_count":51,
 "fetched_at":"2026-10-29 15:30:00","hot_list":[{"rank":1,"title":"#示例热搜#",
 "keyword":"示例热搜","hot_value":1108681,"label":"热","category":"社会",
 "url":"https://s.weibo.com/weibo?q=%23%E7%A4%BA%E4%BE%8B%E7%83%AD%E6%90%9C%23"}]}}]}}
```

Agent 应读取 `data.items[0].result.hot_list` 整理结果，并按 `collected_count` 如实汇报条数。

### query — 查询任务 / 拉取热榜

```bash
node cli.js query <task_id>
node cli.js query <task_id> --wait
```

### export — 导出 CSV

```bash
node cli.js export <task_id> --wait --out 微博热榜.csv
```

CSV 带 BOM，Excel 可直接打开；包含任务汇总与热榜明细（排名、标题、关键词、热度、标签、分类、链接）。

## 典型工作流

1. 用户要求当前微博热搜/热榜时，直接执行 `node cli.js quota` 检查点数。
2. 执行 `node cli.js submit --wait`；24h 内重复采集最新榜单时加 `--force`。
3. 解析 stdout JSON，将 `result.hot_list` 按 `rank` 返回给用户。
4. 用户需要文件时执行 `export <task_id> --wait --out <文件名>.csv`。

## 输出与错误

- 成功：`{"ok":true,"data":{...}}`；失败：`{"ok":false,"code":"...","message":"..."}`。
- 退出码：`0` 成功；`1` 参数错误；`2` 平台认证失败；`3` 点数不足；`4` 网络不可达；`5` 其它错误。
- `1002/1003`：重新执行平台 `login --link`，**不是让用户登录微博**。
- `3001`：点数不足，提示充值，不要盲目重试。
- `status=failed`：读取 `fail_reason`；服务侧失败会自动返还 1 点，可稍后重试。
- `TIMEOUT`：任务可能仍在执行，稍后 `query <task_id>`。
- `4290`：触发限流，稍后重试。

## 红线

- 仅采集公开热榜数据，不绕过登录、验证码或访问控制。
- 热榜实时变化，结果以 `fetched_at` 时点为准；不要承诺每次一定成功。
