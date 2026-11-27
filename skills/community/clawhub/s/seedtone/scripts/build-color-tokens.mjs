import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import StyleDictionary from "style-dictionary";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function parseArgs(argv) {
	const args = {
		tokensDir: path.join(ROOT, "tokens"),
		outFile: path.join(ROOT, "dist", "tokens.generated.css"),
		check: false,
	};
	for (let i = 0; i < argv.length; i++) {
		const a = argv[i];
		if (a === "--tokens" && argv[i + 1]) args.tokensDir = path.resolve(argv[++i]);
		else if (a === "--out" && argv[i + 1]) args.outFile = path.resolve(argv[++i]);
		else if (a === "--check") args.check = true;
	}
	return args;
}

const HEADER = `/* ============================================================
   自动生成，禁止手改。
   生成器：scripts/build-color-tokens.mjs + Style Dictionary 4
   只输出角色变量；基色（--color-*）不进入 CSS。
   重新生成：pnpm tokens:build
   校验：pnpm tokens:check
   ============================================================ */`;

StyleDictionary.registerTransform({
	name: "name/primer",
	type: "name",
	transform: (token) => token.path.join("-"),
});

StyleDictionary.registerTransformGroup({
	name: "css/primer",
	transforms: ["attribute/cti", "name/primer", "color/css"],
});

async function buildTheme(primitivesPath, themePath, selector, destination) {
	const sd = new StyleDictionary({
		source: [primitivesPath, themePath],
		log: { verbosity: "silent" },
		platforms: {
			css: {
				transformGroup: "css/primer",
				buildPath: destination.dir + path.sep,
				files: [
					{
						destination: destination.file,
						format: "css/variables",
						filter: (token) => token.path[0] !== "color",
						options: {
							selector,
							outputReferences: false,
						},
					},
				],
			},
		},
	});
	await sd.buildAllPlatforms();
	return fs.readFileSync(path.join(destination.dir, destination.file), "utf8");
}

export async function buildColorCss(tokensDir = path.join(ROOT, "tokens")) {
	const primitivesPath = path.join(tokensDir, "color.primitives.tokens.json");
	const lightPath = path.join(tokensDir, "color.light.tokens.json");
	const darkPath = path.join(tokensDir, "color.dark.tokens.json");

	for (const f of [primitivesPath, lightPath, darkPath]) {
		if (!fs.existsSync(f)) {
			throw new Error(`找不到 DTCG 令牌文件: ${f}`);
		}
	}

	const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "color-tokens-"));
	try {
		const light = await buildTheme(primitivesPath, lightPath, ":root", { dir: tmp, file: "light.css" });
		const dark = await buildTheme(primitivesPath, darkPath, ".dark", { dir: tmp, file: "dark.css" });
		return `${HEADER}\n\n${light.trim()}\n\n${dark.trim()}\n`;
	} finally {
		fs.rmSync(tmp, { recursive: true, force: true });
	}
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
	const args = parseArgs(process.argv.slice(2));
	const css = await buildColorCss(args.tokensDir);
	if (args.check) {
		const current = fs.existsSync(args.outFile) ? fs.readFileSync(args.outFile, "utf8") : "";
		if (current !== css) {
			console.error(`✗ ${path.relative(ROOT, args.outFile)} 与 DTCG 源不一致，请运行 pnpm tokens:build`);
			process.exit(1);
		}
		console.log(`✓ ${path.relative(ROOT, args.outFile)} 与 DTCG 源一致。`);
	} else {
		fs.mkdirSync(path.dirname(args.outFile), { recursive: true });
		fs.writeFileSync(args.outFile, css);
		console.log(`✓ 已写入 ${path.relative(ROOT, args.outFile)}`);
	}
}
