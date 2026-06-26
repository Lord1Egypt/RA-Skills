#!/usr/bin/env python3
"""
Moji辞書每日词汇测试生成器
"""

import argparse
import json
import os
import random
import sys
from moji_manager import MojiVocabManager


class MojiQuizGenerator:
    def __init__(self, token: str, device_id: str):
        self.manager = MojiVocabManager(token, device_id)
        self.words_cache = None
    
    def load_words(self, max_pages: int = 10) -> list:
        """加载单词（默认前10页=300个）"""
        if self.words_cache is None:
            print("正在加载 Moji 收藏夹...")
            self.words_cache = self.manager.get_all_words(max_pages=max_pages)
            print(f"已加载 {len(self.words_cache)} 个单词")
        return self.words_cache
    
    def extract_def(self, word_data: dict) -> str:
        """提取中文释义"""
        target = word_data.get("target", {})
        
        # 优先使用 excerpt（摘要）
        excerpt = target.get("excerpt", "")
        if excerpt:
            # 去掉 [名·サ变] 这样的标签，取后面的释义
            import re
            clean = re.sub(r'\[.*?\]', '', excerpt).strip()
            return clean[:50] + "..." if len(clean) > 50 else clean
        
        # 其次使用 translation
        trans = target.get("translation", "")
        if trans:
            return trans[:50] + "..." if len(trans) > 50 else trans
        
        return "暂无释义"
    
    def get_jlpt_level(self, word_data: dict) -> str:
        """获取 JLPT 级别"""
        target = word_data.get("target", {})
        tags = target.get("tags", "") or ""
        
        for level in ["N1", "N2", "N3", "N4", "N5"]:
            if level in tags:
                return level
        return "未知"
    
    def generate_options(self, correct_word: dict, all_words: list, count: int = 4) -> list:
        """生成选项"""
        correct_def = self.extract_def(correct_word)
        correct_word_text = self.get_word_text(correct_word)
        
        # 选择干扰项（不同单词）
        other_words = [w for w in all_words 
                      if self.get_word_text(w) != correct_word_text]
        distractors = random.sample(other_words, min(count-1, len(other_words)))
        
        options = [(correct_def, True)]
        for w in distractors:
            d = self.extract_def(w)
            if d != "暂无释义":
                options.append((d, False))
        
        # 补充通用选项
        while len(options) < count:
            generic = ["n. 某种物品或概念", "v. 某种动作", "adj. 某种状态/特征"]
            options.append((random.choice(generic), False))
        
        random.shuffle(options)
        return options[:count]
    
    def get_word_text(self, word_data: dict) -> str:
        """获取单词文本（日语）"""
        target = word_data.get("target", {})
        # 优先使用 spell（汉字），其次 pron（假名）
        spell = target.get("spell", "")
        pron = target.get("pron", "")
        if spell and pron:
            return f"{spell} | {pron}"
        return spell or pron or "未知"
    
    def generate_quiz(self, count: int = 5) -> list:
        """生成测试题"""
        words = self.load_words()
        
        # 过滤有释义的单词
        valid_words = [w for w in words if self.extract_def(w) != "暂无释义"]
        
        if len(valid_words) < count:
            print(f"警告: 只有 {len(valid_words)} 个有效单词")
            count = len(valid_words)
        
        if count == 0:
            print("错误: 没有可用单词")
            return []
        
        selected = random.sample(valid_words, count)
        quiz = []
        
        for i, word in enumerate(selected, 1):
            target = word.get("target", {})
            word_text = self.get_word_text(word)
            romaji = target.get("romaji", "")
            level = self.get_jlpt_level(word)
            
            options = self.generate_options(word, valid_words)
            
            quiz.append({
                "no": i,
                "word": word_text,
                "romaji": romaji,
                "level": level,
                "question": f"{word_text} ({level}) 的意思是？",
                "options": options
            })
        
        return quiz
    
    def print_quiz(self, quiz: list):
        """打印测试题"""
        print("\n" + "="*50)
        print("🇯🇵 Moji辞書每日词汇测试")
        print("="*50)
        
        for q in quiz:
            print(f"\n第{q['no']}题: {q['question']}")
            if q.get('romaji'):
                print(f"罗马音: {q['romaji']}")
            print()
            
            for j, (exp, is_correct) in enumerate(q['options'], 1):
                label = chr(64 + j)
                print(f"{label}) {exp}")
        
        print("\n" + "="*50)
        print("请回复答案（如：A B C D E）")
        print("="*50)


def main():
    parser = argparse.ArgumentParser(description="Moji辞書测试生成器")
    parser.add_argument("--token", help="sessionToken，或设置环境变量 MOJI_TOKEN")
    parser.add_argument("--device-id", help="deviceId，或设置环境变量 MOJI_DEVICE_ID")
    parser.add_argument("--count", type=int, default=5, help="题目数量")
    
    args = parser.parse_args()
    
    token = args.token or os.environ.get("MOJI_TOKEN")
    device_id = args.device_id or os.environ.get("MOJI_DEVICE_ID")
    
    if not token or not device_id:
        print("❌ 错误: 请提供 --token 和 --device-id，或设置环境变量")
        sys.exit(1)
    
    generator = MojiQuizGenerator(token, device_id)
    quiz = generator.generate_quiz(args.count)
    
    if quiz:
        generator.print_quiz(quiz)
        
        # 保存答案
        answers = []
        for q in quiz:
            for j, (exp, is_correct) in enumerate(q['options'], 1):
                if is_correct:
                    answers.append(chr(64 + j))
                    break
        print(f"\n💡 答案: {' '.join(answers)}")


if __name__ == "__main__":
    main()
