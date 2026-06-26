#!/usr/bin/env python3
"""
游记导出生成脚本
用于生成 Markdown、HTML 和 PDF 格式的游记文件
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import markdown
from jinja2 import Environment, FileSystemLoader

# 数据存储路径
DATA_DIR = "./travelogue_data"
TRIPS_FILE = os.path.join(DATA_DIR, "trips.json")
MOMENTS_FILE = os.path.join(DATA_DIR, "moments.json")
TEMPLATES_DIR = "./assets/templates"


def load_trip(trip_id: str) -> Optional[Dict]:
    """加载旅行记录"""
    if not os.path.exists(TRIPS_FILE):
        return None
    
    with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
        trips = json.load(f)
    
    for t in trips:
        if t['tripId'] == trip_id:
            return t
    return None


def load_moments(trip_id: str) -> List[Dict]:
    """加载旅行素材"""
    if not os.path.exists(MOMENTS_FILE):
        return []
    
    with open(MOMENTS_FILE, 'r', encoding='utf-8') as f:
        moments = json.load(f)
    
    moments = [m for m in moments if m['tripId'] == trip_id]
    return sorted(moments, key=lambda m: m['timestamp'])


def format_date(iso_date: str) -> str:
    """格式化 ISO 日期为可读格式"""
    try:
        if 'T' in iso_date:
            dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        else:
            dt = datetime.strptime(iso_date, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y年%m月%d日 %H:%M')
    except:
        return iso_date


def format_date_only(iso_date: str) -> str:
    """只提取日期部分"""
    try:
        if 'T' in iso_date:
            return iso_date.split('T')[0]
        return iso_date.split(' ')[0] if ' ' in iso_date else iso_date
    except:
        return iso_date


def group_moments_by_date(moments: List[Dict]) -> Dict[str, List[Dict]]:
    """按日期分组素材"""
    groups = {}
    for m in moments:
        date_str = format_date_only(m['timestamp'])
        if date_str not in groups:
            groups[date_str] = []
        groups[date_str].append(m)
    return groups


def generate_markdown(trip: Dict, moments: List[Dict]) -> str:
    """生成 Markdown 格式的游记"""
    # 游记标题
    title = trip.get('title', '我的旅行')
    
    md_lines = [f"# 【{title}】", ""]
    
    # 旅行开始信息
    start_time = format_date(trip['startTime'])
    start_loc = trip.get('startLocation', '')
    
    # 按日期分组
    date_groups = group_moments_by_date(moments)
    dates = sorted(date_groups.keys())
    
    # 为每一天生成内容
    for i, date in enumerate(dates, 1):
        day_moments = date_groups[date]
        
        # 提取这一天的主要地点
        locations = [m.get('location') for m in day_moments if m.get('location')]
        main_location = locations[0] if locations else "未知地点"
        
        md_lines.append(f"## Day {i} · {main_location}")
        md_lines.append(f"> {date}")
        md_lines.append("")
        
        # 按时间顺序记录每个素材
        for m in day_moments:
            time_str = format_date(m['timestamp'])
            
            if m['type'] == 'text':
                md_lines.append(m['content'])
                md_lines.append("")
            
            elif m['type'] == 'image':
                md_lines.append(f"![{m.get('content', '旅行照片')}]({m.get('rawUrl', '')})")
                if m.get('content'):
                    md_lines.append(f"*{m['content']}*")
                md_lines.append("")
            
            elif m['type'] == 'audio':
                md_lines.append(f"🎵 *语音记录：{m['content']}*")
                md_lines.append("")
            
            elif m['type'] == 'video':
                md_lines.append(f"🎬 *视频记录：{m['content']}*")
                md_lines.append("")
        
        md_lines.append("---")
        md_lines.append("")
    
    # 后记
    if trip.get('endTime'):
        end_time = format_date(trip['endTime'])
        end_loc = trip.get('endLocation', '')
        end_event = trip.get('endEvent', '')
        
        md_lines.append("## 后记")
        md_lines.append("")
        md_lines.append(f"结束于 {end_time}，从 {end_loc} 返程。")
        if end_event:
            md_lines.append(end_event)
        md_lines.append("")
    
    return '\n'.join(md_lines)


def generate_html_from_markdown(md_content: str, trip: Dict) -> str:
    """从 Markdown 生成 HTML"""
    # 使用 markdown 库转换
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'tables']
    )
    
    # 使用模板
    template_path = os.path.join(TEMPLATES_DIR, 'travelogue.html')
    
    if os.path.exists(template_path):
        # 使用 Jinja2 模板
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template('travelogue.html')
        html = template.render(
            title=trip.get('title', '我的旅行游记'),
            content=html_content,
            generated_at=datetime.now().strftime('%Y年%m月%d日 %H:%M')
        )
    else:
        # 使用简单 HTML 包装
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{trip.get('title', '我的旅行游记')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            color: #7f8c8d;
            font-style: italic;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ecf0f1;
            margin: 30px 0;
        }}
        .footer {{
            text-align: center;
            color: #95a5a6;
            font-size: 14px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
    </style>
</head>
<body>
    {html_content}
    <div class="footer">
        生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
    </div>
</body>
</html>"""
    
    return html


