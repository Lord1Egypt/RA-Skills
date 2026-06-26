#!/usr/bin/env node
/**
 * UTF-8编码工具测试脚本
 * 运行核心功能测试，不依赖外部API
 */

const { UTF8Encoder } = require('./utf8-encoder');
const encoder = new UTF8Encoder();
const fs = require('fs');
const path = require('path');

console.log('🧪 UTF-8编码工具 - 单元测试');
console.log('='.repeat(60));

// 测试结果收集
const testResults = [];

function runTest(name, testFn) {
  console.log(`\n📝 测试: ${name}`);
  try {
    const result = testFn();
    testResults.push({ name, passed: true, result });
    console.log('  ✅ 通过');
    return true;
  } catch (error) {
    testResults.push({ name, passed: false, error: error.message });
    console.log(`  ❌ 失败: ${error.message}`);
    return false;
  }
}

// 测试1: ensureUTF8 基本功能
runTest('ensureUTF8 - 普通字符串', () => {
  const text = '普通文本';
  const result = encoder.ensureUTF8(text);
  if (result !== text) throw new Error('普通字符串不应被修改');
  return result;
});

runTest('ensureUTF8 - Buffer输入', () => {
  const buffer = Buffer.from('Buffer测试', 'utf8');
  const result = encoder.ensureUTF8(buffer);
  if (result !== 'Buffer测试') throw new Error('Buffer转换错误');
  return result;
});

runTest('ensureUTF8 - 数字输入', () => {
  const result = encoder.ensureUTF8(123);
  if (result !== '123') throw new Error('数字转换错误');
  return result;
});

// 测试2: calculateUTF8ByteLength
runTest('calculateUTF8ByteLength - ASCII字符', () => {
  const text = 'Hello World';
  const byteLength = encoder.calculateUTF8ByteLength(text);
  if (byteLength !== text.length) throw new Error(`ASCII字符字节长度应为${text.length}, 实际为${byteLength}`);
  return byteLength;
});

runTest('calculateUTF8ByteLength - 中文字符', () => {
  const text = '中文';
  const byteLength = encoder.calculateUTF8ByteLength(text);
  // 每个中文字符UTF-8通常为3字节
  const expected = 6; // 2个字符 * 3字节
  if (byteLength !== expected) throw new Error(`中文字符字节长度应为${expected}, 实际为${byteLength}`);
  return byteLength;
});

runTest('calculateUTF8ByteLength - 混合字符', () => {
  const text = 'Hello 中文 🎯';
  const byteLength = encoder.calculateUTF8ByteLength(text);
  // Hello(5) + 空格(1) + 中文(6) + 空格(1) + 🎯(4) = 17字节
  const expected = 17;
  if (byteLength !== expected) throw new Error(`混合字符字节长度应为${expected}, 实际为${byteLength}`);
  return byteLength;
});

// 测试3: createUTF8JSONPayload
runTest('createUTF8JSONPayload - 简单对象', () => {
  const data = { message: '测试', number: 123 };
  const json = encoder.createUTF8JSONPayload(data);
  
  // 验证是有效的JSON
  const parsed = JSON.parse(json);
  if (parsed.message !== '测试' || parsed.number !== 123) {
    throw new Error('JSON解析结果不正确');
  }
  
  // 验证UTF-8编码
  const validation = encoder.validateNoGarbledChars(json);
  if (!validation.valid) throw new Error('生成的JSON包含乱码');
  
  return { length: json.length, valid: validation.valid };
});

runTest('createUTF8JSONPayload - 包含中文字符', () => {
  const data = { 
    title: 'UTF-8测试标题',
    content: '这是一段中文内容，包含Emoji🎯和特殊符号!@#$',
    array: ['项目1', '项目2', '项目3']
  };
  
  const json = encoder.createUTF8JSONPayload(data, true); // 美化输出
  const validation = encoder.validateNoGarbledChars(json);
  
  if (!validation.valid) {
    throw new Error('包含中文字符的JSON验证失败');
  }
  
  if (validation.chineseChars < 10) {
    throw new Error(`中文字符数过少: ${validation.chineseChars}`);
  }
  
  return { chineseChars: validation.chineseChars, valid: validation.valid };
});

// 测试4: validateNoGarbledChars
runTest('validateNoGarbledChars - 正常文本', () => {
  const text = '正常中文文本，没有乱码。';
  const result = encoder.validateNoGarbledChars(text);
  
  if (!result.valid) throw new Error('正常文本被误判为有乱码');
  if (result.garbledCount > 0) throw new Error(`正常文本检测到乱码: ${result.garbledCount}`);
  
  return result;
});

