#!/usr/bin/env node
/**
 * ocr.js - 使用 HighPerformanceOCR (Tesseract.js) 进行OCR识别
 * 用法: node ocr.js <image_url>
 * 输出: JSON 格式的识别结果
 */

const { HighPerformanceOCR } = require('./high_performance_ocr_simple');
const fetch = require('node-fetch');
const path = require('path');

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

async function runOCR(imageUrl, options = {}) {
  let ocr = null;
  
  try {
    // 下载图片
    console.error(`开始下载图片: ${imageUrl}`);
    const imageBuffer = await downloadImage(imageUrl);
    
    // 初始化OCR
    ocr = new HighPerformanceOCR({
      language: options.language || 'eng+chi_sim',
      verbose: options.verbose || false,
      enhance: true
    });
    
    // 执行OCR
    console.error('开始OCR识别...');
    const result = await ocr.recognize(imageBuffer, options);
    
    // 输出JSON结果
    const output = {
      text: result.text.trim(),
      confidence: result.confidence,
      processingTime: result.processingTime,
      wordCount: result.text.trim().length
    };
    
    console.log(JSON.stringify(output, null, 2));
    
  } catch (error) {
    const errorOutput = {
      error: error.message,
      text: '',
      confidence: 0,
      processingTime: 0,
      wordCount: 0
    };
    
    console.log(JSON.stringify(errorOutput, null, 2));
    process.exit(1);
    
  } finally {
    if (ocr) {
      await ocr.terminate();
    }
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log(JSON.stringify({
    error: '请提供图片URL作为参数',
    usage: 'node ocr.js <image_url> [language]',
    example: 'node ocr.js https://example.com/image.jpg chi_sim',
    text: '',
    confidence: 0,
    processingTime: 0,
    wordCount: 0
  }, null, 2));
  process.exit(1);
}

const imageUrl = args[0];
const language = args[1] || 'eng+chi_sim';

runOCR(imageUrl, { language, verbose: true }).catch(error => {
  console.error('程序执行失败:', error.message);
  process.exit(1);
});