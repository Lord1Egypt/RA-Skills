# Today Task Skill

通用任务结果推送器，当任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。

## ⚠️ 重要提示：数据存储说明

**本技能会在本地创建运行记录文件：**

- **日志目录** (`logs/`): 包含脱敏的运行信息，用于故障排查
- **推送记录目录** (`push_records/`): 可选保存的任务推送记录

**隐私保护措施：**

- 运行信息在日志中记录用于调试。
- 用户可通过配置控制是否保存推送记录
- 所有文件仅存储在用户本地设备

**用户责任：** 请定期检查和管理这些本地文件，确保符合您的隐私要求。

## 🚀 快速开始

### 安装依赖

```bash
# 确保已安装Python 3.7+
python --version

# 安装依赖
pip install requests
```

### 基本使用

```bash
# 1. 确保已配置身份验证和推送URL

# 2. 推送任务结果（会自动检查版本更新）
python scripts/task_push.py --name "今日新闻" --content "# 今日新闻\n\n- 新闻1: ..." --result "已完成"

# 3. 或使用JSON文件
python scripts/task_push.py --data task_data.json

# 注意：运行时会自动检查技能更新，如有新版本会显示通知
# 更新命令：clawhub update today-task
```

## 📋 数据格式

### 推送数据格式

```json
{
    "userId": "123455", 
    "appPackage": "com.huawei.hag",
    "msgContent": [
    // 消息内容数组
    {
      "scheduleTaskId": "string", // 周期性任务ID（对于周期性任务此ID需要保持一致）
      "scheduleTaskName": "string", // 任务名称
      "summary": "string", // 任务摘要
      "result": "string", // 执行结果
      "content": "string", // 详细内容（markdown格式）
      "source": "string", // 来源（OpenClaw）
      "taskFinishTime": "number" // 任务完成时间戳（秒）
    }
  ]
}
```

**注意**：推送服务的请求头，x-trace-id 是必填的。

## ⏰ 时间戳使用指南

### 重要提醒

**避免使用错误的时间戳获取方式，这可能导致推送时间显示不正确！**

#### ❌ 错误方式（不要使用）

```powershell
# PowerShell 中的错误方式（可能产生时区问题）
[int][double]::Parse((Get-Date -UFormat %s))
[int](Get-Date -UFormat %s)
```

#### ✅ 正确方式

##### Python（本技能使用的方式）

```python
import time
timestamp = int(time.time())  # UTC 时间戳，推荐使用
```

##### PowerShell（其他脚本中使用）

```powershell
# 正确！使用 UTC 时间，避免时区问题
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
```

**避免 json、PowerShell、python 使用不一样的编码，这可能导致内容乱码，中文显示?**

##### PowerShell 需要设置控制台编码为 UTF-8

```powershell
# 正确设置控制台编码为UTF-8
chcp 65001
```

##### 本技能的时间戳处理

本技能自动处理时间戳：

- 使用 Python 的 `time.time()` 获取 UTC 时间戳
- 自动验证时间戳合理性
- 确保与负一屏服务时间一致

### 时区说明

- **负一屏服务使用 UTC 时间戳**
- 本地时间可能因时区设置不同而产生误差
- 始终使用 **UTC 时间** 避免时区问题
- 中国时区（UTC+8）的用户需要注意时间转换

### 验证时间戳

如果你在其他脚本中集成本技能，请验证时间戳：

```python
# 验证时间戳是否在合理范围内
import time

def validate_timestamp(timestamp):
    min_valid = 1609459200  # 2021-01-01
    max_valid = int(time.time()) + 31536000  # 当前时间 + 1年
    return min_valid <= timestamp <= max_valid

# 使用示例
current_ts = int(time.time())
if validate_timestamp(current_ts):
    print(f"时间戳有效: {current_ts}")
else:
    print(f"时间戳可能有问题: {current_ts}")
```

### 常见问题

1. **时间显示不对**：检查是否使用了本地时间而非 UTC 时间
2. **时间戳为 0 或负数**：时间戳获取方式错误
3. **时间差 8 小时**：中国时区（UTC+8）未正确转换

### 最佳实践

1. **统一使用 UTC 时间**：所有时间戳都使用 UTC
2. **验证时间戳**：在关键操作前验证时间戳有效性
3. **记录时间源**：明确记录时间戳的来源和时区
4. **使用本技能的工具**：本技能已正确处理时间戳，无需额外处理

### 输入数据格式

```json
// 格式1：完整格式（推荐）
{
  "schedule_task_id": "周期性任务ID", // 必填，对于周期性任务此ID需要保持一致
  "task_name": "任务名称", // 必填
  "task_result": "执行结果", // 必填，如"任务已完成"
  "task_content": "# Markdown内容" // 必填，markdown格式内容
}

// 注意：content 字段中的换行符
// 正确：使用实际的换行符 \n
// 错误：使用转义的换行符 \\n
```

