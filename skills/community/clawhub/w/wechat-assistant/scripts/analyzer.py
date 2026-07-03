#!/usr/bin/env python3
"""
聊天数据分析脚本
对微信聊天记录进行深度分析，包括关键词提取、频率分析、意图分类、情感分析
"""

import argparse
import json
import sys
from datetime import datetime
from collections import Counter, defaultdict
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    import numpy as np
except ImportError:
    print(json.dumps({
        "status": "error",
        "error": "缺少依赖库，请运行: pip install scikit-learn numpy"
    }, ensure_ascii=False))
    sys.exit(1)


class ChatAnalyzer:
    # 情感词典
    POSITIVE_WORDS = {
        "好", "棒", "优秀", "感谢", "谢谢", "哈哈", "呵呵", "爱你", "喜欢",
        "赞", "不错", "厉害", "期待", "开心", "满意", "ok", "好的", "收到",
        "明白", "可以", "安排", "搞定", "成功", "达成", "完美"
    }
    
    NEGATIVE_WORDS = {
        "不", "没", "别", "难", "差", "错", "麻烦", "问题", "抱歉", "对不起",
        "取消", "算了", "不要", "不想", "困难", "担心", "焦虑", "失败"
    }
    
    # 意图关键词
    INTENT_KEYWORDS = {
        "schedule": ["明天", "后天", "下周", "几点", "时间", "安排", "预约", "什么时候"],
        "meeting": ["会议", "开会", "讨论", "商量", "约", "见面"],
        "question": ["怎么", "如何", "为什么", "什么", "多少", "能否", "可以"],
        "request": ["帮忙", "麻烦", "请", "帮我", "能不能", "方便"],
        "greeting": ["你好", "早上好", "晚安", "hi", "hello", "在吗"],
        "thanks": ["谢谢", "感谢", "辛苦了", "多谢"],
        "confirm": ["确认", "确定", "好的", "收到", "明白", "ok"]
    }
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        self.trained_model = None
    
    def load_data(self, input_file):
        """加载聊天数据"""
        if isinstance(input_file, str):
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("messages", [])
        return input_file
    
    def preprocess(self, text):
        """文本预处理"""
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_keywords(self, messages, top_n=20):
        """提取关键词"""
        texts = [self.preprocess(m.get("content", "")) for m in messages]
        texts = [t for t in texts if len(t) > 1]
        
        if not texts:
            return []
        
        try:
            self.tfidf_vectorizer.fit(texts)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # 计算每个词的TF-IDF总分
            tfidf_matrix = self.tfidf_vectorizer.transform(texts)
            word_scores = tfidf_matrix.sum(axis=0).A1
            
            # 排序
            word_scores = list(zip(feature_names, word_scores))
            word_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [{"word": w, "score": float(s)} for w, s in word_scores[:top_n]]
        except Exception:
            # 降级使用词频统计
            all_words = ' '.join(texts).split()
            counter = Counter(all_words)
            stop_words = {"的", "了", "是", "在", "我", "你", "他", "她", "它", "们", "有", "和"}
            filtered = {w: c for w, c in counter.items() if w not in stop_words and len(w) > 1}
            sorted_words = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
            return [{"word": w, "score": c} for w, c in sorted_words[:top_n]]
    
    def analyze_frequency(self, messages):
        """分析聊天频率"""
        time_counter = defaultdict(int)
        contact_counter = defaultdict(int)
        
        for msg in messages:
            contact = msg.get("contact", "unknown")
            contact_counter[contact] += 1
            
            time_str = msg.get("time", "")
            if time_str:
                try:
                    if len(time_str) == 5:  # HH:mm格式
                        hour = int(time_str.split(":")[0])
                        if 6 <= hour < 12:
                            time_counter["morning"] += 1
                        elif 12 <= hour < 14:
                            time_counter["noon"] += 1
                        elif 14 <= hour < 18:
                            time_counter["afternoon"] += 1
                        elif 18 <= hour < 22:
                            time_counter["evening"] += 1
                        else:
                            time_counter["night"] += 1
                except Exception:
                    pass
        
        return {
            "time_distribution": dict(time_counter),
            "contact_frequency": dict(contact_counter),
            "total_messages": len(messages)
        }
    
    def classify_intent(self, text):
        """意图分类"""
        text_lower = text.lower()
        scores = {}
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[intent] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        return "general"
    
    def analyze_intents(self, messages):
        """分析所有消息的意图分布"""
        intent_counter = defaultdict(int)
        
        for msg in messages:
            content = msg.get("content", "")
            if content:
                intent = self.classify_intent(content)
                intent_counter[intent] += 1
        
        total = sum(intent_counter.values()) or 1
        return {
            "distribution": {k: v for k, v in intent_counter.items()},
            "percentages": {
                k: round(v / total * 100, 1) 
                for k, v in intent_counter.items()
            }
        }
    
    def analyze_sentiment(self, messages):
        """情感分析"""
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for msg in messages:
            content = msg.get("content", "")
            content_set = set(content)
            
            pos = len(content_set & self.POSITIVE_WORDS)
            neg = len(content_set & self.NEGATIVE_WORDS)
            
            if pos > neg:
                positive_count += 1
            elif neg > pos:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(messages) or 1
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "percentages": {
                "positive": round(positive_count / total * 100, 1),
                "negative": round(negative_count / total * 100, 1),
                "neutral": round(neutral_count / total * 100, 1)
            }
        }
    
    def extract_requirements(self, messages):
        """挖掘需求信息"""
        requirements = []
        
        # 模式匹配
        patterns = {
            "schedule": r"(明天|后天|下周|这周)(\s*)([^\s]+)",
            "meeting": r"(约|见面|开会|讨论)(\s*)(.{0,20})",
            "deadline": r"(之前|之前|截止| deadline)(.{0,15})",
            "budget": r"([0-9]+)\s*(元|万|千|预算|价格|费用)",
            "quantity": r"([0-9]+)\s*(个|件|份|批)"
        }
        
        for msg in messages:
            content = msg.get("content", "")
            
            for req_type, pattern in patterns.items():
                matches = re.findall(pattern, content)
                for match in matches:
                    requirements.append({
                        "type": req_type,
                        "content": "".join(match) if isinstance(match, tuple) else match,
                        "source": content[:50],
                        "contact": msg.get("contact", "unknown")
                    })
        
        return requirements
    
    def analyze_interaction_pattern(self, messages):
        """分析互动模式"""
        exchanges = []
        current_exchange = []
        last_is_me = None
        
        for msg in messages:
            is_me = msg.get("is_from_me", False)
            
            if last_is_me is not None and is_me != last_is_me:
                if current_exchange:
                    exchanges.append(current_exchange)
                current_exchange = [msg]
            else:
                current_exchange.append(msg)
            
            last_is_me = is_me
        
        if current_exchange:
            exchanges.append(current_exchange)
        
        # 分析回复延迟(模拟)
        return {
            "total_exchanges": len(exchanges),
            "avg_exchange_length": round(
                sum(len(e) for e in exchanges) / len(exchanges), 1
            ) if exchanges else 0,
            "longest_exchange": max(len(e) for e in exchanges) if exchanges else 0
        }
    
    def generate_insights(self, analysis):
        """生成分析洞察"""
        insights = []
        
        # 基于意图分布
        if "distribution" in analysis["intents"]:
            top_intent = max(
                analysis["intents"]["distribution"].items(),
                key=lambda x: x[1]
            )
            insights.append(f"主要沟通类型是{top_intent[0]}，占比{top_intent[1]}条消息")
        
        # 基于情感
        if analysis["sentiment"]["percentages"]["positive"] > 50:
            insights.append("整体沟通氛围偏积极正向")
        elif analysis["sentiment"]["percentages"]["negative"] > 30:
            insights.append("需要注意部分沟通存在负面情绪")
        
        # 基于时间
        if "time_distribution" in analysis["frequency"]:
            peak_time = max(
                analysis["frequency"]["time_distribution"].items(),
                key=lambda x: x[1]
            ) if analysis["frequency"]["time_distribution"] else None
            if peak_time:
                time_names = {
                    "morning": "上午",
                    "noon": "中午",
                    "afternoon": "下午",
                    "evening": "傍晚",
                    "night": "晚上"
                }
                insights.append(f"沟通高峰时段在{time_names.get(peak_time[0], peak_time[0])}")
        
        # 基于需求
        if analysis["requirements"]:
            req_types = Counter(r["type"] for r in analysis["requirements"])
            top_req = req_types.most_common(1)
            if top_req:
                insights.append(f"识别到{len(analysis['requirements'])}个需求项，主要类型为{top_req[0][0]}")
        
        return insights
    
    def full_analysis(self, messages):
        """完整分析"""
        result = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(messages)
        }
        
        # 执行各项分析
        result["keywords"] = self.extract_keywords(messages)
        result["frequency"] = self.analyze_frequency(messages)
        result["intents"] = self.analyze_intents(messages)
        result["sentiment"] = self.analyze_sentiment(messages)
        result["requirements"] = self.extract_requirements(messages)
        result["interaction_pattern"] = self.analyze_interaction_pattern(messages)
        result["insights"] = self.generate_insights(result)
        
        return result
    
    def run(self, input_data, mode, output):
        """执行分析"""
        messages = self.load_data(input_data)
        
        if mode == "analyze":
            result = self.full_analysis(messages)
        elif mode == "keywords":
            result = {
                "status": "success",
                "keywords": self.extract_keywords(messages)
            }
        elif mode == "intents":
            result = {
                "status": "success",
                "intents": self.analyze_intents(messages)
            }
        elif mode == "sentiment":
            result = {
                "status": "success",
                "sentiment": self.analyze_sentiment(messages)
            }
        elif mode == "requirements":
            result = {
                "status": "success",
                "requirements": self.extract_requirements(messages)
            }
        else:
            result = {"status": "error", "error": f"未知模式: {mode}"}
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            result["file_saved"] = output
        
        return result


def main():
    parser = argparse.ArgumentParser(description='聊天数据分析工具')
    parser.add_argument('--input', required=True, help='输入JSON文件路径')
    parser.add_argument('--mode', default='analyze',
                       choices=['analyze', 'keywords', 'intents', 'sentiment', 'requirements'],
                       help='分析模式')
    parser.add_argument('--output', help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    analyzer = ChatAnalyzer()
    result = analyzer.run(args.input, args.mode, args.output)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
