#!/usr/bin/env node
/**
 * QR Code Generator - 本地生成二维码并保存到文件 (Node.js 版)
 *
 * 用法:
 *   node scripts/generate.js --data <文本> --output <路径> [选项]
 *
 * 输出 JSON:
 *   {"file": "..."}
 *   {"error": "..."}
 */

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = { size: "400x400", format: "png", ecc: "M", border: 2 };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--data": args.data = argv[++i]; break;
      case "--output": args.output = argv[++i]; break;
      case "--size": args.size = argv[++i]; break;
      case "--format": args.format = argv[++i]; break;
      case "--error-correction": args.ecc = argv[++i]; break;
      case "--border": args.border = parseInt(argv[++i]); break;
    }
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.data || !args.output) {
    console.log(JSON.stringify({ error: "用法: node generate.js --data <文本> --output <路径>" }));
    process.exit(1);
  }

  const QRCode = require("qrcode");
  const eccMap = { L: "low", M: "medium", Q: "quartile", H: "high" };
  const opts = { errorCorrectionLevel: eccMap[args.ecc] || "medium", margin: args.border };

  const outputPath = path.resolve(args.output);
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  try {
    if (args.format === "svg") {
      const svg = await QRCode.toString(args.data, { ...opts, type: "svg" });
      fs.writeFileSync(outputPath, svg);
    } else {
      const sizeInt = parseInt(args.size.split("x")[0]) || 400;
      await QRCode.toFile(outputPath, args.data, { ...opts, width: sizeInt });
    }
    console.log(JSON.stringify({ file: outputPath }));
  } catch (e) {
    console.log(JSON.stringify({ error: `生成失败: ${e.message}` }));
    process.exit(1);
  }
}

main();
