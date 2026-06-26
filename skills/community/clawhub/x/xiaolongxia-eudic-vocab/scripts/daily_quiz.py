#!/usr/bin/env python3
"""
欧路词典每日词汇测试 - 用于 Cron 定时任务
每天早上自动发送测试题
"""

import argparse
import json
from quiz_generator import QuizGenerator

def main():
    parser = argparse.ArgumentParser(description="欧路词典每日词汇测试")
    parser.add_argument("--token", help="API Token，如不填则从环境变量 EUDIC_TOKEN 读取")
    parser.add_argument("--count", type=int, default=5, help="题目数量")
    parser.add_argument("--output", default="quiz_output.json", help="输出文件")
    
    args = parser.parse_args()
    
    # 优先从参数获取，其次环境变量
    token = args.token or os.environ.get("EUDIC_TOKEN")
    if not token:
        print("❌ 错误: 请提供 --token 或设置环境变量 EUDIC_TOKEN")
        sys.exit(1)
    
    generator = QuizGenerator(token)
    quiz = generator.generate_quiz(args.count)
    
    if not quiz:
        print("❌ 生成测试题失败")
        return
    
    # 保存到文件供后续使用
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(quiz, f, ensure_ascii=False, indent=2)
    
    # 打印测试题（用于飞书发送）
    print("📚 今日欧路词典词汇测试\n")
    
    for q in quiz:
        print(f"第{q['no']}题: {q['question']}")
        if q['phon']:
            print(f"音标: {q['phon']}")
        print()
        for j, (exp, is_correct) in enumerate(q['options'], 1):
            label = chr(64 + j)
            print(f"{label}) {exp}")
        print()
    
    print("请回复答案（如：A B C D E）")
    
    # 保存答案
    answers = []
    for q in quiz:
        for j, (exp, is_correct) in enumerate(q['options'], 1):
            if is_correct:
                answers.append({
                    "no": q['no'],
                    "word": q['word'],
                    "answer": chr(64 + j),
                    "exp": exp
                })
                break
    
    with open(args.output + '.answers.json', 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
