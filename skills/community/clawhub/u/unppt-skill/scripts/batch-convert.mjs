#!/usr/bin/env node
// 批量转换一个目录里的所有 .pptx（基于 @unppt/unppt 0.3.2）
//
// 用法：
//   node batch-convert.mjs <输入目录> <输出目录> [--single]
//
// 示例：
//   node batch-convert.mjs D:/pptx D:/out            # paged 形式（按需加载，适合放网站）
//   node batch-convert.mjs D:/pptx D:/out --single   # single 形式（每份一个自包含 HTML）
//
// 依赖：
//   npm install @unppt/unppt
//
// 说明：
// - 出图线程池和默认字体包只创建一次，所有文件共用；
// - 单个文件失败不会中断，最后汇总结果；
// - 输出结构：<输出目录>/<pptx文件名>/index.html + media/ + pic/ + thum/ + prop.json。

import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { basename, dirname, extname, join } from 'node:path';
import { convert } from '@unppt/unppt';
import { createRasterPool, loadFontPack } from '@unppt/unppt/node';

const args = process.argv.slice(2);
const single = args.includes('--single');
const positional = args.filter((a) => !a.startsWith('--'));
const [inDir, outRoot] = positional;
if (!inDir || !outRoot) {
  console.error('用法: node batch-convert.mjs <输入目录> <输出目录> [--single]');
  process.exit(2);
}

const wasm = new Uint8Array(await readFile(new URL(import.meta.resolve('@unppt/unppt/resvg.wasm'))));
const pool = await createRasterPool(wasm);   // 多线程出图，所有文件共用
const fontPack = await loadFontPack();       // 默认字体包，读一次共用

const okList = [];
const failList = [];

try {
  for (const name of await readdir(inDir)) {
    // 只处理 .pptx；老格式 .ppt 需先在 PowerPoint 另存为 .pptx（转码器不支持 .ppt）
    if (extname(name).toLowerCase() !== '.pptx') continue;
    const outDir = join(outRoot, basename(name, extname(name)));
    const write = async (path, data) => {
      const target = join(outDir, path);
      await mkdir(dirname(target), { recursive: true });
      await writeFile(target, data);
    };
    try {
      const bytes = await readFile(join(inDir, name));
      const r = await convert(bytes, {
        write,
        output: single ? 'single' : 'paged',
        rasterPool: pool,
        fontPack,
      });
      okList.push(name);
      console.log(`✓ ${name}：${r.slides} 页，字体问题 ${r.fontCheck.errors} 个、提醒 ${r.fontCheck.warnings} 个，警告 ${r.report.warnings.length} 条 -> ${outDir}`);
      for (const w of r.report.warnings) console.warn(`  提示：${w}`);
    } catch (e) {
      failList.push(name);
      console.error(`✗ ${name} 转换失败：${e.message}`);
    }
  }
} finally {
  await pool.close();
}

console.log(`\n完成：成功 ${okList.length}，失败 ${failList.length}${failList.length ? '（' + failList.join('、') + '）' : ''}`);
process.exit(failList.length ? 1 : 0);
