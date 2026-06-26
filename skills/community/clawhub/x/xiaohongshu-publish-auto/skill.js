const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

async function startChromeWithDebug() {
  return new Promise((resolve, reject) => {
    // 检查是否已有调试端口
    const check = spawn('curl', ['-s', 'http://localhost:9222/json/version']);
    check.on('close', (code) => {
      if (code === 0) {
        console.log('✅ Chrome 调试模式已在运行');
        resolve();
      } else {
        // 启动 Chrome
        console.log('🔄 启动 Chrome...');
        const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
        const userDataDir = process.env.HOME + '/Library/Application Support/Google/Chrome';
        
        const chrome = spawn('open', ['-a', 'Google Chrome', '--args', 
          '--remote-debugging-port=9222',
          '--no-first-run',
          '--no-default-browser-check'
        ], {
          detached: true,
          stdio: 'ignore'
        });
        chrome.unref();
        
        // 等待启动
        setTimeout(() => {
          console.log('✅ Chrome 已启动');
          resolve();
        }, 5000);
      }
    });
  });
}

async function publishXiaohongshu() {
  // 先确保 Chrome 在调试模式运行
  await startChromeWithDebug();
  
  const ICLOUD_PATH = "/Users/today/Movies/小红书英语";
  const today = new Date();
  const month = today.getMonth() + 1;
  const day = today.getDate();
  const dateStr = `${month}月${day}日`;

  console.log(`📅 今天的日期: ${dateStr}`);

  // 获取当天文件
  const videoFile = path.join(ICLOUD_PATH, `视频${dateStr}带声.mp4`);
  const titleFile = path.join(ICLOUD_PATH, `标题${dateStr}.txt`);

  if (!fs.existsSync(videoFile)) {
    console.error(`❌ 视频文件不存在: ${videoFile}`);
    return;
  }

  if (!fs.existsSync(titleFile)) {
    console.error(`❌ 标题文件不存在: ${titleFile}`);
    return;
  }

  const fillTitle = "一起学英语";
  const fullContent = fs.readFileSync(titleFile, 'utf8').trim();
  
  const bodyLines = [];
  const topics = [];
  for (const line of fullContent.split('\n')) {
    const trimmed = line.trim();
    if (trimmed.startsWith('#')) {
      const topicParts = trimmed.split(/\s+/);
      for (const part of topicParts) {
        const cleaned = part.replace(/[\u{1F300}-\u{1F9FF}]/gu, '').trim();
        if (cleaned && cleaned.startsWith('#') && cleaned.length > 1) {
          topics.push(cleaned);
        }
      }
    } else if (trimmed) {
      bodyLines.push(trimmed);
    }
  }
  const body = bodyLines.join('\n');
  
  console.log(`✅ 找到当天文件:`);
  console.log(`   视频: ${path.basename(videoFile)}`);
  console.log(`   标题: ${fillTitle}`);
  console.log(`   话题: ${topics.join(', ')}`);

  console.log('🚀 连接到 Chrome（持久化登录）...');
  const browser = await puppeteer.connect({
    browserURL: 'http://localhost:9222'
  });

  try {
    console.log('📱 打开小红书创作平台...');
    const xhsPage = await browser.newPage();
    await xhsPage.goto('https://creator.xiaohongshu.com/publish/publish', {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    await new Promise(r => setTimeout(r, 3000));
    console.log('✅ 页面加载完成');

    // === 1. 上传视频 ===
    console.log('🔍 寻找上传按钮...');
    const fileInput = await xhsPage.$('input[type="file"]');
    if (fileInput) {
      console.log('📁 上传视频...');
      await fileInput.uploadFile(videoFile);
      console.log('⏳ 等待视频上传...');
      await new Promise(r => setTimeout(r, 10000));
    }

    // === 2. 填��标题 ===
    console.log('🔍 填写标题...');
    try {
      const titleInput = await xhsPage.$('input[placeholder*="标题"]');
      if (titleInput) {
        await titleInput.focus();
        await new Promise(r => setTimeout(r, 500));
        await xhsPage.keyboard.down('Meta');
        await xhsPage.keyboard.press('a');
        await xhsPage.keyboard.up('Meta');
        await new Promise(r => setTimeout(r, 200));
        await xhsPage.keyboard.press('Backspace');
        await new Promise(r => setTimeout(r, 300));
        await titleInput.type(fillTitle, { delay: 80 });
        console.log('✅ 标题已填写: ' + fillTitle);
      }
    } catch(e) {
      console.log('⚠️ 标题填写失败: ' + e.message);
    }
    
    await new Promise(r => setTimeout(r, 1000));

    // === 3. 滚动到正文区域并填写正文（不含话题）===
    console.log('📜 滚动到正文区域...');
    await xhsPage.evaluate(() => window.scrollTo(0, 500));
    await new Promise(r => setTimeout(r, 1500));

    console.log('📝 填写正文（不含话题）...');
    try {
      const contentEl = await xhsPage.$('div[contenteditable="true"]');
      if (contentEl) {
        await contentEl.click();
        await new Promise(r => setTimeout(r, 500));
        await xhsPage.keyboard.down('Meta');
        await xhsPage.keyboard.press('a');
        await xhsPage.keyboard.up('Meta');
        await new Promise(r => setTimeout(r, 200));
        await xhsPage.keyboard.press('Backspace');
        await new Promise(r => setTimeout(r, 300));
        await contentEl.type(body, { delay: 50 });
        console.log('✅ 正文已填写（不含话题）');
      }
    } catch(e) {
      console.log('⚠️ 正文填写失败: ' + e.message);
    }
    
    await new Promise(r => setTimeout(r, 1000));

    // === 4. 逐个添加话题 ===
    console.log('🏷️ 添加话题（共' + topics.length + '个）...');
    
    for (let i = 0; i < topics.length; i++) {
      const topic = topics[i];
      console.log('   [' + (i+1) + '/' + topics.length + '] 添加: ' + topic);
      
      try {
        const contentEl = await xhsPage.$('div[contenteditable="true"]');
        if (!contentEl) continue;
        
        await contentEl.click();
        await new Promise(r => setTimeout(r, 400));
        
        // 按右箭头移到末尾
        for (let k = 0; k < 25; k++) await xhsPage.keyboard.press('ArrowRight');
        await new Promise(r => setTimeout(r, 300));
        
        // 输入空格+话题（保留#）
        await xhsPage.keyboard.type(' ', { delay: 30 });
        await new Promise(r => setTimeout(r, 200));
        await xhsPage.keyboard.type(topic, { delay: 80 });
        
        // 等待
        await new Promise(r => setTimeout(r, 1500));
        
        // 按回车确认
        await xhsPage.keyboard.press('Enter');
        console.log('   ✅ 回车确认: ' + topic);
        
        await new Promise(r => setTimeout(r, 600));
        
      } catch(e) {
        console.log('   ⚠️ ' + topic + ' 失败: ' + e.message);
      }
    }
    
    await new Promise(r => setTimeout(r, 1000));
    await xhsPage.screenshot({ path: '/tmp/xhs-topics-check.png', fullPage: true });
    console.log('📸 话题截图已保存');

    // === 5. 滚动到页面底部 ===
    await xhsPage.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise(r => setTimeout(r, 2000));

    // === 6. 点击发布按钮 ===
    console.log('🔴 点击发布按钮...');
    
    let clicked = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      const result = await xhsPage.evaluate(() => {
        const btns = document.querySelectorAll('button');
        for (const btn of btns) {
          if (btn.textContent.trim() === '发布' && btn.className.includes('red')) {
            btn.scrollIntoView({ behavior: 'instant', block: 'center' });
            return new Promise((resolve) => {
              setTimeout(() => {
                btn.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mousemove', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, button: 0 }));
                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, button: 0 }));
                btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                resolve(true);
              }, 500);
            });
          }
        }
        return Promise.resolve(false);
      });
      
      if (result === true) {
        clicked = true;
        console.log('✅ 第 ' + (attempt + 1) + ' 次成功！');
        break;
      }
      await new Promise(r => setTimeout(r, 1000));
    }
    
    if (!clicked) {
      const publishBtn = await xhsPage.$('button.bg-red');
      if (publishBtn) {
        await publishBtn.scrollIntoView();
        await new Promise(r => setTimeout(r, 500));
        await publishBtn.click({ force: true });
        clicked = true;
      }
    }
    
    await new Promise(r => setTimeout(r, 5000));

    await xhsPage.screenshot({ path: '/tmp/xhs-upload-step.png', fullPage: true });
    console.log('📸 截图已保存');

    console.log('');
    console.log('✅ === 发布流程完成 ===');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    console.log('✅ 脚本结束');
  }
}

publishXiaohongshu().catch(console.error);