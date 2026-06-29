#!/usr/bin/env python3
"""
node_writer.py - 节点内容生成器 v1.0

职责：
  接收 prompt 包 → 调用 LLM 生成节点内容 → 提取 key_conclusion → 写入 state

用法（作为模块）：
  from node_writer import write_node
  result = write_node(paper_name, node_id)
  # result = {ok, content, key_conclusion, word_count}

注意：
  模型由调用方运行时决定，不写死在代码里。
  LLM 调用通过 OpenClaw 会话工具实现，不直接请求 API。
"""

import json
import re
import sys
from typing import Any, Dict, Optional

try:
    from .context_builder import build_prompt_package_text, build_prompt_package
except ImportError:
    from context_builder import build_prompt_package_text, build_prompt_package

try:
    from .state_manager_v2 import (
        outline_load, outline_update_status, outline_save, outline_get_node
    )
except ImportError:
    from state_manager_v2 import (
        outline_load, outline_update_status, outline_save, outline_get_node
    )


# ============================================================
# Prompt 构建
# ============================================================

def build_writing_prompt(paper_name: str, node_id: str) -> Optional[str]:
    """
    为指定节点构建完整的写作 prompt 文本。
    返回 None 表示节点不存在或无法构建。
    """
    pkg = build_prompt_package(paper_name, node_id)
    if not pkg.get("ok"):
        return None
    return build_prompt_package_text(pkg)


# ============================================================
# Key Conclusion 提取
# ============================================================

def extract_key_conclusion(content: str, node_title: str = "") -> str:
    """
    从生成的内容中提取关键结论（key_conclusion）。
    
    策略：
    1. 搜索明确的结论标记词段落（因此、综上、本节、由此可见等）
    2. 找到末章小结段落
    3. 取最后有意义的 1-2 句作为结论
    """
    if not content:
        return ""
    
    # 标记词（按优先级排序）
    markers = [
        r'因此[，,．.。]',          # 因此
        r'综上[，,．.。]',          # 综上
        r'由此可见[，,．.。]',      # 由此可见
        r'总之[，,．.。]',          # 总之
        r'本章小结',                 # 章末小结段落
        r'本节小结',                 # 节末小结
        r'通过.*?分析[，,．.。]',    # 通过...分析，得出...
        r'可以得出[，,．.。]',       # 可以得出...
    ]
    
    for marker in markers:
        matches = list(re.finditer(marker, content))
        if matches:
            # 取最后一个匹配的位置往后取句子
            last_match = matches[-1]
            start = last_match.start()
            # 往后取最多 150 字作为结论摘要
            segment = content[start:start+200].strip()
            # 截断到第一个完整句子
            sentence_end = re.search(r'[。！？\.!?]', segment[30:], re.DOTALL)
            if sentence_end:
                conclusion = segment[:30 + sentence_end.end()].strip()
            else:
                conclusion = segment[:150].strip()
            if conclusion:
                return conclusion
    
    # 回退策略：取最后一段有内容的文字（去掉空行段落）
    paragraphs = [p.strip() for p in content.split('\n') if p.strip() and len(p.strip()) > 20]
    if paragraphs:
        last_para = paragraphs[-1]
        # 取最后 100 字
        conclusion = last_para[-150:].strip()
        # 截取到句号
        sentence_end = re.search(r'[。！？\.!?]["\']?\s*$', conclusion, re.DOTALL)
        if sentence_end:
            conclusion = conclusion[:sentence_end.start()+1].strip()
        if conclusion:
            return conclusion
    
    return ""


def extract_key_conclusion_from_response(response_text: str, node_title: str = "") -> str:
    """
    从 LLM 原始回复中提取 key_conclusion。
    兼容两种格式：
    1. 结构化格式：<key_conclusion>结论内容</key_conclusion>
    2. 纯文本格式：调用 extract_key_conclusion()
    """
    if not response_text:
        return ""
    
    # 尝试结构化提取
    tag_match = re.search(r'<key_conclusion>(.*?)</key_conclusion>', response_text, re.DOTALL)
    if tag_match:
        conclusion = tag_match.group(1).strip()
        if conclusion:
            return conclusion
    
    # 回退到纯文本提取
    return extract_key_conclusion(response_text, node_title)


# ============================================================
# 字数统计
# ============================================================

