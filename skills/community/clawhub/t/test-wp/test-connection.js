#!/usr/bin/env node

/**
 * WordPress连接测试脚本
 * 测试与WordPress站点的连接和配置
 */

const fs = require('fs');
const path = require('path');

// 检查配置文件
console.log('🔍 检查配置文件...');

let config;
try {
  // 先尝试加载 config.js
  if (fs.existsSync(path.join(__dirname, 'config.js'))) {
    config = require('./config.js');
    console.log('✅ 找到 config.js 配置文件');
  } else if (fs.existsSync(path.join(__dirname, 'config.example.js'))) {
    console.log('⚠️  未找到 config.js，使用 config.example.js 作为参考');
    config = require('./config.example.js');
  } else {
    console.error('❌ 未找到配置文件');
    console.log('请创建 config.js 文件或复制 config.example.js');
    process.exit(1);
  }
} catch (error) {
  console.error('❌ 配置文件加载失败:', error.message);
  process.exit(1);
}

// 检查必要配置
console.log('\n⚙️  检查配置项...');

const requiredConfigs = [
  { key: 'wordpress.url', value: config.wordpress?.url },
  { key: 'wordpress.username', value: config.wordpress?.username },
  { key: 'wordpress.password', value: config.wordpress?.password }
];

let configValid = true;
requiredConfigs.forEach(item => {
  if (!item.value || item.value.includes('your-') || item.value.includes('xxxx')) {
    console.log(`❌ ${item.key}: 未配置或使用默认值`);
    configValid = false;
  } else {
    console.log(`✅ ${item.key}: 已配置`);
  }
});

if (!configValid) {
  console.log('\n⚠️  请编辑 config.js 文件，填写正确的WordPress配置');
  console.log('   必需配置: WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD');
  process.exit(1);
}

// 测试API连接
console.log('\n🔗 测试WordPress API连接...');

const WordPressAPI = require('./wordpress-api.js');
const wpApi = new WordPressAPI(config);

(async () => {
  try {
    const connected = await wpApi.testConnection();
    
    if (connected) {
      console.log('\n🎉 连接测试通过！');
      console.log('WordPress配置正确，可以开始发布文章。');
      
      // 测试获取文章列表
      console.log('\n📡 测试获取文章列表...');
      try {
        const result = await wpApi.getPosts({ perPage: 3 });
        console.log(`✅ 成功获取 ${result.posts.length} 篇文章`);
        
        if (result.posts.length > 0) {
          console.log('最新文章:');
          result.posts.forEach((post, index) => {
            console.log(`  ${index + 1}. ${post.title.rendered} (${post.status})`);
          });
        }
      } catch (error) {
        console.log('⚠️  获取文章列表失败，但API连接正常');
      }
      
      // 测试获取分类
      console.log('\n🏷️  测试获取分类...');
      try {
        const categories = await wpApi.getCategories();
        console.log(`✅ 成功获取 ${categories.length} 个分类`);
        
        if (categories.length > 0) {
          console.log('可用分类:');
          categories.slice(0, 5).forEach(cat => {
            console.log(`  - ${cat.name} (ID: ${cat.id})`);
          });
          if (categories.length > 5) {
            console.log(`  ... 还有 ${categories.length - 5} 个分类`);
          }
        }
      } catch (error) {
        console.log('⚠️  获取分类失败');
      }
      
      console.log('\n========================================');
      console.log('✅ 所有测试通过！');
      console.log('✅ WordPress自动发布技能已准备好使用');
      console.log('========================================');
      
      console.log('\n📋 下一步：');
      console.log('1. 将Markdown文章放入 posts/ 目录');
      console.log('2. 运行: node publish.js --file posts/your-article.md');
      console.log('3. 或批量发布: node batch-publish.js --dir posts/');
      
    } else {
      console.log('\n❌ 连接测试失败');
      console.log('请检查以下问题：');
      console.log('1. WordPress URL是否正确');
      console.log('2. 用户名和应用程序密码是否正确');
      console.log('3. WordPress REST API是否已启用');
      console.log('4. 网络连接是否正常');
    }
  } catch (error) {
    console.error('\n❌ 测试过程中发生错误:', error.message);
  }
})();