#!/usr/bin/env node

/**
 * OpenClaw SharePoint Skill — CLI for SharePoint file operations via Microsoft Graph API.
 *
 * @author Abdelkrim BOUJRAF <abdelkrim@alt-f1.be>
 * @license MIT
 * @see https://www.alt-f1.be
 */

import { readFileSync, statSync, createReadStream } from 'node:fs';
import { basename, posix, resolve } from 'node:path';
import { Buffer } from 'node:buffer';
import { config } from 'dotenv';
import { Command } from 'commander';
import { ClientCertificateCredential } from '@azure/identity';
import { Client } from '@microsoft/microsoft-graph-client';
import { TokenCredentialAuthenticationProvider } from
  '@microsoft/microsoft-graph-client/authProviders/azureTokenCredentials/index.js';

// ── Config ──────────────────────────────────────────────────────────────────

config(); // load .env

// Lazy config — only validated when a command actually runs
let _cfg;
function getCfg() {
  if (!_cfg) {
    _cfg = {
      tenantId:     env('SP_TENANT_ID'),
      clientId:     env('SP_CLIENT_ID'),
      certPath:     env('SP_CERT_PATH'),
      certPassword: process.env.SP_CERT_PASSWORD || '',
      siteId:       env('SP_SITE_ID'),
      driveId:      process.env.SP_DRIVE_ID || '',
      maxFileSize:  parseInt(process.env.SP_MAX_FILE_SIZE || '52428800', 10), // 50 MB
    };
  }
  return _cfg;
}
const CFG = new Proxy({}, { get: (_, prop) => getCfg()[prop] });

function env(key) {
  const v = process.env[key];
  if (!v) {
    console.error(`ERROR: Missing required env var ${key}. See .env.example`);
    process.exit(1);
  }
  return v;
}

// ── Security helpers ────────────────────────────────────────────────────────

function safePath(p) {
  if (!p) return '';
  const normalized = posix.normalize(p).replace(/\\/g, '/');
  if (normalized.includes('..')) {
    console.error('ERROR: Path traversal detected — ".." is not allowed');
    process.exit(1);
  }
  return normalized.replace(/^\/+/, '');
}

function checkFileSize(filePath) {
  const stat = statSync(filePath);
  if (stat.size > CFG.maxFileSize) {
    console.error(`ERROR: File exceeds size limit (${(stat.size / 1048576).toFixed(1)} MB > ${(CFG.maxFileSize / 1048576).toFixed(1)} MB)`);
    process.exit(1);
  }
  return stat.size;
}

// ── Graph client ────────────────────────────────────────────────────────────

function createGraphClient() {
  const certPath = resolve(CFG.certPath);

  const credentialOptions = {
    certificatePath: certPath,
  };
  if (CFG.certPassword) {
    credentialOptions.certificatePassword = CFG.certPassword;
  }

  const credential = new ClientCertificateCredential(
    CFG.tenantId,
    CFG.clientId,
    credentialOptions,
  );

  const authProvider = new TokenCredentialAuthenticationProvider(credential, {
    scopes: ['https://graph.microsoft.com/.default'],
  });

  return Client.initWithMiddleware({ authProvider });
}

// ── Drive helper ────────────────────────────────────────────────────────────

async function getDriveId(client) {
  if (CFG.driveId) return CFG.driveId;

  const resp = await client.api(`/sites/${CFG.siteId}/drives`)
    .select('id,name,driveType')
    .get();

  const lib = resp.value.find(d => d.driveType === 'documentLibrary');
  if (!lib) {
    console.error('ERROR: No document library found on site');
    process.exit(1);
  }
  return lib.id;
}

function driveItemPath(driveId, remotePath) {
  const safe = safePath(remotePath);
  if (!safe) return `/drives/${driveId}/root`;
  return `/drives/${driveId}/root:/${safe}:`;
}

// ── Text extraction ─────────────────────────────────────────────────────────

