"""图表生成器。基于 DataFrame 生成独立的 ECharts 交互式 HTML 文件。"""

import sys
import json
import re
import html as html_module
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum

if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from core.exceptions import ChartError, ErrorCode
else:
    from .exceptions import ChartError, ErrorCode


ECHARTS_VERSION = '5.4.3'
ECHARTS_WORDCLOUD_VERSION = '2.1.0'
ECHARTS_CDN = f'https://cdn.jsdelivr.net/npm/echarts@{ECHARTS_VERSION}/dist/echarts.min.js'
ECHARTS_CDN_FALLBACK = f'https://unpkg.com/echarts@{ECHARTS_VERSION}/dist/echarts.min.js'
ECHARTS_WORDCLOUD_CDN = f'https://cdn.jsdelivr.net/npm/echarts-wordcloud@{ECHARTS_WORDCLOUD_VERSION}/dist/echarts-wordcloud.min.js'


class ChartType(Enum):
    LINE = 'line'
    BAR = 'bar'
    PIE = 'pie'
    SCATTER = 'scatter'
    AREA = 'area'
    RADAR = 'radar'
    HEATMAP = 'heatmap'
    TREEMAP = 'treemap'
    GRAPH = 'graph'
    BOXPLOT = 'boxplot'
    WATERFALL = 'waterfall'
    GAUGE = 'gauge'
    SANKEY = 'sankey'
    FUNNEL = 'funnel'
    SUNBURST = 'sunburst'
    WORDCLOUD = 'wordcloud'


def _sanitize_value(v):
    """将 NaN / Inf 转为 None，并将浮点数保留两位小数，确保 JSON 序列化后 ECharts 可正常渲染。"""
    if isinstance(v, float):
        if np.isnan(v) or np.isinf(v):
            return None
        return round(v, 2)
    return v


def _sanitize_series(data):
    """清洗列表中的 NaN / Inf 值。"""
    return [_sanitize_value(v) for v in data]


