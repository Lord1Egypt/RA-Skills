const fs = require('fs');
const path = require('path');

// SVG 生成函数
function generateTechSVG(options = {}) {
  const {
    width = 1920,
    height = 1080,
    primaryColor = '#1e3a8a',
    secondaryColor = '#7c3aed',
    opacity = 0.1
  } = options;

  const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 渐变定义 -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${primaryColor}" />
      <stop offset="50%" stop-color="#4f46e5" />
      <stop offset="100%" stop-color="${secondaryColor}" />
    </linearGradient>
    
    <!-- 抽象图案 -->
    <pattern id="codePattern" patternUnits="userSpaceOnUse" width="20" height="20">
      <path d="M0,0 L20,20 M20,0 L0,20" stroke="rgba(255,255,255,${opacity * 0.5})" stroke-width="1"/>
    </pattern>
  </defs>
  
  <!-- 背景 -->
  <rect width="${width}" height="${height}" fill="url(#bgGradient)" />
  
  <!-- 抽象数据流 -->
  <path d="M 200 300 Q 400 200 600 300 T 1000 300" stroke="rgba(255, 255, 255, ${opacity * 2})" stroke-width="2" fill="none" />
  <path d="M 250 400 Q 450 300 650 400 T 1050 400" stroke="rgba(255, 255, 255, ${opacity * 1.5})" stroke-width="2" fill="none" />
  <path d="M 300 500 Q 500 400 700 500 T 1100 500" stroke="rgba(255, 255, 255, ${opacity})" stroke-width="2" fill="none" />
  
  <!-- 网络连接点 -->
  <circle cx="600" cy="300" r="8" fill="#ffffff" opacity="${opacity * 3}" />
  <circle cx="800" cy="300" r="8" fill="#ffffff" opacity="${opacity * 3}" />
  <circle cx="1000" cy="300" r="8" fill="#ffffff" opacity="${opacity * 3}" />
  
  <!-- 装饰性元素 -->
  <circle cx="1800" cy="200" r="50" fill="none" stroke="rgba(255, 255, 255, ${opacity * 0.5})" stroke-width="2" />
  <circle cx="100" cy="200" r="30" fill="none" stroke="rgba(255, 255, 255, ${opacity * 0.5})" stroke-width="2" />
  
  <!-- 抽象电路板图案 -->
  <g opacity="${opacity * 0.5}">
    <rect x="400" y="600" width="200" height="200" fill="url(#codePattern)" />
    <rect x="1300" y="600" width="200" height="200" fill="url(#codePattern)" />
  </g>
</svg>`;

  return svgContent;
}

function generateMinimalSVG(options = {}) {
  const {
    width = 1920,
    height = 1080,
    primaryColor = '#6b7280',
    secondaryColor = '#3b82f6',
    opacity = 0.05
  } = options;

  const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${primaryColor}" />
      <stop offset="100%" stop-color="${secondaryColor}" />
    </linearGradient>
  </defs>
  
  <rect width="${width}" height="${height}" fill="url(#bgGradient)" />
  
  <!-- 简约几何形状 -->
  <circle cx="300" cy="200" r="80" fill="none" stroke="rgba(255,255,255,${opacity})" stroke-width="2"/>
  <rect x="1500" y="150" width="120" height="120" fill="none" stroke="rgba(255,255,255,${opacity})" stroke-width="2" transform="rotate(45 1560 210)"/>
  <line x1="500" y1="800" x2="800" y2="600" stroke="rgba(255,255,255,${opacity * 2})" stroke-width="1"/>
  <line x1="1200" y1="800" x2="900" y2="600" stroke="rgba(255,255,255,${opacity * 2})" stroke-width="1"/>
</svg>`;

  return svgContent;
}

// 命令行参数处理
const args = process.argv.slice(2);
let style = 'tech';
let output = 'output.svg';
let primaryColor = '';
let secondaryColor = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--style' || args[i] === '-s') {
    style = args[i + 1];
    i++;
  } else if (args[i] === '--output' || args[i] === '-o') {
    output = args[i + 1];
    i++;
  } else if (args[i] === '--primary' || args[i] === '-p') {
    primaryColor = args[i + 1];
    i++;
  } else if (args[i] === '--secondary' || args[i] === '-sec') {
    secondaryColor = args[i + 1];
    i++;
  }
}

const options = {};
if (primaryColor) options.primaryColor = primaryColor;
if (secondaryColor) options.secondaryColor = secondaryColor;

let svgContent;
switch (style) {
  case 'minimal':
    svgContent = generateMinimalSVG(options);
    break;
  default:
    svgContent = generateTechSVG(options);
}

// 确保输出目录存在
const outputPath = path.resolve(output);
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(outputPath, svgContent);
console.log(`✅ SVG 文件已生成: ${outputPath}`);