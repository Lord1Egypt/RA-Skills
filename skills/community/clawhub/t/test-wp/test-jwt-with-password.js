#!/usr/bin/env node

/**
 * 使用提供的密码测试JWT认证
 */

const axios = require('axios');
const https = require('https');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

// 创建客户端
const client = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 15000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Test/1.0'
  }
});

async function testJWT() {
  console.log('🔐 使用密码测试JWT认证\n');
  console.log(`站点: ${config.wordpressUrl}`);
  console.log(`用户: ${config.username}`);
  console.log(`密码: ${config.password.substring(0, 10)}...`);
  console.log('='.repeat(60) + '\n');
  
  // 1. 首先测试WordPress连接
  console.log('1. 🔍 测试WordPress连接...');
  try {
    const response = await client.get(`${config.wordpressUrl}/wp-json`);
    console.log(`✅ WordPress REST API可用 (${response.status})`);
    console.log(`   版本: ${response.data.version || '未知'}`);
  } catch (error) {
    console.log(`❌ WordPress连接失败: ${error.message}`);
    return;
  }
  
  // 2. 测试JWT端点
  console.log('\n2. 🔐 测试JWT端点...');
  
  const endpoints = [
    '/wp-json/jwt-auth/v1/token',
    '/?rest_route=/jwt-auth/v1/token',
    '/index.php?rest_route=/jwt-auth/v1/token'
  ];
  
  for (const endpoint of endpoints) {
    console.log(`\n   测试端点: ${endpoint}`);
    
    try {
      // 先测试端点是否存在
      const getResponse = await client.get(config.wordpressUrl + endpoint);
      console.log(`   ✅ 端点存在 (GET: ${getResponse.status})`);
      
      if (getResponse.status === 405) {
        console.log(`   🔍 需要POST请求`);
      }
    } catch (getError) {
      const status = getError.response?.status;
      
      if (status === 404) {
        console.log(`   ❌ 端点不存在 (404)`);
        continue; // 尝试下一个端点
      } else if (status === 405) {
        console.log(`   ✅ 端点存在 (需要POST请求)`);
      } else {
        console.log(`   ⚠️  GET错误: ${status || getError.message}`);
      }
    }
    
    // 尝试POST请求获取令牌
    console.log(`   尝试POST请求获取JWT令牌...`);
    
    try {
      const postResponse = await client.post(
        config.wordpressUrl + endpoint,
        {
          username: config.username,
          password: config.password
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      console.log(`   ✅ POST请求成功 (${postResponse.status})`);
      
      if (postResponse.data && postResponse.data.token) {
        console.log(`\n🎉 JWT令牌获取成功!`);
        console.log(`   令牌: ${postResponse.data.token.substring(0, 30)}...`);
        console.log(`   用户: ${postResponse.data.user_display_name || postResponse.data.user_email}`);
        console.log(`   有效期: ${postResponse.data.expires_in || '未知'}秒`);
        
        // 立即测试API
        await testJWTAPI(postResponse.data.token);
        return;
      } else {
        console.log(`   ⚠️  响应中没有token字段`);
        console.log(`      响应: ${JSON.stringify(postResponse.data).substring(0, 100)}`);
      }
      
    } catch (postError) {
      const status = postError.response?.status;
      const data = postError.response?.data;
      
      if (status === 404) {
        console.log(`   ❌ 端点不存在 (404)`);
      } else if (status === 401 || status === 403) {
        console.log(`   ❌ 认证失败 (${status})`);
        if (data && data.message) {
          console.log(`      错误: ${data.message}`);
        }
      } else if (status === 500) {
        console.log(`   🔥 服务器错误 (500)`);
        if (data) {
          console.log(`      错误: ${data.message || '未知错误'}`);
          console.log(`      代码: ${data.code || '未知'}`);
          
          // 分析JWT错误
          if (data.code === 'jwt_auth_bad_config' || data.code === 'jwt_auth_no_secret_key') {
            console.log(`\n🔧 JWT配置错误: 需要配置wp-config.php`);
            console.log(`   添加以下代码到wp-config.php:`);
            console.log(`   define('JWT_AUTH_SECRET_KEY', 'your-secret-key');`);
            console.log(`   define('JWT_AUTH_CORS_ENABLE', true);`);
          }
        }
      } else {
        console.log(`   ❌ 错误: ${status || postError.message}`);
      }
    }
  }
  
  // 3. 如果JWT失败，尝试应用程序密码方式
  console.log('\n' + '='.repeat(60));
  console.log('🔄 JWT失败，尝试应用程序密码方式...\n');
  
  const api = axios.create({
    baseURL: `${config.wordpressUrl}/wp-json/wp/v2`,
    auth: {
      username: config.username,
      password: config.password
    },
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  try {
    console.log('测试应用程序密码认证...');
    const userResponse = await api.get('/users/me');
    console.log(`✅ 应用程序密码认证成功!`);
    console.log(`   用户: ${userResponse.data.name}`);
    console.log(`   角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
    
    // 测试发布
    console.log('\n测试文章发布...');
    const postData = {
      title: `应用程序密码测试 ${Date.now()}`,
      content: '使用提供的密码测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const postResponse = await api.post('/posts', postData);
    console.log(`🎉 文章发布成功!`);
    console.log(`   文章ID: ${postResponse.data.id}`);
    console.log(`   标题: ${postResponse.data.title.rendered}`);
    
    // 清理
    await api.delete(`/posts/${postResponse.data.id}?force=true`);
    console.log('✅ 测试文章已清理');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 密码可用! 但不是JWT方式，是应用程序密码方式。');
    
  } catch (error) {
    console.log(`❌ 应用程序密码也失败: ${error.response?.data?.message || error.message}`);
    
    if (error.response?.status === 401) {
      console.log('\n🔍 可能的问题:');
      console.log('   1. 密码错误');
      console.log('   2. 用户没有API访问权限');
      console.log('   3. 需要创建应用程序密码');
    }
  }
  
  console.log('\n🎯 测试完成');
}

async function testJWTAPI(token) {
  console.log('\n' + '='.repeat(60));
  console.log('🚀 测试JWT API访问\n');
  
  const api = axios.create({
    baseURL: `${config.wordpressUrl}/wp-json/wp/v2`,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  try {
    // 测试用户信息
    console.log('1. 获取用户信息...');
    const user = await api.get('/users/me');
    console.log(`   ✅ 成功: ${user.data.name}`);
    
    // 测试发布
    console.log('\n2. 发布测试文章...');
    const postData = {
      title: `JWT测试 ${Date.now()}`,
      content: 'JWT认证测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const post = await api.post('/posts', postData);
    console.log(`   🎉 文章发布成功! ID: ${post.data.id}`);
    
    // 清理
    await api.delete(`/posts/${post.data.id}?force=true`);
    console.log('   ✅ 测试文章已清理');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ JWT认证成功! 可以开始自动发布。');
    
  } catch (error) {
    console.log(`❌ JWT API测试失败: ${error.response?.data?.message || error.message}`);
  }
}

// 运行测试
testJWT().catch(error => {
  console.error('测试过程中发生错误:', error);
});