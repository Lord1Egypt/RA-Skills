# Changelog

## 1.3.1 (2026-06-18)

### Bug fix
- 修复 `SKILL.md` frontmatter `XHS_DATA_DIR` envVar description 字符串缺一个 `"` 导致 YAML 解析失败的问题

## 1.3.0 (2026-06-18)

### 行为变更
- **captcha / IP 风控 一律不重试** —— 遇到 `300012` 或 `verifyType=124` 滑块,脚本**直接报错退出**,不再自动 sleep + 重试
  - 原因: 自动重试会让 captcha 锁得更死(IP 持续被标记)
  - 留给用户决定是否换 IP / 等衰减

### 新功能
- **黄金路径: `xhs-harvest.py user <user_id>`** — 走 `user/profile/{uid}/{nid}?xsec_source=pc_user` 桶(桶 4),完全绕开 search 桶 captcha
  - 主页 DOM `note-item` 自带 `xsec_token`,30/30 命中
  - search 桶被锁时仍可照常工作

## 1.2.0 (2026-06-17)

### 新功能
- 引入 4 桶分桶 captcha 概念,默认走 via-user-profile 路径

## 1.1.0 (2026-06-17)

按用户名收割 + 精简文档 + captcha 检测。

### 新功能
- **`xhs-fetch.py user-search <name>`** — 用户名(中文/英文)→ 32hex user_id 解析器
  - 搜该用户名的笔记 → 取 top 1 → 打开 → DOM 找 author 主页链接
  - 过滤掉评论者(`xsec_source=pc_comment`)、侧边栏、自己
  - `--verify` 可选,会多访问一次 user 主页(name 匹配确认)
- **`xhs-harvest.py user --from-name "<name>"`** — 一行从显示名收割
  - 内部调 `user-search` 解析 user_id → 1 次 user 主页访问 → 详情收割
  - **user 主页只访问 1 次**,避免 captcha
  - captcha 时**自动 sleep 60s 重试 3 次**

### Bug fix
- `write_report` 引用了 `cmd_user/ids` 不存在的 `args.sort` / `args.per_keyword` → 用 `getattr` 兜底

### 健壮性
- `xhs-fetch.py user` 检测 `verifyType=124` 滑块验证,返回 exit code 3(独立于 300012 IP 风控的退出码 2)
- `cmd_user_search` 修了一处 `ab_eval` → `ab_open` 缺 sleep(改成 sleep 3s)

### 文档
- SKILL.md 大幅精简:367 行 → 100 行(-73%),同时加入"按用户名收割防 captcha"和"ab 直接调用限速铁律"两段关键经验
- README.md 更新 5 个核心命令 + captcha 陷阱说明
- docs/pitfalls.md 加 3 个新坑(见下)

## 1.0.0 (2026-06-17)

首次发布。

### 核心命令
- `search <keyword>` — 主题搜索（综合/热度/时间三种排序）
- `note <id|url>` — 单笔记详情 + 评论
- `user <id|url>` — 用户主页 + 作品列表
- `hotlist` — TODO（暂未实现）
- `paths` — 打印当前路径配置

### keepalive 子命令
- `inject` — 分号格式 cookies → Netscape
- `load` — 把 cookies 灌入 agent-browser
- `check` — 验证 cookie 是否还有效
- `paths` — 打印路径配置
- `state {save|load|check}` — 管理 agent-browser session

### 关键设计
- **统一走 agent-browser**：xhs 强制 X-s 签名 + IP 风控，curl 不可能过
- **路径自包含**：默认 `$SKILL/data/`，env 可覆盖
- **老路径兼容**：`/tmp/xiaohongshu/` 自动识别

### 已知限制
- `web_session` 6-12h 短效,需定期重导 cookie
- `hotlist` 命令未实现
- 评论深度 harvest 暂未实现
- 写操作（点赞/评论/关注）不在 skill 范围
