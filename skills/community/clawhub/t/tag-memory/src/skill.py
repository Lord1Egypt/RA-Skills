#!/usr/bin/env python3
"""
TagMemory - OpenClaw Skill 核心实现
标签化长期记忆系统 v1.0
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from database import MemoryDatabase, Memory, bm25_search
from verifier import MemoryVerifier
from summarizer import MemorySummarizer, SummaryDraft


class TagMemorySkill:
    """TagMemory OpenClaw Skill 主类"""
    
    def __init__(self):
        self.db = MemoryDatabase()
        self.config = self._load_config()
        self.verifier = MemoryVerifier(self.db)
        self.summarizer = MemorySummarizer(self.db)
        
        # 默认标签
        self.default_tags = [
            "#偏好", "#决定", "#项目", "#人", "#事件", "#知识", "#错误"
        ]
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}
    
    # ==================== 核心功能 ====================
    
    def memory_store(self, content: str, tags: List[str] = None,
                     time_label: str = None, source: str = "dialogue",
                     agent_id: str = "main") -> Dict:
        """
        存储记忆
        
        Args:
            content: 记忆内容
            tags: 标签列表
            time_label: 时间标签 (YYYY-MM)
            source: 来源 (dialogue/summary/manual)
            agent_id: 哪个 agent 产生的（默认 main）
        
        Returns:
            {"success": True, "id": "xxx", "message": "..."}
        """
        try:
            # 处理标签
            if tags is None:
                tags = []
            if not isinstance(tags, list):
                tags = [tags]
            
            # 验证标签有效性
            valid_tags = []
            for tag in tags:
                if not tag.startswith("#"):
                    tag = "#" + tag
                # 检查是否在默认标签中或自定义标签
                valid_tags.append(tag)
            
            # 时间标签
            if not time_label:
                time_label = datetime.now().strftime("%Y-%m")
            
            # 创建记忆
            memory = Memory(
                id="",  # uuid 自动生成
                content=content,
                tags=valid_tags,
                time_label=time_label,
                source=source,
                agent_id=agent_id
            )
            
            # 存储
            memory_id = self.db.insert(memory)
            
            return {
                "success": True,
                "id": memory_id,
                "message": f"✅ 记忆已存储\n📝 内容: {content[:100]}{'...' if len(content) > 100 else ''}\n🏷️ 标签: {', '.join(valid_tags)}\n📅 时间: {time_label}\n🤖 来源: {agent_id}"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_query(self, query: str, tags: List[str] = None,
                     time_range: tuple = None, limit: int = 5) -> Dict:
        """
        查询记忆（BM25 搜索）
        
        Returns:
            {
                "success": True,
                "results": [{"id": "xxx", "content": "...", "tags": [...], "score": 8.5}],
                "total": 10
            }
        """
        try:
            if not query and not tags:
                return {"success": False, "error": "查询条件和标签不能同时为空"}
            
            # 如果没有查询文本但有标签，只用标签过滤
            if not query and tags:
                memories = self.db.get_all(limit=limit, tags=tags)
                results = [{
                    "id": m.id,
                    "content": m.content,
                    "summary": m.summary,
                    "tags": m.tags,
                    "time_label": m.time_label,
                    "created_at": m.created_at,
                    "verified": m.verified,
                    "agent_id": m.agent_id,
                    "score": 1.0  # 无查询时默认分数
                } for m in memories]
            else:
                # BM25 搜索
                search_results = bm25_search(self.db, query, tags, time_range, limit)
                results = [{
                    "id": m.id,
                    "content": m.content,
                    "summary": m.summary,
                    "tags": m.tags,
                    "time_label": m.time_label,
                    "created_at": m.created_at,
                    "verified": m.verified,
                    "agent_id": m.agent_id,
                    "score": round(score, 2)
                } for m, score in search_results]
            
            total = len(results)
            
            # 构建返回消息
            if not results:
                message = "🔍 没有找到相关记忆"
            else:
                lines = ["🔍 查询结果:\n"]
                for i, r in enumerate(results, 1):
                    verified_icon = "✅" if r["verified"] else "❓"
                    lines.append(f"{i}. {verified_icon} [{r['score']}分] {r['content'][:80]}{'...' if len(r['content']) > 80 else ''}")
                    lines.append(f"   🏷️ {', '.join(r['tags'])} | 📅 {r['time_label']} | 🤖 {r.get('agent_id', 'main')}")
                message = "\n".join(lines)
            
            return {
                "success": True,
                "results": results,
                "total": total,
                "message": message
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_verify(self, memory_id: str, action: str,
                     correction: str = None) -> Dict:
        """
        核对/修正/删除记忆
        
        Args:
            memory_id: 记忆 ID
            action: confirm/correct/delete
            correction: 修正内容 (action=correct 时必填)
        
        Returns:
            {"success": True, "message": "..."}
        """
        try:
            memory = self.db.get(memory_id)
            if not memory:
                return {"success": False, "error": "记忆不存在"}
            
            if action == "confirm":
                self.db.update(memory_id, {
                    "verified": True,
                    "verified_at": datetime.now().isoformat()
                })
                return {
                    "success": True,
                    "message": f"✅ 已确认记忆: {memory.content[:50]}..."
                }
            
            elif action == "correct":
                if not correction:
                    return {"success": False, "error": "修正内容不能为空"}
                self.db.update(memory_id, {
                    "content": correction,
                    "verified": False,
                    "updated_at": datetime.now().isoformat()
                })
                return {
                    "success": True,
                    "message": f"✏️ 已修正记忆: {correction[:50]}..."
                }
            
            elif action == "delete":
                self.db.delete(memory_id)
                return {
                    "success": True,
                    "message": f"🗑️ 已删除记忆"
                }
            
            else:
                return {"success": False, "error": f"未知操作: {action}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_list(self, tags: List[str] = None,
                    verified_only: bool = False,
                    page: int = 1, page_size: int = 20) -> Dict:
        """
        列出记忆
        """
        try:
            offset = (page - 1) * page_size
            memories = self.db.get_all(
                limit=page_size,
                offset=offset,
                verified_only=verified_only,
                tags=tags
            )
            
            total = self.db.count(verified_only=verified_only, tags=tags)
            
            results = [{
                "id": m.id,
                "content": m.content,
                "summary": m.summary,
                "tags": m.tags,
                "time_label": m.time_label,
                "created_at": m.created_at,
                "verified": m.verified,
                "agent_id": m.agent_id
            } for m in memories]
            
            return {
                "success": True,
                "results": results,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_summary_request(self, period: str = None) -> Dict:
        """
        请求生成阶段性总结
        """
        try:
            if not period:
                period = datetime.now().strftime("%Y-%m")
            
            # 获取本月记忆
            results = self.memory_query("", time_range=(period + "-01", period + "-31"), limit=50)
            
            if results["total"] == 0:
                return {
                    "success": True,
                    "need_summary": False,
                    "message": f"📅 {period} 暂无记忆，无需总结"
                }
            
            # 标记需要总结
            return {
                "success": True,
                "need_summary": True,
                "period": period,
                "count": results["total"],
                "message": f"📊 {period} 共有 {results['total']} 条记忆，可以生成总结"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== 闲时核对 ====================
    
    def memory_verify_get_pending(self, max_count: int = 3) -> Dict:
        """
        获取待核对的记忆列表
        """
        try:
            pending = self.verifier.get_pending_verifications(max_count=max_count)
            
            if not pending:
                return {
                    "success": True,
                    "has_pending": False,
                    "message": "✅ 暂无待核对的记忆"
                }
            
            lines = ["❓ **待核对记忆**\n"]
            for i, p in enumerate(pending, 1):
                lines.append(f"\n**{i}.** {p['question']}")
                lines.append(f"   📝 {p['content'][:60]}...")
            
            lines.append("\n\n回复格式：")
            lines.append("- 「确认」- 确认第 1 条")
            lines.append("- 「确认2」「确认3」- 确认其他条")
            lines.append("- 「修正1: 正确内容」- 修正内容")
            lines.append("- 「删除1」- 删除")
            
            return {
                "success": True,
                "has_pending": True,
                "pending": pending,
                "message": "\n".join(lines)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_verify_result(self, index: int, action: str, 
                            correction: str = None) -> Dict:
        """
        处理核对结果
        
        Args:
            index: 记忆索引 (1-based)
            action: confirm / correct / delete
            correction: 修正内容
        """
        try:
            # 获取待核对列表
            pending = self.verifier.get_pending_verifications(max_count=10)
            
            if not pending or index < 1 or index > len(pending):
                return {"success": False, "error": "无效的索引"}
            
            memory_id = pending[index - 1]["memory_id"]
            
            # 记录结果
            result = self.verifier.record_verification_result(
                memory_id, action, correction
            )
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_verify_periodic(self) -> Dict:
        """
        执行周期性审核
        """
        try:
            return self.verifier.periodic_audit()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== 定期归纳 ====================
    
    def memory_summarize(self, days: int = 7) -> Dict:
        """
        生成阶段性总结
        """
        try:
            summary = self.summarizer.generate_summary_draft(days=days)
            
            # 保存草稿
            draft_path = self.summarizer.save_draft(summary)
            
            return {
                "success": True,
                "has_content": any([
                    summary.decisions,
                    summary.preferences,
                    summary.projects,
                    summary.learned,
                    summary.events,
                    summary.issues
                ]),
                "draft_path": draft_path,
                "summary": summary.to_dict(),
                "message": summary.format_for_display()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_summarize_confirm(self, feedback: str = "confirm") -> Dict:
        """
        确认总结并存档
        """
        try:
            summary = self.summarizer.load_draft()
            
            if not summary:
                return {"success": False, "error": "没有待确认的总结"}
            
            # 解析反馈
            parse_result = self.summarizer.parse_user_feedback(feedback, summary)
            
            if parse_result["action"] == "cancel":
                self.summarizer.clear_draft()
                return {"success": True, "message": parse_result["message"]}
            
            if parse_result["action"] == "confirm":
                # 存档
                archived = self.summarizer.archive_summary(summary)
                self.summarizer.clear_draft()
                return {
                    "success": True,
                    "archived_count": len(archived),
                    "message": f"✅ 总结已存档，共 {len(archived)} 条记忆"
                }
            
            # 如果是修改，反馈给用户
            return {
                "success": True,
                "action": "correct",
                "feedback_required": True,
                "message": f"✏️ 你说：{feedback}\n请告诉我应该怎么修改具体的某一条。"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def memory_summarize_specific(self, period: str = None) -> Dict:
        """
        生成指定时间段的总结
        """
        try:
            if not period:
                return self.memory_summarize(days=7)
            
            # 解析时间段
            if "~" in period:
                start, end = [s.strip() for s in period.split("~")]
                # 计算天数
                from datetime import datetime as dt
                start_dt = dt.strptime(start, "%Y-%m-%d")
                end_dt = dt.strptime(end, "%Y-%m-%d")
                days = (end_dt - start_dt).days
                
                memories = self.summarizer.get_memories_for_period(start, end)
                summary = self.summarizer.analyze_memories(memories)
            else:
                # 认为是月份
                summary = self.summarizer.generate_summary_draft(days=30)
                summary.period = period
            
            # 保存草稿
            draft_path = self.summarizer.save_draft(summary)
            
            return {
                "success": True,
                "draft_path": draft_path,
                "summary": summary.to_dict(),
                "message": summary.format_for_display()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== 辅助功能 ====================
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = self.db.count()
        verified = self.db.count(verified_only=True)
        unverified = total - verified
        
        return {
            "success": True,
            "stats": {
                "total": total,
                "verified": verified,
                "unverified": unverified,
                "verified_rate": f"{verified/total*100:.1f}%" if total > 0 else "0%"
            }
        }
    
    def get_tags(self) -> List[str]:
        """获取所有使用过的标签"""
        memories = self.db.get_all(limit=1000)
        tags_set = set()
        for m in memories:
            tags_set.update(m.tags)
        return sorted(list(tags_set))


# ==================== OpenClaw 工具入口 ====================

def handle_tool_call(tool_name: str, arguments: Dict) -> Dict:
    """处理 OpenClaw 工具调用"""
    skill = TagMemorySkill()
    
    if tool_name == "memory_store":
        return skill.memory_store(**arguments)
    
    elif tool_name == "memory_query":
        return skill.memory_query(**arguments)
    
    elif tool_name == "memory_verify":
        return skill.memory_verify(**arguments)
    
    elif tool_name == "memory_list":
        return skill.memory_list(**arguments)
    
    elif tool_name == "memory_summary_request":
        return skill.memory_summary_request(**arguments)
    
    # 闲时核对工具
    elif tool_name == "memory_verify_get_pending":
        return skill.memory_verify_get_pending(**arguments)
    
    elif tool_name == "memory_verify_result":
        return skill.memory_verify_result(**arguments)
    
    elif tool_name == "memory_verify_periodic":
        return skill.memory_verify_periodic()
    
    # 定期归纳工具
    elif tool_name == "memory_summarize":
        return skill.memory_summarize(**arguments)
    
    elif tool_name == "memory_summarize_confirm":
        return skill.memory_summarize_confirm(**arguments)
    
    elif tool_name == "memory_summarize_specific":
        return skill.memory_summarize_specific(**arguments)
    
    else:
        return {"success": False, "error": f"未知工具: {tool_name}"}


# ==================== CLI 入口 ====================

if __name__ == "__main__":
    skill = TagMemorySkill()
    
    if len(sys.argv) < 2:
        print("TagMemory CLI")
        print("用法:")
        print("  python skill.py store <content> [tags...]")
        print("  python skill.py query <query>")
        print("  python skill.py list")
        print("  python skill.py stats")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "store":
        content = sys.argv[2] if len(sys.argv) > 2 else ""
        tags = sys.argv[3:] if len(sys.argv) > 3 else []
        result = skill.memory_store(content, tags)
        print(result["message"])
    
    elif cmd == "query":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        result = skill.memory_query(query)
        print(result["message"])
    
    elif cmd == "list":
        result = skill.memory_list()
        print(f"📋 共 {result['total']} 条记忆:")
        for r in result["results"]:
            print(f"  - [{r['id'][:8]}] {r['content'][:50]}...")
    
    elif cmd == "stats":
        result = skill.get_stats()
        s = result["stats"]
        print(f"📊 记忆统计:")
        print(f"  总数: {s['total']}")
        print(f"  已确认: {s['verified']} ({s['verified_rate']})")
        print(f"  待确认: {s['unverified']}")
    
    else:
        print(f"未知命令: {cmd}")
