#!/usr/bin/env node
/**
 * AI Image Generator - 使用 MiniMax image-01 生成视频素材
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  apiKey: process.env.MINIMAX_IMAGE_API_KEY || 'sk-cp-1VnmtfYM3n73pKui2NG3-CtYaWV9F1pnC4y8FDAQjkjq6q5RMzVD-WWZ1RkqjvpU8AUCMdLjXI_hyGrjPaDTv6LQsGuz-73QhUM7PjIdfJwzLsv9Yh5LrW4',
  outputDir: path.join(__dirname, '../../../workspace/aicode/test-video/materials')
};

const log = (msg) => console.log('[' + new Date().toLocaleTimeString() + '] ' + msg);

const ensureDir = (dir) => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
};

// 生成单张图片
function generateImage(prompt, options = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: options.model || 'image-01',
      prompt: prompt,
      aspect_ratio: options.aspectRatio || '1:1',
      response_format: 'url',
      n: options.n || 1,
      prompt_optimizer: options.promptOptimizer !== false
    });

    const optionsReq = {
      hostname: 'api.minimaxi.com',
      path: '/v1/image_generation',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + CONFIG.apiKey,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = https.request(optionsReq, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.base_resp && result.base_resp.status_code === 0) {
            resolve({ success: true, urls: result.data.image_urls, taskId: result.id });
          } else {
            resolve({ success: false, error: result.base_resp?.status_msg || 'Unknown error' });
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 下载图片
function downloadImage(url, outputPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(outputPath);
    https.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        downloadImage(res.headers.location, outputPath).then(resolve).catch(reject);
        return;
      }
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(outputPath);
      });
    }).on('error', (err) => {
      fs.unlink(outputPath, () => {});
      reject(err);
    });
  });
}

// 生成单个场景素材
async function generateSceneMaterial(scene, index) {
  const outputFile = path.join(CONFIG.outputDir, `s${String(index).padStart(2, '0')}_material.png`);
  
  if (!scene.material || !scene.material.prompt) {
    log(`场景${index}: 无素材需求，跳过`);
    return { scene: index, skipped: true };
  }

  log(`场景${index}: 生成素材 "${scene.material.prompt.substring(0, 50)}..."`);
  
  try {
    const result = await generateImage(scene.material.prompt, {
      aspectRatio: scene.material.aspectRatio || '9:16'
    });

    if (result.success && result.urls && result.urls.length > 0) {
      await downloadImage(result.urls[0], outputFile);
      log(`  ✅ 已保存: ${outputFile}`);
      return { scene: index, success: true, path: outputFile };
    } else {
      log(`  ❌ 生成失败: ${result.error}`);
      return { scene: index, success: false, error: result.error };
    }
  } catch (e) {
    log(`  ❌ 错误: ${e.message}`);
    return { scene: index, success: false, error: e.message };
  }
}

// 批量生成
async function generateMaterials(scenes) {
  ensureDir(CONFIG.outputDir);
  log(`\n开始生成 ${scenes.length} 个场景的素材...`);
  log(`输出目录: ${CONFIG.outputDir}\n`);
  
  const results = [];
  
  for (let i = 0; i < scenes.length; i++) {
    const result = await generateSceneMaterial(scenes[i], i);
    results.push(result);
    
    // 间隔2秒避免限流
    if (i < scenes.length - 1) {
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  
  const success = results.filter(r => r.success && !r.skipped).length;
  const failed = results.filter(r => !r.success && !r.skipped).length;
  const skipped = results.filter(r => r.skipped).length;
  
  log(`\n✅ 素材生成完成: ${success}成功, ${failed}失败, ${skipped}跳过`);
  
  return results;
}

// 主入口
async function main() {
  const configFile = process.argv[2];
  
  if (!configFile) {
    console.error('用法: node image_gen.js <config.json>');
    console.error('示例: node image_gen.js scenes.json');
    process.exit(1);
  }
  
  log('读取配置: ' + configFile);
  const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
  const results = await generateMaterials(config.scenes);
  
  // 输出结果
  const outputFile = path.join(CONFIG.outputDir, 'generation_results.json');
  fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
  log(`结果已保存: ${outputFile}`);
  
  return results;
}

// 直接运行时执行
if (require.main === module) {
  main().catch(e => {
    console.error('Fatal error:', e);
    process.exit(1);
  });
}

module.exports = { generateMaterials, generateImage, downloadImage };
