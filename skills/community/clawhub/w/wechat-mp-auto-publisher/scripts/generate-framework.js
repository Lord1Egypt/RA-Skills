#!/usr/bin/env node

/**
 * 生成文章框架
 * 
 * 用法：node scripts/generate-framework.js "文章主题"
 * 输出：examples/framework.md
 */

const fs = require('fs');
const path = require('path');

const TEMPLATES = {
  tutorial: `
## 引言
- 痛点场景描述
- 传统方案的不足
- 本文方案优势
- 学完的效果

## 前置知识
- 基础要求
- 环境准备
- 预计时间

## 核心概念
- 术语解释
- 原理简述
- 适用场景

## 实战步骤
### 步骤 1
- 操作说明
- 代码示例
- 注意事项

### 步骤 2
- 操作说明
- 代码示例
- 常见问题

### 步骤 3
- 操作说明
- 代码示例
- 验证方法

## 进阶技巧
- 性能优化
- 最佳实践
- 避坑指南

## 完整案例
- 案例背景
- 完整代码
- 运行结果

## 总结
- 核心要点
- 下一步建议
- 相关资源
`,
  product: `
## 引言
- 行业背景
- 用户痛点
- 为什么需要

## 产品简介
- 是什么
- 谁开发的
- 核心定位

## 核心功能
### 功能 1
- 解决问题
- 怎么用
- 效果

### 功能 2
- 解决问题
- 怎么用
- 效果

## 对比分析
| 维度 | 本产品 | 方案 A |
|------|--------|--------|
| 价格 | | |
| 易用性 | | |

## 快速上手
- 安装注册
- 基础配置
- 第一个任务

## 适用场景
- ✅ 适合的情况
- ❌ 不适合的情况

## 总结
- 适合谁用
- 核心价值
- 获取方式
`,
  general: `
## 引言
- 背景痛点
- 要解决的问题
- 预期收获

## 核心内容
### 要点 1
- 详细说明
- 示例案例

### 要点 2
- 详细说明
- 示例案例

### 要点 3
- 详细说明
- 示例案例

## 实战应用
- 使用场景
- 操作步骤
- 注意事项

## 常见问题
- Q1 → A
- Q2 → A
- Q3 → A

## 总结
- 核心要点
- 下一步行动
- 相关资源
`,
};

function diagnoseType(topic) {
  const keywords = {
    tutorial: ['教程', '指南', '怎么', '如何', '步骤', '入门', '学习', '使用'],
    product: ['介绍', '推荐', '工具', '产品', '对比', '评测'],
  };
  let maxScore = 0, type = 'general';
  for (const [t, words] of Object.entries(keywords)) {
    const score = words.reduce((s, w) => s + (topic.includes(w) ? 1 : 0), 0);
    if (score > maxScore) { maxScore = score; type = t; }
  }
  return type;
}

const topic = process.argv[2];
if (!topic) {
  console.log('❌ 用法：node generate-framework.js "文章主题"');
  process.exit(1);
}

const type = diagnoseType(topic);
const template = TEMPLATES[type] || TEMPLATES.general;
const framework = `# ${topic}\n${template}\n`;

const outputDir = path.join(__dirname, '..', 'examples');
const outputFile = path.join(outputDir, 'framework.md');
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(outputFile, framework);

console.log('✅ 框架已生成:', outputFile);
console.log('\n📋 框架预览:');
console.log(framework);
