/**
 * Extractors - 多模态提取器模块入口
 * 
 * 提供不同类型文件内容提取器的统一导出和管理
 * 
 * 支持的提取器（未来扩展）：
 * - PDFExtractor: PDF 文档提取
 * - OCRExtractor: 图片 OCR 提取
 * - VideoExtractor: 视频帧提取 + OCR
 * - AudioExtractor: 音频转文字（Whisper）
 */

import { BaseExtractor, TextExtractor } from './base.js';

// ─── 提取器注册表 ───────────────────────────────────────────────────────────────
const extractorRegistry = new Map();

/**
 * 注册提取器
 */
export function registerExtractor(name, ExtractorClass) {
  extractorRegistry.set(name, ExtractorClass);
}

/**
 * 创建提取器实例
 */
export function createExtractor(name, options = {}) {
  const ExtractorClass = extractorRegistry.get(name);
  
  if (!ExtractorClass) {
    throw new Error(`Unknown extractor: ${name}`);
  }
  
  return new ExtractorClass(options);
}

/**
 * 获取适合文件的提取器
 */
export function getExtractorForFile(filePath, options = {}) {
  for (const [name, ExtractorClass] of extractorRegistry) {
    const extractor = new ExtractorClass(options);
    if (extractor.supports(filePath)) {
      return extractor;
    }
  }
  
  return null;
}

/**
 * 自动提取文件内容
 */
export async function autoExtract(filePath, options = {}) {
  const extractor = getExtractorForFile(filePath, options);
  
  if (!extractor) {
    throw new Error(`No extractor found for file: ${filePath}`);
  }
  
  return extractor.extract(filePath, options);
}

/**
 * 获取所有已注册的提取器
 */
export function listExtractors() {
  return [...extractorRegistry.keys()];
}

// ─── 注册默认提取器 ───────────────────────────────────────────────────────────
registerExtractor('text', TextExtractor);

// ─── 导出 ────────────────────────────────────────────────────────────────────

export { BaseExtractor, TextExtractor } from './base.js';

export default {
  BaseExtractor,
  TextExtractor,
  registerExtractor,
  createExtractor,
  getExtractorForFile,
  autoExtract,
  listExtractors,
};
