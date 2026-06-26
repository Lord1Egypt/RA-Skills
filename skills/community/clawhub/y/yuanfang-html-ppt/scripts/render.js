'use strict';
const fs = require('node:fs');
const path = require('node:path');
const PptxGenJS = require('pptxgenjs');
const { parseSlides } = require('./parse-slides');
const { loadTheme, listThemes } = require('./theme-mapper');
const { applyBrandOverride } = require('./brand-override');
const { applyThemeOverride } = require('./theme-override');
const { renderCover, renderContent, renderSummary } = require('./generator-a');
const { renderSection, renderTwoColumn, renderData, renderQuote } = require('./generator-c');
const { renderChartBar, renderChartLine, renderChartPie } = require('./generator-charts');

const VALID_PLATFORMS = {
  macos:      { w: 13.333, h: 7.5 },
  windows:    { w: 13.333, h: 7.5 },
  widescreen: { w: 13.333, h: 7.5 },
  '4-3':      { w: 10, h: 7.5 },
};

const USAGE = `用法: node scripts/render.js --file <content.json> [选项]

必填:
  --file <path>              content.json 路径

内容覆盖 (可选, 优先于 content.json):
  --theme <name>             主题名 (覆盖 content.json 的 theme)
  --brand <name>             品牌名 (覆盖 content.json 的 brand)

输出 (可选):
  --output <path>            输出 .pptx 路径 (默认: output.pptx)
  --platforms <key>          macos / windows / widescreen / 4-3 (默认: macos)
  --logo <path>              cover 幻灯片右上角 logo (覆盖 content.json 的 logo)
  --brand-spec <path>        品牌色 override 文件 (JSON, 优先级最高)

其他:
  --skip-confirm             跳过 Step 2 五项用户确认
  --help, -h                 显示帮助

可用主题: ${'(加载时检查)'} `;

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') {
      args.help = true;
    } else if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

function hardGate(content, context) {
  if (!content.theme) throw new Error('❌ 缺少 theme 字段');
  if (!content.brand) throw new Error('❌ 缺少 brand 字段');
  if (!content.slides?.length && !content.layout) {
    throw new Error('❌ 缺少 slides 数组或单页 layout');
  }
  if (!context.contentConfirmed) throw new Error('❌ 内容未确认');
  if (!context.themeConfirmed) throw new Error('❌ 主题未确认');
  if (!context.brandConfirmed) throw new Error('❌ 品牌未确认');
  if (!context.layoutConfirmed) throw new Error('❌ 布局未确认');
  if (!context.mediaConfirmed) throw new Error('❌ 媒体未确认');
}

async function render(opts) {
  if (opts.help) {
    console.log(USAGE);
    return { help: true };
  }

  const content = JSON.parse(fs.readFileSync(opts.file, 'utf8'));

  if (opts.theme) content.theme = opts.theme;
  if (opts.brand) content.brand = opts.brand;
  if (opts.logo) content.logo = opts.logo;

  const skip = opts['skip-confirm'] || opts.yes === true || opts.yes === 'true';
  const context = {
    contentConfirmed: skip,
    themeConfirmed: skip,
    brandConfirmed: skip,
    layoutConfirmed: skip,
    mediaConfirmed: skip,
  };
  hardGate(content, context);

  const { slides } = parseSlides(content);

  const designDir = path.resolve(__dirname, '..', '..', 'yuanfang-design');
  let theme = loadTheme(content.theme, designDir);

  if (opts['brand-spec']) {
    const specPath = path.resolve(opts['brand-spec']);
    if (fs.existsSync(specPath)) {
      const brandSpec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
      theme = applyBrandOverride(theme, brandSpec);
    } else {
      console.warn(`⚠️ --brand-spec 文件不存在: ${specPath}, 跳过品牌色 override`);
    }
  }

  const platform = opts.platforms || 'macos';
  const dims = VALID_PLATFORMS[platform] || VALID_PLATFORMS.macos;
  const pres = new PptxGenJS();
  pres.defineLayout({ name: 'CUSTOM', width: dims.w, height: dims.h });
  pres.layout = 'CUSTOM';
  pres.title = content.title || 'Untitled Deck';
  pres.subject = content.subject || '';
  pres.author = content.author || '';
  pres.company = content.company || content.author || '';

  for (const slide of slides) {
    const slideTheme = applyThemeOverride(theme, slide);
    try {
      switch (slide.layout) {
        case 'cover':
          renderCover(pres, slide, slideTheme, dims);
          break;
        case 'content':
          renderContent(pres, slide, slideTheme, dims);
          break;
        case 'summary':
          renderSummary(pres, slide, slideTheme, dims);
          break;
        case 'section':
          await renderSection(pres, slide, slideTheme, dims);
          break;
        case 'two-column':
          await renderTwoColumn(pres, slide, slideTheme, dims);
          break;
        case 'data':
          await renderData(pres, slide, slideTheme, dims);
          break;
        case 'quote':
          await renderQuote(pres, slide, slideTheme, dims);
          break;
        case 'chart-bar':
          await renderChartBar(pres, slide, slideTheme, dims);
          break;
        case 'chart-line':
          await renderChartLine(pres, slide, slideTheme, dims);
          break;
        case 'chart-pie':
          await renderChartPie(pres, slide, slideTheme, dims);
          break;
        default:
          console.warn(`⚠️ 跳过 slide: 未知 layout '${slide.layout}'`);
      }
    } catch (err) {
      console.error(`❌ slide 渲染失败 (${slide.layout}): ${err.message}`);
      throw err;
    }
  }

  const outPath = opts.output || 'output.pptx';
  await pres.writeFile({ fileName: outPath });
  console.log(`✅ 已生成 ${outPath} (${slides.length} 张幻灯片, ${platform})`);
  return { outPath, slideCount: slides.length };
}

module.exports = { render, hardGate, parseArgs, VALID_PLATFORMS, USAGE };

if (require.main === module) {
  const args = parseArgs(process.argv);
  if (args.help) {
    console.log(USAGE);
    process.exit(0);
  }
  if (!args.file) {
    console.error('❌ 缺少 --file 参数\n' + USAGE);
    process.exit(1);
  }
  render(args).catch(err => {
    console.error(err.message || err);
    process.exit(1);
  });
}