def count_chinese_chars(text: str) -> int:
    """统计中文字符数（不含标点和空格）"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def count_words(text: str) -> int:
    """统计字数（中文按字符，英文按单词）"""
    chinese = count_chinese_chars(text)
    # 简单统计英文单词
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return chinese + english_words


# ============================================================
# 内容质量检查
# ============================================================

def validate_content(content: str, min_words: int = 50) -> tuple[bool, str]:
    """
    检查生成内容的基本质量。
    返回 (是否有效, 错误信息)
    """
    if not content or len(content.strip()) < 20:
        return False, "内容过短或为空"
    
    word_count = count_words(content)
    if word_count < min_words:
        return False, f"字数不足（{word_count} < {min_words}）"
    
    return True, ""


# ============================================================
# 主入口
# ============================================================

def write_node(paper_name: str, node_id: str) -> Dict[str, Any]:
    """
    为指定节点生成内容。
    
    流程：
      1. 从 state 加载节点信息
      2. 构建 prompt
      3. 调用 LLM（由调用方注入实现）
      4. 提取 content 和 key_conclusion
      5. 写入 state
    
    返回：
      {
        ok: bool,
        node_id: str,
        content: str,
        key_conclusion: str,
        word_count: int,
        error: str  # ok=False 时填充
      }
    
    注意：
      LLM 调用由调用方负责。本函数只负责：
      - prompt 构建
      - response 解析（content / key_conclusion 提取）
      - state 写入
      调用方通过 callback 或直接注入 llm_func 来执行实际 LLM 调用。
      便利函数 write_node_with_llm() 提供了标准实现。
    """
    # 1. 加载节点信息
    node = outline_get_node(paper_name, node_id)
    if not node:
        return {
            "ok": False,
            "node_id": node_id,
            "content": "",
            "key_conclusion": "",
            "word_count": 0,
            "error": f"节点 {node_id} 不存在"
        }
    
    # 2. 构建 prompt
    prompt_text = build_writing_prompt(paper_name, node_id)
    if not prompt_text:
        return {
            "ok": False,
            "node_id": node_id,
            "content": "",
            "key_conclusion": "",
            "word_count": 0,
            "error": f"无法为节点 {node_id} 构建 prompt"
        }
    
    return {
        "ok": True,
        "node_id": node_id,
        "prompt": prompt_text,      # 供调用方使用
        "title": node.get("title", ""),
        "content": "",             # 由调用方填充
        "key_conclusion": "",     # 由调用方填充
        "word_count": 0,           # 由调用方填充
        "error": ""
    }


def write_node_with_llm(
    paper_name: str,
    node_id: str,
    llm_func: callable
) -> Dict[str, Any]:
    """
    write_node 的完整实现：包含 LLM 调用逻辑。
    
    llm_func: 回调函数，签名为 (prompt: str) -> str
              由调用方注入，负责实际 LLM 调用。
              例如：lambda prompt: openai.ChatCompletion.create(
                      model="gpt-4", messages=[{"role":"user","content":prompt}]
                    ).choices[0].message.content
    
    返回值同 write_node()，但 content/key_conclusion/word_count 均已填充。
    """
    # 先获取 prompt 框架
    result = write_node(paper_name, node_id)
    if not result["ok"]:
        return result
    
    prompt_text = result["prompt"]
    
    # 构造系统 prompt：要求输出结构化 key_conclusion 标签
    system_prompt = (
        "你是一位专业的 MBA 学术论文写作者。"
        "请根据以下写作任务生成内容。"
        "生成完成后，请用 <key_conclusion>标签</key_conclusion> 包裹本节的核心结论，"
        "以便程序提取。\n\n"
        "写作要求：\n"
        "1. 内容需符合学术论文规范\n"
        "2. 逻辑清晰，论证充分\n"
        "3. 字数在指定范围内\n"
        "4. 结尾必须包含用 <key_conclusion> 包裹的结论摘要\n"
    )
    
    full_prompt = f"{system_prompt}\n\n{prompt_text}"
    
    try:
        response_text = llm_func(full_prompt)
    except Exception as e:
        return {
            **result,
            "ok": False,
            "error": f"LLM 调用失败: {str(e)}"
        }
    
    # 解析 response
    # 去掉 key_conclusion 标签部分，剩余为正文
    content_clean = re.sub(
        r'<key_conclusion>.*?</key_conclusion>',
        '',
        response_text,
        flags=re.DOTALL
    ).strip()
    
    # 提取 key_conclusion
    key_conclusion = extract_key_conclusion_from_response(response_text)
    
    # 字数
    word_count = count_words(content_clean)
    
    # 更新 state
    update_result = outline_update_status(
        paper_name, node_id, "completed",
        content=content_clean,
        key_conclusion=key_conclusion
    )
    
    return {
        **result,
        "content": content_clean,
        "key_conclusion": key_conclusion,
        "word_count": word_count,
        "state_updated": update_result.get("ok", False),
        "error": ""
    }


# ============================================================
# CLI 入口（供调试）
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <paper_name> <node_id>", file=sys.stderr)
        print("（CLI 模式仅供调试，实际调用需注入 LLM）", file=sys.stderr)
        sys.exit(1)
    
    paper_name = sys.argv[1]
    node_id = sys.argv[2]
    
    result = write_node(paper_name, node_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
