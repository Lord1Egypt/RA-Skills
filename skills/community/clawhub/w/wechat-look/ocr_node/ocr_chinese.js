#!/usr/bin/env node
/**
 * ocr_chinese.js - 支持中英文OCR识别
 */

const Tesseract = require('tesseract.js');
const fetch = require('node-fetch');

async function downloadImage(imageUrl) {
  try {
    const response = await fetch(imageUrl, {
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; wechat-look-ocr/1.0)'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.buffer();
  } catch (error) {
    throw new Error(`下载图片失败: ${error.message}`);
  }
}

async function runOCR(imageUrl) {
  const startTime = Date.now();
  
  try {
    console.error(`开始处理: ${imageUrl}`);
    
    // 下载图片
    const imageBuffer = await downloadImage(imageUrl);
    
    console.error('开始OCR识别...');
    
    // 尝试使用中英文混合识别
    try {
      // 首先尝试中英文混合
      const result = await Tesseract.recognize(imageBuffer, 'eng+chi_sim', {
        logger: m => console.error(m.status)
      });
      
      const processingTime = Date.now() - startTime;
      
      const output = {
        text: result.data.text.trim(),
        confidence: result.data.confidence,
        wordCount: result.data.text.trim().length,
        processingTime: processingTime,
        language: 'eng+chi_sim'
      };
      
      console.log(JSON.stringify(output, null, 2));
      
    } catch (chineseError) {
      console.error('中英文混合识别失败，尝试仅英文:', chineseError.message);
      
      // 如果中英文失败，回退到仅英文
      const result = await Tesseract.recognize(imageBuffer, 'eng');
      
      const processingTime = Date.now() - startTime;
      
      const output = {
        text: result.data.text.trim(),
        confidence: result.data.confidence,
        wordCount: result.data.text.trim().length,
        processingTime: processingTime,
        language: 'eng',
        fallback: true
      };
      
      console.log(JSON.stringify(output, null, 2));
    }
    
  } catch (error) {
    const errorOutput = {
      error: error.message,
      text: '',
      confidence: 0,
      wordCount: 0,
      processingTime: Date.now() - startTime
    };
    
    console.log(JSON.stringify(errorOutput, null, 2));
    process.exit(1);
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log(JSON.stringify({
    error: '请提供图片URL',
    usage: 'node ocr_chinese.js <image_url>',
    text: '',
    confidence: 0,
    wordCount: 0,
    processingTime: 0
  }, null, 2));
  process.exit(1);
}

runOCR(args[0]).catch(error => {
  console.error('程序执行失败:', error.message);
  process.exit(1);
});