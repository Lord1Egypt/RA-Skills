#!/usr/bin/env node
'use strict';

/**
 * UI Template RUID Lookup — run this to get RUID values for UI elements.
 *
 * Usage:
 *   node ruid-lookup.js                    # list available styles
 *   node ruid-lookup.js --style 1          # dump all RUIDs for style 1
 *   node ruid-lookup.js --style 1 --role button   # filter by role keyword
 */

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const SKILL_DIR = path.dirname(SCRIPT_DIR);

const STYLES = {
  '1': { dir: 'style-1-black', pattern: 'Simple Popups (Black)' },
  '2': { dir: 'style-2-diary', pattern: 'Minimal HUD (Diary)' },
  '3': { dir: 'style-3-wood', pattern: 'Multi-Tab (Wood)' },
  '4': { dir: 'style-4-blue', pattern: 'Transaction Flow (Blue)' },
};

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { style: null, role: null };
  for (let i = 0; i < args.length; i++) {
    if ((args[i] === '--style' || args[i] === '-s') && args[i + 1]) {
      result.style = args[++i];
    } else if ((args[i] === '--role' || args[i] === '-r') && args[i + 1]) {
      result.role = args[++i];
    }
  }
  return result;
}

function extractRuids(styleDir) {
  const uiDir = path.join(SKILL_DIR, styleDir);
  const results = [];

  const files = fs.readdirSync(uiDir).filter(f => f.endsWith('.ui')).sort();
  for (const fname of files) {
    const data = JSON.parse(fs.readFileSync(path.join(uiDir, fname), 'utf8'));
    const entities = (data.ContentProto && data.ContentProto.Entities) || [];
    for (const ent of entities) {
      const js = ent.jsonString || {};
      const name = js.name || '';
      const comps = js['@components'] || [];
      for (const comp of comps) {
        const imageRuid = comp.ImageRUID;
        if (imageRuid && typeof imageRuid === 'object') {
          const did = imageRuid.DataId || '';
          if (did) {
            results.push({ file: fname, entity: name, ruid: did });
          }
        }
      }
    }
  }
  return results;
}

function classifyRole(entityName, fileName) {
  const n = entityName.toLowerCase();
  const f = fileName.toLowerCase();

  if (f.includes('toast')) return 'toast';
  if (f.includes('default')) return 'infrastructure';

  if (['btn', 'button', 'ok', 'cancel', 'close', 'exit'].some(k => n.includes(k))) return 'button';
  if (['slot', 'item', 'equip', 'inven'].some(k => n.includes(k))) return 'slot/item';
  if (n.includes('icon')) return 'icon';
  if (['panel', 'bg', 'popup', 'dim', 'paper'].some(k => n.includes(k))) return 'panel/background';
  if (['fill', 'gauge', 'bar', 'hp', 'mp', 'exp', 'progress'].some(k => n.includes(k))) return 'gauge/bar';
  if (['money', 'coin', 'meso', 'reward', 'gold'].some(k => n.includes(k))) return 'currency/reward';
  if (['title', 'deco', 'line', 'pattern', 'effect'].some(k => n.includes(k))) return 'decoration';
  if (['hud', 'match', 'timer', 'score'].some(k => n.includes(k))) return 'hud';

  return 'other';
}

function main() {
  const args = parseArgs();

  if (!args.style) {
    console.log('Available styles:');
    for (const [k, v] of Object.entries(STYLES)) {
      console.log(`  --style ${k}  →  ${v.dir}  (${v.pattern})`);
    }
    console.log('\nRoles: button, panel/background, slot/item, icon, gauge/bar, currency/reward, decoration, hud, toast');
    return;
  }

  if (!STYLES[args.style]) {
    console.error(`Error: style must be 1-4, got '${args.style}'`);
    process.exit(1);
  }

  const styleInfo = STYLES[args.style];
  const results = extractRuids(styleInfo.dir);

  const seen = new Map();
  for (const r of results) {
    const role = classifyRole(r.entity, r.file);
    const key = `${r.ruid}\0${role}`;
    if (!seen.has(key)) {
      seen.set(key, { ruid: r.ruid, role, entities: [] });
    }
    seen.get(key).entities.push(r.entity);
  }

  const grouped = {};
  for (const info of seen.values()) {
    if (!grouped[info.role]) grouped[info.role] = [];
    grouped[info.role].push(info);
  }

  const roleFilter = args.role ? args.role.toLowerCase() : null;

  console.log(`=== Style ${args.style}: ${styleInfo.pattern} (${styleInfo.dir}) ===\n`);

  for (const role of Object.keys(grouped).sort()) {
    if (roleFilter && !role.includes(roleFilter)) continue;
    const items = grouped[role];
    console.log(`[${role}]`);
    for (const item of items) {
      const unique = [...new Set(item.entities)];
      let entitiesStr = unique.slice(0, 4).sort().join(', ');
      if (unique.length > 4) entitiesStr += ` (+${unique.length - 4} more)`;
      console.log(`  ${item.ruid}  ←  ${entitiesStr}`);
    }
    console.log();
  }
}

main();
