 'use strict';
const secrets = new Set();
function remember(value) { if (typeof value === 'string' && value) secrets.add(value); }
function redact(value) {
  let text = String(value);
  for (const secret of secrets) {
    for (const form of [secret, JSON.stringify(secret).slice(1, -1), encodeURIComponent(secret)]) text = text.split(form).join('[REDACTED]');
  }
  return text;
}
function install() {
  for (const stream of [process.stdout, process.stderr]) {
    const write = stream.write.bind(stream);
    stream.write = (chunk, ...args) => write(redact(Buffer.isBuffer(chunk) ? chunk.toString() : chunk), ...args);
  }
}
module.exports = { remember, redact, install };
