// HTML 转 PDF 脚本
// 使用 Playwright 将 HTML 文件转换为 PDF

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function htmlToPdf(inputHtml, outputPdf) {
  // 验证输入文件
  if (!fs.existsSync(inputHtml)) {
    console.error(`❌ 文件不存在：${inputHtml}`);
    process.exit(1);
  }

  // 生成输出路径
  if (!outputPdf) {
    outputPdf = inputHtml.replace('.html', '.pdf');
  }

  console.log(`📄 转换 HTML → PDF`);
  console.log(`   输入：${inputHtml}`);
  console.log(`   输出：${outputPdf}`);

  let browser;
  try {
    // 启动浏览器
    console.log(`🚀 启动浏览器...`);
    browser = await chromium.launch({
      headless: true,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
      ]
    });

    // 创建页面
    const page = await browser.newPage();

    // 打开 HTML 文件（使用绝对路径）
    const absolutePath = path.resolve(inputHtml);
    const fileUrl = `file://${absolutePath}`;
    console.log(`📂 打开文件：${fileUrl}`);
    
    await page.goto(fileUrl, {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // 转 PDF
    console.log(`📝 生成 PDF...`);
    await page.pdf({
      path: outputPdf,
      format: 'A4',
      printBackground: true,
      margin: {
        top: '10mm',
        bottom: '10mm',
        left: '10mm',
        right: '10mm'
      }
    });

    console.log(`✅ PDF 已生成：${outputPdf}`);
    
    // 返回 PDF 路径
    console.log(`MEDIA: ${path.resolve(outputPdf)}`);
    
  } catch (error) {
    console.error(`❌ 错误：${error.message}`);
    process.exit(1);
  } finally {
    // 关闭浏览器
    if (browser) {
      await browser.close();
      console.log(`🔒 浏览器已关闭`);
    }
  }
}

// 命令行参数
const args = process.argv.slice(2);
const inputHtml = args[0];
const outputPdf = args[1];

if (!inputHtml) {
  console.error('用法：node html-to-pdf.js <input.html> [output.pdf]');
  process.exit(1);
}

htmlToPdf(inputHtml, outputPdf);
