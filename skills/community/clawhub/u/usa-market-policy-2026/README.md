# usa-policy-query

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://clawhub.ai/skills/usa-policy-query)
[![DeepSeek v4](https://img.shields.io/badge/DeepSeek-v4-10a37f)](https://deepseek.com)
[![惠迈智能体](https://img.shields.io/badge/惠迈智能体-三层架构-red)](https://huimai.ai)

美国市场政策查询Skill - 提供美国市场政策、法规、投资环境的智能查询和分析

## 🌟 核心特性

### 🚀 DeepSeek v4驱动
- 基于DeepSeek v4最新AI模型
- 智能政策分析和趋势预测
- 多维度风险评估

### 🤖 惠迈智能体协作
- **数据智能体层**：实时采集美国政策数据
- **分析智能体层**：DeepSeek v4驱动的智能分析  
- **应用智能体层**：用户友好的查询接口

### 🌐 多语言支持
- 中文（简体）
- 英文（美国）
- 自动语言检测和切换

### 🔧 数据源可配置
- 灵活配置不同数据源API
- 支持自定义数据源集成
- 环境变量管理敏感信息

## 📦 安装

### 通过ClawHub安装
```bash
clawhub install usa-policy-query
```

### 手动安装
```bash
npm install usa-policy-query
```

## 🚀 快速开始

```javascript
const PolicyQuery = require('usa-policy-query');

// 初始化
const skill = new PolicyQuery({
  language: 'zh-CN', // 或 'en-US'
  dataSources: {
    investment: process.env.INVESTMENT_API_KEY || '[请替换为您的API Key]',
    trade: process.env.TRADE_API_KEY || '[请替换为您的API Key]'
  }
});

// 查询政策
async function example() {
  const policies = await skill.queryPolicies('investment');
  console.log(`找到 ${policies.totalPolicies} 条投资政策`);
  
  const analysis = await skill.analyzeInvestmentEnvironment();
  console.log(`投资环境评分: ${analysis.score}/100`);
}

example();
```

## 🔒 安全配置

### 推荐使用环境变量
```bash
# .env文件
INVESTMENT_API_KEY=your_api_key_here
TRADE_API_KEY=your_trade_api_key_here
```

### 配置文件示例
```javascript
// config.js
module.exports = {
  language: 'zh-CN',
  dataSources: {
    investment: process.env.INVESTMENT_API_KEY,
    trade: process.env.TRADE_API_KEY,
    tax: process.env.TAX_API_KEY,
    labor: process.env.LABOR_API_KEY,
    environment: process.env.ENVIRONMENT_API_KEY
  }
};
```

## 🎯 在OpenClaw中使用

### 传统方式
```
@agent 查询美国最新的投资政策
@agent 分析美国投资环境
```

### 惠迈智能体协作模式（推荐）
```
@惠迈智能体 如何在美国开展业务？
@惠迈智能体 监控美国政策变化
@惠迈智能体 分析美国投资风险
```

## 📊 功能列表

| 功能 | 描述 | 支持语言 |
|------|------|----------|
| 政策查询 | 查询美国各类政策 | 中英文 |
| 投资环境分析 | 分析美国投资环境 | 中英文 |
| 多语言切换 | 自动/手动切换界面语言 | 中英文 |
| 数据源配置 | 灵活配置数据源API | - |
| 缓存管理 | 智能缓存提高性能 | - |

## 🔧 开发

### 运行测试
```bash
cd node_modules/usa-policy-query
npm test
```

### 构建
```bash
npm run build
```

## 📝 API参考

### PolicyQuery(config)
初始化Skill实例。

### queryPolicies(category, options)
查询特定类别的政策。

### analyzeInvestmentEnvironment(region)
分析投资环境。

### setLanguage(language)
切换界面语言。

### getSupportedLanguages()
获取支持的语言列表。

### clearCache()
清理缓存数据。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 支持

如有问题，请：
1. 查看[文档](https://docs.huimai.ai)
2. 提交[Issue](https://github.com/huimai-agents/issues)
3. 联系技术支持

---
**惠迈智能体：让全球业务变得简单** 🚀
