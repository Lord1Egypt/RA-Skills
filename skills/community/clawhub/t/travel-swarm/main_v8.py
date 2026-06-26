"""
TravelMaster V8 多MCP集成版 - 7860端口
支持：FlyAI + 高德vs腾讯验证 + 美团美食 + 麦当劳兜底 + 截图生成
"""
from flask import Flask, request, jsonify, send_file
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from backend.agents.travel_swarm_engine_v8 import TravelSwarmEngineV8

app = Flask(__name__)

# V8引擎实例
engine_v8 = TravelSwarmEngineV8()

@app.route('/')
def index():
    """返回V8前端（使用融合版）"""
    return send_file('/home/admin/.openclaw/workspace/travel_swarm/frontend/index_v7_fusion.html')

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'version': 'V8-MultiMCP',
        'features': engine_v8.features
    })

@app.route('/api/travel', methods=['POST'])
def api_travel():
    """旅行规划API"""
    data = request.json
    message = data.get('message', '')
    
    # 解析用户输入（简化版）
    # 实际应使用苏格拉底探明
    
    try:
        # 示例：直接规划香港
        plan = engine_v8.plan_travel(
            destination='香港',
            departure='北京',
            date='2026-05-01',
            people={'adult': 2, 'child': 1, 'child_age': 5},
            budget=15000,
            days=5
        )
        
        reply = f"""
✅ 已查询真实票价！

**航班**：{len(plan['flights'])}条可选
**火车**：{len(plan['trains'])}条可选
**POI验证**：{plan['poi_verified']}
**路径验证**：{plan['route_verified']}
**美食推荐**：{len(plan['lunch']['options'])}家餐厅
**麦当劳兜底**：{len(plan['mcd_screenshots'])}家门店

请选择方案生成完整攻略。
"""
        
        return jsonify({
            'reply': reply,
            'progress': 60,
            'flights': plan['flights'][:5],
            'trains': plan['trains'][:5],
            'phase': 'recommendation'
        })
    except Exception as e:
        return jsonify({'reply': f'查询失败: {str(e)}', 'progress': 0})

@app.route('/api/select_plan', methods=['POST'])
def api_select_plan():
    """选择方案并生成HTML"""
    data = request.json
    plan_type = data.get('plan', 'A')
    
    try:
        # 重新规划并生成HTML
        plan = engine_v8.plan_travel(
            destination='香港',
            departure='北京',
            date='2026-05-01',
            people={'adult': 2, 'child': 1, 'child_age': 5},
            budget=15000,
            days=5
        )
        
        html = engine_v8.generate_html(plan)
        
        return jsonify({
            'html_report': html,
            'travel_data': {
                '航班数': len(plan['flights']),
                '火车数': len(plan['trains']),
                'POI验证': plan['poi_verified'],
                '路径验证': plan['route_verified']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """重置会话"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("🧳 TravelMaster V8 多MCP集成版启动")
    print("✅ FlyAI MCP已集成")
    print("✅ 高德vs腾讯验证")
    print("✅ 美团美食推荐")
    print("✅ 麦当劳兜底")
    print("✅ 截图生成")
    
    app.run(host='0.0.0.0', port=7860, debug=False)