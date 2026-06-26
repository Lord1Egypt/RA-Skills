const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, LevelFormat } = require('docx');
const fs = require('fs');
const path = require('path');

// ── 可配置路径（环境变量优先）─────────────────────────────
const INPUT_MD  = process.env.REPORT_MD  || 'reports/Report.md';
const OUTPUT_DOCX = process.env.REPORT_DOCX || 'reports/Report.docx';
const REPORT_TITLE = process.env.REPORT_TITLE || '房地产市场调研报告';
// ──────────────────────────────────────────────────────────

// ── 合并Part文件时自动删除交互内容 ─────────────────────────
function mergePartFiles(partFiles) {
    let merged = '';
    for (const file of partFiles) {
        let content = fs.readFileSync(file, 'utf8');
        // 删除末尾交互内容：从 "\n---\n\n**第X章节完成" 或 "---\n**第X章节完成" 到文件末尾
        // 匹配模式：--- 后面跟着换行，然后是 **第X章节完成
        const interactionPattern = /\n?---\n\n?\*\*第[一二三四五六七八九十]+章节完成[\s\S]*$/;
        content = content.replace(interactionPattern, '\n');
        merged += content + '\n\n';
    }
    return merged;
}

// 如果INPUT_MD不存在，从环境变量REPORT_PROJECT_DIR指定的项目目录查找Part文件
const REPORT_PROJECT_DIR = process.env.REPORT_PROJECT_DIR || '';
let markdownContent;
if (!fs.existsSync(INPUT_MD)) {
    if (!REPORT_PROJECT_DIR) {
        console.error('错误：找不到报告文件，请设置环境变量 REPORT_MD 或 REPORT_PROJECT_DIR');
        console.error('  REPORT_MD=reports/MyReport.md          — 直接指定报告文件路径');
        console.error('  REPORT_PROJECT_DIR=cases/ProjectName/  — 指定项目目录（将从Part文件合并）');
        process.exit(1);
    }
    const projPath = path.resolve(REPORT_PROJECT_DIR);
    if (!fs.existsSync(projPath) || !fs.statSync(projPath).isDirectory()) {
        console.error(`错误：项目目录不存在: ${projPath}`);
        process.exit(1);
    }
    const partFiles = fs.readdirSync(projPath)
        .filter(f => f.match(/Part\d+_v0\.[12]\.md/))
        .sort()
        .map(f => path.join(projPath, f));
    
    if (partFiles.length > 0) {
        markdownContent = mergePartFiles(partFiles);
        fs.writeFileSync(INPUT_MD, markdownContent);
        console.log(`已合并 ${partFiles.length} 个Part文件: ${projPath}`);
    } else {
        console.error(`错误：指定目录中找不到Part文件: ${projPath}`);
        process.exit(1);
    }
} else {
    markdownContent = fs.readFileSync(INPUT_MD, 'utf8');
}

// Parse markdown to docx elements
function parseMarkdownToDocx(markdown) {
    const lines = markdown.split('\n');
    const children = [];
    let inTable = false;
    let tableRows = [];
    let tableHeaders = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Skip empty lines
        if (!line) {
            if (inTable) {
                // End table
                if (tableRows.length > 0) {
                    children.push(createTable(tableHeaders, tableRows));
                }
                inTable = false;
                tableRows = [];
                tableHeaders = [];
            }
            continue;
        }
        
        // Handle tables
        if (line.startsWith('|')) {
            if (!inTable) {
                inTable = true;
                tableHeaders = [];
                tableRows = [];
            }
            
            const cells = line.split('|').map(c => c.trim()).filter(c => c);
            
            // Skip separator line (contains ---)
            if (cells.some(c => c.match(/^-+$/))) {
                continue;
            }
            
            if (tableHeaders.length === 0) {
                tableHeaders = cells;
            } else {
                tableRows.push(cells);
            }
            continue;
        }
        
        if (inTable) {
            children.push(createTable(tableHeaders, tableRows));
            inTable = false;
            tableRows = [];
            tableHeaders = [];
        }
        
        // Handle headings
        if (line.startsWith('# ')) {
            children.push(new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun(line.substring(2))]
            }));
        } else if (line.startsWith('## ')) {
            children.push(new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun(line.substring(3))]
            }));
        } else if (line.startsWith('### ')) {
            children.push(new Paragraph({
                heading: HeadingLevel.HEADING_3,
                children: [new TextRun(line.substring(4))]
            }));
        } else if (line.startsWith('#### ')) {
            children.push(new Paragraph({
                heading: HeadingLevel.HEADING_4,
                children: [new TextRun(line.substring(5))]
            }));
        } else if (line.startsWith('**') && line.endsWith('**')) {
            // Bold text
            children.push(new Paragraph({
                children: [new TextRun({ text: line.replace(/\*\*/g, ''), bold: true })]
            }));
        } else if (line.startsWith('> ')) {
            // Blockquote
            children.push(new Paragraph({
                children: [new TextRun({ text: line.substring(2), italics: true, color: "666666" })]
            }));
        } else if (line.startsWith('---')) {
            // Horizontal rule - add page break
            children.push(new Paragraph({ children: [new PageBreak()] }));
        } else if (line.startsWith('【') && line.endsWith('】')) {
            // Section markers like 【核心观点】
            children.push(new Paragraph({
                children: [new TextRun({ text: line, bold: true, color: "2E74B5" })]
            }));
        } else {
            // Regular paragraph
            // Handle inline formatting
            let text = line;
            const runs = [];
            
            // Simple inline bold handling
            const parts = text.split(/(\*\*.*?\*\*)/g);
            parts.forEach(part => {
                if (part.startsWith('**') && part.endsWith('**')) {
                    runs.push(new TextRun({ text: part.slice(2, -2), bold: true }));
                } else if (part) {
                    runs.push(new TextRun(part));
                }
            });
            
            if (runs.length === 0) {
                runs.push(new TextRun(text));
            }
            
            children.push(new Paragraph({ children: runs }));
        }
    }
    
    // Handle any remaining table
    if (inTable && tableRows.length > 0) {
        children.push(createTable(tableHeaders, tableRows));
    }
    
    return children;
}

