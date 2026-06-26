'use strict';

const { addSlideFooter } = require('./slide-footer');
const { ptInch } = require('./units');
const { applyBackground } = require('./background');

const DEFAULT_DIMS = { w: 13.333, h: 7.5 };

function normalizeChartType(layout) {
  if (layout === 'chart-bar') return 'bar';
  if (layout === 'chart-line') return 'line';
  if (layout === 'chart-pie') return 'pie';
  return 'bar';
}

function buildChart(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const usableW = dims.w - ptInch(theme.spacing) * 2;

  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: ptInch(theme.spacing), w: usableW, h: 0.8,
    fontFace: theme.fontTitle, fontSize: theme.sizeH2,
    color: theme.text, bold: true, align: 'left',
  });

  const chartType = normalizeChartType(slide.layout);
  const data = slide.chartData || [];

  if (typeof s.addChart !== 'function' || data.length === 0) {
    s.addText('(no chart data)', {
      x: ptInch(theme.spacing), y: dims.h * 0.5, w: usableW, h: 0.6,
      fontFace: theme.fontBody, fontSize: theme.sizeBase,
      color: theme.secondary, align: 'center',
    });
    addSlideFooter(s, theme, dims, slide);
    return s;
  }

  s.addChart(chartType, data, {
    x: ptInch(theme.spacing), y: dims.h * 0.20,
    w: usableW, h: dims.h * 0.70,
    showLegend: true,
    legendPos: 'b',
    legendFontFace: theme.fontBody,
    legendFontSize: 10,
    legendColor: theme.text,
    catAxisLabelFontFace: theme.fontBody,
    catAxisLabelFontSize: 10,
    catAxisLabelColor: theme.text,
    valAxisLabelFontFace: theme.fontBody,
    valAxisLabelFontSize: 10,
    valAxisLabelColor: theme.textSecondary,
    chartColors: [theme.accent, theme.secondary, theme.text, theme.bgAlt],
  });

  addSlideFooter(s, theme, dims, slide);
  return s;
}

async function renderChartBar(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildChart(pres, slide, theme, dims);
}
async function renderChartLine(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildChart(pres, slide, theme, dims);
}
async function renderChartPie(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildChart(pres, slide, theme, dims);
}

module.exports = { renderChartBar, renderChartLine, renderChartPie, buildChart, normalizeChartType, DEFAULT_DIMS };
