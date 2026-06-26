const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const mdPath = process.argv[2];
const cssPath = process.argv[3];
const outPath = process.argv[4] || 'output.html';

if (!mdPath || !cssPath) {
    console.error('Usage: node convert.js <markdown_file> <css_file> [output_file]');
    process.exit(1);
}

function installAndRequire(packageName, moduleName, tempDir) {
    try {
        return require(moduleName);
    } catch (e) {
        console.log(`Installing ${packageName} temporarily...`);
        cp.execSync(`npm install ${packageName} --no-save`, { cwd: tempDir, stdio: 'ignore' });
        return require(path.join(tempDir, 'node_modules', moduleName));
    }
}

const tempDir = path.join(process.cwd(), '.wechat-temp');
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir);
    fs.writeFileSync(path.join(tempDir, 'package.json'), '{"name":"temp","private":true}');
}

try {
    const marked = installAndRequire('marked@4', 'marked', tempDir);
    const juice = installAndRequire('juice@8', 'juice', tempDir);

    console.log('Reading files...');
    const md = fs.readFileSync(path.resolve(mdPath), 'utf8');
    const css = fs.readFileSync(path.resolve(cssPath), 'utf8');

    console.log('Converting Markdown to HTML...');
    const html = marked.parse(md);
    const wrapped = '<section id="MdWechat">' + html + '</section>';

    console.log('Inlining CSS...');
    const finalHtml = juice.inlineContent(wrapped, css);

    fs.writeFileSync(path.resolve(outPath), finalHtml);
    console.log(`\n✅ Success! WeChat HTML generated at: ${outPath}`);
} catch (err) {
    console.error('❌ Error during conversion:', err.message);
} finally {
    try {
        if (fs.existsSync(tempDir)) {
            fs.rmSync(tempDir, { recursive: true, force: true });
        }
    } catch (e) { }
}
