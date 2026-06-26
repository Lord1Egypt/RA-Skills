#!/usr/bin/env node

/**
 * 查找正确的JWT端点URL
 * WordPress可能有不同的URL结构
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';

// 创建axios实例
const client = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 10000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Endpoint-Finder/1.0'
  }
});

// 所有可能的JWT端点URL模式
const POSSIBLE_ENDPOINTS = [
  // 标准格式（WordPress 4.7+，固定链接启用）
  { url: '/wp-json/jwt-auth/v1/token', name: '标准wp-json格式' },
  { url: '/wp-json/jwt-auth/v1/token/validate', name: '标准验证端点' },
  
  // 旧格式（WordPress 4.4-4.6）
  { url: '/?rest_route=/jwt-auth/v1/token', name: 'rest_route参数格式' },
  { url: '/index.php?rest_route=/jwt-auth/v1/token', name: 'index.php rest_route格式' },
  
  // 插件特定格式
  { url: '/wp-json/api/v1/token', name: '插件API v1格式' },
  { url: '/wp-json/api/v1/jwt/token', name: '插件JWT格式' },
  { url: '/wp-json/api/v1/auth', name: '插件Auth格式' },
  
  // 自定义端点
  { url: '/api/jwt/token', name: '自定义API端点' },
  { url: '/api/auth/token', name: '自定义Auth端点' },
  { url: '/api/v1/jwt-auth', name: '自定义v1端点' },
  
  // 其他常见格式
  { url: '/?oauth=token', name: 'OAuth格式' },
  { url: '/oauth/token', name: 'OAuth2格式' },
  { url: '/auth/jwt', name: '简单Auth格式' },
  
  // 测试所有wp-json命名空间
  { url: '/wp-json/wp/v2', name: 'WordPress核心API' },
  { url: '/wp-json/oembed/1.0', name: 'oEmbed端点' },
  
  // 检查插件是否使用不同路径
  { url: '/?jwt_auth_token', name: '查询参数格式' },
  { url: '/wp-admin/admin-ajax.php?action=jwt_auth_token', name: 'Admin AJAX格式' }
];

async function testEndpoint(endpoint) {
  const fullUrl = WORDPRESS_URL + endpoint.url;
  
  try {
    // 首先尝试GET请求（端点可能只接受POST，但GET会返回405而不是404）
    const response = await client.get(fullUrl);
    
    return {
      success: true,
      url: endpoint.url,
      name: endpoint.name,
      status: response.status,
      method: 'GET',
      data: response.data
    };
  } catch (error) {
    const status = error.response?.status;
    
    // 405表示方法不允许，但端点存在（应该用POST）
    if (status === 405) {
      return {
        success: true,
        url: endpoint.url,
        name: endpoint.name,
        status: status,
        method: '需要POST',
        error: '方法不允许（应用POST请求）'
      };
    }
    
    // 404表示端点不存在
    if (status === 404) {
      return {
        success: false,
        url: endpoint.url,
        name: endpoint.name,
        status: status,
        error: '端点不存在'
      };
    }
    
    // 其他错误
    return {
      success: false,
      url: endpoint.url,
      name: endpoint.name,
      status: status || '未知',
      error: error.message
    };
  }
}

async function discoverEndpoints() {
  console.log('🔍 JWT端点URL发现工具\n');
  console.log(`WordPress站点: ${WORDPRESS_URL}`);
  console.log(`开始时间: ${new Date().toISOString()}`);
  console.log('='.repeat(70) + '\n');
  
  console.log('📋 测试所有可能的JWT端点URL...\n');
  
  const results = [];
  
  // 批量测试所有端点
  for (const endpoint of POSSIBLE_ENDPOINTS) {
    process.stdout.write(`测试: ${endpoint.name.padEnd(30)} ${endpoint.url}... `);
    
    const result = await testEndpoint(endpoint);
    results.push(result);
    
    if (result.success) {
      if (result.method === '需要POST') {
        console.log(`✅ 存在 (需要POST请求)`);
      } else {
        console.log(`✅ 存在 (状态: ${result.status})`);
      }
    } else {
      console.log(`❌ 不存在`);
    }
    
    // 避免请求过快
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // 分析结果
  console.log('\n' + '='.repeat(70));
  console.log('📊 分析结果\n');
  
  const existingEndpoints = results.filter(r => r.success);
  const possibleJWTEndpoints = existingEndpoints.filter(e => 
    e.url.includes('jwt') || 
    e.url.includes('auth') || 
    e.url.includes('token') ||
    e.name.includes('JWT') ||
    e.name.includes('Auth') ||
    e.name.includes('Token')
  );
  
  if (existingEndpoints.length === 0) {
    console.log('❌ 没有找到任何API端点');
    console.log('\n🔧 可能的问题:');
    console.log('1. WordPress REST API未启用');
    console.log('2. 服务器配置阻止了API访问');
    console.log('3. 站点URL不正确');
    return;
  }
  
  console.log(`✅ 找到 ${existingEndpoints.length} 个可访问的端点`);
  
  if (possibleJWTEndpoints.length > 0) {
    console.log(`\n🎯 可能的JWT端点:`);
    possibleJWTEndpoints.forEach(endpoint => {
      console.log(`   ${endpoint.method === '需要POST' ? '🔐' : '✅'} ${endpoint.name}`);
      console.log(`        URL: ${endpoint.url}`);
      console.log(`        状态: ${endpoint.status}`);
      if (endpoint.method === '需要POST') {
        console.log(`        注意: 需要使用POST请求`);
      }
      console.log('');
    });
  } else {
    console.log('\n⚠️  没有找到明显的JWT端点');
    console.log('   可能是:');
    console.log('   1. JWT插件未安装');
    console.log('   2. 插件使用非标准端点');
    console.log('   3. 需要检查WordPress后台');
  }
  
  // 检查WordPress REST API结构
  console.log('\n🔍 WordPress REST API结构分析');
  
  try {
    const wpJson = await client.get(WORDPRESS_URL + '/wp-json');
    
    if (wpJson.data && wpJson.data.routes) {
      console.log(`✅ WordPress REST API可用`);
      console.log(`   站点名称: ${wpJson.data.name || '未设置'}`);
      console.log(`   API命名空间: ${wpJson.data.namespaces?.join(', ') || '未知'}`);
      
      // 查找所有包含jwt或auth的路由
      const jwtRoutes = Object.keys(wpJson.data.routes).filter(route => 
        route.toLowerCase().includes('jwt') || 
        route.toLowerCase().includes('auth')
      );
      
      if (jwtRoutes.length > 0) {
        console.log(`\n🎯 发现的JWT/Auth相关路由:`);
        jwtRoutes.forEach(route => {
          console.log(`   - ${route}`);
          const methods = wpJson.data.routes[route]?.methods || [];
          console.log(`     支持方法: ${Array.isArray(methods) ? methods.join(', ') : '未知'}`);
        });
      } else {
        console.log(`\n⚠️  在路由表中未找到JWT/Auth相关路由`);
        console.log(`   前10个可用路由:`);
        Object.keys(wpJson.data.routes).slice(0, 10).forEach(route => {
          console.log(`   - ${route}`);
        });
        if (Object.keys(wpJson.data.routes).length > 10) {
          console.log(`   ... 还有 ${Object.keys(wpJson.data.routes).length - 10} 个路由`);
        }
      }
    }
  } catch (error) {
    console.log(`❌ 无法获取WordPress REST API结构: ${error.message}`);
  }
  
  // 测试POST请求到可能的端点
  console.log('\n' + '='.repeat(70));
  console.log('🚀 测试JWT令牌获取\n');
  
  if (possibleJWTEndpoints.length > 0) {
    console.log('尝试使用POST请求获取JWT令牌...\n');
    
    for (const endpoint of possibleJWTEndpoints.slice(0, 3)) { // 只测试前3个
      if (endpoint.method === '需要POST' || endpoint.url.includes('token') || endpoint.url.includes('auth')) {
        console.log(`测试: ${endpoint.url}`);
        
        try {
          const postResponse = await client.post(
            WORDPRESS_URL + endpoint.url,
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
          
          console.log(`✅ POST请求成功!`);
          console.log(`   状态码: ${postResponse.status}`);
          
          if (postResponse.data) {
            if (postResponse.data.token) {
              console.log(`   🎉 找到JWT令牌!`);
              console.log(`      令牌: ${postResponse.data.token.substring(0, 30)}...`);
              console.log(`      用户: ${postResponse.data.user_email || '未知'}`);
              
              // 保存成功的配置
              console.log('\n📋 成功配置:');
              console.log(`   JWT端点: ${endpoint.url}`);
              console.log(`   请求方法: POST`);
              console.log(`   内容类型: application/json`);
              console.log(`   请求体: {"username":"admin","password":"你的密码"}`);
              
              return; // 找到有效的端点，停止测试
            } else {
              console.log(`   响应数据: ${JSON.stringify(postResponse.data).substring(0, 100)}...`);
            }
          }
        } catch (postError) {
          const status = postError.response?.status;
          console.log(`❌ POST请求失败: ${status || postError.message}`);
          
          if (postError.response?.data) {
            console.log(`   错误信息: ${JSON.stringify(postError.response.data).substring(0, 150)}`);
          }
        }
        
        console.log('');
      }
    }
  }
  
  // 最终建议
  console.log('\n' + '='.repeat(70));
  console.log('📋 最终建议\n');
  
  console.log('1. 🔧 检查WordPress后台:');
  console.log('   访问 https://your-site.com/wp-admin/plugins.php');
  console.log('   确认"JWT Authentication for WP REST API"插件已安装并激活');
  
  console.log('\n2. ⚙️  检查插件设置:');
  console.log('   有些JWT插件可能有设置页面');
  console.log('   检查插件是否启用了自定义端点');
  
  console.log('\n3. 🔍 手动检查:');
  console.log('   在浏览器中访问: https://your-site.com/wp-json');
  console.log('   搜索"jwt"或"auth"查看可用端点');
  
  console.log('\n4. 📝 如果还是找不到:');
  console.log('   考虑使用WordPress内置的应用程序密码功能');
  console.log('   或者安装其他REST API认证插件');
  
  console.log('\n5. 🚀 备用方案:');
  console.log('   使用Basic Auth或OAuth插件');
  console.log('   或者配置应用程序密码');
}

// 运行发现工具
discoverEndpoints().catch(error => {
  console.error('发现过程中发生错误:', error);
});