## 🔍 内容字段问题排查

### 问题现象

content 字段显示 `\n\n` 而不是实际的换行。

### 可能原因

1. **JSON 双重序列化**：数据被多次 JSON 序列化
2. **字符串转义错误**：手动转义了换行符
3. **数据源问题**：其他系统返回的数据已转义

### 诊断方法

#### 方法 1：使用诊断工具

```bash
# 诊断 JSON 文件
python scripts/diagnose_content.py your_data.json

# 诊断 JSON 字符串
python scripts/diagnose_content.py --json '{"task_content": "你的内容"}'
```

#### 方法 2：手动检查

```python
import json

# 检查数据
data = {"task_content": "你的内容"}
print(f"原始内容: {repr(data['task_content'])}")
print(f"实际内容: {data['task_content']}")

# 检查是否有转义的换行符
if '\\n' in data['task_content'] and '\n' not in data['task_content']:
    print("⚠️  发现转义的换行符 (\\\\n)")
```

### 解决方案

#### 方案 1：修复数据源

```python
# 在数据生成时避免转义
content = "第一行\n\n第二行"  # 正确：使用实际换行符
# content = "第一行\\n\\n第二行"  # 错误：使用转义换行符
```

#### 方案 2：修复已转义的数据

```python
# 如果数据已转义，修复它
if '\\n' in content:
    fixed_content = content.replace('\\n', '\n')
```

#### 方案 3：使用本技能的预处理

本技能已添加内容预处理功能，会自动处理转义的换行符。

### 预防措施

1. **统一数据生成**：所有数据源使用相同的序列化方式
2. **避免多重序列化**：不要对 JSON 字符串再次序列化
3. **测试验证**：生成数据后验证内容格式
4. **使用诊断工具**：定期检查数据质量

**注意**：输入数据中的身份验证应通过 OpenClaw 全局配置设置，不建议在输入数据中传递身份验证。

## 🔧 配置说明

### 本地配置文件 (config.json)

```json(注意这只是一个配置示例，使用的时候要使用skill里面的config.json文件)
{
  "timeout": 30,
  "max_content_length": 5000,
  "auto_generate_id": true,
  "default_result": "任务已完成",
  "log_level": "INFO",
  "save_records": true,
  "records_dir": "push_records",
  "max_records": 100,
  }
```

**重要说明**：

- 身份验证 (``) 必须通过 OpenClaw 全局配置设置


## 📖 使用示例

### 示例 1：命令行使用

```bash
# 基本使用
python scripts/task_push.py --name "天气报告" --content "# 天气报告\n\n- 温度: 23°C\n- 天气: 多云" --result "已完成"

# 使用JSON文件
python scripts/task_push.py --data task_result.json

# 试运行（不实际推送）
python scripts/task_push.py --name "测试" --content "测试内容" --dry-run

# 详细输出
python scripts/task_push.py --name "测试" --content "测试内容" --verbose
```

### 示例 2：JSON 文件

创建 `task_result.json`:

```json
{
  "task_name": "任务名称",
  "task_content": "# 任务报告\n\n## 执行结果\n\n任务执行成功，以下是详细内容...\n\n---\n\n*生成时间: 2024-03-27 10:30:00*",
  "task_result": "任务已完成",
  "task_id": "task_20240327_1030"
}
```

注意：task_content 要是 markdown 格式的

运行：

```bash
python scripts/task_push.py --data task_result.json
```

### 示例 3：Python 代码集成

```python
from task_pusher import TaskPusher

# 初始化推送器
pusher = TaskPusher()

# 准备任务数据
task_data = {
    "task_name": "数据分析报告",
    "task_content": "# 数据分析报告\n\n## 关键指标\n\n| 指标 | 数值 | 状态 |\n|------|------|------|\n| 完成率 | 95% | ✅ |\n| 平均用时 | 2.5分钟 | ⏱️ |\n| 错误率 | 0.5% | ⚠️ |\n\n## 详细分析\n\n1. 数据质量良好\n2. 处理速度正常\n3. 建议优化存储结构\n\n---\n\n*报告生成时间: 2024-03-27 11:00:00*",
    "task_result": "分析完成",
    "task_id": "analysis_20240327_1100"
}

注意：task_content要是markdown格式的

# 推送结果
result = pusher.push(task_data)
print(f"推送结果: {result['success']}")
```

## 🎨 Markdown 内容规范

### 标题层级

```markdown
# 主标题 (Subtitle_L, 18px, Bold)

## 一级标题 (Body_L, 16px, Bold)

### 二级标题 (Body_M, 14px, Bold)
```

### 文本样式

```markdown
**粗体文本** - 用于强调
_斜体文本_ - 用于次要强调
`代码文本` - 用于代码或术语
```

### 列表

```markdown
- 无序列表项 1
- 无序列表项 2
  - 子列表项

1. 有序列表项 1
2. 有序列表项 2
```

