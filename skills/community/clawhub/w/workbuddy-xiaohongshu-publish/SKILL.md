---
name: xiaohongshu-publish
description: |
  将笔记 / 内容一键发布为小红书图文笔记，macOS 优先用本地 Chrome 图形界面，全程可视化、最稳。
  触发场景：
  - "把这份笔记发到小红书" / "发布到小红书" / "发小红书图文" / "把 XX 内容发到小红书"
  - 需要把 Markdown / HTML 内容渲染成小红书竖版卡片图（封面 + 分页）并发布
  沉淀了 macOS 下最稳的发布姿势：本地 Chrome + cookies.json 放在 MCP 启动目录，
  避开了 headless 登录态读不到、Linux Xvfb 在 macOS 拦路、图片按字符串排序错乱等坑。
agent_created: true
---

# 小红书图文一键发布技能（macOS 优化版）

基于 `xiaohongshu-mcp`（Go 二进制 + rod/本地 Chrome 驱动网页版）封装的发布工作流。
与官方 `xiaohongshu` skill 互补：本技能专注「从内容到发布的端到端自动化」，
并固化了 macOS 上最稳的本地 Chrome 启动方式。

## 前置依赖（一次性）

二进制在 `~/.local/bin/`：
- `xiaohongshu-mcp`（MCP 服务）
- `xiaohongshu-login`（登录工具，扫码生成 cookies.json）

若缺失，从 GitHub release 下载 darwin-amd64 包解压：
```bash
TAG="v2026.06.12.1403-5c43e3d"   # 以 https://github.com/xpzouying/xiaohongshu-mcp/releases 最新为准
curl -sSL -x http://127.0.0.1:56925 -o /tmp/xhs.tar.gz \
  "https://github.com/xpzouying/xiaohongshu-mcp/releases/download/${TAG}/xiaohongshu-mcp-darwin-amd64.tar.gz"
mkdir -p ~/.local/bin && tar -xzf /tmp/xhs.tar.gz -C ~/.local/bin
mv -f ~/.local/bin/xiaohongshu-mcp-darwin-amd64 ~/.local/bin/xiaohongshu-mcp
mv -f ~/.local/bin/xiaohongshu-login-darwin-amd64 ~/.local/bin/xiaohongshu-login
chmod +x ~/.local/bin/xiaohongshu-mcp ~/.local/bin/xiaohongshu-login
```
（macOS 有系统代理时给 curl 加 `-x http://127.0.0.1:56925`，或去掉走直连。）

还需要 `jq`、`python3`、以及本地 Chrome（`/Applications/Google Chrome.app`）。

## 四步流程

```
① 准备内容 + 渲染竖图  →  extract_xhs.py 从 HTML 提取(含官方配图)→ content.json → render_cards.py 生成 1080×1920 卡片 PNG
② 登录（首次/过期）     →  xiaohongshu-login 在 workdir 运行，扫码生成 cookies.json
③ 启动 MCP              →  start_mcp_local.sh <workdir>（本地 Chrome 图形界面）
④ 裁剪后【先给用户确认】再发布 →  publish.sh <workdir> <标题> <正文文件> <图片目录> <标签>
```

### 步骤① 从 HTML 提取并渲染竖图（推荐：保留官方配图）

若源是带 `<!-- N -->` 分节注释的 HTML（每节含 `<h2>` 标题、`.scene/.wrong/.prompt/.why` 块、可选 `<img>` 配图），
用 `extract_xhs.py` 自动抽取文案**并保留配图**，再交给 `render_cards.py` 渲染：
```bash
python3 scripts/extract_xhs.py \
  --html /path/to/WorkBuddy十大技巧实战案例.html \
  --out  /path/to/outputs/xhs
# 产出：outputs/xhs/content.json（每 tip 带 img 字段）+ outputs/xhs/img/tipN.png（官方配图）
python3 scripts/render_cards.py \
  --content /path/to/outputs/xhs/content.json \
  --out /path/to/outputs/xhs
# 产出：cover.png + tip1.png … tip10.png（1080×1920，tip1~tip9 内嵌官方配图，tip10 无图）
```
- `extract_xhs.py` 会把 HTML 里的 `<img>`（base64 data URI）解码导出为 `img/tipN.png`，
  并在 `content.json` 对应技巧写 `img` 字段；`render_cards.py` 据此把配图嵌入卡片。
