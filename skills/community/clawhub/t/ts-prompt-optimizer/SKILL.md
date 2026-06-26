---
name: ts-prompt-optimizer
description: 冬冬主人定制提示词优化器 - 完全个性化 多模型支持 智能路由集成 使用前缀 "ts:" 触发 
version: 1.0.0
author: 陈冬冬定制版
metadata:
  openclaw:
    emoji: "[TARGET]"
    homepage: "https://github.com/openclaw/clawhub"
    requires:
      env:
        - name: DEEPSEEK_API_KEY
          description: "DeepSeek API密钥（用于简单优化）"
          required: false
        - name: BAILIAN_API_KEY
          description: "千问API密钥（用于复杂优化）"
          required: false
      bins:
        - python3
---

# TS-Prompt-Optimizer 技能文档

## 技能概述

**TS-Prompt-Optimizer**（Task Specification Prompt Optimizer）是专为冬冬主人定制的提示词优化技能，具有以下核心特点：

1. **完全个性化** - 基于主人使用习惯和学习历史定制优化规则
2. **多模型支持** - 智能选择最优模型进行提示词优化
3. **智能路由集成** - 与现有模型路由系统深度集成
4. **上下文感知** - 理解对话历史和任务背景
5. **学习进化** - 从主人反馈中持续改进优化策略

## 触发机制

### 前缀触发
- **标准前缀**：`ts:`（Task Specification）
- **备用前缀**：`ts-opt:` `优化:`
- **位置要求**：必须位于消息开头（允许前导空格）
- **大小写**：不敏感（`TS:` `Ts:` `tS:` 均可）

### 触发示例
```
ts: 帮我写一个Python脚本
ts-opt: 分析这张图片
优化: 总结这篇文章
```

## 功能特点

### 1. 智能前缀检测
- **多前缀支持**：`ts:` `ts-opt:` `优化:` 三种触发方式
- **灵活匹配**：大小写不敏感，支持前导空格
- **快速响应**：检测时间 < 100ms

### 2. 多模型智能路由
- **成本优先**：简单任务使用DeepSeek（成本低）
- **能力优先**：复杂任务使用千问（能力强）
- **自动切换**：根据任务复杂度自动选择最优模型
- **故障转移**：主模型失败时自动切换到备用模型

### 3. 个性化优化规则
- **主人专属**：基于冬冬主人使用习惯定制
- **任务分类**：自动识别技术 写作 分析 创意等任务类型
- **上下文感知**：结合对话历史进行优化
- **持续学习**：从主人反馈中不断改进

### 4. 完整配置系统
- **环境变量**：支持DEEPSEEK_API_KEY和BAILIAN_API_KEY
- **交互式向导**：`config_wizard.py` 提供友好配置界面
- **命令行工具**：`ts-config` 提供完整配置管理功能
- **状态检查**：实时监控配置状态和模型可用性

### 5. 性能优化
- **快速响应**：优化过程 < 2秒
- **成本控制**：优化成本 < 任务成本的10%
- **资源高效**：内存占用低，无外部依赖
- **稳定可靠**：完善的错误处理和恢复机制

## 使用方法

### 基本使用
直接在对话中使用 `ts:` 前缀触发优化：

```
ts: 帮我写个Python爬虫脚本
ts-opt: 分析这个季度的销售数据
优化: 为新产品写个营销文案
```

### 高级使用

#### 1. 指定任务类型
可以在前缀后添加任务类型提示：

```
ts: [技术] 设计数据库表结构
ts: [写作] 写封商务邮件
ts: [分析] 分析用户行为数据
```

#### 2. 添加约束条件
在任务描述中明确约束：

```
ts: 写个Python函数，要求：
- 使用异步编程
- 支持错误重试
- 输出JSON格式
```

#### 3. 结合上下文
优化器会自动结合对话历史：

```
用户：我之前在做电商项目
用户：ts: 帮我设计用户表结构
优化器：会结合电商项目上下文进行优化
```

### 配置管理

#### 1. 初始配置
```bash
# 进入技能目录
cd skills/ts-prompt-optimizer/scripts

# 运行配置向导
python config_wizard.py

# 或使用命令行工具
ts-config setup
```

