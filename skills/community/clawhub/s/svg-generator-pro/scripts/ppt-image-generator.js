#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// PPT 展示图模板配置
const pptTemplates = {
  // 数据可视化风格
  'data-viz': {
    width: 1920,
    height: 1080,
    colors: ['#1e40af', '#3b82f6', '#60a5fa'],
    elements: ['charts', 'data-flow', 'network-nodes']
  },
  // 科技简约风格  
  'tech-minimal': {
    width: 1920,
    height: 1080,
    colors: ['#1e3a8a', '#4f46e5', '#7c3aed'],
    elements: ['abstract-shapes', 'geometric-patterns', 'subtle-gradients']
  },
  // 商务专业风格
  'business-pro': {
    width: 1920,
    height: 1080,
    colors: ['#0c4a6e', '#0ea5e9', '#7dd3fc'],
    elements: ['clean-lines', 'professional-icons', 'corporate-colors']
  },
  // 创意设计风格
  'creative-design': {
    width: 1920,
    height: 1080,
    colors: ['#7c2d12', '#f59e0b', '#fbbf24'],
    elements: ['artistic-elements', 'creative-patterns', 'bold-colors']
  }
};

function generatePPTImage(template, outputPath) {
  const config = pptTemplates[template] || pptTemplates['tech-minimal'];
  
  let svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${config.width}" height="${config.height}" viewBox="0 0 ${config.width} ${config.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 渐变定义 -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${config.colors[0]}" />
      <stop offset="50%" stop-color="${config.colors[1]}" />
      <stop offset="100%" stop-color="${config.colors[2]}" />
    </linearGradient>
  </defs>
  
  <!-- 背景 -->
  <rect width="${config.width}" height="${config.height}" fill="url(#bgGradient)" />
  
  <!-- 根据模板添加元素 -->
  `;
  
  // 添加不同模板的元素
  if (template === 'data-viz') {
    svgContent += `
  <!-- 数据流图表 -->
  <path d="M 300 400 Q 500 300 700 400 T 1100 400" stroke="rgba(255, 255, 255, 0.3)" stroke-width="3" fill="none" />
  <path d="M 350 500 Q 550 400 750 500 T 1150 500" stroke="rgba(255, 255, 255, 0.2)" stroke-width="3" fill="none" />
  <path d="M 400 600 Q 600 500 800 600 T 1200 600" stroke="rgba(255, 255, 255, 0.1)" stroke-width="3" fill="none" />
  
  <!-- 数据点 -->
  <circle cx="700" cy="400" r="12" fill="#ffffff" opacity="0.4" />
  <circle cx="900" cy="400" r="12" fill="#ffffff" opacity="0.4" />
  <circle cx="1100" cy="400" r="12" fill="#ffffff" opacity="0.4" />
    `;
  } else if (template === 'business-pro') {
    svgContent += `
  <!-- 商务线条 -->
  <line x1="200" y1="300" x2="1720" y2="300" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" />
  <line x1="200" y1="500" x2="1720" y2="500" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" />
  <line x1="200" y1="700" x2="1720" y2="700" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" />
  
  <!-- 专业图标占位符 -->
  <rect x="860" y="400" width="200" height="200" rx="20" fill="rgba(255, 255, 255, 0.05)" />
    `;
  } else if (template === 'creative-design') {
    svgContent += `
  <!-- 创意几何形状 -->
  <polygon points="600,300 700,200 800,300 700,400" fill="rgba(255, 255, 255, 0.1)" />
  <polygon points="1100,500 1200,400 1300,500 1200,600" fill="rgba(255, 255, 255, 0.1)" />
  <circle cx="950" cy="700" r="80" fill="rgba(255, 255, 255, 0.05)" />
    `;
  } else {
    // 默认科技简约风格
    svgContent += `
  <!-- 抽象数据流 -->
  <path d="M 200 300 Q 400 200 600 300 T 1000 300" stroke="rgba(255, 255, 255, 0.2)" stroke-width="2" fill="none" />
  <path d="M 250 400 Q 450 300 650 400 T 1050 400" stroke="rgba(255, 255, 255, 0.15)" stroke-width="2" fill="none" />
  <path d="M 300 500 Q 500 400 700 500 T 1100 500" stroke="rgba(255, 255, 255, 0.1)" stroke-width="2" fill="none" />
  
  <!-- 网络连接点 -->
  <circle cx="600" cy="300" r="8" fill="#ffffff" opacity="0.3" />
  <circle cx="800" cy="300" r="8" fill="#ffffff" opacity="0.3" />
  <circle cx="1000" cy="300" r="8" fill="#ffffff" opacity="0.3" />
    `;
  }
  
  svgContent += `
</svg>`;
  
  // 确保输出目录存在
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  fs.writeFileSync(outputPath, svgContent);
  console.log(`✅ PPT 展示图已生成: ${outputPath}`);
}

// 命令行参数处理
if (require.main === module) {
  const args = process.argv.slice(2);
  let template = 'tech-minimal';
  let outputPath = './ppt-slide-background.svg';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--template' || args[i] === '-t') {
      template = args[i + 1];
      i++;
    } else if (args[i] === '--output' || args[i] === '-o') {
      outputPath = args[i + 1];
      i++;
    }
  }
  
  generatePPTImage(template, outputPath);
}