class ChartGenerator:

    def __init__(self, output_dir: str = './smart_charts_output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_chart(
        self,
        df: pd.DataFrame,
        chart_type: str,
        title: str = '数据图表',
        x_axis: Optional[str] = None,
        y_axis: Optional[List[str]] = None,
        transform_code: Optional[str] = None,
        width: int = 900,
        height: int = 560,
        auto_confirm: bool = False,
    ) -> Dict[str, str]:
        """生成图表。

        Args:
            auto_confirm: 是否跳过数据转换代码的用户确认。
                          默认 False（需要用户确认），与 SKILL.md 安全承诺一致。
                          当 LLM 在调用前已向用户展示并确认转换代码时，可设为 True。
        """
        if df.empty:
            raise ChartError("数据为空", ErrorCode.DATA_EMPTY)
        try:
            ct = ChartType(chart_type)
        except ValueError:
            supported = ', '.join(t.value for t in ChartType)
            raise ChartError(f"不支持的图表类型: {chart_type}，支持: {supported}", ErrorCode.CHART_TYPE_UNSUPPORTED)

        gen = getattr(self, f'_{ct.value}', None)
        if gen is None:
            raise ChartError(f"暂不支持该图表类型: {chart_type}", ErrorCode.CHART_TYPE_UNSUPPORTED)

        if transform_code:
            if __package__ is None:
                from core.data_transformer import DataTransformer
            else:
                from .data_transformer import DataTransformer
            df = DataTransformer(auto_confirm=auto_confirm).transform(df, transform_code)

        x_axis, y_axis = self._prepare_axes(df, chart_type, x_axis, y_axis)
        option = gen(df, x_axis, y_axis, title)
        html_path = self._save_html(option, title, width, height, chart_type)
        return {'html_path': str(html_path)}

    def generate_multi_charts(
        self,
        df: pd.DataFrame,
        chart_configs: List[Dict[str, Any]],
        width: int = 900,
        height: int = 560,
        auto_confirm: bool = False,
    ) -> Dict[str, Any]:
        """批量生成多个图表，返回 {'charts': [{'type', 'title', 'html_path'}]}"""
        results = []
        for cfg in chart_configs:
            try:
                r = self.generate_chart(
                    df=df,
                    chart_type=cfg.get('type', 'bar'),
                    title=cfg.get('title', ''),
                    x_axis=cfg.get('x_axis'),
                    y_axis=cfg.get('y_axis'),
                    transform_code=cfg.get('transform_code'),
                    width=cfg.get('width', width),
                    height=cfg.get('height', height),
                    auto_confirm=auto_confirm,
                )
                results.append({**cfg, 'html_path': r['html_path'], 'success': True})
            except Exception as e:
                results.append({**cfg, 'error': str(e), 'success': False})
        return {'charts': results}

    # ---- 轴自动检测 ----

    def _prepare_axes(self, df, chart_type, x_axis, y_axis) -> Tuple[str, List[str]]:
        if x_axis is None:
            date_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns
            cat_cols = df.select_dtypes(include=['object', 'string', 'category']).columns
            x_axis = date_cols[0] if len(date_cols) > 0 else (cat_cols[0] if len(cat_cols) > 0 else df.columns[0])

        if y_axis is None:
            avail = [c for c in df.columns if c != x_axis]
            nums = df[avail].select_dtypes(include=[np.number]).columns.tolist()
            y_axis = nums[:5] if nums else avail[:3]
        elif isinstance(y_axis, str):
            y_axis = [y_axis]

        if x_axis not in df.columns:
            raise ChartError(f"X轴字段不存在: {x_axis}", ErrorCode.CHART_CONFIG_ERROR)
        for y in y_axis:
            if y not in df.columns:
                raise ChartError(f"Y轴字段不存在: {y}", ErrorCode.CHART_CONFIG_ERROR)
        return x_axis, y_axis

    # ---- 图表配置生成 ----

    # tooltip formatter 占位符：json.dumps 会将其序列化为字符串，
    # _save_html 中再将带引号的占位符替换为真正的 JS 函数，避免 ECharts 把函数当纯文本渲染。
    _TOOLTIP_FORMATTER_AXIS = '__TOOLTIP_FORMATTER_AXIS__'
    _TOOLTIP_FORMATTER_AXIS_JS = (
        "function(params) {\n"
        "                var res = params[0].axisValue + '<br/>';\n"
        "                params.forEach(function(p) {\n"
        "                    var val = (p.value === null || p.value === undefined || p.value === 'NaN' || p.value === 'Infinity') ? '无数据' : p.value;\n"
        "                    res += p.marker + p.seriesName + ': ' + val + '<br/>';\n"
        "                });\n"
        "                return res;\n"
        "            }"
    )

    def _base(self, title, x_label='', y_label=''):
        return {
            'title': {'text': title, 'left': 'center', 'textStyle': {'fontSize': 16}},
            'tooltip': {'trigger': 'axis', 'formatter': self._TOOLTIP_FORMATTER_AXIS},
            'legend': {'top': 'bottom'},
            'grid': {'left': '3%', 'right': '4%', 'bottom': '12%', 'containLabel': True},
        }

    def _line(self, df, x, y, title):
        opt = self._base(title)
        opt['xAxis'] = {'type': 'category', 'data': df[x].astype(str).tolist()}
        opt['yAxis'] = {'type': 'value', 'name': y[0] if len(y) == 1 else ''}
        opt['series'] = [
            {'name': col, 'type': 'line', 'smooth': True, 'data': _sanitize_series(df[col].tolist())}
            for col in y
        ]
        return opt

    def _bar(self, df, x, y, title):
        opt = self._base(title)
        opt['xAxis'] = {'type': 'category', 'data': df[x].astype(str).tolist()}
        opt['yAxis'] = {'type': 'value'}
        opt['series'] = [
            {'name': col, 'type': 'bar', 'data': _sanitize_series(df[col].tolist())}
            for col in y
        ]
        return opt

    def _pie(self, df, x, y, title):
        opt = self._base(title)
        opt['tooltip'] = {'trigger': 'item', 'formatter': '{a} <br/>{b}: {c} ({d}%)'}
        opt['legend'] = {'orient': 'vertical', 'left': 'left', 'top': 'center'}
        y_col = y[0] if y else df.columns[-1]
        data = [{'name': str(r[x]), 'value': _sanitize_value(float(r[y_col]))} for _, r in df.iterrows()]
        opt['series'] = [{
            'name': y_col, 'type': 'pie', 'radius': ['40%', '70%'], 'data': data,
            'label': {'show': True, 'formatter': '{b}: {c} ({d}%)'},
            'emphasis': {'itemStyle': {'shadowBlur': 10, 'shadowColor': 'rgba(0,0,0,0.5)'}},
        }]
        return opt

    def _scatter(self, df, x, y, title):
        opt = self._base(title)
        opt['tooltip'] = {'trigger': 'item', 'formatter': '({c})'}
        y_col = y[0] if y else df.columns[-1]
        # 判断 x 轴是否为数值类型
        x_is_numeric = pd.api.types.is_numeric_dtype(df[x])
        if x_is_numeric:
            opt['xAxis'] = {'type': 'value', 'name': x, 'scale': True}
            data = [[_sanitize_value(float(r[x])), _sanitize_value(float(r[y_col]))] for _, r in df.iterrows()]
        else:
            opt['xAxis'] = {'type': 'category', 'data': df[x].astype(str).tolist()}
            data = [_sanitize_value(float(r[y_col])) for _, r in df.iterrows()]
        opt['yAxis'] = {'type': 'value', 'name': y_col, 'scale': True}
        opt['series'] = [{'name': '数据点', 'type': 'scatter', 'data': data, 'symbolSize': 10}]
        return opt

    def _area(self, df, x, y, title):
        opt = self._line(df, x, y, title)
        for s in opt['series']:
            s['areaStyle'] = {'opacity': 0.5}
        return opt

    def _radar(self, df, x, y, title):
        opt = self._base(title)
        opt['tooltip'] = {'trigger': 'item'}
        max_val = float(df[y].max().max() * 1.2) if len(y) > 0 else 100
        max_val = _sanitize_value(max_val) or 100
        indicator = [{'name': str(r[x]), 'max': max_val} for _, r in df.iterrows()]
        opt['radar'] = {'indicator': indicator, 'shape': 'polygon'}
        opt['series'] = [{'name': '雷达图', 'type': 'radar', 'data': [{'name': c, 'value': _sanitize_series(df[c].tolist())} for c in y]}]
        return opt

    def _heatmap(self, df, x, y, title):
        opt = self._base(title)
        opt['tooltip'] = {'position': 'top'}
        x_data = df[x].astype(str).tolist()
        y_data = y
        matrix = []
        for i, row_label in enumerate(x_data):
            for j, col_label in enumerate(y_data):
                val = _sanitize_value(float(df.iloc[i][col_label]))
                matrix.append([j, i, val])
        all_vals = [v for row in matrix for v in [row[2]] if v is not None]
        vmin = min(all_vals) if all_vals else 0
        vmax = max(all_vals) if all_vals else 100
        opt['xAxis'] = {'type': 'category', 'data': y_data, 'splitArea': {'show': True}}
        opt['yAxis'] = {'type': 'category', 'data': x_data, 'splitArea': {'show': True}}
        opt['visualMap'] = {'min': vmin, 'max': vmax, 'calculable': True, 'orient': 'horizontal', 'left': 'center', 'bottom': '15%'}
        opt['series'] = [{'name': '热力图', 'type': 'heatmap', 'data': matrix, 'label': {'show': True}}]
        return opt

    def _treemap(self, df, x, y, title):
        opt = self._base(title)
        opt['tooltip'] = {'trigger': 'item'}
        y_col = y[0] if y else df.columns[-1]
        data = [{'name': str(r[x]), 'value': _sanitize_value(float(r[y_col]))} for _, r in df.iterrows()]
        opt['series'] = [{'name': '树图', 'type': 'treemap', 'data': data, 'roam': False, 'breadcrumb': {'show': True}}]
        return opt

    def _graph(self, df, x, y, title):
        opt = self._base(title)
        # 检测是否有"源/目标"列格式
        source_col = target_col = weight_col = None
        for col in df.columns:
            cl = col.lower()
            if cl in ('源', 'source', 'from', '起始', '起点') and source_col is None:
                source_col = col
            elif cl in ('目标', 'target', 'to', '终点', '到达') and target_col is None:
                target_col = col
            elif cl in ('权重', 'weight', '值', 'value', 'val') and weight_col is None:
                weight_col = col

        if source_col and target_col:
            # 源/目标/权重格式
            node_names = set(df[source_col].astype(str).tolist() + df[target_col].astype(str).tolist())
            nodes = [{'name': n, 'category': 0} for n in node_names]
            links = []
            for _, r in df.iterrows():
                link = {'source': str(r[source_col]), 'target': str(r[target_col])}
                if weight_col and weight_col in df.columns:
                    w = _sanitize_value(float(r[weight_col]))
                    if w is not None:
                        link['value'] = w
                links.append(link)
        else:
            # 通用格式：x 列为节点名，y 列为值，链式连接
            y_col = y[0] if y else df.columns[-1]
            nodes = [{'name': str(r[x]), 'value': _sanitize_value(float(r[y_col])), 'category': 0} for _, r in df.iterrows()]
            links = [{'source': nodes[i]['name'], 'target': nodes[i+1]['name'], 'value': 1} for i in range(len(nodes)-1)]

        opt['tooltip'] = {'trigger': 'item'}
        opt['series'] = [{'name': '关系图', 'type': 'graph', 'layout': 'force', 'data': nodes, 'links': links,
                          'roam': True, 'label': {'show': True}, 'force': {'repulsion': 200, 'edgeLength': [50, 150]}}]
        return opt

    def _boxplot(self, df, x, y, title):
        opt = self._base(title)
        opt['tooltip'] = {'trigger': 'item', 'axisPointer': {'type': 'shadow'}}
        cols = y[:3] if len(y) > 0 else df.select_dtypes(include=[np.number]).columns[:3].tolist()
        box_data = []
        outlier_data = []  # 格式: [[categoryIndex, value], ...]
        for cat_idx, col in enumerate(cols):
            s = df[col].dropna()
            if s.empty:
                box_data.append([0, 0, 0, 0, 0])
                continue
            q1, q2, q3 = float(s.quantile(0.25)), float(s.quantile(0.5)), float(s.quantile(0.75))
            iqr = q3 - q1
            lo = max(float(s.min()), q1 - 1.5 * iqr)
            hi = min(float(s.max()), q3 + 1.5 * iqr)
            box_data.append([lo, q1, q2, q3, hi])
            # ECharts scatter 在 category xAxis 下需要 [xIndex, yValue] 格式
            outliers = s[(s < lo) | (s > hi)]
            for val in outliers:
                outlier_data.append([cat_idx, float(val)])
        opt['xAxis'] = {'type': 'category', 'data': cols, 'boundaryGap': True}
        opt['yAxis'] = {'type': 'value'}
        opt['series'] = [
            {'name': '箱线图', 'type': 'boxplot', 'data': box_data},
            {'name': '异常值', 'type': 'scatter', 'data': outlier_data, 'symbolSize': 8},
        ]
        return opt

    def _waterfall(self, df, x, y, title):
        opt = self._bar(df, x, y, title)
        y_col = y[0] if y else df.columns[-1]
        vals = df[y_col].tolist()
        diffs = [vals[0]] + [vals[i] - vals[i-1] for i in range(1, len(vals))]
        opt['series'][0]['data'] = _sanitize_series(diffs)
        opt['series'][0]['label'] = {'show': True, 'position': 'top'}
        return opt

    def _gauge(self, df, x, y, title):
        y_col = y[0] if y else df.select_dtypes(include=[np.number]).columns[0]
        value = float(df[y_col].mean())
        value = _sanitize_value(value)
        if value is None:
            value = 0
        max_val = max(float(df[y_col].max()) * 1.2, value * 1.5, 100)
        max_val = _sanitize_value(max_val) or 100
        opt = {'title': {'text': title, 'left': 'center'}}
        opt['series'] = [{'name': '仪表盘', 'type': 'gauge', 'max': max_val,
                          'detail': {'formatter': '{value}'},
                          'data': [{'value': value, 'name': y_col}],
                          'axisLine': {'lineStyle': {'width': 10, 'color': [[0.3, '#67e0e3'], [0.7, '#37a2da'], [1, '#fd666d']]}}}]
        return opt

    def _sankey(self, df, x, y, title):
        opt = {'title': {'text': title, 'left': 'center'}}
        # 检测是否有"源/目标"列格式
        source_col = target_col = value_col = None
        for col in df.columns:
            cl = col.lower()
            if cl in ('源', 'source', 'from', '起始', '起点') and source_col is None:
                source_col = col
            elif cl in ('目标', 'target', 'to', '终点') and target_col is None:
                target_col = col
            elif cl in ('值', 'value', 'val', '权重', 'weight') and value_col is None:
                value_col = col

        nodes, links = [], []
        if source_col and target_col:
            # 源/目标/值格式
            node_names = set(df[source_col].astype(str).tolist() + df[target_col].astype(str).tolist())
            nodes = [{'name': n} for n in node_names]
            for _, r in df.iterrows():
                val = 1
                if value_col and value_col in df.columns:
                    v = _sanitize_value(float(r[value_col]))
                    val = v if v is not None else 1
                links.append({'source': str(r[source_col]), 'target': str(r[target_col]), 'value': val})
        else:
            # 通用格式：链式连接
            y_col = y[0] if y else df.columns[-1]
            for i, r in df.iterrows():
                nodes.append({'name': str(r[x])})
                if i > 0:
                    val = _sanitize_value(float(r[y_col])) if pd.notna(r.get(y_col)) else 1
                    links.append({'source': str(df.iloc[i-1][x]), 'target': str(r[x]), 'value': val if val is not None else 1})

        opt['tooltip'] = {'trigger': 'item'}
        opt['series'] = [{'name': '桑基图', 'type': 'sankey', 'data': nodes, 'links': links,
                          'emphasis': {'focus': 'adjacency'}, 'lineStyle': {'curveness': 0.5}}]
        return opt

    def _funnel(self, df, x, y, title):
        opt = self._base(title)
        y_col = y[0] if y else df.columns[-1]
        data = [{'name': str(r[x]), 'value': _sanitize_value(float(r[y_col]))} for _, r in df.iterrows()]
        all_vals = [d['value'] for d in data if d['value'] is not None]
        max_val = max(all_vals) if all_vals else 100
        opt['series'] = [{'name': '漏斗图', 'type': 'funnel', 'left': '10%', 'top': 60, 'bottom': 60, 'width': '80%',
                          'min': 0, 'max': max_val, 'sort': 'descending', 'gap': 2,
                          'label': {'show': True, 'position': 'inside'},
                          'data': data}]
        return opt

    def _sunburst(self, df, x, y, title):
        opt = {'title': {'text': title, 'left': 'center'}}
        y_col = y[0] if y else df.columns[-1]
        data = [{'name': str(r[x]), 'value': _sanitize_value(float(r[y_col]))} for _, r in df.iterrows()]
        opt['series'] = [{'name': '旭日图', 'type': 'sunburst', 'data': data, 'radius': [0, '90%'],
                          'label': {'rotate': 'radial'}}]
        return opt

    def _wordcloud(self, df, x, y, title):
        opt = {'title': {'text': title, 'left': 'center'}}
        y_col = y[0] if y else df.columns[-1]
        data = [{'name': str(r[x]), 'value': _sanitize_value(float(r[y_col]))} for _, r in df.iterrows()]
        opt['series'] = [{'name': '词云', 'type': 'wordCloud', 'shape': 'circle',
                          'sizeRange': [12, 60], 'rotationRange': [-90, 90], 'rotationStep': 45,
                          'data': data}]
        return opt

    # ---- HTML 输出 ----

    def _save_html(self, option: Dict, title: str, width: int, height: int, chart_type: str = '') -> Path:
        import hashlib
        content_str = json.dumps(option, ensure_ascii=False, sort_keys=True)
        suffix = hashlib.md5(content_str.encode()).hexdigest()[:6]
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:30]
        filename = f"{safe_title}_{suffix}.html"
        path = self.output_dir / filename

        # XSS 防护：转义所有用户输入插入 HTML 的部分
        esc_title = html_module.escape(title)
        esc_safe_title = html_module.escape(safe_title)

        option_json = json.dumps(option, ensure_ascii=False, indent=2, allow_nan=False)

        # 将占位符字符串替换为真正的 JS 函数（去掉 json.dumps 添加的引号）
        option_json = option_json.replace(
            f'"{self._TOOLTIP_FORMATTER_AXIS}"',
            self._TOOLTIP_FORMATTER_AXIS_JS
        )

        # 判断是否需要加载 wordcloud 插件
        wordcloud_script = ''
        if chart_type == 'wordcloud':
            wordcloud_script = f'<script src="{ECHARTS_WORDCLOUD_CDN}"></script>'

        # 宽高比，用于响应式高度计算
        aspect_ratio = width / height if height > 0 else 16 / 9

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc_title}</title>
<script src="{ECHARTS_CDN}"></script>
<script>
if(typeof echarts==='undefined'){{
document.write('<script src="{ECHARTS_CDN_FALLBACK}"><\\/script>');
}}
</script>
{wordcloud_script}
<style>
* {{ box-sizing: border-box; }}
body {{ font-family: 'Microsoft YaHei', 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans CJK SC', sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
.container {{ max-width: {width}px; width: 100%; margin: 0 auto; background: #fff; padding: 30px;
             border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
.header {{ text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #4CAF50; }}
.title {{ font-size: clamp(16px, 4vw, 24px); font-weight: 700; color: #2E7D32; margin: 0; }}
.subtitle {{ font-size: 12px; color: #999; }}
.chart-wrapper {{ width: 100%; position: relative; }}
.chart {{ width: 100%; aspect-ratio: {aspect_ratio:.4f}; min-height: 300px; }}
.controls {{ text-align: center; margin: 15px 0; }}
.btn {{ display: inline-block; padding: 6px 16px; background: #4CAF50; color: #fff;
        border: none; border-radius: 4px; cursor: pointer; font-size: 13px; margin: 0 4px; }}
.btn:hover {{ background: #45a049; }}
.footer {{ margin-top: 25px; padding-top: 15px; border-top: 1px solid #eee; text-align: center;
          font-size: 11px; color: #aaa; }}
@media (max-width: 640px) {{
  .container {{ padding: 15px; }}
  .chart {{ min-height: 250px; }}
}}
@media print {{ .controls {{ display: none; }} .container {{ box-shadow: none; }} }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1 class="title">{esc_title}</h1>
    <div class="subtitle">Smart Charts &middot; {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
  </div>
  <div class="controls">
    <button class="btn" onclick="saveAsImage()">保存图片</button>
    <button class="btn" onclick="toggleFull()">全屏</button>
  </div>
  <div class="chart-wrapper">
    <div id="chart" class="chart"></div>
  </div>
  <div class="footer">由 Smart Charts 生成 &middot; ECharts 5.4.3</div>
</div>
<script>
var chartDom = document.getElementById('chart');
var chart = echarts.init(chartDom);
chart.setOption({option_json});
window.addEventListener('resize', function() {{ chart.resize(); }});
new ResizeObserver(function() {{ chart.resize(); }}).observe(chartDom);
function saveAsImage() {{
  var url = chart.getDataURL({{ type: 'png', pixelRatio: 2, backgroundColor: '#fff' }});
  var a = document.createElement('a'); a.href = url; a.download = '{esc_safe_title}.png'; a.click();
}}
function toggleFull() {{
  var el = document.getElementById('chart');
  if (!document.fullscreenElement) el.requestFullscreen();
  else document.exitFullscreen();
}}
</script>
</body>
</html>"""
        path.write_text(html, encoding='utf-8')
        return path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python chart_generator.py <file_path> <chart_type> [--title 标题] [--x-axis 列名] [--y-axis 列1 列2] [--transform-code 代码] [--output-dir 目录] [--auto-confirm]")
        sys.exit(1)

    args = sys.argv[1:]
    file_path = args[0]
    chart_type = args[1]

    title = '数据图表'
    x_axis = None
    y_axis = None
    transform_code = None
    output_dir = './smart_charts_output'
    auto_confirm = False

    i = 2
    while i < len(args):
        if args[i] == '--title' and i + 1 < len(args):
            title = args[i + 1]; i += 2
        elif args[i] == '--x-axis' and i + 1 < len(args):
            x_axis = args[i + 1]; i += 2
        elif args[i] == '--y-axis':
            y_list = []
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                y_list.extend(args[i].split())
                i += 1
            y_axis = y_list if y_list else None
        elif args[i] == '--transform-code' and i + 1 < len(args):
            transform_code = args[i + 1]; i += 2
        elif args[i] == '--output-dir' and i + 1 < len(args):
            output_dir = args[i + 1]; i += 2
        elif args[i] == '--auto-confirm':
            auto_confirm = True; i += 1
        else:
            i += 1

    if __package__ is None:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from core.data_parser import DataParser
    else:
        from .data_parser import DataParser

    try:
        dp = DataParser()
        df = dp.parse_file(file_path)
        gen = ChartGenerator(output_dir=output_dir)
        result = gen.generate_chart(df, chart_type, title=title, x_axis=x_axis, y_axis=y_axis,
                                    transform_code=transform_code, auto_confirm=auto_confirm)
        print(result['html_path'])
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
