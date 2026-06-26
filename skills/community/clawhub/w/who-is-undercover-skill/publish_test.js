// Publish test script for Who is Undercover skill
const fs = require('fs');
const path = require('path');

console.log("=== Who is Undercover Skill - Publish Validation ===");

// Check required files
const requiredFiles = ['SKILL.md', 'index.js', 'game_logic.js', 'README.md'];
const optionalFiles = ['USER_GUIDE.md', 'INSTALL.md', 'package.json', '.clawhubignore'];

const skillDir = path.join(__dirname);

console.log("\n1. Checking required files:");
let allRequiredPresent = true;
requiredFiles.forEach(file => {
    const exists = fs.existsSync(path.join(skillDir, file));
    console.log(`   ${file}: ${exists ? '✅' : '❌'}`);
    if (!exists) allRequiredPresent = false;
});

console.log(`\n2. Required files status: ${allRequiredPresent ? '✅ PASS' : '❌ FAIL'}`);

// Check SKILL.md format
console.log("\n3. Checking SKILL.md format:");
const skillMd = fs.readFileSync(path.join(skillDir, 'SKILL.md'), 'utf8');
const hasFrontmatter = skillMd.startsWith('---\n');
console.log(`   Has YAML frontmatter: ${hasFrontmatter ? '✅' : '❌'}`);

if (hasFrontmatter) {
    const frontmatterMatch = skillMd.match(/---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
        const frontmatter = frontmatterMatch[1];
        const hasName = frontmatter.includes('name:');
        const hasDescription = frontmatter.includes('description:');
        const hasVersion = frontmatter.includes('version:');
        console.log(`   Has name: ${hasName ? '✅' : '❌'}`);
        console.log(`   Has description: ${hasDescription ? '✅' : '❌'}`);
        console.log(`   Has version: ${hasVersion ? '✅' : '❌'}`);
    }
}

// Check file sizes
console.log("\n4. Checking file sizes:");
const totalSize = fs.readdirSync(skillDir)
    .filter(file => !file.startsWith('.') && !file.endsWith('.log') && !file.includes('node_modules'))
    .map(file => fs.statSync(path.join(skillDir, file)).size)
    .reduce((sum, size) => sum + size, 0);

console.log(`   Total size: ${(totalSize / 1024).toFixed(2)} KB`);
console.log(`   Size limit check: ${totalSize < 50 * 1024 * 1024 ? '✅ PASS' : '❌ FAIL'}`);

// Check for binary files
console.log("\n5. Checking for binary files:");
const textExtensions = ['.md', '.js', '.json', '.txt', '.yml', '.yaml', '.ts', '.css', '.html'];
let hasBinaryFiles = false;
fs.readdirSync(skillDir).forEach(file => {
    const ext = path.extname(file).toLowerCase();
    if (!textExtensions.includes(ext) && !file.startsWith('.')) {
        console.log(`   Binary file detected: ${file} ❌`);
        hasBinaryFiles = true;
    }
});
console.log(`   Binary files check: ${!hasBinaryFiles ? '✅ PASS' : '❌ FAIL'}`);

console.log("\n=== Validation Complete ===");
console.log(`Overall status: ${allRequiredPresent && hasFrontmatter && totalSize < 50 * 1024 * 1024 && !hasBinaryFiles ? '✅ READY FOR PUBLISH' : '❌ NEEDS FIXES'}`);