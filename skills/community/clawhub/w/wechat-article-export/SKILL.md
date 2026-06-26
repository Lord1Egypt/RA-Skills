---
name: wechat-article-export
description: 微信公众号多功能导出工具。將公眾號文章導出為長截圖（PNG）、PDF 或 Markdown，支持任選一種或多種格式。觸發詞：「導出微信文章」、「公眾號截圖」、「文章轉PDF」、「文章轉Markdown」、「微信導出」。
author: 闪电 ⚡️
allowed-tools: Read, Write  # 僅執行 Python 腳本，無 shell 命令
version: "1.1.0"
tags:
  - wechat
  - 微信
  - 公众号
  - 导出
  - 截图
  - PDF
  - Markdown
  - mp.weixin.qq.com
allowed-tools: Read, Write  # 僅執行 Python 腳本，無 shell 命令
---

# 微信公众号多功能导出工具

集成長截圖、PDF、Markdown 三種導出方式於一體，根據需要自由選擇。

## upported Formats 支持格式

| 格式 | 說明 |
|------|------|
| `screenshot` | 移動端長截圖（PNG），3x DPR，自動拼接，隱藏底部工具欄 |
| `pdf` | PDF 文檔（基於截圖轉換） |
| `markdown` | 高質量 Markdown，含 YAML frontmatter、代碼塊、圖片 |

## 觸發方式

- 「導出微信文章」
- 「公眾號截圖」
- 「文章轉PDF」
- 「文章轉Markdown」
- 「微信導出」
- 收到 `mp.weixin.qq.com` 連結

## 導出格式組合示例

```
# 全部格式
-f all

# 僅截圖
-f screenshot

# 僅 Markdown
-f markdown

# 截圖 + PDF
-f screenshot,pdf

# 三種都要
-f screenshot,pdf,markdown
```

## 執行命令

### 方式一：CLI（直接指定格式）

```bash
# 全部導出
python3 /path/to/wechat_export.py "<URL>" -f all -o /workspace/output

# 指定格式導出
python3 /path/to/wechat_export.py "<URL>" -f screenshot -o /workspace/output
python3 /path/to/wechat_export.py "<URL>" -f markdown -o /workspace/output
python3 /path/to/wechat_export.py "<URL>" -f screenshot,pdf -o /workspace/output

# Markdown 不下載圖片（保留遠程 URL）
python3 /path/to/wechat_export.py "<URL>" -f markdown --no-images -o /workspace/output

# Markdown 不含 YAML frontmatter
python3 /path/to/wechat_export.py "<URL>" -f markdown --no-frontmatter -o /workspace/output
```

### 方式二：Python 函數調用（推薦 Agent 內嵌使用）

```python
import sys
sys.path.insert(0, "/path/to/scripts")
from wechat_export import export_wechat_article

# 導出全部格式
result = await export_wechat_article(
    "https://mp.weixin.qq.com/s/xxxxx",
    formats=["screenshot", "pdf", "markdown"],  # 可任選
    output_dir="/workspace/output",
    download_imgs=True,    # Markdown 是否下載圖片
    no_frontmatter=False,   # Markdown 是否含 frontmatter
)

# result 包含:
# {
#     "title": "文章標題",
#     "url": "https://...",
#     "screenshot_path": "/path/to/xxx.png",   # or None
#     "pdf_path": "/path/to/xxx.pdf",          # or None
#     "markdown_path": "/path/to/xxx.md",     # or None
#     "error": None or "錯誤信息",
# }
```

## 依賴

```bash
pip install playwright beautifulsoup4 markdownify requests Pillow
playwright install chromium
```

## 輸出目錄結構

```
<OUTPUT_DIR>/
└── <Article_Title>/
    ├── <Article_Title>-20260410.png    # 長截圖（如選）
    ├── <Article_Title>-20260410.pdf    # PDF（如選）
    └── <Article_Title>.md              # Markdown（如選）
        └── images/
            ├── img_000.png
            └── img_001.jpg
```

## 核心功能亮點

### 長截圖 (`screenshot`)
- 移動端視圖（393×852，3x DPR）
- 智能滾動觸發懶加載圖片
- 隱藏底部工具欄、干擾元素
- 15% 重疊拼接，消除接縫
- 深度反檢測偽裝

### PDF (`pdf`)
- 自動基於截圖轉換
- RGBA / P 模式自動墊白底
- 分辨率 100 DPI

### Markdown (`markdown`)
- YAML frontmatter（元數據）
- 30+ 微信噪聲元素深度移除
- 代碼塊識別 25+ 語言
- 富文本優化（標題/列表/引用）
- 圖片可選本地下載或保留遠程 URL
- 多線程並發下載（5 線程，2 次重試）

---

## Changelog

### v1.1.0 (2026-04-11)

**修复：**
- 修复 URL 验证逻辑：`/s/` → `parsed.path.startswith("/s")`，支持临时分享链接（路径为 `/s` 而非 `/s/`）
- 截图前自动关闭并隐藏「此为临时链接」横幅（`.rich_media_global_msg_inner` / `#preview_bar`），避免横幅在每个分段重复出现
- 将横幅元素加入 NOISE_SELECTORS 黑名单
