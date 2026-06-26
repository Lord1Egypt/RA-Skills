#!/usr/bin/env node
/**
 * Smart Agent Memory — CLI
 *
 * Usage:
 *   node memory-cli.js index                                    ← compact memory index (read FIRST)
 *   node memory-cli.js context [--tag x] [--skill x] [--days 7] ← load scoped context on demand
 *   node memory-cli.js skill-mem <skill-name>                   ← get skill experience memory
 *   node memory-cli.js remember <content> [--tags tag1,tag2] [--source conversation] [--skill name]
 *   node memory-cli.js recall <query> [--limit 10] [--tags tag1]
 *   node memory-cli.js forget <id>
 *   node memory-cli.js facts [--tags tag1] [--limit 50]
 *   node memory-cli.js learn --action "..." --context "..." --outcome positive --insight "..."
 *   node memory-cli.js lessons [--context topic] [--outcome positive|negative]
 *   node memory-cli.js entity <name> <type> [--attr key=value ...]
 *   node memory-cli.js entities [--type person]
 *   node memory-cli.js gc [--days 30]
 *   node memory-cli.js reflect
 *   node memory-cli.js extract <lesson-id> [--skill-name my-skill]
 *   node memory-cli.js stats
 *   node memory-cli.js search <query>
 *   node memory-cli.js export
 *   node memory-cli.js temperature
 */

'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { createStore } = require('../lib/store');
const { runGC, getTemperatureReport } = require('../lib/temperature');
const { searchFiles, smartSearch } = require('../lib/search');
const { extractSkill } = require('../lib/extract');
const cn = require('../lib/cn-optimize');

// ── Config ──────────────────────────────────────────────────────────────────
const MEMORY_DIR = process.env.MEMORY_DIR ||
  path.join(os.homedir(), '.openclaw', 'workspace', 'memory');

const { store, backend } = createStore(MEMORY_DIR);

// ── CLI Parsing ─────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const cmd = args[0];
const flag = (name) => args.includes(name);
const flagVal = (name, def) => {
  const i = args.indexOf(name);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
};
const flagInt = (name, def) => {
  const v = flagVal(name);
  return v !== undefined ? parseInt(v, 10) : def;
};

// Extract positional args (skip flags and their values)
const FLAGS_WITH_VALUES = ['--tags', '--limit', '--tag', '--skill', '--entity-type', '--days',
  '--context', '--outcome', '--action', '--insight', '--source', '--skill-name', '--attr'];
function positionalArgs(startIndex = 1) {
  const result = [];
  for (let i = startIndex; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      if (FLAGS_WITH_VALUES.includes(args[i])) i++; // skip value too
      continue;
    }
    result.push(args[i]);
  }
  return result;
}

// ── Colors ──────────────────────────────────────────────────────────────────
const c = {
  green: s => `\x1b[32m${s}\x1b[0m`,
  yellow: s => `\x1b[33m${s}\x1b[0m`,
  red: s => `\x1b[31m${s}\x1b[0m`,
  cyan: s => `\x1b[36m${s}\x1b[0m`,
  dim: s => `\x1b[2m${s}\x1b[0m`,
  bold: s => `\x1b[1m${s}\x1b[0m`,
};

