#!/usr/bin/env node

/**
 * JWT插件安装后的完整测试脚本
 * 需要先安装 "JWT Authentication for WP REST API" 插件
 * 并配置 wp-config.php
 */

const axios = require('axios');

// 配置 - 修改这些值
const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password', // 你的WordPress密码
  
  // JWT端点
  jwtTokenEndpoint: '/wp-json/jwt-auth/v1/token',
  jwtValidateEndpoint: '/wp-json/jwt-auth/v1/token/validate',
  
  // 重试设置
  maxRetries: 3,
  retryDelay: 1000
};

class WordPressJWTClient {
  constructor(config) {
    this.config = config;
    this.jwtToken = null;
    this.tokenExpiry = null;
  }
  
  async getJWTToken() {
    console.log('🔐 获取JWT令牌...');
    
    try {
      const response = await axios.post(
        `${this.config.wordpressUrl}${this.config.jwtTokenEndpoint}`,
        {
          username: this.config.username,
          password: this.config.password
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
        
        console.log('✅ JWT令牌获取成功！');
        console.log(`   令牌: ${this.jwtToken.substring(0, 30)}...`);
        console.log(`   用户: ${response.data.user_email}`);
        console.log(`   显示名: ${response.data.user_display_name}`);
        console.log(`   过期时间: ${new Date(this.tokenExpiry).toLocaleString()}`);
        
        return this.jwtToken;
      } else {
        throw new Error('响应中没有找到JWT令牌');
      }
    } catch (error) {
      console.error('❌ 获取JWT令牌失败:');
      
      if (error.response) {
        console.log(`   状态码: ${error.response.status}`);
        console.log(`   错误: ${error.response.data?.message || JSON.stringify(error.response.data)}`);
        
        // 提供具体诊断
        if (error.response.status === 404) {
          console.log('\n🔧 可能的问题:');
          console.log('1. JWT插件未安装或未激活');
          console.log('2. WordPress URL不正确');
          console.log('3. JWT端点路径错误');
        } else if (error.response.status === 403) {
          console.log('\n🔧 可能的问题:');
          console.log('1. 用户名或密码错误');
          console.log('2. 用户被锁定或禁用');
        } else if (error.response.status === 500) {
          console.log('\n🔧 可能的问题:');
          console.log('1. JWT密钥未配置或配置错误');
          console.log('2. 检查wp-config.php中的JWT_AUTH_SECRET_KEY');
        }
      } else {
        console.log(`   错误: ${error.message}`);
      }
      
      throw error;
    }
  }
  
  async validateToken() {
    if (!this.jwtToken) {
      throw new Error('没有可用的JWT令牌');
    }
    
    console.log('\n🔍 验证JWT令牌...');
    
    try {
      const response = await axios.post(
        `${this.config.wordpressUrl}${this.config.jwtValidateEndpoint}`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${this.jwtToken}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      console.log('✅ JWT令牌验证成功！');
      console.log(`   状态码: ${response.status}`);
      console.log(`   数据: ${JSON.stringify(response.data)}`);
      
      return true;
    } catch (error) {
      console.error('❌ JWT令牌验证失败:', error.response?.data?.message || error.message);
      return false;
    }
  }
  
  createAPI() {
    if (!this.jwtToken) {
      throw new Error('需要先获取JWT令牌');
    }
    
    return axios.create({
      baseURL: `${this.config.wordpressUrl}/wp-json/wp/v2`,
      headers: {
        'Authorization': `Bearer ${this.jwtToken}`,
        'Content-Type': 'application/json',
        'User-Agent': 'OpenClaw-JWT-Client/1.0'
      },
      timeout: 10000
    });
  }
  
  async testAPIConnection() {
    console.log('\n🌐 测试WordPress API连接...');
    
    const api = this.createAPI();
    
    try {
      // 测试1: 获取当前用户
      console.log('1. 获取当前用户信息...');
      const userResponse = await api.get('/users/me');
      console.log(`   ✅ 成功: ${userResponse.data.name} (${userResponse.data.roles?.join(', ')})`);
      
      // 测试2: 检查权限
      console.log('2. 检查用户权限...');
      const caps = userResponse.data.capabilities || {};
      const hasPublish = caps.publish_posts || caps.edit_posts;
      console.log(`   ${hasPublish ? '✅' : '❌'} 发布权限: ${hasPublish ? '有' : '无'}`);
      
      return {
        success: true,
        user: userResponse.data,
        hasPublishPermission: hasPublish
      };
    } catch (error) {
      console.error('❌ API连接测试失败:', error.response?.data?.message || error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async createTestPost() {
    console.log('\n📝 创建测试文章...');
    
    const api = this.createAPI();
    
    try {
      const postData = {
        title: `JWT自动发布测试 ${Date.now()}`,
        content: '这是通过JWT认证自动发布的测试文章。\n\n## 功能测试\n- JWT认证\n- 自动发布\n- Markdown支持\n- 分类和标签',
        status: 'draft',
        excerpt: 'JWT自动发布功能测试',
        categories: [1], // 未分类
        tags: ['JWT', 'API', '自动化', 'WordPress']
      };
      
      const response = await api.post('/posts', postData);
      
      console.log('✅ 文章创建成功！');
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   标题: ${response.data.title.rendered}`);
      console.log(`   状态: ${response.data.status}`);
      console.log(`   链接: ${response.data.link}`);
      console.log(`   创建时间: ${response.data.date}`);
      
      return {
        success: true,
        postId: response.data.id,
        post: response.data
      };
    } catch (error) {
      console.error('❌ 文章创建失败:');
      console.log(`   错误: ${error.response?.data?.message || error.message}`);
      console.log(`   状态码: ${error.response?.status}`);
      console.log(`   错误代码: ${error.response?.data?.code}`);
      
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async deletePost(postId) {
    console.log(`\n🗑️  删除文章 ${postId}...`);
    
    const api = this.createAPI();
    
    try {
      await api.delete(`/posts/${postId}?force=true`);
      console.log('✅ 文章删除成功');
      return true;
    } catch (error) {
      console.error('❌ 文章删除失败:', error.message);
      return false;
    }
  }
}

async function runFullTest() {
  console.log('🚀 JWT插件完整测试\n');
  console.log(`WordPress站点: ${config.wordpressUrl}`);
  console.log(`用户名: ${config.username}`);
  console.log('='.repeat(50));
  
  const client = new WordPressJWTClient(config);
  
  try {
    // 1. 获取JWT令牌
    await client.getJWTToken();
    
    // 2. 验证令牌
    const isValid = await client.validateToken();
    if (!isValid) {
      console.log('❌ 令牌验证失败，停止测试');
      return;
    }
    
    // 3. 测试API连接
    const connectionTest = await client.testAPIConnection();
    if (!connectionTest.success || !connectionTest.hasPublishPermission) {
      console.log('❌ API连接测试失败或没有发布权限');
      return;
    }
    
    // 4. 创建测试文章
    const postResult = await client.createTestPost();
    
    // 5. 清理测试文章
    if (postResult.success) {
      await client.deletePost(postResult.postId);
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 JWT测试完成！');
    
    if (postResult.success) {
      console.log('\n📋 使用示例:');
      console.log(`
const axios = require('axios');

// 1. 获取JWT令牌
const tokenResponse = await axios.post('${config.wordpressUrl}/wp-json/jwt-auth/v1/token', {
  username: '${config.username}',
  password: '你的密码'
});

const jwtToken = tokenResponse.data.token;

// 2. 创建API客户端
const api = axios.create({
  baseURL: '${config.wordpressUrl}/wp-json/wp/v2',
  headers: {
    'Authorization': \`Bearer \${jwtToken}\`,
    'Content-Type': 'application/json'
  }
});

// 3. 发布文章
const postData = {
  title: '文章标题',
  content: '文章内容',
  status: 'draft' // 或 'publish'
};

const response = await api.post('/posts', postData);
      `);
    }
    
  } catch (error) {
    console.error('\n❌ 测试过程中发生致命错误:', error.message);
  }
}

// 运行测试
runFullTest();