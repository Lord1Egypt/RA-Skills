const https = require('https');
const fs = require('fs');
const path = require('path');

/**
 * Converts a local image file to base64 data URI.
 * @param {string} imagePath - Path to the image file.
 * @returns {string} Base64 data URI (data:image/xxx;base64,...)
 */
function imageToBase64DataURI(imagePath) {
    const mimeTypes = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff'
    };
    const ext = path.extname(imagePath).toLowerCase();
    const mime = mimeTypes[ext] || 'image/jpeg';
    const data = fs.readFileSync(imagePath);
    const base64 = data.toString('base64');
    return `data:${mime};base64,${base64}`;
}

/**
 * Generates an image using the Volcengine Seedream API.
 *
 * @param {Object} params - The inputs for the generation request.
 * @param {string} params.prompt - The text description of the image to generate. Required.
 * @param {string} [params.model] - The endpoint ID of the model. If missing, uses SEEDREAM_ENDPOINT_ID.
 * @param {string} [params.api_key] - Custom API key to use. Overrides environment variable.
 * @param {string} [params.size] - Target image size. Can be a resolution class (e.g., '2K', '3K') or explicit dimensions (e.g., '2048x2048').
 * @param {boolean} [params.watermark=false] - Whether to include an AI watermark.
 * @param {Object} [params.optimize_prompt_options] - Options to auto-optimize the prompt.
 * @param {Array} [params.tools] - A list of tools for the model to use (e.g., [{"type": "web_search"}]).
 * @param {string} [params.output_format] - Output image format (e.g., 'png', 'jpeg').
 * @param {string} [params.sequential_image_generation] - Sequential image generation strategy (e.g., 'auto').
 * @param {string} [params.download_dir] - Directory to save generated images.
 * @param {string|Array<string>} [params.image] - Local image path or array of local image paths to use as input (for I2I).
 *
 * @returns {Promise<Object>} A promise resolving to the API response object.
 *
 * Return value format (on success):
 * {
 *   "data": [
 *     {
 *       "url": "https://...",
 *       "size": "2048x2048"
 *     }
 *   ],
 *   "input_params": { ... },
 *   "usage": {
 *       "generated_images": 1,
 *       ...
 *   }
 * }
 *
 * Return value format (on failure):
 * {
 *   "error": "<Error Details or HTTP Code>",
 *   "message": "<Optional Server Message>"
 * }
 */
