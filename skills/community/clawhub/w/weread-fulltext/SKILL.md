---
name: weread-fulltext
description: 微信读书整本书全文导出为 Markdown。两层架构：采集层（大视口画布扫掠 + 真实键盘翻页，零注入零写入）+ 离线重建层（官方章节骨架 + 证据化拼接 + 全程溯源）。支持 canvas 防拷贝渲染书籍。产物带来源索引与质量报告。
---

# 微信读书全文导出 (weread-fulltext) v2

把微信读书里一本书的**完整正文**导出为可溯源的 Markdown。

## 两层架构

| 层 | 依赖 | 职责 |
| --- | --- | --- |
| **采集层** | 浏览器登录态 | 大视口（1920×2160）下画布容纳整章，真实键盘 ArrowRight 逐跨页推进，被动 `toDataURL` 导出画布 |
| **重建层** | 无（纯离线） | 官方 chapterUid 骨架 + 阅读顺序指针分章 + 证据化拼接（包含/重叠/页序连续），OCR 缓存键 = 图片 SHA-256，产出正文 + source_map.json + quality_report.md |

## 使用

```bash
# 0) 依赖（一次性）
pip install -r scripts/requirements.txt
playwright install chromium

# 1) 首次登录（弹出浏览器，微信扫码）
python scripts/export_fulltext.py --login

# 2) 采集 + 重建一本书
python scripts/export_fulltext.py --book-id 3300229133 --out ./exports

# 3) 仅离线重建已有运行（不打开浏览器）
python scripts/export_fulltext.py --rebuild-run ./exports/3300229133/run_YYYYMMDD_HHMMSS

# 可选：--headless --max-spreads 60
```

产物在 `exports/<bookId>/run_<时间戳>/` 下：`fde_rebuilt.md`（正文，问题章节带状态标注 + 备选捕获附录）、`source_map.json`（段落→图片→OCR 行溯源）、`quality_report.md`、`manifest.jsonl`、`run_meta.json`（起止位置与停止原因）、`spreads/` 截图。

## 账号安全设计

- **只读不写**：不调用写接口，不写想法/划线/书架
- **原生翻页**：只发真实键盘方向键；不注入 JS、不 hook 任何页面对象、不拦截请求
- **拟人节奏**：翻页间隔 2.3–3.4s 随机；采集前自动回退到书首并记录实际位置
- **零第三方窗口**；OCR 全程本地（RapidOCR）
- ⚠️ 自动化仍有理论风险，**建议优先小号**；一次一本，勿连续批量

## 已验证能力（FDE 一书，52 章实测）

- 48/52 章 OK（字数覆盖 96–100%）；4 个例外均为结构性页面（封面无正文、版权页为背景图、两枚分隔页）
- 长章跨跨页自动拼接（2.3 章三片段 → 98%）；同章重复渲染自动识别为备选，不静默丢弃
- 重复的 7.1 异文已定性为 OCR 行级方差，处置记录在 quality_report.md

## 未验证范围与限制（诚实声明）

- **整书完整性**：质量报告只主张"现有材料已全部处理 + 章节归属可信 + 拼接有据"；字数比是异常筛查指标，不是完整性证明。整书完整取决于采集覆盖（见 run_meta.json 的 stop_reason）
- OCR 非逐字精确：中文接近无损，英文专名有 I/l 混淆（内置小词典校正，无法覆盖的保留原文）；个别错字建议对照原文核验
- 版权页/图片页正文为图片渲染，OCR 不可得，不计入完整性
- 采集层已在真实账号环境跑通，但独立脚本路径（全新 Playwright + 扫码登录）与 FDE 成品所用环境不完全相同，首次使用建议小号验证

## 与其他方案的区别

- 划线类工具（obsidian-weread-plugin、weread2notion）：只有划线，无正文
- weread-dl（ClawHub）：依赖 DOM 绝对定位字符，canvas 防拷贝书拿不到正文
- 本 skill：canvas 书可用；v2 起带来源溯源与质量报告，错误可回溯到原图
