# Orchestrator ↔ Agent 交互协议

## 概述

V3.0采用orchestrator.py控制流程，Agent只负责执行prompt返回JSON。

## 交互模式

Agent在整个流程中只做以下几类事情：

### 1. 调用orchestrator命令
```bash
exec: python3 {SKILL_DIR}/tools/orchestrator.py --action <action> [--args ...]
```

### 2. 执行LLM prompt并返回JSON
当orchestrator需要LLM能力时（P0-P7），Agent：
1. 读取orchestrator指定的prompt文件
2. 读取orchestrator指定的输入数据
3. 用自己的推理能力生成JSON结果
4. 将JSON结果传给orchestrator的step_run action

### 3. 读取图片（PX步骤）
当orchestrator返回图片列表时，Agent：
1. 逐张read图片文件
2. 描述图片内容
3. 将描述结果传给orchestrator的step0_8_save action

## 标准流程

```
Agent: exec orchestrator.py --action init
       → 获得 task_id, data_dir

Agent: exec orchestrator.py --action onboarding --skill-dir ... --data-dir ... --task-id ...
       → 获得环境检查结果
       → 输出: ✅ Onboarding完成 | 环境正常 | task_id=xxx

[PRD审查交互 - 如需要]
[L5上传交互 - 如需要]

Agent: exec orchestrator.py --action step0 --requirement-file "xxx.docx" ...
       → 获得 domain, requirement_length
       → 输出: ✅ Step 0完成 | 需求已解析 | 业务域:xxx

Agent: exec orchestrator.py --action step0_8_prep --requirement-file "xxx.docx" ...
       → 获得待理解的图片列表
       → Agent逐张read图片，生成描述
Agent: exec orchestrator.py --action step0_8_save --results-json '[...]' ...
       → 输出: ✅ PX完成 | 图片N张/视觉V张 | 文件已保存

[对每个P0-P7步骤:]
Agent: read {SKILL_DIR}/prompts/P{N}_xxx.md  (读取prompt)
Agent: read {DATA_DIR}/p{N-1}_output.json    (读取上游产物)
Agent: [用推理能力生成JSON结果]
Agent: exec orchestrator.py --action step_run --step P{N} --agent-output '{JSON}' ...
       → orchestrator校验+写文件+guard+gate pass
       → 输出: ✅ P{N}完成 | {指标} | 文件已保存

Agent: exec orchestrator.py --action step7_export ...
       → 输出: ✅ Excel已生成 | {文件路径}
       → MEDIA:{excel_path}
```

## Agent输出规则

1. 每个orchestrator调用后，只输出1行状态
2. 不输出JSON内容、中间分析、调试信息
3. orchestrator返回error时，输出1行错误信息
4. 不自行写文件、不绕过orchestrator
