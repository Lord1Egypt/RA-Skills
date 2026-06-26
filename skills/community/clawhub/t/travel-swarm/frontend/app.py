import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import os
import asyncio
import gradio as gr
from dotenv import load_dotenv

load_dotenv('/home/admin/.openclaw/workspace/travel_swarm/.env')

from backend.agents.travel_swarm_engine import TravelSwarmEngine

engine = TravelSwarmEngine()

def get_progress_ui(anchor, phase="探明", extra_info=""):
    """进度条 + 当前阶段 + 详细信息"""
    rate = int(anchor.get("convergence_rate", 0) * 100)
    dims = {"who":"👥人数","where":"📍城市","when":"📅天数","how_much":"💰预算","why":"🎯偏好","what":"🎢必玩","how":"🚗交通"}
    missing = anchor.get("missing", [])
    
    badges = "".join([
        f'<span style="background:{"#10b981" if k not in missing else "#e5e7eb"};color:{"white" if k not in missing else "#6b7280"};padding:4px 10px;border-radius:12px;margin:4px;display:inline-block;font-size:12px;">{v}</span>'
        for k, v in dims.items()
    ])
    
    # 阶段进度条颜色
    phase_colors = {
        "探明": "#3b82f6",
        "搜索景点": "#10b981",
        "生成行程": "#f59e0b",
        "蜂群审核": "#8b5cf6",
        "完成": "#10b981",
        "部分完成": "#f59e0b"
    }
    bar_color = phase_colors.get(phase, "#3b82f6")
    
    # 阶段图标
    phase_icons = {
        "探明": "🔍",
        "搜索景点": "🗺️",
        "生成行程": "📝",
        "蜂群审核": "🐝",
        "完成": "✅",
        "部分完成": "⚠️"
    }
    phase_icon = phase_icons.get(phase, "⏳")
    
    extra_html = f'<div style="margin-top:8px;color:#6b7280;font-size:12px;">{extra_info}</div>' if extra_info else ""
    
    return f"""
    <div style="padding:15px;border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc;">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="font-weight:bold;">{phase_icon} {phase}</span>
            <span style="color:{bar_color};">{rate}%</span>
        </div>
        <div style="width:100%;background:#e5e7eb;height:10px;border-radius:5px;margin-bottom:12px;">
            <div style="width:{rate}%;background:{bar_color};height:10px;border-radius:5px;transition:0.3s;"></div>
        </div>
        <div>{badges}</div>
        {extra_html}
    </div>
    """

dims_keys = ["who","why","what","where","when","how","how_much"]

def respond_sync(message, history):
    """同步包装器 + 实时进度反馈"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        print(f"[Frontend] 用户输入: {message[:50]}...")
        
        res = loop.run_until_complete(engine.process_user_message(message))
        reply_text = res.get("reply", "解析中...")
        anchor = res.get("anchor", {})
        phase = res.get("phase", "探明")
        extra_info = ""
        
        # 如果有数据摘要，显示
        if "data_summary" in res:
            summary = res["data_summary"]
            extra_info = f"景点: {summary.get('景点数', 0)}个 | 酒店: {summary.get('酒店数', 0)}家"
        
        # 如果生成了HTML报告
        if "html_report" in res:
            report_html = res["html_report"]
            iframe = f'<iframe srcdoc="{report_html.replace(chr(34), "&quot;")}" width="100%" height="500px" style="border:none;margin-top:15px;border-radius:8px;"></iframe>'
            reply_text += f"\n\n{iframe}"
        
        loop.close()
        
        new_history = history.copy() if history else []
        new_history.append((message, reply_text))
        
        return "", new_history, get_progress_ui(anchor, phase, extra_info)
        
    except Exception as e:
        print(f"[Frontend错误] {e}")
        import traceback
        traceback.print_exc()
        new_history = history.copy() if history else []
        new_history.append((message, f"❌ 系统错误: {str(e)}"))
        empty_anchor = {"convergence_rate": 0, "missing": dims_keys}
        return "", new_history, get_progress_ui(empty_anchor, "错误")

with gr.Blocks(css=".gradio-container{max-width:900px!important}footer{visibility:hidden}") as demo:
    gr.HTML("""
    <h2 style='text-align:center;color:#1e40af;'>✈️ TravelSwarm 极简旅行专家</h2>
    <p style='text-align:center;color:#6b7280;font-size:14px;'>数学锚点收敛 + 真实高德API + 进度可视化</p>
    """)
    progress_display = gr.HTML(get_progress_ui({"convergence_rate": 0, "missing": dims_keys}))
    chat = gr.Chatbot(height=450, show_copy_button=True)
    msg = gr.Textbox(placeholder="告诉我您的旅行计划，一句话即可...", scale=8)
    clear_btn = gr.Button("🔄 重新规划", scale=1)
    
    msg.submit(respond_sync, [msg, chat], [msg, chat, progress_display])
    clear_btn.click(lambda: ([], "", get_progress_ui({"convergence_rate": 0, "missing": dims_keys})), outputs=[chat, msg, progress_display])

if __name__ == "__main__":
    print("🧳 TravelSwarm V3 进度可视化版启动（端口7860）")
    demo.launch(server_name="0.0.0.0", server_port=7860)