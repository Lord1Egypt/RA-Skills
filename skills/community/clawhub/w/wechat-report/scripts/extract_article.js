#!/usr/bin/env node

const path = require('path');
const fs = require('fs');

async function main() {
  const [, , vendorRoot, sourceUrl, htmlFilePath] = process.argv;
  if (!vendorRoot || !sourceUrl) {
    throw new Error('Usage: node extract_article.js <vendorRoot> <sourceUrl> [htmlFilePath]');
  }

  const modulePath = path.resolve(vendorRoot, 'scripts', 'extract.js');
  const extractor = require(modulePath);
  const input = htmlFilePath ? fs.readFileSync(htmlFilePath, 'utf8') : sourceUrl;
  const result = await extractor.extract(input, {
    url: sourceUrl,
    shouldReturnContent: true,
    shouldReturnRawMeta: false,
    shouldFollowTransferLink: true,
    shouldExtractMpLinks: true,
    shouldExtractTags: false,
    shouldExtractRepostMeta: true
  });
  process.stdout.write(JSON.stringify(result));
}

main().catch((error) => {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
});
