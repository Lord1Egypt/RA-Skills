#!/usr/bin/env python3
"""
Vocabulary Lookup - GPT4单词库查询工具
从8714词GPT4词典中查询单词详情
"""

import argparse
import json
import random
import os
import sys

# 默认词典路径（可配置）
DEFAULT_DICT_PATH = os.environ.get('VOCABULARY_DICT_PATH', 'dictionary-by-gpt4.json')


def get_dict_path():
    """获取词典路径"""
    env_path = os.environ.get('VOCABULARY_DICT_PATH')
    if env_path and os.path.exists(env_path):
        return env_path
    
    # 尝试当前目录
    if os.path.exists('dictionary-by-gpt4.json'):
        return 'dictionary-by-gpt4.json'
    
    # 尝试skill目录
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    local_dict = os.path.join(skill_dir, 'dictionary-by-gpt4.json')
    if os.path.exists(local_dict):
        return local_dict
    
    return None


def load_dict(dict_path=None):
    """加载词典（建立word->content的字典）"""
    if dict_path is None:
        dict_path = get_dict_path()
    
    if not dict_path or not os.path.exists(dict_path):
        print(f"错误：词典文件不存在: {dict_path}")
        print(f"\n请通过以下方式提供词典：")
        print(f"1. 设置环境变量：export VOCABULARY_DICT_PATH=/path/to/dictionary-by-gpt4.json")
        print(f"2. 命令行参数：--dict-path /path/to/dictionary-by-gpt4.json")
        print(f"3. 将词典文件放在当前目录或skill目录")
        print(f"\n词典文件获取方式：")
        print(f"- 从 ClawHub 或 GitHub 下载 dictionary-by-gpt4.json")
        print(f"- 或联系 Maosi English Team 获取")
        return None
    
    word_dict = {}
    print(f"加载词典: {dict_path}", end=" ", flush=True)
    
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    word = obj.get('word', '').upper()
                    word_dict[word] = obj.get('content', '')
                except json.JSONDecodeError:
                    continue
    
    print(f"完成，共 {len(word_dict)} 个单词")
    return word_dict


def lookup_word(word_dict, word):
    """查询单词"""
    result = word_dict.get(word.upper())
    if result:
        return format_output(word, result)
    else:
        return f"未找到单词: {word}"


def search_words(word_dict, query, limit=10):
    """模糊搜索"""
    query_upper = query.upper()
    matches = [w for w in word_dict.keys() if query_upper in w]
    if not matches:
        return f"未找到包含 '{query}' 的单词"
    
    results = []
    for i, word in enumerate(matches[:limit]):
        results.append(format_output(word, word_dict[word]))
    
    header = f"找到 {len(matches)} 个包含 '{query}' 的单词，显示前 {len(results)} 个：\n"
    return header + "\n---\n".join(results)


def random_words(word_dict, count=5):
    """随机抽取单词"""
    all_words = list(word_dict.keys())
    if count > len(all_words):
        count = len(all_words)
    
    selected = random.sample(all_words, count)
    results = []
    for word in selected:
        results.append(format_output(word, word_dict[word]))
    
    return f"随机抽取 {count} 个单词：\n\n" + "\n---\n".join(results)


def starts_with(word_dict, letter, limit=10):
    """按首字母筛选"""
    letter_upper = letter.upper()
    matches = [w for w in word_dict.keys() if w.startswith(letter_upper)]
    
    if not matches:
        return f"没有找到以 '{letter}' 开头的单词"
    
    results = []
    for word in matches[:limit]:
        results.append(format_output(word, word_dict[word]))
    
    header = f"以 '{letter_upper}' 开头的单词共 {len(matches)} 个，显示前 {len(results)} 个：\n"
    return header + "\n---\n".join(results)


def format_output(word, content):
    """格式化输出"""
    return f"### {word}\n\n{content}"


def main():
    parser = argparse.ArgumentParser(
        description='GPT4单词库查询',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 vocabulary_lookup.py --word camel
  python3 vocabulary_lookup.py --word apple --word banana
  python3 vocabulary_lookup.py --search app
  python3 vocabulary_lookup.py --random 5
  python3 vocabulary_lookup.py --dict-path /path/to/dictionary.json

词典路径优先级:
  1. 命令行 --dict-path 参数
  2. 环境变量 VOCABULARY_DICT_PATH
  3. 当前目录 dictionary-by-gpt4.json
  4. skill目录 dictionary-by-gpt4.json
        """
    )
    parser.add_argument('--word', '-w', action='append', help='查询的单词（可多个）')
    parser.add_argument('--search', '-s', help='模糊搜索')
    parser.add_argument('--random', '-r', type=int, help='随机抽取N个单词')
    parser.add_argument('--starts-with', '-a', help='按首字母筛选')
    parser.add_argument('--limit', '-l', type=int, default=10, help='结果显示数量')
    parser.add_argument('--dict-path', '-d', help='词典文件路径')
    
    args = parser.parse_args()
    
    word_dict = load_dict(args.dict_path)
    if not word_dict:
        sys.exit(1)
    
    if args.word:
        for word in args.word:
            print(f"\n{lookup_word(word_dict, word)}\n")
    
    if args.search:
        print(f"\n{search_words(word_dict, args.search, args.limit)}\n")
    
    if args.random:
        print(f"\n{random_words(word_dict, args.random)}\n")
    
    if args.starts_with:
        print(f"\n{starts_with(word_dict, args.starts_with, args.limit)}\n")
    
    if not any([args.word, args.search, args.random, args.starts_with]):
        parser.print_help()


if __name__ == "__main__":
    main()
