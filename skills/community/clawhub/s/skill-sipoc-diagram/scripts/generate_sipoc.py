#!/usr/bin/env python3
"""
SIPOC Diagram Generator
生成标准SIPOC（供应商-输入-流程-输出-客户）流程图
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print(json.dumps({"status": "error", "message": "缺少jinja2库，请运行: pip install jinja2"}))
    sys.exit(1)


def load_css_template(template_dir: Path) -> str:
    """加载CSS模板"""
    css_path = template_dir / "sipoc-template.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return get_default_css()


def get_default_css() -> str:
    """默认CSS样式"""
    return """
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
        background: #f5f7fa;
        padding: 20px;
    }
    
    .sipoc-container {
        max-width: 1200px;
        margin: 0 auto;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .sipoc-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 24px 32px;
        text-align: center;
    }
    
    .sipoc-header h1 {
        font-size: 28px;
        margin-bottom: 8px;
    }
    
    .sipoc-header .process-id {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .sipoc-grid {
        display: grid;
        grid-template-columns: 15% 15% 40% 15% 15%;
        min-height: 500px;
    }
    
    .sipoc-column {
        padding: 20px;
        display: flex;
        flex-direction: column;
    }
    
    .sipoc-column.header {
        background: #f8f9fa;
        font-weight: bold;
        text-align: center;
        align-items: center;
        justify-content: center;
        border-bottom: 3px solid #dee2e6;
    }
    
    .sipoc-column.content {
        background: #fff;
        border: 1px solid #dee2e6;
        border-top: none;
        gap: 12px;
    }
    
    .column-supplier { border-left: 4px solid #e74c3c; }
    .column-supplier .column-title { color: #e74c3c; }
    
    .column-input { border-left: 4px solid #f39c12; }
    .column-input .column-title { color: #f39c12; }
    
    .column-process { border-left: 4px solid #3498db; }
    .column-process .column-title { color: #3498db; }
    
    .column-output { border-left: 4px solid #27ae60; }
    .column-output .column-title { color: #27ae60; }
    
    .column-customer { border-left: 4px solid #9b59b6; }
    .column-customer .column-title { color: #9b59b6; }
    
    .column-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid currentColor;
    }
    
    .column-title-en {
        font-size: 11px;
        font-weight: normal;
        opacity: 0.8;
        display: block;
        margin-top: 2px;
    }
    
    .item-card {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 12px;
        border: 1px solid #e9ecef;
        transition: all 0.2s;
    }
    
    .item-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    .item-name {
        font-weight: bold;
        font-size: 14px;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .item-desc {
        font-size: 12px;
        color: #6c757d;
        line-height: 1.4;
    }
    
    .flow-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: #adb5bd;
        writing-mode: vertical-lr;
        text-orientation: mixed;
    }
    
    .process-step {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border-radius: 6px;
        padding: 14px;
        text-align: center;
    }
    
    .process-step .step-name {
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 4px;
    }
    
    .process-step .step-num {
        font-size: 10px;
        opacity: 0.8;
    }
    
    .connection-line {
        position: relative;
    }
    
    .connection-line::after {
        content: '';
        position: absolute;
        right: -12px;
        top: 50%;
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-left: 10px solid #adb5bd;
        transform: translateY(-50%);
    }
    
    .sipoc-footer {
        background: #f8f9fa;
        padding: 16px 32px;
        text-align: center;
        color: #6c757d;
        font-size: 12px;
        border-top: 1px solid #dee2e6;
    }
    
    @media print {
        body { background: white; padding: 0; }
        .sipoc-container { box-shadow: none; }
    }
    """


def generate_html(data: dict, css: str) -> str:
    """生成SIPOC HTML"""
    
    process_name = data.get("process_name", "流程图")
    process_id = data.get("process_id", "")
    supplier = data.get("supplier", [])
    inputs = data.get("input", [])
    process_steps = data.get("process", [])
    outputs = data.get("output", [])
    customers = data.get("customer", [])
    
    def render_items(items, type_name):
        """渲染项目卡片"""
        html = ""
        for i, item in enumerate(items, 1):
            if isinstance(item, dict):
                name = item.get("name", f"{type_name} {i}")
                desc = item.get("description", item.get("desc", ""))
                provides = item.get("provides", [])
                receives = item.get("receives", [])
                
                if provides:
                    desc = "→ " + ", ".join(provides) if not desc else desc
                if receives:
                    desc = "→ " + ", ".join(receives) if not desc else desc
            else:
                name = str(item)
                desc = ""
            
            html += f'''
            <div class="item-card">
                <div class="item-name">{name}</div>
                {"<div class=\"item-desc\">" + desc + "</div>" if desc else ""}
            </div>
            '''
        return html
    
    supplier_html = render_items(supplier, "供应商")
    input_html = render_items(inputs, "输入")
    output_html = render_items(outputs, "输出")
    customer_html = render_items(customers, "客户")
    
    process_html = ""
    for i, step in enumerate(process_steps, 1):
        if isinstance(step, dict):
            step_name = step.get("step", step.get("name", f"步骤 {i}"))
            step_desc = step.get("description", step.get("desc", ""))
        else:
            step_name = str(step)
            step_desc = ""
        
        process_html += f'''
        <div class="process-step">
            <div class="step-num">步骤 {i}</div>
            <div class="step-name">{step_name}</div>
            {"<div class=\"item-desc\" style=\"color:rgba(255,255,255,0.8);margin-top:4px;\">" + step_desc + "</div>" if step_desc else ""}
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIPOC - {process_name}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="sipoc-container">
        <div class="sipoc-header">
            <h1>{process_name}</h1>
            {"<div class=\"process-id\">流程编号: " + process_id + "</div>" if process_id else ""}
        </div>
        
        <div class="sipoc-grid">
            <div class="sipoc-column header">
                <div>
                    供应商
                    <span class="column-title-en">SUPPLIER</span>
                </div>
            </div>
            <div class="sipoc-column header">
                <div>
                    输入
                    <span class="column-title-en">INPUT</span>
                </div>
            </div>
            <div class="sipoc-column header">
                <div>
                    流程
                    <span class="column-title-en">PROCESS</span>
                </div>
            </div>
            <div class="sipoc-column header">
                <div>
                    输出
                    <span class="column-title-en">OUTPUT</span>
                </div>
            </div>
            <div class="sipoc-column header">
                <div>
                    客户
                    <span class="column-title-en">CUSTOMER</span>
                </div>
            </div>
            
            <div class="sipoc-column content column-supplier">
                {supplier_html}
            </div>
            <div class="sipoc-column content column-input connection-line">
                {input_html}
            </div>
            <div class="sipoc-column content column-process">
                {process_html}
            </div>
            <div class="sipoc-column content column-output">
                {output_html}
            </div>
            <div class="sipoc-column content column-customer">
                {customer_html}
            </div>
        </div>
        
        <div class="sipoc-footer">
            使用 SIPOC 方法论生成 | 流程管理与持续改进工具
        </div>
    </div>
</body>
</html>'''
    
    return html


def main():
    parser = argparse.ArgumentParser(description="生成标准SIPOC流程图")
    parser.add_argument("--data", required=True, help="SIPOC数据JSON字符串或文件路径")
    parser.add_argument("--output", default="sipoc_diagram.html", help="输出HTML文件路径")
    parser.add_argument("--css", default=None, help="自定义CSS文件路径")
    
    args = parser.parse_args()
    
    # 解析数据
    if args.data.startswith("{") or args.data.startswith("["):
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "error", "message": f"JSON解析失败: {str(e)}"}))
            sys.exit(1)
    else:
        data_path = Path(args.data)
        if data_path.exists():
            try:
                data = json.loads(data_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                print(json.dumps({"status": "error", "message": f"JSON文件解析失败: {str(e)}"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "message": f"数据文件不存在: {args.data}"}))
            sys.exit(1)
    
    # 获取CSS
    if args.css:
        css_path = Path(args.css)
        if css_path.exists():
            css = css_path.read_text(encoding="utf-8")
        else:
            print(json.dumps({"status": "warning", "message": f"CSS文件不存在，使用默认样式: {args.css}"}))
            css = get_default_css()
    else:
        # 尝试从assets目录加载
        script_dir = Path(__file__).parent
        asset_css = script_dir.parent / "assets" / "sipoc-template.css"
        if asset_css.exists():
            css = asset_css.read_text(encoding="utf-8")
        else:
            css = get_default_css()
    
    # 生成HTML
    html = generate_html(data, css)
    
    # 输出文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    
    result = {
        "status": "success",
        "output": str(output_path.absolute()),
        "message": f"SIPOC流程图已生成: {output_path.name}"
    }
    
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
