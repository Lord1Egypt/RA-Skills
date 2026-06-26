'use strict';

const VALID_LAYOUTS = ['cover', 'section', 'content', 'two-column', 'data', 'quote', 'summary', 'chart-bar', 'chart-line', 'chart-pie'];

const REQUIRED_FIELDS = {
  'data':       ['metrics'],
  'two-column': ['leftPoints', 'rightPoints'],
  'quote':      ['quote', 'attribution'],
  'chart-bar':  ['chartData'],
  'chart-line': ['chartData'],
  'chart-pie':  ['chartData'],
};

function parseSlides(content) {
  if (!content || typeof content !== 'object') {
    throw new Error('content 必须是对象');
  }
  let slides;
  if (Array.isArray(content.slides) && content.slides.length > 0) {
    slides = content.slides;
  } else if (content.layout) {
    const { layout, title, body, subtitle, points, leftTitle, leftPoints, rightTitle, rightPoints, metrics, quote, attribution, closing, notes, background, chartType, chartData, themeOverride } = content;
    slides = [{ layout, title, body, subtitle, points, leftTitle, leftPoints, rightTitle, rightPoints, metrics, quote, attribution, closing, notes, background, chartType, chartData, themeOverride }];
  } else {
    throw new Error('content 缺少 slides 数组或单页 layout');
  }
  for (let i = 0; i < slides.length; i++) {
    const s = slides[i];
    if (!VALID_LAYOUTS.includes(s.layout)) {
      throw new Error(`slide #${i + 1}: layout '${s.layout}' 未知. 支持: ${VALID_LAYOUTS.join(', ')}`);
    }
    if (!s.title) {
      throw new Error(`slide #${i + 1}: 缺少 title 字段`);
    }
    const required = REQUIRED_FIELDS[s.layout];
    if (required) {
      for (const field of required) {
        const val = s[field];
        const isEmpty = val === undefined || val === null ||
          (Array.isArray(val) && val.length === 0) ||
          (typeof val === 'string' && val.trim() === '');
        if (isEmpty) {
          throw new Error(`slide #${i + 1} (${s.layout}): 缺少必填字段 '${field}'`);
        }
      }
    }
  }
  return {
    brand: content.brand,
    theme: content.theme,
    title: content.title || slides[0]?.title,
    author: content.author,
    company: content.company,
    date: content.date,
    logo: content.logo,
    slides,
  };
}

module.exports = { parseSlides, VALID_LAYOUTS, REQUIRED_FIELDS };
