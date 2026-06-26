# Second Brain Triage

智能信息分诊系统，基于Tiago Forte的PARA方法（Projects/Areas/Resources/Archive）自动分类和优先级排序。

## 功能特点

- 🤖 **智能分类**：自动识别内容类型并分类到PARA体系
- ⚡ **紧急度评分**：多维度算法评估处理优先级
- 🔗 **关联检测**：发现内容间的相似性和关联关系
- 📊 **批量处理**：支持批量分诊和导出报告
- 📝 **多种格式**：支持JSON/Markdown/CSV导出

## 快速开始

```bash
# 安装
cd second-brain-triage
npm install

# 运行测试
npm test

# 使用CLI
node scripts/triage.js "TODO: 完成项目报告"
node scripts/triage.js --file ./note.txt --format markdown
```

## 使用示例

### JavaScript API

```javascript
const { SecondBrainTriage } = require('./src');

const triage = new SecondBrainTriage();

// 分诊单个内容
const result = triage.triage('TODO: 完成项目报告，截止本周五');

console.log(result.summary);
// {
//   title: "完成项目报告，截止本周五",
//   type: "task",
//   category: "项目",
//   urgency: "高紧急",
//   urgencyScore: 8,
//   action: "今天处理：建议在24小时内完成"
// }

// 批量分诊
const results = triage.triageBatch([
  '学习React Hooks',
  'https://github.com/user/repo',
  'TODO: 修复登录bug',
]);

// 导出报告
const report = triage.exportReport(results, 'markdown');
```

### CLI使用

```bash
# 分析单个内容
node scripts/triage.js "需要处理的文本内容"

# 从文件读取
node scripts/triage.js --file ./notes.txt --format markdown

# 批量分析
node scripts/triage.js --batch ./items.json --output report.md --format markdown
```

## PARA分类说明

| 分类 | 说明 | 示例 |
|------|------|------|
| **Projects** | 有明确目标和截止日期的项目 | 开发新功能、完成报告 |
| **Areas** | 长期负责的标准和责任领域 | 健康管理、技能提升 |
| **Resources** | 感兴趣的主题和参考资料 | 技术文章、学习笔记 |
| **Archive** | 已完成或不活跃的内容 | 已完成项目、历史记录 |
| **Inbox** | 待分类的临时存储 | 无法确定分类的内容 |

## 紧急度等级

| 分数 | 等级 | 建议 |
|------|------|------|
| 9-10 | 极紧急 | 立即处理 |
| 7-8 | 高紧急 | 24小时内完成 |
| 5-6 | 中等 | 本周内安排 |
| 3-4 | 低紧急 | 可以延后 |
| 1-2 | 不急 | 存档备查 |

## 项目结构

```
second-brain-triage/
├── src/
│   ├── content-analyzer.js     # 内容分析器
│   ├── para-classifier.js      # PARA分类器
│   ├── urgency-scorer.js       # 紧急度评分
│   ├── relatedness-detector.js # 关联性检测
│   └── index.js                # 主入口
├── scripts/
│   └── triage.js               # CLI工具
├── test/
│   └── test.js                 # 测试套件
├── SKILL.md                    # 技能文档
├── README.md                   # 本文件
└── package.json
```

## 算法说明

### 紧急度评分维度

1. **时间敏感性** (30%)：截止日期、时间关键词
2. **行动需求** (25%)：必须/计划/可能等行动词
3. **后果** (20%)：不处理的潜在影响
4. **上下文信号** (15%)：阻塞、外部依赖等
5. **用户偏好** (10%)：可配置的优先级

### 关联性检测

- 标签相似度（Jaccard系数）
- 文本相似度（余弦相似度）
- 语义相似度（基于语义组）
- 类型匹配

## 许可证

MIT