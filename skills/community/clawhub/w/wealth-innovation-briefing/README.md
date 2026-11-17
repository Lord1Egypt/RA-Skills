# wealth-innovation-briefing

一个可复用的 **WorkBuddy Skill**：一键生成《金融创新简报（财富管理）》竖版 A4 海报 PDF。

面向银行/财富管理从业者（尤其某股份制银行财富管理条线），每日/每周自动采集私人银行、存款理财、公募私募、银保、信托等领域的**产品权益 / 活动场景创新动态**，结构化输出 30 条案例，渲染成"高大上、可邮件分享、适合向领导汇报"的海报式 PDF。

## 功能特性

- **6 大方向 × 5 条 = 30 条**创新动态：存款理财 / 理财货架 / 公募基金 / 私募与高净值 / 银保协同 / 信托创新。
- 每条必含：**具体公司 + 新闻链接 + 事件说明(≥100字) + 创新点 + 某股份制银行学习点**。
- 每方向配 **关键趋势 / 核心洞察 / 银行行动建议**。
- 输出 **竖版 A4 海报 PDF**（封面 → 摘要 → 6 方向导读页 + 案例页 + 小结卡，共 20 页）。
- **数据与样式解耦**：版式模板一次性写好，每次只换数据变量即可，不动 CSS。

## 目录结构

```
wealth-innovation-briefing/
├── SKILL.md                      # Skill 主说明（WorkBuddy 调用入口）
├── README.md                     # 本文件
├── LICENSE
├── .gitignore
└── references/
    ├── build_briefing_template.py  # 海报版式构建模板（只覆盖变量后 build()）
    ├── convert_pdf.py             # 用本地缓存 Chromium 渲染 A4 PDF
    └── content_template.py        # DIRECTIONS / EXTRA 数据结构模板
```

## 快速使用

1. 准备数据文件 `content_20260728.py`，导出 `DIRECTIONS`（6 方向 × 5 条）与 `EXTRA`（按方向标题索引）：

   ```python
   DIRECTIONS = [{"title": "存款理财：...", "subtitle": "...", "items": [
       {"title": "...", "source": "...", "link": "https://...",
        "body": "≥100字...", "innovation": "...", "learning": "..."},
       # ... 每方向 5 条
   ]}, ...]
   EXTRA = {"存款理财：...": {"tags": [...], "insight": "...", "action": "..."}, ...}
   ```

2. 写构建脚本 `build_20260728.py`：

   ```python
   import sys, os
   sys.path.insert(0, os.path.dirname(__file__))
   import build_briefing_template as tpl
   from content_20260728 import DIRECTIONS, EXTRA
   tpl.today = "2026年7月28日"
   tpl.DIRECTIONS = DIRECTIONS
   tpl.EXTRA = EXTRA
   tpl.SUMMARY_LEAD = "三条主线摘要……"
   if __name__ == '__main__':
       tpl.build()          # 产出 briefing.html
   ```

3. 渲染 PDF（依赖 `pip install playwright`，复用本机已缓存的 Chromium）：

   ```bash
   python build_20260728.py
   python convert_pdf.py    # 产出 金融创新简报_财富管理_2026-07-28.pdf
   ```

## 已知坑（已踩过）

- `convert_pdf.py` 的 `OUT_DIR` **不能被批量 sed 替换误改**——那会把工作目录名一起改掉导致 `net::ERR_FILE_NOT_FOUND`。
- `EXTRA` 的键必须 **严格等于** `DIRECTIONS[].title`（含 `：` 前后文），否则导读页/小结卡内容为空。
- 浏览器里 HTML 是连续滚动的（屏幕不认 `@page`），但 PDF 渲染会按 `page-break-after` 正确分页，属正常现象。

## License

MIT © forrestneo
