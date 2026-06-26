---
name: unified-kb
description: |
  统一知识库入口技能（#kb）。当用户发送内容并标记 #kb 时触发。
  自动完成：素材下载 → IMA 知识库存储 → workspace/kb 归档 → memory 记录。
  支持：微信公众号文章、网页链接、YouTube 视频（字幕提取）、纯文本、文件路径。
---

# 统一知识库（#kb）技能

> 触发条件：用户发送内容并包含 `#kb` 标签
> 协同存储：IMA（腾讯知识库）+ workspace KB（本地结构化知识库）

## 工作流程

```
用户发送 #kb 内容
        ↓
① 判断内容类型
        ↓
② 下载/解析/提取字幕
        ↓
③ 存入 IMA（知识库 + 笔记）
        ↓
④ 存入 workspace/kb
        ↓
⑤ 记录到 memory/YYYY-MM-DD.md
        ↓
⑥ 重建 KB 索引（自动更新 kb_master_index.md）
        ↓
⑦ 向用户确认完成
```

## 支持的内容类型

| 类型 | 示例 | 处理方式 |
|------|------|---------|
| 微信公众号文章 | `https://mp.weixin.qq.com/s/xxx` | 下载并导出 Markdown |
| 网页链接 | `https://example.com/article` | web_fetch 抓取内容 |
| **YouTube 视频** | `https://youtu.be/xxx` | **下载字幕 → 生成总结 → 存笔记** |
| 纯文本/摘要 | `#kb 这段话说的是...` | 直接存储文本 |
| 本地文件路径 | `#kb /path/to/file` | 读取文件内容后存储 |

## YouTube 视频 #kb 处理流程（重点）

> 当 `#kb` 链接是 YouTube 视频时，启用完整字幕提取流程。**优先级：NotebookLM > 本地 Whisper**。

```
YouTube 视频链接
    ↓
① NotebookLM 优先（推荐）
   ├─ notebooklm-kit: add_source(url=YouTube_URL)
   ├─ 等待同步 (~30s)
   └─ generation.chat() 提取完整解说词原文
    ↓
② 本地 Whisper 兜底
   └─ 仅在 NotebookLM 配额不足时使用
      ├─ yt-dlp TV client 下载音频
      ├─ Whisper small 模型转录
      └─ 解析 VTT → 纯文本
    ↓
③ 存入 IMA
    ├─ 知识库：视频链接（来源引用）
    └─ 笔记：总结 + 完整字幕原文
    ↓
④ 存入 workspace/kb
    ├─ kb/YYYYMMDD_视频标题_总结.md
    └─ kb/YYYYMMDD_视频标题_字幕原文.txt
    ↓
⑤ 记录 memory
```

**NotebookLM 优先提取脚本**（详见 video-processor skill）：
```python
# 1. 添加视频到 notebook
client.add_source(url="YouTube_URL", notebook_id="notebook_id")

# 2. 等待同步后，提问提取原文
response = client.chat("请提取这个视频的完整解说词原文，包括所有数据和论述细节。不要总结，我要原文。")
```

**本地 Whisper 兜底命令**（当 NotebookLM 不可用时）：
```bash
yt-dlp --js-runtimes "node:/usr/bin/node" \
  --cookies /tmp/youtube_cookies.txt \
  --extractor-args "youtube:player_client=tv" \
  --write-subs --skip-download \
  -o "/tmp/subs.%(ext)s" \
  "https://youtu.be/VIDEO_ID"
```

**完整 shell 命令（yt-dlp 字幕下载）**：
```bash
yt-dlp --js-runtimes "node:/usr/bin/node" \
  --cookies /tmp/youtube_cookies.txt \
  --extractor-args "youtube:player_client=tv" \
  --write-subs --skip-download \
  -o "/tmp/subs.%(ext)s" \
  "https://youtu.be/VIDEO_ID"
```

**字幕解析为纯文本（Python）**：
```python
import re
with open('/tmp/subs.vtt', 'r', encoding='utf-8') as f:
    content = f.read()
segments = re.findall(
    r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\s*\n(.+?)(?=\n\n|\n-->)',
    content, re.DOTALL
)
full_text = '\n'.join([s[2].strip().replace('\n', ' ') for s in segments])
```

**IMA 笔记分段上传（字幕过长时）**：
```python
# 每段 ~12000 字符，分多次 append_doc
chunk_size = 12000
for i in range(0, len(full_text), chunk_size):
    chunk = full_text[i:i+chunk_size]
    # import_doc 第一段，append_doc 后续段
```

