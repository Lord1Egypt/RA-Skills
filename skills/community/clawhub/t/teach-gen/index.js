#!/usr/bin/env node

/**
 * teach-gen - 交互式教学网页生成器
 * Skill主入口文件
 */

const fs = require('fs').promises;
const path = require('path');

// 简化版生成器（浏览器环境完整版见 generator.js）
const SimplifiedGenerator = {
  subjects: ['math', 'physics', 'chemistry'],
  grades: ['elementary', 'middle', 'high', 'college'],

  parseOptions(args) {
    const options = {
      subject: 'math',
      grade: 'high',
      theme: 'light',
      output: 'output.html'
    };

    // 处理 --key value 和 --key=value 两种格式
    for (let i = 0; i < args.length; i++) {
      const arg = args[i];

      if (arg.startsWith('--subject=')) {
        options.subject = arg.split('=')[1];
      } else if (arg === '--subject' && args[i + 1]) {
        options.subject = args[++i];
      } else if (arg.startsWith('--grade=')) {
        options.grade = arg.split('=')[1];
      } else if (arg === '--grade' && args[i + 1]) {
        options.grade = args[++i];
      } else if (arg.startsWith('--theme=')) {
        options.theme = arg.split('=')[1];
      } else if (arg === '--theme' && args[i + 1]) {
        options.theme = args[++i];
      } else if (arg.startsWith('--output=')) {
        options.output = arg.split('=')[1];
      } else if (arg === '--output' && args[i + 1]) {
        options.output = args[++i];
      } else if (!arg.startsWith('--')) {
        options.input = arg;
      }
    }

    return options;
  },

  validateOptions(options) {
    const errors = [];

    if (!this.subjects.includes(options.subject)) {
      errors.push(`无效的学科: ${options.subject}，可选: ${this.subjects.join(', ')}`);
    }

    if (!this.grades.includes(options.grade)) {
      errors.push(`无效的学龄: ${options.grade}，可选: ${this.grades.join(', ')}`);
    }

    if (!options.input) {
      errors.push('请指定输入文件路径');
    }

    return errors;
  },

  async generateFromMarkdown(content, options) {
    const subjectNames = {
      math: { name: '数学', color: '#4F46E5', icon: '∫' },
      physics: { name: '物理', color: '#0891B2', icon: 'F' },
      chemistry: { name: '化学', color: '#059669', icon: '⚗' }
    };

    const subject = subjectNames[options.subject];
    const title = this.extractTitle(content) || '交互式教学课件';

    // 生成现代简约风格HTML
    const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    :root {
      --primary: ${subject.color};
      --bg: #ffffff;
      --text: #1f2937;
      --text-light: #6b7280;
      --border: #e5e7eb;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.7;
      color: var(--text);
      background: #f9fafb;
    }

    .container {
      max-width: 1000px;
      margin: 0 auto;
      padding: 40px 20px;
    }

    header {
      text-align: center;
      padding: 50px 30px;
      background: linear-gradient(135deg, var(--primary) 0%, ${this.adjustColor(subject.color, -30)} 100%);
      color: white;
      border-radius: 20px;
      margin-bottom: 40px;
      box-shadow: 0 10px 40px -10px rgba(0,0,0,0.2);
    }

    header h1 {
      font-size: clamp(1.8rem, 4vw, 3rem);
      font-weight: 700;
      margin-bottom: 15px;
    }

    header .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 20px;
      background: rgba(255,255,255,0.2);
      border-radius: 30px;
      font-size: 0.95rem;
      backdrop-filter: blur(10px);
    }

    section {
      background: var(--bg);
      border-radius: 16px;
      padding: 35px;
      margin-bottom: 30px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      border: 1px solid var(--border);
    }

    section h2 {
      font-size: 1.6rem;
      color: var(--primary);
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 2px solid var(--primary);
    }

    p {
      margin-bottom: 1.2em;
      font-size: 1.05rem;
    }

    .formula {
      padding: 25px;
      background: #f3f4f6;
      border-radius: 12px;
      margin: 25px 0;
      text-align: center;
      font-size: 1.2rem;
      overflow-x: auto;
    }

    .animation-box {
      padding: 30px;
      background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
      border-radius: 16px;
      margin: 30px 0;
    }

    .animation-controls {
      display: flex;
      gap: 12px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .animation-controls button {
      padding: 10px 24px;
      border: none;
      background: var(--primary);
      color: white;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .animation-controls button:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .animation-controls button.secondary {
      background: white;
      color: var(--text);
    }

    canvas {
      max-width: 100%;
      height: auto;
      border-radius: 12px;
      background: white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    footer {
      text-align: center;
      padding: 40px;
      color: var(--text-light);
      font-size: 0.9rem;
    }

    @media (max-width: 640px) {
      .container { padding: 20px 15px; }
      section { padding: 25px; }
      header { padding: 35px 20px; }
    }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js"></script>
</head>
<body>
  <div class="container">
    <header>
      <h1>${title}</h1>
      <span class="badge">${subject.icon} ${subject.name}</span>
    </header>

    ${this.renderMarkdownSections(content)}

    <footer>
      <p>由交互式教学网页生成器创建</p>
    </footer>
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      renderMathInElement(document.body, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false}
        ]
      });
      initAnimations();
    });

    function initAnimations() {
      // 示例动画初始化
      document.querySelectorAll('.animation-box canvas').forEach(canvas => {
        drawGraph(canvas);
      });
    }

    function drawGraph(canvas) {
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;

      ctx.clearRect(0, 0, w, h);

      // 绘制坐标轴
      ctx.strokeStyle = '#d1d5db';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, h/2);
      ctx.lineTo(w, h/2);
      ctx.moveTo(w/2, 0);
      ctx.lineTo(w/2, h);
      ctx.stroke();

      // 绘制函数曲线
      ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim();
      ctx.lineWidth = 3;
      ctx.beginPath();

      for (let px = 0; px <= w; px++) {
        const x = (px - w/2) / 50;
        const y = -x * x;
        const py = y * 50 + h/2;
        if (px === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // 动画效果
      anime({
        targets: canvas,
        opacity: [0, 1],
        scale: [0.9, 1],
        duration: 800,
        easing: 'easeOutCubic'
      });
    }
  </script>
</body>
</html>`;

    return html;
  },

  extractTitle(content) {
    const match = content.match(/^#\s+(.+)$/m);
    return match ? match[1] : null;
  },

  adjustColor(hex, amount) {
    const num = parseInt(hex.replace('#', ''), 16);
    const r = Math.min(255, Math.max(0, (num >> 16) + amount));
    const g = Math.min(255, Math.max(0, ((num >> 8) & 0x00FF) + amount));
    const b = Math.min(255, Math.max(0, (num & 0x0000FF) + amount));
    return '#' + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
  },

  renderMarkdownSections(content) {
    const lines = content.split('\n');
    let html = '';
    let currentSection = null;
    let inCodeBlock = false;

    lines.forEach(line => {
      if (line.startsWith('```')) {
        inCodeBlock = !inCodeBlock;
        return;
      }
      if (inCodeBlock) return;

      if (line.startsWith('# ')) {
        if (currentSection) html += '</section>';
        const title = line.replace(/^#\s+/, '');
        html += `<section><h2>${title}</h2>`;
        currentSection = 'main';
      } else if (line.startsWith('## ')) {
        if (currentSection) html += '</section>';
        const title = line.replace(/^##\s+/, '');
        html += `<section><h2>${title}</h2>`;
        currentSection = 'sub';
      } else if (line.trim()) {
        if (line.includes('$$')) {
          html += `<div class="formula">${line.replace(/\$\$/g, '')}</div>`;
        } else if (line.match(/^\[动画:/)) {
          html += this.renderAnimationBox(line);
        } else {
          html += `<p>${line}</p>`;
        }
      }
    });

    if (currentSection) html += '</section>';
    return html;
  },

  renderAnimationBox(line) {
    return `
    <div class="animation-box">
      <div class="animation-controls">
        <button onclick="playAnimation()">▶ 播放动画</button>
        <button class="secondary" onclick="resetAnimation()">↺ 重置</button>
      </div>
      <canvas width="600" height="300"></canvas>
    </div>`;
  }
};

// 主函数
async function main(args) {
  const options = SimplifiedGenerator.parseOptions(args);

  const errors = SimplifiedGenerator.validateOptions(options);
  if (errors.length > 0) {
    console.error('错误:');
    errors.forEach(e => console.error(`  ✗ ${e}`));
    process.exit(1);
  }

  try {
    // 读取输入文件
    const content = await fs.readFile(options.input, 'utf-8');

    // 生成HTML
    const html = await SimplifiedGenerator.generateFromMarkdown(content, options);

    // 写入输出文件
    await fs.writeFile(options.output, html, 'utf-8');

    console.log(`✓ 成功生成: ${options.output}`);
    console.log(`  学科: ${options.subject}`);
    console.log(`  学龄: ${options.grade}`);
    console.log(`  主题: ${options.theme}`);

    return { success: true, output: options.output };
  } catch (error) {
    console.error(`✗ 生成失败: ${error.message}`);
    process.exit(1);
  }
}

// CLI入口
if (require.main === module) {
  main(process.argv.slice(2));
}

module.exports = { SimplifiedGenerator, main };
