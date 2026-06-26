from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from src.core.temporal_analyzer import TemporalAnalyzer
from src.core.progress_estimator import ProgressEstimator
from src.core.anomaly_detector import AnomalyDetector
from src.core.social_temporal import SocialTemporal
from src.core.causal_predictor import CausalPredictor
from src.core.time_anchor import TimeAnchorInjector

class TemporalAgentTool(BaseTool):
    """LangChain时序感知工具
    """
    
    name = "temporal_agent"
    description = "时序感知工具，用于处理时间相关的任务，包括进度预估、异常检测、社交时序理解等"
    
    def __init__(self):
        super().__init__()
        # 使用集成了所有功能的TemporalAnalyzer
        self.temporal_analyzer = TemporalAnalyzer()
    
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
    
    async def _arun(self, task_type: str, **kwargs) -> Dict[str, Any]:
        """异步运行时序感知工具
        
        Args:
            task_type: 任务类型
            **kwargs: 额外参数
            
        Returns:
            结果
        """
        return self._run(task_type, **kwargs)

class LangChainAdapter:
    """LangChain适配器
    
    用于与LangChain框架集成
    """
    
    def __init__(self):
        self.temporal_tool = TemporalAgentTool()
    
    def get_tools(self) -> list:
        """获取工具列表
        
        Returns:
            工具列表
        """
        return [self.temporal_tool]
    
    def create_agent(self, llm) -> AgentExecutor:
        """创建智能体
        
        Args:
            llm: 语言模型
            
        Returns:
            智能体执行器
        """
        tools = self.get_tools()
        
        # 创建提示模板
        prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant with temporal awareness. Use the temporal_agent tool to:
            1. Estimate task durations
            2. Track progress
            3. Detect anomalies
            4. Understand social timing
            5. Predict action latencies
            
            Always consider time when responding to user requests.
            
            {input}
            
            {agent_scratchpad}
            """
        )
        
        # 创建智能体
        agent = AgentExecutor.from_agent_and_tools(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=tools,
            llm=llm,
            prompt=prompt,
            verbose=True
        )
        
        return agent