#!/usr/bin/env python3
"""
AI生成课程大纲

用法:
  python gen_outline.py --topic "AI入门" --project "C:\\Users\\liweiwei\\course-video-remotion" --lesson "ai_introduction"
  python gen_outline.py --topic "医疗AI" --industry "医疗健康" --audience "医院管理者" --project "C:\\Users\\liweiwei\\course-video-remotion" --lesson "industry_medical"

输出: {project}/src/slides/{lesson}/outline.json
"""

import argparse
import json
import os
import requests
from pathlib import Path

PROJECT_DIR = Path(os.environ.get('PROJECT_DIR', Path.cwd()))

DASHSCOPE_CONFIG_PATH = Path.home() / '.openclaw/workspace/credentials/dashscope.json'


def call_dashscope_api(prompt: str) -> dict:
    """调用DashScope qwen-max API"""
    if DASHSCOPE_CONFIG_PATH.exists():
        config = json.loads(DASHSCOPE_CONFIG_PATH.read_text(encoding='utf-8'))
        api_key = config.get('api_key')
        base_url = config.get('base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    else:
        raise FileNotFoundError(f'DashScope配置文件不存在: {DASHSCOPE_CONFIG_PATH}')
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # DashScope 使用不同的请求格式
    data = {
        "model": "qwen-max",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message",
            "temperature": 0.7
        }
    }
    
    print(f'[DEBUG] 正在调用DashScope API...')
    # 根据配置文件更新完整的API URL
    # DashScope 使用特定的API端点而非标准OpenAI格式
    if 'compatible-mode' in base_url:
        # 兼容模式使用类似OpenAI的接口
        api_endpoint = f'{base_url}/chat/completions'
    else:
        # 标准DashScope接口
        api_endpoint = f'{base_url}/services/aigc/text-generation/generation'
    
    print(f'[DEBUG] API请求URL: {api_endpoint}')
    response = requests.post(
        api_endpoint,
        headers=headers,
        json=data
    )
    
    print(f'[DEBUG] API响应状态: {response.status_code}')
    if response.status_code == 200:
        result = response.json()
        print(f'[DEBUG] API响应内容预览: {str(result)[:200]}...')
        # DashScope的响应格式不同
        content = result['output']['choices'][0]['message']['content']
        
        # 提取JSON部分，如果内容中包含说明文字和代码块
        import re
        # 查找```json ... ```代码块
        json_match = re.search(r'```(?:json)?\n([\s\S]*?)```', content)
        if json_match:
            # 如果找到代码块，提取其中的内容
            json_str = json_match.group(1).strip()
        else:
            # 如果没有找到代码块，尝试直接解析整个内容
            json_str = content.strip()
        
        # 尝试解析JSON
        try:
            parsed_result = json.loads(json_str)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试查找大括号包围的JSON对象
            json_pattern = r'(\{[\s\S]*?\})'
            obj_match = re.search(json_pattern, json_str)
            if obj_match:
                json_str = obj_match.group(1)
                parsed_result = json.loads(json_str)
            else:
                raise ValueError(f'无法解析JSON: {json_str[:200]}...')
        
        print(f'[DEBUG] 解析后的结果预览: {str(parsed_result)[:200]}...')
        return parsed_result
        print(f'[DEBUG] 解析后的结果预览: {str(parsed_result)[:200]}...')
        return parsed_result
    else:
        print(f'[ERROR] API调用失败: {response.text}')
        raise Exception(f'DashScope API调用失败: {response.status_code} - {response.text}')


OUTLINE_PROMPT = """你是一个课程幻灯片设计专家。请为以下主题设计一节课的幻灯片大纲。

主题：{topic}
行业：{industry}
受众：{audience}
幻灯片数量：{slides}个
每张幻灯片时长：30-60秒

要求：
1. 第1张是封面页，包含课程标题和讲师信息
2. 第2张是钩子页，用一个吸引人的问题或事实开头
3. 中间3-5张是内容页，每张包含：标题、2-4个要点、视觉元素建议
4. 倒数第2张是总结页，回顾关键点
5. 最后一张是行动指南页，给出具体建议
6. 幻灯片之间有逻辑递进关系
7. 标题要口语化、吸引人，不要太学术

输出JSON格式：
{{
  "slideTitle": "幻灯片标题",
  "slides": [
    {{
      "slide": 1,
      "type": "cover|hook|content|summary|action",
      "title": "幻灯片标题",
      "content": "主要内容",
      "visual_hint": "视觉元素建议",
      "key_points": ["要点1", "要点2", "要点3"]
    }}
  ]
}}
"""


def generate_outline(topic: str, industry: str, audience: str, slides: int) -> dict:
    """
    生成课程幻灯片大纲。
    使用DashScope qwen-max API调用。
    """
    prompt = OUTLINE_PROMPT.format(topic=topic, industry=industry, audience=audience, slides=slides)
    try:
        outline = call_dashscope_api(prompt)
        # 确保返回的数据格式正确
        if 'slides' not in outline:
            raise ValueError('API返回的JSON格式错误：缺少slides字段')
        if len(outline['slides']) < slides:
            print(f'⚠️ API返回的幻灯片数量({len(outline["slides"])})少于预期({slides})，使用实际数量')
        return outline
    except Exception as e:
        print(f'[WARN] DashScope API调用失败，使用模板生成: {e}')
        # 模板生成（备用）
        outline = {
            "slideTitle": f"{topic}课程幻灯片",
            "topic": topic,
            "industry": industry,
            "audience": audience,
            "slideCount": slides,
            "slides": []
        }

        slide_types = ["cover", "hook", "content", "content", "content", "summary", "action"]
        
        for i in range(1, min(slides, 8)):  # 最多7张幻灯片
            slide_type = slide_types[i-1] if i <= len(slide_types) else "content"
            slide = {
                "slide": i,
                "type": slide_type,
                "title": f"第{i}张幻灯片：{topic}相关内容",
                "content": f"关于{topic}的主要内容",
                "visual_hint": f"与{topic}相关的视觉元素",
                "key_points": [
                    f"{topic}要点{i}-1",
                    f"{topic}要点{i}-2",
                    f"{topic}要点{i}-3",
                ]
            }
            outline["slides"].append(slide)

        return outline


def main():
    parser = argparse.ArgumentParser(description='AI生成课程大纲')
    parser.add_argument('--topic', required=True, help='课程主题')
    parser.add_argument('--industry', default='通用', help='行业领域')
    parser.add_argument('--audience', default='零基础', help='目标受众')
    parser.add_argument('--slides', type=int, default=7, help='幻灯片数量')
    parser.add_argument('--project', required=True, help='项目路径')
    parser.add_argument('--lesson', required=True, help='课程名称')
    args = parser.parse_args()

    outline = generate_outline(args.topic, args.industry, args.audience, args.slides)

    # 创建输出目录
    output_dir = Path(args.project) / "src" / "slides" / args.lesson
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "outline.json"
    output_path.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[SUCCESS] 大纲已生成: {output_path}")
    print(f"   共 {len(outline['slides'])} 张幻灯片")


if __name__ == '__main__':
    main()