#### 2. 状态检查
```bash
ts-config status      # 查看配置状态
ts-config check       # 检查配置问题
ts-config test        # 测试模型连接
```

#### 3. 模型管理
```bash
ts-config show        # 显示模型详情
ts-config get deepseek  # 获取特定模型配置
ts-config optimize "测试优化功能"  # 测试优化功能
```

## 配置系统

### 配置文件结构
TS-Prompt-Optimizer 使用分层配置系统：

1. **默认配置**：`config/model_config.json` - 基础模型配置
2. **用户配置**：`~/.openclaw/ts-optimizer-config.yaml` - 用户个性化配置
3. **环境变量**：`DEEPSEEK_API_KEY` `BAILIAN_API_KEY` - API密钥
4. **运行时配置**：内存中的动态配置

### 配置优先级
```
环境变量 > 用户配置文件 > 默认配置文件
```

### 配置项说明

#### 模型配置
```yaml
models:
  deepseek:
    provider: deepseek
    model: deepseek-chat
    api_key_env: DEEPSEEK_API_KEY
    enabled: true
    priority: 1
    cost_per_1k_tokens: 0.42
    capabilities:
      - 日常对话
      - 简单优化
      - 代码审查

  qwen35:
    provider: bailian
    model: qwen3.5-plus
    api_key_env: BAILIAN_API_KEY
    enabled: true
    priority: 2
    cost_per_1k_tokens: 0.00
    capabilities:
      - 复杂任务
      - 图像识别
      - 中文写作

  qwen_coder:
    provider: bailian
    model: qwen3-coder-next
    api_key_env: BAILIAN_API_KEY
    enabled: true
    priority: 3
    cost_per_1k_tokens: 0.00
    capabilities:
      - 技术开发
      - 代码生成
      - 系统设计
```

#### 路由策略
```yaml
routing:
  strategy: cost_effective  # 成本优先策略
  fallback_model: deepseek  # 备用模型
  cost_threshold: 1.00      # 成本阈值（美元/千token）
```

#### 用户偏好
```yaml
user_preferences:
  default_optimization_level: standard
  show_config_summary: true
  auto_test_connections: true
  preferred_output_formats:
    code: "完整代码 + 注释 + 测试"
    report: "Markdown + 数据可视化"
    email: "正式商务邮件格式"
```

### 配置验证
配置系统会自动验证：
1. **API密钥有效性**：检查密钥格式和权限
2. **模型可用性**：测试模型连接状态
3. **配置完整性**：检查必需配置项
4. **环境兼容性**：检查系统环境和依赖

### 配置备份与恢复
```bash
# 备份配置
ts-config backup

# 恢复配置
ts-config restore backup_20240404.yaml

# 导出配置
ts-config export > my_config.yaml

# 导入配置
ts-config import < my_config.yaml
```

### 前缀触发
- **标准前缀**：`ts:`（Task Specification）
- **备用前缀**：`ts-opt:` `优化:`
- **位置要求**：必须位于消息开头（允许前导空格）
- **大小写**：不敏感（`TS:` `Ts:` `tS:` 均可）

### 触发示例
```
ts: 帮我写一个Python脚本
ts-opt: 分析这张图片
优化: 总结这篇文章
```

## 配置系统

### 多模型API配置
TS-Prompt-Optimizer 支持多种AI模型，需要配置相应的API密钥：

#### **配置方式**：
1. **环境变量**（推荐）：
   ```bash
   export DEEPSEEK_API_KEY="sk-xxx"
   export BAILIAN_API_KEY="sk-yyy"
   ```

2. **交互式配置向导**：
   ```bash
   cd skills/ts-prompt-optimizer/scripts
   python config_wizard.py
   ```

3. **命令行工具**：
   ```bash
   ts-config setup      # 运行配置向导
   ts-config status     # 查看配置状态
   ts-config test       # 测试模型连接
   ts-config check      # 检查配置问题
   ```

#### **支持的模型**：
- **DeepSeek**：日常对话 简单任务（成本低）
- **千问 3.5 Plus**：复杂任务 图像识别（免费额度）
- **千问 Coder Next**：技术开发 代码生成（免费额度）
- **自定义模型**：支持其他AI模型

#### **配置检查**：
运行以下命令检查配置状态：
```bash
ts-config status
```