function createTable(headers, rows) {
    const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
    const borders = { top: border, bottom: border, left: border, right: border };
    
    // Calculate column widths
    const numCols = headers.length;
    const colWidth = Math.floor(9360 / numCols);
    const columnWidths = Array(numCols).fill(colWidth);
    
    const tableRows = [];
    
    // Header row
    tableRows.push(new TableRow({
        children: headers.map(h => new TableCell({
            borders,
            width: { size: colWidth, type: WidthType.DXA },
            shading: { fill: "E20713", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, font: "微软雅黑" })] })]
        }))
    }));
    
    // Data rows
    rows.forEach(row => {
        tableRows.push(new TableRow({
            children: row.map(cell => new TableCell({
                borders,
                width: { size: colWidth, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: cell, font: "微软雅黑" })] })]
            }))
        }));
    });
    
    return new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths,
        rows: tableRows
    });
}

// Create document
const children = parseMarkdownToDocx(markdownContent);

const doc = new Document({
    styles: {
        default: {
            document: {
                run: { font: "微软雅黑", size: 24 }  // 12pt, 微软雅黑
            }
        },
        paragraphStyles: [
            {
                id: "Heading1",
                name: "Heading 1",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 28, bold: true, font: "微软雅黑" },  // 14pt
                paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 }
            },
            {
                id: "Heading2",
                name: "Heading 2",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 24, bold: true, font: "微软雅黑" },  // 12pt
                paragraph: { spacing: { before: 300, after: 150 }, outlineLevel: 1 }
            },
            {
                id: "Heading3",
                name: "Heading 3",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 24, bold: true, font: "微软雅黑" },  // 12pt
                paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 }
            },
            {
                id: "Heading4",
                name: "Heading 4",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 26, bold: true, font: "SimHei" },  // 13pt
                paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 3 }
            }
        ]
    },
    sections: [{
        properties: {
            page: {
                size: {
                    width: 11906,   // A4 width
                    height: 16838   // A4 height
                },
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        headers: {
            default: new Header({
                children: [new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ text: REPORT_TITLE, size: 20, color: "666666" })]
                })]
            })
        },
        footers: {
            default: new Footer({
                children: [new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [
                        new TextRun({ text: "第 ", size: 20 }),
                        new TextRun({ children: [PageNumber.CURRENT], size: 20 }),
                        new TextRun({ text: " 页", size: 20 })
                    ]
                })]
            })
        },
        children: children
    }]
});

// Generate document
Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(OUTPUT_DOCX, buffer);
    // 清理 Word 默认样式（防止字号/字体覆盖脚本设置）
    const { execFileSync } = require('child_process');
    try {
        execFileSync('python3', [path.join(__dirname, 'clean_docx_styles.py'), OUTPUT_DOCX], { stdio: 'inherit' });
    } catch (e) {}
    console.log('Word document generated successfully!');
}).catch(err => {
    console.error('Error generating document:', err);
});
