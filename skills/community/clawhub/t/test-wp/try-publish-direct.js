#!/usr/bin/env node

/**
 * 直接尝试发布文章
 * 获取详细的错误信息
 */

const axios = require('axios');

const config = {
  url: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

async function tryPublishDirectly() {
  console.log('🎯 直接尝试发布文章到WordPress\n');
  console.log(`站点: ${config.url}`);
  console.log(`用户: ${config.username}`);
  console.log('='.repeat(50) + '\n');
  
  const api = axios.create({
    baseURL: `${config.url}/wp-json/wp/v2`,
    auth: {
      username: config.username,
      password: config.password
    },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'OpenClaw-Direct-Publish/1.0'
    },
    timeout: 10000
  });
  
  // 准备测试文章
  const testArticle = {
    title: `直接发布测试 ${Date.now()}`,
    content: `# 直接发布测试
    
这是一个直接尝试发布到WordPress的测试文章。

## 测试详情
- 时间: ${new Date().toISOString()}
- 方法: Basic Auth
- 状态: draft

## 期望结果
希望能够成功发布，即使返回错误也能获得详细诊断信息。

*测试结束*`,
    status: 'draft',
    excerpt: '直接发布功能测试',
    categories: [1],
    tags: ['测试', 'API', 'WordPress']
  };
  
  console.log('📝 准备发布文章...');
  console.log(`标题: "${testArticle.title}"`);
  console.log(`状态: ${testArticle.status}`);
  console.log('');
  
  try {
    console.log('1. 🚀 尝试发布文章...');
    const response = await api.post('/posts', testArticle);
    
    console.log('🎉 成功! 文章已发布');
    console.log(`文章ID: ${response.data.id}`);
    console.log(`标题: ${response.data.title.rendered}`);
    console.log(`状态: ${response.data.status}`);
    console.log(`链接: ${response.data.link}`);
    
    // 立即删除测试文章
    console.log('\n2. 🗑️  清理测试文章...');
    try {
      await api.delete(`/posts/${response.data.id}?force=true`);
      console.log('✅ 测试文章已清理');
    } catch (deleteError) {
      console.log(`⚠️  清理失败: ${deleteError.message}`);
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('✅ 发布成功! 当前配置可用');
    
  } catch (error) {
    console.log('❌ 发布失败，获取详细错误信息:\n');
    
    if (error.response) {
      // 服务器响应了错误
      console.log(`📊 响应信息:`);
      console.log(`   状态码: ${error.response.status}`);
      console.log(`   状态文本: ${error.response.statusText}`);
      
      if (error.response.data) {
        console.log(`\n📝 响应数据:`);
        
        if (typeof error.response.data === 'object') {
          console.log(JSON.stringify(error.response.data, null, 2));
          
          // 分析常见错误
          if (error.response.data.code === 'rest_cannot_create') {
            console.log('\n🔍 错误分析: rest_cannot_create');
            console.log('   这个错误通常表示:');
            console.log('   1. 用户没有发布文章的权限');
            console.log('   2. 认证失败');
            console.log('   3. 用户角色不正确');
          } else if (error.response.data.code === 'rest_not_logged_in') {
            console.log('\n🔍 错误分析: rest_not_logged_in');
            console.log('   这个错误表示认证失败');
            console.log('   可能原因:');
            console.log('   1. 用户名或密码错误');
            console.log('   2. 使用的不是应用程序密码');
            console.log('   3. Basic Auth未正确配置');
          }
        } else {
          console.log(error.response.data);
        }
      }
      
      console.log(`\n📋 响应头:`);
      Object.entries(error.response.headers || {}).forEach(([key, value]) => {
        if (key.toLowerCase().includes('auth') || key.toLowerCase().includes('server')) {
          console.log(`   ${key}: ${value}`);
        }
      });
      
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.log('❌ 没有收到服务器响应');
      console.log('请求信息:', error.request);
    } else {
      // 请求设置时发生错误
      console.log('❌ 请求配置错误:', error.message);
    }
    
    // 提供解决方案
    console.log('\n' + '='.repeat(50));
    console.log('🔧 解决方案建议:\n');
    
    console.log('方案A: 使用WordPress应用程序密码 (推荐)');
    console.log('   1. 登录 https://your-site.com/wp-admin');
    console.log('   2. 进入 用户 → 个人资料');
    console.log('   3. 找到"应用程序密码"部分');
    console.log('   4. 创建新密码 (如: OpenClaw-API)');
    console.log('   5. 使用生成的密码替换当前密码');
    
    console.log('\n方案B: 安装JWT插件');
    console.log('   1. 安装 "JWT Authentication for WP REST API"');
    console.log('   2. 配置 wp-config.php');
    console.log('   3. 使用JWT令牌认证');
    
    console.log('\n方案C: 检查用户权限');
    console.log('   1. 确认用户 "admin" 有发布权限');
    console.log('   2. 需要"作者"或以上角色');
    console.log('   3. 检查用户角色设置');
    
    console.log('\n方案D: 测试其他认证方式');
    console.log('   1. 尝试使用登录密码 (如果不是应用程序密码)');
    console.log('   2. 检查是否有其他API密钥');
    console.log('   3. 联系主机提供商检查服务器配置');
    
    console.log('\n📞 需要的信息:');
    console.log('   1. WordPress用户的确切角色');
    console.log('   2. 是否有服务器访问权限');
    console.log('   3. WordPress安装方式 (cPanel/手动等)');
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('🎯 测试完成');
}

// 运行测试
tryPublishDirectly().catch(error => {
  console.error('测试过程中发生未捕获的错误:', error);
});