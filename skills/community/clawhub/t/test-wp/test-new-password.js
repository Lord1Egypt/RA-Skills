#!/usr/bin/env node

/**
 * 测试新提供的密码
 */

const axios = require('axios');

// 测试不同的认证方式
const testCases = [
  {
    name: '新密码作为应用程序密码',
    username: 'admin',
    password: 'your-app-password'
  },
  {
    name: '新密码作为JWT密码',
    username: 'admin', 
    password: 'your-app-password'
  },
  {
    name: '新密码去掉空格',
    username: 'admin',
    password: 'SAGIb8ZiQBOmCQhWxl4NlmP1'
  }
];

const WORDPRESS_URL = 'https://your-site.com';

async function testAuthentication(testCase) {
  console.log(`\n🔐 测试: ${testCase.name}`);
  console.log(`   用户名: ${testCase.username}`);
  console.log(`   密码: ${testCase.password.substring(0, 10)}...`);
  
  // 测试Basic Auth
  try {
    const api = axios.create({
      baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
      auth: {
        username: testCase.username,
        password: testCase.password
      },
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const response = await api.get('/users/me');
    console.log(`   ✅ Basic Auth成功: ${response.data.username}`);
    return { method: 'basic', success: true, data: response.data };
  } catch (error) {
    console.log(`   ❌ Basic Auth失败: ${error.response?.data?.message || error.message}`);
  }
  
  // 测试JWT
  try {
    const jwtResponse = await axios.post(`${WORDPRESS_URL}/wp-json/jwt-auth/v1/token`, {
      username: testCase.username,
      password: testCase.password
    });
    
    if (jwtResponse.data.token) {
      console.log(`   ✅ JWT认证成功: 获取到令牌`);
      
      // 测试使用JWT访问API
      const jwtApi = axios.create({
        baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${jwtResponse.data.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      const userResponse = await jwtApi.get('/users/me');
      console.log(`   ✅ JWT API访问成功: ${userResponse.data.username}`);
      return { method: 'jwt', success: true, token: jwtResponse.data.token, data: userResponse.data };
    }
  } catch (error) {
    console.log(`   ❌ JWT认证失败: ${error.response?.status || error.message}`);
  }
  
  return { success: false };
}

async function runTests() {
  console.log('🔍 测试新提供的密码...');
  console.log(`WordPress站点: ${WORDPRESS_URL}`);
  console.log('---');
  
  let successfulMethod = null;
  
  for (const testCase of testCases) {
    const result = await testAuthentication(testCase);
    if (result.success) {
      successfulMethod = result.method;
      console.log(`\n🎉 找到有效的认证方式: ${testCase.name}`);
      console.log(`   方法: ${result.method}`);
      
      if (result.method === 'jwt') {
        console.log(`   JWT令牌: ${result.token.substring(0, 30)}...`);
        console.log(`\n📋 使用示例:`);
        console.log(`
const axios = require('axios');

const api = axios.create({
  baseURL: '${WORDPRESS_URL}/wp-json/wp/v2',
  headers: {
    'Authorization': 'Bearer ${result.token}',
    'Content-Type': 'application/json'
  }
});

// 发布文章
const postData = {
  title: '测试文章',
  content: '内容',
  status: 'draft'
};

const response = await api.post('/posts', postData);
        `);
      }
      
      break;
    }
  }
  
  if (!successfulMethod) {
    console.log('\n❌ 所有认证方式都失败了');
    console.log('\n🔧 建议:');
    console.log('1. 确认密码是否正确');
    console.log('2. 检查WordPress是否启用了REST API认证');
    console.log('3. 可能需要安装认证插件:');
    console.log('   - Application Passwords (WordPress内置)');
    console.log('   - JWT Authentication for WP REST API');
    console.log('4. 检查用户权限');
  }
  
  console.log('\n🎯 测试完成');
}

runTests();