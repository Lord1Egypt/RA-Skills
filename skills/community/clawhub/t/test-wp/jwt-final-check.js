#!/usr/bin/env node

/**
 * JWT插件最终检查脚本
 * 检查为什么JWT端点仍然404
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';

// 创建客户端
const client = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 15000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Final-Check/1.0'
  }
});

async function finalCheck() {
  console.log('🔍 JWT插件最终检查\n');
  console.log(`站点: ${WORDPRESS_URL}`);
  console.log('='.repeat(70) + '\n');
  
  // 1. 检查WordPress REST API
  console.log('1. 🌐 检查WordPress REST API...');
  try {
    const apiResponse = await client.get(`${WORDPRESS_URL}/wp-json`);
    console.log(`✅ REST API可用 (${apiResponse.status})`);
    
    // 检查所有路由
    const routes = Object.keys(apiResponse.data.routes || {});
    console.log(`   发现 ${routes.length} 个API端点`);
    
    // 查找任何包含"jwt"或"auth"的路由
    const authRoutes = routes.filter(route => 
      route.toLowerCase().includes('jwt') || 
      route.toLowerCase().includes('auth')
    );
    
    if (authRoutes.length > 0) {
      console.log(`\n🔍 发现认证相关路由:`);
      authRoutes.forEach(route => {
        console.log(`   - ${route}`);
      });
    } else {
      console.log(`\n⚠️  未发现JWT/Auth相关路由`);
    }
    
  } catch (error) {
    console.log(`❌ REST API检查失败: ${error.message}`);
    return;
  }
  
  // 2. 测试JWT端点
  console.log('\n2. 🔐 测试JWT端点...');
  
  const testCases = [
    { url: '/wp-json/jwt-auth/v1/token', desc: '标准JWT端点' },
    { url: '/wp-json/jwt-auth/v1/token/validate', desc: 'JWT验证端点' },
    { url: '/wp-json/api/v1/token', desc: 'API v1端点' },
    { url: '/wp-json/api/jwt/token', desc: 'API JWT端点' },
    { url: '/?rest_route=/jwt-auth/v1/token', desc: 'rest_route端点' }
  ];
  
  let anyEndpointFound = false;
  
  for (const test of testCases) {
    try {
      const response = await client.get(WORDPRESS_URL + test.url);
      console.log(`✅ ${test.desc}: 响应 ${response.status}`);
      
      if (response.status === 405) {
        console.log(`   🔍 端点存在，需要POST请求`);
        anyEndpointFound = true;
      }
      
    } catch (error) {
      const status = error.response?.status;
      
      if (status === 404) {
        console.log(`❌ ${test.desc}: 不存在 (404)`);
      } else if (status === 405) {
        console.log(`✅ ${test.desc}: 端点存在 (需要POST请求)`);
        anyEndpointFound = true;
      } else if (status === 500) {
        console.log(`🔥 ${test.desc}: 服务器错误 (500)`);
        anyEndpointFound = true; // 端点存在但有错误
      } else {
        console.log(`⚠️  ${test.desc}: 错误 (${status || error.message})`);
      }
    }
  }
  
  // 3. 尝试POST请求
  console.log('\n3. 🚀 尝试POST请求获取令牌...');
  
  const postEndpoints = [
    '/wp-json/jwt-auth/v1/token',
    '/?rest_route=/jwt-auth/v1/token'
  ];
  
  for (const endpoint of postEndpoints) {
    console.log(`\n   尝试: ${endpoint}`);
    
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
      
      if (response.data && response.data.token) {
        console.log(`   🎉 获取到JWT令牌!`);
        console.log(`      令牌: ${response.data.token.substring(0, 30)}...`);
        console.log(`      用户: ${response.data.user_display_name}`);
        
        // 立即测试
        await testWithToken(response.data.token);
        return;
      }
      
    } catch (error) {
      const status = error.response?.status;
      const data = error.response?.data;
      
      if (status === 404) {
        console.log(`   ❌ 端点不存在 (404)`);
      } else if (status === 500) {
        console.log(`   🔥 服务器错误 (500)`);
        
        if (data) {
          console.log(`      错误: ${data.message || '未知'}`);
          console.log(`      代码: ${data.code || '未知'}`);
          
          if (data.code === 'jwt_auth_bad_config' || data.code === 'jwt_auth_no_secret_key') {
            console.log(`\n🔧 JWT配置错误: 需要配置wp-config.php`);
          }
        }
      } else {
        console.log(`   ❌ 错误: ${status || error.message}`);
      }
    }
  }
  
  // 4. 分析结果
  console.log('\n' + '='.repeat(70));
  console.log('📋 检查结果分析\n');
  
  if (!anyEndpointFound) {
    console.log('❌ 结论: JWT插件没有正确工作');
    console.log('\n🔧 可能的原因:');
    console.log('   1. 插件已安装但未激活');
    console.log('   2. 插件激活但wp-config.php未配置');
    console.log('   3. 固定链接设置有问题');
    console.log('   4. 插件冲突');
    
    console.log('\n🚀 立即检查步骤:');
    console.log('   1. 访问 https://your-site.com/wp-admin/plugins.php');
    console.log('      - 确认JWT插件显示为"已激活"');
    console.log('      - 不是仅"已安装"，必须是"已激活"');
    
    console.log('\n   2. 检查wp-config.php配置');
    console.log('      - 必须包含:');
    console.log('        define(\'JWT_AUTH_SECRET_KEY\', \'your-key\');');
    console.log('        define(\'JWT_AUTH_CORS_ENABLE\', true);');
    
    console.log('\n   3. 重新保存固定链接');
    console.log('      - 访问 https://your-site.com/wp-admin/options-permalink.php');
    console.log('      - 点击"保存更改"');
    
    console.log('\n   4. 如果仍然失败:');
    console.log('      - 暂时禁用其他所有插件');
    console.log('      - 切换到默认主题');
    console.log('      - 检查服务器错误日志');
    
  } else {
    console.log('✅ 端点存在，但可能有配置问题');
  }
  
  // 5. 备选方案
  console.log('\n' + '='.repeat(70));
  console.log('🔄 备选方案: 使用应用程序密码\n');
  
  console.log('如果JWT配置太复杂，使用WordPress内置的应用程序密码:');
  console.log('\n步骤:');
  console.log('   1. 访问 https://your-site.com/wp-admin/profile.php');
  console.log('   2. 找到"应用程序密码"部分');
  console.log('   3. 创建密码: "OpenClaw-Auto-Publish"');
  console.log('   4. 复制生成的密码');
  console.log('   5. 运行测试: node test-with-app-password.js');
  
  console.log('\n优点:');
  console.log('   - 无需安装插件');
  console.log('   - 无需配置wp-config.php');
  console.log('   - 更简单，更稳定');
  
  console.log('\n' + '='.repeat(70));
  console.log('🎯 需要你确认:');
  console.log('   1. 插件是否确实显示为"已激活"？');
  console.log('   2. wp-config.php是否已配置JWT密钥？');
  console.log('   3. 是否重新保存了固定链接？');
}

async function testWithToken(token) {
  console.log('\n' + '='.repeat(70));
  console.log('🚀 JWT令牌测试\n');
  
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
      title: `JWT最终测试 ${Date.now()}`,
      content: 'JWT插件最终测试成功!',
      status: 'draft',
      categories: [1]
    };
    
    const post = await api.post('/posts', postData);
    console.log(`   🎉 文章发布成功! ID: ${post.data.id}`);
    
    // 清理
    await api.delete(`/posts/${post.data.id}?force=true`);
    console.log('   ✅ 测试文章已清理');
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ JWT插件工作正常! 可以开始自动发布。');
    
  } catch (error) {
    console.log(`❌ JWT测试失败: ${error.response?.data?.message || error.message}`);
  }
}

// 运行最终检查
finalCheck().catch(error => {
  console.error('检查过程中发生错误:', error);
});