#!/usr/bin/env node

/**
 * JWT插件安装详细诊断
 * 检查为什么JWT端点仍然返回404
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';

// 创建不验证SSL的axios实例
const client = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 10000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Debug/1.0'
  }
});

async function debugJWTInstallation() {
  console.log('🔍 JWT插件安装详细诊断\n');
  console.log(`WordPress站点: ${WORDPRESS_URL}`);
  console.log(`诊断时间: ${new Date().toISOString()}`);
  console.log('='.repeat(70) + '\n');
  
  // 1. 检查WordPress基本信息
  console.log('1. 📊 WordPress基本信息检查');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  try {
    const wpInfo = await client.get(`${WORDPRESS_URL}/wp-json`);
    console.log('✅ WordPress REST API可用');
    console.log(`   站点名称: ${wpInfo.data.name || '未设置'}`);
    console.log(`   API命名空间: ${wpInfo.data.namespaces?.join(', ') || '未知'}`);
    
    // 检查是否有jwt相关路由
    const jwtRoutes = Object.keys(wpInfo.data.routes || {}).filter(route => 
      route.includes('jwt') || route.includes('auth')
    );
    
    if (jwtRoutes.length > 0) {
      console.log(`\n🎯 发现的JWT/Auth相关路由:`);
      jwtRoutes.forEach(route => {
        console.log(`   - ${route}`);
      });
    } else {
      console.log(`\n⚠️  路由表中未发现JWT/Auth相关路由`);
    }
  } catch (error) {
    console.log(`❌ 无法获取WordPress信息: ${error.message}`);
  }
  
  // 2. 测试所有可能的JWT端点
  console.log('\n2. 🔐 测试所有JWT端点格式');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  const endpoints = [
    { url: '/wp-json/jwt-auth/v1/token', desc: '标准JWT端点' },
    { url: '/wp-json/jwt-auth/v1/token/validate', desc: 'JWT验证端点' },
    { url: '/?rest_route=/jwt-auth/v1/token', desc: 'rest_route格式' },
    { url: '/index.php?rest_route=/jwt-auth/v1/token', desc: 'index.php格式' },
    { url: '/wp-json/api/v1/token', desc: 'API v1格式' },
    { url: '/wp-json/api/jwt/token', desc: 'API JWT格式' }
  ];
  
  for (const endpoint of endpoints) {
    try {
      const response = await client.get(WORDPRESS_URL + endpoint.url);
      console.log(`✅ ${endpoint.desc}: 可用 (${response.status})`);
      
      if (response.data && typeof response.data === 'object') {
        if (response.data.code === 'jwt_auth_no_auth_header') {
          console.log(`   🔍 端点存在但需要认证头`);
        }
      }
    } catch (error) {
      const status = error.response?.status;
      if (status === 404) {
        console.log(`❌ ${endpoint.desc}: 不存在 (404)`);
      } else if (status === 405) {
        console.log(`✅ ${endpoint.desc}: 存在 (需要POST请求)`);
      } else if (status === 500) {
        console.log(`🔥 ${endpoint.desc}: 服务器错误 (500)`);
        if (error.response?.data) {
          console.log(`   错误: ${JSON.stringify(error.response.data).substring(0, 100)}`);
        }
      } else {
        console.log(`⚠️  ${endpoint.desc}: 错误 (${status || error.message})`);
      }
    }
  }
  
  // 3. 尝试POST请求获取令牌
  console.log('\n3. 🚀 尝试POST请求获取JWT令牌');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  const postEndpoints = [
    '/wp-json/jwt-auth/v1/token',
    '/?rest_route=/jwt-auth/v1/token'
  ];
  
  for (const endpoint of postEndpoints) {
    console.log(`\n   尝试端点: ${endpoint}`);
    
    try {
      const response = await client.post(
        WORDPRESS_URL + endpoint,
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
      
      console.log(`   ✅ POST请求成功 (${response.status})`);
      
      if (response.data) {
        if (response.data.token) {
          console.log(`   🎉 获取到JWT令牌!`);
          console.log(`      令牌: ${response.data.token.substring(0, 30)}...`);
          console.log(`      用户: ${response.data.user_display_name || response.data.user_email}`);
          console.log(`      有效期: ${response.data.expires_in || '未知'} 秒`);
          
          // 立即测试使用令牌
          await testWithToken(response.data.token);
          return; // 成功，停止测试
        } else {
          console.log(`   ⚠️  响应中没有token字段`);
          console.log(`      响应: ${JSON.stringify(response.data).substring(0, 150)}`);
        }
      }
    } catch (error) {
      const status = error.response?.status;
      
      if (status === 404) {
        console.log(`   ❌ 端点不存在 (404)`);
      } else if (status === 401 || status === 403) {
        console.log(`   ❌ 认证失败: ${error.response?.data?.message || '用户名或密码错误'}`);
      } else if (status === 500) {
        console.log(`   🔥 服务器错误 (500)`);
        
        if (error.response?.data) {
          const errorData = error.response.data;
          console.log(`      错误信息: ${errorData.message || '未知错误'}`);
          console.log(`      错误代码: ${errorData.code || '未知'}`);
          
          // 分析常见JWT错误
          if (errorData.code === 'jwt_auth_bad_config') {
            console.log(`\n🔧 JWT配置错误: 需要在wp-config.php中添加:`);
            console.log(`   define('JWT_AUTH_SECRET_KEY', 'your-secret-key');`);
            console.log(`   define('JWT_AUTH_CORS_ENABLE', true);`);
          } else if (errorData.code === 'jwt_auth_no_secret_key') {
            console.log(`\n🔧 JWT密钥未设置: 需要配置JWT_AUTH_SECRET_KEY`);
          }
        }
      } else {
        console.log(`   ❌ 请求失败: ${status || error.message}`);
      }
    }
  }
  
  // 4. 检查插件是否真的安装
  console.log('\n4. 🧩 检查插件安装状态');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  console.log('   需要手动检查:');
  console.log('   1. 访问 https://your-site.com/wp-admin/plugins.php');
  console.log('   2. 确认 "JWT Authentication for WP REST API" 已激活');
  console.log('   3. 检查是否有错误消息');
  
  // 5. 检查wp-config.php配置
  console.log('\n5. ⚙️  检查wp-config.php配置');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  console.log('   需要检查wp-config.php是否包含:');
  console.log(`
   // JWT配置
   define('JWT_AUTH_SECRET_KEY', 'your-strong-secret-key');
   define('JWT_AUTH_CORS_ENABLE', true);
  `);
  
  console.log('\n   如果没有配置，需要:');
  console.log('   1. 编辑wp-config.php文件');
  console.log('   2. 添加上述配置');
  console.log('   3. 生成安全密钥: openssl rand -base64 32');
  
  // 6. 检查固定链接
  console.log('\n6. 🔗 检查固定链接设置');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  console.log('   需要检查:');
  console.log('   1. 访问 https://your-site.com/wp-admin/options-permalink.php');
  console.log('   2. 选择"文章名"或"数字"格式');
  console.log('   3. 点击"保存更改"');
  
  // 7. 最终建议
  console.log('\n' + '='.repeat(70));
  console.log('📋 诊断总结和建议\n');
  
  console.log('🎯 当前状态: JWT端点仍然返回404');
  console.log('\n🔧 可能的原因和解决方案:');
  
  console.log('\nA. 插件未正确激活 (最常见)');
  console.log('   1. 登录WordPress后台');
  console.log('   2. 进入 插件 → 已安装的插件');
  console.log('   3. 找到 "JWT Authentication for WP REST API"');
  console.log('   4. 确保已激活（不是仅安装）');
  
  console.log('\nB. wp-config.php未配置');
  console.log('   1. 编辑 wp-config.php 文件');
  console.log('   2. 添加JWT配置（见上面）');
  console.log('   3. 生成并设置安全密钥');
  
  console.log('\nC. 固定链接问题');
  console.log('   1. 重新保存固定链接设置');
  console.log('   2. 检查 .htaccess 文件权限');
  
  console.log('\nD. 插件冲突');
  console.log('   1. 暂时禁用其他插件');
  console.log('   2. 只启用JWT插件测试');
  
  console.log('\n🚀 立即行动步骤:');
  console.log('   1. ✅ 确认插件已激活');
  console.log('   2. ✅ 配置 wp-config.php');
  console.log('   3. ✅ 重新保存固定链接');
  console.log('   4. ✅ 清除WordPress缓存');
  
  console.log('\n📞 需要的信息:');
  console.log('   1. 插件是否显示为"已激活"？');
  console.log('   2. wp-config.php是否已配置JWT密钥？');
  console.log('   3. 是否有服务器错误日志？');
}

async function testWithToken(jwtToken) {
  console.log('\n' + '='.repeat(70));
  console.log('🎯 使用JWT令牌测试API访问\n');
  
  try {
    const api = axios.create({
      baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
      headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    // 测试用户信息
    console.log('1. 测试用户信息访问...');
    const userResponse = await api.get('/users/me');
    console.log(`   ✅ 成功: ${userResponse.data.name}`);
    console.log(`      角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
    
    // 测试文章发布
    console.log('\n2. 测试文章发布...');
    const postData = {
      title: `JWT测试 ${Date.now()}`,
      content: 'JWT令牌认证测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const postResponse = await api.post('/posts', postData);
    console.log(`   🎉 文章发布成功!`);
    console.log(`      文章ID: ${postResponse.data.id}`);
    console.log(`      标题: ${postResponse.data.title.rendered}`);
    
    // 清理测试文章
    console.log('\n3. 清理测试文章...');
    await api.delete(`/posts/${postResponse.data.id}?force=true`);
    console.log('   ✅ 文章已清理');
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ JWT插件安装配置成功!');
    console.log('\n🚀 可以开始自动发布文章了!');
    
  } catch (error) {
    console.log(`❌ JWT令牌测试失败: ${error.response?.data?.message || error.message}`);
  }
}

// 运行诊断
debugJWTInstallation().catch(error => {
  console.error('诊断过程中发生错误:', error);
});