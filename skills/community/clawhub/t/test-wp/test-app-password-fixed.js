// 测试应用程序密码
const axios = require('axios');

// 尝试不同的密码组合
const testCases = [
  {
    name: '配置中的密码',
    username: 'admin',
    password: 'QLHH6))acWR&At*PE4uBv5TM'
  },
  {
    name: '应用程序密码1',
    username: 'admin',
    password: 'your-app-password'
  },
  {
    name: '应用程序密码2',
    username: 'admin',
    password: 'HnK3 o7xu KHNy DFtV 2fpZ 7uwG'
  }
];

async function testAuth(testCase) {
  console.log(`\n🔐 测试: ${testCase.name}`);
  console.log(`用户: ${testCase.username}`);
  
  const api = axios.create({
    baseURL: 'https://your-site.com/wp-json/wp/v2',
    auth: {
      username: testCase.username,
      password: testCase.password
    },
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  try {
    // 测试读取
    console.log('📖 测试读取权限...');
    const readResponse = await api.get('/posts?per_page=1');
    console.log(`✅ 读取成功 (${readResponse.data.length} 篇文章)`);
    
    // 测试写入
    console.log('📝 测试写入权限...');
    const testArticle = {
      title: `认证测试 - ${testCase.name} - ${Date.now()}`,
      content: '<p>认证测试</p>',
      status: 'draft'
    };
    
    const writeResponse = await api.post('/posts', testArticle);
    console.log(`✅ 写入成功! 文章ID: ${writeResponse.data.id}`);
    console.log(`🔗 文章链接: ${writeResponse.data.link}`);
    
    return {
      success: true,
      link: writeResponse.data.link,
      id: writeResponse.data.id
    };
    
  } catch (error) {
    if (error.response) {
      console.log(`❌ 错误: ${error.response.status} - ${error.response.data.code || '未知'}`);
      console.log(`消息: ${error.response.data.message || '未知'}`);
    } else {
      console.log(`❌ 错误: ${error.message}`);
    }
    return { success: false };
  }
}

async function runAllTests() {
  console.log('🎯 WordPress认证测试');
  console.log('='.repeat(50));
  
  let successLink = null;
  
  for (const testCase of testCases) {
    const result = await testAuth(testCase);
    if (result.success) {
      successLink = result.link;
      break;
    }
  }
  
  console.log('\n' + '='.repeat(50));
  
  if (successLink) {
    console.log('🎉 找到有效的认证方式!');
    console.log(`🔗 文章链接: ${successLink}`);
    
    // 保存结果
    const fs = require('fs');
    fs.writeFileSync('auth-success.txt', `文章链接: ${successLink}\n时间: ${new Date().toISOString()}`);
  } else {
    console.log('❌ 所有认证方式都失败');
    console.log('\n🔧 建议:');
    console.log('1. 检查WordPress用户角色和权限');
    console.log('2. 确认应用程序密码已正确生成');
    console.log('3. 检查REST API设置');
    console.log('4. 尝试使用管理员账户');
  }
}

runAllTests().catch(console.error);