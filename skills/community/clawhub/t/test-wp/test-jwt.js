#!/usr/bin/env node

/**
 * WordPress JWT认证测试
 * 需要安装JWT Authentication for WP REST API插件
 * 插件地址: https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/
 */

const axios = require('axios');

// WordPress配置
const config = {
  url: 'https://your-site.com',  // 修改为你的WordPress站点
  username: 'admin',       // 修改为你的用户名
  password: 'HnK3 o7xu KHNy DFtV 2fpZ 7uwG'  // 修改为你的密码
};

// JWT认证端点
const JWT_ENDPOINT = '/wp-json/jwt-auth/v1/token';
const JWT_VALIDATE_ENDPOINT = '/wp-json/jwt-auth/v1/token/validate';

// 创建axios实例
const api = axios.create({
  baseURL: config.url,
  headers: {
    'Content-Type': 'application/json'
  }
});

async function testJWT() {
  console.log('🔐 测试WordPress JWT认证...\n');
  console.log(`WordPress站点: ${config.url}`);
  console.log(`用户名: ${config.username}`);
  console.log('---\n');
  
  try {
    // 步骤1: 获取JWT令牌
    console.log('1. 获取JWT令牌...');
    const tokenResponse = await api.post(JWT_ENDPOINT, {
      username: config.username,
      password: config.password
    });
    
    if (tokenResponse.data && tokenResponse.data.token) {
      const jwtToken = tokenResponse.data.token;
      console.log('✅ JWT令牌获取成功！');
      console.log(`   令牌: ${jwtToken.substring(0, 30)}...`);
      console.log(`   用户邮箱: ${tokenResponse.data.user_email}`);
      console.log(`   用户昵称: ${tokenResponse.data.user_nicename}`);
      console.log(`   用户显示名: ${tokenResponse.data.user_display_name}`);
      
      // 步骤2: 验证JWT令牌
      console.log('\n2. 验证JWT令牌...');
      try {
        const validateResponse = await api.post(JWT_VALIDATE_ENDPOINT, {}, {
          headers: {
            'Authorization': `Bearer ${jwtToken}`
          }
        });
        console.log('✅ JWT令牌验证成功！');
        console.log(`   状态码: ${validateResponse.status}`);
        console.log(`   返回数据: ${JSON.stringify(validateResponse.data)}`);
      } catch (validateError) {
        console.log('❌ JWT令牌验证失败:', validateError.response?.data?.message || validateError.message);
      }
      
      // 步骤3: 使用JWT访问WordPress REST API
      console.log('\n3. 使用JWT访问WordPress REST API...');
      
      // 创建带JWT认证的API实例
      const jwtApi = axios.create({
        baseURL: `${config.url}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${jwtToken}`,
          'Content-Type': 'application/json'
        }
      });
      
      // 测试3.1: 获取当前用户信息
      console.log('3.1 获取当前用户信息...');
      try {
        const userResponse = await jwtApi.get('/users/me');
        console.log('✅ 用户信息获取成功:');
        console.log(`   用户名: ${userResponse.data.username}`);
        console.log(`   显示名: ${userResponse.data.name}`);
        console.log(`   角色: ${userResponse.data.roles ? userResponse.data.roles.join(', ') : '未知'}`);
        console.log(`   ID: ${userResponse.data.id}`);
      } catch (userError) {
        console.log('❌ 用户信息获取失败:', userError.response?.data?.message || userError.message);
      }
      
      // 测试3.2: 创建测试文章
      console.log('\n3.2 创建测试文章...');
      try {
        const postData = {
          title: 'JWT API测试文章 ' + Date.now(),
          content: '这是一个通过JWT认证创建的测试文章',
          status: 'draft',
          excerpt: 'JWT认证测试摘要'
        };
        
        const postResponse = await jwtApi.post('/posts', postData);
        console.log('✅ 文章创建成功！');
        console.log(`   文章ID: ${postResponse.data.id}`);
        console.log(`   标题: ${postResponse.data.title.rendered}`);
        console.log(`   状态: ${postResponse.data.status}`);
        console.log(`   链接: ${postResponse.data.link}`);
        
        // 测试3.3: 删除测试文章
        console.log('\n3.3 删除测试文章...');
        try {
          await jwtApi.delete(`/posts/${postResponse.data.id}?force=true`);
          console.log('✅ 文章删除成功');
        } catch (deleteError) {
          console.log('❌ 文章删除失败:', deleteError.response?.data?.message || deleteError.message);
        }
      } catch (postError) {
        console.log('❌ 文章创建失败:', postError.response?.data?.message || postError.message);
        console.log('   状态码:', postError.response?.status);
        console.log('   错误代码:', postError.response?.data?.code);
      }
      
      // 测试3.4: 获取分类列表
      console.log('\n3.4 获取分类列表...');
      try {
        const categoriesResponse = await jwtApi.get('/categories?per_page=5');
        console.log(`✅ 成功获取 ${categoriesResponse.data.length} 个分类`);
        categoriesResponse.data.forEach(cat => {
          console.log(`   - ${cat.name} (ID: ${cat.id}, 文章数: ${cat.count})`);
        });
      } catch (catError) {
        console.log('❌ 分类获取失败:', catError.response?.data?.message || catError.message);
      }
      
      // 测试3.5: 上传媒体文件（如果需要）
      console.log('\n3.5 测试媒体上传权限...');
      try {
        // 这里可以测试媒体上传，但需要实际文件
        console.log('ℹ️  媒体上传测试需要实际文件，跳过此测试');
      } catch (mediaError) {
        console.log('❌ 媒体权限测试失败:', mediaError.response?.data?.message || mediaError.message);
      }
      
    } else {
      console.log('❌ JWT令牌获取失败: 响应中没有token字段');
      console.log('响应数据:', JSON.stringify(tokenResponse.data, null, 2));
    }
    
  } catch (error) {
    console.error('❌ JWT测试过程中发生错误:');
    
    if (error.response) {
      // 服务器响应了错误状态码
      console.log('状态码:', error.response.status);
      console.log('响应数据:', JSON.stringify(error.response.data, null, 2));
      console.log('响应头:', error.response.headers);
      
      // 检查是否是JWT插件未安装
      if (error.response.status === 404) {
        console.log('\n⚠️  可能的原因:');
        console.log('1. JWT Authentication for WP REST API插件未安装');
        console.log('2. WordPress站点URL不正确');
        console.log('3. JWT插件未激活');
        console.log('\n🔧 解决方案:');
        console.log('1. 安装插件: https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/');
        console.log('2. 在wp-config.php中添加以下代码:');
        console.log(`
define('JWT_AUTH_SECRET_KEY', 'your-top-secret-key');
define('JWT_AUTH_CORS_ENABLE', true);
        `);
      }
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.log('没有收到响应:', error.request);
    } else {
      // 请求设置时发生错误
      console.log('请求错误:', error.message);
    }
  }
  
  console.log('\n🎯 JWT测试完成！');
  console.log('\n📋 总结:');
  console.log('如果JWT认证成功，你可以使用以下方式调用WordPress API:');
  console.log(`
const axios = require('axios');

const jwtApi = axios.create({
  baseURL: '${config.url}/wp-json/wp/v2',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  }
});

// 创建文章
const response = await jwtApi.post('/posts', {
  title: '文章标题',
  content: '文章内容',
  status: 'draft'  // 或 'publish'
});
  `);
}

// 运行测试
testJWT();