输出示例：
```
TS-Prompt-Optimizer 配置状态
============================================================
总模型数: 3
已配置模型: 2
启用模型: 3

模型详情：
  deepseek: deepseek/deepseek-chat [可用]
  qwen35: bailian/qwen3.5-plus [可用]
  qwen_coder: bailian/qwen3-coder-next [启用但未配置]
```

## 优化流程（四层架构）

### 层 1：输入处理
```
原始输入   前缀检测   意图提取   上下文分析
```

### 层 2：多模型优化
```
原始意图   模型选择器   发送到最优模型   返回优化结果
```

**模型选择策略**：
- **简单优化**（日常对话 简单任务）  DeepSeek（成本低）
- **复杂优化**（技术任务 创意写作）  千问 3.5 Plus（免费且能力强）
- **专业优化**（特定领域任务）  其他专业模型

### 层 3：个性化适配
```
优化结果   主人偏好适配   应用个性化规则   最终提示词
```

**个性化规则来源**：
1. `memory/ts-optimization-history.md` - 历史优化案例
2. `memory/dongdong-preferences.md` - 主人明确偏好
3. 实时对话上下文分析

### 层 4：执行与反馈
```
最终提示词   执行   收集反馈   更新知识库
```

## 优化原则（冬冬主人定制版）

### 1. 角色定义优化
**默认角色**：`资深AI助手专家，专为冬冬主人服务`
**根据任务类型自动调整**：
- 技术任务   `资深全栈开发工程师`
- 写作任务   `专业文案策划师`
- 分析任务   `数据分析专家`
- 创意任务   `创意策划专家`

### 2. 任务澄清优化
**原则**：将模糊指令转化为具体可执行任务
**示例**：
- 原始：`写个脚本`
- 优化：`编写一个Python脚本，功能是...，要求...，输出格式...`

### 3. 上下文补充优化
**自动补充**：
- 对话历史中的相关信息
- 主人的已知偏好和习惯
- 任务相关的背景假设

### 4. 输出格式规范
**标准化输出格式**：
- 代码任务   完整可运行代码 + 注释 + 使用说明
- 文档任务   Markdown格式 + 清晰结构
- 分析任务   数据表格 + 结论总结
- 创意任务   结构化内容 + 风格说明

### 5. 质量约束优化
**自动添加**：
- 字数/篇幅要求
- 技术栈约束
- 风格/语气要求
- 时间/复杂度估计

## 与智能路由系统集成

### 集成方式
```
主人输入 "ts: [任务]"   触发优化技能   智能路由选择模型   优化提示词   执行优化后的任务
```

### 成本优化
- **优化过程本身**：使用成本最低的合适模型
- **任务执行**：根据任务复杂度自动选择最优模型
- **总体目标**：在保证质量的前提下最大化成本节省

## 个性化学习机制

### 学习数据源
1. **历史优化记录**：每次优化都记录到 `memory/ts-optimization-history.md`
2. **主人反馈**：通过  /  反馈收集优化效果
3. **成功案例**：记录特别成功的优化案例
4. **失败教训**：分析优化失败的原因

### 学习算法
1. **模式识别**：识别主人偏好的优化模式
2. **反馈学习**：根据主人反馈调整优化策略
3. **上下文关联**：学习任务类型与优化方式的关联
4. **持续进化**：定期回顾和更新优化规则

## 使用示例

### 示例 1：简单技术任务
**主人输入**：
```
ts: 写个排序函数
```

**优化过程**：
1. 检测到 `ts:` 前缀，触发优化
2. 识别为技术任务，选择千问 3.5 Plus 优化
3. 应用技术任务优化规则
4. 生成优化后的提示词

**优化结果**：
```
作为资深Python开发工程师，请编写一个高效的排序函数，要求：
1. 支持多种排序算法（快速排序 归并排序 堆排序）
2. 包含完整的类型提示和文档字符串
3. 提供性能测试和复杂度分析
4. 输出完整的可运行代码
请使用Python 3.9+语法，代码风格符合PEP 8规范 
```

### 示例 2：复杂分析任务
**主人输入**：
```
ts: 分析销售数据
```

