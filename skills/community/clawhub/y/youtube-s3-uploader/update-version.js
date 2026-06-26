const fs = require('fs');
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
console.log('当前版本:', packageJson.version);
packageJson.version = '3.0.2';
fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
console.log('更新后版本:', packageJson.version);
