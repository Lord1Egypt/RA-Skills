// 示例3: 发布图文
import { publishContent } from '../src/xhs-tools.js';
import { closeBrowser } from '../src/browser.js';

console.log('🧪 小红书MCP服务 - 发布图文示例\n');

// 发布配置
const noteConfig = {
  title: '测试笔记 - 请勿发布',
  content: `
这是一篇测试笔记的正文内容。

可以包含多行文字，最多1000字。

#测试 #自动化
  `.trim(),
  images: [
    // 请替换为实际图片路径
    // './test-photo.jpg',
    // 或使用URL
    // 'https://example.com/photo.jpg'
  ],
  tags: ['测试', '自动化', 'MCP'],
  isOriginal: false,
  visibility: '仅自己可见', // 建议测试时使用"仅自己可见"
};

console.log('发布配置:');
console.log('  标题:', noteConfig.title);
console.log('  正文长度:', noteConfig.content.length, '字');
console.log('  图片数量:', noteConfig.images.length);
console.log('  标签:', noteConfig.tags.join(', '));
console.log('  可见性:', noteConfig.visibility);

console.log('\n⚠️  注意: 实际发布会真实操作账号！');
console.log('建议: 测试时使用"仅自己可见"模式\n');

// 实际发布（取消注释以启用）
/*
console.log('正在发布...');
const result = await publishContent(noteConfig);

if (result.success) {
  console.log('✅ 发布成功！');
  console.log('笔记ID:', result.noteId);
  console.log('笔记链接:', result.url);
} else {
  console.log('❌ 发布失败:', result.message);
}
*/

console.log('\n💡 提示: 取消代码中的注释以实际发布');

await closeBrowser();
console.log('\n✅ 发布示例完成！');
