/**
 * 小红书 MCP 服务 - 发布图文示例
 *
 * 说明：演示如何发布图文笔记
 * 运行：node examples/03-发布示例.mjs
 *
 * ⚠️  注意：实际发布会真实操作账号，请谨慎使用！
 */

import { publishContent } from '../src/xhs-tools.js';
import { closeBrowser } from '../src/browser.js';

console.log('🧪 小红书MCP服务 - 发布图文示例\n');

// ==================== 配置发布内容 ====================
// 💡 提示：请根据实际情况修改以下配置

const noteConfig = {
  // 标题（最多20字）
  title: '测试笔记 - 请修改',

  // 正文内容（最多1000字）
  content: `
这是一篇测试笔记的正文内容。

💡 使用说明：
1. 请替换为你自己的内容
2. 图片路径可以是相对路径或绝对路径
3. 建议测试时使用"仅自己可见"

#测试 #示例
  `.trim(),

  // 图片列表（至少1张）
  // 💡 使用相对路径（相对于项目根目录）或绝对路径
  images: [
    // 示例：相对路径
    // './my-photos/photo1.jpg',
    // './my-photos/photo2.jpg',

    // 示例：绝对路径
    // '/Users/username/Pictures/photo.jpg',  // Mac/Linux
    // 'C:\\Users\\Username\\Pictures\\photo.jpg',  // Windows

    // 示例：网络图片URL
    // 'https://example.com/photo.jpg',
  ],

  // 标签（可选）
  tags: ['测试', '示例', 'MCP'],

  // 是否原创（可选，默认false）
  isOriginal: false,

  // 可见范围（可选，默认"公开可见"）
  // 💡 建议：测试时使用"仅自己可见"
  visibility: '仅自己可见',  // 公开可见 | 仅自己可见 | 仅互关好友可见

  // 定时发布（可选）
  // 格式：ISO 8601，如 '2026-03-16T10:00:00Z'
  // scheduleAt: '2026-03-16T10:00:00Z',
};

// ==================== 显示配置信息 ====================

console.log('发布配置:');
console.log('  标题:', noteConfig.title);
console.log('  正文长度:', noteConfig.content.length, '字');
console.log('  图片数量:', noteConfig.images.length);
console.log('  标签:', noteConfig.tags?.join(', ') || '无');
console.log('  可见性:', noteConfig.visibility);
console.log('  原创:', noteConfig.isOriginal ? '是' : '否');

// ==================== 内容验证 ====================

if (noteConfig.title.length > 20) {
  console.log('\n❌ 错误: 标题超过20字');
  await closeBrowser();
  process.exit(1);
}

if (noteConfig.content.length > 1000) {
  console.log('\n❌ 错误: 正文超过1000字');
  await closeBrowser();
  process.exit(1);
}

if (noteConfig.images.length === 0) {
  console.log('\n⚠️  警告: 未配置图片');
  console.log('   请在 noteConfig.images 中添加图片路径');
}

// ==================== 执行发布 ====================

console.log('\n⚠️  重要提示:');
console.log('   1. 此操作会真实发布笔记到小红书');
console.log('   2. 建议测试时使用"仅自己可见"模式');
console.log('   3. 确保图片路径正确且文件存在');
console.log('\n📝 要实际发布，请取消下面的注释\n');

// 实际发布代码（取消注释以启用）
/*
console.log('正在发布笔记...');
console.log('(这可能需要10-30秒)\n');

try {
  const result = await publishContent(noteConfig);

  if (result.success) {
    console.log('\n✅ 发布成功！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('笔记ID:', result.noteId);
    console.log('笔记链接:', result.url);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  } else {
    console.log('\n❌ 发布失败');
    console.log('错误信息:', result.message);
  }
} catch (error) {
  console.log('\n❌ 发布出错');
  console.log('错误:', error.message);
  console.log('堆栈:', error.stack);
}
*/

console.log('💡 提示: 取消代码中的注释以实际发布');
console.log('   查找: /* 和 */ 并删除它们\n');

await closeBrowser();
console.log('✅ 发布示例完成！');
