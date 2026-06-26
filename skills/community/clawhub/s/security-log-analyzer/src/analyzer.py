"""
安全事件日志分析器 - 主程序
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from llm_client import LLMClient


def truncate_log(log_content: str, max_tokens: int = 4000) -> str:
    """
    截断过长的日志内容
    
    Args:
        log_content: 原始日志
        max_tokens: 最大 token 数（估算：1 token ≈ 4 字符）
        
    Returns:
        截断后的日志
    """
    max_chars = max_tokens * 4
    if len(log_content) <= max_chars:
        return log_content
    
    # 保留开头和结尾
    head_len = max_chars // 2
    tail_len = max_chars // 2
    truncated = log_content[:head_len] + "\n\n... [内容已截断] ...\n\n" + log_content[-tail_len:]
    
    print(f"⚠️  日志过长，已截断至{max_chars}字符（原始：{len(log_content)}字符）")
    return truncated


def analyze_security_log(log_content: str, mode: str = "brief") -> str:
    """
    分析安全日志
    
    Args:
        log_content: 日志内容
        mode: 分析模式 ("brief" 或 "detailed")
        
    Returns:
        分析报告
    """
    # 截断过长的日志
    max_tokens = int(os.getenv("MAX_LOG_TOKENS", "4000"))
    log_content = truncate_log(log_content, max_tokens)
    
    # 创建客户端并分析
    client = LLMClient()
    print(f"🔍 正在{mode}分析日志...")
    
    report = client.analyze_log(log_content, mode)
    
    return report


def interactive_mode():
    """交互式分析模式"""
    print("=" * 60)
    print("🛡️  安全事件日志调查助手")
    print("=" * 60)
    print()
    
    # 选择分析模式
    print("请选择分析模式：")
    print("1. 简要分析（快速提取关键信息）")
    print("2. 详细分析（深度分析报告）")
    print()
    
    choice = input("输入选项 (1/2): ").strip()
    mode = "detailed" if choice == "2" else "brief"
    
    print()
    print("请输入安全日志内容（粘贴后按 Ctrl+D 或输入 END 结束）：")
    print("-" * 60)
    
    # 读取日志内容
    log_lines = []
    for line in sys.stdin:
        if line.strip() == "END":
            break
        log_lines.append(line)
    
    log_content = "".join(log_lines).strip()
    
    if not log_content:
        print("❌ 未输入日志内容")
        return
    
    print()
    print("=" * 60)
    
    # 执行分析
    try:
        report = analyze_security_log(log_content, mode)
        print(report)
        print("=" * 60)
        print("✅ 分析完成")
    except Exception as e:
        print(f"❌ 分析失败：{e}")


def main():
    """主函数"""
    # 检查环境变量
    if not os.getenv("SILICONFLOW_API_KEY"):
        print("❌ 错误：SILICONFLOW_API_KEY 未配置")
        print("请复制.env.example 为.env 并填写 API Key")
        sys.exit(1)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 从文件读取日志
        log_file = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "brief"
        
        if not os.path.exists(log_file):
            print(f"❌ 文件不存在：{log_file}")
            sys.exit(1)
        
        with open(log_file, "r", encoding="utf-8") as f:
            log_content = f.read()
        
        report = analyze_security_log(log_content, mode)
        print(report)
    else:
        # 交互模式
        interactive_mode()


if __name__ == "__main__":
    main()
