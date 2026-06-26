#!/usr/bin/env python3
"""
AI生成逐字稿 (narration.json)

用法:
  python gen_narration.py --outline "C:\\Users\\liweiwei\\course-video-remotion\\src\\slides\\industry_medical\\outline.json" --project "C:\\Users\\liweiwei\\course-video-remotion" --lesson "industry_medical"
  python gen_narration.py --outline "C:\\Users\\liweiwei\\course-video-remotion\\src\\slides\\industry_medical\\outline.json" --project "C:\\Users\\liweiwei\\course-video-remotion" --lesson "industry_medical" --style casual

输出: {project}/src/slides/{lesson}/narration.json

铁律:
  - narration[0] 必须是封面(isCover=true, narration="")
  - narration[1] 必须是开场钩子
  - 每个slide有唯一语义ID
  - 非封面slide配音≥20字
"""

import argparse
import json
import os
import re
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

    print(f'[DEBUG] 正在调用DashScope API for narration...')
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


NARRATION_PROMPT = """你是一个短视频逐字稿撰写专家。请根据以下幻灯片大纲撰写逐字稿。

幻灯片信息:
- 主题:{topic}
- 行业:{industry}
- 受众:{audience}
- 幻灯片列表:{slides}

要求:
1. 口语化,像跟朋友聊天一样
2. 每段配音50-150字
3. 开场用钩子问题吸引注意力
4. 结论先行,再展开解释
5. 用比喻和具体例子让抽象概念具象化
6. 结尾总结+行动指南
7. 严格按照幻灯片顺序生成
8. 【强制】禁止编造具体数字/百分比，改用趋势性描述(如"大幅提升"、"显著降低"、"成倍增长")

输出JSON数组格式(严格遵守):
[
  {{ "id": "cover", "isCover": true, "title": "封面标题", "narration": "" }},
  {{ "id": "hook", "isCover": false, "title": "开场钩子", "narration": "配音文字..." }},
  {{ "id": "slide_01", "isCover": false, "title": "幻灯片1", "narration": "配音文字..." }},
  {{ "id": "slide_02", "isCover": false, "title": "幻灯片2", "narration": "配音文字..." }},
  {{ "id": "summary", "isCover": false, "title": "总结", "narration": "配音文字..." }},
  {{ "id": "action", "isCover": false, "title": "行动指南", "narration": "配音文字..." }}
]

语义ID规则:cover, hook, slide_01, slide_02, ..., summary, action
"""


def generate_narration(outline: dict) -> list:
    """
    生成逐字稿。
    使用DashScope qwen-max API调用。
    """
    topic = outline.get("topic", "未知主题")
    industry = outline.get("industry", "通用行业")
    audience = outline.get("audience", "普通受众")
    slides = outline.get("slides", [])

    prompt = NARRATION_PROMPT.format(
        topic=topic,
        industry=industry,
        audience=audience,
        slides=json.dumps(slides, ensure_ascii=False)
    )

    try:
        narration = call_dashscope_api(prompt)
        # 验证返回格式
        if not isinstance(narration, list) or len(narration) == 0:
            raise ValueError('API返回的JSON格式错误:不是有效的数组')

        # 确保第一个元素是封面
        if narration[0].get('id') != 'cover' or not narration[0].get('isCover'):
            print('⚠️ API返回的第一个元素不是封面,正在修正')
            narration[0] = {
                "id": "cover",
                "isCover": True,
                "title": outline.get("slideTitle", topic),
                "narration": ""
            }

        return narration
    except Exception as e:
        print(f'[WARN] DashScope API调用失败,使用模板生成: {e}')
        # 模板生成(备用)
        narration = [
            {
                "id": "cover",
                "isCover": True,
                "title": outline.get("slideTitle", topic),
                "narration": ""
            }
        ]

        # 遍历幻灯片生成对应的配音
        for idx, slide in enumerate(outline.get("slides", [])):
            slide_type = slide.get("type", "content")
            slide_title = slide.get("title", f"幻灯片{idx+1}")
            slide_content = slide.get("content", "幻灯片内容")
            
            # 生成唯一的ID
            if slide_type == "cover":
                # 封面已经在上面添加，跳过
                continue
            elif slide_type == "hook":
                narration.append({
                    "id": "hook",
                    "isCover": False,
                    "title": slide_title,
                    "narration": f"{slide_content}。今天我花几分钟把这个重要的知识点给你讲明白。"
                })
            elif slide_type == "summary":
                narration.append({
                    "id": "summary",
                    "isCover": False,
                    "title": slide_title,
                    "narration": f"我们来总结一下刚才讲的内容。{slide_content}"
                })
            elif slide_type == "action":
                narration.append({
                    "id": "action",
                    "isCover": False,
                    "title": slide_title,
                    "narration": f"那么现在你可以采取什么行动呢？{slide_content}"
                })
            else:
                narration.append({
                    "id": f"slide_{idx:02d}" if slide_type == "content" else slide_type,
                    "isCover": False,
                    "title": slide_title,
                    "narration": f"{slide_content}。让我们详细了解一下。"
                })

        return narration


def validate_narration(narration: list) -> list[str]:
    """验证narration是否符合铁律"""
    errors = []
    if len(narration) < 3:
        errors.append(f"narration至少3个slide(封面+钩子+总结),当前{len(narration)}")
    if narration[0].get('id') != 'cover':
        errors.append("narration[0].id 必须是 'cover'")
    if narration[0].get('isCover') != True:
        errors.append("narration[0].isCover 必须是 true")
    if narration[0].get('narration', 'x') != '':
        errors.append("narration[0].narration 必须为空")

    ids = set()
    for i, s in enumerate(narration):
        if s['id'] in ids:
            errors.append(f"重复ID: {s['id']}")
        ids.add(s['id'])
        if not s.get('isCover') and len(s.get('narration', '')) < 20:
            errors.append(f"slide [{s['id']}] 配音不足20字")

    # 检查停顿标记
    for s in narration:
        if re.search(r'(停顿\d+秒)', s.get('narration', '')):
            errors.append(f"slide [{s['id']}] 包含停顿标记,需要清洗")

    return errors


def main():
    parser = argparse.ArgumentParser(description='AI生成逐字稿')
    parser.add_argument('--outline', required=True, help='大纲文件路径')
    parser.add_argument('--project', required=True, help='项目路径')
    parser.add_argument('--lesson', required=True, help='课程名称')
    parser.add_argument('--style', default='casual', help='风格:casual/formal/story')
    args = parser.parse_args()

    outline_path = Path(args.outline)
    outline = json.loads(outline_path.read_text(encoding='utf-8'))

    narration = generate_narration(outline)

    # 清洗停顿标记
    for s in narration:
        s['narration'] = re.sub(r'(停顿\d+秒)', '', s.get('narration', ''))

    # 验证
    errors = validate_narration(narration)
    if errors:
        print("[WARN] 验证警告:")
        for e in errors:
            print(f"  - {e}")

    # 输出到指定目录
    output_dir = Path(args.project) / "src" / "slides" / args.lesson
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "narration.json"
    output_path.write_text(json.dumps(narration, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[SUCCESS] 逐字稿已生成: {output_path}")
    print(f"   共 {len(narration)} 个slide（封面+{len(narration)-1}个内容）")


if __name__ == '__main__':
    main()
