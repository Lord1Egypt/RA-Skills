#!/usr/bin/env node
'use strict';

/**
 * UI Template Structure Viewer — shows entity hierarchy, layout, and key properties.
 *
 * Usage:
 *   node ui-structure.js --style 1                          # show all .ui files in style
 *   node ui-structure.js --style 1 --file ButtonGroup.ui    # show specific file
 *   node ui-structure.js --style 1 --file PopupGroup.ui --depth 2   # limit hierarchy depth
 *   node ui-structure.js --style 1 --entity BasicPopup      # dump full JSON for entity
 *   node ui-structure.js --style 1 --grep ExitButton        # search entity name across all files
 */

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const SKILL_DIR = path.dirname(SCRIPT_DIR);

const STYLES = {
  '1': 'style-1-black',
  '2': 'style-2-diary',
  '3': 'style-3-wood',
  '4': 'style-4-blue',
};

function parseArgs() {
  const argv = process.argv.slice(2);
  const result = { style: null, file: null, depth: null, entity: null, grep: null };
  for (let i = 0; i < argv.length; i++) {
    if ((argv[i] === '--style' || argv[i] === '-s') && argv[i + 1]) {
      result.style = argv[++i];
    } else if ((argv[i] === '--file' || argv[i] === '-f') && argv[i + 1]) {
      result.file = argv[++i];
    } else if ((argv[i] === '--depth' || argv[i] === '-d') && argv[i + 1]) {
      result.depth = parseInt(argv[++i], 10);
    } else if ((argv[i] === '--entity' || argv[i] === '-e') && argv[i + 1]) {
      result.entity = argv[++i];
    } else if ((argv[i] === '--grep' || argv[i] === '-g') && argv[i + 1]) {
      result.grep = argv[++i];
    }
  }
  return result;
}

function getAlignmentName(val) {
  const names = {
    0: 'Center', 1: 'Left', 2: 'Right',
    3: 'TopCenter', 4: 'TopLeft', 5: 'TopRight',
    6: 'BottomCenter', 7: 'BottomLeft', 8: 'BottomRight',
    9: 'HStretchTop', 10: 'HStretchCenter', 11: 'HStretchBottom',
    12: 'VStretchLeft', 13: 'VStretchCenter', 14: 'VStretchRight',
    15: 'StretchAll',
  };
  return names[val] || String(val);
}

function summarizeEntity(js) {
  const info = {};
  info.name = js.name || '?';
  info.enable = js.enable !== undefined ? js.enable : true;
  info.displayOrder = js.displayOrder || 0;

  const comps = js['@components'] || [];
  const compTypes = [];

  for (const comp of comps) {
    let t = (comp['@type'] || '').replace('MOD.Core.', '');
    compTypes.push(t);

    if (t === 'UITransformComponent') {
      const align = comp.AlignmentOption || 0;
      info.align = getAlignmentName(align);
      const pos = comp.anchoredPosition || {};
      info.pos = `(${Math.round(pos.x || 0)}, ${Math.round(pos.y || 0)})`;
      const size = comp.RectSize || {};
      info.size = `${Math.round(size.x || 0)}x${Math.round(size.y || 0)}`;
    } else if (t === 'UIGroupComponent') {
      info.groupOrder = comp.GroupOrder || 0;
      info.defaultShow = comp.DefaultShow !== undefined ? comp.DefaultShow : true;
    } else if (t === 'ButtonComponent') {
      compTypes[compTypes.length - 1] = 'Button';
    } else if (t === 'TextComponent') {
      const text = comp.Text || '';
      if (text) info.text = text.slice(0, 30);
    } else if (t === 'ScrollLayoutGroupComponent') {
      compTypes[compTypes.length - 1] = 'ScrollLayout';
    }
  }

  info.components = compTypes.filter(c => c !== 'UITransformComponent');
  return info;
}

