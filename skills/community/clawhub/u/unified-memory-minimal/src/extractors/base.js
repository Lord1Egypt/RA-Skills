/**
 * Base Extractor - 多模态提取器基类
 * 
 * 为不同类型的文件（PDF、图片、视频等）提供统一的内容提取接口
 * 
 * 功能：
 * - extract(file): 提取文件内容
 * - 支持多种文件格式
 * - 统一的输出格式
 */

import { log } from '../logger.js';
import { config } from '../config.js';
import { extname } from 'path';

// ─── 提取器状态 ───────────────────────────────────────────────────────────────
const ExtractorStatus = {
  READY: 'ready',
  EXTRACTING: 'extracting',
  ERROR: 'error',
  DISABLED: 'disabled',
};

// ─── 支持的文件类型 ───────────────────────────────────────────────────────────
const FILE_TYPES = {
  // 文档类型
  pdf: 'document',
  doc: 'document',
  docx: 'document',
  txt: 'text',
  md: 'text',
  
  // 图片类型
  jpg: 'image',
  jpeg: 'image',
  png: 'image',
  gif: 'image',
  webp: 'image',
  
  // 音频类型
  mp3: 'audio',
  wav: 'audio',
  m4a: 'audio',
  
  // 视频类型
  mp4: 'video',
  avi: 'video',
  mov: 'video',
  mkv: 'video',
};

// ─── BaseExtractor 基类 ────────────────────────────────────────────────────────

/**
 * 多模态提取器基类
 * 所有具体提取器应继承此类
 */
export class BaseExtractor {
  /**
   * @param {object} options
   * @param {string} options.name - 提取器名称
   * @param {string} options.type - 提取器类型（pdf, ocr, video 等）
   * @param {Array<string>} options.supportedFormats - 支持的文件格式
   */
  constructor(options = {}) {
    this.name = options.name || 'base-extractor';
    this.type = options.type || 'base';
    this.supportedFormats = options.supportedFormats || [];
    this.status = ExtractorStatus.READY;
    
    // 统计信息
    this.stats = {
      totalExtractions: 0,
      totalFiles: 0,
      totalErrors: 0,
      totalBytes: 0,
    };
  }
  
  /**
   * 检查是否支持指定文件格式
   * @param {string} filePath - 文件路径
   * @returns {boolean}
   */
  supports(filePath) {
    const ext = extname(filePath).slice(1).toLowerCase();
    return this.supportedFormats.includes(ext);
  }
  
  /**
   * 提取文件内容
   * @param {string} filePath - 文件路径
   * @param {object} [options] - 提取选项
   * @returns {Promise<{ content: string, metadata: object }>}
   */
  async extract(filePath, options = {}) {
    log('info', `[${this.name}] Extracting: ${filePath}`);
    
    const startTime = Date.now();
    this.status = ExtractorStatus.EXTRACTING;
    
    try {
      // 检查是否支持
      if (!this.supports(filePath)) {
        throw new Error(`Unsupported file format: ${filePath}`);
      }
      
      // 调用子类实现
      const result = await this._doExtract(filePath, options);
      
      // 更新统计
      this.stats.totalExtractions++;
      this.stats.totalFiles++;
      this.status = ExtractorStatus.READY;
      
      const duration = Date.now() - startTime;
      log('info', `[${this.name}] Extraction complete: ${duration}ms`);
      
      return {
        content: result.content || '',
        metadata: {
          source: filePath,
          extractor: this.name,
          extractorType: this.type,
          extractedAt: new Date().toISOString(),
          duration,
          ...result.metadata,
        },
      };
    } catch (e) {
      this.status = ExtractorStatus.ERROR;
      this.stats.totalErrors++;
      
      log('error', `[${this.name}] Extraction failed: ${e.message}`);
      
      throw e;
    }
  }
  
  /**
   * 实际提取逻辑（子类重写）
   */
  async _doExtract(filePath, options = {}) {
    throw new Error('Subclass must implement _doExtract()');
  }
  
  /**
   * 批量提取
   * @param {Array<string>} filePaths - 文件路径列表
   * @param {object} [options] - 提取选项
   * @returns {Promise<Array>}
   */
  async extractBatch(filePaths, options = {}) {
    const results = [];
    
    for (const filePath of filePaths) {
      try {
        const result = await this.extract(filePath, options);
        results.push(result);
      } catch (e) {
        results.push({
          error: e.message,
          source: filePath,
        });
      }
    }
    
    return results;
  }
  
  /**
   * 获取文件类型
   */
  getFileType(filePath) {
    const ext = extname(filePath).slice(1).toLowerCase();
    return FILE_TYPES[ext] || 'unknown';
  }
  
  /**
   * 获取提取器状态
   */
  getStatus() {
    return {
      name: this.name,
      type: this.type,
      status: this.status,
      supportedFormats: this.supportedFormats,
      stats: { ...this.stats },
    };
  }
  
  /**
   * 销毁提取器
   */
  async destroy() {
    this.status = ExtractorStatus.DISABLED;
    log('info', `[${this.name}] Extractor destroyed`);
  }
}

// ─── 文本提取器（简单实现）────────────────────────────────────────────────────

/**
 * 文本文件提取器
 */
export class TextExtractor extends BaseExtractor {
  constructor(options = {}) {
    super({
      name: 'text-extractor',
      type: 'text',
      supportedFormats: ['txt', 'md', 'markdown', 'json', 'yaml', 'yml', 'csv'],
      ...options,
    });
  }
  
  async _doExtract(filePath, options = {}) {
    const { readFile } = await import('fs/promises');
    const content = await readFile(filePath, 'utf-8');
    
    return {
      content,
      metadata: {
        fileType: this.getFileType(filePath),
        size: Buffer.byteLength(content, 'utf-8'),
      },
    };
  }
}

export default BaseExtractor;
