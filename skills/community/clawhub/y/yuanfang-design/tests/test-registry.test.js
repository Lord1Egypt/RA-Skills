// Validates registry.json files match shadcn schema and reference real files.
// Prevents shipping a registry with dangling paths or missing themes.

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const SCHEMA = 'https://ui.shadcn.com/schema/registry.json';

function loadRegistry(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function checkRegistry(p) {
  const reg = loadRegistry(p);
  assert.strictEqual(reg['$schema'], SCHEMA, `${p}: $schema must point to shadcn registry schema`);
  if (reg.items) {
    for (const item of reg.items) {
      assert.ok(item.name, `${p}: item missing name`);
      assert.ok(item.type, `${p}: item ${item.name} missing type`);
      assert.ok(item.title, `${p}: item ${item.name} missing title`);
      assert.ok(item.description, `${p}: item ${item.name} missing description`);
      if (item.type === 'registry:theme' || item.type === 'registry:layout') {
        assert.ok(item.files && item.files.length > 0, `${p}: ${item.name} has no files`);
        for (const file of item.files) {
          const fullPath = path.join(ROOT, file.path);
          assert.ok(fs.existsSync(fullPath), `${p}: ${item.name} references missing file ${file.path}`);
        }
      }
    }
  }
  if (reg.include) {
    for (const inc of reg.include) {
      const fullPath = path.join(path.dirname(p), inc);
      assert.ok(fs.existsSync(fullPath), `${p}: include path ${inc} not found`);
    }
  }
}

test('root registry.json: schema + items + includes resolve', () => {
  const p = path.join(ROOT, 'registry.json');
  assert.ok(fs.existsSync(p), 'root registry.json must exist');
  checkRegistry(p);
});

test('themes/registry.json: all 12 themes have real files', () => {
  const p = path.join(ROOT, 'yuanfang-design', 'themes', 'registry.json');
  checkRegistry(p);
});

test('layout-types/registry.json: cover layout has real file', () => {
  const p = path.join(ROOT, 'yuanfang-design', 'layout-types', 'registry.json');
  checkRegistry(p);
});

test('registry item names are unique across all files', () => {
  const allNames = new Set();
  const files = [
    path.join(ROOT, 'registry.json'),
    path.join(ROOT, 'yuanfang-design', 'themes', 'registry.json'),
    path.join(ROOT, 'yuanfang-design', 'layout-types', 'registry.json'),
  ];
  for (const f of files) {
    if (!fs.existsSync(f)) continue;
    const reg = loadRegistry(f);
    if (!reg.items) continue;
    for (const item of reg.items) {
      assert.ok(!allNames.has(item.name), `duplicate item name: ${item.name}`);
      allNames.add(item.name);
    }
  }
});
