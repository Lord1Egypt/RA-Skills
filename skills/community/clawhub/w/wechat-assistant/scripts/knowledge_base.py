#!/usr/bin/env python3
"""
知识库管理脚本
基于TF-IDF的轻量级知识检索系统，用于学习和匹配用户沟通风格
"""

import argparse
import json
import sys
import os
from datetime import datetime
from collections import defaultdict

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    print(json.dumps({
        "status": "error",
        "error": "缺少依赖库，请运行: pip install scikit-learn numpy"
    }, ensure_ascii=False))
    sys.exit(1)


class KnowledgeBase:
    def __init__(self, kb_file="kb_data.json"):
        self.kb_file = kb_file
        self.data = {
            "samples": [],
            "intents": {},
            "templates": {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self_vectors = None
        self._load()
    
    def _load(self):
        """加载知识库"""
        if os.path.exists(self.kb_file):
            try:
                with open(self.kb_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                self._build_index()
            except Exception:
                pass
    
    def _save(self):
        """保存知识库"""
        self.data["updated_at"] = datetime.now().isoformat()
        with open(self.kb_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def _build_index(self):
        """构建TF-IDF索引"""
        texts = [s["input"] + " " + s.get("output", "") for s in self.data["samples"]]
        if texts:
            self_vectors = self.vectorizer.fit_transform(texts)
    
    def add_samples(self, samples):
        """添加学习样本"""
        if isinstance(samples, str) and os.path.exists(samples):
            with open(samples, 'r', encoding='utf-8') as f:
                samples = json.load(f)
        
        if isinstance(samples, list):
            for item in samples:
                self.data["samples"].append({
                    "input": item.get("input", ""),
                    "output": item.get("output", ""),
                    "intent": item.get("intent", "general"),
                    "tags": item.get("tags", []),
                    "added_at": datetime.now().isoformat()
                })
            
            self._build_index()
            self._save()
            return True
        return False
    
    def add_intent(self, intent_name, patterns, responses):
        """添加意图模式"""
        self.data["intents"][intent_name] = {
            "patterns": patterns,
            "responses": responses
        }
        self._save()
        return True
    
    def add_template(self, template_type, content):
        """添加回复模板"""
        if template_type not in self.data["templates"]:
            self.data["templates"][template_type] = []
        self.data["templates"][template_type].append({
            "content": content,
            "added_at": datetime.now().isoformat()
        })
        self._save()
        return True
    
    def query(self, text, top_k=5):
        """查询相似样本"""
        if not self.data["samples"] or self_vectors is None:
            return []
        
        query_vec = self.vectorizer.transform([text])
        similarities = cosine_similarity(query_vec, self_vectors)[0]
        
        # 获取top_k相似结果
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:
                sample = self.data["samples"][idx]
                results.append({
                    "input": sample["input"],
                    "output": sample["output"],
                    "intent": sample.get("intent", "general"),
                    "tags": sample.get("tags", []),
                    "similarity": float(similarities[idx])
                })
        
        return results
    
    def get_intent(self, text):
        """识别意图"""
        text_lower = text.lower()
        for intent_name, intent_data in self.data["intents"].items():
            for pattern in intent_data.get("patterns", []):
                if pattern.lower() in text_lower:
                    return intent_name
        return "general"
    
    def get_response_by_intent(self, intent):
        """根据意图获取回复"""
        if intent in self.data["intents"]:
            responses = self.data["intents"][intent].get("responses", [])
            if responses:
                return responses[0]
        return None
    
    def get_template(self, template_type):
        """获取模板"""
        templates = self.data["templates"].get(template_type, [])
        return templates
    
    def generate_reply_suggestions(self, input_text, context=""):
        """生成回复建议"""
        # 1. 查询相似样本
        similar = self.query(input_text, top_k=5)
        
        # 2. 识别意图
        intent = self.get_intent(input_text)
        
        # 3. 获取模板
        templates = self.get_template(intent)
        
        suggestions = []
        
        # 从相似样本中提取回复
        for item in similar:
            if item["output"] and item["output"] not in [s["text"] for s in suggestions]:
                suggestions.append({
                    "text": item["output"],
                    "source": "similar_sample",
                    "confidence": item["similarity"]
                })
        
        # 从模板中添加
        for tmpl in templates[:2]:
            if tmpl["content"] not in [s["text"] for s in suggestions]:
                suggestions.append({
                    "text": tmpl["content"],
                    "source": "template",
                    "confidence": 0.7
                })
        
        # 按置信度排序
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        
        return suggestions[:5]
    
    def learn_from_conversation(self, user_input, agent_response):
        """从对话中学习"""
        self.data["samples"].append({
            "input": user_input,
            "output": agent_response,
            "intent": self.get_intent(user_input),
            "tags": [],
            "added_at": datetime.now().isoformat()
        })
        self._build_index()
        self._save()
        return True
    
    def get_stats(self):
        """获取统计信息"""
        return {
            "total_samples": len(self.data["samples"]),
            "total_intents": len(self.data["intents"]),
            "total_templates": sum(len(v) for v in self.data["templates"].values()),
            "created_at": self.data["created_at"],
            "updated_at": self.data["updated_at"]
        }


def main():
    parser = argparse.ArgumentParser(description='知识库管理工具')
    parser.add_argument('--action', required=True, 
                       choices=['add', 'query', 'add_intent', 'add_template', 'learn', 'stats'],
                       help='操作类型')
    parser.add_argument('--samples', help='样本文件路径(add/add_template)')
    parser.add_argument('--text', help='查询文本(query)')
    parser.add_argument('--top_k', type=int, default=5, help='返回结果数量')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--intent', help='意图名称(add_intent)')
    parser.add_argument('--patterns', help='意图模式，逗号分隔(add_intent)')
    parser.add_argument('--responses', help='回复内容，逗号分隔(add_intent)')
    parser.add_argument('--template_type', help='模板类型(add_template)')
    parser.add_argument('--content', help='模板内容(add_template)')
    parser.add_argument('--input', help='用户输入(learn)')
    parser.add_argument('--response', help='回复内容(learn)')
    parser.add_argument('--kb_file', default='./kb_data.json', help='知识库文件路径')
    
    args = parser.parse_args()
    
    kb = KnowledgeBase(args.kb_file)
    
    result = {"status": "success", "action": args.action}
    
    if args.action == 'add':
        if args.samples:
            kb.add_samples(args.samples)
            result["message"] = "样本添加成功"
        else:
            result["status"] = "error"
            result["error"] = "缺少samples参数"
    
    elif args.action == 'query':
        if args.text:
            results = kb.query(args.text, args.top_k)
            result["results"] = results
            result["count"] = len(results)
        else:
            result["status"] = "error"
            result["error"] = "缺少text参数"
    
    elif args.action == 'add_intent':
        if args.intent and args.patterns:
            patterns = args.patterns.split(',')
            responses = args.responses.split(',') if args.responses else []
            kb.add_intent(args.intent, patterns, responses)
            result["message"] = f"意图 {args.intent} 添加成功"
        else:
            result["status"] = "error"
            result["error"] = "缺少intent或patterns参数"
    
    elif args.action == 'add_template':
        if args.template_type and args.content:
            kb.add_template(args.template_type, args.content)
            result["message"] = "模板添加成功"
        else:
            result["status"] = "error"
            result["error"] = "缺少template_type或content参数"
    
    elif args.action == 'learn':
        if args.input and args.response:
            kb.learn_from_conversation(args.input, args.response)
            result["message"] = "学习成功"
        else:
            result["status"] = "error"
            result["error"] = "缺少input或response参数"
    
    elif args.action == 'stats':
        result["stats"] = kb.get_stats()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
