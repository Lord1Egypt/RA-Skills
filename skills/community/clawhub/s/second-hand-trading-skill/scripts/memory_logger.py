import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any


class MemoryLogger:
    """
    Log system to help Agent remember interaction history and conversation content
    with other Agents for quick recall upon next startup
    """
    
    def __init__(self, log_file: str = None):
        """
        Initialize memory logging system

        Args:
            log_file: Log file path, stored in JSONL format, defaults to memory folder
        """
        if log_file is None:
            # 获取当前脚本所在的技能目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(current_dir, "..", "memory")
            os.makedirs(log_dir, exist_ok=True)
            self.log_file = os.path.join(log_dir, "agent_memory.jsonl")
        else:
            self.log_file = log_file
        self._ensure_log_dir()
        
    def _ensure_log_dir(self):
        """Ensure log file directory exists"""
        dir_name = os.path.dirname(self.log_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            
    def log_interaction(self, 
                        agent_id: str, 
                        other_agent_id: str, 
                        interaction_type: str, 
                        content: str,
                        topics: Optional[List[str]] = None,
                        keywords: Optional[List[str]] = None,
                        metadata: Optional[Dict[str, Any]] = None):
        """
        记录与其他Agent的交互
        
        Args:
            agent_id: 当前Agent的ID
            other_agent_id: 交互的其他Agent的ID
            interaction_type: 交互类型（send_message, receive_message, broadcast, etc.）
            content: 交互内容
            topics: 话题列表
            keywords: 关键词列表
            metadata: 其他元数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "interaction",
            "agent_id": agent_id,
            "other_agent_id": other_agent_id,
            "interaction_type": interaction_type,
            "content": content,
            "topics": topics or [],
            "keywords": keywords or [],
            "metadata": metadata or {}
        }
        self._write_entry(log_entry)
        
    def log_agent_info(self, agent_id: str, other_agent_id: str, 
                      agent_name: Optional[str] = None, 
                      persona: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      metadata: Optional[Dict[str, Any]] = None):
        """
        记录其他Agent的信息
        
        Args:
            agent_id: 当前Agent的ID
            other_agent_id: 其他Agent的ID
            agent_name: 其他Agent的名称
            persona: 其他Agent的人格描述
            tags: 标签列表
            metadata: 其他元数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_info",
            "agent_id": agent_id,
            "other_agent_id": other_agent_id,
            "agent_name": agent_name,
            "persona": persona,
            "tags": tags or [],
            "metadata": metadata or {}
        }
        self._write_entry(log_entry)
        
    def log_contract(self, agent_id: str, other_agent_id: str, contract_id: str,
                    contract_type: str, terms: str, status: str,
                    metadata: Optional[Dict[str, Any]] = None):
        """
        记录合同信息
        
        Args:
            agent_id: 当前Agent的ID
            other_agent_id: 其他Agent的ID
            contract_id: 合同ID
            contract_type: 合同类型
            terms: 合同条款
            status: 合同状态
            metadata: 其他元数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "contract",
            "agent_id": agent_id,
            "other_agent_id": other_agent_id,
            "contract_id": contract_id,
            "contract_type": contract_type,
            "terms": terms,
            "status": status,
            "metadata": metadata or {}
        }
        self._write_entry(log_entry)
        
    def log_event(self, agent_id: str, event_type: str, 
                 description: str,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        记录重要事件
        
        Args:
            agent_id: 当前Agent的ID
            event_type: 事件类型
            description: 事件描述
            metadata: 其他元数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "event",
            "agent_id": agent_id,
            "event_type": event_type,
            "description": description,
            "metadata": metadata or {}
        }
        self._write_entry(log_entry)
        
    def log_error(self, agent_id: str, error_type: str, 
                 error_message: str,
                 context: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        记录错误信息
        
        Args:
            agent_id: 当前Agent的ID
            error_type: 错误类型
            error_message: 错误信息
            context: 错误上下文
            metadata: 其他元数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "agent_id": agent_id,
            "error_type": error_type,
            "error_message": error_message,
            "context": context,
            "metadata": metadata or {}
        }
        self._write_entry(log_entry)
        
    def _write_entry(self, entry: Dict[str, Any]):
        """
        Write log entry

        Args:
            entry: Log entry dictionary
        """
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Failed to write memory log: {e}")
            
    def clear_memory(self, agent_id: str = None, clear_all: bool = False):
        """
        Clear memory

        Args:
            agent_id: Agent ID for which to clear memory. If None and clear_all=True, all memory will be cleared
            clear_all: Whether to clear all memory
        """
        if os.path.exists(self.log_file):
            if clear_all:
                # Clear all memory
                open(self.log_file, 'w', encoding='utf-8').close()
            elif agent_id:
                # Only clear memory for specific Agent
                new_entries = []
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("agent_id") != agent_id:
                                new_entries.append(entry)
                        except Exception:
                            continue

                with open(self.log_file, 'w', encoding='utf-8') as f:
                    for entry in new_entries:
                        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        
    def get_memory(self, agent_id: str,
                  other_agent_id: Optional[str] = None,
                  interaction_type: Optional[str] = None,
                  time_limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Read memory log

        Args:
            agent_id: Current Agent's ID
            other_agent_id: Optional, other Agent's ID for filtering
            interaction_type: Optional, interaction type for filtering
            time_limit: Optional, time limit in hours, only return memory from specified time period

        Returns:
            List of memories
        """
        memories = []
        
        if not os.path.exists(self.log_file):
            return memories
            
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            if entry.get("agent_id") == agent_id:
                                # Check other filters
                                if other_agent_id and entry.get("other_agent_id") != other_agent_id:
                                    continue

                                if interaction_type and "interaction_type" in entry and \
                                   entry.get("interaction_type") != interaction_type:
                                    continue

                                # Check time limit
                                if time_limit:
                                    entry_time = datetime.fromisoformat(entry.get("timestamp"))
                                    time_diff = datetime.now() - entry_time
                                    if time_diff.total_seconds() > time_limit * 3600:
                                        continue

                                memories.append(entry)
                        except json.JSONDecodeError:
                            continue

            # Sort by time
            memories.sort(key=lambda x: x.get("timestamp"))

        except Exception as e:
            print(f"Failed to read memory log: {e}")
            
        return memories
        
    def get_agent_summary(self, agent_id: str, other_agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get interaction summary with specific Agent

        Args:
            agent_id: Current Agent's ID
            other_agent_id: Other Agent's ID

        Returns:
            Dictionary with interaction summary
        """
        memories = self.get_memory(agent_id, other_agent_id)
        
        if not memories:
            return None
            
        # 计算交互统计
        total_interactions = len(memories)
        interaction_types = {}
        topics = set()
        keywords = set()
        last_interaction = None
        
        for memory in memories:
            # 统计交互类型
            if "interaction_type" in memory:
                itype = memory.get("interaction_type")
                interaction_types[itype] = interaction_types.get(itype, 0) + 1
                
            # 收集话题和关键词
            if memory.get("topics"):
                for topic in memory.get("topics", []):
                    topics.add(topic)
                    
            if memory.get("keywords"):
                for keyword in memory.get("keywords", []):
                    keywords.add(keyword)
                    
            # 记录最后一次交互
            if last_interaction is None or memory.get("timestamp") > last_interaction.get("timestamp"):
                last_interaction = memory
                
        # 查找Agent信息
        agent_info = next((m for m in memories if m.get("type") == "agent_info"), None)
        
        # 构建返回结果
        result = {
            "other_agent_id": other_agent_id,
            "agent_name": agent_info.get("agent_name") if agent_info else None,
            "persona": agent_info.get("persona") if agent_info else None,
            "total_interactions": total_interactions,
            "interaction_types": interaction_types,
            "topics": list(topics),
            "keywords": list(keywords),
            "last_interaction": last_interaction
        }
        
        # 为cyber-friending-skill添加tags字段（如果存在）
        if agent_info and "tags" in agent_info:
            result["tags"] = agent_info.get("tags", [])
            
        return result
        
    def get_all_agents(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get list of all other Agents that have interacted with current Agent

        Args:
            agent_id: Current Agent's ID

        Returns:
            List of Agents with summary information
        """
        memories = self.get_memory(agent_id)
        
        if not memories:
            return []
            
        # 收集所有交互过的Agent
        other_agent_ids = set()
        for memory in memories:
            if "other_agent_id" in memory and memory.get("other_agent_id"):
                other_agent_ids.add(memory.get("other_agent_id"))
                
        # 为每个Agent获取摘要
        agents = []
        for other_agent_id in other_agent_ids:
            summary = self.get_agent_summary(agent_id, other_agent_id)
            if summary:
                agents.append(summary)
                
        # 按交互次数排序
        agents.sort(key=lambda x: x.get("total_interactions", 0), reverse=True)
        
        return agents
