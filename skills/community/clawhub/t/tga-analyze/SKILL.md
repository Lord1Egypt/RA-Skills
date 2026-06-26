---
name: tga-analyze
description: Logs into TGA (hortorgames), parses projectId and dashboardId from panel URL, downloads report zip via API, unzips to tga-downloads/, and analyzes all xlsx files. Use when the user asks to analyze current TGA webpage data, analyze TGA data, or download and analyze TGA reports.
---

# TGA 网页数据分析

从 TGA 面板 URL 登录、下载报表 zip、解压并综合分析所有 xlsx。凭证来自skill中的 `.env`，token 缓存在本技能所在目录下。

## 前置条件

当前 skill 所在目录下存在 `.env`，且包含（勿提交真实凭证到 git）：

- `TGA_LOGIN_NAME`：登录名
- `TGA_ENCRYPTED_PASSWORD`：前端加密后的密码（登录请求中 `enPassword` 的值）
- `TGA_COOKIES`：**必填**。浏览器 Cookie 中的 `gm_encrypted_open_id_prod` 与 `gm_encrypted_open_id_test`，格式为 `gm_encrypted_open_id_prod=xxx; gm_encrypted_open_id_test=yyy`（从开发者工具或浏览器复制完整 cookie 字符串）。登录接口依赖此 cookie，缺少会导致登录失败。

## 工作流

1. **获取并解析 URL**  
   若用户未提供，提示粘贴当前 TGA 面板 URL。从 hash `#/panel/panel/<projectId>_<dashboardId>` 解析出 `projectId`、`dashboardId`（例如 `https://tga-web.hortorgames.com/#/panel/panel/377_5851` → projectId=377, dashboardId=5851）。

2. **登录或取缓存**  
   读取**本技能所在目录**下的 `.tga-token`。若无该文件或内容无效，或后续下载返回 401，则执行登录脚本（会读同目录 `.env` 并写入 `.tga-token`）：
   ```bash
   node ~/.agents/skills/tga-analyze/scripts/tga.js login
   ```
   脚本会使用 `.env` 中的 `TGA_LOGIN_NAME`、`TGA_ENCRYPTED_PASSWORD`、`TGA_COOKIES` 请求登录接口并保存 token。

3. **下载**  
   执行下载脚本（与 [tgaCheck/example.md](tgaCheck/example.md) 一致：**启动下载 → 轮询进度 → 真正下载**）：
   ```bash
   node ~/.agents/skills/tga-analyze/scripts/tga.js download <projectId> <dashboardId> [outputDir] [--task-id=<id>]
   ```
   脚本会：① 调用启动下载接口拿到 taskId（并提示「若中途断掉可加 --task-id=xxx 从进度轮询继续」）；② 轮询 `asyncTaskProgress` 直到 `async_ok`（单次请求失败会重试 4 次，不会因偶发断线直接退出）；③ 请求 `taskFileDownload` 保存 zip。  
   **断线续跑**：若轮询阶段断掉但服务端任务已生成完成，可直接用上次打印的 taskId 执行 `... download <projectId> <dashboardId> [outputDir] --task-id=<taskId>`，跳过启动、只做轮询与下载。

4. **解压**  
   下载脚本输出的 zip 路径会打印在控制台。使用 `unzip` 将该 zip 解压到同目录或同名子目录（如 `tga-downloads/377_5851_2026-03-12-1625/`），便于后续只在该目录下查找 xlsx。

5. **分析 xlsx**  
   列出解压目录下所有 `.xlsx`，用 Python 的 `pandas.read_excel` 逐个读取，根据表结构做综合汇总（多表关键指标、趋势、对比等），输出结构化结论。

---

## Node 脚本（推荐）

登录与下载由脚本完成，无需手写 curl。脚本位于本技能目录下 `scripts/tga.js`，读取同目录的 `.env` 与 `.tga-token`。

| 操作 | 命令 |
|------|------|
| 登录并写 token | `node ~/.agents/skills/tga-analyze/scripts/tga.js login` |
| 下载 zip | `node ~/.agents/skills/tga-analyze/scripts/tga.js download <projectId> <dashboardId> [outputDir] [--task-id=<id>]` |

下载流程与 example.md 一致：启动下载 → 监控进度（轮询 asyncTaskProgress，单次失败自动重试）→ 完成后请求 taskFileDownload 保存 zip。可选第三参数为输出目录。**断线续跑**：若轮询中途断掉但任务已在服务端完成，使用 `--task-id=<上文的 taskId>` 可跳过启动、直接轮询并下载。脚本位于 `~/.agents/skills/tga-analyze/scripts/tga.js`。

## 术语约定

统一使用：登录、token、projectId、dashboardId、下载接口、解压目录、xlsx。不写死 377、5851，均由 URL 解析或用户输入得到。
