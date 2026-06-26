/**
 * 头条号封面上传脚本
 * 用法：node upload-cover.js <coverImagePath>
 * 示例：node upload-cover.js ./cover.jpg
 */

const puppeteer = require('puppeteer-core');
const path = require('path');

const COVER_PATH = process.argv[2] || path.resolve(__dirname, '../assets/cover.jpg');

(async () => {
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:28800',
      defaultViewport: null
    });

    // 获取头条页面
    const pages = await browser.pages();
    let page = pages.find(p => p.url().includes('mp.toutiao.com'));

    if (!page) {
      const targets = await browser.targets();
      const target = targets.find(t => t.url().includes('mp.toutiao.com'));
      if (target) {
        page = await target.page();
      }
    }

    if (!page) {
      console.error('ERROR: 头条页面未找到，请先打开发布页');
      process.exit(1);
    }

    console.log('Page URL:', page.url());

    // 检查封面文件是否存在
    const fs = require('fs');
    if (!fs.existsSync(COVER_PATH)) {
      console.error('ERROR: 封面文件不存在:', COVER_PATH);
      process.exit(1);
    }

    console.log('封面路径:', COVER_PATH);
    const stats = fs.statSync(COVER_PATH);
    console.log('文件大小:', stats.size, 'bytes');

    // 上传封面
    const fileInputs = await page.$$('input[type="file"]');
    console.log('找到 file input 数量:', fileInputs.length);

    if (fileInputs.length === 0) {
      console.error('ERROR: 未找到 file input，请先点击上传区域');
      process.exit(1);
    }

    await fileInputs[0].uploadFile(COVER_PATH);
    console.log('上传完成');

    // 等待上传处理
    await new Promise(r => setTimeout(r, 5000));

    // 点击确定按钮
    const confirmResult = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const confirmBtn = btns.find(b => b.textContent?.trim() === '确定');
      if (confirmBtn) {
        confirmBtn.click();
        confirmBtn.dispatchEvent(new Event('click', { bubbles: true }));
        return 'clicked confirm';
      }
      return 'no confirm button';
    });
    console.log('确认:', confirmResult);

    await new Promise(r => setTimeout(r, 2000));
    console.log('封面上传完成！');
    process.exit(0);

  } catch (error) {
    console.error('ERROR:', error.message);
    process.exit(1);
  }
})();
