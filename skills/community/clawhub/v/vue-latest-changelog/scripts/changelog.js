const fs = require('fs');
const path = require('path');
async function getFirstSectionFromMarkdown() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/vuejs/core/refs/heads/main/CHANGELOG.md');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdownContent = await response.text();
        const regex = /^## (.*?)\n((.|\n)*?)(?=^## )/m;
        const match = markdownContent.match(regex);
        let content;
        if (match) {
            content = '##'+ match[1] + '\n' + match[2].trim();
        } else {
            content = '未找到匹配内容';
        }
        // 写入文件
        const filePath = path.join(__dirname,'../assets/', 'latest_changelog.md');
        fs.writeFileSync(filePath, content, 'utf8');
        return content;
    } catch (error) {
        console.error('获取内容时出错:', error);
        return '获取内容时出错';
    }
}

getFirstSectionFromMarkdown().then(() => {
    console.log('内容已写入文件:');
});