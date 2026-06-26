/**
 * SkillForge Skill 测试
 */

import {
  detectCapabilityGap,
  formatServiceList,
  formatInvocationResult,
  CAPABILITY_KEYWORDS
} from './handler.js';

// 测试能力检测
function testDetectCapabilityGap() {
  console.log('\n=== 测试能力检测 ===\n');
  
  const testCases = [
    { task: '帮我生成一张猫的图片', expected: ['image_generation'] },
    { task: '把这段文字转成语音', expected: ['speech_synthesis'] },
    { task: '翻译这段话成英文', expected: ['text_translation'] },
    { task: '帮我分析这份数据', expected: ['data_analysis'] },
    { task: '提取这个PDF里的文字', expected: ['pdf_processing'] },
    { task: '识别这张图片里的文字', expected: ['ocr'] },
    { task: '今天天气怎么样', expected: ['weather_data'] },
    { task: '查一下苹果的股价', expected: ['stock_data'] },
    { task: '帮我写一个函数', expected: [] }, // 本地能力
    { task: '生成一个二维码', expected: ['qrcode_generation'] },
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const { task, expected } of testCases) {
    const result = detectCapabilityGap(task);
    const match = JSON.stringify(result.sort()) === JSON.stringify(expected.sort());
    
    if (match) {
      console.log(`✅ "${task}"`);
      console.log(`   检测到: ${result.join(', ') || '无'}`);
      passed++;
    } else {
      console.log(`❌ "${task}"`);
      console.log(`   预期: ${expected.join(', ') || '无'}`);
      console.log(`   实际: ${result.join(', ') || '无'}`);
      failed++;
    }
  }
  
  console.log(`\n结果: ${passed} 通过, ${failed} 失败\n`);
  return failed === 0;
}

// 测试服务列表格式化
function testFormatServiceList() {
  console.log('\n=== 测试服务列表格式化 ===\n');
  
  const services = [
    {
      id: 'svc_1',
      name: 'DALL-E 3',
      description: '高质量图像生成',
      category: 'image',
      price: 0.04,
      priceUnit: 'per_call',
      rating: 4.8,
      calls: 12500,
      developer: 'OpenAI'
    },
    {
      id: 'svc_2',
      name: 'Stable Diffusion',
      description: '开源图像生成模型',
      category: 'image',
      price: 0.02,
      priceUnit: 'per_call',
      rating: 4.5,
      calls: 8500,
      developer: 'Stability AI'
    },
    {
      id: 'svc_3',
      name: 'Free OCR',
      description: '免费文字识别',
      category: 'utility',
      price: 0,
      priceUnit: 'free',
      rating: 4.2,
      calls: 50000,
      developer: '社区'
    }
  ];
  
  const formatted = formatServiceList(services);
  console.log(formatted);
  
  // 检查关键字
  const checks = [
    { name: '包含服务名', test: formatted.includes('DALL-E 3') },
    { name: '包含价格', test: formatted.includes('$0.0400') || formatted.includes('免费') },
    { name: '包含评分', test: formatted.includes('⭐') },
    { name: '包含开发者', test: formatted.includes('OpenAI') },
  ];
  
  let allPassed = true;
  for (const { name, test } of checks) {
    if (test) {
      console.log(`✅ ${name}`);
    } else {
      console.log(`❌ ${name}`);
      allPassed = false;
    }
  }
  
  // 测试空列表
  const emptyFormatted = formatServiceList([]);
  console.log('\n空列表:', emptyFormatted);
  
  return allPassed;
}

// 测试调用结果格式化
function testFormatInvocationResult() {
  console.log('\n=== 测试调用结果格式化 ===\n');
  
  // 成功结果
  const successResult = {
    success: true,
    data: { image_url: 'https://example.com/image.png' },
    billing: {
      charged: 0.04,
      remaining: 12.50
    },
    meta: {
      requestId: 'req_xxx',
      serviceId: 'svc_xxx',
      serviceName: 'DALL-E 3',
      duration: 2500
    }
  };
  
  console.log('成功结果:');
  console.log(formatInvocationResult(successResult));
  
  // 免费结果
  const freeResult = {
    success: true,
    data: { text: '识别结果' },
    billing: {
      charged: 0,
      remaining: 12.50
    },
    meta: {
      serviceName: 'Free OCR',
      duration: 500
    }
  };
  
  console.log('\n免费结果:');
  console.log(formatInvocationResult(freeResult));
  
  // 失败结果
  const failResult = {
    success: false,
    error: {
      code: 'INSUFFICIENT_BALANCE',
      message: '余额不足'
    }
  };
  
  console.log('\n失败结果:');
  console.log(formatInvocationResult(failResult));
  
  return true;
}

// 测试能力关键词覆盖
function testCapabilityKeywords() {
  console.log('\n=== 测试能力关键词覆盖 ===\n');
  
  const capabilities = Object.keys(CAPABILITY_KEYWORDS);
  console.log(`共有 ${capabilities.length} 种能力:\n`);
  
  for (const cap of capabilities) {
    const keywords = CAPABILITY_KEYWORDS[cap];
    const chineseKw = keywords.filter(k => /[\u4e00-\u9fa5]/.test(k));
    const englishKw = keywords.filter(k => !/[\u4e00-\u9fa5]/.test(k));
    
    console.log(`${cap}:`);
    if (chineseKw.length > 0) {
      console.log(`  中文: ${chineseKw.join(', ')}`);
    }
    if (englishKw.length > 0) {
      console.log(`  英文: ${englishKw.slice(0, 3).join(', ')}`);
    }
  }
  
  return true;
}

// 运行所有测试
function runTests() {
  console.log('🧪 SkillForge Skill 测试套件\n');
  console.log('='.repeat(50));
  
  const results = [
    testDetectCapabilityGap(),
    testFormatServiceList(),
    testFormatInvocationResult(),
    testCapabilityKeywords()
  ];
  
  console.log('\n' + '='.repeat(50));
  console.log('\n📊 测试总结\n');
  
  const passed = results.filter(r => r).length;
  const failed = results.filter(r => !r).length;
  
  console.log(`总计: ${results.length} 个测试套件`);
  console.log(`✅ 通过: ${passed}`);
  console.log(`❌ 失败: ${failed}`);
  
  if (failed === 0) {
    console.log('\n🎉 所有测试通过!\n');
  } else {
    console.log('\n⚠️ 部分测试失败，请检查\n');
  }
  
  process.exit(failed > 0 ? 1 : 0);
}

runTests();