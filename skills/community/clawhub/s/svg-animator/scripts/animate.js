#!/usr/bin/env node

/**
 * SVG Animator - Generate animated videos from SVG frames
 * 
 * Usage:
 *   node animate.js --theme "description" --frames N --output /path/to/output.mp4
 *   node animate.js --story "story description" --scenes N --output /path/to/output.mp4
 * 
 * Examples:
 *   node animate.js --theme "running dog" --frames 24 --output /tmp/dog.mp4
 *   node animate.js --theme "flying bird" --duration 3 --output /tmp/bird.mp4
 *   node animate.js --story "a day of a cat" --scenes 4 --output /tmp/cat_story.mp4
 */

const fs = require('fs');
const { execSync } = require('child_process');

// 解析参数
const args = process.argv.slice(2);
let theme = '';
let story = '';
let frames = 24;
let duration = 2;
let scenes = 1;
let output = '/tmp/animation.mp4';
let fps = 12;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--theme' || args[i] === '-t') theme = args[++i];
  else if (args[i] === '--story' || args[i] === '-s') story = args[++i];
  else if (args[i] === '--frames' || args[i] === '-f') frames = parseInt(args[++i]);
  else if (args[i] === '--duration' || args[i] === '-d') duration = parseFloat(args[++i]);
  else if (args[i] === '--scenes' || args[i] === '-c') scenes = parseInt(args[++i]);
  else if (args[i] === '--output' || args[i] === '-o') output = args[++i];
  else if (args[i] === '--fps') fps = parseInt(args[++i]);
}

const size = 400;

// 根据主题生成动画的函数
function generateAnimationFrame(i, totalFrames, theme) {
  const t = (i / totalFrames) * Math.PI * 2;
  const progress = i / totalFrames;
  
  // 默认生成一个奔跑的小狗
  const legOffset = Math.sin(t) * 40;
  const tailAngle = Math.sin(t * 2) * 25;
  const bodyBob = Math.sin(t) * 5;
  const bodyY = 240 + bodyBob;
  
  // 通用运动参数
  const params = {
    t, progress,
    legOffset, tailAngle, bodyBob, bodyY,
    wingUp: Math.sin(t) * -45,
    jumpHeight: -Math.abs(Math.sin(t)) * 80,
    rotation: Math.sin(t) * 15,
    wave: Math.sin(t * 3) * 5
  };
  
  // 主题检测并生成对应 SVG
  let svg;
  const lowerTheme = theme.toLowerCase();
  
  if (lowerTheme.includes('dog') || lowerTheme.includes('狗')) {
    svg = generateDogFrame(params, size);
  } else if (lowerTheme.includes('cat') || lowerTheme.includes('猫')) {
    svg = generateCatFrame(params, size);
  } else if (lowerTheme.includes('bird') || lowerTheme.includes('鸟')) {
    svg = generateBirdFrame(params, size);
  } else if (lowerTheme.includes('fish') || lowerTheme.includes('鱼')) {
    svg = generateFishFrame(params, size);
  } else if (lowerTheme.includes('sun') || lowerTheme.includes('日出') || lowerTheme.includes('日落')) {
    svg = generateSunFrame(params, size);
  } else if (lowerTheme.includes('rain') || lowerTheme.includes('雨')) {
    svg = generateRainFrame(params, size);
  } else if (lowerTheme.includes('cloud') || lowerTheme.includes('云')) {
    svg = generateCloudFrame(params, size);
  } else {
    // 默认小狗奔跑
    svg = generateDogFrame(params, size);
  }
  
  return svg;
}