### 表格

```markdown
| 列 1   | 列 2   | 列 3   |
| ------ | ------ | ------ |
| 数据 1 | 数据 2 | 数据 3 |
| 数据 4 | 数据 5 | 数据 6 |
```

### 分割线

```markdown
--- # 使用三个减号
```

### 最佳实践模板

```markdown
# 任务名称

## 执行结果

✅ 任务已完成 / ❌ 任务失败

## 关键信息

- 项目 1: 结果描述
- 项目 2: 结果描述
- 项目 3: 结果描述

## 详细内容

这里是详细的任务执行结果...

## 数据统计

| 指标   | 数值   | 状态 |
| ------ | ------ | ---- |
| 完成率 | 100%   | ✅   |
| 用时   | 5 分钟 | ⏱️   |
| 准确率 | 98.5%  | 📊   |

## 建议与下一步

1. 建议 1
2. 建议 2
3. 建议 3

---

_生成时间: 2024-03-27 10:30:00_
_AI 生成内容，仅供参考_
```

## 📁 文件结构

```
today-task/
├── SKILL.md                    # 技能定义
├── README.md                   # 使用说明
├── config.example.json         # 配置文件示例
├── simple_example.json         # 简单示例文件
├── scripts/
│   ├── task_push.py           # 命令行入口
│   ├── task_pusher.py         # 推送器主类
│   ├── config.py              # 配置管理
│   ├── logger.py              # 日志工具
│   ├── hiboards_client.py     # 负一屏客户端
│   ├── simple_test.py         # 简单测试脚本
│   └── __init__.py
├── push_records/              # 推送记录（自动创建）
└── logs/                      # 日志文件（自动创建）
```

## 🔍 调试与故障排除

### 常见问题

1. **身份验证错误**

   ```
   错误: 缺少身份验证或身份验证无效
   解决方案:
     - 使用OpenClaw全局配置设置身份验证:
       
   ```

2. **网络连接失败**

   ```
   错误: 连接失败或超时
   解决方案:
     - 检查网络连接是否正常
     - 确认推送URL可访问: https://hag-drcn.op.dbankcloud.com/...
     - 检查是否有代理设置影响连接
     - 尝试使用备用URL
   ```

3. **配置缺失错误**

   ```
      解决方案:
          - 运行配置检查: openclaw config get skills.entries.today-task
     - 确保技能配置已正确加载
   ```

4. **数据格式错误**

   ```
   错误: JSON解析失败
   解决方案:
     - 使用--dry-run检查数据格式
     - 确保JSON格式有效
     - 检查任务数据是否符合要求格式
   ```

5. **数据存储疑问**
   ```
   疑问: 技能文档说"不存储敏感信息"，但为什么有本地日志和记录文件？
   解答:
     - "不存储敏感信息"指的是不存储完整的身份验证等敏感数据
     - 本地文件包含脱敏的运行记录，用于故障排查：
       * 日志文件: 包含脱敏信息（身份验证显示为 `Twe7***` 格式）
       * 推送记录: 可选保存，用于历史追踪（可通过配置关闭）
     - 用户控制:
       * 通过 `save_records` 配置项控制是否保存推送记录
       * 通过 `max_records` 配置项限制记录数量
       * 可定期清理 `logs/` 和 `push_records/` 目录
     - 所有存储均在用户本地设备，不外传
   ```

### 调试模式

```bash
# 启用详细日志
python scripts/task_push.py --name "测试" --content "内容" --verbose

# 试运行模式
python scripts/task_push.py --name "测试" --content "内容" --dry-run
```

### 查看日志

```bash
# 查看最新日志
tail -f logs/task_push_*.log

# 查看推送记录
ls -la push_records/
cat push_records/push_*.json
```

## 📝 更新日志

### v2.1 (2026-04-01)

- 新增自动版本更新检查功能
- 运行脚本时自动检查 ClawHub 上的最新版本
- 输出版本更新通知（不自动更新）
- 提供更新命令和注意事项说明

### v2.0 (2024-03-27)

- 重构为统一数据格式
- 支持标准 pushData 格式
- 简化配置和使用
- 改进错误处理和日志

### v1.0 (2024-03-26)

- 初始版本
- 支持多种任务类型
- 基础推送功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请：

1. **查看本文档**：特别是配置要求和常见问题部分
2. **检查日志文件**：查看 `logs/task_push_*.log` 获取详细错误信息
3. **验证配置**：运行 `openclaw config get skills.entries.today-task`
4. **测试配置**：使用 `--dry-run` 模式测试数据格式
5. **检查网络**：确保可以访问推送服务 URL

### 获取帮助

- 确保已按照"配置要求"部分正确设置身份验证和推送 URL
- 使用 `--verbose` 参数获取详细日志输出
- 检查推送记录目录 `push_records/` 查看历史推送状态

3. 提交 Issue
