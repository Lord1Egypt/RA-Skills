/**
 * 封面图生成模块
 * 调用 wan2.6 生成微信公众号封面图
 */

import { spawnSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { loadOpenClawEnv, resolveDashScopeKey } from '../lib/openclaw_env.js';

const __coverDir = path.dirname(fileURLToPath(import.meta.url));
loadOpenClawEnv({ skillRoot: path.join(__coverDir, '..') });

/** 与 main.js 一致：$HOME/WorkBuddy/<技能文件夹名>（技能名 = 本仓库目录名） */
const SKILL_DIR_NAME = path.basename(path.resolve(__coverDir, '..', '..'));
const DEFAULT_WORKBUDDY_OUTPUT = path.join(
  process.env.HOME || process.env.USERPROFILE || '~',
  'WorkBuddy',
  SKILL_DIR_NAME
);

/**
 * 查找已有的封面图文件
 * @param {string} outputDir - 输出目录
 * @returns {string|null} 封面图路径，未找到返回 null
 */
function findExistingCover(outputDir) {
  const candidates = ['cover.jpg', 'cover.jpeg', 'cover.png', 'cover.webp'];
  
  for (const name of candidates) {
    const coverPath = path.join(outputDir, name);
    if (fs.existsSync(coverPath)) {
      return coverPath;
    }
    const inImages = path.join(outputDir, 'images', name);
    if (fs.existsSync(inImages)) {
      return inImages;
    }
  }
  return null;
}

/**
 * 生成微信公众号封面图
 * 生成失败时自动回退到上次已有的封面图
 * @param {Object} options - 选项
 * @param {string} options.title - 文章标题
 * @param {string} options.content - 内容摘要
 * @param {string} options.style - 风格描述
 * @param {string} options.outputDir - 输出目录
 * @returns {Promise<Object>} 生成结果
 */
export async function generateCover(options) {
  const defaultDir = DEFAULT_WORKBUDDY_OUTPUT;
  const { title, content = '', style = '', outputDir = defaultDir } = options;
  
  console.log('\n🎨 开始生成封面图...');
  console.log(`  标题：${title}`);
  console.log(`  内容：${content.substring(0, 50)}...`);
  console.log(`  风格：${style || '默认'}`);
  
  const dashKey = resolveDashScopeKey();
  if (!dashKey) {
    console.warn('  ⚠️  未配置 DashScope API Key，跳过生成');
    return fallbackToExisting(outputDir);
  }
  
  try {
    const result = await callWan26API(title, content, style, dashKey);
    
    if (result.success && result.images && result.images.length > 0) {
      const imageUrl = result.images[0].url;
      console.log('  ✅ 封面图生成成功');
      console.log(`  URL: ${imageUrl}`);
      
      const localPath = await downloadImage(imageUrl, path.join(outputDir, 'cover.jpg'));
      
      return {
        success: true,
        url: imageUrl,
        path: localPath
      };
    }
    
    console.warn('  ⚠️  封面生成未返回图片');
    return fallbackToExisting(outputDir);
  } catch (error) {
    console.warn(`  ⚠️  封面生成失败: ${error.message}`);
    return fallbackToExisting(outputDir);
  }
}

/**
 * 回退到已有的封面图
 */
function fallbackToExisting(outputDir) {
  const existing = findExistingCover(outputDir);
  if (existing) {
    console.log(`  📎 复用已有封面图: ${existing}`);
    return { success: true, path: existing, reused: true };
  }
  console.log('  ❌ 未找到可复用的封面图');
  return { success: false, error: '生成失败且无可复用的封面图' };
}

/**
 * 调用 wan2.6 API
 */
async function callWan26API(title, content, style, dashKey) {
  // 构建提示词
  const prompt = buildCoverPrompt(title, content, style);
  
  console.log('  📝 提示词:', prompt);
  
  // 使用 Python 脚本调用（复用 wan26-text-to-image 技能）
  // Python 脚本会自动从环境变量读取 DASHSCOPE_API_KEY
  try {
    const pythonScript = path.join(
      process.env.HOME,
      '.workbuddy/skills/wan26-text-to-image/wan26_generator.py'
    );

    if (!fs.existsSync(pythonScript)) {
      return { success: false, error: `未找到生成脚本: ${pythonScript}` };
    }

    // 优先使用当前环境 python3，避免硬编码路径导致失败
    const pyCandidates = ['python3', 'python'];
    let lastError = '';

    for (const pyCmd of pyCandidates) {
      const result = spawnSync(
        pyCmd,
        [
          pythonScript,
          '--json-only',
          'cover',
          '--title',
          title,
          '--content',
          content,
          '--style',
          style || ''
        ],
        {
          encoding: 'utf-8',
          timeout: 120000,
          env: {
            ...process.env,
            DASHSCOPE_API_KEY: dashKey
          }
        }
      );

      if (result.error) {
        lastError = `${pyCmd}: ${result.error.message}`;
        continue;
      }

      const output = `${result.stdout || ''}\n${result.stderr || ''}`.trim();
      if (output) {
        console.log(output);
      }

      if (result.status !== 0) {
        lastError = `${pyCmd} 退出码 ${result.status}`;
        continue;
      }

      const stdoutText = (result.stdout || '').trim();
      if (stdoutText) {
        try {
          return JSON.parse(stdoutText);
        } catch (e) {
          // fallback to regex parsing below
        }
      }

      const jsonMatch = output.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }

      lastError = `${pyCmd}: 无法解析输出`;
    }

    return { success: false, error: lastError || '调用 Python 失败' };
    
  } catch (error) {
    console.error('  Python 脚本调用失败:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 构建封面图提示词
 */
function buildCoverPrompt(title, content, style) {
  let prompt = `微信公众号文章封面图，标题：${title}`;
  
  if (content) {
    prompt += `\n内容关键词：${content}`;
  }
  
  if (style) {
    prompt += `\n风格要求：${style}`;
  }
  
  prompt += '\n要求：高清，专业，吸引眼球，适合做封面，无文字或少文字，16:9 比例';
  
  return prompt;
}

/**
 * 下载图片到本地
 */
async function downloadImage(url, filePath) {
  const https = (await import('https')).default;
  
  fs.mkdirSync(path.dirname(filePath), { recursive: true });

  return await new Promise((resolve, reject) => {
    https
      .get(url, response => {
        if (response.statusCode !== 200) {
          reject(new Error(`HTTP ${response.statusCode}`));
          return;
        }
        
        const file = fs.createWriteStream(filePath);
        response.pipe(file);
        
        file.on('finish', () => {
          file.close();
          resolve(filePath);
        });
      })
      .on('error', err => {
        fs.unlink(filePath, () => {});
        reject(err);
      });
  });
}

/**
 * 生成技术架构图
 */
export async function generateTechDiagram(options) {
  const defaultDir2 = DEFAULT_WORKBUDDY_OUTPUT;
  const { description, components = '', style = '', outputDir = defaultDir2 } = options;
  
  console.log('\n🎨 开始生成技术架构图...');
  console.log(`  描述：${description}`);
  
  // 类似封面图生成逻辑，调用 wan2.6
  // TODO: 实现技术架构图生成
  
  return {
    success: false,
    message: '技术架构图生成功能开发中...'
  };
}
