const test = require('node:test');
const assert = require('node:assert');
const { renderChartBar, renderChartLine, renderChartPie, buildChart, normalizeChartType } = require('../../scripts/generator-charts');

const theme = {
  bg: '#ffffff', text: '#111111', textSecondary: '#666666',
  accent: '#4f46e5', secondary: '#64748b', bgAlt: '#f5f5f5',
  fontBody: 'system-ui', fontTitle: 'Georgia, serif',
  sizeH1: 60, sizeH2: 28, sizeBase: 18, sizeSm: 12,
  spacing: 12, rectRadius: 8,
};

function makeMockPresWithChart() {
  const calls = [];
  const slide = {
    addText: function(text, opts) { calls.push({ type: 'text', text, opts }); return this; },
    addShape: function() { return this; },
    addImage: function() { return this; },
    addNotes: function() { return this; },
    addChart: function(type, data, opts) { calls.push({ type: 'chart', chartType: type, data, opts }); return this; },
  };
  return { addSlide: () => slide, _calls: calls, _slide: slide };
}

test('normalizeChartType maps layouts to pptxgenjs chart names', () => {
  assert.strictEqual(normalizeChartType('chart-bar'), 'bar');
  assert.strictEqual(normalizeChartType('chart-line'), 'line');
  assert.strictEqual(normalizeChartType('chart-pie'), 'pie');
  assert.strictEqual(normalizeChartType('unknown'), 'bar');
});

test('buildChart emits a chart call with correct data and dimensions', () => {
  const pres = makeMockPresWithChart();
  const slide = {
    layout: 'chart-bar',
    title: 'Monthly Revenue',
    chartData: [
      { name: 'Revenue', labels: ['Jan', 'Feb', 'Mar'], values: [100, 150, 200] },
    ],
  };
  buildChart(pres, slide, theme, { w: 13.333, h: 7.5 });
  const chartCalls = pres._calls.filter(c => c.type === 'chart');
  assert.strictEqual(chartCalls.length, 1);
  assert.strictEqual(chartCalls[0].chartType, 'bar');
  assert.deepStrictEqual(chartCalls[0].data[0].labels, ['Jan', 'Feb', 'Mar']);
  assert.deepStrictEqual(chartCalls[0].data[0].values, [100, 150, 200]);
  assert.ok(chartCalls[0].opts.x !== undefined);
  assert.ok(chartCalls[0].opts.w > 0);
});

test('buildChart uses theme colors (accent, secondary, text) for chart palette', () => {
  const pres = makeMockPresWithChart();
  const slide = { layout: 'chart-bar', title: 'T', chartData: [{ name: 'X', labels: ['a'], values: [1] }] };
  buildChart(pres, slide, theme, { w: 13.333, h: 7.5 });
  const chartCall = pres._calls.find(c => c.type === 'chart');
  assert.ok(chartCall.opts.chartColors.includes(theme.accent));
  assert.ok(chartCall.opts.chartColors.includes(theme.secondary));
});

test('buildChart falls back to placeholder when no chartData', () => {
  const pres = makeMockPresWithChart();
  const slide = { layout: 'chart-bar', title: 'T' };
  buildChart(pres, slide, theme, { w: 13.333, h: 7.5 });
  const chartCalls = pres._calls.filter(c => c.type === 'chart');
  assert.strictEqual(chartCalls.length, 0);
  const texts = pres._calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.includes('(no chart data)'));
});

test('renderChartBar / renderChartLine / renderChartPie all map to correct types', async () => {
  for (const [fn, expected, layout] of [
    [renderChartBar, 'bar', 'chart-bar'],
    [renderChartLine, 'line', 'chart-line'],
    [renderChartPie, 'pie', 'chart-pie'],
  ]) {
    const pres = makeMockPresWithChart();
    const slide = {
      layout,
      title: 'T',
      chartData: [{ name: 'X', labels: ['a', 'b'], values: [1, 2] }],
    };
    await fn(pres, slide, theme, { w: 13.333, h: 7.5 });
    const chartCall = pres._calls.find(c => c.type === 'chart');
    assert.ok(chartCall, `${fn.name} should emit a chart call`);
    assert.strictEqual(chartCall.chartType, expected);
  }
});

test('parseSlides accepts chart-bar/chart-line/chart-pie layouts', () => {
  const { parseSlides } = require('../../scripts/parse-slides');
  const result = parseSlides({
    brand: 'x', theme: 'x',
    slides: [
      { layout: 'chart-bar', title: 'T', chartData: [{ name: 'X', labels: ['a'], values: [1] }] },
      { layout: 'chart-line', title: 'T2', chartData: [{ name: 'X', labels: ['a'], values: [1] }] },
      { layout: 'chart-pie', title: 'T3', chartData: [{ name: 'X', labels: ['a'], values: [1] }] },
    ],
  });
  assert.strictEqual(result.slides.length, 3);
  assert.strictEqual(result.slides[0].layout, 'chart-bar');
  assert.strictEqual(result.slides[1].layout, 'chart-line');
  assert.strictEqual(result.slides[2].layout, 'chart-pie');
});

test('parseSlides rejects chart-bar without chartData', () => {
  const { parseSlides } = require('../../scripts/parse-slides');
  assert.throws(() => parseSlides({
    brand: 'x', theme: 'x',
    slides: [{ layout: 'chart-bar', title: 'T' }],
  }), /缺少必填字段 'chartData'/);
});
