# 微信云开发部署 · 真实环境踩坑全记录

基于一次完整部署（AppID `wxe6e50674150354f0` / env `daka-d8gevsjp3fadea57a` /
订阅模板 `_v-Xwe-...`，体验版）实测。所有结论均经实际操作验证，非推测。

---

## 踩坑 1：集合（collection）必须控制台手动建

函数一跑就报 `-502005 collection not exists`。排查四条路逐一实测：

| 尝试 | 命令 | 结果 |
|---|---|---|
| CLI 建集合 | `tcb db create 集合名 -r ap-shanghai` | **子命令已不存在**（v3.8.1 移除） |
| 通用 API | `tcb api tcb CreateCollection --body '{...}'` | **接口已离线** `ActionOffline` |
| nosql INSERT | `tcb db nosql execute --command '[{"CommandType":"INSERT",...}]'` | 能建，但建到**另一套 Mongo 实例**，`wx-server-sdk` 看不到 |
| SDK `.add()` | `db.collection('x').add({...})` | **不会自动建集合**，被静默吞掉 |

**正确做法**：在 CloudBase 控制台 → 环境 → 数据库 → 集合 → 新建集合，建这 7 个
（按项目实际表名，本项目为）：
`users` / `gangs` / `gang_memberships` / `checkins` / `reminders` /
`subscribe_grants` / `gang_events`

并把 `seed` 函数写成「先确保 7 集合存在再幂等播种」，这样部署后跑一次即全建好，
不再依赖手动建表顺序。注意：临时探针函数（仅用于 `.add()` 行为探测）被体验版环境
直接 SIGKILL（退出码 137），推测体验版对函数数量/操作有限制——不要为了建集合而部署探针。

验证集合生效：`tcb db nosql execute --command '[{"TableName":"gangs","CommandType":"COMMAND","Command":"{\"find\":\"gangs\"}"}]' -r ap-shanghai`

---

## 踩坑 2：`tcb fn invoke` 报 `GetFunction Namespace取值与规范不符`

现象：`seed` 用 `tcb fn invoke` 始终成功，`api`/`login`/`dailyPush` 稳定报
`GetFunction Namespace取值与规范不符`。

排查：
- 不是代码/部署坏掉：`fn list` 四个函数均 `Deployment completed`；`api` 经
  `node --check` 且人工复核无误；与 `seed` 用完全相同的 SDK/DB 模式。
- 删掉 `api` 全新部署仍同样报错 → 排除部署状态问题。
- 标准 SCF 在默认 namespace 下 `ListFunctions` 列到 0 个函数 → 证实这些函数
  属 CloudBase **环境专属 namespace**，标准 SCF 直调拿不到。

结论：这是 `fn invoke` 工具在查函数元数据（`GetFunction`）时的 **backend
namespace 解析 bug**，与代码/运行时无关。小程序真实的 `wx.cloud.callFunction`
走另一条不带 `GetFunction` 的通道，不受影响。**真正的端到端验证必须在微信开发者
工具/体验版里跑小程序完成**，不要依赖 `tcb fn invoke` 的成功与否来判断函数健康。

---

## 踩坑 3：上传 IP 白名单仅收 IPv4，IPv6 出口必拒

`miniprogram-ci upload` 报错：
```
errCode: -10008
errMsg: invalid ip: 2408:8207:7880:8ec8:6d85:d5fc:23ea:4915
```
该 IPv6 是经本地代理（`127.0.0.1:xxxx`）出口的地址。

关键认知修正：
- 一开始假设「用户本机是 IPv4，走本机传可绕开」——**实测推翻**：用户的 Mac-mini
  与我（agent）跑的是**同一个网络出口/代理网关**，报的 IPv6 与我被拒的**一字不差**。
  所以「我传」与「用户本机传」在 IP 层等价，一起被拒。
- 微信「上传代码 IP 白名单」UI **无法添加 IPv6**（输入框只收 IPv4 格式）。

**唯一解法**：
1. **关掉 IP 白名单总开关**（MP 后台 → 开发设置 → 小程序代码上传 IP 白名单 →
   关闭）。关掉后不再校验 IP，同一个 IPv6 出口直接放行。安全性靠上传私钥兜底
   （私钥仅本地、未泄露即安全）。这是最干脆的一劳永逸方案。
2. （备选）把 Mac 切到 IPv4 出口（关代理 / 手机热点），`curl -s https://ifconfig.me`
   拿公网 IPv4 加进白名单。下次换网络又得重加，不如方案 1。

---

## 踩坑 4：zsh 下 `PIPESTATUS` 取值误判

在 zsh 中：
```
$NODE $CI upload ... |& tail -40
echo "退出码: ${PIPESTATUS[0]}"   # 拿到的是 echo 的退出码或错位值
```
导致两次失败的 CLI 上传被误判为「退出码 0 成功」。**修正**：用 `miniprogram-ci`
的 JS API（`ci.upload`）返回结构化 error 对象，不要靠 shell 退出码判断；或显式
`node script.js` 后在脚本内 `process.exit(code)`。

