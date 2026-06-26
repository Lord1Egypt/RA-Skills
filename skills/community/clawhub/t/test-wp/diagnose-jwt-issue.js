#!/usr/bin/env node

/**
 * JWT插件问题诊断工具
 * 检查为什么没有 wp-json/jwt-auth/v1 目录
 */

const axios = require('axios');
const https = require('https');

const WORDPRESS_URL = 'https://your-site.com';

// 创建不验证SSL的axios实例（用于测试）
const insecureAxios = axios.create({
  httpsAgent: new https.Agent({
    rejectUnauthorized: false
  }),
  timeout: 10000,
  headers: {
    'User-Agent': 'OpenClaw-JWT-Diagnostic/1.0'
  }
});

async function diagnoseJWTIssue() {
  console.log('🔍 JWT插件问题诊断\n');
  console.log(`WordPress站点: ${WORDPRESS_URL}`);
  console.log(`诊断时间: ${new Date().toISOString()}`);
  console.log('='.repeat(60) + '\n');
  
  // 1. 检查WordPress REST API基础
  console.log('1. 📊 检查WordPress REST API基础');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  try {
    const apiBase = await insecureAxios.get(`${WORDPRESS_URL}/wp-json`);
    console.log('   ✅ WordPress REST API可用');
    
    if (apiBase.data.routes) {
      console.log(`      发现 ${Object.keys(apiBase.data.routes).length} 个API端点`);
      
      // 检查是否有jwt-auth相关端点
      const jwtRoutes = Object.keys(apiBase.data.routes).filter(route => 
        route.includes('jwt-auth') || route.includes('jwt')
      );
      
      if (jwtRoutes.length > 0) {
        console.log(`      ✅ 发现JWT相关端点: ${jwtRoutes.length} 个`);
        jwtRoutes.forEach(route => {
          console.log(`          - ${route}`);
        });
      } else {
        console.log(`      ❌ 未发现JWT相关端点`);
      }
    }
  } catch (error) {
    console.log(`   ❌ WordPress REST API不可用: ${error.message}`);
    console.log(`      HTTP状态码: ${error.response?.status}`);
    return;
  }
  
  // 2. 测试JWT端点
  console.log('\n2. 🔐 测试JWT认证端点');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  const jwtEndpoints = [
    '/wp-json/jwt-auth/v1/token',
    '/wp-json/jwt-auth/v1/token/validate',
    '/?rest_route=/jwt-auth/v1/token',  // 备用URL格式
    '/index.php?rest_route=/jwt-auth/v1/token'  // 另一种格式
  ];
  
  for (const endpoint of jwtEndpoints) {
    try {
      const response = await insecureAxios.get(`${WORDPRESS_URL}${endpoint}`);
      console.log(`   ✅ ${endpoint}: 可用 (${response.status})`);
      
      if (response.data && typeof response.data === 'object') {
        console.log(`      响应类型: ${response.data.code ? '错误' : '正常'}`);
        if (response.data.message) {
          console.log(`      消息: ${response.data.message}`);
        }
      }
    } catch (error) {
      const status = error.response?.status;
      if (status === 404) {
        console.log(`   ❌ ${endpoint}: 不存在 (404)`);
      } else if (status === 405) {
        console.log(`   ⚠️  ${endpoint}: 方法不允许 (405) - 可能需要POST请求`);
      } else if (status === 500) {
        console.log(`   🔥 ${endpoint}: 服务器错误 (500) - 可能配置有问题`);
      } else if (error.code === 'ECONNREFUSED') {
        console.log(`   ❌ ${endpoint}: 连接被拒绝`);
      } else {
        console.log(`   ❌ ${endpoint}: 错误 (${status || error.message})`);
      }
    }
  }
  
  // 3. 检查插件API端点
  console.log('\n3. 🧩 检查其他插件端点');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  const pluginEndpoints = [
    '/wp-json/wp/v2',  // WordPress核心API
    '/wp-json/wp/v2/posts',  // 文章API
    '/wp-json/oembed/1.0',  // oEmbed端点
    '/wp-admin/admin-ajax.php'  // Admin AJAX
  ];
  
  for (const endpoint of pluginEndpoints) {
    try {
      const response = await insecureAxios.get(`${WORDPRESS_URL}${endpoint}`);
      console.log(`   ✅ ${endpoint}: 可用 (${response.status})`);
    } catch (error) {
      const status = error.response?.status;
      if (status === 404) {
        console.log(`   ❌ ${endpoint}: 不存在 (404)`);
      } else {
        console.log(`   ❌ ${endpoint}: 错误 (${status || '未知'})`);
      }
    }
  }
  
  // 4. 检查固定链接
  console.log('\n4. 🔗 检查固定链接设置');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  try {
    // 尝试访问带有rest_route参数的URL
    const restRouteTest = await insecureAxios.get(
      `${WORDPRESS_URL}/index.php?rest_route=/wp/v2/posts&per_page=1`
    );
    
    if (restRouteTest.data && Array.isArray(restRouteTest.data)) {
      console.log('   ✅ 通过rest_route参数可以访问REST API');
      console.log(`      这意味着固定链接可能未正确设置`);
      
      // 测试漂亮的URL
      try {
        await insecureAxios.get(`${WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=1`);
        console.log('   ✅ 漂亮的URL也可以工作');
      } catch (error) {
        console.log(`   ❌ 漂亮的URL无法工作: ${error.response?.status || error.message}`);
        console.log(`      🔧 建议: 重新保存固定链接设置`);
      }
    }
  } catch (error) {
    console.log(`   ❌ 无法通过rest_route测试: ${error.message}`);
  }
  
  // 5. 检查.htaccess或Nginx配置
  console.log('\n5. ⚙️  检查服务器配置线索');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  try {
    const serverHeaders = await insecureAxios.head(WORDPRESS_URL);
    const serverType = serverHeaders.headers['server'] || serverHeaders.headers['Server'];
    
    console.log(`   服务器类型: ${serverType || '未知'}`);
    
    if (serverType && serverType.toLowerCase().includes('nginx')) {
      console.log(`   🔍 检测到Nginx服务器`);
      console.log(`      Nginx需要特殊配置来支持WordPress REST API`);
    } else if (serverType && serverType.toLowerCase().includes('apache')) {
      console.log(`   🔍 检测到Apache服务器`);
      console.log(`      需要检查.htaccess文件和mod_rewrite模块`);
    }
    
    // 检查是否返回X-Powered-By
    if (serverHeaders.headers['x-powered-by']) {
      console.log(`   PHP信息: ${serverHeaders.headers['x-powered-by']}`);
    }
    
  } catch (error) {
    console.log(`   ⚠️  无法获取服务器信息: ${error.message}`);
  }
  
  // 6. 诊断总结
  console.log('\n6. 📋 诊断总结和建议');
  console.log('   '.repeat(4) + '-'.repeat(52));
  
  console.log('\n   🎯 可能的问题:');
  console.log('   1. JWT插件未安装或未激活');
  console.log('   2. 固定链接未正确设置');
  console.log('   3. 服务器配置问题（特别是Nginx）');
  console.log('   4. .htaccess文件缺失或权限问题');
  
  console.log('\n   🔧 解决方案步骤:');
  
  console.log('\n   A. 首先检查插件:');
  console.log('      1. 访问 https://your-site.com/wp-admin/plugins.php');
  console.log('      2. 检查JWT插件是否已安装并激活');
  console.log('      3. 如果未安装，下载并安装插件');
  
  console.log('\n   B. 然后检查固定链接:');
  console.log('      1. 访问 https://your-site.com/wp-admin/options-permalink.php');
  console.log('      2. 选择"文章名"或"数字"格式');
  console.log('      3. 点击"保存更改"');
  
  console.log('\n   C. 如果使用Nginx:');
  console.log('      1. 检查Nginx站点配置');
  console.log('      2. 确保有正确的重写规则');
  console.log('      3. 重启Nginx服务');
  
  console.log('\n   D. 测试命令:');
  console.log('      # 测试固定链接');
  console.log(`      curl -I "${WORDPRESS_URL}/wp-json/wp/v2"`);
  console.log('      # 测试rest_route方式');
  console.log(`      curl "${WORDPRESS_URL}/index.php?rest_route=/wp/v2/posts&per_page=1"`);
  
  console.log('\n   ⚡ 快速修复尝试:');
  console.log('      1. 禁用所有插件，然后只启用JWT插件');
  console.log('      2. 切换到默认主题测试');
  console.log('      3. 检查WordPress调试日志');
  
  console.log('\n   📞 需要的信息:');
  console.log('      1. WordPress确切的安装方式（cPanel、手动等）');
  console.log('      2. 服务器类型和配置');
  console.log('      3. 是否有服务器访问权限');
  console.log('      4. 其他插件是否正常工作');
}

// 运行诊断
diagnoseJWTIssue().catch(error => {
  console.error('诊断过程中发生错误:', error);
});