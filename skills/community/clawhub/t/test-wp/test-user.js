#!/usr/bin/env node

/**
 * 测试WordPress用户权限
 */

const config = require('./config.js');
const WordPressAPI = require('./wordpress-api.js');

const wpApi = new WordPressAPI(config);

async function testUserPermissions() {
  console.log('🔍 测试WordPress用户权限...');
  
  try {
    // 测试连接
    console.log('1. 测试API连接...');
    const connected = await wpApi.testConnection();
    if (!connected) {
      console.error('❌ API连接失败');
      return;
    }
    console.log('✅ API连接成功');
    
    // 测试获取当前用户
    console.log('\n2. 测试获取当前用户信息...');
    try {
      const users = await wpApi.getUsers();
      const currentUser = users.find(user => user.username === config.wordpress.username);
      
      if (currentUser) {
        console.log('✅ 找到当前用户:');
        console.log(`   用户名: ${currentUser.username}`);
        console.log(`   显示名: ${currentUser.name}`);
        console.log(`   角色: ${currentUser.roles ? currentUser.roles.join(', ') : '未知'}`);
        console.log(`   ID: ${currentUser.id}`);
        console.log(`   邮箱: ${currentUser.email || '未设置'}`);
        
        // 检查权限
        console.log('\n3. 检查用户权限...');
        if (currentUser.roles && currentUser.roles.length > 0) {
          const hasAuthorRole = currentUser.roles.includes('author') || 
                               currentUser.roles.includes('editor') || 
                               currentUser.roles.includes('administrator');
          
          if (hasAuthorRole) {
            console.log('✅ 用户有发布文章的权限');
          } else {
            console.log('❌ 用户角色可能没有发布权限');
            console.log(`   当前角色: ${currentUser.roles.join(', ')}`);
            console.log('   需要角色: author, editor, 或 administrator');
          }
        } else {
          console.log('⚠️  无法确定用户角色');
        }
      } else {
        console.log('❌ 未找到当前用户');
        console.log('找到的用户:', users.map(u => u.username).join(', '));
      }
    } catch (error) {
      console.error('❌ 获取用户信息失败:', error.message);
      if (error.response) {
        console.error('状态码:', error.response.status);
        console.error('响应数据:', JSON.stringify(error.response.data, null, 2));
      }
    }
    
    // 测试获取分类（这是一个公开的端点）
    console.log('\n4. 测试获取分类...');
    try {
      const categories = await wpApi.getCategories();
      console.log(`✅ 成功获取 ${categories.length} 个分类`);
      if (categories.length > 0) {
        console.log('前5个分类:');
        categories.slice(0, 5).forEach(cat => {
          console.log(`   - ${cat.name} (ID: ${cat.id}, 数量: ${cat.count})`);
        });
      }
    } catch (error) {
      console.error('❌ 获取分类失败:', error.message);
    }
    
  } catch (error) {
    console.error('❌ 测试过程中发生错误:', error.message);
  }
}

// 运行测试
testUserPermissions();