/**
 * volc-image-gen 单元测试
 */

const { generateImage, batchGenerate, styleMap, supportedSizes } = require('../src/image-gen');
const { editImage, createVariations } = require('../src/image-edit');
const { validateApiKey, generateFilename, generateCacheKey } = require('../src/utils');

// 测试结果统计
let passed = 0;
let failed = 0;

/**
 * 断言函数
 */
function assert(condition, message) {
  if (condition) {
    console.log(`✅ ${message}`);
    passed++;
  } else {
    console.error(`❌ ${message}`);
    failed++;
  }
}

/**
 * 异步测试
 */
async function runTests() {
  console.log('🧪 开始运行 volc-image-gen 单元测试\n');
  console.log('=' .repeat(50));

  // ========== 工具函数测试 ==========
  console.log('\n📦 工具函数测试:\n');

  // 测试文件名生成
  const filename1 = generateFilename('test');
  const filename2 = generateFilename('test');
  assert(filename1.startsWith('test_'), '文件名以前缀开头');
  assert(filename1 !== filename2, '每次生成的文件名不同');
  assert(filename1.endsWith('.png'), '文件名以.png 结尾');

  // 测试缓存键生成
  const cacheKey1 = generateCacheKey('prompt1', { size: '1024x1024' });
  const cacheKey2 = generateCacheKey('prompt1', { size: '1024x1024' });
  const cacheKey3 = generateCacheKey('prompt2', { size: '1024x1024' });
  assert(cacheKey1 === cacheKey2, '相同参数生成相同缓存键');
  assert(cacheKey1 !== cacheKey3, '不同参数生成不同缓存键');

  // 测试 API Key 验证（应该是 false，因为没有配置环境变量）
  const hasKey = validateApiKey();
  console.log(`ℹ️  VOLC_API_KEY 已配置：${hasKey}`);

  // ========== 风格映射测试 ==========
  console.log('\n🎨 风格映射测试:\n');

  const expectedStyles = ['realistic', 'anime', 'oil', 'watercolor', 'sketch', 'cyberpunk', 'fantasy'];
  for (const style of expectedStyles) {
    assert(styleMap[style] !== undefined, `风格 ${style} 存在`);
    assert(typeof styleMap[style] === 'string', `风格 ${style} 是字符串`);
    assert(styleMap[style].length > 0, `风格 ${style} 描述不为空`);
  }

  // ========== 尺寸验证测试 ==========
  console.log('\n📐 尺寸验证测试:\n');

  const validSizes = ['512x512', '1024x1024', '1024x1536'];
  for (const size of validSizes) {
    assert(supportedSizes.includes(size), `尺寸 ${size} 支持`);
  }

  const invalidSizes = ['100x100', '2000x2000', 'abc'];
  for (const size of invalidSizes) {
    assert(!supportedSizes.includes(size), `尺寸 ${size} 不支持（预期）`);
  }

  // ========== API 调用测试（需要 API Key） ==========
  console.log('\n🌐 API 调用测试:\n');

  if (validateApiKey()) {
    console.log('⚠️  检测到 API Key，跳过实际 API 调用测试（避免产生费用）\n');
    // 可以在这里添加实际的 API 调用测试
  } else {
    console.log('ℹ️  未配置 VOLC_API_KEY，测试 API 错误处理...\n');

    // 测试缺少 API Key 时的错误处理
    const result = await generateImage({ prompt: 'test' });
    assert(!result.success, '缺少 API Key 时返回失败');
    assert(result.code === 401, '错误码为 401');
    assert(result.error.includes('VOLC_API_KEY'), '错误信息提示 API Key');

    // 测试缺少 prompt 时的错误处理
    const result2 = await generateImage({});
    assert(!result2.success, '缺少 prompt 时返回失败');

    // 测试不支持的尺寸
    const result3 = await generateImage({ prompt: 'test', size: '9999x9999' });
    assert(!result3.success, '不支持的尺寸返回失败');
    assert(result3.code === 400, '错误码为 400');
  }

  // ========== 批量生成测试 ==========
  console.log('\n📦 批量生成测试:\n');

  if (!validateApiKey()) {
    const batchResult = await batchGenerate(['test1', 'test2'], { concurrent: 2 });
    // 批量生成会调用 generateImage，每个子任务都会失败，但批量本身可能返回 success:true（因为有 successful/failed 统计）
    assert(batchResult.successful === 0 || !batchResult.success, '批量生成在没有 API Key 时失败或无成功');
  }

  // ========== 图生图测试 ==========
  console.log('\n🖼️ 图生图测试:\n');

  if (!validateApiKey()) {
    const editResult = await editImage({ 
      image: 'test.png', 
      prompt: 'test' 
    });
    assert(!editResult.success, '图生图在没有 API Key 时失败');
  }

  // ========== 输出测试结果 ==========
  console.log('\n' + '='.repeat(50));
  console.log(`\n📊 测试结果：${passed} 通过，${failed} 失败\n`);

  if (failed === 0) {
    console.log('🎉 所有测试通过！\n');
    process.exit(0);
  } else {
    console.log('⚠️  部分测试失败，请检查代码\n');
    process.exit(1);
  }
}

// 运行测试
runTests().catch(error => {
  console.error('💥 测试执行出错:', error);
  process.exit(1);
});
