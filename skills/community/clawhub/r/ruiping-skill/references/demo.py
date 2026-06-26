#!/usr/bin/env python3
"""
锐评生成器 - 命令行工具
用法: python demo.py "事件描述" 或 python demo.py --file news.txt

本工具作为格式化框架，深度分析由SKILL.md指导AI完成。
"""

import argparse
import sys
import re
from datetime import datetime
from pathlib import Path


class RuiPingGenerator:
    """锐评生成器类 - 对齐SKILL.md v3.0标准输出格式"""
    
    def __init__(self):
        # 完全对齐SKILL.md v3.0的标准输出格式
        self.template = """📌 【锐评】{title}

📰 原新闻
{original_news}

📎 来源：{source}

一句话结论：{one_sentence_conclusion}

▌这事到底怎么了
{what_happened}

▌会怎么发展
{how_it_develops}

▌对谁有影响，影响多大
{who_affected}

▌你应该怎么做
{what_to_do}

▌一句话锐评
{final_comment}
"""
    
    def extract_keywords(self, event: str) -> list:
        """从事件描述中提取关键词"""
        stopwords = ['的', '了', '是', '在', '又', '很', '非常', '这个', '那个', '最近', '今天', '昨天', '一下', '什么', '怎么', '为什么']
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', event)
        return [w for w in words if w not in stopwords and len(w) > 1]
    
    def generate_title(self, event: str) -> str:
        """生成锐评标题 - 完整保留事件名称，不截断"""
        keywords = self.extract_keywords(event)
        if len(keywords) >= 2:
            # 不截断，完整保留前两个有意义的关键词
            return f"{keywords[0]}与{keywords[1]}"
        elif len(keywords) == 1:
            return keywords[0]
        return event
    
    def generate_original_news(self, event: str) -> str:
        """生成原新闻摘要"""
        # 作为格式化框架，这里给出占位提示
        return f"【由AI根据输入填充】{event}\n（AI将搜索新闻原文，提取核心事实和数据）"
    
    def generate_source(self, event: str) -> str:
        """生成来源信息"""
        return "【由AI根据搜索结果填充】"
    
    def generate_one_sentence_conclusion(self, event: str) -> str:
        """生成一句话结论"""
        keywords = self.extract_keywords(event)
        if len(keywords) >= 2:
            return f"表面是{keywords[0]}，实质是{keywords[1]}的博弈。"
        elif len(keywords) == 1:
            return f"{keywords[0]}这事，需要深入分析。"
        return "【由AI根据深度分析填充犀利判断】"
    
    def generate_what_happened(self, event: str) -> str:
        """生成'这事到底怎么了'分析"""
        return """【由AI根据输入填充】

分析框架：
- 表面新闻背后真正发生的事是什么？
- 这个政策/事件/变化的本质逻辑是什么？
- 背后的利益链条是什么？
"""
    
    def generate_how_it_develops(self, event: str) -> str:
        """生成"会怎么发展" """
        return f"""【由AI根据输入填充】

分析框架：
- 短期（1-3个月）会怎样？
- 中期（半年到1年）可能演化出什么？
- 最大的变量/变数是什么？
- 最可能的结果是什么？最坏的结果是什么？
"""
    
    def generate_who_affected(self, event: str) -> str:
        """生成"对谁有影响" """
        return f"""【由AI根据输入填充】

分析框架：
- 影响对象1：[具体机制、量级、时间线]
- 影响对象2：[同上]
- 影响对象3：[同上]

说明：如果是上市公司，需关联具体业务线、影响多大营收比例
"""
    
    def generate_what_to_do(self, event: str) -> str:
        """生成"你应该怎么做" """
        return f"""【由AI根据输入填充】

分析框架：
- 如果你是投资者：[具体方向、关联标的、时间窗口]
- 如果你是从业者：[对职业/业务的具体影响，该准备什么]
- 如果你是普通用户：[对你日常生活/消费的具体影响]
"""
    
    def generate_final_comment(self, event: str) -> str:
        """生成一句话锐评"""
        return "【由AI生成金句收尾，不是重复结论，是升华——让人看完想转发的那个点】"
    
    def generate(self, event: str) -> str:
        """生成完整锐评"""
        title = self.generate_title(event)
        original_news = self.generate_original_news(event)
        source = self.generate_source(event)
        one_sentence_conclusion = self.generate_one_sentence_conclusion(event)
        what_happened = self.generate_what_happened(event)
        how_it_develops = self.generate_how_it_develops(event)
        who_affected = self.generate_who_affected(event)
        what_to_do = self.generate_what_to_do(event)
        final_comment = self.generate_final_comment(event)
        
        return self.template.format(
            title=title,
            original_news=original_news,
            source=source,
            one_sentence_conclusion=one_sentence_conclusion,
            what_happened=what_happened,
            how_it_develops=how_it_develops,
            who_affected=who_affected,
            what_to_do=what_to_do,
            final_comment=final_comment
        )


def read_input(source: str) -> str:
    """读取输入内容"""
    path = Path(source)
    if path.exists() and path.is_file():
        try:
            return path.read_text(encoding='utf-8').strip()
        except UnicodeDecodeError:
            try:
                return path.read_text(encoding='gbk').strip()
            except Exception as e:
                raise ValueError(f"无法读取文件: {e}")
    return source


def save_output(content: str, output_path: str = None) -> str:
    """保存输出到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_path = f"ruiping_{timestamp}.md"
    save_path = output_path or default_path
    
    try:
        Path(save_path).write_text(content, encoding='utf-8')
        return save_path
    except Exception as e:
        raise ValueError(f"无法保存文件: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='锐评生成器 v3.0 - 对齐SKILL.md标准输出格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python demo.py "特斯拉又降价了"
  python demo.py --file news.txt
  python demo.py "OpenAI发布GPT-5，性能大幅提升" -o ai_review.md

注意:
  本工具作为格式化框架+事件解析框架使用，
  深度分析由SKILL.md指导AI根据实际新闻内容完成。
        """
    )
    
    parser.add_argument(
        'event',
        nargs='?',
        help='要锐评的事件描述'
    )
    parser.add_argument(
        '-f', '--file',
        help='从文件读取事件描述'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（可选，默认保存为 ruiping_时间戳.md）'
    )
    parser.add_argument(
        '-s', '--stdout-only',
        action='store_true',
        help='仅输出到stdout，不保存文件'
    )
    
    args = parser.parse_args()
    
    # 获取事件描述
    if args.file:
        try:
            event = read_input(args.file)
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.event:
        event = args.event
    else:
        print("错误: 请提供事件描述或使用 --file 指定文件", file=sys.stderr)
        print("使用 --help 查看帮助", file=sys.stderr)
        sys.exit(1)
    
    if not event:
        print("错误: 事件描述不能为空", file=sys.stderr)
        sys.exit(1)
    
    # 生成锐评
    generator = RuiPingGenerator()
    try:
        result = generator.generate(event)
    except Exception as e:
        print(f"错误: 生成锐评失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 输出结果
    print(result)
    
    # 保存文件
    if not args.stdout_only:
        try:
            saved_path = save_output(result, args.output)
            print(f"\n[已保存到: {saved_path}]", file=sys.stderr)
        except ValueError as e:
            print(f"警告: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
