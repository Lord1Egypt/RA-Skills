#!/usr/bin/env node

/**
 * JWT插件安装验证脚本
 * 检查具体哪里出了问题
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';

// 创建客户端
const client = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 10000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Verify/1.0'
  }
});

async function verifyJWTInstallation() {
  console.log('🔍 JWT插件安装验证\n');
  console.log(`WordPress站点: ${WORDPRESS_URL}`);
  console.log('='.repeat(60) + '\n');
  
  // 1. 检查WordPress基本信息
  console.log('1. 📊 检查WordPress基本信息');
  try {
    const info = await client.get(`${WORDPRESS_URL}/wp-json`);
    console.log('✅ WordPress REST API可用');
    console.log(`   名称: ${info.data.name || '未设置'}`);
    console.log(`   描述: ${info.data.description || '未设置'}`);
    
    // 检查所有路由，查找JWT相关
    const routes = Object.keys(info.data.routes || {});
    const jwtRoutes = routes.filter(route => route.includes('jwt') || route.includes('auth'));
    
    if (jwtRoutes.length > 0) {
      console.log(`\n🎯 发现的JWT/Auth相关路由:`);
      jwtRoutes.forEach(route => {
        console.log(`   - ${route}`);
      });
    } else {
      console.log(`\n⚠️  路由表中未发现JWT/Auth相关路由`);
      console.log(`   前5个可用路由:`);
      routes.slice(0, 5).forEach(route => {
        console.log(`   - ${route}`);
      });
    }
  } catch (error) {
    console.log(`❌ 无法获取WordPress信息: ${error.message}`);
  }
  
  // 2. 测试JWT端点
  console.log('\n2. 🔐 测试JWT端点');
  
  const endpoints = [
    { url: '/wp-json/jwt-auth/v1/token', method: 'POST', desc: '标准JWT端点' },
    { url: '/wp-json/jwt-auth/v1/token/validate', method: 'POST', desc: 'JWT验证端点' },
    { url: '/?rest_route=/jwt-auth/v1/token', method: 'POST', desc: 'rest_route格式' }
  ];
  
  for (const endpoint of endpoints) {
    console.log(`\n   测试: ${endpoint.desc}`);
    console.log(`   端点: ${endpoint.url}`);
    
    try {
      // 先测试端点是否存在（GET请求）
      const getResponse = await client.get(WORDPRESS_URL + endpoint.url);
      console.log(`   ✅ 端点存在 (GET: ${getResponse.status})`);
      
      if (getResponse.status === 405) {
        console.log(`   🔍 需要${endpoint.method}请求`);
      }
    } catch (getError) {
      const status = getError.response?.status;
      
      if (status === 404) {
        console.log(`   ❌ 端点不存在 (404)`);
        
        // 如果是标准JWT端点，提供具体建议
        if (endpoint.url === '/wp-json/jwt-auth/v1/token') {
          console.log(`\n🔧 这意味着:`);
          console.log(`   1. JWT插件未激活 或`);
          console.log(`   2. 插件激活但wp-config.php未配置 或`);
          console.log(`   3. 固定链接设置有问题`);
        }
      } else if (status === 405) {
        console.log(`   ✅ 端点存在 (需要POST请求)`);
      } else {
        console.log(`   ⚠️  错误: ${status || getError.message}`);
      }
    }
  }
  
  // 3. 尝试获取JWT令牌
  console.log('\n3. 🚀 尝试获取JWT令牌');
  console.log('   用户名: admin');
  
  try {
    const response = await client.post(
      `${WORDPRESS_URL}/wp-json/jwt-auth/v1/token`,
      {
        username: 'admin',
        password: 'your-app-password'
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (response.data.token) {
      console.log(`\n🎉 JWT令牌获取成功!`);
      console.log(`   令牌: ${response.data.token.substring(0, 30)}...`);
      console.log(`   用户: ${response.data.user_display_name || response.data.user_email}`);
      console.log(`   有效期: ${response.data.expires_in || '未知'}秒`);
      
      // 立即测试API访问
      await testJWTAPI(response.data.token);
      return;
    }
    
  } catch (error) {
    const status = error.response?.status;
    const data = error.response?.data;
    
    console.log(`\n❌ JWT令牌获取失败`);
    console.log(`   状态码: ${status}`);
    
    if (data) {
      console.log(`   错误: ${data.message || '未知错误'}`);
      console.log(`   代码: ${data.code || '未知'}`);
      
      // 分析错误
      analyzeJWTError(data.code, data.message);
    }
  }
  
  // 4. 提供解决方案
  console.log('\n' + '='.repeat(60));
  console.log('📋 解决方案检查清单\n');
  
  console.log('请确认以下步骤已完成:');
  console.log('\n✅ 1. 插件安装');
  console.log('   访问: https://your-site.com/wp-admin/plugins.php');
  console.log('   确认 "JWT Authentication for WP REST API" 已安装');
  
  console.log('\n✅ 2. 插件激活');
  console.log('   在插件页面，找到JWT插件');
  console.log('   必须显示为"已激活"（蓝色"停用"按钮）');
  
  console.log('\n✅ 3. wp-config.php 配置');
  console.log('   编辑 wp-config.php，在末尾添加:');
  console.log(`
   define('JWT_AUTH_SECRET_KEY', 'your-strong-secret-key');
   define('JWT_AUTH_CORS_ENABLE', true);
  `);
  console.log('   生成密钥: openssl rand -base64 32');
  
  console.log('\n✅ 4. 固定链接设置');
  console.log('   访问: https://your-site.com/wp-admin/options-permalink.php');
  console.log('   点击"保存更改"（即使设置没变）');
  
  console.log('\n✅ 5. 清除缓存');
  console.log('   清除WordPress缓存（如果有缓存插件）');
  console.log('   清除浏览器缓存');
  
  console.log('\n🚀 如果以上都正确，但仍然失败:');
  console.log('   1. 暂时禁用其他所有插件');
  console.log('   2. 切换到默认主题测试');
  console.log('   3. 检查服务器错误日志');
  
  console.log('\n🔗 备选方案:');
  console.log('   使用WordPress应用程序密码:');
  console.log('   1. 访问 https://your-site.com/wp-admin/profile.php');
  console.log('   2. 创建应用程序密码');
  console.log('   3. 运行: node app-password-test.js');
}

function analyzeJWTError(code, message) {
  console.log('\n🔍 错误分析:');
  
  if (code === 'jwt_auth_bad_config' || code === 'jwt_auth_no_secret_key') {
    console.log(`   ❌ JWT配置错误`);
    console.log(`      需要在 wp-config.php 中添加:`);
    console.log(`      define('JWT_AUTH_SECRET_KEY', 'your-secret-key');`);
    console.log(`      define('JWT_AUTH_CORS_ENABLE', true);`);
    
    console.log(`\n🔑 生成密钥:`);
    console.log(`   openssl rand -base64 32`);
    console.log(`   或使用: https://randomkeygen.com/`);
    
  } else if (code === 'rest_cannot_create' || message?.includes('not allowed')) {
    console.log(`   ❌ 权限问题`);
    console.log(`      用户可能没有发布文章的权限`);
    console.log(`      需要作者或以上角色`);
    
  } else if (message?.includes('username') || message?.includes('password')) {
    console.log(`   ❌ 认证失败`);
    console.log(`      用户名或密码错误`);
    
  } else {
    console.log(`   ⚠️  ${message || '未知错误'}`);
  }
}

async function testJWTAPI(token) {
  console.log('\n' + '='.repeat(60));
  console.log('🚀 测试JWT API访问\n');
  
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
    console.log(`      角色: ${user.data.roles?.join(', ') || '未知'}`);
    
    // 测试文章发布
    console.log('\n2. 测试文章发布...');
    const postData = {
      title: `JWT验证测试 ${Date.now()}`,
      content: 'JWT插件验证测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const post = await api.post('/posts', postData);
    console.log(`   🎉 文章发布成功!`);
    console.log(`      文章ID: ${post.data.id}`);
    console.log(`      标题: ${post.data.title.rendered}`);
    
    // 清理测试文章
    console.log('\n3. 清理测试文章...');
    await api.delete(`/posts/${post.data.id}?force=true`);
    console.log('   ✅ 文章已清理');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ JWT插件安装配置成功!');
    console.log('\n📋 可以开始自动发布文章了!');
    
  } catch (error) {
    console.log(`❌ API测试失败: ${error.response?.data?.message || error.message}`);
  }
}

// 运行验证
verifyJWTInstallation().catch(error => {
  console.error('验证过程中发生错误:', error);
});