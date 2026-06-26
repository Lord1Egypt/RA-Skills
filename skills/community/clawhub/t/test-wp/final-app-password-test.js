#!/usr/bin/env node

/**
 * 应用程序密码最终测试
 * 在创建应用程序密码后运行
 */

const axios = require('axios');

// 配置 - 创建应用程序密码后更新这里
const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  appPassword: 'YOUR_APPLICATION_PASSWORD_HERE' // ← 替换为你的应用程序密码
};

async function finalTest() {
  console.log('🚀 WordPress应用程序密码最终测试\n');
  console.log('='.repeat(60));
  console.log('重要: 请先在WordPress中创建应用程序密码');
  console.log('步骤: 用户 → 个人资料 → 应用程序密码');
  console.log('='.repeat(60) + '\n');
  
  if (config.appPassword === 'YOUR_APPLICATION_PASSWORD_HERE') {
    console.log('❌ 请先更新配置中的 appPassword');
    console.log('将 YOUR_APPLICATION_PASSWORD_HERE 替换为你的应用程序密码');
    console.log('应用程序密码格式: xxxx xxxx xxxx xxxx xxxx xxxx');
    return;
  }
  
  console.log(`站点: ${config.wordpressUrl}`);
  console.log(`用户: ${config.username}`);
  console.log(`密码: ${config.appPassword.substring(0, 10)}...`);
  console.log('');
  
  const api = axios.create({
    baseURL: `${config.wordpressUrl}/wp-json/wp/v2`,
    auth: {
      username: config.username,
      password: config.appPassword
    },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'OpenClaw-Final-Test/1.0'
    },
    timeout: 10000
  });
  
  try {
    // 1. 测试认证
    console.log('1. 🔐 测试应用程序密码认证...');
    const userResponse = await api.get('/users/me');
    console.log(`   ✅ 认证成功!`);
    console.log(`      用户: ${userResponse.data.name}`);
    console.log(`      角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
    console.log(`      ID: ${userResponse.data.id}`);
    
    // 2. 发布测试文章
    console.log('\n2. 📝 发布测试文章...');
    
    const postData = {
      title: `应用程序密码测试 ${Date.now()}`,
      content: `# 应用程序密码自动发布测试
    
这是一个使用WordPress应用程序密码成功发布的测试文章。

## 测试详情
- **时间**: ${new Date().toISOString()}
- **方法**: WordPress应用程序密码
- **状态**: draft
- **用户**: ${userResponse.data.name}

## 功能验证
✅ 应用程序密码认证
✅ 文章自动发布  
✅ 参数格式正确
✅ 权限检查通过

## 技术信息
- WordPress版本: 6.9.4
- 认证方式: Basic Auth with Application Password
- API版本: wp/v2
- 自动化工具: OpenClaw

*测试成功完成*`,
      status: 'draft',
      excerpt: '应用程序密码自动发布功能测试',
      categories: [1] // 未分类
    };
    
    const publishResponse = await api.post('/posts', postData);
    
    console.log(`   🎉 文章发布成功!`);
    console.log(`      文章ID: ${publishResponse.data.id}`);
    console.log(`      标题: ${publishResponse.data.title.rendered}`);
    console.log(`      状态: ${publishResponse.data.status}`);
    console.log(`      链接: ${publishResponse.data.link}`);
    
    const postId = publishResponse.data.id;
    
    // 3. 测试更新
    console.log('\n3. 🔄 测试文章更新...');
    try {
      const updateResponse = await api.put(`/posts/${postId}`, {
        title: `更新后的标题 ${Date.now()}`,
        excerpt: '更新后的摘要'
      });
      console.log(`   ✅ 文章更新成功`);
    } catch (updateError) {
      console.log(`   ❌ 更新失败: ${updateError.message}`);
    }
    
    // 4. 测试删除
    console.log('\n4. 🗑️  测试文章删除...');
    try {
      await api.delete(`/posts/${postId}?force=true`);
      console.log(`   ✅ 文章删除成功`);
    } catch (deleteError) {
      console.log(`   ❌ 删除失败: ${deleteError.message}`);
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('🎉 恭喜! JWT自动发布功能配置成功!\n');
    
    console.log('📋 成功配置总结:');
    console.log(`
✅ 认证方式: WordPress应用程序密码
✅ API端点: ${config.wordpressUrl}/wp-json/wp/v2
✅ 用户权限: 已验证
✅ 发布功能: 工作正常

🚀 使用代码示例:

const axios = require('axios');

const wordpress = {
  url: '${config.wordpressUrl}',
  username: '${config.username}',
  appPassword: '你的应用程序密码'
};

const api = axios.create({
  baseURL: \`\${wordpress.url}/wp-json/wp/v2\`,
  auth: {
    username: wordpress.username,
    password: wordpress.appPassword
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

// 自动发布函数
async function autoPublishToWordPress(title, content, options = {}) {
  const postData = {
    title: title,
    content: content,
    status: options.status || 'draft',
    excerpt: options.excerpt || '',
    categories: options.categories || [1]
  };
  
  const response = await api.post('/posts', postData);
  return response.data;
}

// 使用示例
const article = {
  title: '自动发布的文章',
  content: '文章内容...',
  status: 'draft'
};

const result = await autoPublishToWordPress(article.title, article.content, {
  status: article.status
});

console.log('文章已发布，ID:', result.id);
    `);
    
    console.log('\n🔧 后续步骤:');
    console.log('1. 将成功配置保存到环境变量或配置文件中');
    console.log('2. 创建自动发布脚本或定时任务');
    console.log('3. 添加错误处理和日志记录');
    console.log('4. 考虑添加图片上传和标签管理');
    
  } catch (error) {
    console.log('\n❌ 测试失败:');
    
    if (error.response) {
      console.log(`状态码: ${error.response.status}`);
      console.log(`错误: ${error.response.data?.message || '未知错误'}`);
      console.log(`代码: ${error.response.data?.code || '未知'}`);
      
      if (error.response.status === 401) {
        console.log('\n🔍 可能的问题:');
        console.log('1. 应用程序密码不正确');
        console.log('2. 密码格式错误（应该是 xxxx xxxx xxxx xxxx xxxx xxxx）');
        console.log('3. 用户没有足够的权限');
      }
    } else {
      console.log(`错误: ${error.message}`);
    }
    
    console.log('\n🔧 请检查:');
    console.log('1. 是否正确创建了应用程序密码');
    console.log('2. 是否复制了完整的密码（24字符，有空格）');
    console.log('3. 用户是否有发布文章的权限');
  }
  
  console.log('\n🎯 测试完成');
}

// 运行最终测试
finalTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});