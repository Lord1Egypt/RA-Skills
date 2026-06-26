#!/usr/bin/env node
/**
 * Video Producer - 短视频一键生成脚本 v2.2.0
 * 重构：调用video-director进行画面规划
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
  fps: 30,
  width: 1080,
  height: 1920,
  ttsApiKey: process.env.MINIMAX_API_KEY || 'sk-api-h-4sIEVwzDP2Rde_Tu87ptd48Zddl9zx77S6Jqrk1pytO7ZeYXnALDx67kwEsIEuxPnYei0YsYnK0JzvbszlQcdNBH1NhFQXp9fvAAUgr0rCwKYAq56EpIY',
  imageApiKey: process.env.MINIMAX_IMAGE_API_KEY || 'sk-cp-1VnmtfYM3n73pKui2NG3-CtYaWV9F1pnC4y8FDAQjkjq6q5RMzVD-WWZ1RkqjvpU8AUCMdLjXI_hyGrjPaDTv6LQsGuz-73QhUM7PjIdfJwzLsv9Yh5LrW4',
  ttsScript: path.join(__dirname, '../../minimax-tts-cn/scripts/tts.py'),
  directorScript: path.join(__dirname, '../../video-director/scripts/plan.js'),
  projectDir: path.join(__dirname, '../test-output'),
  materialsDir: '',
  audioDir: ''
};

CONFIG.materialsDir = path.join(CONFIG.projectDir, 'materials');
CONFIG.audioDir = path.join(CONFIG.projectDir, 'audio');

const log = (msg) => console.log('[' + new Date().toLocaleTimeString() + '] ' + msg);

const ensureDir = (dir) => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
};

// ========== AI 生图 ==========

function generateImage(prompt, options) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'image-01',
      prompt: prompt,
      aspect_ratio: options.aspectRatio || '9:16',
      response_format: 'url',
      n: 1,
      prompt_optimizer: true
    });

    const optionsReq = {
      hostname: 'api.minimaxi.com',
      path: '/v1/image_generation',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + CONFIG.imageApiKey,
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
            resolve({ success: true, urls: result.data.image_urls });
          } else {
            resolve({ success: false, error: result.base_resp.status_msg });
          }
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

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
      file.on('finish', () => { file.close(); resolve(outputPath); });
    }).on('error', (err) => { fs.unlink(outputPath, () => {}); reject(err); });
  });
}

// ========== TTS ==========

function generateTTS(text, outputFile) {
  return new Promise((resolve, reject) => {
    const cmd = 'MINIMAX_API_KEY=' + CONFIG.ttsApiKey + ' python3 "' + CONFIG.ttsScript + '" "' + text.replace(/"/g, '\\"') + '" --output "' + outputFile + '"';
    try {
      const result = execSync(cmd, { encoding: 'utf-8', timeout: 60000 });
      const match = result.match(/时长: ([\d.]+)秒/);
      const duration = match ? parseFloat(match[1]) : 3.0;
      resolve({ duration: duration, file: outputFile });
    } catch (e) {
      resolve({ duration: 3.0, file: outputFile });
    }
  });
}

// ========== Step 1: 分镜规划（调用video-director） ==========

function callDirector(topic, points, options = {}) {
  log('Step 1: 调用video-director生成分镜规划...');
  
  const inputFile = path.join(CONFIG.projectDir, 'input.json');
  const outputFile = path.join(CONFIG.projectDir, 'storyboard.json');
  
  ensureDir(CONFIG.projectDir);
  
  const inputData = { topic, points, ending: options.ending };
  fs.writeFileSync(inputFile, JSON.stringify(inputData, null, 2));
  
  try {
    const cmd = 'node "' + CONFIG.directorScript + '" "' + inputFile + '" -o "' + outputFile + '"';
    execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    
    if (fs.existsSync(outputFile)) {
      const storyboard = JSON.parse(fs.readFileSync(outputFile, 'utf-8'));
      log('分镜规划完成: ' + storyboard.scenes.length + ' 个场景，总时长: ' + storyboard.totalDuration + '秒');
      return storyboard;
    } else {
      throw new Error('分镜文件未生成');
    }
  } catch (error) {
    log('⚠️ video-director调用失败，使用内置规划: ' + error.message);
    const { planScenes } = require(CONFIG.directorScript);
    return planScenes(topic, points);
  }
}

// ========== 生成画面设计文档 ==========

function generateStoryboardMarkdown(topic, scenes, totalDuration) {
  let md = [];
  md.push('# 「' + topic + '」画面设计方案\n');
  md.push('**总时长：** ' + totalDuration + '秒\n');
  md.push('');
  md.push('| 场景 | 时间 | 类型 | 口播 | 素材 |');
  md.push('|:----:|------|------|------|------|');
  
  scenes.forEach(s => {
    const materials = s.visual.elements.filter(e => e.type === '素材' || e.type === '背景').map(e => e.desc || e.type).join(', ') || '-';
    md.push('| ' + s.id + ' | ' + s.timeStart + '-' + s.timeEnd + 's | ' + s.type + ' | ' + s.script.substring(0, 25) + '... | ' + materials + ' |');
  });
  
  md.push('');
  md.push('---');
  md.push('');
  
  scenes.forEach(s => {
    md.push('## 场景' + s.id + '：' + s.title);
    md.push('');
    md.push('**时间：** ' + s.timeStart + 's - ' + s.timeEnd + 's (' + s.duration + '秒)');
    md.push('');
    md.push('**口播：** ' + s.script);
    md.push('');
    md.push('### 画面设计');
    md.push('');
    md.push('```');
    
    s.visual.elements.forEach(e => {
      const endFrame = (e.delay || 0) + (e.duration || 20);
      if (e.type === '背景') {
        md.push('[背景] ' + e.desc + ' - ' + (e.anim || 'fadeIn') + ' ' + (e.delay || 0) + '-' + endFrame + '帧');
      } else if (e.type === '素材') {
        md.push('[素材] ' + e.desc + ' - ' + (e.anim || 'fadeIn') + ' ' + (e.delay || 0) + '-' + endFrame + '帧');
      } else if (e.type === 'emoji') {
        md.push('[Emoji] ' + e.value + ' - ' + (e.anim || 'popIn') + ' ' + (e.delay || 0) + '-' + endFrame + '帧');
      } else if (e.type === '文字') {
        md.push('[文字] "' + e.value + '" - ' + (e.anim || 'fadeSlideUp') + ' ' + (e.delay || 0) + '-' + endFrame + '帧');
      } else if (e.type === '描述') {
        md.push('[描述] "' + e.value + '" - ' + (e.anim || 'fadeSlideUp') + ' ' + (e.delay || 0) + '-' + endFrame + '帧');
      }
    });
    
    md.push('```');
    md.push('');
    md.push('### 素材清单');
    md.push('');
    
    const materialElements = s.visual.elements.filter(e => e.type === '素材' || e.type === '背景');
    if (materialElements.length > 0) {
      md.push('| 元素 | 类型 | Prompt | 尺寸 | 保存路径 |');
      md.push('|------|------|--------|------|----------|');
      materialElements.forEach(e => {
        const shortPrompt = e.prompt.length > 40 ? e.prompt.substring(0, 40) + '...' : e.prompt;
        md.push('| ' + e.desc + ' | ' + e.type + ' | ' + shortPrompt + ' | ' + (e.aspect || '1:1') + ' | ' + e.filename + ' |');
      });
    } else {
      md.push('无额外素材（纯文字场景）');
    }
    md.push('');
  });
  
  return md.join('\n');
}

// ========== Step 2: AI生图 ==========

async function generateMaterials(scenes) {
  log('Step 2: AI生成素材...');
  ensureDir(CONFIG.materialsDir);
  
  const results = [];
  
  for (const scene of scenes) {
    for (const element of scene.visual.elements) {
      if ((element.type === '素材' || element.type === '背景') && element.prompt) {
        const outputFile = path.join(CONFIG.materialsDir, element.filename);
        
        log('场景' + scene.id + ': 生成"' + element.desc + '"...');
        
        try {
          const result = await generateImage(element.prompt, { aspectRatio: element.aspect || '1:1' });
          if (result.success && result.urls && result.urls[0]) {
            await downloadImage(result.urls[0], outputFile);
            element.generatedPath = outputFile;
            log('  ✅ ' + element.filename);
            results.push({ scene: scene.id, element: element.desc, path: outputFile, success: true });
          } else {
            log('  ❌ ' + result.error);
            results.push({ scene: scene.id, element: element.desc, success: false, error: result.error });
          }
        } catch (e) {
          log('  ❌ ' + e.message);
          results.push({ scene: scene.id, element: element.desc, success: false, error: e.message });
        }
        
        await new Promise(r => setTimeout(r, 2000));
      }
    }
  }
  
  return results;
}

// ========== Step 3: TTS ==========

async function generateTTSForScenes(scenes) {
  log('Step 3: 生成TTS配音...');
  ensureDir(CONFIG.audioDir);
  
  const audioFiles = [];
  
  for (const scene of scenes) {
    const outputFile = path.join(CONFIG.audioDir, 's' + scene.id + '.mp3');
    log('场景' + scene.id + ': "' + scene.script.substring(0, 30) + '..."');
    
    let success = false;
    let retryCount = 0;
    
    while (!success && retryCount < 3) {
      try {
        if (fs.existsSync(outputFile)) fs.unlinkSync(outputFile);
        
        const result = await generateTTS(scene.script, outputFile);
        
        if (fs.existsSync(outputFile)) {
          const stats = fs.statSync(outputFile);
          if (stats.size > 1000) {
            scene.duration = result.duration;
            audioFiles.push({ id: scene.id, duration: result.duration, file: outputFile });
            log('  ⏱️ ' + result.duration + '秒 (' + stats.size + '字节)');
            success = true;
          } else {
            log('  ⚠️ 文件太小，重试...');
            retryCount++;
          }
        } else {
          log('  ⚠️ 文件未生成，重试...');
          retryCount++;
        }
      } catch (e) {
        log('  ⚠️ 错误: ' + e.message + '，重试...');
        retryCount++;
      }
      
      if (!success && retryCount < 3) await new Promise(r => setTimeout(r, 2000));
    }
    
    if (!success) {
      log('  ❌ 生成失败，使用默认时长');
      scene.duration = 3.0;
      audioFiles.push({ id: scene.id, duration: 3.0, file: outputFile });
    }
  }
  
  // 验证
  const missingFiles = audioFiles.filter(a => !fs.existsSync(a.file));
  if (missingFiles.length > 0) {
    log('⚠️ 警告: ' + missingFiles.length + ' 个音频文件缺失');
  }
  log('TTS配音完成: ' + audioFiles.length + ' 个文件');
  
  return audioFiles;
}

// ========== Step 4: 生成视频代码 ==========

function generateVideoCode(scenes, audioFiles) {
  log('Step 4: 生成视频代码...');
  
  let currentFrame = 0;
  const sceneFrames = [];
  
  for (const scene of scenes) {
    const audio = audioFiles.find(a => a.id === scene.id);
    const duration = audio ? audio.duration : scene.duration || 3.0;
    const frames = Math.ceil(duration * CONFIG.fps);
    sceneFrames.push({ ...scene, startFrame: currentFrame, duration: frames });
    currentFrame += frames;
  }
  
  const totalFrames = currentFrame;
  log('视频总时长: ' + (totalFrames / CONFIG.fps).toFixed(1) + '秒 (' + totalFrames + '帧)');
  
  // 收集所有导入 - 使用ASCII名称
  const imports = [];
  let imgIndex = 0;
  sceneFrames.forEach((s, si) => {
    s.visual.elements.forEach(e => {
      if ((e.type === '素材' || e.type === '背景') && e.generatedPath) {
        const importName = 'bgimg' + imgIndex;
        imports.push({ path: e.generatedPath, name: importName, sceneIndex: si, elementType: e.type });
        imgIndex++;
      }
    });
  });
  
  // 生成导入代码
  const importCode = imports.map(imp => "import " + imp.name + " from '" + imp.path.replace(/\\\\/g, '/') + "';").join('\n');
  
  // 生成场景代码
  const sceneCodeStr = sceneFrames.map((s, si) => {
    const titleColor = s.id === 0 ? "'#FFD700'" : "'white'";
    const titleSize = s.id === 0 ? '72' : '56';
    
    const bgElement = s.visual.elements.find(e => e.type === '背景' && e.generatedPath);
    const hasBg = !!bgElement;
    
    const materialElements = s.visual.elements.filter(e => e.type === '素材' && e.generatedPath);
    const featuredMaterial = materialElements.length > 0 ? materialElements[0] : null;
    
    const emojiEl = s.visual.elements.find(e => e.type === 'emoji');
    const emojiValue = emojiEl ? emojiEl.value : '📌';
    
    const textEl = s.visual.elements.find(e => e.type === '文字');
    const textValue = textEl ? textEl.value : s.title;
    
    const descEl = s.visual.elements.find(e => e.type === '描述');
    const descValue = descEl ? descEl.value : '';
    
    // 构建JSX
    let jsx = '';
    jsx += '    <>\n';
    
    if (hasBg) {
      const imgName = imports.find(i => i.sceneIndex === si && i.elementType === '背景')?.name || 'bg' + si;
      jsx += '      <img src={' + imgName + '} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: 0.3 }} />\n';
    }
    
    if (featuredMaterial) {
      const imgName = imports.find(i => i.sceneIndex === si && i.elementType === '素材')?.name || 'mat' + si;
      jsx += '      <img src={' + imgName + '} style={{ position: "absolute", width: 120, height: 120, objectFit: "contain", opacity: 0.85, right: 30, top: 80 }} />\n';
    }
    
    jsx += '      <AbsoluteFill style={{ width: "100%", height: "100%", backgroundColor: "#0a0a0a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: "Noto Color Emoji, sans-serif" }}>\n';
    jsx += '        <div style={{ opacity: iconAnim.opacity, transform: "scale(" + iconAnim.scale + ")", fontSize: 160, marginBottom: 40, zIndex: 1 }}>' + emojiValue + '</div>\n';
    jsx += '        <div style={{ opacity: titleAnim.opacity, transform: "translateY(" + titleAnim.translateY + "px)", fontSize: ' + titleSize + ", color: " + titleColor + ", fontWeight: '900', textAlign: 'center', padding: '0 60px', zIndex: 1 }}>" + textValue + '</div>\n';
    
    if (descValue) {
      jsx += "        <div style={{ opacity: descAnim.opacity, transform: 'translateY(' + descAnim.translateY + 'px)', fontSize: 36, color: '#9ca3af', marginTop: 30, textAlign: 'center', padding: '0 40px', zIndex: 1 }}>" + descValue + '</div>\n';
    }
    
    jsx += '      </AbsoluteFill>\n';
    jsx += '    </>\n';
    
    return "// Scene" + s.id + "\n" +
"const Scene" + s.id + " = () => {\n" +
"  const frame = useCurrentFrame();\n" +
"  const f = frame - " + s.startFrame + ";\n" +
"  const iconAnim = popIn(f, 0);\n" +
"  const titleAnim = fadeSlideUp(f, 25);\n" +
"  const descAnim = fadeSlideUp(f, 50);\n" +
"  return (\n" + jsx + "  );\n" +
"};\n";
  }).join('\n');
  
  // switch
  const switchCode = sceneFrames.map((s, i) => 
    i === 0 
      ? "if (frame < " + s.duration + ") return <Scene" + s.id + " />;"
      : "if (frame < " + (s.startFrame + s.duration) + ") return <Scene" + s.id + " />;"
  ).join('\n  ');
  
  const code = "import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';\n" +
"import React from 'react';\n" +
importCode + "\n\n" +
"const popIn = (frame, delay) => {\n" +
"  const progress = Math.max(0, Math.min(1, (frame - delay) / 15));\n" +
"  const scale = 0.5 + progress * 0.5;\n" +
"  return { scale, opacity: progress };\n" +
"};\n\n" +
"const fadeSlideUp = (frame, delay, duration) => {\n" +
"  const d = duration || 20;\n" +
"  const progress = Math.max(0, Math.min(1, (frame - delay) / d));\n" +
"  return { opacity: progress, translateY: interpolate(progress, [0, 1], [30, 0]) };\n" +
"};\n\n" +
sceneCodeStr + "\n\n" +
"export const Video = () => {\n" +
"  const frame = useCurrentFrame();\n" +
"  " + switchCode + "\n" +
"  return <Scene" + sceneFrames[sceneFrames.length - 1].id + " />;\n" +
"};\n";

  return { code, totalFrames };
}
// ========== Step 5: 渲染 ==========

async function renderVideo(code, totalFrames) {
  log('Step 5: 渲染视频...');
  
  const srcFile = path.join(CONFIG.projectDir, 'src/Video.js');
  const indexFile = path.join(CONFIG.projectDir, 'src/index.js');
  const outFile = path.join(CONFIG.projectDir, 'out/video-only.mp4');
  
  ensureDir(path.join(CONFIG.projectDir, 'src'));
  ensureDir(path.join(CONFIG.projectDir, 'out'));
  
  fs.writeFileSync(srcFile, code);
  log('Video.js 已保存');
  
  const indexCode = "import { registerRoot, Composition } from 'remotion';\n" +
"import React from 'react';\n" +
"import { Video } from './Video';\n\n" +
"const MyComp = () => (\n" +
"  <Composition\n" +
"    id='Video'\n" +
"    component={Video}\n" +
"    durationInFrames={" + totalFrames + "}\n" +
"    fps={30}\n" +
"    width={1080}\n" +
"    height={1920}\n" +
"  />\n" +
");\n\n" +
"registerRoot(MyComp);\n";
  
  fs.writeFileSync(indexFile, indexCode);
  log('index.js 已更新');
  
  const cmd = 'cd "' + CONFIG.projectDir + '" && npx remotion render src/index.js Video "' + outFile + '" 2>&1';
  log('开始渲染...');
  execSync(cmd, { stdio: 'inherit' });
  log('渲染完成');
  return outFile;
}

// ========== Step 6: 合并 ==========

async function mergeAudioVideo(videoFile, audioFiles) {
  log('Step 6: 合并音视频...');
  
  const concatFile = path.join(CONFIG.audioDir, 'all_audio.txt');
  const allAudioMp3 = path.join(CONFIG.audioDir, 'all_audio_new.mp3');
  const finalFile = path.join(CONFIG.projectDir, 'out/final.mp4');
  
  const list = audioFiles.map(a => "file '" + a.file + "'").join('\n');
  fs.writeFileSync(concatFile, list);
  
  execSync('cd "' + CONFIG.audioDir + '" && ffmpeg -y -f concat -safe 0 -i all_audio.txt -c copy "' + allAudioMp3 + '" 2>&1 | tail -3');
  
  const cmd = 'ffmpeg -y -i "' + videoFile + '" -i "' + allAudioMp3 + '" -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 -shortest "' + finalFile + '" 2>&1 | tail -5';
  execSync(cmd, { stdio: 'inherit' });
  
  log('✅ 完成！视频: ' + finalFile);
  return finalFile;
}

// ========== 主流程 ==========

async function main() {
  const topic = process.argv[2] || '知识短视频';
  const pointsJson = process.argv[3] || '[]';
  const endingJson = process.argv[4] || 'null';
  
  let points;
  let ending;
  try {
    points = JSON.parse(pointsJson);
  } catch {
    points = [
      { text: '知识要点一', emoji: '💡', title: '第一个要点', description: '详细说明' },
      { text: '知识要点二', emoji: '📚', title: '第二个要点', description: '详细说明' },
      { text: '知识要点三', emoji: '🎯', title: '第三个要点', description: '详细说明' }
    ];
  }
  try { ending = JSON.parse(endingJson); } catch { ending = null; }
  
  log('\n========== Video Producer v2.2.0 ==========');
  log('主题: ' + topic);
  log('要点数: ' + points.length + '\n');
  
  // Step 1: 调用video-director进行分镜规划
  const storyboard = callDirector(topic, points, { ending });
  const { scenes, totalDuration } = storyboard;
  
  // 生成画面设计文档
  const storyboardMd = generateStoryboardMarkdown(topic, scenes, totalDuration);
  const storyboardFile = path.join(CONFIG.projectDir, 'storyboard.md');
  fs.writeFileSync(storyboardFile, storyboardMd);
  log('画面设计方案已保存: ' + storyboardFile);
  console.log('\n' + storyboardMd + '\n');
  
  // Step 2: AI生图
  await generateMaterials(scenes);
  
  // Step 3: TTS
  const audioFiles = await generateTTSForScenes(scenes);
  
  // Step 4: 生成视频代码
  const { code, totalFrames } = generateVideoCode(scenes, audioFiles);
  
  // Step 5: 渲染
  const videoFile = await renderVideo(code, totalFrames);
  
  // Step 6: 合并
  const finalFile = await mergeAudioVideo(videoFile, audioFiles);
  
  log('\n========== 完成！==========');
  log('最终视频: ' + finalFile);
  log('总时长: ' + (totalFrames / 30).toFixed(1) + '秒');
  log('场景数: ' + scenes.length);
  log('画面设计: ' + storyboardFile);
  
  return { finalFile, scenes, audioFiles, totalFrames, storyboard };
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
