from typing import Dict, Any, Optional, List
from llama_index.core.tools import BaseTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import LLM

from src.core.temporal_analyzer import TemporalAnalyzer
from src.core.progress_estimator import ProgressEstimator
from src.core.anomaly_detector import AnomalyDetector
from src.core.social_temporal import SocialTemporal
from src.core.causal_predictor import CausalPredictor
from src.core.time_anchor import TimeAnchorInjector

class TemporalAgentTool(BaseTool):
    """LlamaIndex时序感知工具
    """
    
    def __init__(self):
        super().__init__()
        # 使用集成了所有功能的TemporalAnalyzer
        self.temporal_analyzer = TemporalAnalyzer()
    
    @property
    def metadata(self) -> ToolMetadata:
        """工具元数据
        """
        return ToolMetadata(
            name="temporal_agent",
            description="时序感知工具，用于处理时间相关的任务，包括进度预估、异常检测、社交时序理解等",
            parameters={
                "task_type": {
                    "type": "string",
                    "description": "任务类型: start_timer, stop_timer, predict_duration, start_task, update_progress, detect_anomaly, record_utterance, should_respond, predict_latency"
                },
                "task_id": {
                    "type": "string",
                    "description": "任务ID"
                },
                "task_type": {
                    "type": "string",
                    "description": "任务类型"
                },
                "complexity": {
                    "type": "number",
                    "description": "复杂度因子"
                },
                "total_steps": {
                    "type": "integer",
                    "description": "总步骤数"
                },
                "current_step": {
                    "type": "integer",
                    "description": "当前步骤"
                },
                "event_type": {
                    "type": "string",
                    "description": "事件类型"
                },
                "duration": {
                    "type": "number",
                    "description": "持续时间"
                },
                "speaker": {
                    "type": "string",
                    "description": "说话者"
                },
                "content": {
                    "type": "string",
                    "description": "内容"
                },
                "action": {
                    "type": "string",
                    "description": "动作"
                },
                "timezone": {
                    "type": "string",
                    "description": "时区"
                },
                "prompt": {
                    "type": "string",
                    "description": "提示词"
                }
            }
        )
    
    def _run(self, task_type: str, **kwargs) -> Dict[str, Any]:
        """运行时序感知工具
        
        Args:
            task_type: 任务类型
            **kwargs: 额外参数
            
        Returns:
            结果
        """
        if task_type == "start_timer":
            task_id = kwargs.get("task_id", f"task_{id(self)}")
            task_type = kwargs.get("task_type", "general")
            expected_duration = kwargs.get("expected_duration", 60.0)
            dependencies = kwargs.get("dependencies")
            start_time = self.temporal_analyzer.start_timer(task_id, task_type, expected_duration, dependencies)
            return {"task_id": task_id, "start_time": start_time}
        
        elif task_type == "stop_timer":
            task_id = kwargs.get("task_id")
            duration = self.temporal_analyzer.stop_timer(task_id)
            return {"task_id": task_id, "duration": duration}
        
        elif task_type == "predict_duration":
            task_type = kwargs.get("task_type")
            complexity = kwargs.get("complexity", 1.0)
            predicted_duration = self.temporal_analyzer.predict_duration(task_type, complexity)
            return {"task_type": task_type, "predicted_duration": predicted_duration}
        
        elif task_type == "update_task_progress":
            task_id = kwargs.get("task_id")
            progress = kwargs.get("progress")
            self.temporal_analyzer.update_task_progress(task_id, progress)
            return {"task_id": task_id, "progress": progress}
        
        elif task_type == "detect_task_anomaly":
            task_id = kwargs.get("task_id")
            anomaly_result = self.temporal_analyzer.detect_task_anomaly(task_id)
            return anomaly_result
        
        elif task_type == "record_utterance":
            speaker = kwargs.get("speaker")
            content = kwargs.get("content")
            timestamp = kwargs.get("timestamp")
            self.temporal_analyzer.record_utterance(speaker, content, timestamp)
            return {"speaker": speaker, "content": content}
        
        elif task_type == "should_respond":
            should_respond = self.temporal_analyzer.should_respond()
            return {"should_respond": should_respond}
        
        elif task_type == "get_time_context":
            timezone = kwargs.get("timezone")
            session_id = kwargs.get("session_id")
            time_context = self.temporal_analyzer.get_time_context(timezone, session_id)
            return time_context
        
        elif task_type == "inject_time_anchor":
            prompt = kwargs.get("prompt")
            timezone = kwargs.get("timezone")
            session_id = kwargs.get("session_id")
            injected_prompt = self.temporal_analyzer.inject_time_anchor(prompt, timezone, session_id)
            return {"injected_prompt": injected_prompt}
        
        elif task_type == "get_task_statistics":
            task_type = kwargs.get("task_type")
            stats = self.temporal_analyzer.get_task_statistics(task_type)
            return stats
        
        elif task_type == "get_prediction_confidence":
            task_type = kwargs.get("task_type")
            confidence = self.temporal_analyzer.get_prediction_confidence(task_type)
            return {"confidence": confidence}
        
        elif task_type == "get_bayesian_stats":
            task_type = kwargs.get("task_type")
            stats = self.temporal_analyzer.get_bayesian_stats(task_type)
            return stats
        
        elif task_type == "get_all_bayesian_stats":
            stats = self.temporal_analyzer.get_all_bayesian_stats()
            return stats
        
        elif task_type == "get_calibration_report":
            report = self.temporal_analyzer.get_calibration_report()
            return report
        
        elif task_type == "get_all_abnormal_events":
            events = self.temporal_analyzer.get_all_abnormal_events()
            return {"events": events}
        
        elif task_type == "get_all_blockages":
            blockages = self.temporal_analyzer.get_all_blockages()
            return {"blockages": blockages}
        
        elif task_type == "get_conversation_flow":
            flow = self.temporal_analyzer.get_conversation_flow()
            return {"flow": flow}
        
        else:
            return {"error": f"Unknown task type: {task_type}"}

class LlamaIndexAdapter:
    """LlamaIndex适配器
    
    用于与LlamaIndex框架集成
    """
    
    def __init__(self):
        self.temporal_tool = TemporalAgentTool()
    
    def get_tools(self) -> List[BaseTool]:
        """获取工具列表
        
        Returns:
            工具列表
        """
        return [self.temporal_tool]
    
    def create_agent(self, llm: LLM) -> ReActAgent:
        """创建智能体
        
        Args:
            llm: 语言模型
            
        Returns:
            ReAct智能体
        """
        tools = self.get_tools()
        
        # 创建ReAct智能体
        agent = ReActAgent.from_llm_and_tools(
            llm=llm,
            tools=tools,
            verbose=True
        )
        
        return agent