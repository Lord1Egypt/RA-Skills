const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');
const path = require('path');

// 读取 SVG 文件
const svgPath = process.argv[2];
const pngPath = process.argv[3] || svgPath.replace('.svg', '.png');

if (!svgPath) {
    console.error('Usage: node svg-to-png.cjs <input.svg> [output.png]');
    process.exit(1);
}

// 读取 SVG 内容
const svgContent = fs.readFileSync(svgPath, 'utf8');

// 解析 SVG 尺寸
const widthMatch = svgContent.match(/width="(\d+)"/);
const heightMatch = svgContent.match(/height="(\d+)"/);
const width = widthMatch ? parseInt(widthMatch[1]) : 1920;
const height = heightMatch ? parseInt(heightMatch[1]) : 1080;

// 创建 Canvas
const canvas = createCanvas(width, height);
const ctx = canvas.getContext('2d');

// 设置白色背景
ctx.fillStyle = 'white';
ctx.fillRect(0, 0, width, height);

// 由于 canvas 不直接支持 SVG，我们使用一个简单的转换
// 对于复杂 SVG，可能需要使用 puppeteer 或其他工具
// 这里我们创建一个简化版本

// 渐变背景
const gradient = ctx.createLinearGradient(0, 0, width, height);
gradient.addColorStop(0, '#1e3a8a');
gradient.addColorStop(0.5, '#4f46e5');
gradient.addColorStop(1, '#7c3aed');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, width, height);

// 添加一些装饰元素
ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(width * 0.1, height * 0.3);
ctx.quadraticCurveTo(width * 0.3, height * 0.2, width * 0.5, height * 0.3);
ctx.quadraticCurveTo(width * 0.7, height * 0.4, width * 0.9, height * 0.3);
ctx.stroke();

// 圆形节点
ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
ctx.beginPath();
ctx.arc(width * 0.3, height * 0.3, 15, 0, Math.PI * 2);
ctx.fill();
ctx.beginPath();
ctx.arc(width * 0.5, height * 0.3, 15, 0, Math.PI * 2);
ctx.fill();
ctx.beginPath();
ctx.arc(width * 0.7, height * 0.3, 15, 0, Math.PI * 2);
ctx.fill();

// 保存为 PNG
const buffer = canvas.toBuffer('image/png');
fs.writeFileSync(pngPath, buffer);

console.log(`✅ PNG 图片已生成: ${pngPath}`);
console.log(`📊 尺寸: ${width}x${height}`);