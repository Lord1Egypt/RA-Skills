const { chromium } = require('playwright');
const path = require('path');
const os = require('os');

(async () => {
  console.log('🚀 启动 ClawHub 自动发布...\n');
  
  // 使用已安装的 Chrome
  const browser = await chromium.launch({
    headless: false,  // 显示浏览器窗口
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  
  const page = await context.newPage();

  try {
    // 1. 访问 ClawHub publish 页面
    console.log('1️⃣  访问 ClawHub publish 页面...');
    await page.goto('https://clawhub.com/publish', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(3000);
    
    // 2. 检查是否需要登录
    const loginButton = await page.locator('button:has-text("Sign in"), a:has-text("Sign in")').first();
    if (await loginButton.isVisible().catch(() => false)) {
      console.log('⚠️  检测到登录按钮，请确认是否已登录...');
      console.log('如果已登录，请等待页面自动跳转...');
      await page.waitForTimeout(5000);
    }
    
    // 3. 等待表单加载
    console.log('2️⃣  等待表单加载...');
    await page.waitForSelector('input[type="file"], input[name="name"], form', { timeout: 30000 });
    console.log('   ✅ 表单已加载');
    
    // 4. 上传文件
    console.log('3️⃣  上传文件...');
    const fileInput = await page.locator('input[type="file"]').first();
    const filePath = path.join(os.homedir(), 'Desktop', 'qqbot-v1.0.0.zip');
    await fileInput.setInputFiles(filePath);
    console.log('   ✅ 文件已选择:', filePath);
    await page.waitForTimeout(2000);
    
    // 5. 填写表单
    console.log('4️⃣  填写表单...');
    
    // 名称
    await page.fill('input[name="name"], input[placeholder*="name" i]', 'qqbot');
    console.log('   ✅ 名称: qqbot');
    
    // 版本
    await page.fill('input[name="version"], input[placeholder*="version" i]', '1.0.0');
    console.log('   ✅ 版本: 1.0.0');
    
    // 描述
    const description = `QQ 官方机器人配置指南，包含完整部署流程和常见问题解决方案

一键配置 QQ 官方机器人，支持私聊、群聊、频道消息。

功能特点:
✅ WebSocket 实时连接
✅ 支持私聊、群聊、频道消息
✅ 内置 AI 处理器接口
✅ 完整的故障排除指南
✅ 自动 IP 白名单监控脚本

安装命令: openclaw skill install qqbot`;
    
    await page.fill('textarea[name="description"], textarea[placeholder*="description" i]', description);
    console.log('   ✅ 描述已填写');
    
    // 作者
    await page.fill('input[name="author"], input[placeholder*="author" i]', '小皮');
    console.log('   ✅ 作者: 小皮');
    
    // 6. 选择许可证和分类
    console.log('5️⃣  选择许可证和分类...');
    
    // 尝试选择 MIT 许可证
    try {
      await page.selectOption('select[name="license"]', 'MIT');
      console.log('   ✅ 许可证: MIT');
    } catch (e) {
      console.log('   ⚠️  许可证选择失败（可能不需要或需要手动选择）');
    }
    
    // 尝试选择分类
    try {
      await page.selectOption('select[name="category"]', { label: 'IM' });
      console.log('   ✅ 分类: IM');
    } catch (e) {
      console.log('   ⚠️  分类选择失败（可能不需要或需要手动选择）');
    }
    
    // 7. 添加标签
    console.log('6️⃣  添加标签...');
    const tags = ['qq', 'bot', 'im', '机器人'];
    for (const tag of tags) {
      try {
        const tagInput = await page.locator('input[placeholder*="tag" i], input[name*="tag"]').first();
        await tagInput.fill(tag);
        await tagInput.press('Enter');
        await page.waitForTimeout(500);
        console.log(`   ✅ 标签: ${tag}`);
      } catch (e) {
        console.log(`   ⚠️  标签 ${tag} 添加失败`);
      }
    }
    
    console.log('\n✅ 表单填写完成！');
    console.log('⏳ 请在浏览器中检查信息是否正确，然后手动点击 Submit 按钮');
    console.log('📝 浏览器将保持打开，等待您确认提交...\n');
    
    // 保持浏览器打开，让用户确认并提交
    await new Promise(() => {});
    
  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    console.log('\n⚠️  请手动完成发布');
    
    // 截图保存
    try {
      await page.screenshot({ path: '/tmp/clawhub-error.png', fullPage: true });
      console.log('📸 错误截图已保存: /tmp/clawhub-error.png');
    } catch (e) {}
    
    await browser.close();
    process.exit(1);
  }
})();
