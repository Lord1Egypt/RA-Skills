#!/usr/bin/env node
/**
 * ocr_simple.js - 简化版OCR，不依赖sharp
 * 用法: node ocr_simple.js <image_url>
 */

const { HighPerformanceOCR } = require('./high_performance_ocr_simple');
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

async function runOCR(imageUrl, options = {}) {
  let ocr = null;
  
  try {
    console.error(`开始下载图片: ${imageUrl}`);
    const imageBuffer = await downloadImage(imageUrl);
    
    ocr = new HighPerformanceOCR({
      language: options.language || 'eng+chi_sim',
      verbose: options.verbose || false
    });
    
    console.error('开始OCR识别...');
    const result = await ocr.recognize(imageBuffer, options);
    
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
    error: '请提供图片URL',
    usage: 'node ocr_simple.js <image_url> [language]',
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