function printTree(entities, maxDepth) {
  const sorted = entities.slice().sort((a, b) => {
    const aJs = a.jsonString || {};
    const bJs = b.jsonString || {};
    const pathCmp = (aJs.path || '').localeCompare(bJs.path || '');
    if (pathCmp !== 0) return pathCmp;
    return (aJs.displayOrder || 0) - (bJs.displayOrder || 0);
  });

  for (const ent of sorted) {
    const js = ent.jsonString || {};
    const entPath = js.path || '';

    const depth = (entPath.match(/\//g) || []).length - 2;
    if (maxDepth !== null && depth > maxDepth) continue;

    const indent = '  '.repeat(Math.max(0, depth));
    const info = summarizeEntity(js);

    const parts = [info.name];

    if (info.groupOrder !== undefined) parts.push(`GroupOrder=${info.groupOrder}`);
    if (info.defaultShow === false) parts.push('hidden');

    if (info.align) parts.push(info.align);
    if (info.pos && info.pos !== '(0, 0)') parts.push(info.pos);
    if (info.size && info.size !== '0x0') parts.push(info.size);

    const notableComps = (info.components || []).filter(
      c => c !== 'CanvasGroupComponent' && c !== 'SpriteGUIRendererComponent'
    );
    if (notableComps.length) parts.push(`[${notableComps.join(', ')}]`);

    if (info.text) parts.push(`"${info.text}"`);
    if (!info.enable) parts.push('(disabled)');

    console.log(`${indent}${parts.join(' | ')}`);
  }
}

function findEntity(styleDir, entityName, targetFile) {
  const files = targetFile
    ? [targetFile]
    : fs.readdirSync(styleDir).filter(f => f.endsWith('.ui')).sort();
  let found = false;

  for (const fname of files) {
    const filepath = path.join(styleDir, fname);
    if (!fs.existsSync(filepath)) continue;
    const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    const entities = (data.ContentProto && data.ContentProto.Entities) || [];

    for (const ent of entities) {
      const js = ent.jsonString || {};
      const name = js.name || '';
      if (name.toLowerCase() === entityName.toLowerCase()) {
        found = true;
        console.log(`\n--- ${fname} / ${js.path || ''} ---`);
        console.log(JSON.stringify(ent, null, 2));
      }
    }
  }

  if (!found) {
    console.log(`Entity '${entityName}' not found.`);
    console.log('Tip: use --grep to search partial names.');
  }
}

function grepEntities(styleDir, keyword, targetFile) {
  const files = targetFile
    ? [targetFile]
    : fs.readdirSync(styleDir).filter(f => f.endsWith('.ui')).sort();
  const results = [];

  for (const fname of files) {
    const filepath = path.join(styleDir, fname);
    if (!fs.existsSync(filepath)) continue;
    const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    const entities = (data.ContentProto && data.ContentProto.Entities) || [];

    for (const ent of entities) {
      const js = ent.jsonString || {};
      const name = js.name || '';
      const entPath = js.path || '';
      if (name.toLowerCase().includes(keyword.toLowerCase()) ||
          entPath.toLowerCase().includes(keyword.toLowerCase())) {
        const info = summarizeEntity(js);
        results.push({ file: fname, path: entPath, info });
      }
    }
  }

  if (!results.length) {
    console.log(`No entities matching '${keyword}' found.`);
    return;
  }

  console.log(`Found ${results.length} entities matching '${keyword}':\n`);
  for (const { file, path: p, info } of results) {
    const parts = [info.name];
    if (info.align) parts.push(info.align);
    if (info.size && info.size !== '0x0') parts.push(info.size);
    const notable = (info.components || []).filter(
      c => c !== 'CanvasGroupComponent' && c !== 'SpriteGUIRendererComponent'
    );
    if (notable.length) parts.push(`[${notable.join(', ')}]`);
    if (!info.enable) parts.push('(disabled)');
    console.log(`  ${file}  ${p}`);
    console.log(`    ${parts.join(' | ')}`);
  }
  console.log(`\nUse --entity <name> to dump full JSON for a specific entity.`);
}

function processFile(filepath, maxDepth) {
  const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
  const filename = path.basename(filepath);
  const entities = (data.ContentProto && data.ContentProto.Entities) || [];
  console.log(`\n${'='.repeat(60)}`);
  console.log(`  ${filename}  (${entities.length} entities)`);
  console.log(`${'='.repeat(60)}`);
  printTree(entities, maxDepth);
}

function main() {
  const args = parseArgs();

  if (!args.style) {
    console.error("Error: --style is required. Use --style 1-4.");
    process.exit(1);
  }

  if (!STYLES[args.style]) {
    console.error(`Error: style must be 1-4, got '${args.style}'`);
    process.exit(1);
  }

  const styleDir = path.join(SKILL_DIR, STYLES[args.style]);

  if (args.entity) {
    findEntity(styleDir, args.entity, args.file);
    return;
  }

  if (args.grep) {
    grepEntities(styleDir, args.grep, args.file);
    return;
  }

  if (args.file) {
    const filepath = path.join(styleDir, args.file);
    if (!fs.existsSync(filepath)) {
      console.error(`Error: ${filepath} not found`);
      const available = fs.readdirSync(styleDir).filter(f => f.endsWith('.ui'));
      console.error(`Available: ${available.join(', ')}`);
      process.exit(1);
    }
    processFile(filepath, args.depth);
  } else {
    const files = fs.readdirSync(styleDir).filter(f => f.endsWith('.ui')).sort();
    for (const fname of files) {
      processFile(path.join(styleDir, fname), args.depth);
    }
  }
}

main();
