---
name: "temporal-agent-plugin"
description: "Provides temporal awareness for AI agents, including timing prediction, progress monitoring, and social timing understanding. Invoke when AI needs time perception capabilities or when timing-related issues need to be addressed."
---

# 智能体时序感知插件

一个为AI及AI框架设计的时序感知插件，解决AI的"体感缺失"问题。

## 核心功能

### 1. 任务执行中的"过程体感" - 解决"黑盒焦虑"
- **耗时预估**：基于历史执行数据和任务类型，预测完成时间
- **进度感知**：提供实时进度更新和预估剩余时间
- **异常检测**：识别执行过程中的异常延迟，主动采取措施

### 2. 用户交互中的"社交体感" - 解决"读不懂空气"
- **动态打断管理**：识别用户的停顿和犹豫，合理控制回应时机
- **沉默管理**：理解不同长度停顿的语义，避免打断或忽略用户
- **上下文时效性**：根据时间窗口判断信息的时效性，提供适当的回应

### 3. 物理/数字操作中的"因果体感" - 解决"时空错位"
- **动作与反馈时序对齐**：预测操作延迟，实现精准控制
- **长流程任务记忆**：通过"双时态记忆"保持任务的时间连贯性
- **因果关系预测**：理解动作和结果之间的时间延迟，做出合理预判

## 技术架构

### 核心组件
- **TemporalAnalyzer**：时序分析引擎，处理时间相关数据
- **ProgressEstimator**：进度预估系统，预测任务执行进度和剩余时间
- **AnomalyDetector**：异常检测模块，识别执行过程中的异常延迟
- **SocialTemporal**：社交时序理解，理解对话中的停顿和节奏
- **CausalPredictor**：因果预测模型，预测动作和结果之间的时间关系

### 框架集成
- **LangChainAdapter**：与LangChain框架集成
- **LlamaIndexAdapter**：与LlamaIndex框架集成
- **CustomAdapter**：与自定义AI框架集成

## 安装

### 依赖项
```bash
pip install pandas numpy scikit-learn pyarrow fastapi uvicorn pytest python-dateutil scipy matplotlib pytz geopy
```

## 使用方法

### 作为Python库使用

```python
from src.core.temporal_analyzer import TemporalAnalyzer
from src.core.progress_estimator import ProgressEstimator
from src.core.anomaly_detector import AnomalyDetector
from src.core.social_temporal import SocialTemporal
from src.core.causal_predictor import CausalPredictor

# 初始化时序分析引擎
analyzer = TemporalAnalyzer()

# 开始计时
task_id = "download_task"
analyzer.start_timer(task_id)

# 执行任务
# ...

# 停止计时
duration = analyzer.stop_timer(task_id)
print(f"任务执行时间：{duration}秒")

# 预测任务执行时间
predicted_duration = analyzer.predict_duration("analysis", complexity=2.0)
print(f"预测执行时间：{predicted_duration}秒")
```

### 与LangChain集成

```python
from src.adapters.langchain_adapter import LangChainAdapter
from langchain.chat_models import ChatOpenAI

# 初始化适配器
adapter = LangChainAdapter()

# 创建语言模型
llm = ChatOpenAI(temperature=0)

# 创建智能体
agent = adapter.create_agent(llm)

# 运行智能体
result = agent.run("帮我分析一份100页的财报，告诉我需要多久")
print(result)
```

### 与LlamaIndex集成

```python
from src.adapters.llama_index_adapter import LlamaIndexAdapter
from llama_index.core.llms import OpenAI

# 初始化适配器
adapter = LlamaIndexAdapter()

# 创建语言模型
llm = OpenAI(temperature=0)

# 创建智能体
agent = adapter.create_agent(llm)

# 运行智能体
result = agent.chat("帮我分析一份100页的财报，告诉我需要多久")
print(result)
```

## 应用场景

### 1. AI助手
- 为AI助手添加时间感知能力，让它知道任务需要多长时间
- 当任务执行时间过长时，主动告知用户
- 理解用户的停顿和犹豫，实现自然的对话

### 2. 自动化工具
- 监控自动化任务的执行进度
- 检测异常延迟，及时采取措施
- 预测任务完成时间，合理安排后续任务

### 3. 物理操作智能体
- 预测操作延迟，实现精准控制
- 理解动作和结果之间的时间关系
- 保持长流程任务的时间连贯性

## 技术特点

- **精确的时间感知**：基于历史数据和统计分析，提供准确的时间预测
- **实时的进度反馈**：实时更新任务进度，提供剩余时间预估
- **智能的异常处理**：自动检测异常延迟，主动采取措施
- **自然的社交交互**：理解对话中的停顿和节奏，实现自然的交互
- **精准的因果预测**：预测动作和结果之间的时间关系，实现精准控制

## 版本

- **2.0.0**：新增贝叶斯预测器、智能超时预测器、分布式时钟同步等功能
- **1.0.0**：初始版本，包含所有核心功能

## 许可

MIT-0
