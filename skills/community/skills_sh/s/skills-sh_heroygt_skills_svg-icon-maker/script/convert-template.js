const { vectorize, ColorMode, Hierarchical, PathSimplifyMode } = require('@neplex/vectorizer');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// Parse command-line arguments
const args = process.argv.slice(2);
const inputFile = args[0]; // First argument: input PNG file path
const outputDir = args[1] || './svg-output'; // Second argument: output directory (optional)

// Validate input
if (!inputFile) {
    console.error('❌ Usage: node convert-template.js <input-file> [output-dir]');
    console.error('   Example: node convert-template.js ./my-image.png ./output');
    process.exit(1);
}

if (!fs.existsSync(inputFile)) {
    console.error(`❌ Error: Input file not found: ${inputFile}`);
    process.exit(1);
}

// Create timestamped folder for this run (format: YYYY-MM-DDTHH-mm-ss-SSSZ)
const now = new Date();
const TIMESTAMP = now.toISOString().replace(/:/g, '-').replace(/\./g, '-');
const JOB_DIR = path.join(outputDir, TIMESTAMP);

// Ensure output directory exists
if (!fs.existsSync(JOB_DIR)) {
    fs.mkdirSync(JOB_DIR, { recursive: true });
}

const INPUT = inputFile;
// -------- helpers --------

/**
 * Remove any obvious background added by vectorizer (defensive).
 * This is a fallback — the real fix is making the input transparent first.
 */
function stripSvgBackground(svg) {
    let out = svg;

    // 1) Remove full-canvas rect backgrounds (common)
    out = out.replace(
        /<rect\b[^>]*(?:width="100%"|width="\d+")[^>]*(?:height="100%"|height="\d+")[^>]*\bfill="[^"]+"[^>]*\/?>/gi,
        ''
    );

    // 2) Remove svg root background style if present
    out = out.replace(/style="[^"]*background[^"]*"/gi, (m) => {
        // Remove only background part inside style="..."
        const styleVal = m.slice(7, -1); // content inside quotes
        const cleaned = styleVal
            .split(';')
            .map(s => s.trim())
            .filter(s => s && !/^background\s*:/i.test(s))
            .join(';');
        return cleaned ? `style="${cleaned}"` : '';
    });

    return out;
}

/**
 * Preprocess image:
 * - Ensure alpha exists
 * - Flood fill transparency starting from ALL 4 CORNERS logic to handle split backgrounds
 * - Preserves inner white pixels that are not connected to the background
 */
