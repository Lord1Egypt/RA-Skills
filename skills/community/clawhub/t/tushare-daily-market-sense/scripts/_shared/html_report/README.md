# shared/html_report

仓库级 HTML 报告渲染器。各 skill 在 SKILL.md 工作流末端调用它,把 Markdown 研报 + JSON 证据包套成一份自包含的 HTML 单页。

## 调用方式

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "_shared"))

from html_report import HtmlReportBuilder, ChartHook

builder = HtmlReportBuilder(
    title="600519 贵州茅台 基本面分析",
    theme="default",                    # "default" 或 "print"
    meta_text="600519 · 贵州茅台 · 2026-05-23",
)
builder.add_chart_hook(ChartHook(
    name="valuation-band",
    payload={"bands": {...}, "series": [...]},
    js=VALUATION_BAND_JS,               # 字符串,在 IIFE 内执行,可读 __payload
))
builder.add_ui_decoration(SUMMARY_HERO_JS)  # 可选:把 "核心判断" 段升格成 hero 卡

html = builder.render(markdown_text)        # validate_text_preserved 自动跑
Path(out_path).write_text(html, encoding="utf-8")
```

## ChartHook JS 协议

每个 hook 的 JS 在专属 IIFE 中执行,渲染器自动注入:

- `__payload` — 当前 hook 的 payload(已经 JSON.parse)
- `window.__chartData` — 整个 envelope `{ hookName: payload, ... }`,供需要跨 hook 取数据的场景

```js
/* 示例 hook JS */
const root = document.getElementById("report-body");
if (!root) return;
const series = __payload.series || [];
// ... 构造 SVG 插入到 root
```

## 主题

- `default`:Claude-UI 暖橙 + 数据红绿,默认值
- `print`:黑白衬线、A4 友好、移除 hover/动效,适合导出 PDF 或邮件附件

新增主题:在 `themes/` 下放 `<name>.css`,`list_themes()` 自动发现。SVG 图表色板由各 hook JS 控制,主题层不强制约束。

## 同步路径

仓库源码位于 `shared/html_report/`。通过 `skill-sync.yaml` 的 `shared.bundles` 同步到目标 skill 的 `scripts/_shared/html_report/`,各 skill 用 `sys.path` 引导导入。
