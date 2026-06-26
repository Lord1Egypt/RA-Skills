#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容提炼脚本
将口语化的语音转录转换为规范的操作步骤说明

用法:
    python refine_content.py <语音转录文件> [输出文件]

环境变量:
    ANTHROPIC_API_KEY - Anthropic Claude API Key
    OPENAI_API_KEY - OpenAI API Key
"""

import os
import sys
import json
import re


def refine_with_llm(voice_text: str, api_type: str = "auto") -> dict:
    """
    用大模型提炼语音内容
    
    Args:
        voice_text: 语音原文
        api_type: API类型 (anthropic/openai/auto)
    
    Returns:
        {"title": str, "description": str}
    """
    prompt = f"""你是操作手册撰写专家。将以下口语化的语音解说转换为规范的操作步骤说明。

要求：
1. 生成简洁的步骤标题（5-10字，如"输入合同号"、"点击拍照"）
2. 提取核心操作动作（点击、输入、选择等）
3. 界面元素名称用「」包裹（如「合同号」输入框、「拍照」按钮）
4. 说明可选操作（标注"可选"）
5. 分条列出操作步骤，每条一个动作

语音原文：
"{voice_text}"

直接输出 JSON 格式，不要有其他内容：
{{"title": "步骤标题", "description": "1. 动作1\\n2. 动作2\\n3. 动作3"}}"""

    # 尝试使用 Anthropic Claude
    if api_type in ["auto", "anthropic"]:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                result_text = response.content[0].text.strip()
                # 提取 JSON
                json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except Exception as e:
                print(f"Claude API 调用失败: {e}")
    
    # 尝试使用 OpenAI
    if api_type in ["auto", "openai"]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                result_text = response.choices[0].message.content.strip()
                json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except Exception as e:
                print(f"OpenAI API 调用失败: {e}")
    
    # 无 API 时使用规则提取
    return refine_with_rules(voice_text)


def refine_with_rules(voice_text: str) -> dict:
    """
    规则提炼（无需 API）
    
    从口语化文本中提取结构化的操作步骤
    """
    # 清理文本
    text = voice_text.strip()
    
    # 常见动作模式
    action_patterns = [
        # 点击操作
        (r'点击[「\[]?([^」\]]+)[」\]]?按钮?', r'点击「\1」按钮'),
        (r'点击[「\[]?([^」\]]+)[」\]]?', r'点击「\1」'),
        (r'点[「\[]?([^」\]]+)[」\]]?', r'点击「\1」'),
        (r'按[「\[]?([^」\]]+)[」\]]?按钮?', r'点击「\1」按钮'),
        
        # 输入操作
        (r'输入[「\[]?([^」\]]+)[」\]]?[:：]?\s*([^，。,\n]+)', r'在「\1」输入框中输入\2'),
        (r'输入[「\[]?([^」\]]+)[」\]]?', r'在「\1」输入框中输入'),
        (r'填写[「\[]?([^」\]]+)[」\]]?', r'填写「\1」'),
        
        # 选择操作
        (r'选择[「\[]?([^」\]]+)[」\]]?', r'选择「\1」'),
        (r'勾选[「\[]?([^」\]]+)[」\]]?', r'勾选「\1」'),
        
        # 滑动/拖拽
        (r'向上?滑动', r'向上滑动'),
        (r'向?下?滑动', r'向下滑动'),
        (r'向左?滑动', r'向左滑动'),
        (r'向右?滑动', r'向右滑动'),
        
        # 确认/提交
        (r'确认', r'确认'),
        (r'提交', r'提交'),
        (r'保存', r'保存'),
    ]
    
    # 提取句子
    sentences = re.split(r'[。；\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 处理每个句子
    actions = []
    for sent in sentences:
        modified = sent
        for pattern, replacement in action_patterns:
            modified = re.sub(pattern, replacement, modified)
        if modified != sent or any(kw in modified for kw in ['点击', '输入', '选择', '滑动', '确认', '提交', '保存', '打开', '关闭']):
            actions.append(modified)
        elif sent:
            actions.append(sent)
    
    # 去重保持顺序
    seen = set()
    unique_actions = []
    for a in actions:
        if a not in seen:
            seen.add(a)
            unique_actions.append(a)
    
    # 生成标题
    title = ""
    for action in unique_actions:
        # 提取第一个动作作为标题
        match = re.search(r'[点选输滑确提保打关][击择入动认交存开闭][「\[（]?([^」\]]）））））)', action)
        if match:
            title = match.group(1)[:10]
            break
    
    if not title:
        # 取原文前8字
        title = text[:8].replace(" ", "")
    
    # 过滤掉纯口语（无操作动词）
    verb_keywords = ['点击', '输入', '选择', '勾选', '滑动', '确认', '提交', '保存', '打开', '关闭', '拍照', '扫码', '上传', '下载', '删除', '编辑', '返回', '退出']
    filtered_actions = [a for a in unique_actions if any(kw in a for kw in verb_keywords)]
    
    if not filtered_actions:
        filtered_actions = unique_actions[:3] if unique_actions else [text]
    
    # 生成描述
    description = "\n".join([f"{i+1}. {a}" for i, a in enumerate(filtered_actions[:5])])
    
    return {
        "title": title if title else "操作步骤",
        "description": description
    }


def refine_transcript(transcript_file: str, output_file: str = None):
    """
    提炼整个语音转录文件
    
    Args:
        transcript_file: 语音转录 JSON 文件
        output_file: 输出文件路径
    """
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = json.load(f)
    
    segments = transcript.get("segments", [])
    refined_segments = []
    
    print(f"开始提炼 {len(segments)} 个语音片段...")
    
    # 检查是否有 API
    has_api = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"))
    if has_api:
        print("✓ 检测到 API Key，将使用大模型提炼")
    else:
        print("⚠ 未检测到 API Key，将使用规则提炼（效果有限）")
        print("  可设置 ANTHROPIC_API_KEY 或 OPENAI_API_KEY 环境变量提升效果")
    
    for i, seg in enumerate(segments):
        voice_text = seg.get("text", "").strip()
        if not voice_text:
            continue
        
        print(f"  [{i+1}/{len(segments)}] 提炼: {voice_text[:30]}...")
        
        refined = refine_with_llm(voice_text)
        
        refined_segments.append({
            "start": seg.get("start", 0),
            "end": seg.get("end", 0),
            "voice_original": voice_text,
            "title": refined.get("title", "操作步骤"),
            "description": refined.get("description", voice_text)
        })
    
    result = {
        "refined": True,
        "refined_at": "2025-01-01",
        "api_used": has_api,
        "segment_count": len(refined_segments),
        "segments": refined_segments
    }
    
    if not output_file:
        output_file = transcript_file.replace(".json", "_refined.json")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n提炼完成，保存到: {output_file}")
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python refine_content.py <语音转录文件> [输出文件]")
        print("\n环境变量:")
        print("  ANTHROPIC_API_KEY - Anthropic Claude API Key（优先）")
        print("  OPENAI_API_KEY - OpenAI API Key（备选）")
        print("\n无 API Key 时使用规则提炼")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(transcript_file):
        print(f"错误: 语音转录文件不存在: {transcript_file}")
        sys.exit(1)
    
    refine_transcript(transcript_file, output_file)


if __name__ == "__main__":
    main()
