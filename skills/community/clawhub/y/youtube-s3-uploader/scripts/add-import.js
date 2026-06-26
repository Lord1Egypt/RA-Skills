const fs = require('fs');

const scriptPath = 'scripts/video-to-s3-universal.js';
const importLine = 'const { sanitizeFileName } = require("./sanitize-filename.js");';

let scriptContent = fs.readFileSync(scriptPath, 'utf8');

// 在第6行之后添加导入
const lines = scriptContent.split('\n');
lines.splice(6, 0, importLine);

scriptContent = lines.join('\n');

fs.writeFileSync(scriptPath, scriptContent);

console.log('✅ 已添加 sanitizeFileName 导入');
