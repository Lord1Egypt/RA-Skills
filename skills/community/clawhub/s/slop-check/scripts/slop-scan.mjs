#!/usr/bin/env node
/**
 * slop-scan — deterministic metrics for the slop-check skill.
 *
 * Dependency-free (Node 18+). Walks a repo, builds a best-effort import graph,
 * and emits metrics + pre-computed subscores for the script-owned scoring
 * categories (coupling, duplication, dead weight, AI tells).
 *
 * Usage: node slop-scan.mjs <root> [--out <path>]
 */
import { readdirSync, readFileSync, statSync, existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, relative, extname, dirname, basename, resolve, sep } from 'node:path';
// ---------------------------------------------------------------------------
// CLI
const argv = process.argv.slice(2);
const root = resolve(argv.find((a) => !a.startsWith('--')) ?? process.cwd());
const outFlag = argv.indexOf('--out');
const outPath = outFlag !== -1 ? resolve(argv[outFlag + 1]) : join(root, '.slop-check', 'metrics.json');
if (!existsSync(root)) {
    console.error(`slop-scan: root does not exist: ${root}`);
    process.exit(1);
}
// ---------------------------------------------------------------------------
// Config
const MAX_FILES = 50000;
const MAX_FILE_BYTES = 1_200_000;
const DUP_WINDOW = 6; // lines per duplication window
const DUP_MIN_CHARS = 60; // ignore trivial windows
const MAX_TELL_EXAMPLES = 200;
const IGNORE_DIRS = new Set([
    'node_modules', '.git', '.hg', '.svn', 'dist', 'build', 'out', 'target',
    'vendor', 'coverage', '.next', '.nuxt', '.svelte-kit', '.turbo', '.cache',
    '__pycache__', '.venv', 'venv', 'env', '.tox', '.mypy_cache', '.pytest_cache',
    '.idea', '.vscode', '.DS_Store', 'bower_components', '.gradle', '.dart_tool',
    '.slop-check', '.understand-anything', 'Pods', 'DerivedData', '.terraform',
]);
const LANG_BY_EXT = {
    '.ts': 'typescript', '.tsx': 'typescript', '.mts': 'typescript', '.cts': 'typescript',
    '.js': 'javascript', '.jsx': 'javascript', '.mjs': 'javascript', '.cjs': 'javascript',
    '.py': 'python', '.rb': 'ruby', '.go': 'go', '.rs': 'rust', '.java': 'java',
    '.kt': 'kotlin', '.kts': 'kotlin', '.cs': 'csharp', '.php': 'php',
    '.c': 'c', '.h': 'c', '.cpp': 'cpp', '.cc': 'cpp', '.hpp': 'cpp',
    '.swift': 'swift', '.scala': 'scala', '.vue': 'vue', '.svelte': 'svelte',
    '.dart': 'dart', '.lua': 'lua', '.sh': 'shell', '.bash': 'shell', '.zsh': 'shell',
};
// Languages whose relative imports we resolve into the graph.
const RESOLVABLE = new Set(['typescript', 'javascript', 'python', 'vue', 'svelte']);
const HASH_COMMENT_LANGS = new Set(['python', 'ruby', 'shell']);
const AI_TELL_PATTERNS = [
    ['narration', /(?:\/\/|#)\s*(?:loop through|iterate over|return the|create a new|initialize the|get the|set the|check if the|call the|define the|import the)\b/i],
    ['tutorial-voice', /(?:\/\/|#)\s*(?:first,? we|next,? we|now,? we|note that|as you can see|here,? we|let's)\b/i],
    ['hedge-apology', /(?:\/\/|#|\*)\s*(?:in a real(?:-world)? (?:app|application|scenario|project)|for simplicity|this is a simplified|in production,? you (?:would|should)|for demo purposes|for the sake of)/i],
    ['placeholder', /(?:TODO:?\s*(?:implement|add) (?:actual|real|proper|the actual)|YOUR_API_KEY|your-api-key-here|REPLACE_ME|<your[-_ ]|lorem ipsum)/i],
    ['emoji-header', /(?:\/\/|#)\s*[\u{1F300}-\u{1FAFF}\u{2728}\u{2705}\u{26A0}\u{2B50}]/u],
];
// Display names for the canonical language ids, so reports read "TypeScript", not "typescript".
const LANG_DISPLAY = {
    typescript: 'TypeScript', javascript: 'JavaScript', python: 'Python', ruby: 'Ruby',
    go: 'Go', rust: 'Rust', java: 'Java', kotlin: 'Kotlin', csharp: 'C#', php: 'PHP',
    c: 'C', cpp: 'C++', swift: 'Swift', scala: 'Scala', vue: 'Vue', svelte: 'Svelte',
    dart: 'Dart', lua: 'Lua', shell: 'Shell',
};
const langName = (id) => LANG_DISPLAY[id] ?? (id.charAt(0).toUpperCase() + id.slice(1));
const ENTRY_BASENAME = /^(index|main|app|server|cli|run|setup|conftest|manage|wsgi|asgi|__init__|__main__|vite|next|webpack|rollup|babel|jest|vitest|playwright|tailwind|postcss|eslint|prettier)\b/i;
const ENTRY_PATH = /(^|\/)(pages|app|routes|api|scripts?|bin|tools?|tests?|__tests__|spec|e2e|examples?|samples?|demos?|migrations|seeds?|stories|\.storybook|commands|tasks|jobs|workers|functions|lambdas?|hooks|plugins|docs)(\/|$)/i;
const TEST_FILE = /\.(test|spec|stories)\.[^.]+$|_test\.[^.]+$|test_[^/]+\.py$/i;
const UTILS_SEGMENT = /^(utils?|helpers?|common|misc|shared|lib)$/i;
const UTILS_BASENAME = /^(utils?|helpers?|misc|common)\d*(\.|$)/i;
const clamp = (n, lo = 0, hi = 100) => Math.max(lo, Math.min(hi, Math.round(n)));
// ---------------------------------------------------------------------------
// .gitignore (best-effort: plain names and simple dir patterns only)
const extraIgnores = new Set();
try {
    const gi = readFileSync(join(root, '.gitignore'), 'utf8');
    for (let line of gi.split('\n')) {
        line = line.trim();
        if (!line || line.startsWith('#') || line.startsWith('!'))
            continue;
        line = line.replace(/^\//, '').replace(/\/$/, '');
        if (line && !/[*?[\]]/.test(line))
            extraIgnores.add(line);
    }
}
catch { /* no .gitignore */ }
// ---------------------------------------------------------------------------
// Walk
const files = [];
let truncated = false;
function walk(dir) {
    if (files.length >= MAX_FILES) {
        truncated = true;
        return;
    }
    let entries;
    try {
        entries = readdirSync(dir, { withFileTypes: true });
    }
    catch {
        return;
    }
    for (const e of entries) {
        if (files.length >= MAX_FILES) {
            truncated = true;
            return;
        }
        const abs = join(dir, e.name);
        const rel = relative(root, abs).split(sep).join('/');
        if (e.name.startsWith('.') && e.isDirectory() && e.name !== '.github')
            continue;
        if (IGNORE_DIRS.has(e.name) || extraIgnores.has(e.name) || extraIgnores.has(rel))
            continue;
        if (e.isDirectory()) {
            walk(abs);
            continue;
        }
        if (!e.isFile())
            continue;
        const ext = extname(e.name).toLowerCase();
        const lang = LANG_BY_EXT[ext];
        if (!lang)
            continue; // only analyze recognized code files
        let size;
        try {
            size = statSync(abs).size;
        }
        catch {
            continue;
        }
        if (size > MAX_FILE_BYTES)
            continue;
        files.push({ rel, abs, lang, ext });
    }
}
walk(root);
// ---------------------------------------------------------------------------
// Per-file analysis
const fileData = new Map();
const tellExamples = [];
const dupIndex = new Map();
const dupWindowsByFile = new Map();
function fnv(str) {
    let h = 0x811c9dc5;
    for (let i = 0; i < str.length; i++) {
        h ^= str.charCodeAt(i);
        h = (h * 0x01000193) >>> 0;
    }
    return h.toString(36);
}
function extractImports(lang, lines) {
    const specs = [];
    for (const line of lines) {
        if (lang === 'typescript' || lang === 'javascript' || lang === 'vue' || lang === 'svelte') {
            const m = line.match(/(?:import\s[^'"]*?from\s*|import\s*\(\s*|require\s*\(\s*|export\s[^'"]*?from\s*)['"]([^'"]+)['"]/);
            if (m)
                specs.push(m[1]);
        }
        else if (lang === 'python') {
            let m = line.match(/^\s*from\s+([\w.]+)\s+import\b/);
            if (m)
                specs.push(m[1]);
            m = line.match(/^\s*import\s+([\w.]+)/);
            if (m)
                specs.push(m[1]);
        }
    }
    return specs;
}
for (const f of files) {
    let text;
    try {
        text = readFileSync(f.abs, 'utf8');
    }
    catch {
        continue;
    }
    const lines = text.split('\n');
    // Skip minified/generated
    const avgLen = text.length / Math.max(1, lines.length);
    if (avgLen > 250)
        continue;
    const hashComments = HASH_COMMENT_LANGS.has(f.lang);
    let blank = 0, comment = 0, commentedOutCode = 0, inBlock = 0;
    let tells = 0, debugLeftovers = 0;
    const codeLinesNorm = [];
    for (let i = 0; i < lines.length; i++) {
        const raw = lines[i];
        const t = raw.trim();
        if (!t) {
            blank++;
            continue;
        }
        let isComment = false;
        if (inBlock > 0) {
            isComment = true;
            if (t.includes('*/'))
                inBlock = 0;
        }
        else if (hashComments ? t.startsWith('#') : (t.startsWith('//') || t.startsWith('*'))) {
            isComment = true;
        }
        else if (!hashComments && t.startsWith('/*')) {
            isComment = true;
            if (!t.includes('*/'))
                inBlock = 1;
        }
        // AI tells scan all lines (comments are where tells live)
        for (const [kind, re] of AI_TELL_PATTERNS) {
            if (re.test(t)) {
                tells++;
                if (tellExamples.length < MAX_TELL_EXAMPLES) {
                    tellExamples.push({ file: f.rel, line: i + 1, kind, text: t.slice(0, 140) });
                }
                break;
            }
        }
        if (isComment) {
            comment++;
            const body = t.replace(/^(\/\/|#|\*|\/\*)\s?/, '');
            if (/^(const |let |var |if\s*\(|for\s*\(|while\s*\(|return |function |def |class |import |from\s+\S+\s+import|console\.|await |\}\s*else)/.test(body) || /[;{}]\s*$/.test(body)) {
                commentedOutCode++;
            }
            continue;
        }
        if (/\bconsole\.log\s*\(/.test(t) || /^\s*debugger\b/.test(t))
            debugLeftovers++;
        const norm = t.replace(/\s+/g, ' ');
        codeLinesNorm.push([norm, i + 1]);
    }
    // Duplication windows
    const windows = [];
    if (!TEST_FILE.test(f.rel)) {
        for (let i = 0; i + DUP_WINDOW <= codeLinesNorm.length; i++) {
            const chunk = codeLinesNorm.slice(i, i + DUP_WINDOW).map((c) => c[0]).join('\n');
            if (chunk.length < DUP_MIN_CHARS)
                continue;
            const h = fnv(chunk);
            windows.push({ hash: h, startLine: codeLinesNorm[i][1] });
            if (!dupIndex.has(h))
                dupIndex.set(h, new Set());
            dupIndex.get(h).add(f.rel);
        }
    }
    dupWindowsByFile.set(f.rel, windows);
    // Standalone scripts are entry points, not dead code
    const isScriptEntry = text.startsWith('#!')
        || text.includes('process.argv')
        || text.includes("__name__ == '__main__'")
        || text.includes('__name__ == "__main__"');
    fileData.set(f.rel, {
        lang: f.lang,
        totalLines: lines.length,
        codeLines: codeLinesNorm.length,
        commentLines: comment,
        tells, debugLeftovers, commentedOutCode,
        isScriptEntry,
        importSpecs: extractImports(f.lang, lines),
    });
}
// ---------------------------------------------------------------------------
// Import graph (relative imports for JS/TS/Python; '@/' and 'src/' aliases)
const fileSet = new Set(fileData.keys());
const JS_EXTS = ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.vue', '.svelte'];
function resolveJs(fromRel, spec) {
    let base;
    if (spec.startsWith('./') || spec.startsWith('../')) {
        base = join(dirname(fromRel), spec).split(sep).join('/');
    }
    else if (spec.startsWith('@/')) {
        base = 'src/' + spec.slice(2);
    }
    else if (spec.startsWith('~/')) {
        base = 'src/' + spec.slice(2);
    }
    else
        return null;
    base = base.replace(/\\/g, '/');
    const candidates = [base, ...JS_EXTS.map((e) => base + e), ...JS_EXTS.map((e) => base + '/index' + e)];
    // NodeNext TS style: `import './x.js'` refers to x.ts on disk
    const jsToTs = base.match(/^(.*)\.(js|jsx|mjs|cjs)$/);
    if (jsToTs)
        candidates.push(jsToTs[1] + '.ts', jsToTs[1] + '.tsx', jsToTs[1] + '.mts');
    for (const c of candidates)
        if (fileSet.has(c))
            return c;
    return null;
}
function resolvePy(fromRel, spec) {
    const fromDir = dirname(fromRel);
    const asPath = spec.replace(/^\.+/, (dots) => '../'.repeat(Math.max(0, dots.length - 1))).replace(/\./g, '/');
    const candidates = [];
    if (spec.startsWith('.')) {
        candidates.push(join(fromDir, asPath).split(sep).join('/'));
    }
    else {
        candidates.push(spec.replace(/\./g, '/'));
        candidates.push('src/' + spec.replace(/\./g, '/'));
    }
    for (const base of candidates) {
        for (const c of [base + '.py', base + '/__init__.py'])
            if (fileSet.has(c))
                return c;
    }
    return null;
}
const edges = [];
const fanOut = new Map();
const fanIn = new Map();
for (const rel of fileSet) {
    fanOut.set(rel, new Set());
    fanIn.set(rel, new Set());
}
for (const [rel, data] of fileData) {
    if (!RESOLVABLE.has(data.lang))
        continue;
    for (const spec of data.importSpecs) {
        const target = data.lang === 'python' ? resolvePy(rel, spec) : resolveJs(rel, spec);
        if (target && target !== rel && !fanOut.get(rel).has(target)) {
            fanOut.get(rel).add(target);
            fanIn.get(target).add(rel);
            edges.push([rel, target]);
        }
    }
}
// Cycles via Tarjan SCC
function tarjanSCCs() {
    let idx = 0;
    const index = new Map();
    const low = new Map();
    const onStack = new Set();
    const stack = [];
    const sccs = [];
    const nodes = [...fileSet];
    for (const start of nodes) {
        if (index.has(start))
            continue;
        // iterative Tarjan
        const work = [[start, 0]];
        while (work.length) {
            const frame = work[work.length - 1];
            const [v, pi] = frame;
            if (pi === 0) {
                index.set(v, idx);
                low.set(v, idx);
                idx++;
                stack.push(v);
                onStack.add(v);
            }
            const neighbors = [...fanOut.get(v)];
            let recursed = false;
            for (let i = pi; i < neighbors.length; i++) {
                const w = neighbors[i];
                if (!index.has(w)) {
                    frame[1] = i + 1;
                    work.push([w, 0]);
                    recursed = true;
                    break;
                }
                else if (onStack.has(w)) {
                    low.set(v, Math.min(low.get(v), index.get(w)));
                }
            }
            if (recursed)
                continue;
            if (low.get(v) === index.get(v)) {
                const scc = [];
                let w;
                do {
                    w = stack.pop();
                    onStack.delete(w);
                    scc.push(w);
                } while (w !== v);
                if (scc.length > 1)
                    sccs.push(scc);
            }
            work.pop();
            if (work.length) {
                const [parent] = work[work.length - 1];
                low.set(parent, Math.min(low.get(parent), low.get(v)));
            }
        }
    }
    return sccs;
}
const sccs = tarjanSCCs().sort((a, b) => b.length - a.length);
// God files
const resolvableFiles = [...fileData.entries()].filter(([, d]) => RESOLVABLE.has(d.lang));
const degrees = [...fileSet].map((rel) => [rel, fanIn.get(rel).size + fanOut.get(rel).size]);
const avgDegree = degrees.reduce((s, [, d]) => s + d, 0) / Math.max(1, resolvableFiles.length);
const godThreshold = Math.max(12, Math.ceil(avgDegree * 4));
const godFiles = degrees
    .filter(([, d]) => d >= godThreshold)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([rel, d]) => ({ file: rel, fanIn: fanIn.get(rel).size, fanOut: fanOut.get(rel).size, degree: d }));
// Orphans (only meaningful among resolvable langs and when a graph exists)
let orphans = [];
if (edges.length >= 5) {
    orphans = resolvableFiles
        .filter(([rel]) => fanIn.get(rel).size === 0)
        .filter(([rel, d]) => {
        const name = basename(rel);
        return !d.isScriptEntry && !ENTRY_BASENAME.test(name) && !ENTRY_PATH.test(rel)
            && !TEST_FILE.test(rel) && !rel.endsWith('.d.ts') && !/config|rc\./i.test(name);
    })
        .map(([rel, d]) => ({ file: rel, codeLines: d.codeLines }))
        .sort((a, b) => b.codeLines - a.codeLines)
        .slice(0, 30);
}
// Duplication totals
let dupLines = 0, totalCodeLines = 0;
const dupFilePairs = new Set();
for (const [rel, data] of fileData) {
    totalCodeLines += data.codeLines;
    const windows = dupWindowsByFile.get(rel) ?? [];
    const dupLineSet = new Set();
    for (const w of windows) {
        const sharers = dupIndex.get(w.hash);
        if (sharers && sharers.size > 1) {
            for (let k = 0; k < DUP_WINDOW; k++)
                dupLineSet.add(w.startLine + k);
            for (const other of sharers)
                if (other !== rel)
                    dupFilePairs.add([rel, other].sort().join('|'));
        }
    }
    dupLines += dupLineSet.size;
}
const dupRatio = totalCodeLines ? dupLines / totalCodeLines : 0;
// Worst duplication clusters (for findings)
const dupClusters = [...dupIndex.entries()]
    .filter(([, s]) => s.size > 1)
    .map(([, s]) => [...s].sort().join(' <-> '))
    .reduce((m, key) => m.set(key, (m.get(key) ?? 0) + 1), new Map());
const topDupClusters = [...dupClusters.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([pair, windows]) => ({ files: pair.split(' <-> '), approxDupLines: windows * DUP_WINDOW }));
// Aggregate counts
let tells = 0, debugLeftovers = 0, commentedOutCode = 0, totalLines = 0;
const langTotals = new Map();
const utilsFiles = [];
const giantFiles = [];
for (const [rel, d] of fileData) {
    tells += d.tells;
    debugLeftovers += d.debugLeftovers;
    commentedOutCode += d.commentedOutCode;
    totalLines += d.totalLines;
    langTotals.set(d.lang, (langTotals.get(d.lang) ?? 0) + d.codeLines);
    const segs = rel.split('/');
    if (segs.slice(0, -1).some((s) => UTILS_SEGMENT.test(s)) || UTILS_BASENAME.test(basename(rel)))
        utilsFiles.push(rel);
    if (d.codeLines > 400)
        giantFiles.push({ file: rel, codeLines: d.codeLines });
}
giantFiles.sort((a, b) => b.codeLines - a.codeLines);
const utilsDirs = new Set(utilsFiles.map((f) => dirname(f)));
const kloc = Math.max(0.25, totalCodeLines / 1000);
const codeFileCount = fileData.size;
// ---------------------------------------------------------------------------
// Subscores (0 = pristine, 100 = max slop) — formulas documented in SCORING.md
const graphMeaningful = edges.length >= 5 && resolvableFiles.length >= 10;
const cycleFiles = sccs.reduce((s, c) => s + c.length, 0);
const subscores = {
    coupling: graphMeaningful
        ? clamp(sccs.length * 12 + (cycleFiles / resolvableFiles.length) * 120 + (godFiles.length / codeFileCount) * 350)
        : null,
    duplication: clamp(dupRatio * 400),
    deadWeight: clamp((graphMeaningful ? (orphans.length / Math.max(1, resolvableFiles.length)) * 280 : 0)
        + (commentedOutCode / kloc) * 6),
    aiTells: clamp((tells / kloc) * 14 + (debugLeftovers / kloc) * 3),
};
// ---------------------------------------------------------------------------
// Sample suggestions for the taste pass (deterministic)
// Sample ~12% of code files (min 10, max 300). The ceiling is a context limit,
// not a taste call: ~50 deeply-read files per reviewer x 6 reviewers max — beyond
// that, reviewers skim instead of read. Mix: most-connected files, largest files,
// highest AI-tell files, plus an even spread across the whole tree.
const sampleCap = Math.max(10, Math.min(300, Math.round(codeFileCount * 0.12)));
const nDegree = Math.ceil(sampleCap * 0.30);
const nSize = Math.ceil(sampleCap * 0.15);
const nTells = Math.ceil(sampleCap * 0.15);
const nSpread = Math.ceil(sampleCap * 0.45);
const byDegree = degrees.slice().sort((a, b) => b[1] - a[1]).slice(0, nDegree).map(([rel]) => rel);
const bySize = [...fileData.entries()].sort((a, b) => b[1].codeLines - a[1].codeLines).slice(0, nSize).map(([rel]) => rel);
const byTells = [...fileData.entries()].filter(([, d]) => d.tells > 0).sort((a, b) => b[1].tells - a[1].tells).slice(0, nTells).map(([rel]) => rel);
const all = [...fileData.keys()].sort();
const spread = Array.from({ length: nSpread }, (_, i) => all[Math.floor(((i + 0.5) / nSpread) * (all.length - 1))]);
const sampleSuggestions = [...new Set([...byDegree, ...bySize, ...byTells, ...spread])].filter(Boolean).slice(0, sampleCap);
// ---------------------------------------------------------------------------
// Output
const result = {
    tool: 'slop-scan',
    version: 1,
    root,
    truncated,
    totals: {
        codeFiles: codeFileCount,
        totalLines,
        codeLines: totalCodeLines,
        languages: Object.fromEntries([...langTotals.entries()].sort((a, b) => b[1] - a[1])),
        // Ready-to-use shares to one decimal place, so the report shows e.g. TypeScript 99.7%
        // / JavaScript 0.3% instead of rounding a real second language down to nothing.
        // Copy this straight into the report payload's project.languages.
        languagePercents: [...langTotals.entries()]
            .map(([id, lines]) => ({ name: langName(id), pct: Math.round((lines / Math.max(1, totalCodeLines)) * 1000) / 10 }))
            .filter((l) => l.pct >= 0.1)
            .sort((a, b) => b.pct - a.pct),
    },
    graph: {
        meaningful: graphMeaningful,
        resolvableFiles: resolvableFiles.length,
        edges: edges.length,
        cycles: sccs.slice(0, 10).map((c) => ({ size: c.length, files: c.slice(0, 8) })),
        cycleCount: sccs.length,
        godFiles,
        godThreshold,
        orphans,
    },
    duplication: {
        duplicatedLines: dupLines,
        ratio: +dupRatio.toFixed(4),
        crossFilePairs: dupFilePairs.size,
        topClusters: topDupClusters,
    },
    aiTells: {
        count: tells,
        perKloc: +(tells / kloc).toFixed(2),
        debugLeftovers,
        examples: tellExamples,
    },
    deadWeight: {
        commentedOutCode,
        commentedOutPerKloc: +(commentedOutCode / kloc).toFixed(2),
        orphanCount: orphans.length,
    },
    hygiene: {
        utilsFiles: utilsFiles.length,
        utilsDirs: [...utilsDirs].slice(0, 10),
        giantFiles: giantFiles.slice(0, 10),
    },
    subscores,
    sampleSuggestions,
};
// ---------------------------------------------------------------------------
// The Slop Map: the full per-file knowledge the scan produced, written separately
// so metrics.json stays small enough to read whole. Downstream fixing agents
// consult this instead of re-exploring the repo — the tokens were already spent.
const godSet = new Set(godFiles.map((g) => g.file));
const orphanSet = new Set(orphans.map((o) => o.file));
const giantSet = new Set(giantFiles.map((g) => g.file));
const dupSet = new Set(topDupClusters.flatMap((c) => c.files));
const utilsSet = new Set(utilsFiles);
const mapFiles = {};
for (const [rel, d] of fileData) {
    const flags = [];
    if (godSet.has(rel))
        flags.push('god-file');
    if (orphanSet.has(rel))
        flags.push('possible-orphan');
    if (giantSet.has(rel))
        flags.push('giant');
    if (dupSet.has(rel))
        flags.push('in-dup-cluster');
    if (utilsSet.has(rel))
        flags.push('utils');
    mapFiles[rel] = {
        lang: d.lang,
        codeLines: d.codeLines,
        importedBy: [...fanIn.get(rel)].sort(),
        imports: [...fanOut.get(rel)].sort(),
        ...(flags.length ? { flags } : {}),
    };
}
const slopMap = {
    tool: 'slop-check',
    kind: 'slop-map',
    version: 1,
    root,
    note: 'Per-file import graph + flags from the last slop-check run. Consult before moving, renaming, or refactoring files — importedBy tells you the blast radius.',
    cycles: sccs.slice(0, 25).map((c) => c.slice(0, 12)),
    dupClusters: topDupClusters,
    files: mapFiles,
};
const mapPath = join(dirname(outPath), 'slop-map.json');
mkdirSync(dirname(outPath), { recursive: true });
writeFileSync(outPath, JSON.stringify(result, null, 2));
writeFileSync(mapPath, JSON.stringify(slopMap, null, 1));
console.log(`slop-scan: analyzed ${codeFileCount} code files (${totalCodeLines.toLocaleString()} code lines)`);
console.log(`slop-scan: wrote slop map (${Object.keys(mapFiles).length} files, ${edges.length} edges) to ${mapPath}`);
console.log(`slop-scan: subscores — coupling=${subscores.coupling ?? 'n/a'} duplication=${subscores.duplication} deadWeight=${subscores.deadWeight} aiTells=${subscores.aiTells}`);
console.log(`slop-scan: wrote ${outPath}`);
