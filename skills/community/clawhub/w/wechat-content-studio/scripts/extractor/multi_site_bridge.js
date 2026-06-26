/**
 * multi-site-extractor 桥接层
 * 调用 Python 脚本并返回与旧 extract() 兼容的统一格式
 */

import { execSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __bridgeDir = path.dirname(fileURLToPath(import.meta.url));
const EXTRACT_SCRIPT = path.resolve(__bridgeDir, '../../../multi-site-extractor/scripts/extract.py');

/**
 * 抓取任意站点文章（微信/CSDN/博客园/掘金/知乎/简书/思否/少数派等）
 * @param {string} url - 文章 URL
 * @returns {Promise<Object>} 与旧 extract() 兼容的结果格式
 */
export async function extractArticle(url) {
  if (!fs.existsSync(EXTRACT_SCRIPT)) {
    console.error(`❌ multi-site-extractor 未安装: ${EXTRACT_SCRIPT}`);
    return { done: false, code: -1, msg: 'multi-site-extractor 未安装' };
  }

  try {
    const result = execSync(
      `python3 "${EXTRACT_SCRIPT}" "${url}" --json`,
      { encoding: 'utf-8', timeout: 60000, stdio: ['pipe', 'pipe', 'pipe'] }
    );

    const parsed = JSON.parse(result.trim());

    if (parsed.error) {
      return { done: false, code: -1, msg: parsed.error };
    }

    return {
      done: true,
      code: 0,
      data: {
        msg_title: parsed.title || '',
        msg_author: parsed.author || '',
        msg_content: parsed.markdown || '',
        msg_desc: parsed.digest || '',
        msg_cover: parsed.cover_image || '',
        msg_publish_time_str: parsed.publish_time || '',
        msg_source: parsed.source || '',
        msg_source_url: parsed.source_url || url,
        msg_tags: parsed.tags || [],
        msg_images: parsed.images || [],
        msg_word_count: parsed.word_count || 0,
        // 保留兼容字段
        account_name: parsed.author || '',
        content: parsed.markdown || '',
        markdown: parsed.markdown || '',
        title: parsed.title || '',
      }
    };
  } catch (error) {
    const stderr = error.stderr ? error.stderr.toString() : '';
    const stdout = error.stdout ? error.stdout.toString() : '';

    // 尝试从 stdout 解析 JSON（Python 脚本即使出错也会输出 JSON）
    if (stdout.trim()) {
      try {
        const parsed = JSON.parse(stdout.trim());
        if (parsed.error) {
          return { done: false, code: -1, msg: parsed.error };
        }
      } catch (_) {
        // ignore
      }
    }

    return {
      done: false,
      code: -1,
      msg: stderr || error.message || '抓取失败'
    };
  }
}

/**
 * 批量抓取多篇文章
 * @param {string[]} urls - URL 列表
 * @returns {Promise<Object[]>} 结果列表
 */
export async function extractArticles(urls) {
  const results = [];
  for (const url of urls) {
    const result = await extractArticle(url);
    results.push(result);
  }
  return results;
}
