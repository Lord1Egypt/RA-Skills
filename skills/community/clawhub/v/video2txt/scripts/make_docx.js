#!/usr/bin/env node
/**
 * make_docx.js - Generate a .docx file from plain text
 *
 * Prerequisites: npm install -g docx
 *
 * Usage:
 *   node make_docx.js <output_path> <title> [text_content]
 *   echo "text" | node make_docx.js <output_path> <title>
 */

const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require("docx");

async function main() {
  const outputPath = process.argv[2];
  const title = process.argv[3] || "Transcript";

  if (!outputPath) {
    console.error("Usage: node make_docx.js <output_path> <title> [text]");
    process.exit(1);
  }

  // Read content from argv[4] or stdin
  let content = process.argv[4];
  if (!content) {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    content = Buffer.concat(chunks).toString("utf8");
  }

  const lines = content.split(/\r?\n/);

  const children = [
    new Paragraph({ text: title, heading: HeadingLevel.HEADING_1 }),
    new Paragraph({ text: "" }),
  ];

  for (const line of lines) {
    children.push(
      new Paragraph({
        children: [new TextRun({ text: line, size: 24, font: "Arial" })],
        spacing: { after: 120 },
      })
    );
  }

  const doc = new Document({ sections: [{ children }] });
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log("OK:" + outputPath);
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
