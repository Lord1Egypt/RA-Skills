/**
 * Core PDF to Markdown converter
 * Supports native text PDFs and scanned documents (OCR)
 * Uses @opendocsg/pdf2md via require() when installed, or npx when not (no node_modules needed).
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');

const { resolveOutputPath } = require('./output-handler.cjs');
const { detectPdfType, resolveMode } = require('./pdf-detector.cjs');

/**
 * Convert PDF file to Markdown
 *
 * @param {object} options
 * @param {string} options.input - Input PDF file path
 * @param {string|null} options.output - Output markdown path (optional)
 * @param {string} options.mode - Conversion mode: 'auto', 'native', 'ocr'
 * @returns {Promise<{success: boolean, input: string, output: string, stats?: object, error?: string}>}
 */
async function convert(options) {
  const { input, output, mode = 'auto' } = options;

  // Validate input
  if (!input) {
    return { success: false, error: 'Input file path is required' };
  }

  const absoluteInput = path.resolve(input);
  if (!fs.existsSync(absoluteInput)) {
    return { success: false, error: `Input file not found: ${absoluteInput}` };
  }

  // Check file extension
  const ext = path.extname(absoluteInput).toLowerCase();
  if (ext !== '.pdf') {
    return { success: false, error: `Invalid file type: ${ext}. Expected .pdf` };
  }

  try {
    // Detect PDF type
    const detection = await detectPdfType(absoluteInput);
    const effectiveMode = resolveMode(mode, detection);

    // Track statistics
    const stats = { pages: 0, mode: effectiveMode };

    // Resolve output path
    const outputPath = resolveOutputPath(absoluteInput, output, '.md');

    let markdown;

    if (effectiveMode === 'native') {
      markdown = await convertNative(absoluteInput, stats);
    } else {
      // OCR mode
      const ocrResult = await convertOcr(absoluteInput, stats);
      if (!ocrResult.success) {
        return ocrResult;
      }
      markdown = ocrResult.markdown;
    }

    // Write output
    fs.writeFileSync(outputPath, markdown, 'utf8');

    // Verify output
    if (!fs.existsSync(outputPath)) {
      return { success: false, error: 'Markdown generation failed - no output file created' };
    }

    return {
      success: true,
      input: absoluteInput,
      output: outputPath,
      stats
    };

  } catch (error) {
    return {
      success: false,
      error: error.message || 'Unknown conversion error',
      stack: process.env.DEBUG ? error.stack : undefined
    };
  }
}

/**
 * Convert native text PDF via npx @opendocsg/pdf2md (folder-based CLI)
 * @param {string} pdfPath - Path to PDF file
 * @param {object} stats - Statistics object to update
 * @returns {Promise<string>} Markdown content
 */
async function convertNativeViaNpx(pdfPath, stats) {
  const tmpDir = os.tmpdir();
  const tmpIn = fs.mkdtempSync(path.join(tmpDir, 'pdf2md-in-'));
  const tmpOut = fs.mkdtempSync(path.join(tmpDir, 'pdf2md-out-'));
  const base = path.basename(pdfPath);
  const copyPath = path.join(tmpIn, base);

  try {
    fs.copyFileSync(pdfPath, copyPath);
    const result = spawnSync(
      'npx',
      [
        '--yes',
        '@opendocsg/pdf2md',
        `--inputFolderPath=${tmpIn}`,
        `--outputFolderPath=${tmpOut}`
      ],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }
    );

    if (result.status !== 0) {
      const stderr = (result.stderr || '').trim() || result.error?.message || 'Unknown error';
      throw new Error(`npx @opendocsg/pdf2md failed: ${stderr}`);
    }

    const outMd = path.join(tmpOut, path.basename(base, '.pdf') + '.md');
    if (!fs.existsSync(outMd)) {
      throw new Error('npx @opendocsg/pdf2md did not produce expected output file');
    }
    const markdown = fs.readFileSync(outMd, 'utf8');
    stats.pages = Math.max(1, Math.ceil(markdown.length / 3000));
    return markdown;
  } finally {
    try { fs.unlinkSync(copyPath); } catch { }
    try { fs.rmSync(tmpIn, { recursive: true, force: true }); } catch { }
    try { fs.rmSync(tmpOut, { recursive: true, force: true }); } catch { }
  }
}

/**
 * Convert native text PDF to Markdown (library when installed, else npx)
 * @param {string} pdfPath - Path to PDF file
 * @param {object} stats - Statistics object to update
 * @returns {Promise<string>} Markdown content
 */
async function convertNative(pdfPath, stats) {
  try {
    const pdf2md = require('@opendocsg/pdf2md');
    const pdfBuffer = fs.readFileSync(pdfPath);
    const data = pdfBuffer instanceof Buffer ? new Uint8Array(pdfBuffer) : pdfBuffer;
    const result = await pdf2md(data);
    if (result && typeof result === 'string') {
      stats.pages = Math.max(1, Math.ceil(result.length / 3000));
      return result;
    }
    throw new Error('Library returned no text');
  } catch (err) {
    if (err.code === 'MODULE_NOT_FOUND' || err.message?.includes('Cannot find module')) {
      return convertNativeViaNpx(pdfPath, stats);
    }
    throw err;
  }
}

/**
 * Convert scanned PDF using OCR
 * @param {string} pdfPath - Path to PDF file
 * @param {object} stats - Statistics object to update
 * @returns {Promise<{success: boolean, markdown?: string, error?: string}>}
 */
async function convertOcr(pdfPath, stats) {
  // Check if OCR dependencies are available
  let tesseract;
  try {
    tesseract = require('tesseract.js');
  } catch (err) {
    return {
      success: false,
      error: 'OCR mode requires tesseract.js. Install with: npm install tesseract.js pdfjs-dist canvas',
      hint: 'For native text PDFs, use --mode native'
    };
  }

  // OCR implementation would go here
  // For now, return informative error
  return {
    success: false,
    error: 'OCR conversion not yet implemented. Use --mode native for text-based PDFs.',
    hint: 'Native mode works for most PDFs with selectable text'
  };
}

/**
 * Check if dependencies are available (native = library or npx; ocr = optional)
 * @returns {{native: boolean, ocr: boolean}}
 */
function isAvailable() {
  const result = { native: false, ocr: false };

  try {
    require.resolve('@opendocsg/pdf2md');
    result.native = true;
  } catch {
    const npx = spawnSync('npx', ['--version'], { encoding: 'utf8' });
    result.native = npx.status === 0;
  }

  try {
    require.resolve('tesseract.js');
    require.resolve('pdfjs-dist');
    result.ocr = true;
  } catch { }

  return result;
}

module.exports = { convert, isAvailable };
