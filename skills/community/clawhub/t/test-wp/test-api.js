#!/usr/bin/env node

/**
 * WordPress REST API基础测试
 * 测试API是否可用，无需认证
 */

const axios = require('axios');

// WordPress配置
const config = {
  url: 'https://your-site.com'
};

async function testAPI() {
  console.log('🌐 测试WordPress REST API可用性...\n');
  console.log(`WordPress站点: ${config.url}`);
  console.log('---\n');
  
  const api = axios.create({
    baseURL: `${config.url}/wp-json`,
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  try {
    // 测试1: 获取WordPress信息
    console.log('1. 获取WordPress基本信息...');
    try {
      const response = await api.get('/');
      console.log('✅ WordPress REST API可用！');
      console.log(`   名称: ${response.data.name}`);
      console.log(`   描述: ${response.data.description}`);
      console.log(`   URL: ${response.data.url}`);
      console.log(`   REST API版本: ${response.data.namespaces ? response.data.namespaces.join(', ') : '未知'}`);
      
      // 显示可用的端点
      if (response.data.routes) {
        console.log('\n   可用的API端点:');
        const endpoints = Object.keys(response.data.routes).slice(0, 10); // 只显示前10个
        endpoints.forEach(endpoint => {
          console.log(`     - ${endpoint}`);
        });
        if (Object.keys(response.data.routes).length > 10) {
          console.log(`     ... 还有 ${Object.keys(response.data.routes).length - 10} 个端点`);
        }
      }
    } catch (error) {
      console.log('❌ 获取WordPress信息失败:', error.message);
    }
    
    // 测试2: 获取文章列表（公开）
    console.log('\n2. 测试获取公开文章...');
    try {
      const response = await api.get('/wp/v2/posts?per_page=1');
      console.log(`✅ 成功获取 ${response.data.length} 篇公开文章`);
      if (response.data.length > 0) {
        console.log(`   最新文章: "${response.data[0].title.rendered}"`);
        console.log(`   文章ID: ${response.data[0].id}`);
        console.log(`   状态: ${response.data[0].status}`);
        console.log(`   链接: ${response.data[0].link}`);
      }
    } catch (error) {
      console.log('❌ 获取文章列表失败:', error.message);
    }
    
    // 测试3: 获取分类列表（公开）
    console.log('\n3. 测试获取分类...');
    try {
      const response = await api.get('/wp/v2/categories?per_page=5');
      console.log(`✅ 成功获取 ${response.data.length} 个分类`);
      response.data.forEach(cat => {
        console.log(`   - ${cat.name} (ID: ${cat.id}, 文章数: ${cat.count})`);
      });
    } catch (error) {
      console.log('❌ 获取分类失败:', error.message);
    }
    
    // 测试4: 检查用户端点
    console.log('\n4. 检查用户API端点...');
    try {
      const response = await api.get('/wp/v2/users?per_page=1');
      console.log(`✅ 用户端点可用，获取到 ${response.data.length} 个用户`);
      if (response.data.length > 0) {
        console.log(`   示例用户: ${response.data[0].name} (${response.data[0].slug})`);
      }
    } catch (error) {
      console.log('❌ 用户端点访问失败:', error.message);
      console.log('   可能需要认证才能访问用户端点');
    }
    
    // 测试5: 检查媒体端点
    console.log('\n5. 检查媒体API端点...');
    try {
      const response = await api.get('/wp/v2/media?per_page=1');
      console.log(`✅ 媒体端点可用，获取到 ${response.data.length} 个媒体文件`);
    } catch (error) {
      console.log('❌ 媒体端点访问失败:', error.message);
    }
    
    // 测试6: 检查认证相关端点
    console.log('\n6. 检查认证相关端点...');
    const authEndpoints = [
      '/wp/v2/users/me',
      '/jwt-auth/v1/token',
      '/basic-auth/v1/authenticate'
    ];
    
    for (const endpoint of authEndpoints) {
      try {
        const response = await api.get(endpoint);
        console.log(`✅ ${endpoint} 可用 (状态码: ${response.status})`);
      } catch (error) {
        if (error.response) {
          console.log(`❌ ${endpoint} 不可用 (状态码: ${error.response.status})`);
        } else {
          console.log(`❌ ${endpoint} 不可用: ${error.message}`);
        }
      }
    }
    
  } catch (error) {
    console.error('❌ 测试过程中发生错误:', error.message);
  }
  
  console.log('\n🎯 API测试完成！');
  console.log('\n📋 诊断结果:');
  console.log('1. 如果REST API基本可用，但认证失败，可能需要:');
  console.log('   - 安装Basic Auth插件 (如: Application Passwords)');
  console.log('   - 安装JWT Auth插件');
  console.log('   - 配置正确的用户权限');
  console.log('\n2. 推荐方案:');
  console.log('   - 使用WordPress的"应用程序密码"功能');
  console.log('   - 或者安装JWT插件获得更好的API认证体验');
}

// 运行测试
testAPI();