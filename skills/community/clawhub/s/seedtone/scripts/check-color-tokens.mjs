import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { apcaContrast, hexToOklch, hueDistance, wcagContrast } from "./lib/color-math.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function parseArgs(argv) {
	const args = {
		tokensDir: path.join(ROOT, "tokens"),
		scanDir: null,
	};
	for (let i = 0; i < argv.length; i++) {
		if (argv[i] === "--tokens" && argv[i + 1]) args.tokensDir = path.resolve(argv[++i]);
		else if (argv[i] === "--scan" && argv[i + 1]) args.scanDir = path.resolve(argv[++i]);
	}
	return args;
}

const args = parseArgs(process.argv.slice(2));
const PRIMITIVES = path.join(args.tokensDir, "color.primitives.tokens.json");
const LIGHT = path.join(args.tokensDir, "color.light.tokens.json");
const DARK = path.join(args.tokensDir, "color.dark.tokens.json");

const failures = [];
const notes = [];
const fail = (msg) => failures.push(msg);
const ok = (msg) => notes.push(msg);

function flatten(node, prefix = [], out = []) {
	for (const [key, value] of Object.entries(node)) {
		if (key.startsWith("$")) continue;
		if (value && typeof value === "object" && "$value" in value) {
			out.push({ path: [...prefix, key].join("."), token: value });
		} else if (value && typeof value === "object") {
			flatten(value, [...prefix, key], out);
		}
	}
	return out;
}

function loadTokens(file) {
	if (!fs.existsSync(file)) throw new Error(`缺少令牌文件: ${file}`);
	const json = JSON.parse(fs.readFileSync(file, "utf8"));
	return new Map(flatten(json).map((e) => [e.path, e.token]));
}

function resolveToken(tokenPath, tokens, seen = new Set()) {
	if (seen.has(tokenPath)) throw new Error(`别名循环：${[...seen, tokenPath].join(" → ")}`);
	const token = tokens.get(tokenPath);
	if (!token) throw new Error(`别名目标不存在：${tokenPath}`);
	const value = token.$value;
	const match = typeof value === "string" ? value.match(/^\{(.+)\}$/) : null;
	if (match) return resolveToken(match[1], tokens, new Set([...seen, tokenPath]));
	if (typeof value !== "string" || !value.startsWith("#")) {
		throw new Error(`${tokenPath} 不是有效 Hex 值：${JSON.stringify(value)}`);
	}
	return value.toLowerCase();
}

const primitives = loadTokens(PRIMITIVES);
const lightSemantic = loadTokens(LIGHT);
const darkSemantic = loadTokens(DARK);
const lightTokens = new Map([...primitives, ...lightSemantic]);
const darkTokens = new Map([...primitives, ...darkSemantic]);

const SEMANTIC_GROUPS = new Set(["fgColor", "bgColor", "borderColor", "focus"]);
const semanticPaths = (tokens) =>
	[...tokens.keys()].filter((p) => SEMANTIC_GROUPS.has(p.split(".")[0])).sort();

const CORE_ROLES = [
	"bgColor.accent.emphasis",
	"bgColor.deep",
	"bgColor.default",
	"bgColor.muted",
	"borderColor.accent",
	"borderColor.default",
	"borderColor.emphasis",
	"borderColor.muted",
	"fgColor.accent",
	"fgColor.accentHover",
	"fgColor.danger",
	"fgColor.default",
	"fgColor.disabled",
	"fgColor.muted",
	"fgColor.onDeep",
	"fgColor.onEmphasis",
	"focus.outlineColor",
];

/* 1. 角色拓扑校验 */
{
	const lightPaths = semanticPaths(lightSemantic);
	const darkPaths = semanticPaths(darkSemantic);
	if (lightPaths.join("|") !== darkPaths.join("|")) {
		fail("亮/暗语义角色路径不一致");
	} else {
		const missing = CORE_ROLES.filter((r) => !lightPaths.includes(r));
		if (missing.length > 0) {
			fail(`缺少核心 Primer 角色：${missing.join(", ")}`);
		} else {
			ok(`亮/暗语义角色一致（共 ${lightPaths.length} 个角色，含 17 个核心角色）`);
		}
	}
	for (const p of lightPaths) {
		try {
			resolveToken(p, lightTokens);
			resolveToken(p, darkTokens);
		} catch (err) {
			fail(err.message);
		}
	}
}

