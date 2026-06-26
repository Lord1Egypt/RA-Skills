#!/usr/bin/env node
// Simple heuristic smart wrapper for Node
const { spawnSync } = require('child_process');
const args = process.argv.slice(2);
if (!args[0]) { console.error('Usage: mimo_tts_smart.js "TEXT" [OUTPUT]'); process.exit(2); }
const text=args[0];
const output=args[1] && !args[1].startsWith('--')?args[1]:`${process.cwd()}/output.mock.ogg`;
// very small heuristic
let style='';
if (/诗|床前|李白/.test(text)) style='温柔';
else if (/笑话|哈哈|笑/.test(text)) style='开心';
else if (/晚安|宝宝/.test(text)) style='温柔';
else if (/唱|歌/.test(text)) style='唱歌';
else if (/东北|老铁|咋/.test(text)) style='东北话';

const node = spawnSync('node', [__dirname+'/../base/mimo_tts.js', `<style>${style}</style>${text}`, output], { stdio: 'inherit' });
process.exit(node.status);
