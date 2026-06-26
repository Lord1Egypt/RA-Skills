# 服务器日志分析参考文档

## 日志格式说明

### 标准格式
```
[YYYY/MM/DD HH:MM:SS] 模块路径 日志级别 行号: 消息内容
```

### 示例
```
[2026/04/15 12:08:03] sanhai.flow.linear_data_flow INFO 127: flow_id:2044266474671067136 - ✅ Worker【CorrectorWorker】完成，耗时 0.00s
```

## 主要模块分类

| 模块前缀 | 所属系统 | 功能说明 |
|---------|---------|---------|
| `sanhai.flow.*` | 工作流系统 | 流程编排与执行控制 |
| `sanhai.workers.*` | Worker处理器 | 各类图像处理、OCR、批改任务 |
| `sanhai.task.*` | 任务调度 | 批改任务加载与调度 |
| `sanhai.math_tools.*` | 数学工具 | 数据库操作、邮件发送 |
| `sanhai.models.*` | 模型推理 | PaddleOCR等深度学习模型 |
| `sanhai.correction.*` | 批改系统 | 答案评分与批改逻辑 |

## Worker类型说明

| Worker名称 | 功能 |
|-----------|------|
| `LoadImageWorker` | 加载图像文件 |
| `DetPaperDirectionWorker` | 纸张方向检测 |
| `DetPaperClassifyWorker` | 纸张类型分类 |
| `DetObjectWorker` | 答题区域检测 |
| `RecPaperTextWorker` | 文本识别（OCR） |
| `RecPaperInfoWorker` | 页码/学号识别 |
| `ExtractBookPageWorker` | 教材页匹配 |
| `RecCorrectMarksWorker` | 批改符号识别 |
| `RecPaperAnswerTextWorker` | 学生答案识别 |
| `CorrectorWorker` | 批改评分 |
| `PaperAutoBranchWorker` | 流程分支控制 |

## 问题模式与诊断

### 🔴 高优先级问题

#### 1. 数据库更新失败
**模式**: `[DB] 更新失败: 实际更新0条`
**可能原因**:
- 数据记录不存在
- 数据库连接问题
- SQL语句错误
- 外键约束失败

#### 2. 题目缺少批改器
**模式**: `topic type xxx has no corrector`
**可能原因**:
- 题库中未配置该题型的批改器
- 题目类型编号不匹配
- 题库版本过旧

### 🟡 中优先级问题

#### 1. 邮件发送失败
**模式**: `[Email] 无法获取xxx，发送邮件通知失败`
**可能原因**:
- 批次信息不完整
- 缺少年级/科目ID
- 邮件服务配置问题

#### 2. 纸张类型识别失败
**模式**: `纸张类型识别错误` / `所有图像均为 classify=0/未知`
**可能原因**:
- 图像质量过低
- 非标准答题卡
- 纸张类型模型未覆盖该类型

#### 3. 图像无有效答题
**模式**: `图像无有效答题`
**可能原因**:
- 答题区域检测模型未检出
- 图像中无明显答题痕迹
- 图像拍摄角度问题

### 🟢 低优先级问题

#### 1. 学号识别失败
**模式**: `识别出无效学号` / `未识别出学号，跳过`
**影响**: 不影响批改，仅影响学生归类

#### 2. 批量处理耗时
**模式**: `batch_process cost: X.XXXs`
**诊断**: 关注耗时过长的批次（>1s）

## 性能指标解读

### TPS (Tasks Per Second)
- **定义**: 每秒处理的批改任务数
- **正常范围**: 50-300 tps（取决于图像复杂度）
- **低TPS原因**:
  - GPU显存不足
  - 批量处理分组过多
  - 网络IO瓶颈

### 批处理耗时分析
| Worker | 正常耗时 | 异常阈值 |
|-------|---------|---------|
| LoadImageWorker | <0.1s | >0.5s |
| DetPaperDirectionWorker | 0.2-0.3s | >1s |
| RecPaperTextWorker | 0.2-3s | >5s |
| ExtractBookPageWorker | <0.1s | >0.5s |
| CorrectorWorker | <0.1s | >0.5s |

### 批改状态码
| 状态码 | 含义 |
|-------|------|
| 400013 | 纸张类型不支持 |
| 400014 | 纸张类型识别失败 |
| 400018 | 图像无有效答题 |
| 400021 | 批改完成 |
| 400023 | 批改完成（需复核） |

## 常见问题排查流程

### 1. 批改失败排查
```
检查纸张分类 → 检查答题区域 → 检查OCR识别 → 检查题库匹配 → 检查批改器
```

### 2. 性能问题排查
```
检查TPS指标 → 分析耗时Worker → 检查GPU使用 → 检查批量分组
```

### 3. 数据问题排查
```
检查日志时间范围 → 提取ERROR/WARNING → 定位flow_id → 追溯数据ID
```

## flow_id 追踪方法

flow_id 是日志中的关键追踪标识：
```
flow_id:2044266474671067136
```

可用于：
- 串联同一批次的所有日志
- 追踪数据在各个Worker间的流转
- 定位特定请求的问题节点

## Python 异常追踪

### 异常日志格式
```
[YYYY/MM/DD HH:MM:SS] 模块路径 ERROR 行号: 错误消息
Traceback (most recent call last):
  File "/path/to/file.py", line xxx, in function_name
    ...
ExceptionType: 错误描述
```

### 示例
```
[2026/04/13 15:52:41] sanhai.models.base_model ERROR 78: (PreconditionNotMet) Tensor holds no memory.
Traceback (most recent call last):
  File "/home/javanep/service/mathHubV4/sanhai/models/base_model.py", line 72, in __call__
    out = self.output(batch_images, **kwargs)
  File "/home/javanep/service/mathHubV4/sanhai/models/rec_abi_model.py", line 45, in output
    output = self.output_handles[0].copy_to_cpu()
RuntimeError: (PreconditionNotMet) Tensor holds no memory. Call Tensor::mutable_data firstly.
```

### 异常优先级
**🚨 Python 程序异常是最高优先级的问题**，比普通ERROR日志更严重，需要优先处理。

### 常见异常类型

| 异常类型 | 可能原因 | 严重程度 |
|---------|---------|---------|
| `RuntimeError` | PaddlePaddle Tensor内存问题 | 🔴 高 |
| `ValueError` | 数据形状不匹配 | 🔴 高 |
| `TypeError` | 数据类型错误 | 🔴 高 |
| `ConnectionError` | 数据库/网络连接问题 | 🔴 高 |
| `FileNotFoundError` | 文件路径问题 | 🟡 中 |
| `KeyError` | 字典键不存在 | 🟡 中 |

### 关键异常诊断

#### 1. Tensor内存问题 (RuntimeError: Tensor holds no memory)
**原因**: PaddlePaddle多线程GPU推理时，Tensor未正确初始化
**涉及文件**: `base_model.py`, `rec_abi_model.py`
**建议**: 检查模型推理的线程安全性，确保Tensor在主线程初始化

#### 2. 数据形状不匹配 (ValueError: shapes do not match)
**原因**: 输入图像预处理与模型预期输入不一致
**涉及文件**: `workers/*.py`
**建议**: 检查图像resize/normalize流程
