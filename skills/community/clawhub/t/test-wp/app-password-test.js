#!/usr/bin/env node

/**
 * WordPress应用程序密码测试
 * 无需安装JWT插件
 * 使用WordPress内置的应用程序密码功能
 */

const axios = require('axios');

// 配置 - 需要设置应用程序密码
const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  appPassword: 'your-app-password', // 这应该是应用程序密码，不是登录密码
  
  // 如果当前密码不是应用程序密码，需要先创建
  needAppPassword: true
};

async function testWithAppPassword() {
  console.log('🔐 WordPress应用程序密码测试\n');
  console.log(`站点: ${config.wordpressUrl}`);
  console.log(`用户: ${config.username}`);
  console.log('='.repeat(50) + '\n');
  
  if (config.needAppPassword) {
    console.log('⚠️  注意: 当前使用的可能不是应用程序密码');
    console.log('   应用程序密码格式: xxxx xxxx xxxx xxxx xxxx xxxx (24字符，有空格)');
    console.log('\n📋 如何创建应用程序密码:');
    console.log('   1. 登录WordPress后台: https://your-site.com/wp-admin');
    console.log('   2. 进入 用户 → 个人资料');
    console.log('   3. 找到"应用程序密码"部分');
    console.log('   4. 输入名称: "OpenClaw Auto-Publish"');
    console.log('   5. 点击"添加新应用程序密码"');
    console.log('   6. 立即复制生成的密码');
    console.log('\n   然后更新配置中的 appPassword');
    console.log('='.repeat(50) + '\n');
  }
  
  // 创建Basic Auth API客户端
  const api = axios.create({
    baseURL: `${config.wordpressUrl}/wp-json/wp/v2`,
    auth: {
      username: config.username,
      password: config.appPassword
    },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'OpenClaw-App-Password-Test/1.0'
    },
    timeout: 10000
  });
  
  try {
    // 测试1: 获取当前用户
    console.log('1. 🔍 测试应用程序密码认证...');
    try {
      const userResponse = await api.get('/users/me');
      console.log(`   ✅ 认证成功!`);
      console.log(`      用户: ${userResponse.data.name}`);
      console.log(`      角色: ${userResponse.data.roles?.join(', ') || '未知'}`);
      console.log(`      邮箱: ${userResponse.data.email || '未知'}`);
    } catch (error) {
      console.log(`   ❌ 认证失败: ${error.response?.data?.message || error.message}`);
      console.log(`      状态码: ${error.response?.status}`);
      console.log(`      错误代码: ${error.response?.data?.code}`);
      
      if (error.response?.status === 401) {
        console.log('\n🔧 建议:');
        console.log('   1. 确认使用的是应用程序密码，不是登录密码');
        console.log('   2. 在WordPress中创建应用程序密码');
        console.log('   3. 检查用户权限');
      }
      return;
    }
    
    // 测试2: 创建测试文章
    console.log('\n2. 📝 创建测试文章...');
    try {
      const postData = {
        title: `应用程序密码测试 ${Date.now()}`,
        content: '这是通过应用程序密码创建的测试文章。\n\n## 功能测试\n- 应用程序密码认证\n- 自动发布功能\n- Basic Auth集成',
        status: 'draft',
        excerpt: '应用程序密码功能测试',
        categories: [1], // 未分类
        tags: ['API', '自动化', 'WordPress', '应用程序密码']
      };
      
      const response = await api.post('/posts', postData);
      console.log('   ✅ 文章创建成功!');
      console.log(`      文章ID: ${response.data.id}`);
      console.log(`      标题: ${response.data.title.rendered}`);
      console.log(`      状态: ${response.data.status}`);
      console.log(`      链接: ${response.data.link}`);
      
      const postId = response.data.id;
      
      // 测试3: 更新文章
      console.log('\n3. 🔄 更新测试文章...');
      try {
        const updateData = {
          title: `更新后的标题 ${Date.now()}`,
          content: '更新后的文章内容',
          excerpt: '更新后的摘要'
        };
        
        const updateResponse = await api.put(`/posts/${postId}`, updateData);
        console.log(`   ✅ 文章更新成功`);
        console.log(`      新标题: ${updateResponse.data.title.rendered}`);
      } catch (updateError) {
        console.log(`   ❌ 文章更新失败: ${updateError.message}`);
      }
      
      // 测试4: 删除文章
      console.log('\n4. 🗑️  删除测试文章...');
      try {
        await api.delete(`/posts/${postId}?force=true`);
        console.log('   ✅ 文章删除成功');
      } catch (deleteError) {
        console.log(`   ❌ 文章删除失败: ${deleteError.message}`);
      }
      
    } catch (error) {
      console.log(`   ❌ 文章操作失败: ${error.response?.data?.message || error.message}`);
      console.log(`      状态码: ${error.response?.status}`);
      console.log(`      错误代码: ${error.response?.data?.code}`);
    }
    
    // 测试5: 列出文章
    console.log('\n5. 📋 列出文章...');
    try {
      const postsResponse = await api.get('/posts?per_page=3&status=draft,publish');
      console.log(`   ✅ 成功获取 ${postsResponse.data.length} 篇文章`);
      postsResponse.data.forEach(post => {
        console.log(`      - "${post.title.rendered}" (ID: ${post.id}, 状态: ${post.status})`);
      });
    } catch (error) {
      console.log(`   ❌ 获取文章列表失败: ${error.message}`);
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 应用程序密码测试完成!\n');
    
    console.log('📋 成功配置示例:');
    console.log(`
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://your-site.com/wp-json/wp/v2',
  auth: {
    username: 'admin',
    password: 'xxxx xxxx xxxx xxxx xxxx xxxx' // 应用程序密码
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

// 发布文章
const postData = {
  title: '文章标题',
  content: '文章内容',
  status: 'draft' // 或 'publish'
};

const response = await api.post('/posts', postData);
    `);
    
  } catch (error) {
    console.error('\n❌ 测试过程中发生错误:', error.message);
  }
}

// 运行测试
testWithAppPassword();