---
name: wechat-assistant
description: 微信聊天记录智能分析与自动回复助手；自动抓取聊天记录、智能分析挖掘需求、生成回复内容并支持审核发送；当用户需要分析微信聊天数据、自动生成回复、管理人脉关系或规划任务提醒时使用
dependency:
  python:
    - uiautomation==3.17.1
    - scikit-learn==1.3.2
    - matplotlib==3.8.2
    - numpy==1.26.2
    - pandas==2.1.4
  system:
    - uiautomation-core（Windows系统UI自动化驱动）
---

# 微信聊天助手

## 任务目标
- 本Skill用于:Windows平台微信聊天记录的智能抓取、分析与自动回复
- 能力包含:聊天记录抓取、需求分析挖掘、知识库管理、回复生成与审核、数据可视化、任务规划
- 触发条件:用户需要分析微信聊天、管理人脉关系、自动回复消息或规划任务提醒

## 前置准备
- 依赖说明:Python 3.8+，uiautomation库(Windows UI自动化)，scikit-learn(文本分析)，matplotlib(可视化)
- 系统要求:Windows 10/11，微信桌面版已安装并登录
- 准备工作:
  1. 确保微信已打开并登录
  2. 确认要操作的聊天窗口可见
  3. 准备好知识库文件(kb_data.json)

## 操作步骤

### 1. 聊天记录抓取
自动定位并抓取指定聊天窗口的记录:
```bash
python scripts/chat_capture.py --contact "联系人名称" --count 100 --output ./chat_records.json
```

### 2. 知识库管理
添加对话样本学习用户沟通风格:
```bash
python scripts/knowledge_base.py --action add --samples ./samples.json
python scripts/knowledge_base.py --action query --text "需要回复的内容" --top_k 5
```

### 3. 需求分析与挖掘
对聊天记录进行深度分析:
```bash
python scripts/analyzer.py --input ./chat_records.json --mode analyze --output ./analysis_result.json
```

### 4. 自动回复生成
结合知识库生成回复并进入审核流程:
```bash
python scripts/auto_reply.py --input "对方消息内容" --contact "联系人" --knowledge_base ./kb_data.json
```
审核环节会输出候选回复供选择，支持批准/修改/拒绝三种操作。

### 5. 数据可视化
生成分析图表和人脉关系图:
```bash
python scripts/visualizer.py --input ./chat_records.json --type relationship --output ./relationship.png
python scripts/visualizer.py --input ./analysis_result.json --type timeline --output ./timeline.png
```

## 使用示例

### 示例1:抓取并分析聊天记录
- 场景/输入:抓取与"张三"最近200条聊天记录并分析
- 预期产出:JSON格式聊天记录文件 + 分析报告(关键词、频率、情感)
- 关键要点:确保微信窗口可见，联系人名称需精确匹配

### 示例2:生成并审核回复
- 场景/输入:对方发来"明天下午有空吗？"，需要生成回复
- 预期产出:3个候选回复选项 + 审核确认后发送
- 关键要点:先查询知识库学习用户风格，审核后执行发送

### 示例3:生成人脉关系图
- 场景/输入:分析所有聊天记录生成人脉关系可视化
- 预期产出:PNG格式关系图，节点大小表示互动频率
- 关键要点:需要先抓取足够多的聊天数据

## 资源索引
- 脚本:见 [scripts/chat_capture.py](scripts/chat_capture.py)(用途:抓取微信聊天记录，参数:contact/count/output)
- 脚本:见 [scripts/knowledge_base.py](scripts/knowledge_base.py)(用途:知识库管理，参数:action/samples/text/top_k)
- 脚本:见 [scripts/analyzer.py](scripts/analyzer.py)(用途:聊天数据分析，参数:input/mode/output)
- 脚本:见 [scripts/auto_reply.py](scripts/auto_reply.py)(用途:生成回复+审核，参数:input/contact/knowledge_base)
- 脚本:见 [scripts/visualizer.py](scripts/visualizer.py)(用途:数据可视化，参数:input/type/output)
- 参考:见 [references/format_spec.md](references/format_spec.md)(何时读取:定义输入输出数据格式)

## 注意事项
- 仅在Windows平台使用，需要微信桌面版支持
- 自动发送前必须经过审核确认，不可自动发送
- 抓取频率建议控制在合理范围，避免触发微信限制
- 知识库需要持续更新以提升回复质量
