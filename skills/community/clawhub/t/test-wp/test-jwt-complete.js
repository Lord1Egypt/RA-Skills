#!/usr/bin/env node

/**
 * 完整的JWT工作流程测试
 * 现在DNS问题已修复
 */

const axios = require('axios');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

async function testCompleteJWT() {
  console.log('🚀 完整的JWT工作流程测试\n');
  console.log(`站点: ${config.wordpressUrl}`);
  console.log(`用户: ${config.username}`);
  console.log('='.repeat(60) + '\n');
  
  // 1. 获取JWT令牌
  console.log('1. 🔐 获取JWT令牌...');
  
  let jwtToken = null;
  let userInfo = null;
  
  try {
    const tokenResponse = await axios.post(
      `${config.wordpressUrl}/wp-json/jwt-auth/v1/token`,
      {
        username: config.username,
        password: config.password
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (tokenResponse.data.token) {
      jwtToken = tokenResponse.data.token;
      userInfo = {
        email: tokenResponse.data.user_email,
        name: tokenResponse.data.user_display_name,
        nicename: tokenResponse.data.user_nicename
      };
      
      console.log(`✅ JWT令牌获取成功!`);
      console.log(`   令牌: ${jwtToken.substring(0, 30)}...`);
      console.log(`   用户: ${userInfo.name} (${userInfo.email})`);
      console.log(`   有效期: ${tokenResponse.data.expires_in || '未知'}秒`);
    } else {
      console.log(`❌ 响应中没有token字段`);
      return;
    }
    
  } catch (error) {
    console.log(`❌ 获取JWT令牌失败: ${error.response?.data?.message || error.message}`);
    return;
  }
  
  // 2. 创建JWT API客户端
  const api = axios.create({
    baseURL: `${config.wordpressUrl}/wp-json/wp/v2`,
    headers: {
      'Authorization': `Bearer ${jwtToken}`,
      'Content-Type': 'application/json'
    }
  });
  
  // 3. 测试用户信息
  console.log('\n2. 👤 测试用户信息访问...');
  
  try {
    const userResponse = await api.get('/users/me');
    console.log(`✅ 用户信息获取成功!`);
    console.log(`   姓名: ${userResponse.data.name}`);
    console.log(`   角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
    console.log(`   ID: ${userResponse.data.id}`);
    
    // 检查权限
    const caps = userResponse.data.capabilities || {};
    const canPublish = caps.publish_posts || caps.edit_posts;
    console.log(`   ${canPublish ? '✅' : '❌'} 发布权限: ${canPublish ? '有' : '无'}`);
    
    if (!canPublish) {
      console.log(`   ⚠️  用户可能没有足够的权限发布文章`);
    }
    
  } catch (error) {
    console.log(`❌ 用户信息获取失败: ${error.response?.data?.message || error.message}`);
    return;
  }
  
  // 4. 测试文章发布
  console.log('\n3. 📝 测试文章发布...');
  
  const postData = {
    title: `JWT自动发布测试 ${Date.now()}`,
    content: `# JWT自动发布测试成功！
    
这是一个使用JWT令牌认证成功发布的测试文章。

## 测试详情
- **时间**: ${new Date().toISOString()}
- **认证方式**: JWT令牌
- **令牌**: ${jwtToken.substring(0, 20)}...
- **用户**: ${userInfo.name}

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
    const publishResponse = await api.post('/posts', postData);
    console.log(`🎉 文章发布成功!`);
    console.log(`   文章ID: ${publishResponse.data.id}`);
    console.log(`   标题: ${publishResponse.data.title.rendered}`);
    console.log(`   状态: ${publishResponse.data.status}`);
    console.log(`   链接: ${publishResponse.data.link}`);
    
    const postId = publishResponse.data.id;
    
    // 5. 测试文章更新
    console.log('\n4. 🔄 测试文章更新...');
    
    try {
      const updateResponse = await api.put(`/posts/${postId}`, {
        title: `更新后的标题 ${Date.now()}`,
        excerpt: '更新后的摘要 - JWT测试'
      });
      console.log(`✅ 文章更新成功`);
    } catch (updateError) {
      console.log(`❌ 更新失败: ${updateError.message}`);
    }
    
    // 6. 测试文章删除
    console.log('\n5. 🗑️  测试文章删除...');
    
    try {
      await api.delete(`/posts/${postId}?force=true`);
      console.log(`✅ 文章删除成功`);
    } catch (deleteError) {
      console.log(`❌ 删除失败: ${deleteError.message}`);
    }
    
  } catch (error) {
    console.log(`❌ 文章发布失败:`);
    console.log(`   错误: ${error.response?.data?.message || error.message}`);
    console.log(`   状态码: ${error.response?.status}`);
    console.log(`   错误代码: ${error.response?.data?.code}`);
    
    if (error.response?.data?.data) {
      console.log(`   错误详情: ${JSON.stringify(error.response.data.data)}`);
    }
    return;
  }
  
  // 7. 显示成功信息和使用示例
  console.log('\n' + '='.repeat(60));
  console.log('✅ JWT自动发布测试完全成功!\n');
  
  console.log('📋 JWT工作流程总结:');
  console.log(`
1. 获取JWT令牌
   POST ${config.wordpressUrl}/wp-json/jwt-auth/v1/token
   Body: {"username":"${config.username}","password":"你的密码"}

2. 使用令牌访问API
   Authorization: Bearer ${jwtToken.substring(0, 30)}...

3. 发布文章
   POST ${config.wordpressUrl}/wp-json/wp/v2/posts
   Body: 文章数据
  `);
  
  console.log('🚀 完整代码示例:');
  console.log(`
const axios = require('axios');

class WordPressJWTClient {
  constructor(url, username, password) {
    this.url = url;
    this.username = username;
    this.password = password;
    this.token = null;
  }
  
  async getToken() {
    const response = await axios.post(
      \`\${this.url}/wp-json/jwt-auth/v1/token\`,
      {
        username: this.username,
        password: this.password
      },
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );
    
    this.token = response.data.token;
    return this.token;
  }
  
  createAPI() {
    return axios.create({
      baseURL: \`\${this.url}/wp-json/wp/v2\`,
      headers: {
        'Authorization': \`Bearer \${this.token}\`,
        'Content-Type': 'application/json'
      }
    });
  }
  
  async publishPost(title, content, options = {}) {
    const api = this.createAPI();
    
    const postData = {
      title: title,
      content: content,
      status: options.status || 'draft',
      excerpt: options.excerpt || '',
      categories: options.categories || [1],
      tags: options.tags || []
    };
    
    const response = await api.post('/posts', postData);
    return response.data;
  }
}

// 使用
const client = new WordPressJWTClient(
  '${config.wordpressUrl}',
  '${config.username}',
  '你的密码'
);

await client.getToken();
const result = await client.publishPost('文章标题', '文章内容');
console.log('文章已发布，ID:', result.id);
  `);
  
  console.log('🎯 现在可以开始自动发布文章了!');
}

// 运行测试
testCompleteJWT().catch(error => {
  console.error('测试过程中发生错误:', error);
});