- **注意**：`render_cards.py` 早期版本会过滤掉 `<img>` 导致卡片是纯文字、视觉上「没更新」，务必用带配图版本。
- `file://` 传给 Chrome 时必须用**绝对路径**，否则图片加载失败（显示「无法访问此网站」）。
- 若内容已是现成图片或纯文字 `content.json`，可跳过 extract，直接用 `render_cards.py`（见下）。
- 通用 `content.json` 结构见 `scripts/sample_content.json`。

### 步骤①b 纯文字/现成图片渲染（备选）
```bash
python3 scripts/render_cards.py \
  --content scripts/sample_content.json \
  --out /path/to/outputs/xhs
```
- 自动探测浏览器（本地 Chrome 优先，否则用 rod 的 Chromium）。
- 输出 `cover.png` + `tip1.png … tipN.png`（1080×1920）。
- 若要发布已有的整页 HTML：直接把 HTML 用 Chrome `--headless=new --screenshot` 截成竖图即可。

### 步骤① 渲染竖图（可选，若内容已是现成图片则跳过）

把笔记内容写成 `content.json`，用内置模板生成「封面 + N 张卡」：
```bash
python3 scripts/render_cards.py \
  --content scripts/sample_content.json \
  --out /path/to/outputs/xhs
```
- 自动探测浏览器（本地 Chrome 优先，否则用 rod 的 Chromium）。
- 输出 `cover.png` + `tip1.png … tipN.png`（1080×1920）。
- `content.json` 结构见 `scripts/sample_content.json`。
- 若要发布已有的整页 HTML：直接把 HTML 用 Chrome `--headless=new --screenshot` 截成竖图即可。

### 步骤② 登录（仅首次或 cookies 过期）

```bash
cd /your/workdir
~/.local/bin/xiaohongshu-login          # 弹出浏览器，用小红书 App 扫码
```
- 登录成功后会在**当前目录**写出 `cookies.json`（含 xiaohongshu 域名登录态）。
- Cookies 有效期约 30 天；过期重新跑这条命令。
- **关键**：`cookies.json` 必须和后续启动 MCP 的目录一致（见步骤③）。

### 步骤③ 启动 MCP（核心：本地 Chrome 图形界面）

```bash
bash scripts/start_mcp_local.sh /your/workdir
```
脚本会 `cd` 到 workdir 后启动：
```bash
~/.local/bin/xiaohongshu-mcp \
  -bin "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  -headless=false -port ":18060"
```
- 用 **`run_in_background`** 方式运行该脚本，使 MCP 常驻（不要 nohup &，会被工具调用结束回收）。
- 本地 Chrome 会弹出真实窗口，发布时能看到实际操作，更可控、登录态稳定。

### 步骤④ 发布

```bash
bash scripts/publish.sh \
  /your/workdir \
  "WorkBuddy 10个上手技巧" \
  /path/to/body.txt \
  /path/to/outputs/xhs \
  "WorkBuddy,AI工具,效率提升,提示词,职场干货"
```
`publish.sh` 会自动：
1. 收集图片目录里的 PNG/JPG，**封面(cover)优先，其余按文件名数字排序**（避免 tip10 排在 tip2 前）。
2. 用 `jq` 构造 `publish_content` 参数（title / content / images / tags / is_original=true）。
3. 经本地 MCP 调用发布，本地 Chrome 窗口自动填表、上传、点发布。
4. 发布中请留意本地 Chrome 是否弹出滑块/验证——若出现需人工辅助。

