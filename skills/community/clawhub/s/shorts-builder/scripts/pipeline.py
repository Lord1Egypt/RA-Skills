#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情管道主控模块
协调各模块，管理双确认控制流程
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict

# 导入其他模块
from graph_manager import get_graph_manager, GraphManager
from ai_reviewer import get_ai_reviewer, AIReviewer, ReviewResult
from episode_generator import get_episode_generator, EpisodeGenerator


# 状态文件路径
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "pipeline_state.json")

# 注意：人工审核没有最大次数限制，用户可以一直要求修改直到满意


@dataclass
class PipelineState:
    """管道状态"""
    pipeline_id: str
    theme: str
    target_episodes: int
    current_episode: int
    status: str
    created_at: str
    updated_at: str
    style: str = "写实电影感"
    retry_count: int = 0
    ai_review: Optional[Dict] = None
    last_output: Optional[Dict] = None
    error_message: Optional[str] = None


class StoryPipeline:
    """剧情管道控制器"""
    
    def __init__(self):
        """初始化管道控制器"""
        self.graph_manager = get_graph_manager()
        self.ai_reviewer = get_ai_reviewer()
        self.episode_generator = get_episode_generator()
        self.states: Dict[str, PipelineState] = {}
        self._load_states()
    
    def _load_states(self):
        """加载状态文件"""
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for pid, state in data.get("pipelines", {}).items():
                        self.states[pid] = PipelineState(**state)
            except (json.JSONDecodeError, Exception) as e:
                print(f"加载状态文件失败: {e}")
    
    def _save_states(self):
        """保存状态文件"""
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        data = {
            "pipelines": {
                pid: asdict(state) for pid, state in self.states.items()
            }
        }
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_pipeline(
        self,
        theme: str,
        target_episodes: int,
        style: str = "写实电影感"
    ) -> Dict[str, Any]:
        """
        创建新的管道
        
        Args:
            theme: 故事主题
            target_episodes: 目标集数
            style: 风格
            
        Returns:
            创建结果
        """
        # 生成管道ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        pipeline_id = f"pipeline_{timestamp}"
        
        # 创建状态
        state = PipelineState(
            pipeline_id=pipeline_id,
            theme=theme,
            target_episodes=target_episodes,
            current_episode=0,
            status="initialized",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            style=style
        )
        
        self.states[pipeline_id] = state
        self._save_states()
        
        return {
            "success": True,
            "pipeline_id": pipeline_id,
            "message": f"管道创建成功，主题：{theme}，目标：{target_episodes}集"
        }
    
    def start_generation(self, pipeline_id: str) -> Dict[str, Any]:
        """
        开始生成（第一集或继续生成）
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            生成提示词，供LLM使用
        """
        if pipeline_id not in self.states:
            return {"success": False, "error": "管道不存在"}
        
        state = self.states[pipeline_id]
        
        # 更新状态
        state.current_episode += 1
        state.status = "generating"
        state.updated_at = datetime.now().isoformat()
        self._save_states()
        
        if state.current_episode == 1:
            # 生成第一集
            prompt = self.episode_generator.generate_first_episode(
                theme=state.theme,
                target_episodes=state.target_episodes,
                style=state.style
            )
        else:
            # 查询图谱
            graph_result = self.graph_manager.query_graph(
                pipeline_id, 
                state.current_episode - 1
            )
            
            # 获取未闭环钩子
            open_hooks = self.graph_manager.get_open_hooks(pipeline_id)
            
            # 获取上一集内容
            prev_content = ""
            if state.last_output:
                prev_content = state.last_output.get("content", "")
            
            # 判断是否最终集
            if state.current_episode >= state.target_episodes:
                prompt = self.episode_generator.generate_final_episode(
                    episode_number=state.current_episode,
                    prev_content=prev_content,
                    graph_data=graph_result,
                    open_hooks=open_hooks,
                    style=state.style
                )
            else:
                prompt = self.episode_generator.generate_next_episode(
                    episode_number=state.current_episode,
                    prev_content=prev_content,
                    graph_data=graph_result,
                    open_hooks=open_hooks,
                    style=state.style
                )
        
        return {
            "success": True,
            "pipeline_id": pipeline_id,
            "episode": state.current_episode,
            "prompt": prompt
        }
    
    def submit_episode(
        self,
        pipeline_id: str,
        episode: int,
        content: str
    ) -> Dict[str, Any]:
        """
        提交生成的剧集内容，进入AI审核阶段
        
        Args:
            pipeline_id: 管道ID
            episode: 剧集序号
            content: 剧集内容
            
        Returns:
            AI审核提示词
        """
        if pipeline_id not in self.states:
            return {"success": False, "error": "管道不存在"}
        
        state = self.states[pipeline_id]
        
        # 更新状态
        state.status = "ai_reviewing"
        state.updated_at = datetime.now().isoformat()
        self._save_states()
        
        # 获取上一集内容（如果有）
        prev_content = None
        if episode > 1:
            graph_result = self.graph_manager.query_graph(pipeline_id, episode - 1)
            prev_content = graph_result.get("content", "")
        
        # 创建审核提示词
        review_prompt = self.ai_reviewer.create_review_prompt(
            episode_content=content,
            prev_content=prev_content,
            graph_data=None,
            episode_number=episode
        )
        
        return {
            "success": True,
            "pipeline_id": pipeline_id,
            "episode": episode,
            "review_prompt": review_prompt
        }
    
    def process_ai_review(
        self,
        pipeline_id: str,
        episode: int,
        ai_review_result: str,
        generated_content: str
    ) -> Dict[str, Any]:
        """
        处理AI审核结果
        
        注意：AI审核不通过时可以无限重试，没有次数限制
        
        Args:
            pipeline_id: 管道ID
            episode: 剧集序号
            ai_review_result: AI审核结果（JSON字符串）
            generated_content: 生成的剧集内容
            
        Returns:
            处理结果
        """
        if pipeline_id not in self.states:
            return {"success": False, "error": "管道不存在"}
        
        state = self.states[pipeline_id]
        
        # 解析审核结果
        review = self.ai_reviewer.parse_review_result(ai_review_result)
        
        if not review.passed:
            # AI审核未通过，可以无限重试
            state.retry_count += 1
            state.status = "ai_retry_needed"
            self._save_states()
            
            return {
                "success": False,
                "passed": False,
                "retry_count": state.retry_count,
                "review": {
                    "score": review.score,
                    "checks": review.checks,
                    "suggestions": review.suggestions
                },
                "message": f"AI审核未通过（得分{review.score}），需要重新生成（无次数限制）"
            }
        
        # AI审核通过，进入等待人工确认状态
        # 注意：此时还不存储图谱，等人工确认通过后才存储
        state.status = "waiting_user_confirm"
        state.retry_count = 0
        state.ai_review = {
            "score": review.score,
            "checks": review.checks,
            "suggestions": review.suggestions,
            "summary": review.summary
        }
        state.last_output = {
            "episode": episode,
            "content": generated_content,
            "summary": self._extract_summary(generated_content)
        }
        state.updated_at = datetime.now().isoformat()
        self._save_states()
        
        return {
            "success": True,
            "passed": True,
            "status": "waiting_user_confirm",
            "review": {
                "score": review.score,
                "summary": review.summary
            },
            "preview": {
                "episode": episode,
                "summary": state.last_output["summary"],
                "content_preview": generated_content[:500] + "..." if len(generated_content) > 500 else generated_content
            },
            "message": "AI审核通过，等待人工确认"
        }
    
    def user_confirm(
        self,
        pipeline_id: str,
        action: str,
        modification_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理用户确认
        
        Args:
            pipeline_id: 管道ID
            action: 用户操作 (approve/modify/pause/end)
            modification_note: 修改意见（action=modify时需要）
            
        Returns:
            处理结果
        """
        if pipeline_id not in self.states:
            return {"success": False, "error": "管道不存在"}
        
        state = self.states[pipeline_id]
        
        if action == "approve":
            # 用户确认通过，存储图谱
            if state.last_output:
                save_result = self.graph_manager.save_graph(
                    pipeline_id=pipeline_id,
                    episode=state.last_output["episode"],
                    content=state.last_output["content"]
                )
                
                if not save_result.get("success"):
                    return {
                        "success": False,
                        "error": "图谱存储失败",
                        "detail": save_result.get("error")
                    }
            
            # 检查是否完成
            if state.current_episode >= state.target_episodes:
                state.status = "completed"
                state.updated_at = datetime.now().isoformat()
                self._save_states()
                
                return {
                    "success": True,
                    "status": "completed",
                    "message": "剧情管道已完成！所有集数已生成。"
                }
            
            # 准备生成下一集
            state.status = "ready_for_next"
            state.updated_at = datetime.now().isoformat()
            self._save_states()
            
            return {
                "success": True,
                "status": "ready_for_next",
                "next_episode": state.current_episode + 1,
                "message": f"第{state.current_episode}集已确认，准备生成第{state.current_episode + 1}集"
            }
        
        elif action == "modify":
            # 用户要求修改
            state.status = "modification_requested"
            state.error_message = modification_note
            state.retry_count = 0
            state.updated_at = datetime.now().isoformat()
            self._save_states()
            
            return {
                "success": True,
                "status": "modification_requested",
                "message": f"将根据修改意见重新生成：{modification_note}"
            }
        
        elif action == "pause":
            # 用户暂停
            state.status = "paused"
            state.updated_at = datetime.now().isoformat()
            self._save_states()
            
            return {
                "success": True,
                "status": "paused",
                "message": f"管道已暂停，当前进度：第{state.current_episode}集"
            }
        
        elif action == "end":
            # 用户结束
            state.status = "user_ended"
            state.updated_at = datetime.now().isoformat()
            self._save_states()
            
            return {
                "success": True,
                "status": "user_ended",
                "message": f"管道已结束，共生成{state.current_episode}集"
            }
        
        else:
            return {"success": False, "error": f"未知操作：{action}"}
    
    def get_status(self, pipeline_id: str) -> Dict[str, Any]:
        """
        获取管道状态
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            状态信息
        """
        if pipeline_id not in self.states:
            return {"success": False, "error": "管道不存在"}
        
        state = self.states[pipeline_id]
        
        return {
            "success": True,
            "pipeline_id": pipeline_id,
            "theme": state.theme,
            "target_episodes": state.target_episodes,
            "current_episode": state.current_episode,
            "status": state.status,
            "created_at": state.created_at,
            "updated_at": state.updated_at,
            "ai_review": state.ai_review,
            "last_output": state.last_output
        }
    
    def list_pipelines(self) -> Dict[str, Any]:
        """
        列出所有管道
        
        Returns:
            管道列表
        """
        pipelines = []
        for pid, state in self.states.items():
            pipelines.append({
                "pipeline_id": pid,
                "theme": state.theme,
                "current_episode": state.current_episode,
                "target_episodes": state.target_episodes,
                "status": state.status,
                "updated_at": state.updated_at
            })
        
        return {
            "success": True,
            "count": len(pipelines),
            "pipelines": pipelines
        }
    
    def resume_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """
        恢复暂停的管道
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            恢复结果
        """
        if pipeline_id not in self.states:
            return {"success": False, "error": "管道不存在"}
        
        state = self.states[pipeline_id]
        
        if state.status != "paused":
            return {"success": False, "error": f"管道状态不是暂停状态：{state.status}"}
        
        state.status = "ready_for_next"
        state.updated_at = datetime.now().isoformat()
        self._save_states()
        
        return {
            "success": True,
            "message": f"管道已恢复，当前进度：第{state.current_episode}集",
            "next_episode": state.current_episode + 1
        }
    
    def _extract_summary(self, content: str) -> str:
        """从内容中提取摘要"""
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "剧情摘要" in line or "摘要" in line:
                # 获取下一行
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        # 如果没有找到摘要，返回前100字
        return content[:100] + "..." if len(content) > 100 else content


# 单例实例
_pipeline = None

def get_pipeline() -> StoryPipeline:
    """获取管道控制器单例"""
    global _pipeline
    if _pipeline is None:
        _pipeline = StoryPipeline()
    return _pipeline


# 便捷函数
def create_pipeline(theme: str, target_episodes: int, style: str = "写实电影感") -> Dict:
    """创建新管道"""
    return get_pipeline().create_pipeline(theme, target_episodes, style)

def start_generation(pipeline_id: str) -> Dict:
    """开始生成"""
    return get_pipeline().start_generation(pipeline_id)

def submit_episode(pipeline_id: str, episode: int, content: str) -> Dict:
    """提交剧集"""
    return get_pipeline().submit_episode(pipeline_id, episode, content)

def process_ai_review(pipeline_id: str, episode: int, ai_result: str, content: str) -> Dict:
    """处理AI审核"""
    return get_pipeline().process_ai_review(pipeline_id, episode, ai_result, content)

def user_confirm(pipeline_id: str, action: str, note: str = None) -> Dict:
    """用户确认"""
    return get_pipeline().user_confirm(pipeline_id, action, note)

def get_status(pipeline_id: str) -> Dict:
    """获取状态"""
    return get_pipeline().get_status(pipeline_id)

def list_pipelines() -> Dict:
    """列出管道"""
    return get_pipeline().list_pipelines()

def resume_pipeline(pipeline_id: str) -> Dict:
    """恢复管道"""
    return get_pipeline().resume_pipeline(pipeline_id)