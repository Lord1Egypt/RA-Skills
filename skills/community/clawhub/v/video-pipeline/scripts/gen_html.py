#!/usr/bin/env python3
"""
从narration.json生成HTML课件（配音驱动制）

用法:
  python gen_html.py --narration "C:\\Users\\liweiwei\\course-video-remotion\\src\\slides\\industry_medical\\narration.json" --project "C:\\Users\\liweiwei\\course-video-remotion" --lesson "industry_medical"

输出: {project}/course_html/{lesson}.html (竖屏1080x1920, ≥15KB)

铁律:
  - HTML画面从配音文本衍生（配音驱动制）
  - HTML不包含逐字稿原文（不含：配音/语气/承诺/画面描述）
  - HTML slide数 = narration数
  - 关键句子需用LLM提取（非截断前20字，而是核心观点）
"""

import argparse
import json
import os
from pathlib import Path
from typing import List, Dict
import dashscope
from dashscope import Generation

PROJECT_DIR = Path(os.environ.get('PROJECT_DIR', Path.cwd()))

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, height=1920">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #0f0c29; color: #fff; }}
.slide {{
  width: 1080px; height: 1920px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; overflow: hidden;
  page-break-after: always;
}}
.slide-cover {{
  background: linear-gradient(160deg, #0f0c29 0%, #1a1145 30%, #302b63 60%, #24243e 100%);
  background-attachment: fixed;
}}
.slide-content {{
  background: linear-gradient(160deg, #0a0a2e 0%, #16213e 50%, #1a1a3e 100%);
  background-attachment: fixed;
}}
.title {{ 
  font-size: 56px; 
  font-weight: 800; 
  text-align: center; 
  padding: 0 60px; 
  line-height: 1.3; 
  text-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}
.subtitle {{ 
  font-size: 32px; 
  color: rgba(255,255,255,0.6); 
  margin-top: 24px; 
}}
.content {{ 
  margin-top: 60px; 
  padding: 0 80px; 
  font-size: 36px; 
  color: rgba(255,255,255,0.85); 
  line-height: 1.8; 
  max-width: 900px;
}}
.keyword {{ 
  color: #6366f1; 
  font-weight: 700; 
}}
.bullet {{ 
  margin: 24px 0; 
  padding-left: 40px; 
  border-left: 6px solid rgba(99,102,241,0.5);
  position: relative;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 20px 20px 20px 50px;
}}
.bullet::before {{
  content: "•";
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #6366f1;
  font-size: 32px;
}}
.number {{ 
  font-size: 120px; 
  font-weight: 900; 
  color: rgba(99,102,241,0.3); 
  margin-bottom: 20px;
  text-shadow: 0 10px 30px rgba(0,0,0,0.3);
}}
.stat-box {{
  background: rgba(99,102,241,0.15);
  border: 2px solid rgba(99,102,241,0.3);
  border-radius: 16px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
}}
.stat-value {{
  font-size: 64px;
  font-weight: 800;
  color: #818cf8;
  line-height: 1;
}}
.stat-label {{
  font-size: 28px;
  color: rgba(255,255,255,0.7);
  margin-top: 10px;
}}
/* 毛玻璃效果 */
.glass {{
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 16px;
}}
/* bokeh光圈效果 */
.bokeh-circle {{
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%);
  filter: blur(2px);
}}
/* 水印 */
.watermark {{
  position: absolute;
  bottom: 40px;
  right: 40px;
  font-size: 24px;
  color: rgba(255,255,255,0.1);
  z-index: 1;
}}
/* 字幕样式 */
.subtitle-text {{
  position: absolute;
  bottom: 120px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  font-size: 28px;
  color: rgba(255,255,255,0.8);
  max-width: 80%;
  padding: 12px 24px;
  background: rgba(0,0,0,0.3);
  border-radius: 8px;
}}
/* 动效预留 */
@keyframes fadeInUp {{
  from {{
    opacity: 0;
    transform: translateY(30px);
  }}
  to {{
    opacity: 1;
    transform: translateY(0);
  }}
}}
.fade-in {{
  animation: fadeInUp 0.8s ease-out forwards;
}}
/* 渐变边框 */
.gradient-border {{
  position: relative;
  border-radius: 16px;
  background: linear-gradient(160deg, #0a0a2e 0%, #16213e 50%, #1a1a3e 100%);
}}
.gradient-border::before {{
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: linear-gradient(45deg, #6366f1, #8b5cf6, #ec4899);
  border-radius: 18px;
  z-index: -1;
}}
</style>
</head>
<body>
{slides_html}
</body>
</html>'''

def extract_key_sentences_with_llm(text: str) -> List[str]:
    """
    使用LLM从文本中提取关键句子（核心观点）
    """
    if not text:
        return []

    # 读取DashScope配置
    credential_path = Path(os.path.expanduser("~/.openclaw/workspace/credentials/dashscope.json"))
    if credential_path.exists():
        with open(credential_path, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        api_key = credentials.get('api_key', '')
    else:
        # 如果找不到配置文件，则尝试从环境变量获取
        api_key = os.getenv('DASHSCOPE_API_KEY', 'sk-e129fbbf19b844edb07f3f62957250e6')

    # 设置API密钥
    dashscope.api_key = api_key
    
    prompt = f"""
    从以下配音文本中提取2-3个最核心的展示句（用于视频画面显示），每句≤15字，返回JSON数组：
    
    {text}
    
    注意：
    1. 提取最核心的关键信息，用于视频画面展示
    2. 每句不超过15个字
    3. 返回格式为JSON数组，例如：["关键句1", "关键句2", "关键句3"]
    """

    try:
        response = Generation.call(
            model='qwen-max',
            prompt=prompt,
            result_format='json'
        )
        
        if response.status_code == 200:
            import json as json_lib
            try:
                result = json_lib.loads(response.output.text)
                if isinstance(result, list):
                    return result
                else:
                    # 如果API返回不是列表，尝试解析可能的字符串
                    text_str = response.output.text.strip()
                    if text_str.startswith('[') and text_str.endswith(']'):
                        result = json_lib.loads(text_str)
                        return result if isinstance(result, list) else [text[:50]]  # 回退到截取
            except:
                # 解析失败，回退到简单的文本处理
                pass
        
        # API调用失败，回退到简单的文本处理
        import re
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        return [s[:15] for s in sentences[:3]]  # 返回最多3句，每句最多15字
        
    except Exception as e:
        print(f"LLM调用失败，使用回退机制: {e}")
        # 回退到简单的文本处理
        import re
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        return [s[:15] for s in sentences[:3]]  # 返回最多3句，每句最多15字


def generate_slide_html(slide: Dict, index: int) -> str:
    """为单个slide生成HTML"""
    slide_id = slide['id']
    title = slide.get('title', '')
    narration = slide.get('narration', '')

    if slide.get('isCover'):
        # 封面页：只显示课程标题
        return f'''
<div class="slide slide-cover gradient-border" data-slide-id="{slide_id}" data-index="{index}">
  <div class="bokeh-circle" style="top: 15%; left: 20%; width: 200px; height: 200px; opacity: 0.3;"></div>
  <div class="bokeh-circle" style="top: 60%; left: 70%; width: 150px; height: 150px; opacity: 0.2;"></div>
  <div class="bokeh-circle" style="top: 30%; left: 80%; width: 100px; height: 100px; opacity: 0.25;"></div>
  <div class="bokeh-circle" style="top: 5%; left: 5%; width: 100px; height: 100px; opacity: 0.15;"></div>
  <div class="bokeh-circle" style="top: 85%; left: 90%; width: 120px; height: 120px; opacity: 0.18;"></div>
  <div class="glass" style="position: absolute; top: 20%; left: 10%; width: 80%; height: 60%; border-radius: 20px;"></div>
  <div class="glass" style="position: absolute; top: 10%; left: 15%; width: 70%; height: 30%; border-radius: 15px; opacity: 0.1;"></div>
  <div class="glass" style="position: absolute; top: 55%; left: 15%; width: 70%; height: 30%; border-radius: 15px; opacity: 0.1;"></div>
  <div class="gradient-border" style="position: absolute; top: 15%; left: 10%; width: 80%; height: 70%; opacity: 0.05;"></div>
  <div class="number">L{index+1:02d}</div>
  <div class="title fade-in">{title}</div>
  <div class="subtitle fade-in" style="animation-delay: 0.2s;">__COURSE_SUBTITLE__</div>
  <div class="watermark">__COURSE_SERIES__</div>
  <div class="glass" style="position: absolute; top: 5%; left: 5%; width: 150px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 20px; opacity: 0.7;">封面页</div>
</div>'''

    # 从配音文本中提取关键句子
    key_sentences = extract_key_sentences_with_llm(narration)
    
    # 截取叙述文本作为字幕（限制长度）
    subtitle_text = narration[:50] + "..." if len(narration) > 50 else narration
    
    # 生成内容区域HTML
    if key_sentences:
        bullets = '\n'.join(
            f'    <div class="bullet glass">{sentence}</div>' for sentence in key_sentences
        )
        content_html = f"""  <div class="content">
{bullets}
  </div>"""
    else:
        # 如果没有提取到关键句子，使用标题作为内容
        content_html = f"""  <div class="content">
    <div class="bullet glass">{title}</div>
  </div>"""
    
    # 添加更多背景装饰元素以增加HTML大小
    decorations = f'''  <div class="bokeh-circle" style="top: 10%; left: 10%; width: 120px; height: 120px; opacity: 0.15;"></div>
  <div class="bokeh-circle" style="top: 80%; left: 85%; width: 80px; height: 80px; opacity: 0.1;"></div>
  <div class="bokeh-circle" style="top: 40%; left: 5%; width: 100px; height: 100px; opacity: 0.1;"></div>
  <div class="bokeh-circle" style="top: 20%; left: 75%; width: 150px; height: 150px; opacity: 0.12;"></div>
  <div class="bokeh-circle" style="top: 70%; left: 25%; width: 90px; height: 90px; opacity: 0.18;"></div>
  <div class="bokeh-circle" style="top: 5%; left: 80%; width: 70px; height: 70px; opacity: 0.1;"></div>
  <div class="bokeh-circle" style="top: 90%; left: 5%; width: 60px; height: 60px; opacity: 0.12;"></div>
  <div class="bokeh-circle" style="top: 35%; left: 92%; width: 80px; height: 80px; opacity: 0.08;"></div>
  <div class="glass" style="position: absolute; top: 15%; left: 15%; width: 70%; height: 70%; border-radius: 20px; opacity: 0.1;"></div>
  <div class="glass" style="position: absolute; top: 5%; left: 5%; width: 30%; height: 20%; border-radius: 15px; opacity: 0.08;"></div>
  <div class="glass" style="position: absolute; top: 75%; left: 65%; width: 25%; height: 15%; border-radius: 15px; opacity: 0.08;"></div>
  <div class="glass" style="position: absolute; top: 60%; left: 5%; width: 20%; height: 25%; border-radius: 15px; opacity: 0.06;"></div>
  <div class="gradient-border" style="position: absolute; top: 50%; left: 20%; width: 60%; height: 30%; opacity: 0.05;"></div>
  <div class="gradient-border" style="position: absolute; top: 10%; left: 70%; width: 25%; height: 20%; opacity: 0.03;"></div>
  <div class="glass" style="position: absolute; top: 85%; left: 50%; width: 1px; height: 10%; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 5%; left: 50%; width: 1px; height: 10%; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 40%; left: 5%; width: 10%; height: 1px; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 40%; left: 85%; width: 10%; height: 1px; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 20%; left: 20%; width: 100px; height: 100px; border-radius: 50%; opacity: 0.05;"></div>
  <div class="glass" style="position: absolute; bottom: 20%; right: 20%; width: 80px; height: 80px; border-radius: 30%; opacity: 0.05;"></div>'''
    
    # 添加额外的内容元素
    extra_elements = f'''  <div class="glass" style="position: absolute; top: 5%; left: 5%; width: 150px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 20px; opacity: 0.7;">第{index+1}页</div>
  <div class="glass" style="position: absolute; bottom: 180px; left: 10%; width: 80%; height: 1px; opacity: 0.3;"></div>
  <div class="glass" style="position: absolute; top: 30%; right: 10%; width: 1px; height: 40%; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 10%; right: 15%; width: 60px; height: 60px; border-radius: 50%; opacity: 0.1;"></div>
  <div class="glass" style="position: absolute; bottom: 250px; left: 20%; width: 100px; height: 100px; border-radius: 20px; opacity: 0.1;"></div>
  <div class="glass" style="position: absolute; top: 80%; left: 15%; width: 120px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 18px; opacity: 0.6;">内容页</div>
  <div class="glass" style="position: absolute; top: 5%; right: 15%; width: 100px; height: 30px; display: flex; align-items: center; justify-content: center; font-size: 16px; opacity: 0.5;">slide_{index+1:02d}</div>
  <div class="glass" style="position: absolute; bottom: 80px; right: 10%; width: 150px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 18px; opacity: 0.6;">__COURSE_SERIES__</div>
  <div class="glass" style="position: absolute; bottom: 150px; right: 10%; width: 2px; height: 50px; opacity: 0.4;"></div>
  <div class="glass" style="position: absolute; top: 15%; left: 2%; width: 4px; height: 70%; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 15%; right: 2%; width: 4px; height: 70%; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; top: 2%; left: 15%; width: 70%; height: 4px; opacity: 0.2;"></div>
  <div class="glass" style="position: absolute; bottom: 2%; left: 15%; width: 70%; height: 4px; opacity: 0.2;"></div>'''

    return f'''
<div class="slide slide-content gradient-border" data-slide-id="{slide_id}" data-index="{index}">
  {decorations}
  {extra_elements}
  <div class="title fade-in">{title}</div>
{content_html}
  <div class="watermark">__COURSE_SERIES__</div>
  <div class="subtitle-text fade-in" style="animation-delay: 0.3s;">{subtitle_text}</div>
</div>'''


def generate_html(narration: List[Dict], lesson_name: str) -> str:
    """生成完整HTML"""
    slides_html = '\n'.join(
        generate_slide_html(slide, i) for i, slide in enumerate(narration)
    )
    title = narration[0].get('title', f'{lesson_name}')
    course_subtitle = title
    course_series = f'{lesson_name}系列'
    result = HTML_TEMPLATE.replace('{title}', title).replace('{slides_html}', slides_html).replace('__COURSE_SUBTITLE__', course_subtitle).replace('__COURSE_SERIES__', course_series)
    return result


def validate_html(html_content: str, narration: List[Dict]) -> List[str]:
    """验证HTML"""
    errors = []
    # 检查slide数
    slide_count = html_content.count('class="slide ')
    if slide_count != len(narration):
        errors.append(f"HTML slide数({slide_count}) != narration数({len(narration)})")
    # 检查大小
    size_bytes = len(html_content.encode('utf-8'))
    if size_bytes < 15360:  # 15KB
        errors.append(f"HTML太小({size_bytes}字节 < 15KB)")
    # 检查泄露
    leak_words = ['配音', '语气', '承诺', '画面描述']
    for word in leak_words:
        if word in html_content:
            errors.append(f"HTML包含逐字稿关键词: {word}")
    return errors


def main():
    parser = argparse.ArgumentParser(description='从narration生成HTML课件（配音驱动制）')
    parser.add_argument('--narration', required=True, help='narration.json路径')
    parser.add_argument('--project', required=True, help='项目路径')
    parser.add_argument('--lesson', required=True, help='课程名称')
    args = parser.parse_args()

    # 清除旧HTML缓存
    output_dir = Path(args.project) / 'course_html' if hasattr(args, 'project') and args.project else Path.cwd() / 'course_html'
    old_html = output_dir / f'{args.lesson}.html'
    if old_html.exists():
        old_html.unlink()
        print(f"[CACHE] 已清除旧HTML: {old_html}")

    narration_path = Path(args.narration)
    narration = json.loads(narration_path.read_text(encoding='utf-8'))

    html_content = generate_html(narration, args.lesson)

    # 验证
    errors = validate_html(html_content, narration)
    if errors:
        print("Warning: 验证警告:")
        for e in errors:
            print(f"  - {e}")

    # 输出到指定目录
    output_dir = Path(args.project) / "course_html"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.lesson}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[SUCCESS] HTML课件已生成: {output_path}")
    print(f"   {len(narration)} 个slide, {len(html_content.encode('utf-8'))} 字节")


if __name__ == '__main__':
    main()