### 发布前务必「先确认再发」（重要约定）

- 发布是**不可逆且只有发新帖接口**（MCP 无编辑/删除笔记能力）。因此裁剪完竖图后，
  **用 present_files 把所有卡片预览给用户，等用户明确说「可以发 / 发吧」再执行 publish.sh**。
- 用户曾反馈「发布的和上次一样、没更新」，根因是渲染时丢掉了 HTML 里的官方配图（卡片变纯文字）。
  **每次更新 HTML 后必须重跑 extract_xhs.py + render_cards.py，并确认配图已嵌入**。

## 参数约束（小红书限制）

- 标题 ≤ 20 字符
- 正文 ≤ 1000 字符
- 图片至少 1 张（本地绝对路径或 HTTP URL）
- 日发布 ≤ 50 条

## 踩坑清单（务必遵守）

1. **macOS 不要用 Xvfb / headless 兜底逻辑**：官方 `start-mcp.sh` 里有 Linux 的 Xvfb 分支，在 macOS 会拦住启动。直接用本技能的 `start_mcp_local.sh`（本地 Chrome + `-headless=false`）。
2. **`cookies.json` 位置 = MCP 启动目录**：MCP 启动时在当前目录找 `cookies.json`。务必 `cd` 到含该文件的 workdir 再启动，否则读不到登录态、发布会失败或要求重登。
3. **图片务必数字排序**：文件名字符串排序会让 `tip10` 排在 `tip2` 之前。本技能 `publish.sh` 已按文件名内数字排序，封面始终第一。
4. **后台常驻用 `run_in_background`**：在 Bash 工具里用 `run_in_background=true` 直接跑 MCP 二进制/脚本；`nohup ... &` 形式会随工具调用结束被回收。
5. **`check_login_status` 在 headless 下可能误报未登录**：只要 `xiaohongshu-login` 已成功写出 `cookies.json` 且 MCP 在正确目录启动，可直接发布，不必死等 status 返回「已登录」。
6. **同一账号避免多 MCP 实例同时跑**：会抢同一浏览器会话导致登录态错乱。发布前确认只有一个 MCP 在 18060 端口。
7. **代理**：MCP 操作本地 Chrome 走 localhost，调用时加 `--noproxy '*'` 或 `export no_proxy=localhost,127.0.0.1`，避免代理拦截。
8. **HTML 配图别丢**：从 HTML 裁剪时必须用 `extract_xhs.py` 保留 `<img>`（解码导出为 `img/tipN.png` 并写入 `content.json` 的 `img` 字段），否则卡片只剩纯文字，视觉上和旧版一样、用户会以为「没更新」。`render_cards.py` 需据此把配图嵌入卡片。
9. **`file://` 必须绝对路径**：把 HTML 传给 Chrome `--screenshot` 时，HTML 内的图片引用要用绝对路径，否则报「无法访问此网站」、图片加载失败。
10. **发布前先确认**：MCP 只有 `publish_content`（发新帖），无编辑/删除笔记接口。裁剪完务必先 present 预览给用户确认，再发；「更新已发那篇」只能以「发新篇 + 用户 App 手动删旧篇」实现。

## 验证可用的命令速查

```bash
# 查登录态
curl --noproxy '*' -s -X POST http://localhost:18060/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"c","version":"1"}}}'

# 通用 MCP 调用（参考官方 xiaohongshu skill 的 mcp-call.sh）
# publish_content 参数：{"title":"","content":"","images":["/abs/path.png"],"tags":["话题"],"is_original":true}
```

## 与官方 skill 的关系

官方 `xiaohongshu` skill 提供了搜索/评论/详情等读类工具与本项目的 `mcp-call.sh`。
本技能聚焦「发布」闭环，自带正确脚本；二进制与端口（18060）共用，可并行使用。