async function generateImage(params) {
    console.log('[seedream] generateImage input:', JSON.stringify({
        ...params,
        image: params.image !== undefined ? params.image : null
    }));
    const modelId = params.model || "doubao-seedream-5-0-260128";

    const payload = {
        model: modelId,
        prompt: params.prompt,
        watermark: params.watermark !== undefined && params.watermark !== null ? params.watermark : false
    };

    if (params.size !== undefined && params.size !== null) {
        payload.size = params.size;
    }
    if (params.optimize_prompt_options !== undefined && params.optimize_prompt_options !== null) {
        payload.optimize_prompt_options = params.optimize_prompt_options;
    }
    if (params.tools !== undefined && params.tools !== null) {
        payload.tools = params.tools;
    }
    if (params.output_format !== undefined && params.output_format !== null) {
        payload.output_format = params.output_format;
    }
    if (params.sequential_image_generation !== undefined && params.sequential_image_generation !== null) {
        payload.sequential_image_generation = params.sequential_image_generation;
    }
    if (params.response_format !== undefined && params.response_format !== null) {
        payload.response_format = params.response_format;
    }

    // Convert local image path(s) to base64 data URIs for I2I.
    if (params.image !== undefined && params.image !== null) {
        const inputImages = Array.isArray(params.image) ? params.image : [params.image];
        const imageDataUris = [];
        for (const imgPath of inputImages) {
            if (!fs.existsSync(imgPath)) {
                const result = { error: "Image not found", message: imgPath };
                console.error('[seedream] error:', JSON.stringify(result));
                return result;
            }
            try {
                const dataUri = imageToBase64DataURI(imgPath);
                imageDataUris.push(dataUri);
                console.log(`[seedream] loaded image: ${imgPath}`);
            } catch (e) {
                const result = { error: "Failed to load image", message: `${imgPath}: ${e.message}` };
                console.error('[seedream] error:', JSON.stringify(result));
                return result;
            }
        }

        if (imageDataUris.length === 1) {
            payload.image = imageDataUris[0];
        } else {
            payload.image = imageDataUris;
        }
        console.log(`[seedream] total images: ${imageDataUris.length}`);
    }

    const downloadImage = (url, dest) => {
        return new Promise((resolve, reject) => {
            const file = fs.createWriteStream(dest);
            https.get(url, (response) => {
                response.pipe(file);
                file.on('finish', () => {
                    file.close(resolve);
                });
            }).on('error', (err) => {
                fs.unlink(dest, () => { });
                reject(err.message);
            });
        });
    };

    const apiKey = process.env.SEEDREAM_API_KEY;
    if (!apiKey) {
        return { error: "Require SEEDREAM_API_KEY in environment" };
    }

    const baseUrl = process.env.SEEDREAM_BASE_URL || 'https://ark.cn-beijing.volces.com/api/v3/images/generations';
    const parsedUrl = new URL(baseUrl);

    console.log('[seedream] request:', JSON.stringify({
        url: baseUrl,
        payload: {
            ...payload,
            image: payload.image !== undefined ? '<base64_data_redacted>' : undefined
        }
    }));

    const dataString = JSON.stringify(payload);

    const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || 443,
        path: parsedUrl.pathname + parsedUrl.search,
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(dataString)
        }
    };

    return new Promise((resolve) => {
        const req = https.request(options, (res) => {
            let resData = '';
            res.on('data', (chunk) => resData += chunk);
            res.on('end', async () => {
                try {
                    const resJson = JSON.parse(resData);
                    console.log('[seedream] response:', JSON.stringify(resJson));

                    if (resJson.data) {
                        resJson.input_params = payload;

                        if (params.download_dir) {
                            const saveDir = params.download_dir;
                            if (!fs.existsSync(saveDir)) {
                                fs.mkdirSync(saveDir, { recursive: true });
                            }

                            for (let i = 0; i < resJson.data.length; i++) {
                                const item = resJson.data[i];
                                if (item.url) {
                                    try {
                                        const ext = payload.output_format === 'png' ? '.png' : '.jpeg';
                                        const filename = `image_${resJson.created || Date.now()}_${i}${ext}`;
                                        const destPath = path.join(saveDir, filename);
                                        await downloadImage(item.url, destPath);
                                        item.local_path = destPath;
                                    } catch (err) {
                                        item.local_path_error = err;
                                    }
                                }
                            }
                        }
                    }
                    console.log('[seedream] output:', JSON.stringify(resJson));
                    resolve(resJson);
                } catch (e) {
                    const result = { error: "Parse error", message: resData };
                    console.error('[seedream] error:', JSON.stringify(result));
                    resolve(result);
                }
            });
        });

        req.on('error', (e) => {
            const result = { error: e.message };
            console.error('[seedream] error:', JSON.stringify(result));
            resolve(result);
        });
        req.write(dataString);
        req.end();
    });
}

if (require.main === module) {
    const args = process.argv.slice(2);
    const params = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].substring(2);
            params[key] = args[i + 1];
            i++;
        }
    }

    if (params.watermark === "true") params.watermark = true;
    if (params.watermark === "false") params.watermark = false;

    if (params.optimize_prompt_options) {
        try {
            params.optimize_prompt_options = JSON.parse(params.optimize_prompt_options);
        } catch (e) {
            console.error("Error: --optimize_prompt_options must be a valid JSON string");
            process.exit(1);
        }
    }

    if (params.tools) {
        try {
            params.tools = JSON.parse(params.tools);
        } catch (e) {
            console.error("Error: --tools must be a valid JSON string");
            process.exit(1);
        }
    }

    if (params.image) {
        if (params.image.trim().startsWith('[')) {
            try {
                params.image = JSON.parse(params.image);
                if (!Array.isArray(params.image)) {
                    console.error("Error: --image must be a local path or a JSON array of paths");
                    process.exit(1);
                }
            } catch (e) {
                console.error("Error: --image must be a local path or a valid JSON string array");
                process.exit(1);
            }
        }
    }

    if (!params.prompt) {
        console.error("Usage: node seedream.js --prompt <prompt> [--model <model>] [--size <size>] [--watermark <true/false>] [--output_format <format>] [--sequential_image_generation <mode>] [--tools <json>] [--optimize_prompt_options <json>] [--image <path|json_array>] [--download_dir <dir>]");
        process.exit(1);
    }

    generateImage(params).then(res => console.log(JSON.stringify(res, null, 2)));
}

module.exports = { generateImage };
