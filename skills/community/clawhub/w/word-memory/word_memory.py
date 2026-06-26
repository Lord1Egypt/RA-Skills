#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 Word Memory - 单词记忆助手
功能：艾宾浩斯记忆曲线、每日单词推送、单词测试
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta

# 数据文件路径
DATA_DIR = Path(__file__).parent
PROGRESS_FILE = DATA_DIR / "progress.json"
STATS_FILE = DATA_DIR / "stats.json"

# 艾宾浩斯复习间隔（小时）
EBBINGHAUS_INTERVALS = [0.08, 0.5, 12, 24, 48, 96, 168, 360]  # 5min, 30min, 12h, 1d, 2d, 4d, 7d, 15d

# 单词库（示例，实际应导入完整词库）
WORD_DATABASE = {
    "CET-4": [
        {"word": "abandon", "phonetic": "/əˈbændən/", "meaning": "v. 放弃，抛弃", "example": "He abandoned his plan to travel.", "root": "a-(加强) + ban(禁止) → 彻底禁止 → 放弃"},
        {"word": "ability", "phonetic": "/əˈbɪləti/", "meaning": "n. 能力，才能", "example": "She has the ability to pass the exam.", "root": "abil(能) + -ity(名词后缀)"},
        {"word": "abnormal", "phonetic": "/æbˈnɔːrməl/", "meaning": "adj. 异常的，反常的", "example": "The weather is abnormal for this time of year.", "root": "ab-(离开) + normal(正常)"},
        {"word": "aboard", "phonetic": "/əˈbɔːrd/", "meaning": "adv. 在船/车/飞机上", "example": "Welcome aboard!", "root": "a-(在) + board(板) → 在甲板上"},
        {"word": "absolute", "phonetic": "/ˈæbsəluːt/", "meaning": "adj. 绝对的，完全的", "example": "I have absolute confidence in you.", "root": "ab-(加强) + solute(松开) → 完全松开 → 绝对的"},
        {"word": "absorb", "phonetic": "/əbˈzɔːrb/", "meaning": "v. 吸收，吸引", "example": "Plants absorb sunlight.", "root": "ab-(加强) + sorb(吸收)"},
        {"word": "academic", "phonetic": "/ˌækəˈdemɪk/", "meaning": "adj. 学术的，学院的", "example": "The university has high academic standards.", "root": "academ(学院) + -ic(形容词后缀)"},
        {"word": "accelerate", "phonetic": "/əkˈseləreɪt/", "meaning": "v. 加速，促进", "example": "The car accelerated to overtake.", "root": "ac-(加强) + celer(快) + -ate(动词后缀)"},
        {"word": "access", "phonetic": "/ˈækses/", "meaning": "n. 入口，通道 v. 访问", "example": "Students need access to the library.", "root": "ac-(加强) + cess(走) → 走到 → 接近"},
        {"word": "accommodate", "phonetic": "/əˈkɑːmədeɪt/", "meaning": "v. 容纳，提供住宿", "example": "The hotel can accommodate 500 guests.", "root": "ac-(加强) + commod(方便) + -ate → 提供方便"},
    ],
    "CET-6": [
        {"word": "abrupt", "phonetic": "/əˈbrʌpt/", "meaning": "adj. 突然的，唐突的", "example": "The meeting came to an abrupt end.", "root": "ab-(离开) + rupt(断) → 突然断开"},
        {"word": "absurd", "phonetic": "/əbˈsɜːrd/", "meaning": "adj. 荒谬的，可笑的", "example": "That's an absurd idea.", "root": "ab-(加强) + surd(不合理)"},
        {"word": "abundance", "phonetic": "/əˈbʌndəns/", "meaning": "n. 丰富，充裕", "example": "There is an abundance of food.", "root": "ab-(加强) + und(波浪) + -ance → 像波浪一样多"},
    ],
    "考研": [
        {"word": "abolish", "phonetic": "/əˈbɑːlɪʃ/", "meaning": "v. 废除，取消", "example": "Slavery was abolished in the 19th century.", "root": "ab-(离开) + olish(消除)"},
        {"word": "abrupt", "phonetic": "/əˈbrʌpt/", "meaning": "adj. 突然的，唐突的", "example": "An abrupt change.", "root": "ab-(离开) + rupt(断)"},
    ],
}


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"learned": [], "config": {"daily_new": 20, "push_time": "08:00", "word_list": "CET-4"}}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_next_review_time(learned_date, review_count):
    """计算下次复习时间"""
    if review_count >= len(EBBINGHAUS_INTERVALS):
        return None  # 已掌握
    
    hours = EBBINGHAUS_INTERVALS[review_count]
    next_time = learned_date + timedelta(hours=hours)
    return next_time


def get_due_words(progress):
    """获取需要复习的单词"""
    now = datetime.now()
    due_words = []
    
    for item in progress["learned"]:
        if "next_review" not in item:
            continue
        
        next_review = datetime.fromisoformat(item["next_review"])
        if next_review <= now:
            due_words.append(item)
    
    return due_words


def learn_new_words(word_list, count=20):
    """学习新单词"""
    if word_list not in WORD_DATABASE:
        return []
    
    words = WORD_DATABASE[word_list]
    return random.sample(words, min(count, len(words)))


def calculate_mastery(error_count, review_count):
    """计算掌握程度"""
    if review_count == 0:
        return 0.0
    
    # 简单算法：错误率越低，掌握度越高
    error_rate = error_count / review_count
    mastery = max(0, 1 - error_rate)
    return round(mastery, 2)


