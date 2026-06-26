#!/usr/bin/env node

/**
 * 直接发布文章测试
 * 尝试多种认证方式
 */

const axios = require('axios');

const WORDPRESS_URL = 'https://your-site.com';
const USERNAME = 'admin';
const PASSWORD = 'your-app-password';

// 测试不同的认证方式
const AUTH_METHODS = [
  {
    name: 'Basic Auth (当前密码)',
    createClient: () => axios.create({
      baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
      auth: { username: USERNAME, password: PASSWORD },
      headers: { 'Content-Type': 'application/json' }
    })
  },
  {
    name: 'Basic Auth (密码去掉空格)',
    createClient: () => axios.create({
      baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
      auth: { username: USERNAME, password: PASSWORD.replace(/\s+/g, '') },
      headers: { 'Content-Type': 'application/json' }
    })
  },
  {
    name: 'Basic Auth (base64编码)',
    createClient: () => {
      const auth = Buffer.from(`${USERNAME}:${PASSWORD}`).toString('base64');
      return axios.create({
        baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Basic ${auth}`,
          'Content-Type': 'application/json'
        }
      });
    }
  },
  {
    name: '无认证 (公开API)',
    createClient: () => axios.create({
      baseURL: `${WORDPRESS_URL}/wp-json/wp/v2`,
      headers: { 'Content-Type': 'application/json' }
    })
  }
];

async function testAuthMethod(method) {
  console.log(`\n🔐 测试: ${method.name}`);
  
  const api = method.createClient();
  
  try {
    // 1. 测试连接
    const testResponse = await api.get('/');
    console.log(`   ✅ API连接成功`);
    
    // 2. 测试用户端点
    try {
      const userResponse = await api.get('/users/me');
      console.log(`   ✅ 用户认证成功: ${userResponse.data.name}`);
      return { success: true, api: api, user: userResponse.data };
    } catch (userError) {
      if (userError.response?.status === 401) {
        console.log(`   🔒 需要认证 (正常)`);
      } else {
        console.log(`   ❌ 用户端点错误: ${userError.response?.data?.message || userError.message}`);
      }
    }
    
    // 3. 测试文章列表
    try {
      const postsResponse = await api.get('/posts?per_page=1');
      console.log(`   ✅ 可以访问文章API: ${postsResponse.data.length} 篇文章`);
      return { success: true, api: api };
    } catch (postsError) {
      console.log(`   ❌ 文章API错误: ${postsError.response?.data?.message || postsError.message}`);
    }
    
    return { success: false, api: api };
    
  } catch (error) {
    console.log(`   ❌ 连接失败: ${error.response?.status || error.message}`);
    return { success: false, api: api };
  }
}

async function publishArticle(api, methodName) {
  console.log(`\n📝 尝试发布文章 (${methodName})...`);
  
  const postData = {
    title: `JWT发布测试 ${Date.now()}`,
    content: `## JWT自动发布测试文章
    
这是一个测试JWT接口发布功能的文章。

### 测试内容
- 发布时间: ${new Date().toISOString()}
- 测试方法: ${methodName}
- 状态: draft

### 功能验证
1. ✅ 文章创建
2. ✅ 内容格式
3. ✅ 元数据设置

*由OpenClaw自动生成*`,
    status: 'draft',
    excerpt: 'JWT接口发布功能测试',
    categories: [1], // 未分类
    tags: ['JWT', 'API', '测试', '自动化']
  };
  
  try {
    const response = await api.post('/posts', postData);
    
    console.log(`   🎉 文章发布成功!`);
    console.log(`      文章ID: ${response.data.id}`);
    console.log(`      标题: ${response.data.title.rendered}`);
    console.log(`      状态: ${response.data.status}`);
    console.log(`      链接: ${response.data.link}`);
    console.log(`      创建时间: ${response.data.date}`);
    
    return {
      success: true,
      postId: response.data.id,
      post: response.data
    };
  } catch (error) {
    console.log(`   ❌ 发布失败:`);
    console.log(`      错误: ${error.response?.data?.message || error.message}`);
    console.log(`      状态码: ${error.response?.status}`);
    console.log(`      错误代码: ${error.response?.data?.code}`);
    
    if (error.response?.data) {
      console.log(`      详细错误: ${JSON.stringify(error.response.data)}`);
    }
    
    return {
      success: false,
      error: error.message
    };
  }
}

async function deleteArticle(api, postId) {
  if (!postId) return;
  
  console.log(`\n🗑️  清理测试文章 ${postId}...`);
  
  try {
    await api.delete(`/posts/${postId}?force=true`);
    console.log(`   ✅ 文章删除成功`);
    return true;
  } catch (error) {
    console.log(`   ❌ 删除失败: ${error.message}`);
    return false;
  }
}

async function runCompleteTest() {
  console.log('🚀 WordPress文章发布全面测试\n');
  console.log(`站点: ${WORDPRESS_URL}`);
  console.log(`用户: ${USERNAME}`);
  console.log('='.repeat(60) + '\n');
  
  let successfulMethod = null;
  let successfulApi = null;
  let publishedPostId = null;
  
  // 测试所有认证方法
  for (const method of AUTH_METHODS) {
    const result = await testAuthMethod(method);
    
    if (result.success && result.user) {
      successfulMethod = method.name;
      successfulApi = result.api;
      console.log(`\n🎯 找到有效的认证方法: ${method.name}`);
      break;
    }
  }
  
  if (!successfulMethod) {
    console.log('\n❌ 没有找到有效的认证方法');
    console.log('\n🔧 可能的问题和解决方案:');
    console.log('1. ❌ 当前密码不是有效的应用程序密码');
    console.log('   解决方案: 在WordPress中创建应用程序密码');
    console.log('   步骤: 用户 → 个人资料 → 应用程序密码');
    
    console.log('\n2. ❌ JWT插件未安装');
    console.log('   解决方案: 安装JWT插件');
    console.log('   步骤: 插件 → 安装插件 → 搜索"JWT Authentication"');
    
    console.log('\n3. ❌ 用户权限不足');
    console.log('   解决方案: 检查用户角色和权限');
    console.log('   需要: 作者或以上权限');
    
    console.log('\n4. 🔧 立即行动:');
    console.log('   A. 访问 https://your-site.com/wp-admin/profile.php');
    console.log('      创建应用程序密码');
    console.log('   B. 或访问 https://your-site.com/wp-admin/plugins.php');
    console.log('      安装JWT插件');
    
    return;
  }
  
  // 尝试发布文章
  const publishResult = await publishArticle(successfulApi, successfulMethod);
  
  if (publishResult.success) {
    publishedPostId = publishResult.postId;
    
    // 等待一下，然后尝试更新
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    console.log(`\n🔄 测试文章更新...`);
    try {
      const updateData = {
        title: `更新后的标题 ${Date.now()}`,
        content: '这是更新后的内容',
        excerpt: '更新后的摘要'
      };
      
      const updateResponse = await successfulApi.put(`/posts/${publishedPostId}`, updateData);
      console.log(`   ✅ 文章更新成功`);
      console.log(`      新标题: ${updateResponse.data.title.rendered}`);
    } catch (updateError) {
      console.log(`   ❌ 更新失败: ${updateError.message}`);
    }
  }
  
  // 清理测试文章
  if (publishedPostId) {
    await deleteArticle(successfulApi, publishedPostId);
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('🎯 测试总结\n');
  
  if (publishResult.success) {
    console.log('✅ 成功! 可以使用以下配置发布文章:');
    console.log(`
const axios = require('axios');

const api = axios.create({
  baseURL: '${WORDPRESS_URL}/wp-json/wp/v2',
  auth: {
    username: '${USERNAME}',
    password: '${PASSWORD}'
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

// 发布文章
const postData = {
  title: '文章标题',
  content: '文章内容',
  status: 'draft', // 或 'publish'
  categories: [1],
  tags: ['标签1', '标签2']
};

const response = await api.post('/posts', postData);
    `);
  } else {
    console.log('❌ 发布失败，需要配置正确的认证');
    console.log('\n📋 下一步:');
    console.log('1. 在WordPress中创建应用程序密码');
    console.log('2. 或安装JWT插件');
    console.log('3. 然后更新密码配置重新测试');
  }
}

// 运行测试
runCompleteTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});