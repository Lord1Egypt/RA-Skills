#!/usr/bin/env node

/**
 * WordPress Basic Auth测试
 * 测试不同的认证方式
 */

const axios = require('axios');

// WordPress配置
const config = {
  url: 'https://your-site.com',
  username: 'admin',
  password: 'HnK3 o7xu KHNy DFtV 2fpZ 7uwG'
};

async function testBasicAuth() {
  console.log('🔐 测试WordPress Basic Auth认证...\n');
  console.log(`WordPress站点: ${config.url}`);
  console.log(`用户名: ${config.username}`);
  console.log('---\n');
  
  // 测试不同的认证方式
  const testCases = [
    {
      name: '方式1: Basic Auth (用户名:密码)',
      api: axios.create({
        baseURL: `${config.url}/wp-json/wp/v2`,
        auth: {
          username: config.username,
          password: config.password
        },
        headers: {
          'Content-Type': 'application/json'
        }
      })
    },
    {
      name: '方式2: Basic Auth (base64编码)',
      api: axios.create({
        baseURL: `${config.url}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Basic ${Buffer.from(`${config.username}:${config.password}`).toString('base64')}`,
          'Content-Type': 'application/json'
        }
      })
    },
    {
      name: '方式3: 应用程序密码 (用户名:应用程序密码)',
      api: axios.create({
        baseURL: `${config.url}/wp-json/wp/v2`,
        auth: {
          username: config.username,
          password: config.password
        },
        headers: {
          'Content-Type': 'application/json'
        }
      })
    }
  ];
  
  for (const testCase of testCases) {
    console.log(`\n📋 测试: ${testCase.name}`);
    
    try {
      // 测试1: 获取当前用户
      console.log('  1. 获取当前用户信息...');
      try {
        const response = await testCase.api.get('/users/me');
        console.log(`  ✅ 成功: ${response.data.username} (ID: ${response.data.id})`);
      } catch (error) {
        console.log(`  ❌ 失败: ${error.response?.data?.message || error.message}`);
      }
      
      // 测试2: 获取文章列表
      console.log('  2. 获取文章列表...');
      try {
        const response = await testCase.api.get('/posts?per_page=1');
        console.log(`  ✅ 成功: 获取到 ${response.data.length} 篇文章`);
      } catch (error) {
        console.log(`  ❌ 失败: ${error.response?.data?.message || error.message}`);
      }
      
      // 测试3: 创建测试文章
      console.log('  3. 创建测试文章...');
      try {
        const postData = {
          title: 'Basic Auth测试 ' + Date.now(),
          content: '这是一个通过Basic Auth创建的测试文章',
          status: 'draft',
          excerpt: '测试摘要'
        };
        
        const response = await testCase.api.post('/posts', postData);
        console.log(`  ✅ 成功: 文章ID ${response.data.id}`);
        
        // 清理测试文章
        try {
          await testCase.api.delete(`/posts/${response.data.id}?force=true`);
          console.log(`  ✅ 清理: 文章已删除`);
        } catch (deleteError) {
          console.log(`  ⚠️  清理失败: ${deleteError.message}`);
        }
      } catch (error) {
        console.log(`  ❌ 失败: ${error.response?.data?.message || error.message}`);
      }
      
    } catch (error) {
      console.log(`  ❌ 测试异常: ${error.message}`);
    }
  }
  
  console.log('\n🎯 测试完成！');
  console.log('\n📋 建议:');
  console.log('1. 检查WordPress是否启用了REST API');
  console.log('2. 检查用户是否有发布文章的权限');
  console.log('3. 考虑使用应用程序密码而不是登录密码');
  console.log('4. 或者安装JWT插件使用JWT认证');
}

// 运行测试
testBasicAuth();