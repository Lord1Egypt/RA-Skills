#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Analyzer for OpenClaw
分析技能使用频率、技能组合、相似技能、删除/保留建议
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Set
from collections import Counter, defaultdict
import re

try:
    from langchain_chroma import Chroma
    import chromadb
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    sys.exit(1)


class SkillAnalyzer:
    """技能分析器"""
    
    def __init__(self, workspace_dir: str, chroma_dir: str, collection_name: str = "openclaw_skills"):
        self.workspace_dir = Path(workspace_dir)
        self.chroma_dir = Path(chroma_dir)
        self.collection_name = collection_name
        
        # 加载向量存储
        self.vectorstore = self._load_vectorstore()
        
        # 技能元数据
        self.skills_metadata = self._load_metadata()
        
        # 会话历史缓存
        self.session_history = None
        
    def _load_vectorstore(self):
        """加载向量存储"""
        try:
            from skill_indexer import AliyunEmbeddings
            
            client = chromadb.PersistentClient(path=str(self.chroma_dir))
            embeddings = AliyunEmbeddings()
            
            vectorstore = Chroma(
                client=client,
                collection_name=self.collection_name,
                embedding_function=embeddings
            )
            
            print(f"[INFO] Loaded vectorstore: {self.collection_name}")
            return vectorstore
            
        except Exception as e:
            print(f"[ERROR] Failed to load vectorstore: {e}")
            return None
    
    def _load_metadata(self) -> Dict:
        """加载技能元数据"""
        metadata_file = self.chroma_dir / "skills_metadata.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {}
    
    def _load_session_history(self) -> List[Dict]:
        """加载会话历史（从 sessions 目录）"""
        if self.session_history is not None:
            return self.session_history
        
        sessions_dir = self.workspace_dir / ".openclaw" / "sessions"
        history = []
        
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.json"):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                    
                    # 提取消息中的工具调用
                    if "messages" in session_data:
                        for msg in session_data["messages"]:
                            if "tool_calls" in msg:
                                for tool_call in msg["tool_calls"]:
                                    history.append({
                                        "timestamp": msg.get("timestamp", ""),
                                        "session": session_file.stem,
                                        "tool": tool_call.get("function", {}).get("name", ""),
                                        "message_id": msg.get("id", "")
                                    })
                except Exception as e:
                    print(f"[WARN] Failed to load session {session_file}: {e}")
        
        # 也从 memory 中的会话记录提取
        memory_dir = self.workspace_dir / "memory"
        if memory_dir.exists():
            for md_file in memory_dir.glob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 简单的工具调用模式匹配
                    tool_pattern = r'tool_calls?:\s*\[([^\]]+)\]'
                    matches = re.findall(tool_pattern, content)
                    
                    for match in matches:
                        history.append({
                            "timestamp": md_file.stem,
                            "session": md_file.stem,
                            "tool": match.strip(),
                            "source": "memory"
                        })
                except Exception as e:
                    print(f"[WARN] Failed to parse memory {md_file}: {e}")
        
        self.session_history = history
        print(f"[INFO] Loaded {len(history)} tool usage records")
        return history
    
    def get_skill_usage_frequency(self) -> Dict[str, Dict]:
        """
        获取每个技能的使用频率
        
        Returns:
            {skill_name: {count: int, last_used: str, first_used: str, frequency: str}}
        """
        history = self._load_session_history()
        
        # 统计每个技能的使用次数
        skill_counts = Counter()
        skill_timestamps = defaultdict(list)
        
        for record in history:
            tool_name = record.get("tool", "")
            timestamp = record.get("timestamp", "")
            
            # 提取技能名称（从工具名推断）
            skill_name = self._extract_skill_name(tool_name)
            
            if skill_name:
                skill_counts[skill_name] += 1
                if timestamp:
                    skill_timestamps[skill_name].append(timestamp)
        
        # 构建结果
        result = {}
        all_skills = self._get_all_skills()
        
        for skill in all_skills:
            count = skill_counts.get(skill, 0)
            timestamps = sorted(skill_timestamps.get(skill, []))
            
            last_used = timestamps[-1] if timestamps else "从未使用"
            first_used = timestamps[0] if timestamps else "未知"
            
            # 计算频率描述
            if count == 0:
                frequency = "未使用"
            elif count < 5:
                frequency = "低频"
            elif count < 20:
                frequency = "中频"
            else:
                frequency = "高频"
            
            result[skill] = {
                "count": count,
                "last_used": last_used,
                "first_used": first_used,
                "frequency": frequency
            }
        
        return result
    
    def _extract_skill_name(self, tool_name: str) -> str:
        """从工具名提取技能名"""
        if not tool_name:
            return ""
        
        # 常见技能前缀映射
        skill_prefixes = {
            "feishu": "feishu",
            "message": "message",
            "tts": "tts",
            "browser": "browser",
            "web_search": "web_search",
            "memory": "memory",
            "sessions": "sessions",
            "subagents": "subagents"
        }
        
        tool_lower = tool_name.lower()
        
        for prefix, skill in skill_prefixes.items():
            if prefix in tool_lower:
                return skill
        
        # 尝试从工具名直接推断
        if tool_lower:
            return tool_lower.split("_")[0]
        
        return ""
    
    def _get_all_skills(self) -> List[str]:
        """获取所有技能列表"""
        if self.skills_metadata and "skills" in self.skills_metadata:
            return self.skills_metadata["skills"]
        
        # 从 skills 目录扫描
        skills_dir = self.workspace_dir / "skills"
        if skills_dir.exists():
            return list(set([
                d.name for d in skills_dir.iterdir() 
                if d.is_dir() and not d.name.startswith(".")
            ]))
        
        return []
    
    def get_skill_combinations(self, min_co_occurrence: int = 2) -> Dict[str, List[Tuple[str, int]]]:
        """
        获取技能组合（经常配套使用的技能）
        
        Args:
            min_co_occurrence: 最小共现次数
        
        Returns:
            {skill_name: [(co_occurring_skill, count), ...]}
        """
        history = self._load_session_history()
        
        # 按会话分组
        session_skills = defaultdict(set)
        
        for record in history:
            session = record.get("session", "")
            tool_name = record.get("tool", "")
            skill_name = self._extract_skill_name(tool_name)
            
            if skill_name and session:
                session_skills[session].add(skill_name)
        
        # 统计共现
        co_occurrence = defaultdict(Counter)
        
        for session, skills in session_skills.items():
            skills_list = list(skills)
            for i, skill1 in enumerate(skills_list):
                for skill2 in skills_list[i+1:]:
                    co_occurrence[skill1][skill2] += 1
                    co_occurrence[skill2][skill1] += 1
        
        # 过滤低频组合
        result = {}
        for skill, combinations in co_occurrence.items():
            filtered = [
                (other, count) 
                for other, count in combinations.items() 
                if count >= min_co_occurrence
            ]
            if filtered:
                result[skill] = sorted(filtered, key=lambda x: x[1], reverse=True)
        
        return result
    
    def get_similar_skills(self, skill_name: str, top_k: int = 5) -> List[Dict]:
        """
        获取与指定技能相似的其他技能
        
        Args:
            skill_name: 技能名称
            top_k: 返回数量
        
        Returns:
            [{skill_name, similarity, description}, ...]
        """
        if not self.vectorstore:
            return []
        
        # 获取技能的文档内容
        skill_docs = self._get_skill_documents(skill_name)
        
        if not skill_docs:
            return []
        
        # 合并文档内容作为查询
        query_text = " ".join([doc.page_content[:500] for doc in skill_docs[:3]])
        
        # 向量搜索
        try:
            results = self.vectorstore.similarity_search_with_score(query_text, k=top_k + 5)
            
            similar = []
            for doc, score in results:
                doc_skill = doc.metadata.get("skill_name", "")
                
                # 排除自己
                if doc_skill == skill_name:
                    continue
                
                similarity = 1 - score
                
                # 去重
                if not any(s["skill_name"] == doc_skill for s in similar):
                    similar.append({
                        "skill_name": doc_skill,
                        "similarity": round(similarity, 3),
                        "description": doc.page_content[:200] + "..."
                    })
                
                if len(similar) >= top_k:
                    break
            
            return sorted(similar, key=lambda x: x["similarity"], reverse=True)
            
        except Exception as e:
            print(f"[ERROR] Failed to find similar skills: {e}")
            return []
    
    def _get_skill_documents(self, skill_name: str) -> List:
        """获取指定技能的所有文档"""
        if not self.vectorstore:
            return []
        
        try:
            # 使用元数据过滤
            collection = self.vectorstore._client.get_collection(self.collection_name)
            
            # 获取所有包含该技能的块
            results = collection.get(
                where={"skill_name": skill_name},
                include=["documents", "metadatas"]
            )
            
            from langchain_core.documents import Document
            
            docs = []
            if results and results["documents"]:
                for i, content in enumerate(results["documents"]):
                    metadata = results["metadatas"][i] if results["metadatas"] else {}
                    docs.append(Document(page_content=content, metadata=metadata))
            
            return docs
            
        except Exception as e:
            print(f"[ERROR] Failed to get skill documents: {e}")
            return []
    
    def get_deletion_recommendation(self, skill_name: str) -> Dict:
        """
        获取技能删除/保留建议
        
        Args:
            skill_name: 技能名称
        
        Returns:
            {recommendation: str, reasons: [], confidence: float}
        """
        usage = self.get_skill_usage_frequency()
        combinations = self.get_skill_combinations()
        similar = self.get_similar_skills(skill_name)
        
        skill_usage = usage.get(skill_name, {})
        count = skill_usage.get("count", 0)
        frequency = skill_usage.get("frequency", "未知")
        last_used = skill_usage.get("last_used", "未知")
        
        # 决策逻辑
        reasons = []
        score = 50  # 基础分
        
        # 使用频率评分
        if count == 0:
            score -= 30
            reasons.append("从未使用过")
        elif count < 5:
            score -= 15
            reasons.append(f"使用频率低（{count}次）")
        elif count > 20:
            score += 20
            reasons.append(f"使用频率高（{count}次）")
        
        # 最后使用时间评分
        if last_used != "从未使用":
            try:
                last_date = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
                days_ago = (datetime.now() - last_date).days
                
                if days_ago > 90:
                    score -= 20
                    reasons.append(f"超过 3 个月未使用")
                elif days_ago > 30:
                    score -= 10
                    reasons.append(f"超过 1 个月未使用")
                elif days_ago < 7:
                    score += 15
                    reasons.append(f"最近 7 天内使用过")
            except:
                pass
        
        # 技能组合评分
        if skill_name in combinations:
            combo_count = len(combinations[skill_name])
            if combo_count > 3:
                score += 15
                reasons.append(f"经常与其他技能配合使用（{combo_count}个组合）")
            elif combo_count > 0:
                score += 5
                reasons.append(f"有{combo_count}个常用技能组合")
        else:
            score -= 5
            reasons.append("没有常用的技能组合")
        
        # 相似技能评分（如果有高度相似的，可能冗余）
        high_similarity = [s for s in similar if s["similarity"] > 0.8]
        if high_similarity:
            score -= 10
            reasons.append(f"存在{len(high_similarity)}个高度相似技能（可能冗余）")
        
        # 生成建议
        if score >= 70:
            recommendation = "保留"
            confidence = 0.8
        elif score >= 50:
            recommendation = "观察"
            confidence = 0.6
        elif score >= 30:
            recommendation = "考虑删除"
            confidence = 0.7
        else:
            recommendation = "建议删除"
            confidence = 0.9
        
        return {
            "recommendation": recommendation,
            "reasons": reasons,
            "confidence": confidence,
            "score": score
        }
    
    def generate_full_report(self) -> Dict:
        """生成完整分析报告"""
        print("\n" + "=" * 60)
        print("OpenClaw Skill Analysis Report")
        print("=" * 60)
        
        usage = self.get_skill_usage_frequency()
        combinations = self.get_skill_combinations()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_skills": len(usage),
            "usage_statistics": usage,
            "skill_combinations": combinations,
            "recommendations": {}
        }
        
        # 为每个技能生成建议
        for skill_name in usage.keys():
            report["recommendations"][skill_name] = self.get_deletion_recommendation(skill_name)
        
        # 打印摘要
        print(f"\n[INFO] Total skills analyzed: {len(usage)}")
        
        high_freq = [s for s, u in usage.items() if u["frequency"] == "高频"]
        low_freq = [s for s, u in usage.items() if u["frequency"] == "低频" or u["frequency"] == "未使用"]
        delete_recommended = [s for s, r in report["recommendations"].items() if r["recommendation"] in ["建议删除", "考虑删除"]]
        
        print(f"[INFO] High frequency skills: {len(high_freq)}")
        print(f"[INFO] Low/No usage skills: {len(low_freq)}")
        print(f"[INFO] Recommended for deletion: {len(delete_recommended)}")
        
        print("\n" + "=" * 60)
        
        return report


