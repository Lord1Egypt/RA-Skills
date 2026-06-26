# 定制化指南

你可以根据自身需求调整 Scenario Forecaster 的行为。

## 1. 修改框架模型
默认使用 PESTEL 驱动因素框架。如需改为 STEEP 或 SWOT，编辑 `skill/scenario_forecaster.yaml` 中的 `framework` 字段。

## 2. 调整概率评估方法
默认使用贝叶斯更新 + 历史相似事件频率。你可以替换为：
- 德尔菲法（需要人工专家输入）
- 蒙特卡洛模拟（需要数值化驱动因素）

## 3. 增加自定义数据源
在 `workflow.steps[1].sources` 中添加你的私有数据API（如内部CRM数据、销售数据）。

## 4. 输出格式定制
修改 `output_template` 中的键值顺序或添加新章节，例如增加"法律合规风险"专章。

## 5. 部署为Web服务
使用以下伪代码结构快速部署（FastAPI示例）：

```python
from fastapi import FastAPI
from pydantic import BaseModel
from scenario_forecaster import run_forecast

app = FastAPI()

class ForecastRequest(BaseModel):
    event_description: str
    time_horizon: str = "3个月"

@app.post("/forecast")
def forecast(req: ForecastRequest):
    result = run_forecast(req.event_description, req.time_horizon)
    return result
```

## 6. 贡献新的路径生成算法

欢迎提交PR，改进 scenario_generation 模块。