**优化结果**：
```
作为数据分析专家，请分析提供的销售数据，要求：
1. 数据清洗和预处理步骤
2. 关键指标计算（销售额 增长率 客户分布）
3. 可视化图表（折线图 柱状图 饼图）
4.  actionable insights 和建议
5. 输出Markdown格式报告
请假设数据包含日期 产品 销售额 客户ID等字段 
```

## 文件结构

```
skills/ts-prompt-optimizer/
    SKILL.md              # 技能文档（本文件）
    scripts/
        optimizer.py      # 核心优化引擎
        model_selector.py # 模型选择器
        personalizer.py   # 个性化适配器
        learner.py        # 学习模块
    config/
        dongdong_rules.json  # 主人专属优化规则
        model_config.json    # 模型配置
    memory/
        optimization_history.md  # 优化历史
        preferences.md           # 主人偏好
```

## 配置说明

### 主人偏好配置
编辑 `config/dongdong_rules.json`：
```json
{
  "preferred_roles": {
    "technical": "资深全栈工程师",
    "writing": "专业文案策划",
    "analysis": "数据分析专家"
  },
  "output_formats": {
    "code": "完整代码 + 注释 + 测试",
    "report": "Markdown + 数据可视化",
    "email": "正式商务邮件格式"
  },
  "quality_constraints": {
    "default_word_count": 500,
    "preferred_tech_stack": ["Python", "JavaScript", "React"],
    "writing_style": "专业 简洁 实用"
  }
}
```

### 模型配置
编辑 `config/model_config.json`：
```json
{
  "optimization_models": {
    "simple": "deepseek/deepseek-chat",
    "complex": "bailian/qwen3.5-plus",
    "technical": "bailian/qwen3-coder-next",
    "creative": "bailian/qwen3.5-plus"
  },
  "routing_strategy": "cost_effective",
  "fallback_model": "deepseek/deepseek-chat"
}
```

## 性能指标

### 优化质量指标
- **清晰度提升**：模糊指令   明确指令
- **完整性提升**：补充缺失的上下文和约束
- **可执行性**：优化后的指令可直接执行
- **主人满意度**：通过反馈收集

### 效率指标
- **优化时间**：< 2秒
- **成本效率**：优化成本 < 任务执行成本的10%
- **准确率**：优化符合主人意图的比例

## 故障处理

### 常见问题
1. **前缀未触发**：检查消息是否以 `ts:` 开头
2. **优化质量差**：检查个性化规则配置
3. **模型选择错误**：检查模型配置和路由策略
4. **学习数据丢失**：检查 memory/ 目录权限

### 恢复措施
1. 回退到默认优化规则
2. 使用备用模型
3. 提示主人提供更多上下文
4. 记录问题并后续优化

## 安装方法

### 自动安装（推荐）
如果技能已发布到ClawHub，可以通过以下命令安装：

```bash
# 搜索技能
clawhub search ts-prompt-optimizer

# 安装技能
clawhub install ts-prompt-optimizer

# 或指定版本
clawhub install ts-prompt-optimizer@1.0.0
```

### 手动安装
如果从源代码安装：

```bash
# 1. 下载技能包
cd ~/.openclaw/workspace/skills

# 2. 解压技能包
unzip ts-prompt-optimizer.zip

# 3. 运行安装脚本
cd ts-prompt-optimizer/scripts
python quick_setup.py

# 4. 验证安装
ts-config status
```

### 依赖检查
TS-Prompt-Optimizer 需要以下依赖：

```bash
# Python 3.8+
python --version

# 必需Python库
pip install pyyaml

# 可选：用于API调用
pip install requests
```

### 快速安装脚本
技能包中包含快速安装脚本：

```bash
cd ts-prompt-optimizer/scripts
python quick_setup.py
```

该脚本会自动：
1. 检查Python版本
2. 安装必需依赖
3. 创建配置文件
4. 设置环境变量
5. 验证安装

### 安装验证
安装完成后，运行以下命令验证：

```bash
ts-config status     # 检查配置状态
ts-config test       # 测试模型连接
ts-config check      # 检查系统兼容性
```

## 测试方法

### 单元测试
技能包含完整的单元测试套件：

```bash
# 运行所有测试
cd skills/ts-prompt-optimizer/scripts
python test_simple.py

# 运行特定测试
python test_optimizer.py
```

