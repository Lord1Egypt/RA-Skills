const fs = require('fs');
const path = require('path');
const https = require('https');
const PREVIEW_ORIGIN = 'https://video.renderingvideo.com';

const jsonPath = process.argv[2];
if (!jsonPath) {
  console.error('Error: Missing JSON file path');
  process.exit(1);
}

const fullPath = path.isAbsolute(jsonPath) ? jsonPath : path.join(process.cwd(), jsonPath);

if (!fs.existsSync(fullPath)) {
  console.error(`Error: File not found at ${fullPath}`);
  process.exit(1);
}

try {
  const rawJson = fs.readFileSync(fullPath, 'utf-8').replace(/^\uFEFF/, '');
  const schema = JSON.parse(rawJson);
  const postData = JSON.stringify(schema);

  const options = {
    hostname: 'video.renderingvideo.com',
    port: 443,
    path: '/api/preview',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
    },
  };

  const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => {
      data += chunk;
    });
    res.on('end', () => {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        const response = JSON.parse(data);
        const previewPath =
          response.viewerUrl ||
          (typeof response.url === 'string' ? response.url.replace(/^\/t\//, '/preview/') : response.url);
        const previewUrl = previewPath?.startsWith('http')
          ? previewPath
          : new URL(previewPath, PREVIEW_ORIGIN).toString();
        console.log(`\nPreview URL Created Successfully!`);
        console.log(`-----------------------------------`);
        if (response.tempId) {
          console.log(`Temp ID: ${response.tempId}`);
        }
        console.log(`URL: ${previewUrl}`);
        if (response.viewerUrl) {
          console.log(`Viewer URL: ${new URL(response.viewerUrl, PREVIEW_ORIGIN).toString()}`);
        }
        if (response.url) {
          console.log(`Player URL: ${new URL(response.url, PREVIEW_ORIGIN).toString()}`);
        }
        if (response.expiresIn) {
          console.log(`Expires: ${response.expiresIn}`);
        }
        console.log(`-----------------------------------\n`);
      } else {
        console.error(`Error: Server returned status ${res.statusCode}`);
        console.error(data);
        process.exit(1);
      }
    });
  });

  req.on('error', (e) => {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  });

  req.write(postData);
  req.end();
} catch (error) {
  console.error(`Error: Invalid JSON or request failed - ${error.message}`);
  process.exit(1);
}
