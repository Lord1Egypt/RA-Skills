#!/usr/bin/env node

/**
 * JWT插件终极测试
 * 测试所有可能的问题
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
    'User-Agent': 'OpenClaw-Ultimate-JWT-Test/1.0'
  }
});

async function ultimateTest() {
  console.log('🚀 JWT插件终极问题诊断\n');
  console.log(`站点: ${WORDPRESS_URL}`);
  console.log(`用户: ${USERNAME}`);
  console.log('='.repeat(70) + '\n');
  
  // 阶段1: 基础连接测试
  console.log('阶段1: 🔧 基础连接测试');
  console.log('-'.repeat(40));
  
  try {
    // 测试WordPress是否可访问
    const homeResponse = await client.get(WORDPRESS_URL);
    console.log(`✅ WordPress可访问 (${homeResponse.status})`);
    
    // 测试REST API
    const apiResponse = await client.get(`${WORDPRESS_URL}/wp-json`);
    console.log(`✅ REST API可用 (${apiResponse.status})`);
    console.log(`   版本: ${apiResponse.data.version || '未知'}`);
    
    // 检查wp/v2命名空间
    if (apiResponse.data.namespaces && apiResponse.data.namespaces.includes('wp/v2')) {
      console.log(`✅ WordPress 4.7+ API可用`);
    }
    
  } catch (error) {
    console.log(`❌ 基础连接失败: ${error.message}`);
    return;
  }
  
  // 阶段2: JWT插件状态测试
  console.log('\n阶段2: 🔍 JWT插件状态测试');
  console.log('-'.repeat(40));
  
  // 测试所有可能的JWT端点
  const testCases = [
    { method: 'GET', url: '/wp-json/jwt-auth/v1/token', desc: '标准GET测试' },
    { method: 'POST', url: '/wp-json/jwt-auth/v1/token', desc: '标准POST测试' },
    { method: 'GET', url: '/?rest_route=/jwt-auth/v1/token', desc: 'rest_route GET' },
    { method: 'POST', url: '/?rest_route=/jwt-auth/v1/token', desc: 'rest_route POST' }
  ];
  
  let foundEndpoint = false;
  
  for (const test of testCases) {
    try {
      let response;
      
      if (test.method === 'GET') {
        response = await client.get(WORDPRESS_URL + test.url);
      } else {
        response = await client.post(
          WORDPRESS_URL + test.url,
          { username: USERNAME, password: PASSWORD },
          { headers: { 'Content-Type': 'application/json' } }
        );
      }
      
      console.log(`✅ ${test.desc}: ${response.status}`);
      
      if (response.status === 405 && test.method === 'GET') {
        console.log(`   🔍 端点存在，需要${test.method === 'GET' ? 'POST' : 'GET'}请求`);
        foundEndpoint = true;
      }
      
      if (response.data && response.data.token) {
        console.log(`   🎉 获取到JWT令牌!`);
        await testJWTWorkflow(response.data.token);
        return;
      }
      
      if (response.data && response.data.code) {
        console.log(`   🔍 错误代码: ${response.data.code}`);
        console.log(`       消息: ${response.data.message}`);
        
        // 分析常见错误
        analyzeJWTError(response.data.code, response.data.message);
      }
      
    } catch (error) {
      const status = error.response?.status;
      const data = error.response?.data;
      
      if (status === 404) {
        console.log(`❌ ${test.desc}: 端点不存在 (404)`);
      } else if (status === 405) {
        console.log(`✅ ${test.desc}: 端点存在 (需要${test.method === 'GET' ? 'POST' : 'GET'}请求)`);
        foundEndpoint = true;
      } else if (status === 500) {
        console.log(`🔥 ${test.desc}: 服务器错误 (500)`);
        if (data) {
          console.log(`   错误: ${data.message || '未知'}`);
          console.log(`   代码: ${data.code || '未知'}`);
          analyzeJWTError(data.code, data.message);
        }
      } else if (status === 401 || status === 403) {
        console.log(`🔒 ${test.desc}: 认证失败 (${status})`);
        if (data && data.message) {
          console.log(`   消息: ${data.message}`);
        }
      } else {
        console.log(`⚠️  ${test.desc}: 错误 (${status || error.message})`);
      }
    }
  }
  
  // 阶段3: 问题分析和解决方案
  console.log('\n阶段3: 📋 问题分析和解决方案');
  console.log('-'.repeat(40));
  
  if (!foundEndpoint) {
    console.log('❌ 没有找到任何JWT端点');
    console.log('\n🔧 这意味着:');
    console.log('   1. JWT插件未安装 或');
    console.log('   2. 插件已安装但未激活 或');
    console.log('   3. 插件激活但有严重配置错误');
    
    console.log('\n🚀 解决方案:');
    console.log('   1. 确认插件状态:');
    console.log('      访问 https://your-site.com/wp-admin/plugins.php');
    console.log('      找到JWT插件，确认显示"已激活"');
    
    console.log('\n   2. 检查wp-config.php配置:');
    console.log('      必须包含:');
    console.log('      define(\'JWT_AUTH_SECRET_KEY\', \'your-key\');');
    console.log('      define(\'JWT_AUTH_CORS_ENABLE\', true);');
    
    console.log('\n   3. 重新保存固定链接:');
    console.log('      访问 https://your-site.com/wp-admin/options-permalink.php');
    console.log('      点击"保存更改"');
    
    console.log('\n   4. 检查插件冲突:');
    console.log('      暂时禁用其他所有插件');
    console.log('      只启用JWT插件测试');
    
    console.log('\n   5. 检查服务器错误日志:');
    console.log('      查看PHP错误日志');
    console.log('      检查Nginx/Apache错误日志');
  } else {
    console.log('✅ JWT端点存在，但可能配置有问题');
    console.log('\n🔧 需要检查:');
    console.log('   1. JWT密钥配置是否正确');
    console.log('   2. 用户名和密码是否正确');
    console.log('   3. 用户是否有API访问权限');
  }
  
  // 阶段4: 备选方案
  console.log('\n阶段4: 🔄 备选方案');
  console.log('-'.repeat(40));
  
  console.log('如果JWT插件无法工作，考虑:');
  console.log('\n方案A: 使用WordPress应用程序密码');
  console.log('   1. 访问 https://your-site.com/wp-admin/profile.php');
  console.log('   2. 创建应用程序密码');
  console.log('   3. 使用Basic Auth访问API');
  
  console.log('\n方案B: 安装其他认证插件');
  console.log('   1. Application Passwords (官方)');
  console.log('   2. OAuth2 Server');
  console.log('   3. Basic Authentication');
  
  console.log('\n方案C: 检查当前密码是否可用');
  console.log('   运行: node app-password-test.js');
  
  console.log('\n' + '='.repeat(70));
  console.log('🎯 诊断完成');
  console.log('\n📞 需要的信息:');
  console.log('   1. 插件确切状态 (已激活?)');
  console.log('   2. wp-config.php 是否已配置JWT?');
  console.log('   3. 是否有服务器错误日志?');
}

function analyzeJWTError(code, message) {
  console.log('\n🔍 错误分析:');
  
  switch(code) {
    case 'jwt_auth_bad_config':
      console.log('   ❌ JWT配置错误');
      console.log('      需要在 wp-config.php 中添加:');
      console.log('      define(\'JWT_AUTH_SECRET_KEY\', \'your-key\');');
      console.log('      define(\'JWT_AUTH_CORS_ENABLE\', true);');
      break;
      
    case 'jwt_auth_no_secret_key':
      console.log('   ❌ JWT密钥未设置');
      console.log('      必须配置 JWT_AUTH_SECRET_KEY');
      break;
      
    case 'jwt_auth_invalid_token':
      console.log('   ❌ JWT令牌无效');
      console.log('      可能: 令牌过期或格式错误');
      break;
      
    case 'rest_cannot_create':
      console.log('   ❌ 用户没有创建权限');
      console.log('      需要作者或以上角色');
      break;
      
    default:
      if (message) {
        console.log(`   ⚠️  ${message}`);
      }
  }
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
    const user = await api.get('/users/me');
    console.log(`✅ 用户认证: ${user.data.name}`);
    
    // 测试文章发布
    const postData = {
      title: `终极测试 ${Date.now()}`,
      content: 'JWT终极测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const post = await api.post('/posts', postData);
    console.log(`✅ 文章发布: ID ${post.data.id}`);
    
    // 清理
    await api.delete(`/posts/${post.data.id}?force=true`);
    console.log('✅ 测试清理完成');
    
    console.log('\n🎉 JWT插件完全工作正常!');
    console.log('\n📋 成功配置:');
    console.log(`   端点: ${WORDPRESS_URL}/wp-json/jwt-auth/v1/token`);
    console.log(`   令牌: ${token.substring(0, 30)}...`);
    
  } catch (error) {
    console.log(`❌ JWT工作流程失败: ${error.response?.data?.message || error.message}`);
  }
}

// 运行终极测试
ultimateTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});