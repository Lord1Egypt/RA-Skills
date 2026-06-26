const test = require('node:test');
const assert = require('node:assert');
const { renderHTML } = require('../scripts/render');

test('replaces basic text tokens', () => {
  const html = '<h1>{{TITLE}}</h1><p>{{CONTENT}}</p>';
  const result = renderHTML(html, { title: 'Hello', content: 'World' }, {}, { width: 100, height: 100, id: 'test' });
  assert.ok(result.includes('<h1>Hello</h1>'));
  assert.ok(result.includes('<p>World</p>'));
});

test('replaces ACCENT__Axx to rgba', () => {
  const html = '<div style="background: {{ACCENT__A20}}"></div>';
  const result = renderHTML(html, {}, { colors: { accent: '#4F46E5' } }, { width: 100, height: 100, id: 'test' });
  assert.ok(result.includes('rgba(79,70,229,0.125'), `expected rgba with alpha 0.125, got: ${result}`);
});

test('handles missing tokens gracefully (leaves {{TOKEN}} as-is)', () => {
  const html = '<div>{{UNKNOWN}}</div>';
  const result = renderHTML(html, {}, {}, { width: 100, height: 100, id: 'test' });
  assert.ok(result.includes('{{UNKNOWN}}'), 'unknown tokens should be left untouched');
});
