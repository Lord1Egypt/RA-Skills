#!/usr/bin/env python3
"""
自动回复引擎脚本
结合知识库生成回复内容，并提供审核工作流
"""

import argparse
import json
import sys
import os
from datetime import datetime

# 导入知识库
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from knowledge_base import KnowledgeBase


class AutoReplyEngine:
    def __init__(self, kb_file="kb_data.json"):
        self.kb = KnowledgeBase(kb_file)
        self.reply_history = []
        
    def generate_candidates(self, input_text, contact, context=""):
        """生成多个候选回复"""
        # 1. 知识库检索
        kb_suggestions = self.kb.generate_reply_suggestions(input_text, context)
        
        # 2. 基于意图生成
        intent = self.kb.get_intent(input_text)
        intent_response = self.kb.get_response_by_intent(intent)
        
        candidates = []
        seen_texts = set()
        
        # 添加知识库回复
        for suggestion in kb_suggestions[:3]:
            text = suggestion["text"]
            if text not in seen_texts:
                candidates.append({
                    "text": text,
                    "source": suggestion["source"],
                    "confidence": suggestion["confidence"],
                    "type": "kb_generated"
                })
                seen_texts.add(text)
        
        # 添加意图回复
        if intent_response and intent_response not in seen_texts:
            candidates.append({
                "text": intent_response,
                "source": "intent_matched",
                "confidence": 0.8,
                "type": "intent_matched"
            })
            seen_texts.add(intent_response)
        
        # 通用回复模板
        if not candidates:
            candidates.append({
                "text": "收到，我会跟进处理。",
                "source": "fallback",
                "confidence": 0.5,
                "type": "fallback"
            })
            candidates.append({
                "text": "好的，我明白了，请稍等。",
                "source": "fallback",
                "confidence": 0.4,
                "type": "fallback"
            })
            candidates.append({
                "text": "收到消息，稍后回复您。",
                "source": "fallback",
                "confidence": 0.3,
                "type": "fallback"
            })
        
        return candidates
    
    def create_audit_request(self, input_text, contact, candidates):
        """创建审核请求"""
        request = {
            "id": f"req_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "contact": contact,
            "input_message": input_text,
            "candidates": candidates,
            "status": "pending_audit"
        }
        
        # 保存审核请求
        self.reply_history.append(request)
        self._save_history()
        
        return request
    
    def process_audit(self, request_id, decision, modified_text=None):
        """处理审核决策"""
        request = None
        for req in self.reply_history:
            if req["id"] == request_id:
                request = req
                break
        
        if not request:
            return {
                "status": "error",
                "error": f"未找到审核请求: {request_id}"
            }
        
        result = {
            "request_id": request_id,
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        }
        
        if decision == "approve":
            if request["candidates"]:
                # 选择置信度最高的
                best = max(request["candidates"], key=lambda x: x["confidence"])
                result["selected_reply"] = best["text"]
                result["ready_to_send"] = True
            else:
                result["status"] = "error"
                result["error"] = "没有可发送的回复"
        
        elif decision == "modify":
            if modified_text:
                result["selected_reply"] = modified_text
                result["ready_to_send"] = True
            else:
                result["status"] = "error"
                result["error"] = "修改模式下需要提供modified_text"
        
        elif decision == "reject":
            result["selected_reply"] = None
            result["ready_to_send"] = False
            result["message"] = "已拒绝发送"
        
        # 更新请求状态
        request["status"] = f"audited_{decision}"
        request["audit_result"] = result
        self._save_history()
        
        return result
    
    def execute_send(self, request_id):
        """执行发送(模拟)"""
        request = None
        for req in self.reply_history:
            if req["id"] == request_id:
                request = req
                break
        
        if not request:
            return {
                "status": "error",
                "error": f"未找到请求: {request_id}"
            }
        
        audit_result = request.get("audit_result", {})
        
        if not audit_result.get("ready_to_send"):
            return {
                "status": "error",
                "error": "该请求未通过审核，无法发送"
            }
        
        reply = audit_result.get("selected_reply")
        
        # 模拟发送
        result = {
            "status": "success",
            "request_id": request_id,
            "reply": reply,
            "contact": request["contact"],
            "sent_at": datetime.now().isoformat(),
            "message": "模拟发送成功(请在真实环境中使用uiautomation发送)"
        }
        
        # 学习这次对话
        self.kb.learn_from_conversation(request["input_message"], reply)
        
        return result
    
    def _save_history(self):
        """保存历史记录"""
        try:
            with open("reply_history.json", 'w', encoding='utf-8') as f:
                json.dump(self.reply_history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def run(self, input_text, contact, knowledge_base_file):
        """执行完整流程"""
        # 使用指定的知识库
        if knowledge_base_file:
            self.kb = KnowledgeBase(knowledge_base_file)
        
        result = {
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
        # 生成候选回复
        candidates = self.generate_candidates(input_text, contact)
        result["candidates"] = candidates
        result["candidate_count"] = len(candidates)
        
        # 创建审核请求
        audit_request = self.create_audit_request(input_text, contact, candidates)
        result["audit_request"] = {
            "id": audit_request["id"],
            "status": audit_request["status"]
        }
        
        # 审核说明
        result["audit_instructions"] = {
            "approve": "批准使用最高置信度回复并发送",
            "modify": "提供修改后的文本发送",
            "reject": "拒绝本次回复",
            "usage": "使用 python scripts/auto_reply.py --action audit --request_id <id> --decision <approve|modify|reject> --modified_text <text>"
        }
        
        # 发送说明
        result["send_instructions"] = {
            "usage": "审核通过后使用 python scripts/auto_reply.py --action send --request_id <id>",
            "note": "实际发送需要微信窗口可见"
        }
        
        return result


def main():
    parser = argparse.ArgumentParser(description='自动回复引擎')
    parser.add_argument('--action', required=True,
                       choices=['generate', 'audit', 'send'],
                       help='操作类型')
    parser.add_argument('--input', help='输入消息(generate)')
    parser.add_argument('--contact', help='联系人(generate)')
    parser.add_argument('--knowledge_base', default='./kb_data.json', 
                       help='知识库文件路径')
    parser.add_argument('--request_id', help='审核请求ID(audit/send)')
    parser.add_argument('--decision', choices=['approve', 'modify', 'reject'],
                       help='审核决策(audit)')
    parser.add_argument('--modified_text', help='修改后的文本(audit modify)')
    
    args = parser.parse_args()
    
    engine = AutoReplyEngine()
    
    result = {"status": "success", "action": args.action}
    
    if args.action == 'generate':
        if not args.input or not args.contact:
            result = {
                "status": "error",
                "error": "generate模式需要 --input 和 --contact 参数"
            }
        else:
            result = engine.run(args.input, args.contact, args.knowledge_base)
    
    elif args.action == 'audit':
        if not args.request_id or not args.decision:
            result = {
                "status": "error",
                "error": "audit模式需要 --request_id 和 --decision 参数"
            }
        else:
            result = engine.process_audit(
                args.request_id, 
                args.decision, 
                args.modified_text
            )
    
    elif args.action == 'send':
        if not args.request_id:
            result = {
                "status": "error",
                "error": "send模式需要 --request_id 参数"
            }
        else:
            result = engine.execute_send(args.request_id)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
