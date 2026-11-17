'use strict'

const fs = require('node:fs/promises')
const { execFile } = require('node:child_process')
const { promisify } = require('node:util')
const net = require('node:net')

function publicUrl(value, label = 'URL') {
  if (typeof value !== 'string' || value.length > 2048) throw new Error(`${label}: expected HTTP(S) URL of at most 2048 characters`)
  let url
  try { url = new URL(value) } catch { throw new Error(`${label}: invalid URL`) }
  const host = url.hostname.toLowerCase().replace(/^\[|\]$/g, '')
  const v4 = net.isIP(host) === 4 ? host.split('.').map(Number) : null
  const privateV4 = v4 && (v4[0] === 0 || v4[0] === 10 || v4[0] === 127 || v4[0] >= 224 ||
    (v4[0] === 169 && v4[1] === 254) || (v4[0] === 172 && v4[1] >= 16 && v4[1] <= 31) ||
    (v4[0] === 192 && v4[1] === 168) || (v4[0] === 100 && v4[1] >= 64 && v4[1] <= 127))
  const privateV6 = net.isIP(host) === 6 && (host === '::' || host === '::1' || /^f[cd]/.test(host) || /^fe[89ab]/.test(host) || /^ff/.test(host) || host.startsWith('::ffff:'))
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password ||
      host === 'localhost' || host.endsWith('.localhost') || host.endsWith('.local') ||
      host.endsWith('.internal') || privateV4 || privateV6) {
    throw new Error(`${label}: requires a publicly accessible HTTP(S) URL without embedded credentials`)
  }
  return value
}

// Local inspection only. Never downloads a remote file or sends it to an extra metadata service.
async function probeLocal(file) {
  const path = require('node:path').resolve(file)
  const stat = await fs.stat(path)
  if (!stat.isFile()) throw new Error('probe requires a local regular file')
  let stdout
  try {
    ;({ stdout } = await promisify(execFile)('ffprobe', [
      '-v', 'error', '-show_format', '-show_streams', '-of', 'json', path,
    ], { timeout: 15000, maxBuffer: 2 * 1024 * 1024 }))
  } catch (error) {
    if (error.code === 'ENOENT') throw new Error('ffprobe is not installed; media metadata remains unverified')
    throw new Error('ffprobe could not inspect the local file; media metadata remains unverified')
  }
  const info = JSON.parse(stdout)
  return { file: path, bytes: stat.size, verified: true, format: info.format, streams: info.streams }
}

module.exports = { publicUrl, probeLocal }
