---
name: stock-prediction
description: 自动化股票预测工作流。当用户发送包含股票代码的图片，并提及"预测"、"未来x天"、"采样次数"等关键词时触发。包含：图片中股票代码提取、预测环境检查与自启动、模型版本校验与切换、批量预测脚本执行、结果回传。
---

# Stock Prediction Skill

自动化股票预测工作流，处理从图片提取股票代码到执行预测并返回结果的完整流程。

## 触发条件

当同时满足以下条件时触发：
1. 用户发送了1张或多张包含股票代码的图片
2. 用户消息中包含关键词："预测"、"未来x天"、"采样次数"

## 执行流程

### Step 1: 预处理与即时反馈

**日期计算：**
- 获取当前系统日期（Today）
- 解析"未来 N 天"：`开始时间 = Today + 1天`，格式固定为 `YYYY-MM-DD`
- 解析"采样次数"：提取数字

**即时回复用户：**
```
收到{图片数量}张图片，预测开始时间：{开始时间}，采样次数：{采样次数}。
```

**数据持久化：**
- 目录：`C:\Users\Administrator\Desktop\kronos\predict\{MMDD}\`（以当前月日命名文件夹）
- 文件名：`{HHmmss}.txt`（以当前时分秒命名）
- 内容：识别图片中所有股票代码，每行一个

### Step 2: 服务健康检查 (Self-Healing)

调用接口：`GET http://localhost:8000/health`

**逻辑分支：**
- 若返回 `status: healthy` → 执行 Step 3
- 若连接失败或状态异常：
  - 打开终端，切换至 `C:\Users\Administrator\Desktop\kronos\kronos-ai\backend`
  - 执行：`conda activate my_project_env && python .\main.py`
  - 等待 10 秒后重新检查 `/health`，直到正常

### Step 3: 模型版本校验与切换

**检查当前模型：** 查看 Step 2 返回的 `model.model` 是否为 `kronos-base`

**切换逻辑：**
若当前模型不是 `kronos-base`，调用：
```bash
curl -X 'POST' 'http://localhost:8000/model/switch' \
  -H 'Content-Type: application/json' \
  -d '{"model_name": "kronos-base"}'
```
确认返回 `success: true`

### Step 4: 执行预测脚本

**环境准备：** 切换至目录 `C:\Users\Administrator\Desktop\kronos\kronos-ai`

**指令发送：**
```bash
conda activate my_project_env && python .\batch_predict.py --start_date {开始时间} --samples {采样次数}
```

> `{开始时间}` 和 `{采样次数}` 使用 Step 1 中解析的变量

### Step 5: 结果回传

**定位结果文件：**
- 路径：Step 1 的同级目录
- 文件名：`result_{Step1生成的文件名}`（例如 `result_143022.txt`）

**读取与回复：**
- 确认文件内容不为空
- 将文件内的全部预测结果文本直接发送给用户

## 辅助脚本

- `scripts/health_check.py` - 服务健康检查与自启动
- `scripts/model_switch.py` - 模型版本校验与切换
- `scripts/run_prediction.py` - 执行批量预测脚本

## 路径常量

```python
WORK_DIR = "C:\\Users\\Administrator\\Desktop\\kronos"
BACKEND_DIR = f"{WORK_DIR}\\kronos-ai\\backend"
PREDICT_DIR = f"{WORK_DIR}\\kronos-ai"
OUTPUT_BASE = f"{WORK_DIR}\\predict"
HEALTH_URL = "http://localhost:8000/health"
SWITCH_URL = "http://localhost:8000/model/switch"
TARGET_MODEL = "kronos-base"
CONDA_ENV = "my_project_env"
```