def add_learned_word(progress, word, correct=True):
    """添加或更新已学单词"""
    learned = progress["learned"]
    
    # 查找是否已存在
    for item in learned:
        if item["word"] == word["word"]:
            item["review_count"] += 1
            if not correct:
                item["error_count"] += 1
            
            item["mastery"] = calculate_mastery(item["error_count"], item["review_count"])
            item["last_review"] = datetime.now().isoformat()
            
            next_review = get_next_review_time(datetime.now(), item["review_count"])
            if next_review:
                item["next_review"] = next_review.isoformat()
            else:
                item["status"] = "mastered"
            
            return progress
    
    # 新单词
    learned.append({
        "word": word["word"],
        "phonetic": word["phonetic"],
        "meaning": word["meaning"],
        "example": word["example"],
        "root": word["root"],
        "learned_date": datetime.now().isoformat(),
        "review_count": 1 if correct else 0,
        "error_count": 0 if correct else 1,
        "mastery": 1.0 if correct else 0.0,
        "last_review": datetime.now().isoformat(),
        "next_review": get_next_review_time(datetime.now(), 1).isoformat() if correct else None,
        "status": "learning"
    })
    
    return progress


def generate_quiz(word):
    """生成测试题"""
    # 生成选项（1 个正确 + 3 个错误）
    all_words = []
    for words in WORD_DATABASE.values():
        all_words.extend(words)
    
    wrong_options = random.sample([w for w in all_words if w["word"] != word["word"]], 3)
    options = [word] + wrong_options
    random.shuffle(options)
    
    return {
        "question": f"""{word['word']} {word['phonetic']}""",
        "options": options,
        "answer": word["word"]
    }


def format_word(word, show_all=True):
    """格式化单词信息"""
    info = f"""📖 **{word['word']}** {word['phonetic']}
📝 释义：{word['meaning']}"""
    
    if show_all:
        info += f"""
📖 例句：{word['example']}
🌳 词根：{word['root']}"""
    
    return info


def main(query):
    """主函数"""
    query = query.lower()
    progress = load_json(PROGRESS_FILE)
    
    # 开始学习
    if "开始" in query or "学习" in query:
        # 获取今日新词
        config = progress["config"]
        new_words = learn_new_words(config["word_list"], config["daily_new"])
        
        # 获取待复习
        due_words = get_due_words(progress)
        
        response = f"""📚 **今日学习计划** ({datetime.now().strftime('%Y-%m-%d')})

📖 新词 ({len(new_words)}个)
"""
        for i, w in enumerate(new_words[:5], 1):  # 只显示前 5 个
            response += f"{i}. {format_word(w)}\n\n"
        
        if len(new_words) > 5:
            response += f"... 还有{len(new_words) - 5}个\n\n"
        
        if due_words:
            response += f"""
📝 复习 ({len(due_words)}个)
"""
            for i, w in enumerate(due_words[:3], 1):
                response += f"{i}. {w['word']} - 掌握度{w.get('mastery', 0)*100:.0f}%\n"
        
        return response
    
    # 测试
    if "测试" in query or "考我" in query:
        # 随机选一个单词
        all_words = []
        for words in WORD_DATABASE.values():
            all_words.extend(words)
        
        word = random.choice(all_words)
        quiz = generate_quiz(word)
        
        response = f"""📝 **单词测试**

{quiz['question']} 的意思是？

A. {quiz['options'][0]['meaning'].split('。')[0]}
B. {quiz['options'][1]['meaning'].split('。')[0]}
C. {quiz['options'][2]['meaning'].split('。')[0]}
D. {quiz['options'][3]['meaning'].split('。')[0]}

回复 A/B/C/D 作答"""
        return response
    
    # 查询单词
    if "查" in query:
        for word_list, words in WORD_DATABASE.items():
            for word in words:
                if word["word"] in query:
                    return format_word(word)
    
    # 设置词库
    for level in WORD_DATABASE.keys():
        if level in query:
            progress["config"]["word_list"] = level
            save_json(PROGRESS_FILE, progress)
            return f"✅ 已切换到 **{level}** 词库"
    
    # 设置每日数量
    if "每日" in query or "每天" in query:
        import re
        match = re.search(r'(\d+)', query)
        if match:
            count = int(match.group(1))
            progress["config"]["daily_new"] = count
            save_json(PROGRESS_FILE, progress)
            return f"✅ 已设置每日新词 **{count}** 个"
    
    # 进度统计
    if "进度" in query or "统计" in query:
        learned_count = len(progress["learned"])
        mastered_count = len([w for w in progress["learned"] if w.get("status") == "mastered"])
        
        return f"""📊 **学习进度**

📖 已学单词：{learned_count}
✅ 已掌握：{mastered_count}
📈 掌握率：{mastered_count/learned_count*100:.1f}% (如有数据)

配置：
- 词库：{progress['config']['word_list']}
- 每日新词：{progress['config']['daily_new']}
- 推送时间：{progress['config']['push_time']}"""
    
    # 默认回复
    return """📚 我可以帮你：
1. **开始学习** - "开始学习"
2. **单词测试** - "测试我"
3. **查询单词** - "查 abandon"
4. **切换词库** - "切换到六级"
5. **设置数量** - "每日 30 个"
6. **查看进度** - "学习进度"

告诉我你想做什么？👻"""


if __name__ == "__main__":
    # 测试
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("开始学习"))