def main():
    """主函数"""
    workspace_dir = Path(r"C:\Users\Xiabi\.openclaw\workspace")
    chroma_dir = Path(r"C:\Users\Xiabi\.openclaw\workspace\chroma_db")
    
    # 创建分析器
    analyzer = SkillAnalyzer(str(workspace_dir), str(chroma_dir))
    
    # 生成报告
    report = analyzer.generate_full_report()
    
    # 保存报告
    report_file = workspace_dir / "skill_analysis_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[INFO] Report saved to: {report_file}")
    
    # 打印详细结果
    print("\n" + "=" * 60)
    print("技能使用频率 Top 10:")
    print("=" * 60)
    
    usage = report["usage_statistics"]
    sorted_usage = sorted(usage.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
    
    for i, (skill, data) in enumerate(sorted_usage, 1):
        print(f"{i:2d}. {skill:30s} - {data['count']:4d}次 ({data['frequency']}) [最后：{data['last_used'][:10]}]")
    
    print("\n" + "=" * 60)
    print("建议删除的技能:")
    print("=" * 60)
    
    delete_skills = [
        (skill, rec) 
        for skill, rec in report["recommendations"].items() 
        if rec["recommendation"] in ["建议删除", "考虑删除"]
    ]
    
    for skill, rec in delete_skills[:10]:
        print(f"  ❌ {skill:30s} - {rec['recommendation']} ({rec['score']}分)")
        for reason in rec["reasons"][:3]:
            print(f"     • {reason}")
    
    print("\n" + "=" * 60)
    print("技能组合示例:")
    print("=" * 60)
    
    combinations = report["skill_combinations"]
    for skill, combos in list(combinations.items())[:5]:
        print(f"  {skill}:")
        for other, count in combos[:3]:
            print(f"    + {other} ({count}次)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
