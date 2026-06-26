#!/usr/bin/env node

/**
 * 简单的WordPress权限测试
 */

const axios = require('axios');

const config = {
  url: 'https://your-site.com',
  username: 'admin',
  password: 'HnK3 o7xu KHNy DFtV 2fpZ 7uwG'
};

const api = axios.create({
  baseURL: `${config.url}/wp-json/wp/v2`,
  auth: {
    username: config.username,
    password: config.password
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

async function testPermissions() {
  console.log('🔍 测试WordPress用户权限...\n');
  
  try {
    // 测试1: 获取当前用户
    console.log('1. 测试获取当前用户信息...');
    try {
      const response = await api.get('/users/me');
      console.log('✅ 成功获取用户信息:');
      console.log(`   用户名: ${response.data.username}`);
      console.log(`   显示名: ${response.data.name}`);
      console.log(`   角色: ${response.data.roles ? response.data.roles.join(', ') : '未知'}`);
      console.log(`   ID: ${response.data.id}`);
    } catch (error) {
      console.log('❌ 获取用户信息失败:', error.response?.data?.message || error.message);
    }
    
    // 测试2: 获取文章列表（公开）
    console.log('\n2. 测试获取文章列表...');
    try {
      const response = await api.get('/posts?per_page=1');
      console.log(`✅ 成功获取 ${response.data.length} 篇文章`);
      if (response.data.length > 0) {
        console.log(`   最新文章: "${response.data[0].title.rendered}" (ID: ${response.data[0].id})`);
      }
    } catch (error) {
      console.log('❌ 获取文章列表失败:', error.response?.data?.message || error.message);
    }
    
    // 测试3: 创建草稿文章
    console.log('\n3. 测试创建草稿文章...');
    try {
      const postData = {
        title: 'API测试文章 ' + Date.now(),
        content: '这是一个通过API创建的测试文章',
        status: 'draft',
        excerpt: '测试摘要'
      };
      
      const response = await api.post('/posts', postData);
      console.log('✅ 文章创建成功！');
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   标题: ${response.data.title.rendered}`);
      console.log(`   状态: ${response.data.status}`);
      console.log(`   链接: ${response.data.link}`);
      
      // 测试4: 删除测试文章
      console.log('\n4. 测试删除文章...');
      try {
        await api.delete(`/posts/${response.data.id}?force=true`);
        console.log('✅ 文章删除成功');
      } catch (deleteError) {
        console.log('❌ 文章删除失败:', deleteError.response?.data?.message || deleteError.message);
      }
    } catch (error) {
      console.log('❌ 文章创建失败:', error.response?.data?.message || error.message);
      console.log('   状态码:', error.response?.status);
      console.log('   错误代码:', error.response?.data?.code);
    }
    
    // 测试5: 获取分类（需要编辑权限）
    console.log('\n5. 测试创建分类...');
    try {
      const categoryData = {
        name: '测试分类 ' + Date.now(),
        description: '测试分类描述'
      };
      
      const response = await api.post('/categories', categoryData);
      console.log('✅ 分类创建成功！');
      console.log(`   分类ID: ${response.data.id}`);
      console.log(`   名称: ${response.data.name}`);
      
      // 删除测试分类
      try {
        await api.delete(`/categories/${response.data.id}?force=true`);
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
  
  console.log('\n🎯 测试完成！');
}

testPermissions();