/* 2. 对比度硬指标校验（WCAG 2.1 + APCA Lc 参考） */
{
	const PAIRS = [
		["fgColor.default", "bgColor.default", 7.0, 75, "正文 AAA"],
		["fgColor.muted", "bgColor.default", 4.5, 55, "次文字"],
		["fgColor.accent", "bgColor.default", 4.5, 55, "强调文字"],
		["fgColor.accentHover", "bgColor.default", 4.5, 55, "强调 Hover"],
		["fgColor.onEmphasis", "bgColor.accent.emphasis", 4.5, 55, "强调实底反白字"],
		["fgColor.onDeep", "bgColor.deep", 7.0, 75, "深图版文字"],
		["fgColor.danger", "bgColor.default", 4.5, 55, "危险文字"],
		["borderColor.default", "bgColor.default", 3.0, 25, "控件边框"],
		["focus.outlineColor", "bgColor.default", 3.0, 25, "焦点环"],
	];

	for (const extra of ["success", "warning", "info"]) {
		if (lightSemantic.has(`fgColor.${extra}`)) {
			PAIRS.push([`fgColor.${extra}`, "bgColor.default", 4.5, 55, `${extra} 语义文字`]);
		}
	}

	for (const [label, tokens] of [
		["亮色", lightTokens],
		["暗色", darkTokens],
	]) {
		let checked = 0;
		for (const [fg, bg, minWcag, minApca, desc] of PAIRS) {
			const fgHex = resolveToken(fg, tokens);
			const bgHex = resolveToken(bg, tokens);
			const wcag = wcagContrast(fgHex, bgHex);
			const lc = Math.abs(apcaContrast(fgHex, bgHex));
			if (wcag < minWcag) {
				fail(`${label} ${desc}（${fg} / ${bg}）WCAG ${wcag.toFixed(2)}:1 < ${minWcag}:1`);
			}
			if (lc < minApca) {
				notes.push(`! ${label} ${desc} APCA |Lc|=${lc.toFixed(1)} 偏低（建议 ≥${minApca}）`);
			}
			checked += 1;
		}
		ok(`${label}主题 ${checked} 组配对对比度校验完成（WCAG + APCA）`);
	}
}

/* 3. 中性阶 OKLCH 低彩度防漂移检查 */
{
	for (const theme of ["light", "dark"]) {
		const steps = ["0", "100", "200", "300", "400", "900"];
		for (const s of steps) {
			const key = `color.${theme}.neutral.${s}`;
			if (!primitives.has(key)) continue;
			const hex = resolveToken(key, primitives);
			const { C } = hexToOklch(hex);
			if (C > 0.015) {
				fail(`${key} (${hex}) 彩度 C=${C.toFixed(4)} > 0.015，中性阶发生偏色`);
			}
		}
	}
	ok("亮/暗中性阶 OKLCH 彩度 ≤ 0.015，纸面稳定");
}

/* 4. 异色分离检查 */
{
	for (const [label, tokens] of [
		["亮色", lightTokens],
		["暗色", darkTokens],
	]) {
		const accentH = hexToOklch(resolveToken("fgColor.accent", tokens)).H;
		const dangerH = hexToOklch(resolveToken("fgColor.danger", tokens)).H;
		const gap = hueDistance(accentH, dangerH);
		if (gap < 35) {
			notes.push(`! ${label}强调色与危险色色相角距离仅 ${gap.toFixed(1)}°，请确保搭配图标与文案`);
		} else {
			ok(`${label}强调色与危险色色相分离 ${gap.toFixed(1)}°`);
		}
	}
}

/* 5. 可选：扫描业务目录裸字面量 */
if (args.scanDir && fs.existsSync(args.scanDir)) {
	const EXT = new Set([".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".astro", ".html"]);
	let hits = 0;
	const walk = (dir) => {
		for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
			if (entry.name === "node_modules" || entry.name === "dist" || entry.name.startsWith(".")) continue;
			const full = path.join(dir, entry.name);
			if (entry.isDirectory()) walk(full);
			else if (EXT.has(path.extname(entry.name))) {
				const text = fs.readFileSync(full, "utf8");
				const m = text.match(/#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b/g);
				if (m) hits += m.length;
			}
		}
	};
	walk(args.scanDir);
	ok(`业务目录扫描（${path.relative(ROOT, args.scanDir)}）：发现 ${hits} 处 Hex 字面量`);
}

console.log("颜色令牌检查 · scripts/check-color-tokens.mjs\n");
for (const n of notes) console.log(n.startsWith("!") ? n : `✓ ${n}`);
if (failures.length > 0) {
	console.log("\n✗ 失败：");
	for (const f of failures) console.log(`  - ${f}`);
	process.exit(1);
}
console.log("\n全部通过。");