// 各种动物的帧生成函数
function generateDogFrame(p, size) {
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#87CEEB'/>
  <rect x='0' y='${size*0.88}' width='${size}' height='${size*0.12}' fill='#90EE90'/>
  <ellipse cx='${200 + p.legOffset * 0.3}' cy='${p.bodyY}' rx='90' ry='45' fill='#D2691E' stroke='#8B4513' stroke-width='3'/>
  <ellipse cx='${90 + p.legOffset * 0.2}' cy='${p.bodyY - 60}' rx='45' ry='40' fill='#D2691E' stroke='#8B4513' stroke-width='3'/>
  <ellipse cx='${50 + p.legOffset * 0.3}' cy='${p.bodyY - 95}' rx='15' ry='25' fill='#8B4513'/>
  <ellipse cx='${115 + p.legOffset * 0.2}' cy='${p.bodyY - 90}' rx='13' ry='22' fill='#8B4513'/>
  <ellipse cx='${75 + p.legOffset * 0.2}' cy='${p.bodyY - 68}' rx='10' ry='10' fill='white' stroke='black' stroke-width='2'/>
  <ellipse cx='${105 + p.legOffset * 0.2}' cy='${p.bodyY - 68}' rx='10' ry='10' fill='white' stroke='black' stroke-width='2'/>
  <ellipse cx='${78 + p.legOffset * 0.2}' cy='${p.bodyY - 66}' rx='4' ry='4' fill='black'/>
  <ellipse cx='${108 + p.legOffset * 0.2}' cy='${p.bodyY - 66}' rx='4' ry='4' fill='black'/>
  <ellipse cx='${50 + p.legOffset * 0.2}' cy='${p.bodyY - 50}' rx='7' ry='5' fill='black'/>
  <ellipse cx='${120 + p.legOffset * 0.3}' cy='${p.bodyY + 50}' rx='15' ry='30' fill='#D2691E' stroke='#8B4513' stroke-width='2' transform='rotate(${p.legOffset} 120 ${p.bodyY + 50})'/>
  <ellipse cx='${140 - p.legOffset * 0.3}' cy='${p.bodyY + 45}' rx='15' ry='30' fill='#D2691E' stroke='#8B4513' stroke-width='2' transform='rotate(${-p.legOffset} 140 ${p.bodyY + 45})'/>
  <ellipse cx='${260 - p.legOffset * 0.5}' cy='${p.bodyY + 45}' rx='18' ry='35' fill='#D2691E' stroke='#8B4513' stroke-width='2' transform='rotate(${-p.legOffset * 1.2} 260 ${p.bodyY + 45})'/>
  <ellipse cx='${280 + p.legOffset * 0.5}' cy='${p.bodyY + 40}' rx='18' ry='35' fill='#D2691E' stroke='#8B4513' stroke-width='2' transform='rotate(${p.legOffset * 1.2} 280 ${p.bodyY + 40})'/>
  <path d='M 280 ${p.bodyY - 20} Q ${310 + p.tailAngle} ${p.bodyY - 60} ${330 + p.tailAngle * 1.5} ${p.bodyY - 90}' stroke='#8B4513' stroke-width='10' fill='none' stroke-linecap='round'/>
</svg>`;
}

function generateCatFrame(p, size) {
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#E6E6FA'/>
  <rect x='0' y='${size*0.85}' width='${size}' height='${size*0.15}' fill='#DDA0DD'/>
  <ellipse cx='200' cy='${250 + p.bodyBob}' rx='80' ry='50' fill='#FFB347' stroke='#FF8C00' stroke-width='3'/>
  <ellipse cx='200' cy='${160 + p.bodyBob}' rx='55' ry='45' fill='#FFB347' stroke='#FF8C00' stroke-width='3'/>
  <polygon points='150,130 140,70 180,110' fill='#FF8C00'/>
  <polygon points='250,130 260,70 220,110' fill='#FF8C00'/>
  <ellipse cx='180' cy='${150 + p.bodyBob}' rx='12' ry='15' fill='#90EE90' stroke='black' stroke-width='1.5'/>
  <ellipse cx='220' cy='${150 + p.bodyBob}' rx='12' ry='15' fill='#90EE90' stroke='black' stroke-width='1.5'/>
  <ellipse cx='180' cy='${150 + p.bodyBob}' rx='3' ry='9' fill='black'/>
  <ellipse cx='220' cy='${150 + p.bodyBob}' rx='3' ry='9' fill='black'/>
  <ellipse cx='200' cy='${175 + p.bodyBob}' rx='8' ry='5' fill='#FF69B4'/>
  <line x1='140' y1='170' x2='180' y2='175' stroke='#666' stroke-width='1.5'/>
  <line x1='140' y1='180' x2='180' y2='180' stroke='#666' stroke-width='1.5'/>
  <line x1='220' y1='175' x2='260' y2='170' stroke='#666' stroke-width='1.5'/>
  <line x1='220' y1='180' x2='260' y2='180' stroke='#666' stroke-width='1.5'/>
  <ellipse cx='160' cy='${300 + p.bodyBob}' rx='18' ry='25' fill='#FFB347' stroke='#FF8C00' stroke-width='2'/>
  <ellipse cx='240' cy='${300 + p.bodyBob}' rx='18' ry='25' fill='#FFB347' stroke='#FF8C00' stroke-width='2'/>
  <path d='M 280 ${250 + p.bodyBob} Q 320 ${200 + p.bodyBob} 300 ${150 + p.bodyBob}' stroke='#FFB347' stroke-width='15' fill='none' stroke-linecap='round'/>
</svg>`;
}

