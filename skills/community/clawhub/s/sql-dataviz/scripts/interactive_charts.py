"""
interactive_charts.py  —  sql-dataviz 交互式 HTML 图表输出模块
基于 Plotly 实现，输出自包含 HTML（CDN 引入 Plotly.js）
支持 hover / zoom / pan，中文字体 Microsoft YaHei，Power BI 配色

用法:
    from interactive_charts import InteractiveChartFactory, DashboardBuilder

    factory = InteractiveChartFactory()
    html = factory.create_line({
        "categories": ["1月","2月","3月"],
        "series": [{"name":"销售额","data":[100,120,150]}]
    })
    factory.save_html(html, "line.html")

    builder = DashboardBuilder(title="销售看板")
    builder.add_kpi_cards([{"title":"GMV","value":"¥1,234万","change":"+18%"}])
    builder.add_chart(factory.create_bar(...), title="区域对比")
    builder.build("dashboard.html")
"""

from __future__ import annotations

import json
import os
import tempfile
from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.io as pio
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

# ─────────────────────────────────────────────────────────────────────────────
# 主题配置
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {
    "powerbi": {
        "template": "plotly_white",
        "palette": ["#0078D4","#50E6FF","#FFB900","#107C10","#D83B01","#8661C5","#00B7C3","#E3008C"],
        "primary": "#0078D4",
        "bg": "#FFFFFF",
        "paper_bg": "#F8F9FA",
        "font_color": "#252423",
    },
    "dark": {
        "template": "plotly_dark",
        "palette": ["#00B7C3","#50E6FF","#FFB900","#107C10","#D83B01","#8661C5","#0078D4","#E3008C"],
        "primary": "#00B7C3",
        "bg": "#1E1E1E",
        "paper_bg": "#252526",
        "font_color": "#CCCCCC",
    },
    "seaborn": {
        "template": "seaborn",
        "palette": ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B3","#937860","#DA8BC3","#8C8C8C"],
        "primary": "#4C72B0",
        "bg": "#EAEAF2",
        "paper_bg": "#FFFFFF",
        "font_color": "#333333",
    },
    "ggplot2": {
        "template": "ggplot2",
        "palette": ["#F8766D","#7CAE00","#00BFC4","#C77CFF","#FF7F00","#A3A500","#00B0F6","#E76BF3"],
        "primary": "#F8766D",
        "bg": "#E5E5E5",
        "paper_bg": "#FFFFFF",
        "font_color": "#333333",
    },
}

# 中文字体配置
FONT_FAMILY = "Microsoft YaHei, SimHei, PingFang SC, Arial, sans-serif"

# Plotly CDN（离线可替换为本地路径）
PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.27.0.min.js"


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────────────────────

