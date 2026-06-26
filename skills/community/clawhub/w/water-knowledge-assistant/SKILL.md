---
name: water-knowledge-assistant
description: 水务设备知识库 AI 助手，提供设备查询、选型建议、参数对比等功能
version: 1.0.0
author: OpenClaw Team
permissions:
  - read:D:\code\openclaw_lakeskill\outerfiles\
  - readwrite:D:\code\openclaw_lakeskill\
triggers:
  - type: keyword
    words: ["液位计", "水尺", "流量计", "水质传感器", "选型", "参数", "对比", "询价", "说明书"]
tools:
  - vector_search
  - tavily_search
  - file_operation
  - cron_job
audit:
  enabled: true
  log_level: info
  fields: [timestamp, session_id, user_id, action_type, tool_name, input, output, risk_level, trace_id]
---

# 水务设备知识库 AI 助手

## 功能目标

### 1. 知识库问答
- 支持查询：液位计、水尺、流量计、水质传感器
- 数据来源：设备说明书、技术参数、选型指南、应用案例
- AI 优先使用 RAG 检索知识库，再生成答案

### 2. 设备选型建议
根据用户输入的工况信息（如：户外污水池、腐蚀性介质、量程10米、预算有限），提供：
- 工况分析
- 设备类型匹配
- 设备型号推荐
- 推荐理由

### 3. 技术参数查询
支持查询设备的详细技术参数，包括：
- IP等级
- 量程
- 精度
- 供电
- 通讯协议

### 4. 设备对比
支持对不同设备型号进行参数对比，生成对比表

### 5. 询价引导
当用户表达购买意向时，引导用户提供：
- 型号
- 数量
- 公司
- 联系人
- 电话
- 应用场景
并生成询价单草稿

### 6. 文档下载
当用户询问说明书、PDF、选型指南时，返回文档名称和下载路径

## 系统能力

### 1. 审计日志系统（三录）
- **操作录迹**：记录用户输入、AI决策、工具调用
- **结果录存**：记录检索结果、工具返回、生成报告、错误信息
- **可追溯**：支持按时间戳、会话ID、用户ID等维度查询
- **日志格式**：JSONL

### 2. 外部数据采集系统
- 支持从 D:\code\openclaw_lakeskill\outerfiles\ 读取知识库
- 支持文件类型：PDF、Markdown、TXT、DOCX
- 目标目录：D:\code\openclaw_lakeskill\files
- 增量处理：计算SHA256 hash判断是否更新

### 3. Tavily 实时更新
- 支持定时更新：每天凌晨3点（cron: 0 3 * * *）
- 支持按需更新：当用户问题包含"最新"、"最近"、"2026"、"今年"时触发
- 搜索参数：query、max_results、time_range、include_domains
- 结果处理：AI总结后以Markdown存入知识库并建立向量索引

## 使用指南

### 查询示例
1. **知识库问答**："液位计有哪些类型？"
2. **设备选型**："户外污水池，腐蚀性介质，量程10米，预算有限"
3. **参数查询**："RL-1000 的防护等级是多少？"
4. **设备对比**："对比 RL-1000 和 UL-200"
5. **询价引导**："我要买 RL-1000"
6. **文档下载**："RL-1000 的说明书在哪里？"

## 扩展说明

### 新增设备类型
1. 在 references/device_types.md 中添加新设备类型
2. 在 references/selection_rules.md 中添加选型规则
3. 在 references/parameter_fields.md 中添加参数字段

### 新增数据源
1. 在 config/paths.yaml 中配置新的数据源路径
2. 在 scripts/knowledge_base_import.py 中添加新的文件类型支持

### 新增工具
1. 在 SKILL.md 中添加新工具权限
2. 在 scripts/ 目录下添加工具实现
3. 在 config/ 目录下添加工具配置

## 安全规范

### 权限控制
- 仅能访问 D:\code\openclaw_lakeskill\outerfiles\ 和 D:\code\openclaw_lakeskill\
- 禁止访问系统目录和用户目录

### 错误处理
- 所有操作必须包含 try-catch
- 错误信息必须记录到审计日志
- 异常返回统一格式：{"error": true, "message": "错误信息"}

## 安装指南

### 1. 环境准备

#### 硬件要求
- CPU: 4核以上
- 内存: 8GB以上
- 存储空间: 50GB以上

#### 软件要求
- Python 3.8+ 
- Git
- OpenClaw Framework

### 2. 安装步骤

#### 步骤1: 克隆项目
```bash
git clone <项目地址>
cd water-knowledge-assistant
```

#### 步骤2: 创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 步骤3: 安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤4: 配置环境变量
创建 `.env` 文件并添加以下内容：
```env
# OpenAI API Key（用于嵌入模型）
OPENAI_API_KEY=your-openai-api-key

# Tavily API Key（用于实时更新）
TAVILY_API_KEY=your-tavily-api-key
```

#### 步骤5: 配置路径
根据实际情况修改 `config/paths.yaml` 文件中的路径配置：
```yaml
source_paths:
  knowledge_base: D:\code\openclaw_lakeskill\outerfiles\  # 知识库源目录

workspace_paths:
  root: D:\code\openclaw_lakeskill\  # 工作目录
  knowledge_base: D:\code\openclaw_lakeskill\files\  # 知识库存储目录
  vector_store: D:\code\openclaw_lakeskill\water-knowledge-assistant\vector_store\  # 向量存储目录
```

### 3. 初始化

#### 步骤1: 导入知识库
```bash
python scripts/knowledge_base_import.py
```

#### 步骤2: 构建向量索引
```bash
python scripts/vector_index_builder.py
```

#### 步骤3: 配置Cron任务（可选）
```bash
# 在Linux/macOS上
crontab -e
# 添加以下内容
0 2 * * * python /path/to/water-knowledge-assistant/scripts/knowledge_base_import.py
0 3 * * * python /path/to/water-knowledge-assistant/scripts/tavily_update.py
0 4 * * * python /path/to/water-knowledge-assistant/scripts/vector_index_builder.py
0 1 * * 0 python /path/to/water-knowledge-assistant/audit/log_cleanup.py

# 在Windows上使用任务计划程序创建类似的定时任务
```

### 4. 部署到OpenClaw平台

#### 步骤1: 打包Skill
```bash
# 创建zip包
zip -r water-knowledge-assistant.zip *
```

#### 步骤2: 上传到OpenClaw平台
1. 登录OpenClaw平台
2. 进入Skill管理页面
3. 点击"上传新Skill"
4. 选择打包好的zip文件
5. 填写基本信息并提交

#### 步骤3: 配置权限和触发器
1. 在Skill详情页面配置权限
2. 设置触发关键词
3. 配置工具调用权限

### 5. 验证安装

执行以下命令验证安装是否成功：

```bash
# 测试知识库导入
python scripts/knowledge_base_import.py

# 测试向量索引构建
python scripts/vector_index_builder.py
```

如果命令执行成功且没有错误信息，则安装完成。