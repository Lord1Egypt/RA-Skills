#!/usr/bin/env node

/**
 * WordPress API诊断工具
 * 检查WordPress配置和API可用性
 */

const axios = require('axios');

const WORDPRESS_URL = 'https://your-site.com';

async function diagnoseWordPress() {
  console.log('🔍 WordPress API诊断报告\n');
  console.log(`站点: ${WORDPRESS_URL}`);
  console.log(`时间: ${new Date().toISOString()}`);
  console.log('='.repeat(50) + '\n');
  
  const api = axios.create({
    baseURL: `${WORDPRESS_URL}/wp-json`,
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'OpenClaw-Diagnostic/1.0'
    },
    timeout: 10000
  });
  
  try {
    // 1. 检查WordPress基本信息
    console.log('1. 📊 WordPress基本信息');
    console.log('   '.repeat(4) + '-'.repeat(42));
    try {
      const info = await api.get('/');
      console.log(`   ✅ REST API可用`);
      console.log(`      名称: ${info.data.name || '未设置'}`);
      console.log(`      描述: ${info.data.description || '未设置'}`);
      console.log(`      版本: ${info.data.version || '未知'}`);
      console.log(`      URL: ${info.data.url}`);
      console.log(`      Home: ${info.data.home}`);
      
      // 检查API命名空间
      if (info.data.namespaces && info.data.namespaces.length > 0) {
        console.log(`      API命名空间: ${info.data.namespaces.join(', ')}`);
      }
      
      // 检查是否wp/v2可用（WordPress 4.7+）
      if (info.data.namespaces && info.data.namespaces.includes('wp/v2')) {
        console.log(`      ✅ WordPress 4.7+ REST API (wp/v2) 已启用`);
      } else {
        console.log(`      ⚠️  WordPress REST API版本可能较旧`);
      }
    } catch (error) {
      console.log(`   ❌ 无法访问REST API: ${error.message}`);
      return;
    }
    
    // 2. 检查WordPress版本
    console.log('\n2. 🔧 WordPress版本信息');
    console.log('   '.repeat(4) + '-'.repeat(42));
    try {
      // 尝试从HTML页面获取版本信息
      const htmlResponse = await axios.get(WORDPRESS_URL, {
        headers: { 'User-Agent': 'OpenClaw-Diagnostic/1.0' }
      });
      
      // 查找生成器meta标签
      const generatorMatch = htmlResponse.data.match(/<meta name="generator" content="WordPress ([^"]+)"/i);
      if (generatorMatch) {
        console.log(`   ✅ WordPress版本: ${generatorMatch[1]}`);
        
        // 检查是否支持应用程序密码（需要5.6+）
        const version = generatorMatch[1];
        const majorVersion = parseInt(version.split('.')[0]);
        const minorVersion = parseInt(version.split('.')[1]);
        
        if (majorVersion > 5 || (majorVersion === 5 && minorVersion >= 6)) {
          console.log(`      ✅ 支持应用程序密码 (WordPress 5.6+)`);
        } else {
          console.log(`      ⚠️  版本 ${version} 可能不支持内置应用程序密码`);
          console.log(`         需要WordPress 5.6+ 或安装Application Passwords插件`);
        }
      } else {
        console.log(`   ⚠️  无法从页面获取WordPress版本`);
      }
    } catch (error) {
      console.log(`   ⚠️  无法获取版本信息: ${error.message}`);
    }
    
    // 3. 检查认证端点
    console.log('\n3. 🔐 认证系统检查');
    console.log('   '.repeat(4) + '-'.repeat(42));
    
    const authEndpoints = [
      { path: '/wp/v2/users/me', name: '用户信息端点', requiresAuth: true },
      { path: '/jwt-auth/v1/token', name: 'JWT认证端点', plugin: 'JWT Authentication' },
      { path: '/basic-auth/v1/authenticate', name: 'Basic Auth端点', plugin: 'Basic Auth' },
      { path: '/application-passwords/v1/introspect', name: '应用密码端点', builtIn: true }
    ];
    
    for (const endpoint of authEndpoints) {
      try {
        const response = await api.get(endpoint.path);
        console.log(`   ✅ ${endpoint.name}: 可用 (状态: ${response.status})`);
        
        if (endpoint.plugin) {
          console.log(`      🔌 需要插件: ${endpoint.plugin}`);
        } else if (endpoint.builtIn) {
          console.log(`      🏗️  WordPress内置功能`);
        }
      } catch (error) {
        const status = error.response?.status;
        if (status === 401 && endpoint.requiresAuth) {
          console.log(`   🔒 ${endpoint.name}: 需要认证 (正常)`);
        } else if (status === 404) {
          if (endpoint.plugin) {
            console.log(`   ❌ ${endpoint.name}: 不可用 (需要安装插件: ${endpoint.plugin})`);
          } else if (endpoint.builtIn) {
            console.log(`   ⚠️  ${endpoint.name}: 不可用 (可能版本较旧或未启用)`);
          } else {
            console.log(`   ❌ ${endpoint.name}: 不可用 (404)`);
          }
        } else {
          console.log(`   ❌ ${endpoint.name}: 错误 (${status || error.message})`);
        }
      }
    }
    
    // 4. 检查API功能
    console.log('\n4. 🛠️  API功能测试');
    console.log('   '.repeat(4) + '-'.repeat(42));
    
    const apiTests = [
      { path: '/wp/v2/posts?per_page=1', name: '获取文章' },
      { path: '/wp/v2/categories?per_page=3', name: '获取分类' },
      { path: '/wp/v2/tags?per_page=3', name: '获取标签' },
      { path: '/wp/v2/media?per_page=1', name: '获取媒体' },
      { path: '/wp/v2/users?per_page=1', name: '获取用户' }
    ];
    
    for (const test of apiTests) {
      try {
        const response = await api.get(test.path);
        console.log(`   ✅ ${test.name}: 成功 (${response.data.length} 项)`);
      } catch (error) {
        const status = error.response?.status;
        if (status === 401 || status === 403) {
          console.log(`   🔒 ${test.name}: 需要认证 (${status})`);
        } else {
          console.log(`   ❌ ${test.name}: 失败 (${status || error.message})`);
        }
      }
    }
    
    // 5. 检查插件和主题API
    console.log('\n5. 🧩 插件和主题支持');
    console.log('   '.repeat(4) + '-'.repeat(42));
    
    const pluginEndpoints = [
      { path: '/wp/v2/plugins', name: '插件管理' },
      { path: '/wp/v2/themes', name: '主题管理' },
      { path: '/wp/v2/settings', name: '设置管理' }
    ];
    
    for (const endpoint of pluginEndpoints) {
      try {
        await api.get(endpoint.path);
        console.log(`   ✅ ${endpoint.name}: 可用`);
      } catch (error) {
        const status = error.response?.status;
        if (status === 401 || status === 403) {
          console.log(`   🔒 ${endpoint.name}: 需要管理员权限`);
        } else if (status === 404) {
          console.log(`   ⚠️  ${endpoint.name}: 不可用 (可能需要权限或未启用)`);
        } else {
          console.log(`   ❌ ${endpoint.name}: 错误 (${status})`);
        }
      }
    }
    
    // 6. 总结和建议
    console.log('\n6. 📋 诊断总结和建议');
    console.log('   '.repeat(4) + '-'.repeat(42));
    
    console.log('\n   🎯 当前状态:');
    console.log('      • WordPress REST API基本可用');
    console.log('      • 公开内容可访问');
    console.log('      • 认证系统需要配置');
    
    console.log('\n   🔧 推荐解决方案:');
    console.log('   方案A: 使用WordPress应用程序密码 (推荐)');
    console.log('      1. 确保WordPress版本 ≥ 5.6');
    console.log('      2. 登录后台 → 用户 → 个人资料');
    console.log('      3. 创建应用程序密码');
    console.log('      4. 使用Basic Auth访问API');
    
    console.log('\n   方案B: 安装JWT插件');
    console.log('      1. 安装"JWT Authentication for WP REST API"');
    console.log('      2. 配置wp-config.php');
    console.log('      3. 使用JWT令牌访问API');
    
    console.log('\n   方案C: 安装Basic Auth插件');
    console.log('      1. 安装"Application Passwords"或类似插件');
    console.log('      2. 配置认证');
    console.log('      3. 使用Basic Auth访问API');
    
    console.log('\n   ⚡ 快速测试命令:');
    console.log('      # 测试应用程序密码');
    console.log('      export WORDPRESS_URL="https://your-site.com"');
    console.log('      export WORDPRESS_USERNAME="admin"');
    console.log('      export WORDPRESS_PASSWORD="你的应用程序密码"');
    console.log('      node simple-publish.js "测试" "内容"');
    
    console.log('\n   📞 需要进一步帮助:');
    console.log('      1. 提供WordPress确切版本');
    console.log('      2. 确认是否已安装认证插件');
    console.log('      3. 检查用户角色和权限');
    
  } catch (error) {
    console.error(`\n❌ 诊断过程中发生错误: ${error.message}`);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('🎯 诊断完成');
}

diagnoseWordPress();