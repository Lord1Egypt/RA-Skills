#!/usr/bin/env python3
"""Speculative Exec - Predict and pre-load context.
Distilled from Claude Code speculation module.
"""
import re, json, sys, os, argparse, threading, time

WORKFLOW_PATTERNS = [
    {"name":"analyze_stock","patterns":[r"分析.*(?:股票|行情|走势|K线|技术)",r"analyze.*(?:stock|chart|trend)"],"confidence":0.85,"preload":["stock_price","financial_report","news","technical_indicators"]},
    {"name":"analyze_data","patterns":[r"分析.*(?:数据|报告|结果|报表)",r"analyze.*(?:data|report|result)"],"confidence":0.80,"preload":["data_source","previous_analysis"]},
    {"name":"compare_items","patterns":[r"对比|比较|区别|差异|vs|versus"],"confidence":0.90,"preload":["item_a","item_b"]},
    {"name":"search","patterns":[r"搜索|查找|找.*(?:文件|资料|信息|代码)",r"search|find|look for|locate"],"confidence":0.75,"preload":["search_index"]},
    {"name":"read_file","patterns":[r"读.*(?:文件|配置|日志|源码)",r"read|open|show|display|cat\\s+"],"confidence":0.85,"preload":["target_file"]},
    {"name":"write_code","patterns":[r"写.*(?:代码|函数|类|模块|脚本)",r"write|create|implement|code.*(?:function|class|module)"],"confidence":0.80,"preload":["project_context","code_templates","existing_code"]},
    {"name":"edit_code","patterns":[r"修改|更新|重构|优化|refactor|update|modify|change|fix|bug"],"confidence":0.75,"preload":["target_file","related_files"]},
    {"name":"test","patterns":[r"测试|单元测试|集成测试|pytest|unittest|test"],"confidence":0.80,"preload":["test_files","test_fixtures","source_code"]},
    {"name":"deploy","patterns":[r"部署|发布|上线|deploy|release|publish|ship"],"confidence":0.70,"preload":["config_files","deploy_scripts","env_vars"]},
    {"name":"explain","patterns":[r"解释|说明|原理|为什么|how.*work|what.*mean|explain|describe"],"confidence":0.70,"preload":["relevant_docs","code_context"]},
    {"name":"summarize","patterns":[r"总结|摘要|概括|summarize|summary|TLDR|tl;dr"],"confidence":0.75,"preload":["full_content","previous_summaries"]},
    {"name":"debug","patterns":[r"debug|调试|报错|错误|异常|exception|traceback|error|crash"],"confidence":0.85,"preload":["error_logs","stack_trace","recent_changes"]},
]

class SpeculativeCache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
        self._timestamps = {}
    def get(self, key):
        with self._lock: return self._cache.get(key)
    def set(self, key, value, ttl_seconds=300):
        with self._lock:
            self._cache[key] = value
            self._timestamps[key] = time.time() + ttl_seconds
    def is_fresh(self, key):
        with self._lock:
            if key not in self._timestamps: return False
            return time.time() < self._timestamps[key]
    def invalidate(self, key=None):
        with self._lock:
            if key: self._cache.pop(key,None); self._timestamps.pop(key,None)
            else: self._cache.clear(); self._timestamps.clear()
    def status(self):
        with self._lock:
            fresh = sum(1 for k in self._timestamps if time.time() < self._timestamps[k])
            return {"total":len(self._cache),"fresh":fresh,"keys":list(self._cache.keys())}

cache = SpeculativeCache()

def predict(message, confidence_threshold=0.7):
    predictions = []
    for wf in WORKFLOW_PATTERNS:
        for pat in wf["patterns"]:
            if re.search(pat, message):
                predictions.append({"name":wf["name"],"confidence":wf["confidence"],"preload":wf["preload"]})
                break
    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    return [p for p in predictions if p["confidence"] >= confidence_threshold]

def preload_resources(predictions, workspace=None):
    start = time.time()
    loaded = []
    for pred in predictions:
        for resource in pred["preload"]:
            if not cache.is_fresh(resource):
                cache.set(resource, {"status":"preloaded","prediction":pred["name"],"timestamp":time.time()})
                loaded.append(resource)
    elapsed = int((time.time() - start) * 1000)
    return {"loaded": loaded, "elapsed_ms": elapsed}

def predict_from_history(history):
    if not history: return []
    user_msgs = [m.get("content","") for m in history if m.get("role")=="user"][-3:]
    combined = " ".join(user_msgs)
    return predict(combined, confidence_threshold=0.6)

def train(custom_patterns):
    global WORKFLOW_PATTERNS
    WORKFLOW_PATTERNS = WORKFLOW_PATTERNS + custom_patterns
    return {"status":"ok","total_patterns":len(WORKFLOW_PATTERNS)}

def main():
    parser = argparse.ArgumentParser(description="Speculative Exec")
    parser.add_argument("--message","-m",help="User message to predict from")
    parser.add_argument("--history","-f",help="Conversation history JSON file")
    parser.add_argument("--train","-t",help="Custom workflow patterns JSON file")
    parser.add_argument("--status","-s",action="store_true",help="Show cache status")
    parser.add_argument("--threshold",type=float,default=0.7,help="Confidence threshold (0-1)")
    parser.add_argument("--json",action="store_true",help="JSON output")
    args = parser.parse_args()
    if args.status:
        result = {"cache": cache.status()}
        if args.json: print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            s = result["cache"]
            print(f"Cache: {s['fresh']}/{s['total']} fresh | Keys: {s['keys']}")
        return
    if args.train:
        with open(args.train,"r",encoding="utf-8") as f: patterns = json.load(f)
        result = train(patterns)
        if args.json: print(json.dumps(result, indent=2))
        else: print(f"Trained: {result['total_patterns']} total patterns")
        return
    if args.history:
        with open(args.history,"r",encoding="utf-8") as f: history = json.load(f)
        predictions = predict_from_history(history)
    elif args.message:
        predictions = predict(args.message, args.threshold)
    else:
        predictions = predict("", args.threshold)
    if predictions:
        preload_result = preload_resources(predictions)
        result = {"predictions": predictions, "preload": preload_result}
    else:
        result = {"predictions": [], "preload": {"loaded": [], "elapsed_ms": 0}, "note": "No predictions above threshold"}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if not predictions:
            print("[?] No predictions above threshold")
            return
        for p in predictions:
            icon = "[OK]" if p["confidence"] >= 0.8 else "[?]"
            print(f"{icon} {p['name']} (confidence: {p['confidence']:.2f})")
            print(f"  Pre-load: {', '.join(p['preload'])}")
        pr = result["preload"]
        print(f"\nPre-loaded {len(pr['loaded'])} resources in {pr['elapsed_ms']}ms")

if __name__ == "__main__": main()