function generateBirdFrame(p, size) {
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#87CEEB'/>
  <ellipse cx='200' cy='${280 - p.progress * 50}' rx='100' ry='30' fill='#90EE90'/>
  <ellipse cx='200' cy='${200 + p.bodyBob * 2}' rx='25' ry='20' fill='#FFD700'/>
  <ellipse cx='230' cy='${185 + p.bodyBob * 2}' rx='30' ry='8' fill='#FFD700' transform='rotate(${p.wingUp} 230 185)'/>
  <ellipse cx='170' cy='${185 + p.bodyBob * 2}' rx='30' ry='8' fill='#FFD700' transform='rotate(${-p.wingUp} 170 185)'/>
  <circle cx='210' cy='${195 + p.bodyBob * 2}' r='3' fill='black'/>
  <polygon points='225,200 235,205 225,210' fill='orange'/>
  <ellipse cx='200' cy='${230 + p.bodyBob * 2}' rx='15' ry='8' fill='#FF6B6B'/>
  <path d='M 170 ${195 + p.bodyBob * 2} Q 150 ${170 + p.bodyBob * 2} 140 ${190 + p.bodyBob * 2}' stroke='#333' stroke-width='2' fill='none'/>
  <path d='M 230 ${195 + p.bodyBob * 2} Q 250 ${170 + p.bodyBob * 2} 260 ${190 + p.bodyBob * 2}' stroke='#333' stroke-width='2' fill='none'/>
</svg>`;
}

function generateFishFrame(p, size) {
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#4169E1'/>
  <rect x='0' y='${size*0.7}' width='${size}' height='${size*0.3}' fill='#228B22'/>
  <ellipse cx='${200 + p.legOffset}' cy='200' rx='60' ry='25' fill='#FF8C00'/>
  <polygon points='${140 + p.legOffset},200 ${100 + p.legOffset},170 ${100 + p.legOffset},230' fill='#FF8C00'/>
  <circle cx='${230 + p.legOffset}' cy='190' r='5' fill='black'/>
  <ellipse cx='${235 + p.legOffset}' cy='188' rx='2' ry='2' fill='white'/>
  <path d='M ${260 + p.legOffset + p.tailAngle} 200 Q ${300 + p.legOffset} ${180 + p.tailAngle} ${320 + p.legOffset} 200 Q ${300 + p.legOffset} ${220 + p.tailAngle} ${260 + p.legOffset + p.tailAngle} 200' fill='#FF8C00'/>
  <ellipse cx='${180 + p.legOffset}' cy='185' rx='3' ry='3' fill='#333' opacity='0.3'/>
  <ellipse cx='${220 + p.legOffset}' cy='215' rx='3' ry='3' fill='#333' opacity='0.3'/>
  <ellipse cx='${160 + p.legOffset}' cy='210' rx='2' ry='2' fill='#333' opacity='0.3'/>
</svg>`;
}

function generateSunFrame(p, size) {
  const r = Math.floor(255);
  const g = Math.floor(100 + p.progress * 155);
  const b = Math.floor(100);
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='rgb(${r},${g},${b})'/>
  <ellipse cx='${size*0.5}' cy='${size * (0.9 - p.progress * 0.6)}' rx='60' ry='60' fill='#FFD700'/>
  <ellipse cx='${size*0.5}' cy='${size * (0.9 - p.progress * 0.6)}' rx='50' ry='50' fill='#FFFF00'/>
  <line x1='${size*0.5}' y1='${size * (0.9 - p.progress * 0.6) - 70}' x2='${size*0.5}' y2='${size * (0.9 - p.progress * 0.6) - 100}' stroke='#FFD700' stroke-width='4'/>
  <line x1='${size*0.5}' y1='${size * (0.9 - p.progress * 0.6) + 70}' x2='${size*0.5}' y2='${size * (0.9 - p.progress * 0.6) + 100}' stroke='#FFD700' stroke-width='4'/>
  <line x1='${size*0.5 - 70}' y1='${size * (0.9 - p.progress * 0.6)}' x2='${size*0.5 - 100}' y2='${size * (0.9 - p.progress * 0.6)}' stroke='#FFD700' stroke-width='4'/>
  <line x1='${size*0.5 + 70}' y1='${size * (0.9 - p.progress * 0.6)}' x2='${size*0.5 + 100}' y2='${size * (0.9 - p.progress * 0.6)}' stroke='#FFD700' stroke-width='4'/>
  <ellipse cx='${size*0.5}' cy='${size*0.95}' rx='${size*0.6}' ry='${size*0.1}' fill='#228B22'/>
</svg>`;
}

function generateRainFrame(p, size) {
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#4a4a6a'/>
  <ellipse cx='100' cy='${size*0.3}' rx='60' ry='30' fill='#666' opacity='0.7'/>
  <ellipse cx='300' cy='${size*0.25}' rx='70' ry='35' fill='#666' opacity='0.6'/>
  <line x1='50' y1='${(p.progress * size * 0.5) % size}' x2='45' y2='${(p.progress * size * 0.5 + 20) % size}' stroke='#87CEEB' stroke-width='2'/>
  <line x1='150' y1='${(p.progress * size * 0.7 + 100) % size}' x2='145' y2='${(p.progress * size * 0.7 + 120) % size}' stroke='#87CEEB' stroke-width='2'/>
  <line x1='250' y1='${(p.progress * size * 0.6 + 50) % size}' x2='245' y2='${(p.progress * size * 0.6 + 70) % size}' stroke='#87CEEB' stroke-width='2'/>
  <line x1='350' y1='${(p.progress * size * 0.8 + 150) % size}' x2='345' y2='${(p.progress * size * 0.8 + 170) % size}' stroke='#87CEEB' stroke-width='2'/>
  <line x1='100' y1='${(p.progress * size * 0.4 + 200) % size}' x2='95' y2='${(p.progress * size * 0.4 + 220) % size}' stroke='#87CEEB' stroke-width='2'/>
  <line x1='320' y1='${(p.progress * size * 0.5 + 250) % size}' x2='315' y2='${(p.progress * size * 0.5 + 270) % size}' stroke='#87CEEB' stroke-width='2'/>
  <rect x='0' y='${size*0.85}' width='${size}' height='${size*0.15}' fill='#2f4f4f'/>
</svg>`;
}