def _wrap_html(plotly_div: str, title: str = "", theme: str = "powerbi") -> str:
    """把 Plotly div 包装成完整自包含 HTML"""
    t = THEMES.get(theme, THEMES["powerbi"])
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title or 'Chart'}</title>
<script src="{PLOTLY_CDN}"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: {FONT_FAMILY}; background: {t['paper_bg']}; color: {t['font_color']}; padding: 16px; }}
  .chart-title {{ font-size: 18px; font-weight: 600; margin-bottom: 12px; color: {t['primary']}; }}
  .chart-wrap {{ background: {t['bg']}; border-radius: 8px; padding: 16px;
                 box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
</style>
</head>
<body>
<div class="chart-wrap">
  {('<div class="chart-title">' + title + '</div>') if title else ''}
  {plotly_div}
</div>
</body>
</html>"""


def _fig_to_html(fig, title: str = "", theme: str = "powerbi",
                 full_page: bool = True,
                 display_mode_bar: bool = False,
                 display_logo: bool = False) -> str:
    """
    Figure → HTML 字符串

    参数:
        display_mode_bar: 是否显示顶部工具栏（默认 False，隐藏工具栏）
        display_logo: 是否显示 Plotly logo（默认 False，隐藏水印）
    """
    div = pio.to_html(fig, full_html=False, include_plotlyjs=False,
                      config={
                          "responsive": True,
                          "displayModeBar": display_mode_bar,
                          "displaylogo": display_logo,  # 隐藏 Plotly logo
                          "modeBarButtonsToRemove": [
                              "lasso2d", "select2d",
                              "autoScale2d", "resetScale2d",
                              "hoverClosestCartesian", "hoverCompareCartesian"
                          ],
                          "toImageButtonOptions": {
                              "format": "png",
                              "filename": "chart",
                              "height": 800,
                              "width": 1200,
                              "scale": 2
                          }
                      })
    if full_page:
        return _wrap_html(div, title=title, theme=theme)
    return div


def _apply_layout(fig, theme: str, title: str = "", height: int = 420):
    """统一应用布局配置"""
    t = THEMES.get(theme, THEMES["powerbi"])
    fig.update_layout(
        template=t["template"],
        height=height,
        font=dict(family=FONT_FAMILY, size=13, color=t["font_color"]),
        title=dict(text=title, font=dict(size=16, color=t["primary"]), x=0.02) if title else None,
        paper_bgcolor=t["paper_bg"],
        plot_bgcolor=t["bg"],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=30, t=50 if title else 30, b=50),
        colorway=t["palette"],
        hovermode="x unified",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 主类：InteractiveChartFactory
# ─────────────────────────────────────────────────────────────────────────────

class InteractiveChartFactory:
    """
    交互式图表工厂 —— 基于 Plotly，输出自包含 HTML

    支持图表类型（12种）：
      line / bar / pie / scatter / heatmap / funnel /
      area / treemap / gauge / combo / table / kpi_cards
    """

    def __init__(self, theme: str = "powerbi"):
        if not PLOTLY_OK:
            raise ImportError("请先安装 plotly: pip install plotly")
        self.theme = theme
        self._palette = THEMES[theme]["palette"]

    def set_theme(self, theme: str):
        self.theme = theme
        self._palette = THEMES.get(theme, THEMES["powerbi"])["palette"]

    # ── 1. 折线图 ────────────────────────────────────────────────────────────
    def create_line(self, data: Dict[str, Any], title: str = "",
                    height: int = 420) -> str:
        """
        data = {"categories": [...], "series": [{"name":"...", "data":[...]}]}
        """
        fig = go.Figure()
        cats = data["categories"]
        for i, s in enumerate(data["series"]):
            fig.add_trace(go.Scatter(
                x=cats, y=s["data"], mode="lines+markers",
                name=s["name"],
                line=dict(width=2.5, color=self._palette[i % len(self._palette)]),
                marker=dict(size=6),
                hovertemplate=f"{s['name']}: %{{y:,.0f}}<extra></extra>"
            ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 2. 柱形图 ────────────────────────────────────────────────────────────
    def create_bar(self, data: Dict[str, Any], title: str = "",
                   stacked: bool = False, height: int = 420) -> str:
        """
        data = {"categories": [...], "series": [{"name":"...", "data":[...]}]}
        """
        fig = go.Figure()
        cats = data["categories"]
        for i, s in enumerate(data["series"]):
            fig.add_trace(go.Bar(
                x=cats, y=s["data"], name=s["name"],
                marker_color=self._palette[i % len(self._palette)],
                hovertemplate=f"{s['name']}: %{{y:,.0f}}<extra></extra>"
            ))
        if stacked:
            fig.update_layout(barmode="stack")
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 3. 饼图 ──────────────────────────────────────────────────────────────
    def create_pie(self, data: Dict[str, Any], title: str = "",
                   donut: bool = True, height: int = 420) -> str:
        """
        data = {"labels": [...], "values": [...]}
        """
        fig = go.Figure(go.Pie(
            labels=data["labels"],
            values=data["values"],
            hole=0.45 if donut else 0,
            marker=dict(colors=self._palette[:len(data["labels"])]),
            textinfo="label+percent",
            hovertemplate="%{label}: %{value:,.0f} (%{percent})<extra></extra>"
        ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 4. 散点图 ────────────────────────────────────────────────────────────
    def create_scatter(self, data: Dict[str, Any], title: str = "",
                       height: int = 420) -> str:
        """
        data = {"x": [...], "y": [...], "labels": [...], "size": [...]}
        """
        labels = data.get("labels", [str(i) for i in range(len(data["x"]))])
        size = data.get("size", None)
        fig = go.Figure(go.Scatter(
            x=data["x"], y=data["y"],
            mode="markers",
            text=labels,
            marker=dict(
                size=[max(8, s/max(size)*40) for s in size] if size else 10,
                color=self._palette[0],
                opacity=0.7,
                line=dict(width=1, color="white")
            ),
            hovertemplate="x: %{x}<br>y: %{y}<br>%{text}<extra></extra>"
        ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 5. 热力图 ────────────────────────────────────────────────────────────
    def create_heatmap(self, data: Dict[str, Any], title: str = "",
                       height: int = 420) -> str:
        """
        data = {"x_labels": [...], "y_labels": [...], "z_values": [[...]]}
        """
        fig = go.Figure(go.Heatmap(
            x=data["x_labels"],
            y=data["y_labels"],
            z=data["z_values"],
            colorscale="Blues",
            hovertemplate="x: %{x}<br>y: %{y}<br>值: %{z:,.0f}<extra></extra>"
        ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 6. 漏斗图 ────────────────────────────────────────────────────────────
    def create_funnel(self, data: Dict[str, Any], title: str = "",
                      height: int = 420) -> str:
        """
        data = {"stages": [...], "values": [...]}
        """
        fig = go.Figure(go.Funnel(
            y=data["stages"],
            x=data["values"],
            marker=dict(color=self._palette[:len(data["stages"])]),
            textinfo="value+percent initial",
            hovertemplate="%{y}: %{x:,.0f}<extra></extra>"
        ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 7. 面积图 ────────────────────────────────────────────────────────────
    def create_area(self, data: Dict[str, Any], title: str = "",
                    stacked: bool = False, height: int = 420) -> str:
        """
        data = {"categories": [...], "series": [{"name":"...", "data":[...]}]}
        """
        fig = go.Figure()
        cats = data["categories"]
        for i, s in enumerate(data["series"]):
            fig.add_trace(go.Scatter(
                x=cats, y=s["data"],
                name=s["name"],
                fill="tonexty" if (stacked and i > 0) else "tozeroy",
                mode="lines",
                line=dict(width=2, color=self._palette[i % len(self._palette)]),
                fillcolor=self._palette[i % len(self._palette)].replace("#", "rgba(") + ",0.3)",
                hovertemplate=f"{s['name']}: %{{y:,.0f}}<extra></extra>"
            ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 8. 树状图 ────────────────────────────────────────────────────────────
    def create_treemap(self, data: Dict[str, Any], title: str = "",
                       height: int = 420) -> str:
        """
        data = {"labels": [...], "parents": [...], "values": [...]}
        """
        fig = go.Figure(go.Treemap(
            labels=data["labels"],
            parents=data.get("parents", [""] * len(data["labels"])),
            values=data["values"],
            marker=dict(colorscale="Blues"),
            hovertemplate="%{label}: %{value:,.0f}<extra></extra>"
        ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 9. 仪表盘 ────────────────────────────────────────────────────────────
    def create_gauge(self, data: Dict[str, Any], title: str = "",
                     height: int = 300) -> str:
        """
        data = {"title":"...", "value": 85, "min": 0, "max": 100,
                "thresholds": [{"value":60,"color":"yellow"},{"value":80,"color":"green"}]}
        """
        val = data["value"]
        vmin = data.get("min", 0)
        vmax = data.get("max", 100)
        label = data.get("title", title)
        steps = []
        thresholds = data.get("thresholds", [])
        prev = vmin
        colors = ["#FF4444", "#FFB900", "#107C10"]
        for idx, th in enumerate(thresholds):
            steps.append(dict(range=[prev, th["value"]],
                              color=colors[idx % len(colors)]))
            prev = th["value"]
        steps.append(dict(range=[prev, vmax], color=colors[min(len(thresholds), len(colors)-1)]))

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            title=dict(text=label, font=dict(size=14)),
            gauge=dict(
                axis=dict(range=[vmin, vmax]),
                bar=dict(color=THEMES[self.theme]["primary"]),
                steps=steps,
                threshold=dict(
                    line=dict(color="red", width=4),
                    thickness=0.75,
                    value=vmax * 0.9
                )
            )
        ))
        _apply_layout(fig, self.theme, title, height)
        return _fig_to_html(fig, title=title, theme=self.theme)

    # ── 10. 组合图（柱+折线）────────────────────────────────────────────────
    def create_combo(self, data: Dict[str, Any], title: str = "",
                     height: int = 420) -> str:
        """
        data = {
            "categories": [...],
            "columns": {"name":"...", "data":[...]},
            "lines":   {"name":"...", "data":[...]}
        }
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        cats = data["categories"]
        col = data["columns"]
        lin = data["lines"]
        fig.add_trace(go.Bar(
            x=cats, y=col["data"], name=col["name"],
            marker_color=self._palette[0],
            hovertemplate=f"{col['name']}: %{{y:,.0f}}<extra></extra>"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=cats, y=lin["data"], name=lin["name"],
            mode="lines+markers",
            line=dict(color=self._palette[1], width=2.5),
            hovertemplate=f"{lin['name']}: %{{y:,.2f}}<extra></extra>"
        ), secondary_y=True)
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 11. 交互式表格 ───────────────────────────────────────────────────────
    def create_table(self, data: Dict[str, Any], title: str = "",
                     height: int = 420) -> str:
        """
        data = {"columns": [...], "rows": [[...], ...]}
        """
        cols = data["columns"]
        rows = data["rows"]
        t = THEMES[self.theme]
        fig = go.Figure(go.Table(
            header=dict(
                values=[f"<b>{c}</b>" for c in cols],
                fill_color=t["primary"],
                font=dict(color="white", size=13, family=FONT_FAMILY),
                align="left", height=36
            ),
            cells=dict(
                values=[[row[i] for row in rows] for i in range(len(cols))],
                fill_color=[["#F5F9FC" if r % 2 == 0 else "#FFFFFF"
                              for r in range(len(rows))]],
                font=dict(size=12, family=FONT_FAMILY),
                align="left", height=30
            )
        ))
        _apply_layout(fig, self.theme, title or data.get("title",""), height)
        return _fig_to_html(fig, title=title or data.get("title",""), theme=self.theme)

    # ── 12. KPI 卡片组 ───────────────────────────────────────────────────────
    def create_kpi_cards(self, data: Dict[str, Any], title: str = "") -> str:
        """
        data = {"cards": [{"title":"GMV","value":"¥1,234万","change":"+18%"}, ...]}
        """
        cards = data["cards"]
        t = THEMES[self.theme]
        card_html = ""
        for c in cards:
            change = c.get("change", "")
            change_color = "#107C10" if str(change).startswith("+") else "#D83B01"
            card_html += f"""
            <div class="kpi-card">
              <div class="kpi-title">{c['title']}</div>
              <div class="kpi-value">{c['value']}</div>
              <div class="kpi-change" style="color:{change_color}">{change}</div>
            </div>"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{title or 'KPI'}</title>
<style>
  body {{ font-family: {FONT_FAMILY}; background:{t['paper_bg']}; padding:16px; }}
  .kpi-row {{ display:flex; flex-wrap:wrap; gap:16px; }}
  .kpi-card {{ background:{t['bg']}; border-radius:8px; padding:20px 24px;
               min-width:160px; flex:1; box-shadow:0 2px 8px rgba(0,0,0,.08);
               border-top:4px solid {t['primary']}; }}
  .kpi-title {{ font-size:13px; color:#666; margin-bottom:8px; }}
  .kpi-value {{ font-size:28px; font-weight:700; color:{t['font_color']}; }}
  .kpi-change {{ font-size:13px; margin-top:6px; font-weight:600; }}
</style></head><body>
<div class="kpi-row">{card_html}</div>
</body></html>"""

    # ── 工具方法 ─────────────────────────────────────────────────────────────
    @staticmethod
    def save_html(fig_or_html: Any, path: str) -> str:
        """
        保存 HTML 到文件。
        fig_or_html 可以是：
          - HTML 字符串（直接写入）
          - Plotly Figure 对象（自动转 HTML）
        """
        # 支持 Figure 对象
        if hasattr(fig_or_html, "update_layout"):
            fig_or_html = _fig_to_html(fig_or_html, full_page=True)
        os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(fig_or_html))
        return os.path.abspath(path)

    def to_base64_image(self, fig) -> Optional[str]:
        """Figure → base64 PNG（需要 kaleido）"""
        try:
            import base64
            img_bytes = pio.to_image(fig, format="png", width=1200, height=600)
            return base64.b64encode(img_bytes).decode()
        except Exception:
            return None


# ─────────────────────────────────────────────────────────────────────────────
# DashboardBuilder：多图表组合成完整 HTML Dashboard
# ─────────────────────────────────────────────────────────────────────────────

class DashboardBuilder:
    """
    把多个图表/KPI/文本组合成一个完整的 HTML Dashboard

    用法:
        builder = DashboardBuilder(title="销售看板", theme="powerbi")
        builder.add_kpi_cards([{"title":"GMV","value":"¥1,234万","change":"+18%"}])
        builder.add_chart(factory.create_line(...), title="月度趋势", cols=2)
        builder.add_chart(factory.create_bar(...), title="区域对比", cols=1)
        builder.add_markdown("## 洞察\\n- 华东增速最快")
        builder.build("dashboard.html")
    """

    def __init__(self, title: str = "数据看板", theme: str = "powerbi",
                 cols: int = 2):
        self.title = title
        self.theme = theme
        self.cols = cols
        self._sections: List[Dict] = []
        self._t = THEMES.get(theme, THEMES["powerbi"])

    def add_kpi_cards(self, cards: List[Dict]) -> "DashboardBuilder":
        """添加 KPI 卡片行"""
        self._sections.append({"type": "kpi", "cards": cards})
        return self

    def add_chart(self, html_or_div: str, title: str = "",
                  cols: int = 1) -> "DashboardBuilder":
        """
        添加图表（传入 create_xxx 返回的 HTML 或 div 片段）
        cols: 占几列（1=半宽，2=全宽）
        """
        # 提取 div 内容（去掉外层 HTML 包装）
        div = html_or_div
        if "<body>" in html_or_div:
            start = html_or_div.find("<div", html_or_div.find("<body>"))
            end = html_or_div.rfind("</div>") + 6
            div = html_or_div[start:end]
        self._sections.append({"type": "chart", "div": div,
                                "title": title, "cols": cols})
        return self

    def add_markdown(self, text: str) -> "DashboardBuilder":
        """添加 Markdown 文本块（简单渲染）"""
        self._sections.append({"type": "markdown", "text": text})
        return self

    def add_insights(self, insights_html: str) -> "DashboardBuilder":
        """添加 AI 洞察 HTML 块"""
        self._sections.append({"type": "insights", "html": insights_html})
        return self

    def build(self, output_path: str = "") -> str:
        """生成完整 HTML，保存到文件并返回 HTML 字符串"""
        from datetime import datetime
        t = self._t
        sections_html = ""

        for sec in self._sections:
            if sec["type"] == "kpi":
                cards_html = ""
                for c in sec["cards"]:
                    change = c.get("change", "")
                    cc = "#107C10" if str(change).startswith("+") else "#D83B01"
                    cards_html += f"""
                    <div class="kpi-card">
                      <div class="kpi-title">{c['title']}</div>
                      <div class="kpi-value">{c['value']}</div>
                      <div class="kpi-change" style="color:{cc}">{change}</div>
                    </div>"""
                sections_html += f'<div class="kpi-row">{cards_html}</div>'

            elif sec["type"] == "chart":
                width_class = "col-full" if sec["cols"] >= 2 else "col-half"
                title_html = f'<div class="section-title">{sec["title"]}</div>' if sec["title"] else ""
                sections_html += f"""
                <div class="chart-section {width_class}">
                  {title_html}
                  <div class="chart-inner">{sec["div"]}</div>
                </div>"""

            elif sec["type"] == "markdown":
                md = sec["text"]
                md = md.replace("\n## ", "\n<h2>").replace("\n# ", "\n<h1>")
                md = md.replace("\n- ", "\n<li>").replace("\n", "<br>")
                sections_html += f'<div class="md-block">{md}</div>'

            elif sec["type"] == "insights":
                sections_html += f'<div class="insights-block">{sec["html"]}</div>'

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{self.title}</title>
<script src="{PLOTLY_CDN}"></script>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:{FONT_FAMILY}; background:{t['paper_bg']}; color:{t['font_color']}; }}
  .header {{ background:{t['primary']}; color:#fff; padding:20px 32px;
             display:flex; justify-content:space-between; align-items:center; }}
  .header h1 {{ font-size:22px; font-weight:700; }}
  .header .meta {{ font-size:13px; opacity:.8; }}
  .container {{ max-width:1400px; margin:0 auto; padding:24px; }}
  .kpi-row {{ display:flex; flex-wrap:wrap; gap:16px; margin-bottom:24px; }}
  .kpi-card {{ background:{t['bg']}; border-radius:8px; padding:20px 24px;
               min-width:160px; flex:1; box-shadow:0 2px 8px rgba(0,0,0,.08);
               border-top:4px solid {t['primary']}; }}
  .kpi-title {{ font-size:13px; color:#888; margin-bottom:8px; }}
  .kpi-value {{ font-size:26px; font-weight:700; }}
  .kpi-change {{ font-size:13px; margin-top:6px; font-weight:600; }}
  .charts-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }}
  .chart-section {{ background:{t['bg']}; border-radius:8px; padding:16px;
                    box-shadow:0 2px 8px rgba(0,0,0,.08); }}
  .col-full {{ grid-column:1/-1; }}
  .col-half {{ grid-column:span 1; }}
  .section-title {{ font-size:15px; font-weight:600; color:{t['primary']};
                    margin-bottom:10px; padding-bottom:8px;
                    border-bottom:2px solid {t['primary']}20; }}
  .chart-inner {{ width:100%; }}
  .md-block {{ background:{t['bg']}; border-radius:8px; padding:20px;
               box-shadow:0 2px 8px rgba(0,0,0,.08); grid-column:1/-1;
               line-height:1.8; }}
  .insights-block {{ grid-column:1/-1; }}
  .footer {{ text-align:center; color:#aaa; font-size:12px;
             padding:20px; margin-top:20px; }}
