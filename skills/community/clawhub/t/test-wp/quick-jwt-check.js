#!/usr/bin/env node

/**
 * JWT插件快速检查
 * 在配置wp-config.php后运行
 */

const axios = require('axios');

const WORDPRESS_URL = 'https://your-site.com';

async function quickCheck() {
  console.log('🔍 JWT插件快速检查\n');
  console.log(`站点: ${WORDPRESS_URL}`);
  console.log('='.repeat(50) + '\n');
  
  // 1. 测试JWT端点是否存在
  console.log('1. 测试JWT端点...');
  try {
    const response = await axios.get(`${WORDPRESS_URL}/wp-json/jwt-auth/v1/token`);
    console.log(`   ✅ 端点响应: ${response.status}`);
    
    if (response.status === 405) {
      console.log('   🔍 端点存在，需要POST请求');
    }
  } catch (error) {
    if (error.response?.status === 404) {
      console.log('   ❌ 端点不存在 (404)');
      console.log('      可能: 插件未激活 或 wp-config.php未配置');
    } else if (error.response?.status === 500) {
      console.log('   🔥 服务器错误 (500)');
      console.log('      可能: JWT密钥配置错误');
    } else {
      console.log(`   ⚠️  错误: ${error.message}`);
    }
  }
  
  // 2. 尝试获取JWT令牌
  console.log('\n2. 尝试获取JWT令牌...');
  try {
    const response = await axios.post(
      `${WORDPRESS_URL}/wp-json/jwt-auth/v1/token`,
      {
        username: 'admin',
        password: 'your-app-password'
      },
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );
    
    if (response.data.token) {
      console.log('   🎉 JWT令牌获取成功!');
      console.log(`      令牌: ${response.data.token.substring(0, 30)}...`);
      console.log(`      用户: ${response.data.user_display_name}`);
      
      // 立即测试API访问
      console.log('\n3. 测试API访问...');
      const api = axios.create({
        baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${response.data.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      try {
        const userResponse = await api.get('/users/me');
        console.log(`   ✅ API访问成功: ${userResponse.data.name}`);
        
        // 测试发布
        console.log('\n4. 测试文章发布...');
        const postData = {
          title: `快速测试 ${Date.now()}`,
          content: 'JWT快速测试成功!',
          status: 'draft',
          categories: [1]
        };
        
        const postResponse = await api.post('/posts', postData);
        console.log(`   🎉 文章发布成功! ID: ${postResponse.data.id}`);
        
        // 清理
        await api.delete(`/posts/${postResponse.data.id}?force=true`);
        console.log('   ✅ 测试文章已清理');
        
        console.log('\n' + '='.repeat(50));
        console.log('✅ JWT插件配置成功! 可以开始自动发布。');
        
      } catch (apiError) {
        console.log(`   ❌ API访问失败: ${apiError.response?.data?.message || apiError.message}`);
      }
      
    } else {
      console.log('   ⚠️  响应中没有token字段');
      console.log(`      响应: ${JSON.stringify(response.data).substring(0, 100)}`);
    }
    
  } catch (error) {
    const status = error.response?.status;
    
    if (status === 404) {
      console.log('   ❌ JWT端点不存在 (404)');
      console.log('\n🔧 需要:');
      console.log('   1. 确认插件已激活');
      console.log('   2. 配置 wp-config.php');
      console.log('   3. 重新保存固定链接');
    } else if (status === 401 || status === 403) {
      console.log(`   ❌ 认证失败: ${error.response?.data?.message || '用户名或密码错误'}`);
    } else if (status === 500) {
      console.log('   🔥 服务器错误 (500)');
      console.log(`      错误: ${error.response?.data?.message || '未知错误'}`);
      console.log(`      代码: ${error.response?.data?.code || '未知'}`);
      
      if (error.response?.data?.code === 'jwt_auth_bad_config') {
        console.log('\n🔧 JWT配置错误:');
        console.log('   需要在 wp-config.php 中添加:');
        console.log("   define('JWT_AUTH_SECRET_KEY', 'your-secret-key');");
        console.log("   define('JWT_AUTH_CORS_ENABLE', true);");
      }
    } else {
      console.log(`   ❌ 错误: ${status || error.message}`);
    }
  }
  
  console.log('\n🎯 检查完成');
  console.log('\n📋 如果仍然失败:');
  console.log('   1. 确认插件状态: 已激活');
  console.log('   2. 确认 wp-config.php 已配置');
  console.log('   3. 重新保存固定链接');
  console.log('   4. 清除WordPress缓存');
}

quickCheck().catch(error => {
  console.error('检查过程中发生错误:', error);
});