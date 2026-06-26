#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, HeadingLevel, AlignmentType } = require('docx');

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  console.error('Usage: build_deliverable_docx.js <input.md> <output.docx>');
  process.exit(1);
}
const md = fs.readFileSync(input, 'utf8');
const children = [];
for (const raw of md.split(/\r?\n/)) {
  const line = raw.trimEnd();
  if (!line.trim()) {
    children.push(new Paragraph({ text: '' }));
    continue;
  }
  if (line.startsWith('# ')) {
    children.push(new Paragraph({ text: line.slice(2), heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER }));
  } else if (line.startsWith('## ')) {
    children.push(new Paragraph({ text: line.slice(3), heading: HeadingLevel.HEADING_1 }));
  } else if (line.startsWith('### ')) {
    children.push(new Paragraph({ text: line.slice(4), heading: HeadingLevel.HEADING_2 }));
  } else if (line.startsWith('#### ')) {
    children.push(new Paragraph({ text: line.slice(5), heading: HeadingLevel.HEADING_3 }));
  } else if (line.startsWith('- ')) {
    children.push(new Paragraph({ text: line.slice(2), bullet: { level: 0 } }));
  } else {
    children.push(new Paragraph({ text: line }));
  }
}
const title = path.basename(input).replace(/\.md$/i, '');
const doc = new Document({ creator: 'OpenClaw', title, sections: [{ children }] });
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(output, buf);
  console.log(output);
}).catch(err => {
  console.error(String(err));
  process.exit(1);
});
