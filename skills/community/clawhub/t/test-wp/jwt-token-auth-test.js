#!/usr/bin/env node

/**
 * JWT令牌认证完整测试
 * 包括JWT插件检查、令牌获取、API访问和文章发布
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';
const USERNAME = 'admin';
const PASSWORD = 'your-app-password';

// 创建不验证SSL的axios实例
const insecureAxios = axios.create({
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  timeout: 10000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Test/1.0'
  }
});

class JWTTokenTester {
  constructor() {
    this.jwtToken = null;
    this.tokenExpiry = null;
    this.userInfo = null;
  }
  
  async checkJWTPlugin() {
    console.log('🔍 检查JWT插件状态...\n');
    
    const jwtEndpoints = [
      '/wp-json/jwt-auth/v1/token',
      '/?rest_route=/jwt-auth/v1/token',
      '/index.php?rest_route=/jwt-auth/v1/token'
    ];
    
    let pluginInstalled = false;
    let workingEndpoint = null;
    
    for (const endpoint of jwtEndpoints) {
      try {
        const response = await insecureAxios.get(WORDPRESS_URL + endpoint);
        
        // 如果返回405，说明端点存在但需要POST请求
        if (response.status === 405) {
          console.log(`✅ ${endpoint}: JWT端点存在 (需要POST请求)`);
          pluginInstalled = true;
          workingEndpoint = endpoint;
          break;
        }
        
        // 如果返回200但包含错误信息
        if (response.status === 200) {
          console.log(`✅ ${endpoint}: JWT端点响应正常`);
          pluginInstalled = true;
          workingEndpoint = endpoint;
          break;
        }
        
      } catch (error) {
        const status = error.response?.status;
        
        if (status === 404) {
          console.log(`❌ ${endpoint}: 不存在 (404)`);
        } else if (status === 405) {
          console.log(`✅ ${endpoint}: JWT端点存在 (需要POST请求)`);
          pluginInstalled = true;
          workingEndpoint = endpoint;
          break;
        } else {
          console.log(`⚠️  ${endpoint}: 错误 (${status || error.message})`);
        }
      }
    }
    
    if (!pluginInstalled) {
      console.log('\n❌ JWT插件未安装或未激活');
      console.log('\n🔧 需要安装 "JWT Authentication for WP REST API" 插件:');
      console.log('   1. 访问 https://your-site.com/wp-admin/plugins.php');
      console.log('   2. 搜索并安装JWT插件');
      console.log('   3. 激活插件');
      console.log('   4. 配置 wp-config.php (添加JWT密钥)');
      return false;
    }
    
    console.log(`\n✅ JWT插件已安装，使用端点: ${workingEndpoint}`);
    return true;
  }
  
  async getJWTToken() {
    console.log('\n🔐 获取JWT令牌...');
    
    // 尝试不同的端点格式
    const endpoints = [
      '/wp-json/jwt-auth/v1/token',
      '/?rest_route=/jwt-auth/v1/token',
      '/index.php?rest_route=/jwt-auth/v1/token'
    ];
    
    for (const endpoint of endpoints) {
      try {
        console.log(`   尝试端点: ${endpoint}`);
        
        const response = await insecureAxios.post(
          WORDPRESS_URL + endpoint,
          {
            username: USERNAME,
            password: PASSWORD
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        
        if (response.data && response.data.token) {
          this.jwtToken = response.data.token;
          this.tokenExpiry = Date.now() + (response.data.expires_in || 300) * 1000;
          this.userInfo = {
            email: response.data.user_email,
            name: response.data.user_display_name,
            nicename: response.data.user_nicename
          };
          
          console.log(`✅ JWT令牌获取成功!`);
          console.log(`   令牌: ${this.jwtToken.substring(0, 30)}...`);
          console.log(`   用户: ${this.userInfo.name} (${this.userInfo.email})`);
          console.log(`   过期时间: ${new Date(this.tokenExpiry).toLocaleString()}`);
          
          return true;
        }
      } catch (error) {
        const status = error.response?.status;
        
        if (status === 404) {
          console.log(`   ❌ 端点不存在`);
        } else if (status === 401 || status === 403) {
          console.log(`   ❌ 认证失败: ${error.response?.data?.message || '用户名或密码错误'}`);
        } else if (status === 500) {
          console.log(`   ❌ 服务器错误: 可能JWT密钥未配置`);
          console.log(`      需要在 wp-config.php 中添加:`);
          console.log(`      define('JWT_AUTH_SECRET_KEY', 'your-secret-key');`);
        } else {
          console.log(`   ❌ 错误: ${status || error.message}`);
        }
      }
    }
    
    console.log('\n❌ 无法获取JWT令牌');
    return false;
  }
  
  createJWTAPI() {
    if (!this.jwtToken) {
      throw new Error('需要先获取JWT令牌');
    }
    
    return axios.create({
      baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
      headers: {
        'Authorization': `Bearer ${this.jwtToken}`,
        'Content-Type': 'application/json',
        'User-Agent': 'OpenClaw-JWT-API/1.0'
      },
      timeout: 10000
    });
  }
  
  async testJWTAPI() {
    console.log('\n🌐 测试JWT API访问...');
    
    const api = this.createJWTAPI();
    
    try {
      // 测试用户信息
      console.log('1. 获取当前用户信息...');
      const userResponse = await api.get('/users/me');
      console.log(`   ✅ 用户信息: ${userResponse.data.name}`);
      console.log(`      角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
      console.log(`      ID: ${userResponse.data.id}`);
      
      // 检查权限
      const caps = userResponse.data.capabilities || {};
      const canPublish = caps.publish_posts || caps.edit_posts;
      console.log(`   ${canPublish ? '✅' : '❌'} 发布权限: ${canPublish ? '有' : '无'}`);
      
      if (!canPublish) {
        console.log('   ⚠️  用户可能没有足够的权限发布文章');
      }
      
      return {
        success: true,
        user: userResponse.data,
        canPublish: canPublish
      };
      
    } catch (error) {
      console.log(`❌ JWT API测试失败: ${error.response?.data?.message || error.message}`);
      console.log(`   状态码: ${error.response?.status}`);
      
      if (error.response?.status === 401) {
        console.log('   🔍 JWT令牌可能已过期或无效');
      } else if (error.response?.status === 403) {
        console.log('   🔍 权限不足或令牌无效');
      }
      
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async publishWithJWT() {
    console.log('\n📝 使用JWT发布测试文章...');
    
    const api = this.createJWTAPI();
    
    const postData = {
      title: `JWT令牌发布测试 ${Date.now()}`,
      content: `# JWT令牌认证发布测试
    
这是一个使用JWT令牌认证成功发布的测试文章。

## 测试详情
- **时间**: ${new Date().toISOString()}
- **认证方式**: JWT令牌
- **令牌**: ${this.jwtToken.substring(0, 20)}...
- **用户**: ${this.userInfo?.name || USERNAME}

## 功能验证
✅ JWT令牌获取
✅ 令牌认证  
✅ API访问权限
✅ 文章发布功能

## JWT工作流程
1. 客户端发送用户名密码获取JWT令牌
2. 使用Bearer令牌访问WordPress API
3. 令牌自动处理认证和授权
4. 无需每次请求都发送密码

*JWT自动发布测试成功*`,
      status: 'draft',
      excerpt: 'JWT令牌认证自动发布测试',
      categories: [1] // 未分类
    };
    
    try {
      const response = await api.post('/posts', postData);
      
      console.log(`🎉 JWT发布成功!`);
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   标题: ${response.data.title.rendered}`);
      console.log(`   状态: ${response.data.status}`);
      console.log(`   链接: ${response.data.link}`);
      
      return {
        success: true,
        postId: response.data.id,
        post: response.data
      };
      
    } catch (error) {
      console.log(`❌ JWT发布失败:`);
      console.log(`   错误: ${error.response?.data?.message || error.message}`);
      console.log(`   状态码: ${error.response?.status}`);
      console.log(`   错误代码: ${error.response?.data?.code}`);
      
      if (error.response?.data?.data) {
        console.log(`   错误详情: ${JSON.stringify(error.response.data.data)}`);
      }
      
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async deleteTestPost(postId) {
    if (!postId) return;
    
    console.log(`\n🗑️  清理测试文章 ${postId}...`);
    
    const api = this.createJWTAPI();
    
    try {
      await api.delete(`/posts/${postId}?force=true`);
      console.log('✅ 文章删除成功');
      return true;
    } catch (error) {
      console.log(`❌ 删除失败: ${error.message}`);
      return false;
    }
  }
}

async function runCompleteJWTTest() {
  console.log('🚀 JWT令牌认证完整测试\n');
  console.log(`WordPress站点: ${WORDPRESS_URL}`);
  console.log(`用户名: ${USERNAME}`);
  console.log('='.repeat(60) + '\n');
  
  const tester = new JWTTokenTester();
  
  // 1. 检查JWT插件
  const pluginStatus = await tester.checkJWTPlugin();
  if (!pluginStatus) {
    console.log('\n❌ 需要先安装JWT插件才能继续测试');
    return;
  }
  
  // 2. 获取JWT令牌
  const tokenStatus = await tester.getJWTToken();
  if (!tokenStatus) {
    console.log('\n❌ 无法获取JWT令牌，停止测试');
    return;
  }
  
  // 3. 测试JWT API
  const apiTest = await tester.testJWTAPI();
  if (!apiTest.success || !apiTest.canPublish) {
    console.log('\n⚠️  JWT API测试有问题，继续尝试发布...');
  }
  
  // 4. 使用JWT发布文章
  const publishResult = await tester.publishWithJWT();
  
  // 5. 清理测试文章
  if (publishResult.success) {
    await tester.deleteTestPost(publishResult.postId);
  }
  
  console.log('\n' + '='.repeat(60));
  
  if (publishResult.success) {
    console.log('🎉 JWT令牌认证测试成功!\n');
    
    console.log('📋 JWT工作流程:');
    console.log(`
1. 获取JWT令牌
   POST ${WORDPRESS_URL}/wp-json/jwt-auth/v1/token
   Body: {"username":"${USERNAME}","password":"你的密码"}

2. 使用令牌访问API
   Authorization: Bearer ${tester.jwtToken?.substring(0, 30)}...

3. 发布文章
   POST ${WORDPRESS_URL}/wp-json/wp/v2/posts
   Body: 文章数据
    `);
    
    console.log('🚀 完整代码示例:');
    console.log(`
const axios = require('axios');

async function publishWithJWT() {
  // 1. 获取JWT令牌
  const tokenResponse = await axios.post(
    '${WORDPRESS_URL}/wp-json/jwt-auth/v1/token',
    {
      username: '${USERNAME}',
      password: '你的密码'
    },
    {
      headers: { 'Content-Type': 'application/json' }
    }
  );
  
  const jwtToken = tokenResponse.data.token;
  
  // 2. 创建JWT API客户端
  const api = axios.create({
    baseURL: '${WORDPRESS_URL}/wp-json/wp/v2',
    headers: {
      'Authorization': \`Bearer \${jwtToken}\`,
      'Content-Type': 'application/json'
    }
  });
  
  // 3. 发布文章
  const postData = {
    title: '文章标题',
    content: '文章内容',
    status: 'draft',
    categories: [1]
  };
  
  const response = await api.post('/posts', postData);
  return response.data;
}

// 使用
publishWithJWT().then(result => {
  console.log('文章已发布:', result.id);
});
    `);
    
  } else {
    console.log('❌ JWT令牌认证测试失败\n');
    
    console.log('🔧 可能的问题:');
    console.log('1. JWT插件未正确配置 (需要设置JWT_AUTH_SECRET_KEY)');
    console.log('2. 用户名或密码错误');
    console.log('3. 用户权限不足');
    console.log('4. 服务器配置问题');
    
    console.log('\n📋 检查清单:');
    console.log('✅ 1. JWT插件已安装并激活');
    console.log('✅ 2. wp-config.php 配置了JWT密钥');
    console.log('✅ 3. 用户名和密码正确');
    console.log('✅ 4. 用户有发布文章的权限');
    console.log('✅ 5. 服务器支持JWT认证');
  }
  
  console.log('\n🎯 测试完成');
}

// 运行测试
runCompleteJWTTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});