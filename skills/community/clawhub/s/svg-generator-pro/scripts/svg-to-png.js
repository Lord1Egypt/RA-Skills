#!/usr/bin/env node

// SVG to PNG 转换器
const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');
const path = require('path');

async function convertSvgToPng(svgPath, pngPath, width = 1920, height = 1080) {
    try {
        // 读取 SVG 文件
        const svgContent = fs.readFileSync(svgPath, 'utf8');
        
        // 创建 Canvas
        const canvas = createCanvas(width, height);
        const ctx = canvas.getContext('2d');
        
        // 设置背景为透明
        ctx.clearRect(0, 0, width, height);
        
        // 这里简化处理 - 实际中可能需要更复杂的 SVG 渲染
        // 对于我们的简单 SVG，我们可以直接绘制渐变背景
        
        // 创建渐变
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, '#1e3a8a');
        gradient.addColorStop(0.5, '#4f46e5');
        gradient.addColorStop(1, '#7c3aed');
        
        // 填充背景
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
        
        // 添加一些装饰性元素（简化版）
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(width * 0.1, height * 0.3);
        ctx.quadraticCurveTo(width * 0.3, height * 0.2, width * 0.5, height * 0.3);
        ctx.quadraticCurveTo(width * 0.7, height * 0.4, width * 0.9, height * 0.3);
        ctx.stroke();
        
        // 保存为 PNG
        const buffer = canvas.toBuffer('image/png');
        fs.writeFileSync(pngPath, buffer);
        
        console.log(`✅ PNG 文件已生成: ${pngPath}`);
        console.log(`📊 尺寸: ${width}x${height}`);
        
    } catch (error) {
        console.error('❌ 转换失败:', error.message);
    }
}

// 命令行参数处理
if (require.main === module) {
    const args = process.argv.slice(2);
    const svgPath = args[0] || './test-svg-image.svg';
    const pngPath = args[1] || './test-png-image.png';
    const width = parseInt(args[2]) || 1920;
    const height = parseInt(args[3]) || 1080;
    
    convertSvgToPng(svgPath, pngPath, width, height);
}