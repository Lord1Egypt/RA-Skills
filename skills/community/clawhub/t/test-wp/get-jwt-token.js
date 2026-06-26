#!/usr/bin/env node

/**
 * JWT获取Token脚本
 * 从WordPress获取JWT令牌
 */

const axios = require('axios');

// 配置
const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password',
  
  // JWT端点
  jwtEndpoint: '/wp-json/jwt-auth/v1/token',
  
  // 备用端点（如果标准端点不行）
  altEndpoints: [
    '/?rest_route=/jwt-auth/v1/token',
    '/index.php?rest_route=/jwt-auth/v1/token'
  ]
};

class JWTTokenGetter {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.tokenData = null;
  }
  
  async getToken() {
    console.log('🔐 获取JWT Token\n');
    console.log(`WordPress站点: ${this.config.wordpressUrl}`);
    console.log(`用户名: ${this.config.username}`);
    console.log('='.repeat(50) + '\n');
    
    // 首先尝试标准端点
    const endpoints = [this.config.jwtEndpoint, ...this.config.altEndpoints];
    
    for (const endpoint of endpoints) {
      console.log(`尝试端点: ${endpoint}`);
      
      try {
        const response = await axios.post(
          `${this.config.wordpressUrl}${endpoint}`,
          {
            username: this.config.username,
            password: this.config.password
          },
          {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            timeout: 10000
          }
        );
        
        if (response.data && response.data.token) {
          this.token = response.data.token;
          this.tokenData = response.data;
          
          console.log(`✅ Token获取成功!`);
          console.log(`   使用的端点: ${endpoint}`);
          console.log(`   Token: ${this.token.substring(0, 30)}...`);
          console.log(`   用户: ${this.tokenData.user_display_name || this.tokenData.user_email}`);
          console.log(`   有效期: ${this.tokenData.expires_in || '未知'} 秒`);
          
          if (this.tokenData.expires_in) {
            const expiryTime = new Date(Date.now() + this.tokenData.expires_in * 1000);
            console.log(`   过期时间: ${expiryTime.toLocaleString()}`);
          }
          
          return {
            success: true,
            token: this.token,
            data: this.tokenData,
            endpoint: endpoint
          };
        } else {
          console.log(`❌ 响应中没有token字段`);
          console.log(`   响应: ${JSON.stringify(response.data).substring(0, 100)}`);
        }
        
      } catch (error) {
        await this.handleError(error, endpoint);
      }
    }
    
    console.log('\n❌ 所有端点都失败了，无法获取JWT Token');
    return {
      success: false,
      error: '无法从任何端点获取JWT Token'
    };
  }
  
  async handleError(error, endpoint) {
    console.log(`   ❌ 请求失败`);
    
    if (error.response) {
      // 服务器响应了错误状态码
      const status = error.response.status;
      const data = error.response.data;
      
      console.log(`   状态码: ${status}`);
      
      switch(status) {
        case 404:
          console.log(`   错误: 端点不存在 (404)`);
          console.log(`   可能: JWT插件未安装或未激活`);
          break;
          
        case 405:
          console.log(`   错误: 方法不允许 (405)`);
          console.log(`   可能: 应该使用GET请求？`);
          break;
          
        case 401:
        case 403:
          console.log(`   错误: 认证失败 (${status})`);
          if (data && data.message) {
            console.log(`   消息: ${data.message}`);
          }
          console.log(`   可能: 用户名或密码错误`);
          break;
          
        case 500:
          console.log(`   错误: 服务器错误 (500)`);
          if (data) {
            console.log(`   消息: ${data.message || '未知错误'}`);
            console.log(`   代码: ${data.code || '未知'}`);
            
            // 分析JWT特定错误
            this.analyzeJWTError(data.code, data.message);
          }
          break;
          
        default:
          console.log(`   错误: ${status}`);
          if (data && data.message) {
            console.log(`   消息: ${data.message}`);
          }
      }
      
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.log(`   错误: 没有收到响应`);
      console.log(`   可能: 网络问题或服务器宕机`);
    } else {
      // 请求设置时发生错误
      console.log(`   错误: ${error.message}`);
    }
  }
  
  analyzeJWTError(code, message) {
    console.log(`\n🔍 JWT错误分析:`);
    
    switch(code) {
      case 'jwt_auth_bad_config':
        console.log(`   ❌ JWT配置错误`);
        console.log(`      需要在 wp-config.php 中添加:`);
        console.log(`      define('JWT_AUTH_SECRET_KEY', 'your-secret-key');`);
        console.log(`      define('JWT_AUTH_CORS_ENABLE', true);`);
        break;
        
      case 'jwt_auth_no_secret_key':
        console.log(`   ❌ JWT密钥未设置`);
        console.log(`      必须配置 JWT_AUTH_SECRET_KEY`);
        break;
        
      case 'jwt_auth_no_auth_header':
        console.log(`   ❌ 缺少认证头`);
        console.log(`      请求需要正确的认证头`);
        break;
        
      default:
        if (message) {
          console.log(`   ⚠️  ${message}`);
        }
    }
  }
  
  async validateToken() {
    if (!this.token) {
      console.log('❌ 没有可用的Token进行验证');
      return false;
    }
    
    console.log('\n🔍 验证JWT Token...');
    
    try {
      const response = await axios.post(
        `${this.config.wordpressUrl}/wp-json/jwt-auth/v1/token/validate`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      console.log(`✅ Token验证成功`);
      console.log(`   状态码: ${response.status}`);
      
      if (response.data && response.data.data) {
        console.log(`   验证数据: ${JSON.stringify(response.data.data)}`);
      }
      
      return true;
      
    } catch (error) {
      console.log(`❌ Token验证失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  async testWithToken() {
    if (!this.token) {
      console.log('❌ 没有Token可用于测试');
      return;
    }
    
    console.log('\n🚀 使用JWT Token测试API访问...');
    
    const api = axios.create({
      baseURL: `${this.config.wordpressUrl}/wp-json/wp/v2`,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    try {
      // 测试用户信息
      console.log('1. 获取当前用户信息...');
      const userResponse = await api.get('/users/me');
      console.log(`   ✅ 成功: ${userResponse.data.name}`);
      console.log(`      角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
      console.log(`      ID: ${userResponse.data.id}`);
      
      // 测试权限
      const caps = userResponse.data.capabilities || {};
      const canPublish = caps.publish_posts || caps.edit_posts;
      console.log(`   ${canPublish ? '✅' : '❌'} 发布权限: ${canPublish ? '有' : '无'}`);
      
      return {
        success: true,
        user: userResponse.data,
        canPublish: canPublish
      };
      
    } catch (error) {
      console.log(`❌ API测试失败: ${error.response?.data?.message || error.message}`);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  saveTokenToFile(filename = 'jwt-token.json') {
    if (!this.token) return;
    
    const tokenData = {
      token: this.token,
      user: this.tokenData.user_email,
      display_name: this.tokenData.user_display_name,
      expires_in: this.tokenData.expires_in,
      obtained_at: new Date().toISOString(),
      wordpress_url: this.config.wordpressUrl,
      username: this.config.username
    };
    
    const fs = require('fs');
    const path = require('path');
    
    const filePath = path.join(__dirname, filename);
    fs.writeFileSync(filePath, JSON.stringify(tokenData, null, 2));
    
    console.log(`\n💾 Token已保存到: ${filePath}`);
    console.log(`   使用命令查看: cat ${filePath}`);
    
    return filePath;
  }
  
  printUsageExample() {
    console.log('\n' + '='.repeat(50));
    console.log('📋 JWT Token使用示例\n');
    
    console.log('1. 获取Token的代码:');
    console.log(`
const axios = require('axios');

async function getJWToken() {
  const response = await axios.post(
    '${this.config.wordpressUrl}/wp-json/jwt-auth/v1/token',
    {
      username: '${this.config.username}',
      password: '你的密码'
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data.token;
}

// 使用
const token = await getJWToken();
console.log('JWT Token:', token);
    `);
    
    console.log('\n2. 使用Token访问API:');
    console.log(`
const api = axios.create({
  baseURL: '${this.config.wordpressUrl}/wp-json/wp/v2',
  headers: {
    'Authorization': \`Bearer \${token}\`,
    'Content-Type': 'application/json'
  }
});

// 获取用户信息
const user = await api.get('/users/me');
console.log('用户:', user.data.name);

// 发布文章
const postData = {
  title: '测试文章',
  content: '内容',
  status: 'draft'
};

const post = await api.post('/posts', postData);
console.log('文章ID:', post.data.id);
    `);
  }
}

async function main() {
  const tokenGetter = new JWTTokenGetter(config);
  
  // 1. 获取Token
  const result = await tokenGetter.getToken();
  
  if (result.success) {
    // 2. 验证Token
    await tokenGetter.validateToken();
    
    // 3. 测试API访问
    const apiTest = await tokenGetter.testWithToken();
    
    // 4. 保存Token到文件
    tokenGetter.saveTokenToFile();
    
    // 5. 显示使用示例
    tokenGetter.printUsageExample();
    
    console.log('\n🎉 JWT Token获取和使用流程完成!');
    
  } else {
    console.log('\n❌ 无法获取JWT Token');
    console.log('\n🔧 需要检查:');
    console.log('   1. JWT插件是否已安装并激活');
    console.log('   2. wp-config.php 是否配置了JWT密钥');
    console.log('   3. 固定链接设置是否正确');
    console.log('   4. 用户名和密码是否正确');
    
    console.log('\n🚀 备选方案:');
    console.log('   使用WordPress应用程序密码:');
    console.log('   node app-password-test.js');
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('🎯 脚本执行完成');
}

// 运行主函数
main().catch(error => {
  console.error('脚本执行过程中发生错误:', error);
});