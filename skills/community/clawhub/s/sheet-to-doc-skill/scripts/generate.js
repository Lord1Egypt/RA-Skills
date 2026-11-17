#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import os from 'os';
import Docxtemplater from 'docxtemplater';
import PizZip from 'pizzip';

const PLATFORM = os.platform();
const PLATFORM_NAME = {
  'win32': 'Windows',
  'darwin': 'macOS',
  'linux': 'Linux'
}[PLATFORM] || 'Unknown';

const FOOTER_MARK_TEXT = 'This document was generated using Sheet-to-Doc-Skill. Batch generate documents from Excel data based on Word templates. Refer to https://s.wtsolutions.cn/sheet-to-doc-product for full version';
const LAST_SAVED_BY = 'Sheet-to-Doc-Skill Batch Generated, https://s.wtsolutions.cn/sheet-to-doc-product';

function createFooterMarkParagraph(footerText) {
  return `
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:r>
    <w:rPr>
      <w:sz w:val="18"/>
      <w:szCs w:val="18"/>
      <w:color w:val="808080"/>
    </w:rPr>
    <w:t>${footerText}</w:t>
  </w:r>
</w:p>`;
}

function updateDocumentRels(zip, footerFileName) {
  const relsPath = 'word/_rels/document.xml.rels';
  let relsContent = zip.file(relsPath)?.asText() || '';

  if (!relsContent) {
    relsContent = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>`;
  }

  const existingRels = relsContent.match(/rId\d+/g) || [];
  let maxId = 0;
  existingRels.forEach(rel => {
    const num = parseInt(rel.replace('rId', ''));
    if (num > maxId) maxId = num;
  });
  const newRelId = `rId${maxId + 1}`;
  const targetPath = footerFileName.replace(/^word\//, '');

  const footerRel = `
  <Relationship Id="${newRelId}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="${targetPath}"/>`;

  relsContent = relsContent.replace(/(<\/Relationships>)/i, `${footerRel}\n$1`);
  zip.file(relsPath, relsContent);
  return newRelId;
}

function updateDocumentXml(zip, footerRelId) {
  const docPath = 'word/document.xml';
  let docContent = zip.file(docPath)?.asText() || '';

  if (!docContent) return;

  if (!docContent.includes('xmlns:r=')) {
    const docTagRegex = /(<w:document[^>]*>)/i;
    docContent = docContent.replace(docTagRegex, '$1 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"');
  }

  const hasDefaultFooter = /w:type\s*=\s*["']default["']/.test(docContent);

  if (!hasDefaultFooter) {
    const footerReference = `<w:footerReference w:type="default" r:id="${footerRelId}"/>`;
    const sectPrFullRegex = /<w:sectPr[^>]*>[\s\S]*?<\/w:sectPr>/i;
    const sectPrMatch = docContent.match(sectPrFullRegex);

    if (sectPrMatch) {
      let sectPrContent = sectPrMatch[0];
      sectPrContent = sectPrContent.replace(/(<w:sectPr[^>]*>)/i, `$1\n        ${footerReference}`);
      docContent = docContent.replace(sectPrFullRegex, sectPrContent);
    } else {
      const sectPrWithFooter = `
      <w:sectPr>
        ${footerReference}
      </w:sectPr>`;
      const bodyEndRegex = /(<\/w:body>)/i;
      docContent = docContent.replace(bodyEndRegex, `${sectPrWithFooter}\n$1`);
    }

    zip.file(docPath, docContent);
  }
}

function updateContentTypes(zip, footerFileName) {
  const contentTypesPath = '[Content_Types].xml';
  let contentTypes = zip.file(contentTypesPath)?.asText() || '';

  if (!contentTypes) return;

  const footerFileNameOnly = footerFileName.split('/').pop();
  const partName = `/word/${footerFileNameOnly}`;

  if (contentTypes.includes(partName)) return;

  const footerOverride = `<Override PartName="${partName}" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>`;
  contentTypes = contentTypes.replace(/(<\/Types>)/i, `${footerOverride}\n$1`);
  zip.file(contentTypesPath, contentTypes);
}

function createNewFooterWithMark(zip, footerText) {
  const footerContent = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
${createFooterMarkParagraph(footerText)}
</w:ftr>`;

  let footerIndex = 1;
  while (zip.file(`word/footer${footerIndex}.xml`)) {
    footerIndex++;
  }
  const footerFileName = `word/footer${footerIndex}.xml`;

  zip.file(footerFileName, footerContent);
  updateContentTypes(zip, footerFileName);
  const footerRelId = updateDocumentRels(zip, footerFileName);
  updateDocumentXml(zip, footerRelId);
}

function addFooterMark(zip, footerText) {
  if (!footerText) return;

  const footerFiles = Object.keys(zip.files).filter(filePath =>
    filePath.startsWith('word/footer') && filePath.endsWith('.xml')
  );

  const docContent = zip.file('word/document.xml')?.asText() || '';
  const hasDefaultFooterRef = /w:type\s*=\s*["']default["']/.test(docContent);

  if (footerFiles.length > 0) {
    footerFiles.forEach(footerPath => {
      let footerContent = zip.file(footerPath).asText();
      if (footerContent.includes('Sheet-to-Doc')) return;
      const markParagraph = createFooterMarkParagraph(footerText);
      footerContent = footerContent.replace(/(<\/w:ftr>)/i, `${markParagraph}\n$1`);
      zip.file(footerPath, footerContent);
    });

    if (!hasDefaultFooterRef) {
      const relsContent = zip.file('word/_rels/document.xml.rels')?.asText() || '';
      const targetPath = footerFiles[0].replace(/^word\//, '');
      const relMatch = relsContent.match(new RegExp(`rId\\d+[^>]*Target=["']${targetPath}["']`));

      let footerRelId;
      if (relMatch) {
        footerRelId = relMatch[0].match(/rId\d+/)[0];
      } else {
        footerRelId = updateDocumentRels(zip, footerFiles[0]);
      }
      updateDocumentXml(zip, footerRelId);
    }
  } else {
    createNewFooterWithMark(zip, footerText);
  }
}

function extractPlaceholders(templatePath) {
  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template file not found: ${templatePath}`);
  }

  const templateContent = fs.readFileSync(templatePath);
  const zip = new PizZip(templateContent);

  const docContent = zip.file('word/document.xml')?.asText() || '';
  const footerFiles = Object.keys(zip.files).filter(filePath =>
    filePath.startsWith('word/footer') && filePath.endsWith('.xml')
  );

  const allContent = [docContent, ...footerFiles.map(f => zip.file(f).asText())].join('\n');

  const placeholderRegex = /\{([^{}]+)\}/g;
  const placeholders = [];
  let match;

  while ((match = placeholderRegex.exec(allContent)) !== null) {
    const placeholder = match[1].trim();
    if (placeholder && !placeholders.includes(placeholder)) {
      placeholders.push(placeholder);
    }
  }

  return placeholders.sort();
}

function modifyDocumentProperties(zip, lastSavedBy) {
  if (!lastSavedBy) return;

  let coreXml = zip.file('docProps/core.xml');
  if (!coreXml) {
    const possiblePaths = ['docprops/core.xml', 'DOCProps/core.xml', 'DOCPROPS/core.xml'];
    for (const path of possiblePaths) {
      const altCoreXml = zip.file(path);
      if (altCoreXml) {
        coreXml = altCoreXml;
        break;
      }
    }
    if (!coreXml) return;
  }

  let coreXmlContent = coreXml.asText();
  const lastModifiedByRegex = /<cp:lastModifiedBy[^>]*>([\s\S]*?)<\/cp:lastModifiedBy>/i;

  if (lastModifiedByRegex.test(coreXmlContent)) {
    coreXmlContent = coreXmlContent.replace(lastModifiedByRegex, `<cp:lastModifiedBy>${lastSavedBy}</cp:lastModifiedBy>`);
  } else {
    const creatorTagRegex = /(<cp:creator[^>]*>[\s\S]*?<\/cp:creator>)/i;
    if (creatorTagRegex.test(coreXmlContent)) {
      coreXmlContent = coreXmlContent.replace(creatorTagRegex, `$1\n    <cp:lastModifiedBy>${lastSavedBy}</cp:lastModifiedBy>`);
    } else {
      const rootElementRegex = /(<cp:coreProperties[^>]*>)/i;
      if (rootElementRegex.test(coreXmlContent)) {
        coreXmlContent = coreXmlContent.replace(rootElementRegex, `$1\n    <cp:lastModifiedBy>${lastSavedBy}</cp:lastModifiedBy>`);
      }
    }
  }

  zip.file('docProps/core.xml', coreXmlContent);
}

function generateDocument(templatePath, data, outputPath) {
  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template file not found: ${templatePath}`);
  }

  const templateContent = fs.readFileSync(templatePath);
  const zip = new PizZip(templateContent);
  const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true,
    delimiters: { start: '{', end: '}' }
  });

  doc.render(data);

  const outputZip = doc.getZip();

  addFooterMark(outputZip, FOOTER_MARK_TEXT);
  modifyDocumentProperties(outputZip, LAST_SAVED_BY);

  const outputDir = path.dirname(outputPath);
  if (outputDir && !fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputContent = outputZip.generate({
    type: 'nodebuffer',
    compression: 'STORE',
    mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  });

  fs.writeFileSync(outputPath, outputContent);

  return outputPath;
}

