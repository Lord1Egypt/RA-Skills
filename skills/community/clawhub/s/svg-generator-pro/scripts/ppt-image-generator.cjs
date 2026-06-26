const fs = require('fs');
const path = require('path');

// PPT 展示图生成器
// 支持 16:9 和 4:3 两种比例
// 专为 PowerPoint 演示优化

function generatePPTImage(options) {
    const { 
        style = 'tech', 
        colors = 'blue-purple', 
        ratio = '16:9',
        output = 'ppt-image.svg'
    } = options;

    // 根据比例设置尺寸
    let width, height;
    if (ratio === '4:3') {
        width = 1024;
        height = 768;
    } else {
        // 默认 16:9
        width = 1920;
        height = 1080;
    }

    // 颜色配置
    let colorConfig;
    switch(colors) {
        case 'blue-purple':
            colorConfig = {
                start: '#1e3a8a',
                middle: '#4f46e5', 
                end: '#7c3aed'
            };
            break;
        case 'green-blue':
            colorConfig = {
                start: '#047857',
                middle: '#0ea5e9',
                end: '#3b82f6'
            };
            break;
        case 'orange-red':
            colorConfig = {
                start: '#ea580c',
                middle: '#f97316',
                end: '#ef4444'
            };
            break;
        default:
            colorConfig = {
                start: '#1e3a8a',
                middle: '#4f46e5',
                end: '#7c3aed'
            };
    }

    // 生成 SVG 内容
    const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 渐变定义 -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${colorConfig.start}" />
      <stop offset="50%" stop-color="${colorConfig.middle}" />
      <stop offset="100%" stop-color="${colorConfig.end}" />
    </linearGradient>
    
    <!-- 抽象图案 -->
    <pattern id="codePattern" patternUnits="userSpaceOnUse" width="20" height="20">
      <path d="M0,0 L20,20 M20,0 L0,20" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
    </pattern>
  </defs>
  
  <!-- 背景 -->
  <rect width="${width}" height="${height}" fill="url(#bgGradient)" />
  
  <!-- PPT 优化的抽象元素 -->
  <!-- 左侧装饰 -->
  <circle cx="${width * 0.1}" cy="${height * 0.2}" r="${height * 0.05}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" />
  <circle cx="${width * 0.15}" cy="${height * 0.25}" r="${height * 0.03}" fill="rgba(255,255,255,0.15)" />
  
  <!-- 右侧装饰 -->
  <circle cx="${width * 0.9}" cy="${height * 0.8}" r="${height * 0.06}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" />
  <circle cx="${width * 0.85}" cy="${height * 0.75}" r="${height * 0.04}" fill="rgba(255,255,255,0.15)" />
  
  <!-- 中央数据流（适合放置标题） -->
  <path d="M ${width * 0.3} ${height * 0.4} Q ${width * 0.5} ${height * 0.3} ${width * 0.7} ${height * 0.4}" 
        stroke="rgba(255, 255, 255, 0.2)" stroke-width="2" fill="none" />
  <path d="M ${width * 0.3} ${height * 0.6} Q ${width * 0.5} ${height * 0.7} ${width * 0.7} ${height * 0.6}" 
        stroke="rgba(255, 255, 255, 0.15)" stroke-width="2" fill="none" />
  
  <!-- 网络连接点 -->
  <circle cx="${width * 0.4}" cy="${height * 0.4}" r="${height * 0.01}" fill="#ffffff" opacity="0.3" />
  <circle cx="${width * 0.5}" cy="${height * 0.4}" r="${height * 0.01}" fill="#ffffff" opacity="0.3" />
  <circle cx="${width * 0.6}" cy="${height * 0.4}" r="${height * 0.01}" fill="#ffffff" opacity="0.3" />
  <circle cx="${width * 0.4}" cy="${height * 0.6}" r="${height * 0.008}" fill="#ffffff" opacity="0.2" />
  <circle cx="${width * 0.5}" cy="${height * 0.6}" r="${height * 0.008}" fill="#ffffff" opacity="0.2" />
  <circle cx="${width * 0.6}" cy="${height * 0.6}" r="${height * 0.008}" fill="#ffffff" opacity="0.2" />
  
  <!-- 底部装饰性元素 -->
  <g opacity="0.05">
    <rect x="${width * 0.2}" y="${height * 0.85}" width="${width * 0.15}" height="${height * 0.1}" fill="url(#codePattern)" />
    <rect x="${width * 0.65}" y="${height * 0.85}" width="${width * 0.15}" height="${height * 0.1}" fill="url(#codePattern)" />
  </g>
</svg>`;

    // 写入文件
    fs.writeFileSync(output, svgContent);
    console.log(`✅ PPT 展示图已生成: ${output}`);
    console.log(`📊 尺寸: ${width}x${height} (${ratio})`);
    console.log(`🎨 风格: ${style}, 颜色: ${colors}`);
}

// 命令行参数处理
if (require.main === module) {
    const args = process.argv.slice(2);
    const options = {};
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--style') {
            options.style = args[i + 1];
            i++;
        } else if (args[i] === '--colors') {
            options.colors = args[i + 1];
            i++;
        } else if (args[i] === '--ratio') {
            options.ratio = args[i + 1];
            i++;
        } else if (args[i] === '--output') {
            options.output = args[i + 1];
            i++;
        }
    }
    
    generatePPTImage(options);
}

module.exports = { generatePPTImage };