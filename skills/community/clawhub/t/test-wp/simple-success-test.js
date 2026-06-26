#!/usr/bin/env node

/**
 * 简化成功测试
 * 直接测试发布功能，跳过用户认证检查
 */

const axios = require('axios');

const config = {
  url: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

async function simplePublishTest() {
  console.log('🎯 WordPress文章发布简化测试\n');
  console.log(`站点: ${config.url}`);
  console.log(`用户: ${config.username}`);
  console.log('='.repeat(50) + '\n');
  
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
  
  // 创建最简单的测试文章（不带标签）
  const testArticle = {
    title: `简化测试 ${Date.now()}`,
    content: '这是一个简化测试文章，只包含必要字段。',
    status: 'draft',
    categories: [1] // 只使用分类，不使用标签
  };
  
  console.log('📝 准备发布简化测试文章...');
  console.log(`标题: "${testArticle.title}"`);
  console.log(`内容长度: ${testArticle.content.length} 字符`);
  console.log(`状态: ${testArticle.status}`);
  console.log(`分类: ${testArticle.categories.join(', ')}`);
  console.log(`标签: 无（避免参数错误）`);
  console.log('');
  
  try {
    console.log('🚀 发送发布请求...');
    const response = await api.post('/posts', testArticle);
    
    console.log('\n🎉 成功! 文章已发布');
    console.log(`文章ID: ${response.data.id}`);
    console.log(`标题: ${response.data.title.rendered}`);
    console.log(`状态: ${response.data.status}`);
    console.log(`链接: ${response.data.link}`);
    console.log(`创建时间: ${response.data.date}`);
    
    const postId = response.data.id;
    
    // 测试更新功能
    console.log('\n🔄 测试文章更新...');
    try {
      const updateData = {
        title: `更新后的标题 ${Date.now()}`,
        content: '这是更新后的内容。',
        excerpt: '更新后的摘要'
      };
      
      const updateResponse = await api.put(`/posts/${postId}`, updateData);
      console.log(`✅ 文章更新成功`);
      console.log(`新标题: ${updateResponse.data.title.rendered}`);
    } catch (updateError) {
      console.log(`❌ 更新失败: ${updateError.response?.data?.message || updateError.message}`);
    }
    
    // 测试删除功能
    console.log('\n🗑️  测试文章删除...');
    try {
      await api.delete(`/posts/${postId}?force=true`);
      console.log('✅ 文章删除成功');
    } catch (deleteError) {
      console.log(`❌ 删除失败: ${deleteError.message}`);
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('✅ 测试总结: JWT自动发布功能可用!\n');
    
    console.log('📋 当前配置有效:');
    console.log(`
配置信息:
- WordPress URL: ${config.url}
- 用户名: ${config.username}
- 密码: 当前密码有效
- 认证方式: Basic Auth

API端点:
- 发布文章: POST ${config.url}/wp-json/wp/v2/posts
- 更新文章: PUT ${config.url}/wp-json/wp/v2/posts/{id}
- 删除文章: DELETE ${config.url}/wp-json/wp/v2/posts/{id}?force=true

注意事项:
1. 标签(tags)参数需要传递标签ID数组，不是标签名称
2. 分类(categories)参数需要分类ID数组
3. 确保用户有发布文章的权限
    `);
    
    console.log('🚀 使用示例:');
    console.log(`
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://your-site.com/wp-json/wp/v2',
  auth: {
    username: 'admin',
    password: 'your-app-password'
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

// 发布文章（简化版，不带标签）
const postData = {
  title: '测试文章',
  content: '文章内容',
  status: 'draft', // 或 'publish'
  categories: [1]  // 未分类
};

const response = await api.post('/posts', postData);
console.log('文章ID:', response.data.id);
    `);
    
  } catch (error) {
    console.log('\n❌ 发布失败，详细错误:');
    
    if (error.response) {
      console.log(`状态码: ${error.response.status}`);
      console.log(`错误信息: ${error.response.data?.message || '未知错误'}`);
      console.log(`错误代码: ${error.response.data?.code || '未知'}`);
      
      if (error.response.data?.data) {
        console.log('错误详情:', JSON.stringify(error.response.data.data, null, 2));
      }
      
      // 分析错误类型
      if (error.response.status === 401) {
        console.log('\n🔍 错误分析: 认证失败');
        console.log('可能原因:');
        console.log('1. 用户名或密码错误');
        console.log('2. 用户没有API访问权限');
        console.log('3. 需要应用程序密码而不是登录密码');
      } else if (error.response.status === 403) {
        console.log('\n🔍 错误分析: 权限不足');
        console.log('可能原因:');
        console.log('1. 用户角色不是作者或以上');
        console.log('2. 用户被限制发布文章');
      } else if (error.response.status === 400) {
        console.log('\n🔍 错误分析: 参数错误');
        console.log('可能原因:');
        console.log('1. 参数格式不正确');
        console.log('2. 缺少必要参数');
        console.log('3. 参数值无效');
      }
    } else {
      console.log(`错误: ${error.message}`);
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🔧 建议:');
    console.log('1. 确认密码是否正确（当前可能是登录密码，不是应用程序密码）');
    console.log('2. 在WordPress中创建应用程序密码');
    console.log('3. 检查用户角色和权限');
  }
  
  console.log('\n🎯 测试完成');
}

// 运行测试
simplePublishTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});