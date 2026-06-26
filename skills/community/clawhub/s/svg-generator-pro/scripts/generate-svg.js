#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 解析命令行参数
const args = process.argv.slice(2);
const options = {
  style: 'tech',
  colors: 'blue-purple',
  width: 1920,
  height: 1080,
  output: 'output.svg'
};

// 简单的参数解析
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--style' || args[i] === '-s') {
    options.style = args[i + 1];
  } else if (args[i] === '--colors' || args[i] === '-c') {
    options.colors = args[i + 1];
  } else if (args[i] === '--output' || args[i] === '-o') {
    options.output = args[i + 1];
  } else if (args[i] === '--width' || args[i] === '-w') {
    options.width = parseInt(args[i + 1]);
  } else if (args[i] === '--height' || args[i] === '-h') {
    options.height = parseInt(args[i + 1]);
  }
}

// 颜色配置
const colorSchemes = {
  'blue-purple': {
    gradient: ['stop-color="#1e3a8a"', 'stop-color="#4f46e5"', 'stop-color="#7c3aed"'],
    primary: '#4f46e5',
    secondary: '#7c3aed'
  },
  'gray-blue': {
    gradient: ['stop-color="#374151"', 'stop-color="#1e40af"', 'stop-color="#1e3a8a"'],
    primary: '#1e40af',
    secondary: '#1e3a8a'
  },
  'minimal': {
    gradient: ['stop-color="#6b7280"', 'stop-color="#4b5563"', 'stop-color="#374151"'],
    primary: '#4b5563',
    secondary: '#374151'
  }
};

const colors = colorSchemes[options.colors] || colorSchemes['blue-purple'];

// 生成不同风格的 SVG
function generateTechStyle() {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${options.width}" height="${options.height}" viewBox="0 0 ${options.width} ${options.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" ${colors.gradient[0]} />
      <stop offset="50%" ${colors.gradient[1]} />
      <stop offset="100%" ${colors.gradient[2]} />
    </linearGradient>
    <pattern id="codePattern" patternUnits="userSpaceOnUse" width="20" height="20">
      <path d="M0,0 L20,20 M20,0 L0,20" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
    </pattern>
  </defs>
  
  <rect width="${options.width}" height="${options.height}" fill="url(#bgGradient)" />
  
  <!-- 数据流曲线 -->
  <path d="M 200 300 Q 400 200 600 300 T 1000 300" stroke="rgba(255, 255, 255, 0.2)" stroke-width="2" fill="none" />
  <path d="M 250 400 Q 450 300 650 400 T 1050 400" stroke="rgba(255, 255, 255, 0.15)" stroke-width="2" fill="none" />
  <path d="M 300 500 Q 500 400 700 500 T 1100 500" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" fill="none" />
  
  <!-- 网络连接点 -->
  <circle cx="600" cy="300" r="8" fill="#ffffff" opacity="0.3" />
  <circle cx="800" cy="300" r="8" fill="#ffffff" opacity="0.3" />
  <circle cx="1000" cy="300" r="8" fill="#ffffff" opacity="0.3" />
  
  <!-- 抽象电路板图案 -->
  <g opacity="0.05">
    <rect x="400" y="600" width="200" height="200" fill="url(#codePattern)" />
    <rect x="1300" y="600" width="200" height="200" fill="url(#codePattern)" />
  </g>
</svg>`;
}

function generateMinimalStyle() {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${options.width}" height="${options.height}" viewBox="0 0 ${options.width} ${options.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" ${colors.gradient[0]} />
      <stop offset="50%" ${colors.gradient[1]} />
      <stop offset="100%" ${colors.gradient[2]} />
    </linearGradient>
  </defs>
  
  <rect width="${options.width}" height="${options.height}" fill="url(#bgGradient)" />
  
  <!-- 简约几何形状 -->
  <circle cx="${options.width * 0.8}" cy="${options.height * 0.2}" r="50" fill="none" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" />
  <circle cx="${options.width * 0.2}" cy="${options.height * 0.8}" r="30" fill="none" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" />
  <rect x="${options.width * 0.75}" y="${options.height * 0.15}" width="100" height="100" fill="none" stroke="rgba(255, 255, 255, 0.05)" stroke-width="1" transform="rotate(45 ${options.width * 0.8} ${options.height * 0.2})" />
</svg>`;
}

// 生成 SVG
let svgContent;
switch (options.style) {
  case 'minimal':
    svgContent = generateMinimalStyle();
    break;
  case 'tech':
  default:
    svgContent = generateTechStyle();
}

// 写入文件
fs.writeFileSync(options.output, svgContent);
console.log(`✅ SVG generated successfully: ${options.output}`);
console.log(`   Style: ${options.style}, Colors: ${options.colors}`);
console.log(`   Size: ${options.width}x${options.height}`);