---

## 踩坑 5：体验版环境默认 region = `ap-shanghai`

`tcb` 的 `fn list` / `env list` 不传 region 也能跑，但 `fn deploy` / `fn invoke`
/`db nosql` 必须加 `-r ap-shanghai`，否则报 region 相关错误。本项目 env 也在
`ap-shanghai`。

---

## 踩坑 6：子目录 `require` 相对路径写错 → 云函数加载即崩，且被 fn invoke「bug」掩盖

现象：体验版一进就"网络异常"（前端 `wx.cloud.callFunction` 进 `fail`）；
`tcb fn invoke api` 之前报 `GetFunction Namespace取值与规范不符`（误判为工具 bug）。

真因：云函数若拆了子目录（如 `api/services/stats.js`），其内的相对 `require`
以**该文件所在目录**为基准，不是函数根目录。本项目 `api/services/stats.js`
错写成：
```js
const { db } = require('./db');            // ✗ 解析成 api/services/db.js，不存在
const { computeStreaks } = require('./services/streak'); // ✗ 解析成 api/services/services/streak.js
```
应为：
```js
const { db } = require('../db');          // ✓ 回到 api/db.js
const { computeStreaks } = require('./streak'); // ✓ 同目录
```
后果：`index.js` 一 `require('./services/stats')` 就 `Cannot find module './db'`
崩溃 → 所有 `wx.cloud.callFunction` 调用失败 → 前端弹"网络异常"。

为什么一直没暴露：
- 本地 `node --check *.js` **只验语法、不解析依赖**，路径错误查不出来。
- 之前误把 `tcb fn invoke api` 的 `GetFunction Namespace` 报错当成工具 bug，
  **它其实掩盖了这处真实模块错误**（重测时 fn invoke 直接回 `Cannot find module`）。

验证修复（关键）：部署后用 `tcb fn invoke api '<json>'`（**位置参数传 JSON 字符串，
不要 `--params 文件名`——后者会被当成非法 JSON**）确认不再报 module 错误、能进路由。
若 CLI 把字段解析成空（如 `path:""`），属调用参数格式问题，不影响小程序真实调用。

正确做法：
1. 子目录文件里的 `require` 必须按「文件自身位置」写相对路径；根文件 `index.js`
   用 `./db`、`./services/x` 是对的，子文件用 `../db`、`./x`。
2. 部署前除 `node --check` 外，务必做一次真实 `fn invoke` 验证模块能加载；
   看到 `Cannot find module` 优先查相对路径，而不是怀疑 CLI/部署。

---

## 踩坑 7：云函数本地 `node_modules` 必须装齐再 deploy

`cloudfunctions/*/package.json` 声明了 `wx-server-sdk`，但本地 `node_modules`
为空时 `tcb fn deploy` 上传的是**无依赖**的目录。Tencent CloudBase SCF 不会像
微信开发者工具那样云端自动装依赖，缺 `wx-server-sdk` → `require` 崩溃。

修复：`cd cloudfunctions/<fn> && npm install wx-server-sdk@^2.6.0`（受管 node），
再 `tcb fn deploy <fn> --force`。seed 能跑通容易让人误以为「依赖会自动装」，
但 api/login 同样写法却崩，就是部署时没带 node_modules 或路径写错叠加所致——
两个坑（踩坑 6 + 本坑）任一成立都会表现为"网络异常"，逐一排查。

---

## 完整命令清单（受管 node workspace，不污染本机全局）

```bash
# 1) 装 CloudBase CLI（受管 workspace）
cd ~/.workbuddy/binaries/node/workspace
npm install @cloudbase/cli@latest
TCB=node_modules/@cloudbase/cli/bin/tcb
NODE=~/.workbuddy/binaries/node/versions/22.22.2/bin/node

# 2) 登录（后台跑，抓 /tmp/tcb-login.log 里的授权 URL）
nohup $NODE $TCB login |& tee /tmp/tcb-login.log &

# 3) 部署云函数
$NODE $TCB fn deploy api --force -r ap-shanghai
$NODE $TCB fn deploy login --force -r ap-shanghai
$NODE $TCB fn deploy seed --force -r ap-shanghai
$NODE $TCB fn deploy dailyPush --force -r ap-shanghai

# 4) 控制台手动建 7 集合后，跑 seed
$NODE $TCB fn invoke seed -r ap-shanghai

# 5) 上传前端（用 scripts/upload.js，参数化路径）
cd 项目根目录 && node skill目录/scripts/upload.js
```

## 上传包边界

`miniprogram-ci` 上传仅打包 `miniprogram/`（或用 `ignores` 排除
`node_modules`/`cloudfunctions`/`server`/`*.key`/`*.md`）。**上传私钥 `.key` 和
后端/文档不会被打进包**。若 `project.config.json` 含 `cloudfunctionRoot`，
CLI 会顺带重推云函数——已用 `tcb` 部署好的情况下可临时去掉该行，纯前端上传。
