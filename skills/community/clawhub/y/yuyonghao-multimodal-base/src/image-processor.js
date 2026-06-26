/**
 * Multimodal Base - 图像理解模块
 * 支持图像描述、OCR、图表分析
 */

import fs from 'fs/promises';
import path from 'path';
import { EventEmitter } from 'events';
import axios from 'axios';

/**
 * 图像处理器类
 */
export class ImageProcessor extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.openaiApiKey - OpenAI API Key
   * @param {string} config.model - 视觉模型（默认：gpt-4o）
   */
  constructor(config = {}) {
    super();
    this.apiKey = config.openaiApiKey || process.env.OPENAI_API_KEY;
    this.model = config.model || 'gpt-4o';
    this.baseURL = config.baseURL || 'https://api.openai.com/v1';
  }

  /**
   * 将图像编码为 Base64
   * @param {string} imagePath - 图像路径
   * @returns {Promise<string>} - Base64 编码
   */
  async encodeImage(imagePath) {
    const imageBuffer = await fs.readFile(imagePath);
    return imageBuffer.toString('base64');
  }

  /**
   * 理解图像内容（使用 GPT-4V）
   * @param {string} imagePath - 图像路径
   * @param {string} prompt - 提示词
   * @returns {Promise<Object>} - 理解结果
   */
  async understand(imagePath, prompt = '描述这张图片的内容') {
    this.emit('processing', { type: 'understand', path: imagePath });

    try {
      // 编码图像
      const base64Image = await this.encodeImage(imagePath);
      const mimeType = this.getMimeType(imagePath);

      // 调用 GPT-4V
      const response = await axios.post(
        `${this.baseURL}/chat/completions`,
        {
          model: this.model,
          messages: [
            {
              role: 'user',
              content: [
                { type: 'text', text: prompt },
                {
                  type: 'image_url',
                  image_url: {
                    url: `data:${mimeType};base64,${base64Image}`
                  }
                }
              ]
            }
          ],
          max_tokens: 1000
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          timeout: 30000
        }
      );

      const result = {
        description: response.data.choices[0].message.content,
        model: this.model,
        tokens: response.data.usage?.total_tokens || 0,
        path: imagePath
      };

      this.emit('completed', { type: 'understand', result });
      return result;

    } catch (error) {
      this.emit('error', { type: 'understand', error });
      throw new Error(`Image understanding failed: ${error.message}`);
    }
  }

  /**
   * OCR 文字提取（使用 Tesseract.js）
   * @param {string} imagePath - 图像路径
   * @param {string} lang - 语言（默认：chi_sim+eng）
   * @returns {Promise<Object>} - OCR 结果
   */
  async ocr(imagePath, lang = 'chi_sim+eng') {
    this.emit('processing', { type: 'ocr', path: imagePath });

    try {
      // 动态导入 Tesseract（避免启动时加载）
      const { createWorker } = await import('tesseract.js');
      
      const worker = await createWorker(lang);
      const result = await worker.recognize(imagePath);
      await worker.terminate();

      const ocrResult = {
        text: result.data.text,
        confidence: result.data.confidence,
        words: result.data.words,
        path: imagePath
      };

      this.emit('completed', { type: 'ocr', result: ocrResult });
      return ocrResult;

    } catch (error) {
      this.emit('error', { type: 'ocr', error });
      throw new Error(`OCR failed: ${error.message}`);
    }
  }

  /**
   * 分析图表/表格
   * @param {string} imagePath - 图像路径
   * @returns {Promise<Object>} - 分析结果
   */
  async analyzeChart(imagePath) {
    const prompt = `分析这张图表：
1. 图表类型（柱状图、折线图、饼图、表格等）
2. 主要数据趋势
3. 关键数据点
4. 结论和洞察`;

    return await this.understand(imagePath, prompt);
  }

  /**
   * 批量处理图像
   * @param {Array<string>} imagePaths - 图像路径数组
   * @param {Function} processor - 处理函数
   * @returns {Promise<Array>} - 结果数组
   */
  async batchProcess(imagePaths, processor = this.understand.bind(this)) {
    const results = [];
    
    for (const path of imagePaths) {
      try {
        const result = await processor(path);
        results.push({ path, success: true, result });
      } catch (error) {
        results.push({ path, success: false, error: error.message });
      }
    }

    return results;
  }

  /**
   * 获取 MIME 类型
   */
  getMimeType(imagePath) {
    const ext = path.extname(imagePath).toLowerCase();
    const mimeTypes = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.webp': 'image/webp',
      '.bmp': 'image/bmp'
    };
    return mimeTypes[ext] || 'image/jpeg';
  }

  /**
   * 验证图像文件
   */
  async validateImage(imagePath) {
    try {
      const stats = await fs.stat(imagePath);
      if (!stats.isFile()) {
        throw new Error('Path is not a file');
      }
      
      const ext = path.extname(imagePath).toLowerCase();
      const validExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
      if (!validExts.includes(ext)) {
        throw new Error(`Invalid image format: ${ext}`);
      }

      // 检查文件大小（最大 20MB）
      if (stats.size > 20 * 1024 * 1024) {
        throw new Error('Image too large (max 20MB)');
      }

      return true;
    } catch (error) {
      throw new Error(`Image validation failed: ${error.message}`);
    }
  }
}

export default ImageProcessor;
