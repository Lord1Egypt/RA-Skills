#!/usr/bin/env node
/**
 * Canvas Design Generator - 高端PPT图片生成
 * 使用Canvas API生成艺术级幻灯片图片
 */

const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = '/root/.openclaw/workspace/data/canvas-output';

/**
 * 生成艺术级幻灯片图片
 */
function generateArtSlide(options) {
    const { title, subtitle, style, pageNum, totalPages } = options;
    
    const canvas = {
        width: 1280,
        height: 720,
        ctx: null,
        
        init() {
            // 创建一个临时的HTML来渲染canvas
            return this;
        },
        
        render() {
            const styles = this.getStyleConfig(style);
            
            const html = this.generateHTML(title, subtitle, styles, pageNum, totalPages);
            return html;
        },
        
        getStyleConfig(styleName) {
            const configs = {
                'corporate': {
                    bg: '#0f172a',
                    accent: '#3b82f6',
                    secondary: '#1e293b',
                    text: '#f8fafc',
                    pattern: 'grid'
                },
                'tech': {
                    bg: '#0a0a0f',
                    accent: '#00ffff',
                    secondary: '#1a0a2e',
                    text: '#e0e0e0',
                    pattern: 'circuit'
                },
                'luxury': {
                    bg: '#1a1a1a',
                    accent: '#d4af37',
                    secondary: '#2d2d2d',
                    text: '#f5f5f5',
                    pattern: 'geometric'
                },
                'nature': {
                    bg: '#f0f4e8',
                    accent: '#4a7c59',
                    secondary: '#d4e4d1',
                    text: '#2d4a3e',
                    pattern: 'organic'
                }
            };
            
            return configs[styleName] || configs.corporate;
        },
        
        generateHTML(title, subtitle, style, pageNum, totalPages) {
            return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Playfair+Display:wght@400;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            width: 1280px;
            height: 720px;
            background: ${style.bg};
            font-family: 'Noto Sans SC', 'Playfair Display', serif;
            color: ${style.text};
            overflow: hidden;
            position: relative;
        }
        
        /* 背景图案 */
        .pattern {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 0.1;
            background-image: 
                linear-gradient(${style.accent} 1px, transparent 1px),
                linear-gradient(90deg, ${style.accent} 1px, transparent 1px);
            background-size: 50px 50px;
        }
        
        /* 装饰元素 */
        .accent-line {
            position: absolute;
            top: 60px;
            left: 60px;
            width: 200px;
            height: 4px;
            background: ${style.accent};
        }
        
        .accent-dot {
            position: absolute;
            top: 80px;
            left: 270px;
            width: 12px;
            height: 12px;
            background: ${style.accent};
            border-radius: 50%;
        }
        
        /* 主标题 */
        .title {
            position: absolute;
            top: 140px;
            left: 60px;
            right: 60px;
            font-size: 64px;
            font-weight: 700;
            letter-spacing: -1px;
            line-height: 1.2;
        }
        
        /* 副标题 */
        .subtitle {
            position: absolute;
            top: 340px;
            left: 60px;
            right: 60px;
            font-size: 28px;
            font-weight: 300;
            opacity: 0.7;
            letter-spacing: 2px;
        }
        
        /* 底部信息 */
        .footer {
            position: absolute;
            bottom: 40px;
            left: 60px;
            right: 60px;
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            opacity: 0.5;
            letter-spacing: 1px;
        }
        
        /* 装饰角 */
        .corner {
            position: absolute;
            width: 80px;
            height: 80px;
            border: 2px solid ${style.accent};
        }
        .corner-tl { top: 30px; left: 30px; border-right: none; border-bottom: none; }
        .corner-tr { top: 30px; right: 30px; border-left: none; border-bottom: none; }
        .corner-bl { bottom: 30px; left: 30px; border-right: none; border-top: none; }
        .corner-br { bottom: 30px; right: 30px; border-left: none; border-top: none; }
        
        /* 页码 */
        .page-num {
            position: absolute;
            bottom: 40px;
            right: 60px;
            font-size: 14px;
            color: ${style.accent};
        }
    </style>
</head>
<body>
    <div class="pattern"></div>
    <div class="accent-line"></div>
    <div class="accent-dot"></div>
    
    <div class="corner corner-tl"></div>
    <div class="corner corner-tr"></div>
    <div class="corner corner-bl"></div>
    <div class="corner corner-br"></div>
    
    <div class="title">${title}</div>
    <div class="subtitle">${subtitle || ''}</div>
    
    <div class="footer">
        <span>PRESENTATION</span>
        <span>${new Date().getFullYear()}</span>
    </div>
    
    <div class="page-num">${pageNum} / ${totalPages}</div>
</body>
</html>
`;
        }
    };
    
    return canvas.render();
}

// 导出
module.exports = { generateArtSlide };

// 如果直接运行
if (require.main === module) {
    const args = process.argv.slice(2);
    let title = 'Slide Title';
    let subtitle = '';
    let style = 'corporate';
    let pageNum = 1;
    let totalPages = 5;
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--title' && args[i+1]) title = args[++i];
        if (args[i] === '--subtitle' && args[i+1]) subtitle = args[++i];
        if (args[i] === '--style' && args[i+1]) style = args[++i];
        if (args[i] === '--page' && args[i+1]) pageNum = parseInt(args[++i]);
        if (args[i] === '--total' && args[i+1]) totalPages = parseInt(args[++i]);
    }
    
    const gen = new (require('./canvas-generator'))();
    const html = generateArtSlide({ title, subtitle, style, pageNum, totalPages });
    
    const outputPath = path.join(OUTPUT_DIR, `art_slide_${pageNum}.html`);
    fs.writeFileSync(outputPath, html);
    console.log(`Generated: ${outputPath}`);
}