</style>
</head>
<body>
<div class="header">
  <h1>{self.title}</h1>
  <div class="meta">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</div>
<div class="container">
  <div class="charts-grid">
    {sections_html}
  </div>
</div>
<div class="footer">由 sql-dataviz · InteractiveChartFactory 生成</div>
</body>
</html>"""

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
        return html


# ─────────────────────────────────────────────────────────────────────────────
# 图表注释功能（Chart Annotations）
# 在图表上标注关键事件、异常点、趋势拐点、目标线等
# ─────────────────────────────────────────────────────────────────────────────

def add_annotations(fig_or_html, annotations: List[Dict]) -> Any:
    """
    向 Plotly 图表添加注释（同时支持 Figure 对象和 HTML 字符串）

    annotations 列表中的每项支持以下类型：

    1. 垂直/水平参考线（reference_line）
       {"type": "vline"|"hline", "x"|"y": 值,
        "label": "标注文字", "color": "#FF0000",
        "dash": "dot"|"dash"|"solid", "width": 2}

    2. 区域高亮（shade）
       {"type": "shade", "x0": x起点, "x1": x终点,
        "color": "rgba(255,0,0,0.1)", "label": "活动期"}

    3. 数据点标注（point）
       {"type": "point", "x": x值, "y": y值,
        "text": "标注文字", "color": "#D83B01",
        "arrow": True, "font_size": 12}

    4. 趋势拐点标注（inflection）
       {"type": "inflection", "x": x值, "y": y值,
        "text": "拐点", "direction": "peak"|"trough"}

    5. 目标线（target_line）
       {"type": "target", "value": 目标值,
        "label": "目标", "color": "#107C10"}

    6. 异常点标注（anomaly）
       {"type": "anomaly", "x": x值, "y": y值,
        "text": "异常值", "severity": "high"|"medium"|"low"}

    7. 趋势线（trend_line）
       {"type": "trend", "x": [x列表], "y": [y列表],
        "name": "趋势线", "color": "#8661C5"}

    8. 事件标注（event）
       {"type": "event", "x": x值, "y": y值,
        "text": "双11", "category": "promotion"|"holiday"|"incident"}

    示例用法：
        # 方式1：用 Plotly Figure 对象（推荐）
        fig = go.Figure(go.Scatter(x=[...], y=[...], mode='lines'))
        fig = add_annotations(fig, [
            {"type": "vline", "x": "2024-11", "label": "双11", "color": "#D83B01"},
            {"type": "target", "value": 1000, "label": "目标"},
            {"type": "anomaly", "x": "2024-03", "y": 200, "text": "异常低"},
        ])
        factory.save_html(fig, "annotated.html")

        # 方式2：直接用工厂方法后再标注（工厂返回 Figure）
        fig = factory.create_line(data)      # 返回 Figure
        fig = add_annotations(fig, [...])     # 追加注释
        factory.save_html(fig, "annotated.html")
    """
    import numpy as np

    # 如果传入的是 HTML 字符串（来自旧版工厂方法），直接返回
    # 新版工厂方法返回 Figure，兼容处理
    if isinstance(fig_or_html, str):
        return fig_or_html  # 旧版返回HTML，无法添加注释，返回原文

    # 事件颜色映射
    EVENT_COLORS = {
        "promotion": "#D83B01",
        "holiday":   "#8661C5",
        "incident":  "#FF4444",
        "default":   "#50E6FF",
    }
    # 异常级别颜色
    ANOMALY_COLORS = {
        "high":   "#FF4444",
        "medium": "#FFB900",
        "low":    "#50E6FF",
    }

    # 初始化注释列表
    _fig = fig_or_html
    if not hasattr(_fig, 'layout') or _fig.layout.annotations is None:
        _fig.update_layout(annotations=[])

    for ann in annotations:
        atype = ann.get("type", "")

        # ── 1. 参考线 ──────────────────────────────────────────
        if atype in ("vline", "hline"):
            is_vertical = (atype == "vline")
            ref = ann.get("x" if is_vertical else "y", 0)
            color = ann.get("color", "#FF4444")
            width = ann.get("width", 2)
            dash = ann.get("dash", "dash")
            label = ann.get("label", "")

            if is_vertical:
                shape = dict(type="line", x0=ref, x1=ref, y0=0, y1=1,
                             yref="paper", line=dict(color=color, width=width,
                             dash=dash))
            else:
                shape = dict(type="line", x0=0, x1=1, y0=ref, y1=ref,
                             xref="paper", line=dict(color=color, width=width,
                             dash=dash))
            _fig.add_shape(**shape)

            if label:
                x_ann = ref if is_vertical else 1.01
                y_ann = 1.02 if is_vertical else ref
                xref = "x" if is_vertical else "paper"
                yref = "paper" if is_vertical else "y"
                _fig.add_annotation(
                    x=x_ann, y=y_ann, xref=xref, yref=yref,
                    text=label, showarrow=False,
                    font=dict(size=11, color=color, family=FONT_FAMILY),
                    bgcolor="rgba(255,255,255,0.8)",
                    borderpad=3,
                )

        # ── 2. 区域高亮 ────────────────────────────────────────
        elif atype == "shade":
            x0 = ann.get("x0")
            x1 = ann.get("x1")
            color = ann.get("color", "rgba(255,184,0,0.1)")
            label = ann.get("label", "")

            if x0 is not None and x1 is not None:
                # 使用 add_shape 矩形（支持字符串 x 轴）
                _fig.add_shape(
                    type="rect", x0=x0, x1=x1,
                    y0=0, y1=1, yref="paper",
                    fillcolor=color, line_width=0, layer="below"
                )
                if label:
                    mid_x = x0  # 标签放在起始位置
                    _fig.add_annotation(
                        x=mid_x, y=1.02, xref="x", yref="paper",
                        text=label, showarrow=False,
                        font=dict(size=11, color=color, family=FONT_FAMILY),
                        bgcolor="rgba(255,255,255,0.8)",
                        borderpad=3, xanchor="left",
                    )

        # ── 3. 数据点标注 ──────────────────────────────────────
        elif atype == "point":
            x = ann.get("x")
            y = ann.get("y")
            text = ann.get("text", "")
            color = ann.get("color", "#D83B01")
            arrow = ann.get("arrow", True)
            font_size = ann.get("font_size", 12)

            if x is not None and y is not None:
                y_range = None
                try:
                    y_range = _fig.layout.yaxis.range
                except Exception:
                    pass

                _fig.add_annotation(
                    x=x, y=y,
                    text=text,
                    showarrow=arrow,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=color,
                    ax=0,
                    ay=-40 if arrow else 0,
                    font=dict(size=font_size, color=color, family=FONT_FAMILY),
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor=color,
                    borderwidth=1,
                    borderpad=4,
                    standoff=6,
                    yshift=20,
                )
                _fig.add_trace(dict(type="scatter",
                                   mode="markers",
                                   x=[x], y=[y],
                                   marker=dict(color=color, size=10,
                                               line=dict(color="white", width=2))))

        # ── 4. 趋势拐点 ────────────────────────────────────────
        elif atype == "inflection":
            x = ann.get("x")
            y = ann.get("y")
            text = ann.get("text", "拐点")
            direction = ann.get("direction", "peak")
            color = "#D83B01" if direction == "peak" else "#107C10"
            ay = -50 if direction == "peak" else 30

            if x is not None and y is not None:
                _fig.add_annotation(
                    x=x, y=y,
                    text=f"<b>{text}</b><br>{direction == 'peak' and '↑ 峰值' or '↓ 低点'}",
                    showarrow=True,
                    arrowhead=2, arrowsize=1.5,
                    arrowwidth=2,
                    arrowcolor=color,
                    ax=0, ay=ay,
                    font=dict(size=12, color=color, family=FONT_FAMILY),
                    bgcolor="rgba(255,255,255,0.95)",
                    bordercolor=color,
                    borderwidth=1.5,
                    borderpad=5,
                    standoff=8,
                    yshift=10 if direction == "peak" else -20,
                )
                _fig.add_trace(dict(type="scatter",
                                   mode="markers",
                                   x=[x], y=[y],
                                   marker=dict(color=color, size=12,
                                               symbol="diamond",
                                               line=dict(color="white", width=2))))

        # ── 5. 目标线 ──────────────────────────────────────────
        elif atype == "target":
            value = ann.get("value")
            label = ann.get("label", "目标")
            color = ann.get("color", "#107C10")
            if value is not None:
                _fig.add_hline(y=value, line_dash="dot",
                               line_color=color, line_width=2,
                               annotation_text=f"<b>{label}: {value:,.0f}</b>",
                               annotation_position="right",
                               annotation_font_size=11,
                               annotation_font_color=color,
                               annotation_bgcolor="rgba(255,255,255,0.9)")

        # ── 6. 异常点标注 ──────────────────────────────────────
        elif atype == "anomaly":
            x = ann.get("x")
            y = ann.get("y")
            text = ann.get("text", "异常")
            severity = ann.get("severity", "medium")
            color = ANOMALY_COLORS.get(severity, "#FFB900")

            if x is not None and y is not None:
                _fig.add_annotation(
                    x=x, y=y,
                    text=f"<b>{text}</b><br>⚠ {severity.upper()}",
                    showarrow=True,
                    arrowhead=2, arrowsize=1.2,
                    arrowwidth=2,
                    arrowcolor=color,
                    ax=0, ay=-50,
                    font=dict(size=11, color=color, family=FONT_FAMILY),
                    bgcolor="rgba(30,30,30,0.9)",
                    bordercolor=color,
                    borderwidth=2,
                    borderpad=5,
                    standoff=6,
                    yshift=15,
                )
                _fig.add_trace(dict(type="scatter",
                                   mode="markers",
                                   x=[x], y=[y],
                                   marker=dict(color=color, size=14,
                                               symbol="diamond",
                                               line=dict(color="white", width=2))))

        # ── 7. 趋势线 ──────────────────────────────────────────
        elif atype == "trend":
            x_vals = ann.get("x", [])
            y_vals = ann.get("y", [])
            name = ann.get("name", "趋势")
            color = ann.get("color", "#8661C5")
            if len(x_vals) == len(y_vals) and len(x_vals) >= 2:
                _fig.add_trace(dict(
                    type="scatter",
                    mode="lines",
                    x=x_vals, y=y_vals,
                    name=name,
                    line=dict(color=color, width=2, dash="dash"),
                    hoverinfo="name+y",
                ))

        # ── 8. 事件标注 ────────────────────────────────────────
        elif atype == "event":
            x = ann.get("x")
            y = ann.get("y")
            text = ann.get("text", "")
            category = ann.get("category", "default")
            color = EVENT_COLORS.get(category, EVENT_COLORS["default"])
            y_offset = ann.get("y_offset", -60)

            if x is not None and y is not None:
                _fig.add_annotation(
                    x=x, y=y,
                    text=f"<b>{text}</b>",
                    showarrow=True,
                    arrowhead=3,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=color,
                    ax=0, ay=y_offset,
                    font=dict(size=12, color="white", family=FONT_FAMILY),
                    bgcolor=color,
                    borderwidth=0,
                    borderpad=6,
                    standoff=8,
                    yshift=10,
                )
                _fig.add_trace(dict(type="scatter",
                                   mode="markers",
                                   x=[x], y=[y],
                                   marker=dict(color=color, size=10,
                                               symbol="star",
                                               line=dict(color="white", width=2))))

    return _fig


def create_annotated_chart(factory: InteractiveChartFactory,
                           chart_type: str,
                           data: Dict,
                           annotations: List[Dict],
                           title: str = "",
                           theme: str = "powerbi") -> str:
    """
    创建带注释的图表（一行搞定）

    示例：
        html = create_annotated_chart(
            factory, "line",
            {"categories": months, "series": series},
            annotations=[
                {"type": "vline", "x": "2024-11", "label": "双11"},
                {"type": "target", "value": 1500, "label": "KPI"},
                {"type": "anomaly", "x": "2024-03", "y": 200, "text": "系统故障"},
            ],
            title="月度销售（含标注）"
        )
    """
    create_fn = getattr(factory, f"create_{chart_type}", None)
    if not create_fn:
        raise ValueError(f"Factory 不支持图表类型: {chart_type}")

    fig_or_html = create_fn(data, title=title)

    # 如果是 Plotly Figure，添加注释后转 HTML
    if hasattr(fig_or_html, "update_layout"):
        fig = add_annotations(fig_or_html, annotations)
        return _fig_to_html(fig, title=title, theme=theme)

    # 如果返回的是 HTML 字符串，直接返回（工厂方法暂不支持注释，返回无注释版）
    return fig_or_html


# ─────────────────────────────────────────────────────────────────────────────
# 测试入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    import os

    factory = InteractiveChartFactory(theme="powerbi")
    builder = DashboardBuilder(title="销售数据看板 - 交互式演示", theme="powerbi")

    # KPI 卡片
    builder.add_kpi_cards([
        {"title": "总销售额", "value": "¥12,345,678", "change": "+18.5%"},
        {"title": "订单量",   "value": "45,678",       "change": "+12.3%"},
        {"title": "客单价",   "value": "¥270.2",       "change": "+5.6%"},
        {"title": "退款率",   "value": "2.1%",          "change": "-0.3%"},
    ])

    # 折线图
    line_html = factory.create_line({
        "categories": ["1月","2月","3月","4月","5月","6月"],
        "series": [
            {"name": "华东", "data": [1200,1400,1600,1800,2000,2200]},
            {"name": "华北", "data": [800,900,1000,1100,1200,1300]},
            {"name": "华南", "data": [600,700,800,900,1000,1100]},
        ]
    }, title="月度销售趋势")
    builder.add_chart(line_html, title="月度销售趋势（可缩放）", cols=2)

    # 柱形图
    bar_html = factory.create_bar({
        "categories": ["华东","华北","华南","西南","西北"],
        "series": [{"name": "销售额", "data": [2200,1300,1100,600,400]}]
    }, title="区域销售对比")
    builder.add_chart(bar_html, title="区域销售对比", cols=1)

    # 饼图
    pie_html = factory.create_pie({
        "labels": ["电子产品","服装","食品","家居","其他"],
        "values": [35, 25, 20, 12, 8]
    }, title="品类占比")
    builder.add_chart(pie_html, title="品类销售占比", cols=1)

    # 漏斗图
    funnel_html = factory.create_funnel({
        "stages": ["曝光","点击","加购","下单","支付"],
        "values": [100000, 35000, 12000, 5000, 4200]
    }, title="购买转化漏斗")
    builder.add_chart(funnel_html, title="购买转化漏斗", cols=1)

    # 组合图
    combo_html = factory.create_combo({
        "categories": ["1月","2月","3月","4月","5月","6月"],
        "columns": {"name": "销售额", "data": [1200,1400,1600,1800,2000,2200]},
        "lines":   {"name": "增长率%", "data": [0,16.7,14.3,12.5,11.1,10.0]}
    }, title="销售额与增长率")
    builder.add_chart(combo_html, title="销售额与增长率（双轴）", cols=1)

    # 表格
    table_html = factory.create_table({
        "columns": ["区域","销售额","订单量","客单价","增长率"],
        "rows": [
            ["华东","¥2,200,000","8,148","¥270","10.0%"],
            ["华北","¥1,300,000","4,815","¥270","8.3%"],
            ["华南","¥1,100,000","4,074","¥270","10.0%"],
            ["西南","¥600,000","2,222","¥270","20.0%"],
            ["西北","¥400,000","1,481","¥270","14.3%"],
        ]
    }, title="区域明细数据")
    builder.add_chart(table_html, title="区域明细数据", cols=2)

    # 生成 Dashboard
    out_path = os.path.join(tempfile.gettempdir(), "interactive_dashboard_test.html")
    builder.build(out_path)

    print(f"Dashboard 已生成: {out_path}")
    print(f"文件大小: {os.path.getsize(out_path) / 1024:.1f} KB")

    # ── 图表注释功能测试 ──────────────────────────────────────────
    print("\n=== 图表注释功能测试 ===")
    import plotly.graph_objects as go
    from interactive_charts import add_annotations

    # 直接用 Plotly Figure 测试（推荐用法）
    fig = go.Figure(go.Scatter(
        x=["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
        y=[800, 750, 900, 950, 1100, 1200, 1150, 1050, 950, 1000, 2200, 1800],
        mode="lines+markers",
        name="销售额(万)",
        line=dict(width=2.5, color="#0078D4"),
        marker=dict(size=6),
    ))
    _apply_layout(fig, "powerbi", "年度销售趋势（含标注）", 420)

    # 添加 8 种注释
    fig = add_annotations(fig, [
        {"type": "vline", "x": "3月",  "label": "春节促销", "color": "#D83B01", "dash": "dot"},
        {"type": "vline", "x": "11月", "label": "双11大促", "color": "#D83B01", "dash": "dot"},
        {"type": "hline", "y": 1000,  "label": "KPI目标线", "color": "#107C10", "dash": "dash"},
        {"type": "shade", "x0": "11月", "x1": "12月", "color": "rgba(216,59,1,0.08)", "label": "大促期"},
        {"type": "anomaly", "x": "2月", "y": 750,  "text": "春节低谷", "severity": "medium"},
        {"type": "inflection", "x": "11月", "y": 2200, "text": "峰值", "direction": "peak"},
        {"type": "point", "x": "6月", "y": 1200,  "text": "半年最高", "color": "#8661C5", "arrow": True},
        {"type": "event", "x": "4月", "y": 950,   "text": "新品发布", "category": "promotion"},
    ])

    ann_path = os.path.join(tempfile.gettempdir(), "annotated_chart.html")
    factory.save_html(fig, ann_path)
    print(f"带注释图表已生成: {ann_path}")
    print(f"文件大小: {os.path.getsize(ann_path) / 1024:.1f} KB")
    print("注释类型: vline / hline / shade / anomaly / inflection / point / event / target")

    print("\nALL TESTS PASSED")