async function preprocessToTransparentPng(inputPath, outPath, threshold = 30) {
    const image = sharp(inputPath).ensureAlpha();
    const { data, info } = await image.raw().toBuffer({ resolveWithObject: true });

    const width = info.width;
    const height = info.height;

    // Auto-detect background color from top-left pixel (0,0)
    const bgR = data[0];
    const bgG = data[1];
    const bgB = data[2];

    console.log(`🔍 Auto-detected background color from (0,0): rgb(${bgR}, ${bgG}, ${bgB})`);

    // Visited array to keep track of checked pixels
    const visited = new Uint8Array(width * height);

    // Queue/Stack for traversal
    const queue = [];

    // Helper to add seed if getting color match
    const addSeed = (x, y) => {
        const idx = (y * width + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];
        const diff = Math.abs(r - bgR) + Math.abs(g - bgG) + Math.abs(b - bgB);

        // Only seed if corner is roughly same color as TL corner (avoid wiping foreground if it touches corner)
        if (diff <= threshold * 3) {
            const vIdx = y * width + x;
            if (visited[vIdx] === 0) {
                visited[vIdx] = 1;
                queue.push(x, y);
            }
        }
    };

    // Add 4 corners as potential seeds
    addSeed(0, 0); // TL
    addSeed(width - 1, 0); // TR
    addSeed(0, height - 1); // BL
    addSeed(width - 1, height - 1); // BR

    // Threshold multiplier logic:
    // Simple RGB distance sum. 
    // Max diff = 255*3 = 765. 
    // Threshold 30 means we tolerate sum of diffs < 90 (avg 30 per channel)
    const distThreshold = threshold * 3;

    let removedCount = 0;

    // Use a stack-based traversal (pop) for simplicity
    while (queue.length > 0) {
        const y = queue.pop();
        const x = queue.pop();

        const idx = (y * width + x) * 4;

        // Remove this pixel
        data[idx + 3] = 0;
        removedCount++;

        // Neighbors (4-connectivity)
        // Check inline to be faster
        // 1. Right
        if (x + 1 < width) {
            const nx = x + 1;
            const ny = y;
            const nIdx = ny * width + nx;
            if (visited[nIdx] === 0) {
                const pIdx = nIdx * 4;
                if (data[pIdx + 3] !== 0) { // optimization
                    const diff = Math.abs(data[pIdx] - bgR) + Math.abs(data[pIdx + 1] - bgG) + Math.abs(data[pIdx + 2] - bgB);
                    if (diff <= distThreshold) {
                        visited[nIdx] = 1;
                        queue.push(nx, ny);
                    }
                }
            }
        }
        // 2. Left
        if (x - 1 >= 0) {
            const nx = x - 1;
            const ny = y;
            const nIdx = ny * width + nx;
            if (visited[nIdx] === 0) {
                const pIdx = nIdx * 4;
                if (data[pIdx + 3] !== 0) {
                    const diff = Math.abs(data[pIdx] - bgR) + Math.abs(data[pIdx + 1] - bgG) + Math.abs(data[pIdx + 2] - bgB);
                    if (diff <= distThreshold) {
                        visited[nIdx] = 1;
                        queue.push(nx, ny);
                    }
                }
            }
        }
        // 3. Down
        if (y + 1 < height) {
            const nx = x;
            const ny = y + 1;
            const nIdx = ny * width + nx;
            if (visited[nIdx] === 0) {
                const pIdx = nIdx * 4;
                if (data[pIdx + 3] !== 0) {
                    const diff = Math.abs(data[pIdx] - bgR) + Math.abs(data[pIdx + 1] - bgG) + Math.abs(data[pIdx + 2] - bgB);
                    if (diff <= distThreshold) {
                        visited[nIdx] = 1;
                        queue.push(nx, ny);
                    }
                }
            }
        }
        // 4. Up
        if (y - 1 >= 0) {
            const nx = x;
            const ny = y - 1;
            const nIdx = ny * width + nx;
            if (visited[nIdx] === 0) {
                const pIdx = nIdx * 4;
                if (data[pIdx + 3] !== 0) {
                    const diff = Math.abs(data[pIdx] - bgR) + Math.abs(data[pIdx + 1] - bgG) + Math.abs(data[pIdx + 2] - bgB);
                    if (diff <= distThreshold) {
                        visited[nIdx] = 1;
                        queue.push(nx, ny);
                    }
                }
            }
        }
    }

    console.log(`   🌊 Flood fill (4-corner) removed ${Math.round(removedCount / (width * height) * 100)}% of background pixels.`);

    const newBuf = await sharp(data, {
        raw: {
            width: width,
            height: height,
            channels: 4
        }
    })
        .png()
        .toBuffer();

    await fs.promises.writeFile(outPath, newBuf);
    return newBuf;
}

// -------- main --------

const OUTPUT_SVG = path.join(JOB_DIR, 'icon.svg');
const OUTPUT_PNG = path.join(JOB_DIR, 'icon_preview.png');
const COPIED_REF = path.join(JOB_DIR, 'reference.png');
const PREPROCESSED_PNG = path.join(JOB_DIR, 'reference_preprocessed.png');

async function convert() {
    try {
        // Copy reference to job folder for archiving
        fs.copyFileSync(INPUT, COPIED_REF);
        console.log('📂 Created job folder:', JOB_DIR);

        // 1) Preprocess: remove background -> transparent
        const THRESHOLD = 30; // tolerance for background color variation
        console.log(`🧼 Preprocessing (auto-remove background), threshold=${THRESHOLD}...`);
        const inputBuffer = await preprocessToTransparentPng(INPUT, PREPROCESSED_PNG, THRESHOLD);
        console.log('🧾 Saved preprocessed PNG:', PREPROCESSED_PNG);

        // 2) Vectorize with HIGH color fidelity
        // Only removes background via flood fill, preserves all original colors
        console.log('🎨 Vectorizing...');
        let svg = await vectorize(inputBuffer, {
            colorMode: ColorMode.Color,
            hierarchical: Hierarchical.Stacked,
            filterSpeckle: 8,           // Reduced: preserve more detail
            colorPrecision: 6,          // MAX (1-8): preserve all color variations
            layerDifference: 32,         // Lower threshold: less color merging
            mode: PathSimplifyMode.Spline,
            cornerThreshold: 60,
            lengthThreshold: 4.0,
            maxIterations: 10,
            spliceThreshold: 45,
        });

        // 3) Defensive cleanup: ensure SVG has no background shapes/styles
        console.log('🔧 Ensuring SVG background is transparent...');
        svg = stripSvgBackground(svg);

        // 4) Write SVG
        await fs.promises.writeFile(OUTPUT_SVG, svg, 'utf8');

        // 5) Preview render to PNG (transparent)
        await sharp(Buffer.from(svg))
            .resize(400, 400, { fit: 'contain' })
            .png()
            .toFile(OUTPUT_PNG);

        console.log('✅ Done!');
        console.log('   SVG:', OUTPUT_SVG);
        console.log('   Preview PNG:', OUTPUT_PNG);
    } catch (err) {
        console.error('❌ Failed:', err);
    }
}

convert();
