"""
transcript 对话提取工具
用于从 OpenClaw 的 JSONL transcript 文件中提取用户-助手的对话内容。
被 cron 的记忆同步脚本调用。

用法:
    python3 extract_dialog.py <transcript.jsonl>

输出格式:
    user: 用户消息
    assistant: 助手回复
    toolResult: 工具执行结果

注意:
    - 只提取最近 200 行
    - 只提取 type=message 的条目
    - 每条内容截断到 300 字符
    - 空内容跳过
"""
import json
import sys


def extract_dialog(filepath: str, max_lines: int = 200) -> list:
    """从 transcript JSONL 文件中提取对话内容
    
    Args:
        filepath: JSONL 文件路径
        max_lines: 读取的最大行数（从文件末尾算起）
    
    Returns:
        对话行列表，每行为 "role: content" 格式
    """
    lines = open(filepath).readlines()
    dialog = []
    
    for line in lines[-max_lines:]:
        try:
            msg = json.loads(line.strip())
            if msg.get('type') != 'message':
                continue
            
            message = msg.get('message', {})
            role = message.get('role', '')
            content = message.get('content', '')
            
            if isinstance(content, list):
                for c in content:
                    if c.get('type') == 'text' and c.get('text', '').strip():
                        dialog.append(f"{role}: {c['text'][:300]}")
            elif isinstance(content, str) and len(content) < 500 and content.strip():
                dialog.append(f"{role}: {content[:300]}")
        except (json.JSONDecodeError, KeyError):
            pass
    
    return dialog


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 extract_dialog.py <transcript.jsonl>", file=sys.stderr)
        sys.exit(1)
    
    filepath = sys.argv[1]
    dialog = extract_dialog(filepath)
    
    for line in dialog:
        print(line)
