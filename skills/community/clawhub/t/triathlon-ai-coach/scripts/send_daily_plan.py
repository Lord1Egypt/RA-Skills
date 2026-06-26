#!/usr/bin/env python3
"""
每日训练计划推送脚本
自动同步 TP 数据，生成计划，推送微信，并保存到 IMA 笔记
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.parse

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trainer import generate_tomorrow_plan, load_config

# IMA 配置
IMA_CLIENTID = "f242d273c5775305be3568367024e9eb"
IMA_APIKEY = "XrGDjvjFGt08oZ1jfc8VIBDMVXtyzyXX4E025s96zlekJsYDhaZp3xaHXNX5mFclBLNFM8v9EA=="
IMA_API_URL = "https://ima.qq.com/openapi/note/v1"


def save_to_ima(title, content):
    """保存训练计划到 IMA 笔记"""
    try:
        # 构建请求
        url = f"{IMA_API_URL}/import_doc"
        
        # 清理特殊字符
        title = title.replace('*', '').replace('#', '').strip()[:50]
        
        payload = {
            "content_format": 1,  # Markdown
            "content": content,
            "title": title
        }
        
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(url, data=data)
        req.add_header('ima-openapi-clientid', IMA_CLIENTID)
        req.add_header('ima-openapi-apikey', IMA_APIKEY)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('code') == 0:
                note_id = result.get('data', {}).get('note_id')
                print(f"✅ 已保存到 IMA 笔记: {title} (ID: {note_id})")
                return note_id
            else:
                print(f"❌ IMA 保存失败: {result.get('msg')}")
                return None
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误: {e.code}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"   响应: {error_body}")
        except:
            pass
        return None
    except Exception as e:
        print(f"❌ IMA 保存失败: {e}")
        return None


def main():
    """主函数"""
    config = load_config()
    user_name = config['user']['name']
    
    # 生成明天计划
    plan = generate_tomorrow_plan()
    
    # 解析计划内容，生成标题
    lines = plan.split('\n')
    date_str = ""
    workout_type = "训练计划"
    
    for line in lines:
        if '2026-03-' in line:
            date_str = line.strip()[:10]
        if '🏊' in line:
            workout_type = "游泳"
        elif '渐进式长跑' in line:
            workout_type = "渐进式长跑"
        elif '🏃' in line:
            workout_type = "跑步"
        elif '🚴' in line:
            workout_type = "骑行"
        elif '🔄' in line:
            workout_type = "骑跑两项"
        elif '🏖️' in line:
            workout_type = "休息日"
    
    # 标题：日期 + 训练类型
    note_title = f"{date_str} {workout_type}" if date_str else f"{datetime.now().strftime('%Y-%m-%d')} 训练计划"
    
    # 清理 Markdown 格式
    content_clean = plan.replace('**', '')
    
    full_content = f"""# {note_title}

{content_clean}

---
💡 由 AI 训练教练自动生成
"""
    
    # 保存到文件
    output_path = Path(__file__).parent / "data" / "tomorrow_plan.md"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ 计划已保存到: {output_path}")
    
    # 保存到 IMA
    print("\n正在保存到 IMA 笔记...")
    save_to_ima(note_title, full_content)
    
    return full_content, note_title


if __name__ == "__main__":
    main()
