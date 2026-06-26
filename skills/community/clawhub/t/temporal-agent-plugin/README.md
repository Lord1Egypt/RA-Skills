# 智能体时序感知插件

一个为AI及AI框架设计的时序感知插件，解决AI的"体感缺失"问题。

## 核心功能

### 1. 任务执行中的"过程体感" - 解决"黑盒焦虑"
- **耗时预估**：基于历史执行数据和任务类型，预测完成时间
- **进度感知**：提供实时进度更新和预估剩余时间
- **异常检测**：识别执行过程中的异常延迟，主动采取措施
- **轻量模式预测**：简化线性预测算法，适用于高频低价值场景（V2.1新增）
- **自适应模式切换**：根据置信度自动选择最佳预测器（V2.1新增）

### 2. 用户交互中的"社交体感" - 解决"读不懂空气"
- **动态打断管理**：识别用户的停顿和犹豫，合理控制回应时机
- **沉默管理**：理解不同长度停顿的语义，避免打断或忽略用户
- **上下文时效性**：根据时间窗口判断信息的时效性，提供适当的回应
- **文化适配停顿分析**：支持13种主流文化的会话停顿阈值（V2.1新增）

### 3. 物理/数字操作中的"因果体感" - 解决"时空错位"
- **动作与反馈时序对齐**：预测操作延迟，实现精准控制
- **长流程任务记忆**：通过"双时态记忆"保持任务的时间连贯性
- **因果关系预测**：理解动作和结果之间的时间延迟，做出合理预判
- **会话级时间锚点**：解决多Agent协作时的时间同步问题（V2.1新增）
- **高频同步协议优化**：轻量同步模式、批量同步、优先级同步（V2.1新增）

### 4. 系统安全性与可靠性
- **依赖项检查**：添加第三方库依赖检查，提供明确的安装指导（V2.1新增）
- **导入路径优化**：使用绝对路径导入，提升安全性（V2.1新增）
- **时间漂移检测**：识别和修正多Agent间的时间漂移（V2.1新增）
- **分布式时钟同步**：确保多Agent间的时间一致性（V2.1新增）

## 技术架构

### 核心组件
- **TemporalAnalyzer**：时序分析引擎，处理时间相关数据
- **ProgressEstimator**：进度预估系统，预测任务执行进度和剩余时间
- **AnomalyDetector**：异常检测模块，识别执行过程中的异常延迟
- **SocialTemporal**：社交时序理解，理解对话中的停顿和节奏（V2.1增强：文化适配）
- **CausalPredictor**：因果预测模型，预测动作和结果之间的时间关系
- **LightweightTimeoutPredictor**：轻量模式预测器，适用于高频场景（V2.1新增）
- **AdaptiveTimeoutPredictor**：自适应预测器，自动切换轻量/完整模式（V2.1新增）
- **ConversationTimeAnchorManager**：会话级时间锚点管理（V2.1新增）
- **CulturalPauseAdapter**：文化适配停顿分析（V2.1新增）
- **DistributedClockSync**：分布式时钟同步（V2.1新增）

### 框架集成
- **LangChainAdapter**：与LangChain框架集成
- **LlamaIndexAdapter**：与LlamaIndex框架集成
- **CustomAdapter**：与自定义AI框架集成

### API接口
- REST API接口，供外部调用

## 安装

### 依赖项
```bash
pip install -r requirements.txt
```

### 主要依赖
- pandas
- numpy
- scikit-learn
- pyarrow
- fastapi
- uvicorn
- pytest
- python-dateutil
- scipy
- matplotlib

## 使用方法

### 1. 作为Python库使用

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

### 2. 与LangChain集成

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

### 3. 与LlamaIndex集成

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

### 4. 使用API接口

```bash
# 启动API服务器
python src/api/endpoints.py

# 调用API
curl -X POST http://localhost:8000/api/duration/predict \
  -H "Content-Type: application/json" \
  -d '{"task_type": "analysis", "complexity": 2.0}'
```

## 测试

```bash
pytest tests/test_temporal.py -v
```

## 项目结构

```
temporal_agent_plugin/
├── src/
│   ├── core/             # 核心功能模块
│   │   ├── temporal_analyzer.py    # 时序分析引擎
│   │   ├── progress_estimator.py   # 进度预估系统
│   │   ├── anomaly_detector.py     # 异常检测模块
│   │   ├── social_temporal.py      # 社交时序理解（V2.1增强）
│   │   ├── causal_predictor.py     # 因果预测模型
│   │   ├── bayesian_predictor.py   # 贝叶斯预测器（V2.1新增）
│   │   ├── smart_timeout_predictor.py # 智能超时预测（V2.1新增）
│   │   ├── conversation_time_anchor.py # 会话级时间锚点（V2.1新增）
│   │   ├── distributed_clock_sync.py # 分布式时钟同步（V2.1新增）
│   │   ├── time_anchor.py          # 时间锚点基础（V2.1新增）
│   │   └── cron_task_context.py    # 定时任务上下文（V2.1新增）
│   ├── adapters/         # 框架适配器
│   │   ├── langchain_adapter.py     # LangChain集成
│   │   ├── llama_index_adapter.py   # LlamaIndex集成
│   │   └── custom_adapter.py        # 自定义框架集成
│   └── api/              # API接口
│       └── endpoints.py             # REST API接口
├── tests/                # 测试文件
│   ├── test_temporal.py             # 测试核心功能
│   └── test_temporal_v2.py           # V2.0功能测试
├── test_bayesian_quick.py        # 贝叶斯预测器测试（V2.1新增）
├── test_conversation_time_anchor.py # 会话时间锚点测试（V2.1新增）
├── test_cultural_pause.py        # 文化适配停顿测试（V2.1新增）
├── test_distributed_clock_sync.py # 分布式时钟同步测试（V2.1新增）
├── test_integration.py           # 集成测试（V2.1新增）
├── requirements.txt      # 依赖项
├── README.md             # 项目文档
├── RELEASE_NOTES.md      # 发布说明（V2.1新增）
├── VERSION_LOG.md        # 版本记录
└── SKILL.md              # 技能配置
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

## 未来规划

- [ ] 支持更多AI框架集成
- [ ] 增加更多时序分析算法
- [ ] 提供Web界面
- [ ] 支持分布式部署
- [ ] 增加更多应用场景的预训练模型

## 许可证

MIT License