def generate_pdf_from_html(html_content: str, output_path: str) -> bool:
    """从 HTML 生成 PDF"""
    try:
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(output_path)
        return True
    except Exception as e:
        print(f"PDF 生成失败: {str(e)}")
        return False


def export_travelogue(trip_id: str, output_format: str, output_path: str) -> Dict:
    """导出游记"""
    # 加载旅行记录
    trip = load_trip(trip_id)
    if not trip:
        return {
            "success": False,
            "error": f"未找到旅行记录：{trip_id}"
        }
    
    # 加载素材
    moments = load_moments(trip_id)
    if not moments:
        return {
            "success": False,
            "error": "该旅行没有任何素材记录"
        }
    
    # 生成 Markdown
    md_content = generate_markdown(trip, moments)
    
    if output_format == 'markdown':
        # 直接保存 Markdown
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return {
            "success": True,
            "file_path": os.path.abspath(output_path),
            "message": f"已生成 Markdown 文件：{output_path}"
        }
    
    elif output_format == 'html':
        # 生成 HTML
        html_content = generate_html_from_markdown(md_content, trip)
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return {
            "success": True,
            "file_path": os.path.abspath(output_path),
            "message": f"已生成 HTML 文件：{output_path}"
        }
    
    elif output_format == 'pdf':
        # 先生成 HTML，再转为 PDF
        html_content = generate_html_from_markdown(md_content, trip)
        
        # 尝试生成 PDF
        if generate_pdf_from_html(html_content, output_path):
            return {
                "success": True,
                "file_path": os.path.abspath(output_path),
                "message": f"已生成 PDF 文件：{output_path}"
            }
        else:
            # PDF 生成失败，保存 HTML 作为备选
            html_path = output_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                "success": False,
                "error": "PDF 生成失败，已保存 HTML 文件",
                "fallback_path": os.path.abspath(html_path)
            }
    
    else:
        return {
            "success": False,
            "error": f"不支持的导出格式：{output_format}"
        }


def preview_travelogue(trip_id: str) -> Dict:
    """预览游记（返回 Markdown 内容）"""
    # 加载旅行记录
    trip = load_trip(trip_id)
    if not trip:
        return {
            "success": False,
            "error": f"未找到旅行记录：{trip_id}"
        }
    
    # 加载素材
    moments = load_moments(trip_id)
    if not moments:
        return {
            "success": False,
            "error": "该旅行没有任何素材记录"
        }
    
    # 生成 Markdown
    md_content = generate_markdown(trip, moments)
    
    # 获取统计信息
    stats = {
        "total_moments": len(moments),
        "text_count": sum(1 for m in moments if m['type'] == 'text'),
        "image_count": sum(1 for m in moments if m['type'] == 'image'),
        "audio_count": sum(1 for m in moments if m['type'] == 'audio'),
        "video_count": sum(1 for m in moments if m['type'] == 'video')
    }
    
    return {
        "success": True,
        "markdown": md_content,
        "trip": trip,
        "stats": stats
    }


def main():
    parser = argparse.ArgumentParser(description='游记导出工具')
    parser.add_argument('--action', required=True, 
                       choices=['export', 'preview'],
                       help='操作类型')
    parser.add_argument('--trip-id', required=True, help='旅行ID')
    parser.add_argument('--format', choices=['markdown', 'html', 'pdf'],
                       default='markdown', help='导出格式')
    parser.add_argument('--output', default='./travelogue', help='输出文件路径')
    
    args = parser.parse_args()
    
    result = None
    
    if args.action == 'export':
        # 确定文件扩展名
        ext_map = {
            'markdown': '.md',
            'html': '.html',
            'pdf': '.pdf'
        }
        output_path = args.output
        if not output_path.endswith(ext_map.get(args.format, '')):
            output_path += ext_map.get(args.format, '')
        
        result = export_travelogue(
            trip_id=args.trip_id,
            output_format=args.format,
            output_path=output_path
        )
    
    elif args.action == 'preview':
        result = preview_travelogue(trip_id=args.trip_id)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
