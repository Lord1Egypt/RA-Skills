---
name: xiaofeng-skills
description: 探店笔记完整生产流水线。接收门店场景图→AI生成探店图 + 接收点评链接→抓取网友推荐菜图片 → 生成爆款文案 → 发布到腾讯文档。适合餐饮品牌线上运营、探店笔记批量代写场景。
version: 1.1.0
author: 小枫 🍁
metadata:
  openclaw:
    emoji: "🍁"
    requires:
      skills:
        - tencent-docs
        - tandian-image-skills
      env:
        - REPLICATE_API_TOKEN
---

# 探店笔记完整生产流水线 SOP

## 概述

本 skill 覆盖探店笔记从**图到文到发布**的全流程，串联两大 skill 实现自动化：

- **tandian-image-skills** → 用 AI 把模特放入门店场景生成探店打卡照
- **tencent-docs** → 上传图片 + 创建文档 + 发布

### 文档最终结构

```
1. 🫣 AI探店图（tandian-image-skills 生成）
2. 🍖 菜谱图 × 2（来自点评网友推荐菜）
3. ✍️ 爆款探店文案
```

---

## 前置条件

### 依赖

- `tandian-image-skills`（依赖最新版，SOP始终跟踪最新版本）— 已安装
- `tencent-docs` — 已安装并授权
- `REPLICATE_API_TOKEN` — 环境变量已配置

### 脚本

- `scripts/publish_note.sh` — 一键发布脚本（上传图片→创建文档→移动→权限→重命名）

---

## 输入

| 输入 | 说明 |
|------|------|
| 门店场景图 | 餐厅门店/环境实拍图，用于 AI 生成探店图 |
| 大众点评链接 | 餐厅的点评链接，用于抓取菜谱图 |

---

## 工作流

### Step 1：生成 AI 探店图

收到门店场景图后，调用 tandian-image-skills 生成美女探店打卡照：

```bash
REPLICATE_API_TOKEN=你的token \
  skills/tandian-image-skills/scripts/run_tandian.sh \
  门店场景图路径
```

输出路径自动生成在当前目录 `output/` 下，带回文件名备用。

### Step 2：抓取网友推荐菜图片

用浏览器打开点评链接，滚动触发懒加载，提取网友推荐菜的图片URL。

- 只抓**网友推荐菜**区域，不抓商家招牌菜
- 选2道菜下载
- 用 ffmpeg 适当压缩（宽度≥1200px、质量≥8，确保手机端清晰）

### Step 3：创作探店文案

按以下模板写文案：

```
# [标题] 感叹句式+情绪词+emoji

[开头] 有"活人味"的个人体验，朋友推荐口吻

[环境] 简单描述店铺氛围

[2道菜品] 统一emoji标记：🍖 菜名 — 简短口感描述

[地址] 📍 餐厅名(分店)
[人均] 💴 人均¥XX

[标签] 8个#话题标签
```

**风格：** 口语化、有烟火气，禁用目录式结构，emoji统一不混用。

### Step 4：一键发布

调用脚本自动完成全部腾讯文档操作：

```bash
bash scripts/publish_note.sh \
  --title "临时标题" \
  --content "文案全文" \
  --name "小枫 AI 探店笔记_[餐厅名(分店)]_[YYYYMMDD]" \
  --photo /path/to/AI探店图.jpg \
  --dish1 /path/to/菜谱图1.jpg \
  --dish2 /path/to/菜谱图2.jpg
```

脚本自动完成：上传图片 → 组装文档 → 创建 → 移动文件夹 → 设公开编辑 → 重命名。

---

## 输出

📄 小枫 AI 探店笔记_[餐厅名(分店)]_[YYYYMMDD]
👉 https://docs.qq.com/aio/[文档ID]

---

## 异常处理

| 问题 | 原因 | 处理 |
|------|------|------|
| 点评滑块验证 | 高频访问 | 等待3-5分钟再试 |
| AI 生图失败 | API 超时/报错 | 重试或换输入图 |
| 图片上传失败 | base64过长 | 脚本通过Python处理，大图也能传 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-05-02 | 初始版本 |
| 1.0.1 | 2026-05-02 | 修正平台描述 |
| 1.0.2 | 2026-05-02 | 移除mcporter，依赖tencent-docs skill |
| 1.0.3 | 2026-05-02 | token优化，压缩图片控制开销 |
| 1.0.4 | 2026-05-02 | 新增scripts/publish_note.sh发布脚本 |
| 1.0.5 | 2026-05-02 | 放宽压缩阈值，手机端清晰 |
| **1.1.0** | **2026-05-02** | **集成tandian-image-skills，完整图→文→发布流水线** |