function generateCloudFrame(p, size) {
  const cloudX = (p.progress * size * 1.5) % (size * 1.5) - size * 0.25;
  return `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='#87CEEB'/>
  <ellipse cx='${size*0.5}' cy='${size*0.95}' rx='${size*0.6}' ry='${size*0.15}' fill='#90EE90'/>
  <ellipse cx='${cloudX}' cy='80' rx='60' ry='35' fill='white' opacity='0.9'/>
  <ellipse cx='${cloudX + 30}' cy='70' rx='50' ry='30' fill='white' opacity='0.9'/>
  <ellipse cx='${cloudX + 60}' cy='85' rx='45' ry='28' fill='white' opacity='0.9'/>
  <ellipse cx='${cloudX + 300}' cy='120' rx='50' ry='28' fill='white' opacity='0.7'/>
  <ellipse cx='${cloudX + 330}' cy='110' rx='40' ry='25' fill='white' opacity='0.7'/>
  <ellipse cx='${cloudX + 500}' cy='60' rx='55' ry='30' fill='white' opacity='0.6'/>
  <ellipse cx='${cloudX + 530}' cy='50' rx='45' ry='25' fill='white' opacity='0.6'/>
</svg>`;
}

// 主函数
async function main() {
  if (!theme && !story) {
    console.log(`
SVG Animator - 动画生成工具

用法:
  node animate.js --theme "描述" [--frames N] [--duration 秒] [--output 文件]
  node animate.js --story "故事描述" [--scenes N] [--output 文件]

示例:
  node animate.js --theme "奔跑的小狗" --frames 24 --output /tmp/dog.mp4
  node animate.js --theme "飞翔的小鸟" --duration 3 --output /tmp/bird.mp4
  node animate.js --story "小猫的一天" --scenes 4 --output /tmp/cat_story.mp4

支持的主题关键词:
  - 动物: dog/cat/bird/fish (狗/猫/鸟/鱼)
  - 场景: sun/sunrise/sunset (日出/日落)
  - 天气: rain/cloud (雨/云)
`);
    return;
  }
  
  // 计算帧数
  if (duration && !frames) {
    frames = Math.ceil(duration * fps);
  }
  
  const outputDir = '/tmp/animation_frames';
  fs.mkdirSync(outputDir, { recursive: true });
  
  console.log(`生成 ${frames} 帧动画...`);
  console.log(`主题: ${theme || story}`);
  
  // 生成帧
  for (let i = 0; i < frames; i++) {
    const svg = generateAnimationFrame(i, frames, theme || story);
    fs.writeFileSync(`${outputDir}/frame_${String(i).padStart(4, '0')}.svg`, svg);
  }
  
  console.log('转换为 PNG...');
  // rsvg-convert 不支持 %04d 格式，用循环处理
  for (let i = 0; i < frames; i++) {
    const svgFile = `${outputDir}/frame_${String(i).padStart(4, '0')}.svg`;
    const pngFile = `${outputDir}/frame_${String(i).padStart(4, '0')}.png`;
    execSync(`rsvg-convert "${svgFile}" -o "${pngFile}"`, { stdio: 'pipe' });
  }
  console.log(`转换完成 ${frames} 个文件`);
  
  console.log('合成视频...');
  execSync(`ffmpeg -y -framerate ${fps} -i "${outputDir}/frame_%04d.png" -c:v mpeg4 -q:v 2 "${output}"`, { stdio: 'inherit' });
  
  console.log(`✅ 完成！视频保存到: ${output}`);
}

main().catch(console.error);