async function extractText(buf, filename) {
  const ext = filename.toLowerCase().split('.').pop();

  switch (ext) {
    case 'docx': {
      const mammoth = await import('mammoth');
      const result = await mammoth.default.extractRawText({ buffer: buf });
      return result.value;
    }
    case 'xlsx': {
      const ExcelJS = await import('exceljs');
      const workbook = new ExcelJS.default.Workbook();
      await workbook.xlsx.load(buf);
      const lines = [];
      workbook.eachSheet((sheet) => {
        lines.push(`\n## Sheet: ${sheet.name}\n`);
        sheet.eachRow((row) => {
          const cells = [];
          row.eachCell((cell) => {
            cells.push(String(cell.value ?? ''));
          });
          lines.push(cells.join('\t'));
        });
      });
      return lines.join('\n');
    }
    case 'pptx': {
      // pptxgenjs is for creating, not reading — use simple XML extraction
      const { Readable } = await import('node:stream');
      const { createInflate } = await import('node:zlib');
      return await extractPptxText(buf);
    }
    case 'pdf': {
      const pdfParse = (await import('pdf-parse')).default;
      const result = await pdfParse(buf);
      return result.text;
    }
    case 'txt':
    case 'md':
    case 'csv':
    case 'json':
    case 'xml':
    case 'html':
    case 'htm':
      return buf.toString('utf-8');
    default:
      return `[Binary file: ${filename} (${buf.length} bytes) — text extraction not supported for .${ext}]`;
  }
}

