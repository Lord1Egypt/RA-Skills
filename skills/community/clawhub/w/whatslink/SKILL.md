---
name: whatslink
description: "查询公开下载/磁力/种子链接的 WhatsLink 元数据，默认只列出摘要与截图 URL，不下载不打开。"
allowed-tools: ["exec", "web_fetch"]
license: "MIT-0"
---

# WhatsLink

主页：https://whatslink.info/

当用户想在打开或下载前了解**公开链接**的大致内容时使用本 skill。它调用 `whatslink.info` 的公开 API，返回识别到的内容类型、文件名、文件数量、总大小，以及可能存在的截图 URL。

> English note: this skill inspects public links through the WhatsLink metadata API. It is not a downloader.

## 隐私与安全

- 只查询公开、非敏感链接。
- 不要提交私密链接、签名 URL、含 token/API key/session ID 的 URL、内网/本机地址、公司内部资源、用户未明确允许提交给第三方服务的文档或链接。
- WhatsLink 是第三方公共服务；把 URL 发给它等于把该链接透露给外部服务。
- 截图可能包含敏感信息。默认人类可读输出**只列出截图 URL**，不会自动下载、打开、转发图片。
- 除非用户明确要求且你确认安全，否则不要下载或打开目标内容，也不要转发截图。
- 结果仅作参考；如果 API 返回未知或空结果，不要臆测文件内容。
- 服务可能有免费额度/反滥用限制；调用保持最小化，对外展示时注明来源。

## API 形态

- Endpoint：`GET https://whatslink.info/api/v1/link?url=<encoded-url>`
- 请求参数：
  - `url`（必填 string）：要检查的公开链接。
- 常见响应字段：
  - `error`（string）：非空表示查询失败。
  - `type`（string）：链接内容类型。
  - `file_type`（string）：例如 `unknown`、`folder`、`video`、`text`、`image`、`audio`、`archive`、`font`、`document`。
  - `name`（string）：内容/资源名称。
  - `size`（number）：总字节数。
  - `count`（number）：包含文件数。
  - `screenshots`（array 或 null）：截图对象，常见字段为 `time` 和 `screenshot` URL。

## CLI 辅助脚本

脚本使用 Python 3 标准库，无需额外依赖。

```bash
cd /root/.openclaw/workspace/skills/whatslink
python3 scripts/whatslink_query.py 'https://example.com/file.torrent'
python3 scripts/whatslink_query.py --json 'https://example.com/file.torrent'
python3 scripts/whatslink_query.py --no-screenshots 'https://example.com/file.torrent'
python3 scripts/whatslink_query.py --max-screenshots 3 'https://example.com/file.torrent'
python3 scripts/whatslink_query.py --timeout 10 --user-agent 'OpenClaw/whatslink' 'https://example.com/file.torrent'
```

参数：

- `url`：必填，要查询的公开 URL。
- `--json`：输出 WhatsLink 原始 JSON 响应；保持原始结构，不做摘要格式化。
- `--no-screenshots`：在人类可读摘要中隐藏截图 URL。
- `--max-screenshots N`：限制摘要中展示的截图 URL 数量；默认展示全部；`0` 表示不列出 URL。
- `--timeout`：请求超时时间，默认 `20` 秒。
- `--endpoint`：API endpoint，默认 `https://whatslink.info/api/v1/link`；主要用于测试或替代服务。
- `--user-agent`：可选自定义 User-Agent。默认 UA 版本为 `OpenClaw-whatslink-skill/0.1.1`。

## 推荐工作流

1. 先判断链接是否适合提交给第三方公共元数据服务：必须是公开、非敏感、无 token、非内网。
2. 使用 `scripts/whatslink_query.py` 获取稳定输出。
3. 默认向用户报告人类可读摘要；如果响应含截图，默认列出截图 URL，但不下载、不打开。
4. 用户只需要机器可读结果时使用 `--json`。
5. API 返回空/未知时，直接说明“未识别出有用元数据”，不要补脑。

## 示例

```bash
cd /root/.openclaw/workspace/skills/whatslink
python3 scripts/whatslink_query.py 'https://releases.ubuntu.com/24.04/ubuntu-24.04.2-desktop-amd64.iso.torrent'
```

摘要通常包含：

- 名称
- 类型
- 文件类型
- 大小（含原始 bytes）
- 文件数
- 截图数
- 截图 URL（如 WhatsLink 返回）

## 版本

- 0.1.1：默认人类可读摘要列出截图 URL；新增 `--no-screenshots` 和 `--max-screenshots`；中文文档与隐私说明增强；UA 更新到 0.1.1。
