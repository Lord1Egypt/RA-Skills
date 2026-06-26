#!/usr/bin/env node

/**
 * 闲鱼搜索技能 - 测试文件
 */

const { parseSearchConfig } = require('./utils');
const { SearchConfig } = require('./search');
const { generateFullReport } = require('./templates');

// 测试用例
const testCases = [
  {
    input: '帮我找闲鱼上的 MacBook Air M1 预算 2300',
    expected: {
      keyword: 'MacBook Air M1',
      budget: 2300,
    },
  },
  {
    input: '搜索二手 iPhone 13 预算 3000 电池 85 以上',
    expected: {
      keyword: 'iPhone 13',
      budget: 3000,
      batteryMin: 85,
    },
  },
  {
    input: '闲鱼上有没有 9 成新的 PS5',
    expected: {
      keyword: 'PS5',
      condition: '9 成新',
    },
  },
  {
    input: '帮我看看闲鱼相机 预算 5000 北京',
    expected: {
      keyword: '相机',
      budget: 5000,
      location: '北京',
    },
  },
];

console.log('🧪 开始测试闲鱼搜索技能...\n');

let passed = 0;
let failed = 0;

testCases.forEach((testCase, index) => {
  console.log(`测试 ${index + 1}: ${testCase.input}`);
  
  const config = parseSearchConfig(testCase.input);
  
  let testPassed = true;
  for (const [key, expected] of Object.entries(testCase.expected)) {
    if (config[key] !== expected) {
      console.log(`  ❌ ${key}: 期望 "${expected}", 得到 "${config[key]}"`);
      testPassed = false;
    }
  }
  
  if (testPassed) {
    console.log(`  ✅ 通过\n`);
    passed++;
  } else {
    console.log(`  ❌ 失败\n`);
    failed++;
  }
});

console.log('─'.repeat(50));
console.log(`测试结果：${passed} 通过，${failed} 失败`);

// 测试 SearchConfig
console.log('\n📋 测试 SearchConfig 类...');
const searchConfig = new SearchConfig({
  keyword: 'MacBook Air M1',
  budget: 2300,
  batteryMin: 85,
});

console.log(`搜索关键词：${searchConfig.getSearchKeywords()}`);
console.log(`搜索 URL: ${searchConfig.getSearchUrl()}`);

// 测试模板
console.log('\n📄 测试模板生成...');
const mockProducts = [
  {
    title: 'MacBook Air M1 2020',
    price: 2300,
    location: '北京',
    battery: '89%',
    credit: '百分百好评',
    url: 'https://www.goofish.com/item?id=123',
    highlights: ['电池健康', '无拆修'],
  },
  {
    title: 'MacBook Air M1 2020',
    price: 2150,
    location: '山东',
    battery: '循环 8 次',
    credit: '卖家信用极好',
    url: 'https://www.goofish.com/item?id=456',
    highlights: ['电池超新'],
  },
];

const report = generateFullReport(searchConfig, mockProducts, 'laptop');
console.log('\n生成的报告预览：');
console.log(report.substring(0, 500) + '...\n');

console.log('✅ 所有测试完成！');