### 功能测试
#### 1. 前缀检测测试
```python
# 测试脚本示例
from optimizer import TSPromptOptimizer

optimizer = TSPromptOptimizer()

test_cases = [
    ('ts: 测试', True),
    ('TS: 大写', True),
    ('ts-opt: 备用', True),
    ('优化: 中文', True),
    ('无前缀', False),
]

for input_text, expected in test_cases:
    result = optimizer.should_optimize(input_text)
    print(f'{input_text}: {result} (期望: {expected})')
```

#### 2. 优化功能测试
```python
# 测试优化功能
result = optimizer.optimize_prompt('ts: 写个Python函数')
print('优化结果:', result)
```

#### 3. 配置系统测试
```bash
# 测试配置系统
ts-config status
ts-config check
ts-config test
```

### 集成测试
#### 1. 与OpenClaw集成测试
```bash
# 在OpenClaw中测试技能触发
# 发送消息: "ts: 帮我写个脚本"
# 检查是否触发优化
```

#### 2. 与智能路由系统集成测试
```bash
# 测试模型路由
# 简单任务应使用DeepSeek
# 复杂任务应使用千问
```

### 性能测试
#### 1. 响应时间测试
```python
import time
from optimizer import TSPromptOptimizer

optimizer = TSPromptOptimizer()
start = time.time()
result = optimizer.optimize_prompt('ts: 测试')
elapsed = time.time() - start
print(f'优化时间: {elapsed:.3f}秒')
```

#### 2. 内存使用测试
```bash
# 使用memory_profiler测试内存使用
pip install memory_profiler
mprof run python test_performance.py
```

### 兼容性测试
#### 1. 平台兼容性
- [OK] Windows 10/11
- [OK] Linux (Ubuntu 20.04+)
- [OK] macOS 12+

#### 2. Python版本兼容性
- [OK] Python 3.8
- [OK] Python 3.9
- [OK] Python 3.10
- [OK] Python 3.11
- [OK] Python 3.12

### 错误处理测试
```python
# 测试错误处理
try:
    # 测试无效输入
    result = optimizer.optimize_prompt('')
    print('空输入测试:', result)
except Exception as e:
    print('错误处理正常:', e)
```

### 自动化测试
技能包含自动化测试脚本：

```bash
# 运行完整测试套件
cd skills/ts-prompt-optimizer/scripts
python run_all_tests.py
```

测试输出示例：
```
========================================
TS-Prompt-Optimizer 测试报告
========================================
[OK] 前缀检测测试: 5/5 通过
[OK] 优化功能测试: 3/3 通过
[OK] 配置系统测试: 4/4 通过
[OK] 性能测试: <2秒响应
[OK] 错误处理测试: 2/2 通过
========================================
总测试: 14/14 通过 (100%)
========================================
```

### 测试覆盖率
```bash
# 使用coverage.py测试代码覆盖率
pip install coverage
coverage run -m pytest test_*.py
coverage report -m
```

目标覆盖率：
- 语句覆盖率: >90%
- 分支覆盖率: >85%
- 函数覆盖率: >95%

## 更新与维护

### 定期维护
- **每周**：回顾优化历史，更新个性化规则
- **每月**：分析主人反馈，调整优化策略
- **每季度**：评估技能效果，进行大版本更新

### 主人参与
主人可以通过以下方式参与技能优化：
1. 提供优化反馈（[OK]/[FAIL]）
2. 分享特别成功的优化案例
3. 提出新的优化需求
4. 调整个性化配置

---

**技能状态**：[OK] 就绪
**最后更新**：2026-04-04
**版本**：1.0.0（冬冬主人定制初版）

### 定期维护
- **每周**：回顾优化历史，更新个性化规则
- **每月**：分析主人反馈，调整优化策略
- **每季度**：评估技能效果，进行大版本更新

### 主人参与
主人可以通过以下方式参与技能优化：
1. 提供优化反馈（ / ）
2. 分享特别成功的优化案例
3. 提出新的优化需求
4. 调整个性化配置

---

**技能状态**：[OK] 就绪
**最后更新**：2026-04-04
**版本**：1.0.0（冬冬主人定制初版）