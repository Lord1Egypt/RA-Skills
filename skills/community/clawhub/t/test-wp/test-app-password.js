#!/usr/bin/env node

/**
 * WordPress应用程序密码测试
 * WordPress 5.6+ 内置了应用程序密码功能
 * 无需安装额外插件
 */

const axios = require('axios');

// WordPress配置
const config = {
  url: 'https://your-site.com',
  username: 'admin',
  appPassword: 'HnK3 o7xu KHNy DFtV 2fpZ 7uwG'  // 应用程序密码
};

async function testAppPassword() {
  console.log('🔐 测试WordPress应用程序密码...\n');
  console.log(`WordPress站点: ${config.url}`);
  console.log(`用户名: ${config.username}`);
  console.log(`应用程序密码: ${config.appPassword ? '已设置' : '未设置'}`);
  console.log('---\n');
  
  // 创建API实例，使用应用程序密码进行Basic Auth
  const api = axios.create({
    baseURL: `${config.url}/wp-json/wp/v2`,
    auth: {
      username: config.username,
      password: config.appPassword
    },
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  try {
    // 测试1: 获取当前用户信息
    console.log('1. 获取当前用户信息...');
    try {
      const response = await api.get('/users/me');
      console.log('✅ 用户信息获取成功！');
      console.log(`   用户名: ${response.data.username}`);
      console.log(`   显示名: ${response.data.name}`);
      console.log(`   角色: ${response.data.roles ? response.data.roles.join(', ') : '未知'}`);
      console.log(`   ID: ${response.data.id}`);
      console.log(`   邮箱: ${response.data.email}`);
    } catch (error) {
      console.log('❌ 用户信息获取失败:', error.response?.data?.message || error.message);
      console.log('   状态码:', error.response?.status);
      console.log('   错误代码:', error.response?.data?.code);
    }
    
    // 测试2: 创建测试文章
    console.log('\n2. 创建测试文章...');
    try {
      const postData = {
        title: '应用程序密码测试 ' + Date.now(),
        content: '这是一个通过应用程序密码创建的测试文章',
        status: 'draft',
        excerpt: '应用程序密码测试摘要',
        categories: [1]  // 未分类
      };
      
      const response = await api.post('/posts', postData);
      console.log('✅ 文章创建成功！');
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   标题: ${response.data.title.rendered}`);
      console.log(`   状态: ${response.data.status}`);
      console.log(`   链接: ${response.data.link}`);
      console.log(`   创建时间: ${response.data.date}`);
      
      const postId = response.data.id;
      
      // 测试3: 更新文章
      console.log('\n3. 更新测试文章...');
      try {
        const updateData = {
          title: '更新后的标题 ' + Date.now(),
          content: '这是更新后的内容',
          excerpt: '更新后的摘要'
        };
        
        const updateResponse = await api.put(`/posts/${postId}`, updateData);
        console.log('✅ 文章更新成功！');
        console.log(`   新标题: ${updateResponse.data.title.rendered}`);
      } catch (updateError) {
        console.log('❌ 文章更新失败:', updateError.response?.data?.message || updateError.message);
      }
      
      // 测试4: 删除测试文章
      console.log('\n4. 删除测试文章...');
      try {
        await api.delete(`/posts/${postId}?force=true`);
        console.log('✅ 文章删除成功');
      } catch (deleteError) {
        console.log('❌ 文章删除失败:', deleteError.response?.data?.message || deleteError.message);
      }
      
    } catch (error) {
      console.log('❌ 文章创建失败:', error.response?.data?.message || error.message);
      console.log('   状态码:', error.response?.status);
      console.log('   错误代码:', error.response?.data?.code);
      console.log('   详细错误:', JSON.stringify(error.response?.data, null, 2));
    }
    
    // 测试5: 获取文章列表（带认证）
    console.log('\n5. 获取文章列表（带认证）...');
    try {
      const response = await api.get('/posts?per_page=3&status=draft,publish');
      console.log(`✅ 成功获取 ${response.data.length} 篇文章`);
      response.data.forEach(post => {
        console.log(`   - "${post.title.rendered}" (ID: ${post.id}, 状态: ${post.status})`);
      });
    } catch (error) {
      console.log('❌ 获取文章列表失败:', error.response?.data?.message || error.message);
    }
    
    // 测试6: 创建分类
    console.log('\n6. 创建测试分类...');
    try {
      const categoryData = {
        name: '测试分类 ' + Date.now(),
        description: '这是一个测试分类',
        slug: 'test-category-' + Date.now()
      };
      
      const response = await api.post('/categories', categoryData);
      console.log('✅ 分类创建成功！');
      console.log(`   分类ID: ${response.data.id}`);
      console.log(`   名称: ${response.data.name}`);
      console.log(`   Slug: ${response.data.slug}`);
      
      const categoryId = response.data.id;
      
      // 删除测试分类
      try {
        await api.delete(`/categories/${categoryId}?force=true`);
        console.log('✅ 分类删除成功');
      } catch (deleteError) {
        console.log('❌ 分类删除失败');
      }
    } catch (error) {
      console.log('❌ 分类创建失败:', error.response?.data?.message || error.message);
    }
    
  } catch (error) {
    console.error('❌ 测试过程中发生错误:', error.message);
  }
  
  console.log('\n🎯 应用程序密码测试完成！');
  console.log('\n📋 如何获取应用程序密码:');
  console.log('1. 登录WordPress后台');
  console.log('2. 进入"用户" → "个人资料"');
  console.log('3. 滚动到"应用程序密码"部分');
  console.log('4. 输入名称（如"API访问"）并点击"添加新应用程序密码"');
  console.log('5. 复制生成的密码（只显示一次）');
  console.log('\n🔧 使用示例:');
  console.log(`
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://your-site.com/wp-json/wp/v2',
  auth: {
    username: 'your-username',
    password: 'your-app-password'  // 应用程序密码，不是登录密码
  },
  headers: {
    'Content-Type': 'application/json'
  }
});
  `);
}

// 运行测试
testAppPassword();