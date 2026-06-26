# Talk Analyzer - AI 对话分析技能

## 技能概述

Talk Analyzer 是一个强大的 AI 驱动的商务对话分析工具，能够自动从会议记录、销售电话、客户支持对话中提取关键信息、行动项和策略建议。

## 核心能力

### 1. 多类型对话分析
- **会议分析** - 自动提取会议要点、决策和待办事项
- **销售分析** - 识别客户异议、购买信号和跟进策略
- **客服分析** - 评估服务质量、客户满意度和问题解决效率
- **谈判分析** - 分析双方立场、让步和谈判策略
- **面试分析** - 评估候选人资质和文化契合度
- **通用分析** - 适用于任何类型的对话内容

### 2. 智能提取功能
- **对话摘要** - 生成 2-3 句话的精炼总结
- **关键要点** - 自动提取讨论的主要话题和结论
- **行动项提取** - 识别任务、负责人和截止日期
- **决策记录** - 记录重要决定及其理由
- **情感分析** - 评估对话情绪和参与度
- **发言者画像** - 分析每个参与者的贡献和风格

### 3. 销售专用功能
- **异议识别** - 自动识别客户提出的顾虑（价格、时间、功能等）
- **购买信号** - 发现客户的购买意向和紧迫性
- **机会点** - 识别痛点、预算信号和决策权
- **跟进建议** - 基于对话内容生成下一步行动策略

### 4. AI 引擎支持
- **Claude (Anthropic)** - 主要分析引擎，提供深度理解
- **OpenAI GPT** - 备选引擎，提供多样化分析
- **本地 LLM** - 支持私密对话的本地处理

## 使用场景

### 场景 1: 团队会议总结
**输入**: 1小时的团队会议记录
**输出**:
- 会议摘要
- 5-10 个关键决策点
- 每个人的待办事项（含截止日期）
- 需要后续讨论的话题

**价值**: 节省 30 分钟的会议纪要整理时间

### 场景 2: 销售电话分析
**输入**: 销售通话文字记录
**输出**:
- 客户需求和痛点
- 提出的异议及严重程度
- 购买信号和时间线
- 跟进策略建议

**价值**: 提高销售转化率 20-30%

### 场景 3: 客服质量评估
**输入**: 客服对话记录
**输出**:
- 客户满意度评分
- 问题解决质量
- 客服沟通技巧评估
- 改进建议

**价值**: 优化客服培训，提升客户满意度

### 场景 4: 批量对话分析
**输入**: 多个对话文件
**输出**:
- 每个对话的独立分析
- 跨对话的模式识别
- 趋势分析和洞察

**价值**: 发现系统性问题和机会

## 技能参数

### 必需参数
- `input` - 对话文本文件路径
- `type` - 分析类型（meeting/sales/support/negotiation/interview/general）

### 可选参数
- `sentiment` - 启用情感分析（布尔值）
- `speakers` - 参与者姓名列表（逗号分隔）
- `focus` - 关注的特定方面（如 "pricing,timeline,objections"）
- `detailed` - 生成详细分析报告（布尔值）
- `output` - 输出文件路径
- `format` - 输出格式（json/markdown）

## 使用示例

### 基础用法
```bash
openclaw-talk analyze \
  --input meeting.txt \
  --type meeting
```

### 高级用法
```bash
openclaw-talk analyze \
  --input sales-call.txt \
  --type sales \
  --sentiment \
  --speakers "John,Sarah" \
  --focus "objections,pricing,timeline" \
  --detailed \
  --output report.json
```

### 批量分析
```bash
openclaw-talk batch \
  --config batch-config.json \
  --output-dir ./reports/
```

### 对话对比
```bash
openclaw-talk compare \
  --inputs "call1.txt,call2.txt,call3.txt" \
  --type sales \
  --output comparison.md
```

## 输出示例

### JSON 格式输出
```json
{
  "type": "meeting",
  "summary": "团队讨论了 Q2 移动应用发布计划，确定4月底上线核心功能，离线模式推迟到5月。",
  "key_points": [
    "移动应用开发进度 70%",
    "推送通知需要 2 周，离线模式需要 4-5 周",
    "决定先发布核心功能，后续迭代添加离线模式",
    "批准营销预算 $30,000"
  ],
  "action_items": [
    {
      "task": "设置 50-100 人的 beta 测试计划",
      "owner": "Bob",
      "deadline": "明天",
      "priority": "high"
    },
    {
      "task": "制定营销策略并分享",
      "owner": "Charlie",
      "deadline": "周五",
      "priority": "high"
    }
  ],
  "decisions": [
    {
      "decision": "同时发布 iOS 和 Android 版本",
      "made_by": "Alice",
      "rationale": "用户群体平均分布"
    }
  ],
  "sentiment": {
    "overall": "positive",
    "participants": {
      "Alice": {"sentiment": "positive", "engagement_level": "high"},
      "Bob": {"sentiment": "neutral", "engagement_level": "medium"},
      "Charlie": {"sentiment": "positive", "engagement_level": "high"}
    }
  }
}
```

## 技术要求

### 环境要求
- Node.js 18.0.0 或更高版本
- npm 或 pnpm 包管理器

### API 密钥
需要以下至少一个 AI 服务的 API 密钥：
- Anthropic Claude API Key
- OpenAI API Key
- 或本地 LLM 服务端点

### 输入格式
- 支持纯文本文件 (.txt)
- 推荐格式: 每个发言者独立一行
- 建议最小长度: 50 字符
- 支持自动语言检测

## 性能指标

- **分析速度**: 1000 字对话约 10-20 秒
- **准确率**: 关键信息提取准确率 > 90%
- **支持语言**: 主要支持中文和英文
- **最大输入**: 单次分析最多 100,000 字符

## 优势特点

1. **高度自动化** - 无需人工整理，一键生成结构化报告
2. **多场景适配** - 6 种预设分析类型，覆盖常见商务场景
3. **深度洞察** - 不仅提取信息，还提供策略建议
4. **灵活配置** - 丰富的参数支持定制化分析
5. **批量处理** - 支持同时分析多个对话文件
6. **隐私保护** - 支持本地 LLM，敏感对话不出本地

## 典型工作流

1. **收集对话** - 从会议、电话录音转文字
2. **配置分析** - 选择分析类型和关注点
3. **执行分析** - 运行 AI 分析引擎
4. **查看结果** - 获取结构化报告
5. **采取行动** - 基于洞察执行后续任务

## 集成能力

### 命令行集成
```bash
# 在脚本中使用
./analyze.sh analyze --input "$MEETING_FILE" --type meeting > report.json
```

### 编程接口
```typescript
import { ConversationAnalyzer } from 'openclaw-talk-analyzer';

const analyzer = new ConversationAnalyzer({...});
const result = await analyzer.analyze(input, options);
```

### 批处理
```bash
# 定时任务分析每日会议
crontab -e
0 18 * * * /path/to/openclaw-talk batch --config daily-config.json
```

## 更新计划

### v1.1.0 (即将推出)
- 实时音频转录集成
- PDF 报告导出
- Web 可视化仪表板

### v1.2.0 (规划中)
- 多语言支持扩展
- CRM 系统集成（Salesforce, HubSpot）
- 团队协作功能

## 支持和文档

- **完整文档**: https://github.com/ZhenRobotics/openclaw-talk-analyzer
- **快速开始**: 见项目 QUICKSTART.md
- **示例文件**: 包含真实场景示例
- **问题反馈**: GitHub Issues

## 许可证

MIT License - 开源免费使用

---

**让 AI 帮你从对话中提取价值，把时间用在更重要的事情上！**
