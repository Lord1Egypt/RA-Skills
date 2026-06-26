'use strict';

const http = require('http');
const { handlePrompt } = require('./index');

const port = Number(process.env.PORT || 3000);
const token = process.env.SKILL_API_TOKEN || '';

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(body));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 1024 * 1024) reject(new Error('request body too large'));
    });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method !== 'POST' || req.url !== '/api/vox/custom-call') {
    return sendJson(res, 404, { error: 'not_found' });
  }

  if (token) {
    const auth = req.headers.authorization || '';
    if (auth !== `Bearer ${token}`) {
      return sendJson(res, 401, { error: 'unauthorized' });
    }
  }

  try {
    const body = JSON.parse(await readBody(req) || '{}');
    const result = await handlePrompt(body.prompt || '', {
      previousIntent: body.previousIntent || {},
      noCall: body.noCall === true,
      postCallCallbackUrl: body.postCallCallbackUrl || '',
      postCallCallbackToken: body.postCallCallbackToken || '',
      postCallOptions: body.postCallOptions || {},
      metadata: body.metadata || {}
    });
    return sendJson(res, result.status === 'failed' ? 502 : 200, result);
  } catch (error) {
    return sendJson(res, 500, { error: 'internal_error', message: error.message });
  }
});

if (require.main === module) {
  server.listen(port, () => {
    console.log(`Hosted Vox custom call API listening on http://localhost:${port}`);
  });
}

module.exports = { server };