runTest('validateNoGarbledChars - 包含Emoji', () => {
  const text = '中文🎯Emoji✅测试🔤';
  const result = encoder.validateNoGarbledChars(text);
  
  if (!result.valid) throw new Error('包含Emoji的文本被误判为有乱码');
  
  return result;
});

// 测试5: createUTF8Headers
runTest('createUTF8Headers - 基本头信息', () => {
  const payload = '测试载荷';
  const headers = encoder.createUTF8Headers(payload);
  
  const requiredHeaders = ['Content-Type', 'Content-Length', 'User-Agent'];
  for (const header of requiredHeaders) {
    if (!headers[header]) throw new Error(`缺少必要头信息: ${header}`);
  }
  
  if (!headers['Content-Type'].includes('charset=utf-8')) {
    throw new Error('Content-Type未指定charset=utf-8');
  }
  
  const contentLength = parseInt(headers['Content-Length']);
  const expectedLength = encoder.calculateUTF8ByteLength(payload);
  
  if (contentLength !== expectedLength) {
    throw new Error(`Content-Length不正确: ${contentLength} != ${expectedLength}`);
  }
  
  return headers;
});

runTest('createUTF8Headers - 附加头信息', () => {
  const payload = '测试';
  const additionalHeaders = {
    'X-Custom-Header': '自定义值',
    'Authorization': 'Bearer token123'
  };
  
  const headers = encoder.createUTF8Headers(payload, additionalHeaders);
  
  for (const [key, value] of Object.entries(additionalHeaders)) {
    if (headers[key] !== value) {
      throw new Error(`附加头信息未正确添加: ${key}`);
    }
  }
  
  return headers;
});

// 测试6: 文件操作模拟
runTest('文件操作模拟 - 创建测试文件', () => {
  const testContent = '# 测试文件\n\n这是UTF-8编码的测试文件。\n包含中文：测试内容🎯\n';
  const testFilePath = path.join(__dirname, 'test-utf8-file.txt');
  
  // 写入文件
  fs.writeFileSync(testFilePath, testContent, 'utf8');
  
  // 读取并验证
  const readContent = encoder.readFileUTF8(testFilePath);
  
  if (readContent !== testContent) {
    throw new Error('读取的文件内容与写入的不一致');
  }
  
  const validation = encoder.validateNoGarbledChars(readContent);
  if (!validation.valid) {
    throw new Error('读取的文件内容包含乱码');
  }
  
  // 清理
  fs.unlinkSync(testFilePath);
  
  return { 
    fileSize: testContent.length,
    validation: validation.valid,
    chineseChars: validation.chineseChars 
  };
});

// 生成测试报告
console.log('\n' + '='.repeat(60));
console.log('📊 测试报告');

const totalTests = testResults.length;
const passedTests = testResults.filter(t => t.passed).length;
const failedTests = totalTests - passedTests;

console.log(`测试总数: ${totalTests}`);
console.log(`通过数量: ${passedTests}`);
console.log(`失败数量: ${failedTests}`);
console.log(`通过率: ${((passedTests / totalTests) * 100).toFixed(1)}%`);

if (failedTests > 0) {
  console.log('\n❌ 失败的测试:');
  testResults.filter(t => !t.passed).forEach((test, index) => {
    console.log(`  ${index + 1}. ${test.name}: ${test.error}`);
  });
  process.exit(1);
} else {
  console.log('\n🎉 所有测试通过！UTF-8编码工具核心功能正常。');
  
  // 输出性能示例
  console.log('\n💡 性能示例:');
  const sampleText = '这是一个包含中文、英文和Emoji🎯的测试文本。';
  console.log(`文本: "${sampleText}"`);
  console.log(`字符数: ${sampleText.length}`);
  console.log(`UTF-8字节数: ${encoder.calculateUTF8ByteLength(sampleText)}`);
  
  const validation = encoder.validateNoGarbledChars(sampleText);
  console.log(`乱码检测: ${validation.valid ? '✅ 通过' : '❌ 失败'}`);
  if (validation.chineseChars > 0) {
    console.log(`中文字符数: ${validation.chineseChars}`);
  }
}

// 清理临时文件
const tempFile = path.join(__dirname, 'test-utf8-file.txt');
if (fs.existsSync(tempFile)) {
  try {
    fs.unlinkSync(tempFile);
  } catch (e) {
    // 忽略清理错误
  }
}

console.log('\n✅ 测试完成。建议运行真实API测试验证平台兼容性。');