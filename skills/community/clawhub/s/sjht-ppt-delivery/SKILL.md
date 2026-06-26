---
name: ppt-delivery
description: |
  Convert HTML slide deck to PDF and send to Feishu user. Use when the user asks to
  generate a PPT/presentation and deliver it as a PDF file via Feishu message. Triggers
  on: "做PPT", "做个演示", "生成PPT", "做幻灯片", "发送PDF", "转PDF", "做报告",
  or when a PPT/slide task is completed and needs delivery. This skill covers the full
  pipeline: HTML slides → font scaling → PDF conversion → Feishu file upload & send.
---

# PPT Delivery — HTML 演示文稿转 PDF 并发送飞书

完整流程：生成 HTML 幻灯片 → 放大字体 → 转 PDF → 上传飞书发送给用户。

## 前置依赖

- `chromium-browser`（已安装）
- `puppeteer-core`（全局 npm 包）
- `pdf-lib`（全局 npm 包）
- Python 3 + `requests`（已安装）
- 飞书机器人已配置（openclaw.json 中有 APP_ID/SECRET）

## 工作流程

### Step 1: 生成 HTML 幻灯片

使用 `frontend-slides` 或 `jobs-style-ppt-generator` skill 生成 HTML 文件。

### Step 2: 字体放大（必须）

用户通常反馈字体太小，默认执行两轮放大：

**第一轮放大**（CSS 修改）：
- body font-size → `22px`
- 所有 ≤1rem → ×1.25
- 所有 1~1.5rem → ×1.35
- 所有 clamp() 值 → ×1.2
- 卡片 padding → ×1.2

**第二轮放大**（如用户仍嫌小）：
- body font-size → `26px`
- 所有字号 → 再 ×1.2
- clamp() 值 → 再 ×1.15
- 卡片 padding → 再 ×1.15

始终保持标题/正文层级关系。

### Step 3: HTML 转 PDF

使用脚本逐 slide 截图嵌入 PDF，保证视觉一致性：

```bash
NODE_PATH=$(npm root -g) node <skill_dir>/scripts/html2pdf.cjs <input.html> <output.pdf>
```

参数：
- `--width 1920`（默认）
- `--height 1080`（默认）

输出：多页 PDF（每页一张幻灯片截图）。

### Step 4: 发送飞书文件

将 PDF 通过飞书 Bot API 发送给用户：

```bash
python3 <skill_dir>/scripts/send_file_feishu.py <pdf_path> <user_open_id>
```

user_open_id 从消息的 inbound metadata `sender_id` 获取。

## 完整示例

```
1. UI agent 生成 /root/projects/report.html
2. 字体放大（两轮）
3. NODE_PATH=$(npm root -g) node ppt-delivery/scripts/html2pdf.cjs /root/projects/report.html /root/projects/report.pdf
4. python3 ppt-delivery/scripts/send_file_feishu.py /root/projects/report.pdf ou_xxxxx
5. 回复用户："PDF 已发送 📎"
```

## 注意事项

- PDF 文件大小通常 1-3MB（5-10 页）
- 如果 chromium 截图有渲染问题，检查字体是否加载完成（脚本内置 3 秒等待）
- 飞书发送需要 bot 有 `im:message:send_as_bot` 权限
- 文件类型支持：pdf、doc、xls、ppt、mp4、opus
