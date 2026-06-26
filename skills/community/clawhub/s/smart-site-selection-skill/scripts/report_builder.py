import json

def generate_html_report(keyword, city, locations_data, macro_insight, amap_key, output_filename):
    names = [loc['name'] for loc in locations_data]
    transit_data = [loc['transit'] for loc in locations_data]
    office_data = [loc['office'] for loc in locations_data]
    competitor_data = [loc['competitors'] for loc in locations_data]

    # 构建高德超清静态地图 URL
    markers_str = "|".join([f"mid,,{chr(65+i)}:{loc['lng']},{loc['lat']}" for i, loc in enumerate(locations_data)])
    static_map_url = f"https://restapi.amap.com/v3/staticmap?markers={markers_str}&key={amap_key}&size=1000*400&zoom=13"

    # 表格区（只展示前 3 个简略名字，保持整洁）
    table_rows = ""
    for i, loc in enumerate(locations_data):
        table_rows += f"""
        <tr>
        <td style="text-align: center;"><strong>Top {i+1}</strong></td>
        <td><strong style="font-size: 1.1em; color: #1a365d;">{loc['name']}</strong></td>
        <td>
            <div style="font-size: 1.1em; font-weight: bold;">{loc['transit']} 个</div>
            <div style="font-size: 0.85em; color: #888; margin-top: 4px;">如：{loc['transit_short']}</div>
        </td>
        <td>
            <div style="font-size: 1.1em; font-weight: bold;">{loc['office']} 个</div>
        </td>
        <td>
            <div style="font-size: 1.1em; font-weight: bold; color: #d9534f;">{loc['competitors']} 家</div>
        </td>
        <td style="color: #e6550d; font-weight: bold; font-size: 1.2em;">{loc['score']} 分</td>
        </tr>
        """

    # 构建微观研判文字区块
    micro_insights_html = ""
    # 构建具体的 Top 10 标签展示区
    detailed_pois_html = ""
    for i, loc in enumerate(locations_data):
        # 组装文本洞察
        micro_insights_html += f"""
        <div class="insight-card">
        <h4>📍 Top {i+1} : {loc['name']}</h4>
        <p>{loc['micro_insight']}</p>
        </div>
        """
        # 组装具体的 Top 10 标签
        office_tags = "".join([f"<span class='poi-tag office-tag'>{name}</span>" for name in loc['office_list']]) or "<span class='poi-tag empty-tag'>暂无核心设施</span>"
        comp_tags = "".join([f"<span class='poi-tag comp-tag'>{name}</span>" for name in loc['comp_list']]) or "<span class='poi-tag empty-tag'>暂无直接竞品</span>"
        
        detailed_pois_html += f"""
        <div class="detail-box">
        <h4 style="margin-top:0; border-bottom: 1px solid #eee; padding-bottom: 10px;">📍 Top {i+1} : {loc['name']}</h4>
        <div style="margin-bottom: 12px;">
            <strong style="color: #1e3c72; font-size: 0.9em; display: block; margin-bottom: 8px;">🏢 核心商务引擎/高端设施 (前 10 名拾取):</strong>
            <div>{office_tags}</div>
        </div>
        <div>
            <strong style="color: #d9534f; font-size: 0.9em; display: block; margin-bottom: 8px;">⚔️ 核心直接竞品雷达 (前 10 名拾取):</strong>
            <div>{comp_tags}</div>
        </div>
        </div>
        """

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{city} {keyword} - 专业选址洞察报告</title>
    <script src="https://cdn.staticfile.net/echarts/5.5.0/echarts.min.js"></script>
    <style>
        :root {{ --primary: #0f2027; --bg: #f8f9fa; --text: #333; }}
        body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); margin: 0; line-height: 1.8; }}
        .header {{ background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 40px 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 2.2em; letter-spacing: 1px; }}
        .container {{ max-width: 1100px; margin: -30px auto 40px; padding: 0 20px; position: relative; z-index: 10; }}
        .card {{ background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); padding: 30px; margin-bottom: 30px; }}
        .card-title {{ border-left: 5px solid #d9534f; padding-left: 15px; font-size: 1.3em; font-weight: bold; margin-bottom: 20px; color: #1e3c72; }}
        .macro-insight {{ background: #fdfbf7; padding: 20px; border-radius: 6px; font-size: 1.05em; color: #555; border-left: 4px solid #f0ad4e; }}
        .insight-card {{ background: #f8f9fa; border-left: 4px solid #5bc0de; padding: 15px 20px; margin-bottom: 15px; border-radius: 4px; }}
        .insight-card h4 {{ margin: 0 0 8px 0; color: #31708f; }}
        .insight-card p {{ margin: 0; color: #666; font-size: 0.95em; }}
        .static-map {{ width: 100%; height: auto; border-radius: 8px; border: 1px solid #ddd; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 16px 15px; text-align: left; border-bottom: 1px solid #eee; vertical-align: middle; }}
        th {{ background-color: #f4f6f8; color: #555; font-weight: bold; }}
        tr:hover {{ background-color: #fcfcfc; }}
        .chart-box {{ width: 100%; height: 350px; margin-top: 20px; }}
        /* 新增：微观业态标签样式 */
        .detail-box {{ background: #fff; border: 1px solid #eaeaea; padding: 20px; border-radius: 6px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }}
        .poi-tag {{ display: inline-block; padding: 4px 10px; margin: 0 8px 8px 0; border-radius: 4px; font-size: 0.85em; font-weight: 500; }}
        .office-tag {{ background: #e8f4f8; color: #1e3c72; border: 1px solid #d0e8f2; }}
        .comp-tag {{ background: #fdf0ef; color: #d9534f; border: 1px solid #f9dcdc; }}
        .empty-tag {{ background: #f8f9fa; color: #aaa; border: 1px dashed #ccc; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{city} · {keyword} 专业选址洞察报告</h1>
    </div>
    
    <div class="container">
        <div class="card">
            <div class="card-title">🌍 宏观市场定调与空间战略</div>
            <div class="macro-insight">
            {macro_insight}
            </div>
        </div>

        <div class="card">
            <div class="card-title">📍 Top 3 选址空间锚点映射</div>
            <img src="{static_map_url}" class="static-map">
        </div>

        <div class="card">
            <div class="card-title">📊 核心引擎明细与多维对比矩阵</div>
            <table>
            <thead>
            <tr>
                <th style="text-align: center;">综合排名</th>
                <th>地段名称</th>
                <th>公共交通引流极</th>
                <th>高端设施/商务引擎</th>
                <th>直接竞品截流</th>
                <th>商业潜力评分</th>
            </tr>
            </thead>
            <tbody>
            {table_rows}
            </tbody>
            </table>
        </div>

        <div class="card">
            <div class="card-title">🔍 商圈微观优劣势深度研判</div>
            {micro_insights_html}
        </div>
        
        <div class="card">
            <div class="card-title">📋 核心商圈业态雷达 (周边微观节点枚举)</div>
            {detailed_pois_html}
        </div>

        <div class="card">
            <div class="card-title">🌊 24 小时客流引擎推演与红蓝海测算</div>
            <div id="lineChart" class="chart-box"></div>
            <div id="barChart" class="chart-box" style="margin-top: 40px;"></div>
        </div>
    </div>

    <script>
        // 注入 ECharts 代码
        var names = {json.dumps(names)};
        
        var lineChart = echarts.init(document.getElementById('lineChart'));
        lineChart.setOption({{
            tooltip: {{ trigger: 'axis' }}, legend: {{ data: names, top: 0 }},
            xAxis: {{ type: 'category', boundaryGap: false, data: ['8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'] }},
            yAxis: {{ type: 'value', name: '客流热度指数' }},
            series: {json.dumps(locations_data)}.map((loc, index) => ({{
                name: loc.name, type: 'line', smooth: true, data: loc.traffic_curve,
                itemStyle: {{ color: ['#1e3c72', '#5bc0de', '#f0ad4e'][index % 3] }}, areaStyle: {{ opacity: 0.1 }}
            }}))
        }});
        
        var barChart = echarts.init(document.getElementById('barChart'));
        barChart.setOption({{
            tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }}, legend: {{ data: ['交通节点', '商务设施', '直接竞品'], top: 0 }},
            xAxis: {{ type: 'category', data: names }}, yAxis: {{ type: 'value' }},
            series: [
                {{ name: '交通节点', type: 'bar', data: {json.dumps(transit_data)}, itemStyle: {{color: '#5bc0de'}} }},
                {{ name: '商务设施', type: 'bar', data: {json.dumps(office_data)}, itemStyle: {{color: '#1e3c72'}} }},
                {{ name: '直接竞品', type: 'bar', data: {json.dumps(competitor_data)}, itemStyle: {{color: '#d9534f'}} }}
            ]
        }});
        
        window.addEventListener('resize', () => {{ lineChart.resize(); barChart.resize(); }});
    </script>
</body>
</html>
"""
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_filename
