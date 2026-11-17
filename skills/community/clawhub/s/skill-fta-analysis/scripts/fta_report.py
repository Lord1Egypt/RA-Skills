#!/usr/bin/env python3
"""
故障树分析报告生成脚本
生成HTML格式的专业分析报告
"""

import argparse
import json
import sys
from pathlib import Path


def load_json(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_fta_data(input_path):
    """加载FTA数据"""
    path = Path(input_path)
    suffix = path.suffix.lower()
    
    if suffix == '.json':
        return load_json(input_path)
    elif suffix in ['.yaml', '.yml']:
        try:
            import yaml
            with open(input_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except ImportError:
            return None
    return None


def generate_html_report(fta_data, calc_result, output_path):
    """生成HTML报告"""
    
    system_name = calc_result.get('system_name', '系统')
    top_event = calc_result.get('top_event', {})
    node_probs = calc_result.get('node_probabilities', [])
    min_cuts = calc_result.get('minimal_cut_sets', [])
    cut_summary = calc_result.get('minimal_cut_sets_summary', {})
    importance = calc_result.get('importance_analysis', {})
    
    nodes = fta_data.get('nodes', {}) if fta_data else {}
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>故障树分析报告 - {system_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif; 
               background: #f5f6fa; color: #2c3e50; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                   color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .meta {{ opacity: 0.9; font-size: 14px; }}
        
        .card {{ background: white; border-radius: 10px; padding: 25px; 
                margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .card h2 {{ color: #2a5298; border-bottom: 2px solid #3498db; 
                    padding-bottom: 10px; margin-bottom: 20px; font-size: 18px; }}
        
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .summary-item {{ background: #f8f9fa; padding: 20px; border-radius: 8px; 
                        border-left: 4px solid #3498db; }}
        .summary-item.warning {{ border-left-color: #e74c3c; }}
        .summary-item.success {{ border-left-color: #27ae60; }}
        .summary-item .value {{ font-size: 32px; font-weight: bold; 
                               color: #2c3e50; margin-bottom: 5px; }}
        .summary-item .label {{ color: #7f8c8d; font-size: 14px; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ecf0f1; }}
        th {{ background: #3498db; color: white; font-weight: normal; }}
        tr:hover {{ background: #f8f9fa; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        
        .probability {{ font-family: "Consolas", monospace; color: #e74c3c; font-weight: bold; }}
        .rank {{ display: inline-block; width: 24px; height: 24px; 
                background: #3498db; color: white; border-radius: 50%; 
                text-align: center; line-height: 24px; font-size: 12px; margin-right: 10px; }}
        
        .alert {{ background: #fff3cd; border: 1px solid #ffc107; 
                 border-radius: 5px; padding: 15px; margin: 15px 0; }}
        .alert-danger {{ background: #f8d7da; border-color: #f5c6cb; }}
        
        .cut-set-item {{ background: #f8f9fa; padding: 15px; border-radius: 5px; 
                        margin-bottom: 10px; display: flex; align-items: center; gap: 15px; }}
        .cut-set-order {{ background: #e74c3c; color: white; padding: 5px 15px; 
                         border-radius: 20px; font-weight: bold; min-width: 80px; text-align: center; }}
        .cut-set-events {{ flex: 1; }}
        
        .footer {{ text-align: center; padding: 20px; color: #95a5a6; font-size: 12px; }}
        
        .chart-placeholder {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                              color: white; padding: 60px; text-align: center; 
                              border-radius: 10px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>故障树分析报告</h1>
            <div class="meta">
                <div>系统名称: {system_name}</div>
                <div>生成时间: <span id="timestamp"></span></div>
            </div>
        </div>
        
        <div class="summary-grid">
            <div class="summary-item warning">
                <div class="value">{top_event.get('probability_scientific', 'N/A')}</div>
                <div class="label">顶事件发生概率</div>
            </div>
            <div class="summary-item">
                <div class="value">{cut_summary.get('total', 0)}</div>
                <div class="label">最小割集数量</div>
            </div>
            <div class="summary-item success">
                <div class="value">{cut_summary.get('first_order', 0)}</div>
                <div class="label">一阶最小割集</div>
            </div>
            <div class="summary-item">
                <div class="value">{len(nodes)}</div>
                <div class="label">事件节点总数</div>
            </div>
        </div>
        
        <div class="card">
            <h2>1. 系统概况</h2>
            <p><strong>顶事件:</strong> {top_event.get('name', 'N/A')}</p>
            <p><strong>顶事件概率:</strong> <span class="probability">{top_event.get('probability', 0):.8f}</span></p>
            <div class="alert alert-danger">
                <strong>风险提示:</strong> 顶事件发生概率为 {top_event.get('probability', 0):.2%}，
                {"需要重点关注并采取预防措施" if top_event.get('probability', 0) > 0.01 else "处于可控范围"}
            </div>
        </div>
        
        <div class="card">
            <h2>2. 故障传播路径</h2>
            <table>
                <thead>
                    <tr>
                        <th>序号</th>
                        <th>中间事件</th>
                        <th>事件概率</th>
                        <th>类型</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''<tr>
                        <td>{{i}}</td>
                        <td>{{row['name']}}</td>
                        <td><span class="probability">{{row['probability']:.6f}}</span></td>
                        <td>{{row['type']}}</td>
                    </tr>''' for i, row in enumerate(node_probs, 1))}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>3. 最小割集分析</h2>
            <p>最小割集表示导致顶事件发生的最小事件组合。数量越少，系统越脆弱。</p>
            <div style="margin: 20px 0;">
                {''.join(f'''<div class="cut-set-item">
                    <div class="cut-set-order">{len(cut['events'])}阶</div>
                    <div class="cut-set-events">
                        {" + ".join(e['name'] for e in cut['events'])}
                    </div>
                </div>''' for cut in min_cuts[:10])}
            </div>
            <p><em>显示前{min(len(min_cuts), 10)}个最小割集，共{cut_summary.get('total', 0)}个</em></p>
        </div>
        
        <div class="card">
            <h2>4. 重要性分析</h2>
            
            <h3 style="color: #27ae60; margin: 20px 0 10px;">临界重要度排序 (改进优先级)</h3>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>基本事件</th>
                        <th>概率</th>
                        <th>Birnbaum重要度</th>
                        <th>临界重要度</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''<tr>
                        <td><span class="rank">{{i}}</span></td>
                        <td>{{item[1]}}</td>
                        <td>-</td>
                        <td>-</td>
                        <td><span class="probability">{{item[2]:.6f}}</span></td>
                    </tr>''' for i, item in enumerate(importance.get('critical_importance', [])[:10], 1))}
                </tbody>
            </table>
            
            <h3 style="color: #3498db; margin: 30px 0 10px;">结构重要度排序</h3>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>基本事件</th>
                        <th>结构重要度</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''<tr>
                        <td><span class="rank">{{i}}</span></td>
                        <td>{{item[1]}}</td>
                        <td><span class="probability">{{item[2]:.6f}}</span></td>
                    </tr>''' for i, item in enumerate(importance.get('structural_importance', [])[:10], 1))}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>5. 改进建议</h2>
            <ul style="margin: 15px; line-height: 2;">
                <li>优先降低临界重要度最高的基本事件故障概率</li>
                <li>针对一阶最小割集中的事件采取冗余设计</li>
                <li>建立定期检测和维护机制</li>
                <li>完善故障预警和应急响应流程</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>本报告由FTA分析技能自动生成 | 故障树分析系统</p>
        </div>
    </div>
    
    <script>
        document.getElementById('timestamp').textContent = new Date().toLocaleString('zh-CN');
    </script>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='故障树分析报告生成工具')
    parser.add_argument('--input', '-i', required=True, help='输入FTA数据文件(JSON/YAML)')
    parser.add_argument('--calc-result', '-c', required=True, help='计算结果文件(JSON)')
    parser.add_argument('--output', '-o', required=True, help='输出HTML报告文件')
    
    args = parser.parse_args()
    
    try:
        fta_data = load_fta_data(args.input)
        calc_result = load_json(args.calc_result)
        
        output_path = generate_html_report(fta_data, calc_result, args.output)
        
        print(json.dumps({
            "status": "success",
            "output": output_path
        }, ensure_ascii=False))
        
    except Exception as e:
        import traceback
        print(json.dumps({
            "status": "error", 
            "message": str(e),
            "trace": traceback.format_exc()
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
