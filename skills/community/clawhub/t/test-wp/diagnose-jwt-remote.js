#!/usr/bin/env node

/**
 * JWT插件远程诊断
 * 插件已激活但在当前服务器上不工作
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';
const USERNAME = 'admin';
const PASSWORD = 'your-app-password';

// 创建客户端
const client = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 15000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Remote-Diagnose/1.0'
  }
});

async function diagnoseRemoteIssue() {
  console.log('🔍 JWT插件远程诊断\n');
  console.log(`站点: ${WORDPRESS_URL}`);
  console.log(`用户: ${USERNAME}`);
  console.log('='.repeat(70) + '\n');
  
  // 1. 测试基础连接
  console.log('1. 🌐 测试基础连接...');
  try {
    const response = await client.get(WORDPRESS_URL);
    console.log(`✅ 站点可访问 (${response.status})`);
    console.log(`   服务器: ${response.headers['server'] || '未知'}`);
    
    // 检查是否重定向
    if (response.request?.res?.responseUrl !== WORDPRESS_URL) {
      console.log(`   🔍 有重定向: ${response.request?.res?.responseUrl}`);
    }
  } catch (error) {
    console.log(`❌ 站点不可访问: ${error.message}`);
    return;
  }
  
  // 2. 测试REST API
  console.log('\n2. 🔧 测试REST API...');
  try {
    const apiResponse = await client.get(`${WORDPRESS_URL}/wp-json`);
    console.log(`✅ REST API可用 (${apiResponse.status})`);
    
    // 检查路由
    const routes = Object.keys(apiResponse.data.routes || {});
    console.log(`   发现 ${routes.length} 个API端点`);
    
    // 查找JWT相关路由
    const jwtRoutes = routes.filter(route => 
      route.includes('jwt-auth') || 
      route.includes('jwt') ||
      route.includes('/token')
    );
    
    if (jwtRoutes.length > 0) {
      console.log(`\n🎯 发现的JWT相关路由:`);
      jwtRoutes.forEach(route => {
        console.log(`   - ${route}`);
      });
    } else {
      console.log(`\n⚠️  未发现JWT相关路由`);
    }
    
  } catch (error) {
    console.log(`❌ REST API错误: ${error.message}`);
  }
  
  // 3. 测试JWT端点
  console.log('\n3. 🔐 详细测试JWT端点...');
  
  const endpoints = [
    '/wp-json/jwt-auth/v1/token',
    '/wp-json/jwt-auth/v1/token/validate',
    '/?rest_route=/jwt-auth/v1/token',
    '/index.php?rest_route=/jwt-auth/v1/token',
    '/wp-json/api/v1/token',
    '/wp-json/api/jwt/token'
  ];
  
  for (const endpoint of endpoints) {
    console.log(`\n   测试: ${endpoint}`);
    
    try {
      // 测试GET请求
      const getResponse = await client.get(WORDPRESS_URL + endpoint);
      console.log(`   ✅ GET: ${getResponse.status}`);
      
      if (getResponse.status === 405) {
        console.log(`   🔍 需要POST请求`);
      }
      
      // 如果GET成功但不是405，尝试POST
      if (getResponse.status !== 405) {
        console.log(`   尝试POST请求...`);
        const postResponse = await client.post(
          WORDPRESS_URL + endpoint,
          { username: USERNAME, password: PASSWORD },
          { headers: { 'Content-Type': 'application/json' } }
        );
        console.log(`   ✅ POST: ${postResponse.status}`);
      }
      
    } catch (error) {
      const status = error.response?.status;
      const headers = error.response?.headers;
      
      if (status === 404) {
        console.log(`   ❌ 端点不存在 (404)`);
        
        // 检查是否是Nginx 404
        if (error.response?.data?.includes('nginx')) {
          console.log(`   🔍 Nginx返回的404 - 可能是服务器配置问题`);
        }
      } else if (status === 405) {
        console.log(`   ✅ 端点存在 (需要POST请求)`);
        
        // 尝试POST
        try {
          const postResponse = await client.post(
            WORDPRESS_URL + endpoint,
            { username: USERNAME, password: PASSWORD },
            { headers: { 'Content-Type': 'application/json' } }
          );
          console.log(`   ✅ POST: ${postResponse.status}`);
          
          if (postResponse.data?.token) {
            console.log(`   🎉 获取到JWT令牌!`);
            await testJWTWorkflow(postResponse.data.token);
            return;
          }
        } catch (postError) {
          console.log(`   ❌ POST失败: ${postError.response?.status || postError.message}`);
        }
      } else if (status === 500) {
        console.log(`   🔥 服务器错误 (500)`);
        
        if (error.response?.data) {
          const data = error.response.data;
          console.log(`      错误: ${data.message || '未知'}`);
          console.log(`      代码: ${data.code || '未知'}`);
          
          if (data.code === 'jwt_auth_bad_config' || data.code === 'jwt_auth_no_secret_key') {
            console.log(`\n🔧 JWT配置错误: wp-config.php需要配置`);
          }
        }
      } else {
        console.log(`   ⚠️  错误: ${status || error.message}`);
      }
    }
  }
  
  // 4. 检查服务器配置
  console.log('\n' + '='.repeat(70));
  console.log('4. ⚙️  检查服务器配置问题\n');
  
  console.log('可能的问题:');
  console.log('\nA. Nginx配置问题 (最常见)');
  console.log('   JWT插件需要Nginx支持授权头，添加以下配置:');
  console.log(`
   location / {
       try_files $uri $uri/ /index.php?$args;
       
       # 添加这些行
       add_header 'Access-Control-Allow-Origin' '*';
       add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
       add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';
   }
  `);
  
  console.log('\nB. .htaccess问题 (如果是Apache)');
  console.log('   确保.htaccess文件包含:');
  console.log(`
   RewriteEngine On
   RewriteBase /
   RewriteRule ^index\.php$ - [L]
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   RewriteRule . /index.php [L]
  `);
  
  console.log('\nC. 固定链接问题');
  console.log('   重新保存固定链接:');
  console.log('   访问 https://your-site.com/wp-admin/options-permalink.php');
  console.log('   点击"保存更改"');
  
  console.log('\nD. 插件冲突');
  console.log('   暂时禁用其他插件测试');
  
  // 5. 测试备选方案
  console.log('\n' + '='.repeat(70));
  console.log('5. 🚀 测试备选方案\n');
  
  console.log('A. 测试应用程序密码:');
  console.log(`   curl -u '${USERNAME}:${PASSWORD}' \\`);
  console.log(`     '${WORDPRESS_URL}/wp-json/wp/v2/users/me'`);
  
  console.log('\nB. 测试不同格式的JWT端点:');
  console.log(`   curl -X POST '${WORDPRESS_URL}/?rest_route=/jwt-auth/v1/token' \\`);
  console.log(`     -H 'Content-Type: application/json' \\`);
  console.log(`     -d '{"username":"${USERNAME}","password":"${PASSWORD}"}'`);
  
  console.log('\nC. 检查WordPress调试日志:');
  console.log('   在wp-config.php中添加:');
  console.log(`   define('WP_DEBUG', true);`);
  console.log(`   define('WP_DEBUG_LOG', true);`);
  console.log(`   然后检查 /wp-content/debug.log`);
  
  console.log('\n' + '='.repeat(70));
  console.log('🎯 诊断完成\n');
  
  console.log('📋 建议的下一步:');
  console.log('   1. 检查Nginx配置 (最可能的问题)');
  console.log('   2. 重新保存固定链接');
  console.log('   3. 启用WordPress调试日志');
  console.log('   4. 如果不行，使用应用程序密码');
}

async function testJWTWorkflow(token) {
  console.log('\n' + '='.repeat(70));
  console.log('🚀 JWT工作流程测试\n');
  
  const api = axios.create({
    baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
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
    
    // 发布测试文章
    console.log('\n2. 发布测试文章...');
    const postData = {
      title: `远程诊断测试 ${Date.now()}`,
      content: 'JWT远程诊断测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const post = await api.post('/posts', postData);
    console.log(`   🎉 文章发布成功! ID: ${post.data.id}`);
    
    // 清理
    await api.delete(`/posts/${post.data.id}?force=true`);
    console.log('   ✅ 测试文章已清理');
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ JWT插件在当前服务器上工作正常!');
    
  } catch (error) {
    console.log(`❌ JWT工作流程失败: ${error.response?.data?.message || error.message}`);
  }
}

// 运行诊断
diagnoseRemoteIssue().catch(error => {
  console.error('诊断过程中发生错误:', error);
});