async function extractPptxText(buf) {
  // PPTX is a ZIP containing XML slides
  const { Readable } = await import('node:stream');
  const { promisify } = await import('node:util');

  try {
    const JSZip = (await import('jszip')).default;
    if (!JSZip) throw new Error('jszip not available');
    const zip = await JSZip.loadAsync(buf);
    const texts = [];
    const slideFiles = Object.keys(zip.files)
      .filter(f => f.match(/^ppt\/slides\/slide\d+\.xml$/))
      .sort();

    for (const file of slideFiles) {
      const xml = await zip.files[file].async('string');
      const slideText = xml.replace(/<[^>]+>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
      if (slideText) {
        const slideNum = file.match(/slide(\d+)/)?.[1];
        texts.push(`\n## Slide ${slideNum}\n${slideText}`);
      }
    }
    return texts.join('\n') || '[No text content found in slides]';
  } catch {
    return '[PPTX text extraction requires jszip — install with: npm i jszip]';
  }
}

// ── Commands ────────────────────────────────────────────────────────────────

async function cmdInfo() {
  const client = createGraphClient();
  const site = await client.api(`/sites/${CFG.siteId}`)
    .select('id,displayName,webUrl')
    .get();

  console.log('SharePoint site connection verified:\n');
  console.log(`  Site:    ${site.displayName}`);
  console.log(`  URL:     ${site.webUrl}`);
  console.log(`  Site ID: ${site.id}`);

  const driveId = await getDriveId(client);
  const drive = await client.api(`/drives/${driveId}`)
    .select('id,name,driveType,quota')
    .get();

  console.log(`  Drive:   ${drive.name} (${drive.driveType})`);
  console.log(`  Drive ID: ${drive.id}`);
  if (drive.quota) {
    const used = ((drive.quota.used || 0) / 1048576).toFixed(1);
    const total = ((drive.quota.total || 0) / 1073741824).toFixed(1);
    console.log(`  Storage: ${used} MB used / ${total} GB total`);
  }
}

async function cmdList(options) {
  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const path = safePath(options.path || '');

  let endpoint;
  if (path) {
    endpoint = `/drives/${driveId}/root:/${path}:/children`;
  } else {
    endpoint = `/drives/${driveId}/root/children`;
  }

  const resp = await client.api(endpoint)
    .select('name,size,lastModifiedDateTime,folder,file')
    .orderby('name')
    .get();

  if (!resp.value.length) {
    console.log('(empty)');
    return;
  }

  for (const item of resp.value) {
    const type = item.folder ? '📁' : '📄';
    const size = item.folder
      ? `${item.folder.childCount} items`
      : `${(item.size / 1024).toFixed(1)} KB`;
    const date = item.lastModifiedDateTime?.substring(0, 10) || '';
    console.log(`${type}  ${item.name.padEnd(40)}  ${size.padStart(12)}  ${date}`);
  }
}

async function cmdRead(options) {
  if (!options.path) {
    console.error('ERROR: --path is required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const path = safePath(options.path);

  // Get file metadata first
  const meta = await client.api(`/drives/${driveId}/root:/${path}`)
    .select('name,size,id')
    .get();

  if (meta.size > CFG.maxFileSize) {
    console.error(`ERROR: File too large (${(meta.size / 1048576).toFixed(1)} MB > ${(CFG.maxFileSize / 1048576).toFixed(1)} MB limit)`);
    process.exit(1);
  }

  // Download content
  const stream = await client.api(`/drives/${driveId}/root:/${path}:/content`).getStream();

  const chunks = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  const buf = Buffer.concat(chunks);

  // Extract text
  const text = await extractText(buf, meta.name);
  process.stdout.write(text);
}

async function cmdUpload(options) {
  if (!options.local || !options.remote) {
    console.error('ERROR: --local and --remote are required');
    process.exit(1);
  }

  const localPath = resolve(options.local);
  const remotePath = safePath(options.remote);

  checkFileSize(localPath);
  const content = readFileSync(localPath);

  const client = createGraphClient();
  const driveId = await getDriveId(client);

  const result = await client.api(`/drives/${driveId}/root:/${remotePath}:/content`)
    .put(content);

  console.log(`✅ Uploaded: ${remotePath}`);
  console.log(`   Size: ${(content.length / 1024).toFixed(1)} KB`);
  console.log(`   ID: ${result.id}`);
}

async function cmdSearch(options) {
  if (!options.query) {
    console.error('ERROR: --query is required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);

  const resp = await client.api(`/drives/${driveId}/root/search(q='${encodeURIComponent(options.query)}')`)
    .select('name,size,lastModifiedDateTime,webUrl,parentReference')
    .get();

  if (!resp.value.length) {
    console.log('No files found.');
    return;
  }

  for (const item of resp.value) {
    const size = item.size ? `${(item.size / 1024).toFixed(1)} KB` : '';
    const date = item.lastModifiedDateTime?.substring(0, 10) || '';
    const folder = item.parentReference?.path?.replace(/.*root:?\/?/, '') || '/';
    console.log(`📄  ${item.name.padEnd(40)}  ${size.padStart(10)}  ${date}  📁 ${folder}`);
  }
}

async function cmdMkdir(options) {
  if (!options.path) {
    console.error('ERROR: --path is required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const fullPath = safePath(options.path);

  const parts = fullPath.split('/');
  const folderName = parts.pop();
  const parentPath = parts.join('/');

  let endpoint;
  if (parentPath) {
    endpoint = `/drives/${driveId}/root:/${parentPath}:/children`;
  } else {
    endpoint = `/drives/${driveId}/root/children`;
  }

  const result = await client.api(endpoint).post({
    name: folderName,
    folder: {},
    '@microsoft.graph.conflictBehavior': 'fail',
  });

  console.log(`✅ Created folder: ${fullPath}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdDelete(options) {
  if (!options.path) {
    console.error('ERROR: --path is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: sharepoint delete --path "file.txt" --confirm');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const path = safePath(options.path);

  await client.api(`/drives/${driveId}/root:/${path}`).delete();

  console.log(`✅ Deleted: ${path}`);
}

// ── Coauthoring helpers ─────────────────────────────────────────────────────

async function resolveItemId(client, driveId, remotePath) {
  const path = safePath(remotePath);
  const meta = await client.api(`/drives/${driveId}/root:/${path}`)
    .select('id,name')
    .get();
  return meta.id;
}

async function cmdCheckout(options) {
  if (!options.path) {
    console.error('ERROR: --path is required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const itemId = await resolveItemId(client, driveId, options.path);

  await client.api(`/drives/${driveId}/items/${itemId}/checkout`).post(null);

  console.log(`🔒 Checked out: ${options.path}`);
  console.log(`   Item ID: ${itemId}`);
  console.log(`   The file is now locked for editing by this app.`);
}

async function cmdCheckin(options) {
  if (!options.path) {
    console.error('ERROR: --path is required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const itemId = await resolveItemId(client, driveId, options.path);

  const comment = options.comment || 'Updated via OpenClaw';
  await client.api(`/drives/${driveId}/items/${itemId}/checkin`).post({ comment });

  console.log(`🔓 Checked in: ${options.path}`);
  console.log(`   Comment: ${comment}`);
}

async function cmdEditLink(options) {
  if (!options.path) {
    console.error('ERROR: --path is required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const itemId = await resolveItemId(client, driveId, options.path);

  const result = await client.api(`/drives/${driveId}/items/${itemId}/createLink`).post({
    type: 'edit',
    scope: 'organization',
  });

  console.log(`🔗 Edit link for: ${options.path}`);
  console.log(`   URL: ${result.link.webUrl}`);
  console.log(`   Scope: organization`);
  console.log(`   Open this URL in a browser to edit in Office Online.`);
}

async function cmdEdit(options) {
  if (!options.path || !options.local) {
    console.error('ERROR: --path and --local are required');
    process.exit(1);
  }

  const client = createGraphClient();
  const driveId = await getDriveId(client);
  const remotePath = safePath(options.path);
  const localPath = resolve(options.local);
  const comment = options.comment || 'Updated via OpenClaw';

  // Step 1: Resolve item ID
  const itemId = await resolveItemId(client, driveId, remotePath);
  console.log(`📄 File: ${remotePath} (ID: ${itemId})`);

  // Step 2: Checkout
  console.log(`🔒 Checking out...`);
  try {
    await client.api(`/drives/${driveId}/items/${itemId}/checkout`).post(null);
  } catch (err) {
    if (err.statusCode === 423) {
      console.error('ERROR: File is already checked out by another user.');
      process.exit(1);
    }
    throw err;
  }

  // Step 3: Upload modified content
  try {
    checkFileSize(localPath);
    console.log(`📤 Uploading modified file...`);
    const content = readFileSync(localPath);
    await client.api(`/drives/${driveId}/items/${itemId}/content`)
      .put(content);
    console.log(`✅ Content replaced.`);
  } catch (err) {
    // If upload fails, try to undo checkout
    console.error(`ERROR during upload: ${err.message}`);
    console.log(`🔓 Undoing checkout...`);
    try {
      await client.api(`/drives/${driveId}/items/${itemId}/checkin`).post({
        comment: 'Reverted — upload failed',
      });
    } catch { /* best effort */ }
    process.exit(1);
  }

  // Step 4: Checkin
  console.log(`🔓 Checking in...`);
  await client.api(`/drives/${driveId}/items/${itemId}/checkin`).post({ comment });

  console.log(`\n✅ Edit complete: ${remotePath}`);
  console.log(`   Comment: ${comment}`);
  console.log(`   Users with the file open will see the updated version.`);
}

// ── CLI ─────────────────────────────────────────────────────────────────────

const program = new Command();

program
  .name('sharepoint')
  .description('OpenClaw SharePoint Skill — secure file operations via Microsoft Graph API')
  .version('0.1.0');

program
  .command('info')
  .description('Show site and drive info (verify connection)')
  .action(wrap(cmdInfo));

program
  .command('list')
  .description('List files and folders')
  .option('-p, --path <folder>', 'Folder path (default: root)')
  .action(wrap(cmdList));

program
  .command('read')
  .description('Read file content (extracts text from Office formats)')
  .requiredOption('-p, --path <file>', 'File path in SharePoint')
  .action(wrap(cmdRead));

program
  .command('upload')
  .description('Upload a file to SharePoint')
  .requiredOption('-l, --local <file>', 'Local file path')
  .requiredOption('-r, --remote <path>', 'Remote path in SharePoint')
  .action(wrap(cmdUpload));

program
  .command('search')
  .description('Search for files by name')
  .requiredOption('-q, --query <text>', 'Search query')
  .action(wrap(cmdSearch));

program
  .command('mkdir')
  .description('Create a folder')
  .requiredOption('-p, --path <folder>', 'Folder path to create')
  .action(wrap(cmdMkdir));

program
  .command('delete')
  .description('Delete a file (requires --confirm)')
  .requiredOption('-p, --path <file>', 'File path to delete')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdDelete));

program
  .command('checkout')
  .description('Check out a file (lock for editing)')
  .requiredOption('-p, --path <file>', 'File path to check out')
  .action(wrap(cmdCheckout));

program
  .command('checkin')
  .description('Check in a previously checked-out file')
  .requiredOption('-p, --path <file>', 'File path to check in')
  .option('-c, --comment <text>', 'Check-in comment', 'Updated via OpenClaw')
  .action(wrap(cmdCheckin));

program
  .command('edit-link')
  .description('Get an edit link to open file in Office Online')
  .requiredOption('-p, --path <file>', 'File path')
  .action(wrap(cmdEditLink));

program
  .command('edit')
  .description('Safe edit: checkout → upload modified file → checkin')
  .requiredOption('-p, --path <file>', 'Remote file path in SharePoint')
  .requiredOption('-l, --local <file>', 'Local modified file to upload')
  .option('-c, --comment <text>', 'Check-in comment', 'Updated via OpenClaw')
  .action(wrap(cmdEdit));

function wrap(fn) {
  return async (...args) => {
    try {
      await fn(...args);
    } catch (err) {
      if (err.statusCode) {
        console.error(`ERROR (${err.statusCode}): ${err.message}`);
        if (err.body) {
          try {
            const body = JSON.parse(err.body);
            console.error(`  Code: ${body.error?.code}`);
            console.error(`  Message: ${body.error?.message}`);
          } catch { /* ignore parse errors */ }
        }
      } else {
        console.error(`ERROR: ${err.message}`);
      }
      process.exit(1);
    }
  };
}

program.parse();
