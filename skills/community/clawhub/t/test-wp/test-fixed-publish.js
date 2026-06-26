// 测试修复后的发布功能
const axios = require('axios');

// 使用config.js中的配置
const config = require('./config.js');

async function testPublish() {
  console.log('🔧 测试修复后的WordPress发布功能\n');
  console.log(`站点: ${config.wordpress.url}`);
  console.log(`用户: ${config.wordpress.username}`);
  console.log('='.repeat(50) + '\n');
  
  // 创建API客户端
  const api = axios.create({
    baseURL: `${config.wordpress.url}${config.wordpress.apiBase}`,
    auth: {
      username: config.wordpress.username,
      password: config.wordpress.password
    },
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  // 首先测试连接
  console.log('🔍 测试API连接...');
  try {
    const testResponse = await api.get('/posts?per_page=1');
    console.log(`✅ API连接成功，找到 ${testResponse.data.length} 篇文章`);
  } catch (error) {
    console.log(`❌ API连接失败: ${error.message}`);
    if (error.response) {
      console.log(`状态码: ${error.response.status}`);
      console.log(`错误: ${JSON.stringify(error.response.data)}`);
    }
    return;
  }
  
  // 创建测试文章
  const testArticle = {
    title: `OpenClaw修复测试 - ${new Date().toISOString()}`,
    content: '<h1>OpenClaw修复测试</h1><p>这是一个测试文章，用于验证修复后的发布功能。</p><p>如果看到这篇文章，说明发布功能已修复！🎉</p>',
    status: 'draft',
    excerpt: 'OpenClaw WordPress发布功能修复测试',
    categories: [1] // 默认分类
  };
  
  console.log('\n📝 准备发布测试文章...');
  console.log(`标题: "${testArticle.title}"`);
  console.log(`状态: ${testArticle.status}`);
  
  try {
    console.log('\n🚀 发布文章...');
    const response = await api.post('/posts', testArticle);
    
    console.log('\n✅ 文章发布成功!');
    console.log(`文章ID: ${response.data.id}`);
    console.log(`文章链接: ${response.data.link}`);
    console.log(`文章状态: ${response.data.status}`);
    
    // 返回文章链接
    return response.data.link;
    
  } catch (error) {
    console.log('\n❌ 发布失败:');
    if (error.response) {
      console.log(`状态码: ${error.response.status}`);
      console.log(`错误代码: ${error.response.data.code || '未知'}`);
      console.log(`错误消息: ${error.response.data.message || '未知'}`);
      
      if (error.response.data.data) {
        console.log(`错误详情: ${JSON.stringify(error.response.data.data)}`);
      }
    } else {
      console.log(`错误: ${error.message}`);
    }
    return null;
  }
}

// 运行测试
testPublish().then(link => {
  if (link) {
    console.log('\n🎯 测试完成!');
    console.log(`🔗 文章链接: ${link}`);
    
    // 保存链接到文件
    const fs = require('fs');
    fs.writeFileSync('publish-success.txt', `文章链接: ${link}\n时间: ${new Date().toISOString()}`);
  } else {
    console.log('\n❌ 测试失败，请检查配置和权限。');
  }
}).catch(error => {
  console.error('测试过程中出错:', error);
});