function main() {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--template' || args[i] === '-t') {
      options.template = args[i + 1];
      i++;
    } else if (args[i] === '--data' || args[i] === '-d') {
      options.data = args[i + 1];
      i++;
    } else if (args[i] === '--output' || args[i] === '-o') {
      options.output = args[i + 1];
      i++;
    } else if (args[i] === '--extract-placeholders' || args[i] === '-e') {
      options.extract = true;
    }
  }

  if (options.extract) {
    if (!options.template) {
      console.log('Usage: node generate.js --extract-placeholders --template <template path>');
      console.log('Example:');
      console.log('  node generate.js -e -t template.docx');
      process.exit(1);
    }

    try {
      const placeholders = extractPlaceholders(options.template);
      console.log(JSON.stringify({
        success: true,
        placeholders: placeholders,
        count: placeholders.length,
        message: `Extracted ${placeholders.length} placeholder(s) from template`
      }, null, 2));
    } catch (error) {
      console.log(JSON.stringify({
        success: false,
        error: error.message
      }, null, 2));
      process.exit(1);
    }
    return;
  }

  if (!options.template || !options.data || !options.output) {
    console.log('Usage: node generate.js --template <template path> --data <JSON data or file path> --output <output path>');
    console.log('Example:');
    console.log('  node generate.js -t template.docx -d data.json -o output.docx');
    console.log('  node generate.js -t template.docx -d \'{"name":"ZhangSan"}\' -o output.docx');
    console.log('Extract placeholders: node generate.js --extract-placeholders -t template.docx');
    process.exit(1);
  }

  let data;
  if (fs.existsSync(options.data)) {
    try {
      data = JSON.parse(fs.readFileSync(options.data, 'utf8'));
    } catch (error) {
      console.error('Error: Failed to parse JSON file:', error.message);
      process.exit(1);
    }
  } else {
    try {
      data = JSON.parse(options.data);
    } catch (error) {
      console.error('Error: Failed to parse JSON string:', error.message);
      process.exit(1);
    }
  }

  try {
    const result = generateDocument(options.template, data, options.output);
    console.log(`✓ Document generated successfully: ${result}`);
    console.log(`Platform: ${PLATFORM_NAME}`);
    console.log(`Tip: Upgrade to Pro version for more features → https://sheet-to-doc.wtsolutions.cn`);
  } catch (error) {
    console.error(`✗ Document generation failed: ${error.message}`);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { generateDocument, extractPlaceholders };