## IMA 存储策略

### 默认目标知识库
**默认存入 IMA "个人知识库"**，不询问用户，除非用户明确指定其他知识库。

> ⚠️ **知识库 ID 配置**：请在 `scripts/store_kb.py` 顶部的 `IMA_KB_ID` 变量中设置目标知识库 ID。
> 当前已配置：`个人知识库`（`IMA_KB_ID = "3ABKKskfyVyAHq_ohwX7KrwDyfrapnxTTHlQ85NFR6E="`）

### 存储方式
| 内容类型 | IMA 模块 | 接口 |
|---------|---------|------|
| 微信公众号文章/网页链接 | `knowledge-base` | `import_urls`（批量添加URL） |
| YouTube 视频链接 | `knowledge-base` | `import_urls`（仅作来源引用） |
| YouTube 总结/字幕 | `notes` | `import_doc` + `append_doc` |
| 纯文本 | `notes` | `import_doc`（新建笔记） |
| 文件 | `knowledge-base` | `create_media` → `add_knowledge` |

> ⚠️ **YouTube 视频特殊处理**：视频链接仅作为来源引用存入知识库，**不要**把链接当成正文内容存入笔记。正文内容（总结 + 字幕）全部通过 `import_doc` / `append_doc` 存入笔记。

## workspace/kb 存储策略

- **YouTube 视频**：两个文件
  - `kb/YYYYMMDD_视频标题_总结.md` — 精华摘要
  - `kb/YYYYMMDD_视频标题_字幕原文.txt` — 完整字幕
- 微信文章/网页：存到 `kb/` 目录，文件名前缀 `YYYYMMDD_`
- 纯文本：存到 `kb/` 目录，文件名前缀 `YYYYMMDD_`
- 附加 `#tag` 标签到文件名和内容中

## 执行脚本

```bash
python3 /home/xdl/.openclaw/workspace/skills/unified-kb/scripts/store_kb.py <content_type> <content> [tags]
```

**YouTube 视频 content_type 为 `youtube`**：
```bash
python3 store_kb.py youtube "https://youtu.be/m8tpIGpXDBc" #kb #半导体
```

## memory 记录格式

在 `memory/YYYY-MM-DD.md` 中记录：
```
- **KB入库**：[标题/摘要] | 来源：[来源] | 路径：`kb/文件名.md` | IMA笔记：note_id | IMA知识库：✅ | 标签：#kb #标签1
```

## 使用示例

- `#kb https://mp.weixin.qq.com/s/xxx` → 自动下载 + 存 IMA 知识库 + 存 KB + 记录 memory
- `#kb https://youtu.be/xxx #半导体` → 下载字幕 + 生成总结 + 存 IMA笔记 + 存 KB + 记录 memory
- `#kb 这段话说的是能源托管...` → 存 IMA 笔记 + 存 KB + 记录 memory
- `#kb https://example.com/article #暖通 #合同` → 抓取网页 + 存 IMA + 存 KB + 记录 memory（标签自动应用）

## YouTube Cookies 配置

YouTube 字幕下载需要浏览器 cookies 绕过机器人验证：

1. 在浏览器安装 EditThisCookie 插件
2. 打开 YouTube 视频页面，导出 cookies 为 JSON
3. 将 JSON 转换为 netscape 格式（`/tmp/youtube_cookies.txt`）
4. 脚本自动使用该文件

**Cookie 文件路径**：`/tmp/youtube_cookies.txt`（固定路径）

## 注意事项

- IMA 凭证从环境变量读取：`IMA_OPENAPI_CLIENTID`、`IMA_OPENAPI_APIKEY`
- workspace KB 路径：`/home/xdl/.openclaw/workspace/kb/`
- IMA 存储失败时，继续存入 workspace/kb，不中断流程
- 微信文章下载内部调用 `wechat-article-reader` 脚本（用于下载），但 **#kb 入口必须走 `store_kb.py`** —— 它会在下载后自动同步 IMA 笔记 + IMA 知识库 + 本地 KB三重存储
- 所有 string 字段存入 IMA notes 前必须做 UTF-8 校验（详见 ima-skill notes 模块说明）
- ⚠️ **API 路径注意**：IMA Wiki API 路径为 `openapi/wiki/v1/...`，不是 `openapi/knowledgebase/v1/...`
- ⚠️ **YouTube 字幕过大处理**：字幕原文 > 12000 字符时需分段 `append_doc`，每段 12000 字符
