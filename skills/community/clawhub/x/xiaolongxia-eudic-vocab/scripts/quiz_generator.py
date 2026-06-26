#!/usr/bin/env python3
"""
欧路词典生词本测试题生成器
自动从生词本中抽取单词生成选择题
"""

import argparse
import random
import re
from vocab_manager import EudicVocabManager


class QuizGenerator:
    def __init__(self, token: str):
        self.manager = EudicVocabManager(token)
        self.words_cache = None
    
    def load_words(self, category_id: str = "0", language: str = "en") -> list:
        """加载所有单词"""
        if self.words_cache is None:
            print("正在加载生词本...")
            self.words_cache = self.manager.get_all_words(category_id, language)
            print(f"已加载 {len(self.words_cache)} 个单词")
        return self.words_cache
    
    def extract_simple_def(self, exp: str) -> str:
        """提取简洁的中文释义"""
        if not exp:
            return "暂无释义"
        # 去掉所有 HTML 标签
        clean = re.sub(r'<[^>]+>', '', exp)
        # 取第一行（按换行分割）
        first_line = clean.split('\n')[0].strip()
        # 如果还有<br>就再分割
        first_line = first_line.split('<br>')[0].strip()
        # 截取前40字
        if len(first_line) > 40:
            return first_line[:40] + "..."
        return first_line if first_line else "暂无释义"
    
    def generate_options(self, correct_word: dict, all_words: list, count: int = 4) -> list:
        """生成干扰选项 - 只显示释义，不显示单词，确保都有有效释义"""
        correct_exp = self.extract_simple_def(correct_word.get('exp', ''))
        
        # 从有有效释义的单词中选择干扰项
        other_words = [w for w in all_words 
                      if w.get('word') != correct_word.get('word') and 
                      self.extract_simple_def(w.get('exp', '')) != "暂无释义"]
        
        if len(other_words) < count - 1:
            print(f"警告: 只有 {len(other_words)} 个有效干扰项")
        
        distractors = random.sample(other_words, min(count-1, len(other_words)))
        
        # 只存储释义和是否正确，不显示单词
        options = [(correct_exp, True)]
        for w in distractors:
            exp = self.extract_simple_def(w.get('exp', ''))
            if exp != "暂无释义":
                options.append((exp, False))
        
        # 如果选项不够，补充一些通用干扰项
        while len(options) < count:
            generic_distractors = [
                "n. 某种抽象概念或物品",
                "adj. 描述某种状态或特征",
                "v. 表示某种动作或行为",
                "n. 人名或地名"
            ]
            options.append((random.choice(generic_distractors), False))
        
        random.shuffle(options)
        return options[:count]
    
    def generate_quiz(self, count: int = 10, category_id: str = "0", language: str = "en") -> list:
        """生成测试题 - 只选择有有效释义的单词"""
        words = self.load_words(category_id, language)
        
        # 过滤掉没有有效释义的单词
        valid_words = [w for w in words if self.extract_simple_def(w.get('exp', '')) != "暂无释义"]
        print(f"有效单词: {len(valid_words)} / {len(words)}")
        
        if len(valid_words) < count:
            print(f"警告: 只有 {len(valid_words)} 个单词有有效释义，少于要求的 {count} 题")
            count = len(valid_words)
        
        if count == 0:
            print("错误: 没有足够的有释义单词可以出题")
            return []
        
        selected = random.sample(valid_words, count)
        quiz = []
        
        for i, word in enumerate(selected, 1):
            options = self.generate_options(word, valid_words)
            quiz.append({
                "no": i,
                "word": word.get('word'),
                "phon": word.get('phon', ''),
                "question": f"{word.get('word')} 的意思是？",
                "options": options
            })
        
        return quiz
    
    def print_quiz(self, quiz: list):
        """打印测试题 - 只显示释义，不显示选项单词"""
        print("\n" + "="*50)
        print("📝 欧路词典生词本测试")
        print("="*50)
        
        for q in quiz:
            print(f"\n第{q['no']}题: {q['question']}")
            if q['phon']:
                print(f"音标: {q['phon']}")
            print("请选择正确释义：")
            
            for j, (exp, is_correct) in enumerate(q['options'], 1):
                label = chr(64 + j)  # A, B, C, D
                print(f"  {label}) {exp}")
        
        print("\n" + "="*50)
        print("请回复答案（如：A B C D...）")
        print("="*50)


def main():
    parser = argparse.ArgumentParser(description="欧路词典测试题生成器")
    parser.add_argument("--token", help="API Token，如不填则从环境变量 EUDIC_TOKEN 读取")
    parser.add_argument("--count", type=int, default=5, help="题目数量")
    parser.add_argument("--category-id", default="0", help="分类ID")
    parser.add_argument("--language", default="en", help="语言")
    
    args = parser.parse_args()
    
    # 优先从参数获取，其次环境变量
    token = args.token or os.environ.get("EUDIC_TOKEN")
    if not token:
        print("❌ 错误: 请提供 --token 或设置环境变量 EUDIC_TOKEN")
        sys.exit(1)
    
    generator = QuizGenerator(token)
    quiz = generator.generate_quiz(args.count, args.category_id, args.language)
    generator.print_quiz(quiz)
    
    # 保存答案供后续核对
    answers = []
    for q in quiz:
        for j, (exp, is_correct) in enumerate(q['options'], 1):
            if is_correct:
                answers.append(chr(64 + j))
                break
    
    print(f"\n💡 答案: {' '.join(answers)}")


if __name__ == "__main__":
    main()
