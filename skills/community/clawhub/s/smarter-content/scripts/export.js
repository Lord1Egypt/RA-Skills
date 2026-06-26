// Export content to different formats
// Usage: node export.js content.md output [format]

const fs = require('fs');
const path = require('path');

function exportToMarkdown(content, outputPath) {
    fs.writeFileSync(outputPath, content, 'utf8');
    console.log(`Exported markdown to ${outputPath}`);
    return true;
}

function exportToHtml(content, outputPath) {
    // Simple markdown to HTML conversion (basic version)
    let html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>${content.split('\n')[0].replace(/^#\s*/, '')}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
}
pre {
    background: #f5f5f5;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
}
img {
    max-width: 100%;
}
</style>
</head>
<body>
${markdownToHtml(content)}
</body>
</html>`;
    
    fs.writeFileSync(outputPath, html, 'utf8');
    console.log(`Exported HTML to ${outputPath}`);
    return true;
}

function markdownToHtml(markdown) {
    // Very basic conversion
    let html = markdown
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\[([^\]]*)\]\(([^)]*)\)/g, '<a href="$2">$1</a>')
        .replace(/^\- (.*)$/gm, '<li>$1</li>')
        .replace(/^\d+\. (.*)$/gm, '<li>$1</li>');
    
    // Wrap paragraphs
    let lines = html.split('\n');
    let inList = false;
    let result = [];
    
    lines.forEach(line => {
        if (line.startsWith('<li>') && !inList) {
            result.push('<ul>');
            inList = true;
        } else if (!line.startsWith('<li>') && inList) {
            result.push('</ul>');
            inList = false;
        }
        result.push(line);
    });
    
    if (inList) {
        result.push('</ul>');
    }
    
    return result.join('\n');
}

function exportContent(content, outputPath, format = 'md') {
    if (format === 'html') {
        return exportToHtml(content, outputPath);
    }
    return exportToMarkdown(content, outputPath);
}

module.exports = {
    exportContent,
    exportToMarkdown,
    exportToHtml
};

// CLI usage
if (require.main === module) {
    const inputFile = process.argv[2];
    const outputPath = process.argv[3];
    const format = process.argv[4] || 'md';
    
    const content = fs.readFileSync(inputFile, 'utf8');
    exportContent(content, outputPath, format);
}