// ── Commands ────────────────────────────────────────────────────────────────
function main() {
  switch (cmd) {

    // ── Layered Context Commands (OpenViking-inspired) ─────────────────
    case 'index': {
      const idx = store.memoryIndex();
      console.log(JSON.stringify(idx, null, 2));
      break;
    }

    case 'context': {
      const tag = flagVal('--tag');
      const skill = flagVal('--skill');
      const entityType = flagVal('--entity-type');
      const days = flagInt('--days');
      const limit = flagInt('--limit', 20);
      if (!tag && !skill && !entityType && !days) {
        return usage('context [--tag <tag>] [--skill <name>] [--entity-type <type>] [--days <n>] [--limit 20]');
      }
      const ctx = store.loadContext({ tag, skill, entityType, days, limit });
      if (ctx.skillMemory) {
        console.log(`\n${c.cyan('=== Skill Experience Memory ===')}\n`);
        console.log(ctx.skillMemory);
      }
      if (ctx.facts.length) {
        console.log(`\n${c.cyan('=== Facts')} (${ctx.facts.length}) ===\n`);
        for (const f of ctx.facts) {
          console.log(`  ${c.bold(f.id)} ${f.content}`);
          if (f.tags.length) console.log(`    ${c.dim(f.tags.join(', '))}`);
        }
      }
      if (ctx.lessons.length) {
        console.log(`\n${c.cyan('=== Lessons')} (${ctx.lessons.length}) ===\n`);
        for (const l of ctx.lessons) {
          const icon = l.outcome === 'positive' ? '✅' : l.outcome === 'negative' ? '❌' : '➖';
          console.log(`  ${icon} ${c.bold(l.id)} ${l.action}`);
          console.log(`    ${c.dim(l.insight)}`);
        }
      }
      if (ctx.entities.length) {
        console.log(`\n${c.cyan('=== Entities')} (${ctx.entities.length}) ===\n`);
        for (const e of ctx.entities) {
          console.log(`  ${c.bold(e.name)} [${e.entityType}]`);
        }
      }
      if (!ctx.facts.length && !ctx.lessons.length && !ctx.entities.length && !ctx.skillMemory) {
        console.log(c.yellow('No matching context found.'));
      }
      break;
    }

    case 'skill-mem': {
      const skillName = args[1];
      if (!skillName) return usage('skill-mem <skill-name>');
      const mem = store.getSkillMemory(skillName);
      if (mem) {
        console.log(mem);
      } else {
        console.log(c.yellow(`No experience memory for skill "${skillName}".`));
        console.log(c.dim('Record one with: remember "lesson learned" --skill ' + skillName));
      }
      break;
    }

    case 'skill-list': {
      const mems = store.listSkillMemories();
      if (mems.length === 0) {
        console.log(c.yellow('No skill experience memories yet.'));
      } else {
        console.log(`\n${c.cyan('Skill Experience Memories')} (${mems.length}):\n`);
        for (const m of mems) {
          console.log(`  📦 ${c.bold(m.skill)} — ${m.entries} entries, updated ${m.lastModified}`);
        }
      }
      break;
    }

    case 'remember': {
      const content = positionalArgs().join(' ');
      if (!content) return usage('remember <content> [--tags t1,t2] [--source conversation] [--confidence 1.0]');
      const tags = flagVal('--tags', '').split(',').filter(Boolean);
      const source = flagVal('--source', 'conversation');
      const confidence = parseFloat(flagVal('--confidence', '1.0'));
      const skill = flagVal('--skill');
      const fact = store.remember(content, { tags, source, confidence, skill });
      console.log(`${c.green('✓')} Remembered: ${c.bold(fact.id)}`);
      console.log(`  "${content}"`);
      if (tags.length) console.log(`  Tags: ${tags.join(', ')}`);
      break;
    }

    case 'recall': {
      const query = positionalArgs().join(' ');
      if (!query) return usage('recall <query> [--limit 10]');
      const limit = flagInt('--limit', 10);
      const results = store.recall(query, { limit });
      if (results.length === 0) {
        console.log(c.yellow('No matching facts found.'));
      } else {
        console.log(`${c.cyan('Found')} ${results.length} fact(s):\n`);
        for (const f of results) {
          const age = Math.floor((Date.now() - new Date(f.createdAt).getTime()) / 86400000);
          console.log(`  ${c.bold(f.id)} ${c.dim(`(${age}d ago, ${f.accessCount}x accessed)`)}`);
          console.log(`    ${f.content}`);
          if (f.tags.length) console.log(`    ${c.dim('Tags: ' + f.tags.join(', '))}`);
        }
      }
      break;
    }

    case 'forget': {
      const id = args[1];
      if (!id) return usage('forget <fact-id>');
      if (store.forget(id)) console.log(`${c.green('✓')} Fact ${id} forgotten.`);
      else console.log(c.red(`Fact ${id} not found.`));
      break;
    }

    case 'facts': {
      const tags = flagVal('--tags', '').split(',').filter(Boolean);
      const limit = flagInt('--limit', 50);
      const facts = store.listFacts({ tags: tags.length ? tags : null, limit });
      if (facts.length === 0) {
        console.log(c.yellow('No facts stored.'));
      } else {
        console.log(`${c.cyan('Facts')} (${facts.length}):\n`);
        for (const f of facts) {
          console.log(`  ${c.bold(f.id)} ${f.content}`);
          if (f.tags.length) console.log(`    ${c.dim(f.tags.join(', '))}`);
        }
      }
      break;
    }

    case 'learn': {
      const action = flagVal('--action');
      const context = flagVal('--context');
      const outcome = flagVal('--outcome');
      const insight = flagVal('--insight');
      if (!action || !context || !outcome || !insight) {
        return usage('learn --action "..." --context "..." --outcome positive|negative|neutral --insight "..."');
      }
      const lesson = store.learn(action, context, outcome, insight);
      console.log(`${c.green('✓')} Lesson recorded: ${c.bold(lesson.id)}`);
      console.log(`  Action:  ${action}`);
      console.log(`  Context: ${context}`);
      console.log(`  Outcome: ${outcome}`);
      console.log(`  Insight: ${insight}`);
      break;
    }

    case 'lessons': {
      const context = flagVal('--context');
      const outcome = flagVal('--outcome');
      const limit = flagInt('--limit', 10);
      const lessons = store.getLessons({ context, outcome, limit });
      if (lessons.length === 0) {
        console.log(c.yellow('No lessons found.'));
      } else {
        console.log(`${c.cyan('Lessons')} (${lessons.length}):\n`);
        for (const l of lessons) {
          const icon = l.outcome === 'positive' ? '✅' : l.outcome === 'negative' ? '❌' : '➖';
          console.log(`  ${icon} ${c.bold(l.id)} ${l.action}`);
          console.log(`    Context: ${l.context} | Applied: ${l.appliedCount}x`);
          console.log(`    ${c.dim(l.insight)}`);
        }
      }
      break;
    }

    case 'entity': {
      const name = args[1];
      const type = args[2];
      if (!name || !type) return usage('entity <name> <type> [--attr key=value ...]');
      const attrs = {};
      for (let i = 3; i < args.length; i++) {
        if (args[i] === '--attr' && args[i + 1]) {
          const [k, ...v] = args[i + 1].split('=');
          if (k) attrs[k] = v.join('=');
          i++;
        }
      }
      const entity = store.trackEntity(name, type, attrs);
      console.log(`${c.green('✓')} Entity tracked: ${c.bold(name)} (${type})`);
      if (Object.keys(attrs).length) {
        for (const [k, v] of Object.entries(attrs)) {
          console.log(`  ${k}: ${v}`);
        }
      }
      break;
    }

    case 'entities': {
      const type = flagVal('--type');
      const entities = store.listEntities(type);
      if (entities.length === 0) {
        console.log(c.yellow('No entities tracked.'));
      } else {
        console.log(`${c.cyan('Entities')} (${entities.length}):\n`);
        for (const e of entities) {
          console.log(`  ${c.bold(e.name)} [${e.entityType}] ${c.dim('since ' + e.firstSeen.slice(0, 10))}`);
          for (const [k, v] of Object.entries(e.attributes)) {
            console.log(`    ${k}: ${v}`);
          }
        }
      }
      break;
    }

    case 'gc': {
      const days = flagInt('--days', 30);
      console.log(`🗑️  Running GC (archiving files older than ${days} days)...\n`);

      // Archive daily logs
      const { archived, stats } = runGC(MEMORY_DIR);
      // Forget stale facts
      const removedFacts = store.forgetStale({ days });

      // Update index
      store.index.lastGC = new Date().toISOString();
      store._saveIndex();

      console.log(`Temperature distribution:`);
      console.log(`  🔥 Hot:  ${stats.hot} files`);
      console.log(`  🟡 Warm: ${stats.warm} files`);
      console.log(`  ❄️ Cold: ${stats.cold} files`);
      console.log('');
      if (archived.length > 0) {
        console.log(`${c.green('✓')} Archived ${archived.length} file(s):`);
        for (const f of archived) console.log(`  → ${f}`);
      } else {
        console.log(c.dim('No files to archive.'));
      }
      if (removedFacts > 0) {
        console.log(`${c.green('✓')} Removed ${removedFacts} stale fact(s) from JSON store.`);
      }
      break;
    }

    case 'reflect': {
      console.log('🌙 Nightly Reflection...\n');

      const s = store.stats();
      const now = new Date().toISOString();
      const today = now.slice(0, 10);

      // Gather richer analysis
      const idx = store.memoryIndex ? store.memoryIndex() : null;
      const topTags = idx ? idx.topTags.slice(0, 10).join(', ') : '(N/A)';
      const recentFactCount = idx ? idx.recentFacts.length : 0;
      const newEntities = idx ? idx.entitySummary.slice(0, 5).join(', ') : '(N/A)';
      const skillMems = idx ? idx.skillMemories : [];
      const recentLessons = idx ? idx.recentLessons : [];

      // Write reflection
      const reflectionDir = path.join(MEMORY_DIR, 'reflections');
      if (!fs.existsSync(reflectionDir)) fs.mkdirSync(reflectionDir, { recursive: true });
      const reflectionFile = path.join(reflectionDir, `${today}.md`);

      const sections = [
        `# Reflection — ${today}`,
        '',
        `## Memory Health`,
        `- Facts: ${s.facts.active} active (🔥${s.facts.hot} 🟡${s.facts.warm} ❄️${s.facts.cold})`,
        `- Lessons: ${s.lessons}`,
        `- Entities: ${s.entities}`,
        `- Skill memories: ${skillMems.length}`,
        `- Archived files: ${s.archived}`,
        '',
        `## Recent Activity (3 days)`,
        `- New facts: ${recentFactCount}`,
        `- Top tags: ${topTags}`,
        '',
        `## Entities`,
        `- Recent: ${newEntities}`,
        '',
        `## Skill Experience`,
        ...(skillMems.length > 0
          ? skillMems.map(sm => `- **${sm.skill}**: ${sm.entries} entries (last: ${sm.lastModified})`)
          : ['- _(none)_']),
        '',
        `## Recent Lessons`,
        ...(recentLessons.length > 0
          ? recentLessons.map(l => `- [${l.outcome}] ${l.action}`)
          : ['- _(none)_']),
        '',
        `## Notes`,
        '_(Add reflections here)_',
      ];
      fs.writeFileSync(reflectionFile, sections.join('\n'));

      store.index.lastReflection = now;
      store._saveIndex();

      console.log(`${c.green('✓')} Reflection saved: reflections/${today}.md`);
      console.log('');
      console.log('Memory Health:');
      console.log(`  Facts:    ${s.facts.active} active (🔥${s.facts.hot} hot, 🟡${s.facts.warm} warm, ❄️${s.facts.cold} cold)`);
      console.log(`  Lessons:  ${s.lessons}`);
      console.log(`  Entities: ${s.entities}`);
      console.log(`  Skills:   ${skillMems.length} with experience`);
      console.log(`  Archived: ${s.archived} files`);
      if (recentFactCount > 0) console.log(`  Recent:   ${recentFactCount} facts in last 3 days`);
      if (topTags !== '(N/A)') console.log(`  Top tags: ${topTags}`);
      break;
    }

    case 'extract': {
      const lessonId = args[1];
      const skillName = flagVal('--skill-name', lessonId ? `lesson-${lessonId}` : null);
      if (!lessonId) return usage('extract <lesson-id> [--skill-name my-skill]');

      // Support both JSON store (.lessons array) and SQLite store (getLessons method)
      const allLessons = store.lessons || store.getLessons({ limit: 9999 });
      const lesson = allLessons.find(l => l.id === lessonId);
      if (!lesson) return console.log(c.red(`Lesson ${lessonId} not found.`));

      const skillDir = path.join(os.homedir(), '.openclaw', 'skills', skillName);
      const outFile = extractSkill(lesson, skillDir, skillName);
      console.log(`${c.green('✓')} Skill extracted: ${outFile}`);
      console.log(`  From lesson: ${lesson.action}`);
      break;
    }

    case 'stats': {
      const s = store.stats();
      console.log('');
      console.log(`🧠 Smart Agent Memory — Stats ${c.dim(`[${backend}]`)}`);
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('');
      console.log('Facts:');
      console.log(`  Total:      ${s.facts.total}`);
      console.log(`  Active:     ${s.facts.active}`);
      console.log(`  🔥 Hot:     ${s.facts.hot} (< 7 days)`);
      console.log(`  🟡 Warm:    ${s.facts.warm} (7-30 days)`);
      console.log(`  ❄️ Cold:    ${s.facts.cold} (> 30 days)`);
      console.log('');
      console.log(`Lessons:      ${s.lessons}`);
      console.log(`Entities:     ${s.entities}`);
      console.log(`Archived:     ${s.archived} files`);
      console.log('');
      if (s.lastGC) console.log(`Last GC:         ${s.lastGC.slice(0, 16).replace('T', ' ')}`);
      if (s.lastReflection) console.log(`Last Reflection: ${s.lastReflection.slice(0, 16).replace('T', ' ')}`);
      console.log('');
      break;
    }

    case 'search': {
      const query = positionalArgs().join(' ');
      if (!query) return usage('search <query>');
      const limit = flagInt('--limit', 20);
      const results = smartSearch(MEMORY_DIR, query, { limit });
      if (results.length === 0) {
        console.log(c.yellow('No matches found in Markdown files.'));
      } else {
        console.log(`${c.cyan('Found')} matches in ${results.length} file(s):\n`);
        for (const r of results) {
          console.log(`  📄 ${c.bold(r.file)} ${c.dim(`(score: ${r.score})`)}`);
          for (const m of r.matches) {
            console.log(`    L${m.line}: ${m.content.slice(0, 120)}`);
          }
        }
      }
      break;
    }

    case 'temperature': {
      const report = getTemperatureReport(MEMORY_DIR);
      console.log('');
      console.log('🌡️  Temperature Report');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`\n🔥 Hot (${report.hot.length}):`);
      for (const f of report.hot) console.log(`  ${f}`);
      console.log(`\n🟡 Warm (${report.warm.length}):`);
      for (const f of report.warm) console.log(`  ${f}`);
      console.log(`\n❄️ Cold (${report.cold.length}):`);
      for (const f of report.cold) console.log(`  ${f}`);
      console.log('');
      break;
    }

    case 'export': {
      const data = store.exportJson();
      console.log(JSON.stringify(data, null, 2));
      break;
    }

    // ── Session Lifecycle (simulate mem9 hooks) ───────────────────────
    case 'session-start': {
      // Simulates mem9's before_prompt_build: load index + recent context
      console.log('📥 Session Start — Loading memory context...\n');
      const idx = store.memoryIndex();
      const { overview, topTags, recentFacts, recentLessons, skillMemories } = idx;

      console.log(`Memory: ${overview.facts} facts (🔥${overview.hot} 🟡${overview.warm} ❄️${overview.cold}) | ${overview.lessons} lessons | ${overview.entities} entities`);
      if (topTags.length) console.log(`Tags: ${topTags.slice(0, 8).join(', ')}`);
      if (recentFacts.length) {
        console.log(`\nRecent (${recentFacts.length}):`);
        for (const f of recentFacts.slice(0, 5)) {
          console.log(`  • ${f.preview}${f.tags.length ? ' ' + c.dim(f.tags.join(', ')) : ''}`);
        }
      }
      if (recentLessons.length) {
        console.log(`\nLessons:`);
        for (const l of recentLessons.slice(0, 3)) {
          console.log(`  • [${l.outcome}] ${l.action}`);
        }
      }
      if (skillMemories.length) {
        console.log(`\nSkill experience: ${skillMemories.map(s => s.skill).join(', ')}`);
      }

      // Also output JSON for programmatic use
      if (flag('--json')) {
        console.log('\n---JSON---');
        console.log(JSON.stringify(idx, null, 2));
      }
      break;
    }

    case 'session-end': {
      // Simulates mem9's before_reset + agent_end: save session summary
      const summary = positionalArgs().join(' ');
      if (!summary) return usage('session-end <session summary text>');

      console.log('📤 Session End — Saving summary...\n');
      const fact = store.remember(summary, {
        tags: ['session-summary', `date:${new Date().toISOString().slice(0, 10)}`],
        source: 'session-end',
      });
      console.log(`${c.green('✓')} Session summary saved: ${c.bold(fact.id)}`);
      console.log(`  "${summary.slice(0, 100)}${summary.length > 100 ? '...' : ''}"`);
      break;
    }

    // ── Chinese Optimization (memory-cn) ─────────────────────────────────
    case 'diagnose': {
      console.log('🔍 Running memory diagnostic...\n');
      const report = cn.diagnose(MEMORY_DIR);
      console.log(`${c.cyan('=== Diagnostic Report ===')}`);
      console.log(`Total files: ${report.totalFiles}`);
      console.log(`Files with tags: ${report.filesWithTags} (${report.tagsCoverage}%)`);
      console.log(`Lessons health: ${report.lessonsHealth}%`);
      console.log('');
      if (report.fts5Bug) {
        console.log(c.yellow('⚠️ FTS5 Chinese tokenization bug detected!'));
      } else {
        console.log(c.green('✓ FTS5 Chinese tokenization: OK'));
      }
      if (report.issues.length > 0) {
        console.log(c.yellow('\nIssues found:'));
        for (const issue of report.issues) {
          console.log(`  - ${issue}`);
        }
      } else {
        console.log(c.green('\n✓ No issues found'));
      }
      break;
    }

    case 'optimize-tags': {
      console.log('🏷️ Optimizing tags (adding spaces between Chinese characters)...\n');
      const results = cn.optimizeAllTags(MEMORY_DIR);
      console.log(`Processed: ${results.processed} files`);
      console.log(c.green(`Updated: ${results.updated} files`));
      if (results.errors.length > 0) {
        console.log(c.red('Errors:'));
        for (const err of results.errors) {
          console.log(`  - ${err}`);
        }
      }
      break;
    }

    case 'compress': {
      const maxKB = flagInt('--max-kb', 5);
      console.log(`🗜️ Compressing logs (max ${maxKB}KB)...\n`);
      const results = cn.compressLogs(MEMORY_DIR, maxKB);
      console.log(`Processed: ${results.processed} files`);
      console.log(c.green(`Compressed: ${results.compressed} files`));
      if (results.archived.length > 0) {
        console.log(c.cyan('\nArchived:'));
        for (const a of results.archived) {
          console.log(`  → ${a}`);
        }
      }
      break;
    }

    case 'optimize-search': {
      console.log('⚙️ Generating optimized search config...\n');
      const config = cn.getOptimizedSearchConfig();
      console.log(c.cyan('Optimized memorySearch config:'));
      console.log(JSON.stringify(config, null, 2));
      console.log(c.dim('\nUse with: gateway config.patch'));
      break;
    }

    case 'optimize-flush': {
      console.log('📝 Generating optimized memoryFlush prompt...\n');
      const prompt = cn.getOptimizedMemoryFlushPrompt();
      console.log(c.cyan('Optimized memoryFlush prompt:'));
      console.log(prompt.prompt);
      console.log(c.dim('\nUse with: gateway config.patch'));
      break;
    }

    default:
      console.log(`
🧠 Smart Agent Memory v2.0.0 + CN Optimizer
   Cross-platform memory system for OpenClaw agents

Commands:
  ${c.bold('index')}                                   ${c.cyan('★')} Compact memory index (read FIRST, saves tokens)
  ${c.bold('context')}  [--tag x] [--skill x] [--days n]  ${c.cyan('★')} Load scoped context on demand
  ${c.bold('skill-mem')} <skill-name>                  ${c.cyan('★')} Get skill experience memory
  ${c.bold('skill-list')}                              ${c.cyan('★')} List all skill experience memories
  ${c.bold('remember')} <content> [--tags t1,t2] [--skill name]  Store a fact (with optional skill tag)
  ${c.bold('recall')}   <query> [--limit 10]          Search facts
  ${c.bold('forget')}   <id>                          Delete a fact
  ${c.bold('facts')}    [--tags t1] [--limit 50]      List all facts
  ${c.bold('learn')}    --action --context --outcome --insight   Record a lesson
  ${c.bold('lessons')}  [--context topic]              List lessons
  ${c.bold('entity')}   <name> <type> [--attr k=v]    Track entity
  ${c.bold('entities')} [--type person]                List entities
  ${c.bold('gc')}       [--days 30]                    Archive old + clean stale
  ${c.bold('reflect')}                                 Generate nightly reflection
  ${c.bold('extract')}  <lesson-id> [--skill-name x]  Extract lesson → skill
  ${c.bold('stats')}                                   Memory health dashboard
  ${c.bold('search')}   <query>                        Full-text search .md files
  ${c.bold('temperature')}                             Show file temperature report
  ${c.bold('session-start')}                            ${c.cyan('★')} Load memory context (run at conversation start)
  ${c.bold('session-end')} <summary>                    ${c.cyan('★')} Save session summary (run before reset/end)
  ${c.bold('export')}                                  Export all data as JSON

Chinese Optimization (memory-cn):
  ${c.bold('diagnose')}                                 Diagnose FTS5 Chinese issues
  ${c.bold('optimize-tags')}                           Auto-add Chinese spaces to tags
  ${c.bold('compress')}   [--max-kb 5]                Compress large log files
  ${c.bold('optimize-search')}                         Show optimized search config
  ${c.bold('optimize-flush')}                          Show optimized memoryFlush prompt

Memory dir: ${MEMORY_DIR}
Backend:    ${backend === 'sqlite' ? '⚡ SQLite + FTS5 (node:sqlite)' : '📄 JSON (upgrade to Node >= 22.5 for SQLite)'}
`);
  }
}

function usage(text) {
  console.log(`Usage: node memory-cli.js ${text}`);
}

main();
