'use strict'

const fs = require('node:fs')
const fsp = require('node:fs/promises')
const path = require('node:path')
const crypto = require('node:crypto')
const https = require('node:https')
const { VibbitError } = require('./client')

const MAX_UPLOAD_BYTES = 1024 * 1024 * 1000
// Storage endpoints used by Vibbit's China and international deployments.
// Keep this list independent of MATERIAL_UPLOAD responses.
const APPROVED_OSS_HOSTS = new Set([
  'willing-video-test.oss-cn-shanghai.aliyuncs.com',
  'vibbit-ai.oss-ap-southeast-1.aliyuncs.com',
])

function uploadDestination(host) {
  let url
  try { url = new URL(text(host, 'host')) } catch {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD returned an invalid OSS host')
  }
  if (url.protocol !== 'https:' || url.username || url.password || url.port || url.search || url.hash || url.pathname !== '/') {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS host must be an HTTPS origin without credentials, port, path, query, or fragment')
  }
  if (!APPROVED_OSS_HOSTS.has(url.hostname)) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD returned an unapproved storage host; contact Vibbit support')
  }
  return url
}

function decodePolicy(policy) {
  let decoded
  try {
    if (typeof policy !== 'string' || policy.length > 2 * 1024 * 1024 || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(policy)) throw new Error()
    decoded = JSON.parse(Buffer.from(policy, 'base64').toString('utf8'))
  } catch {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD returned an invalid Base64 JSON OSS policy')
  }
  if (!decoded || typeof decoded !== 'object' || Array.isArray(decoded) || !Array.isArray(decoded.conditions) || !decoded.conditions.length) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS policy has no conditions')
  }
  const expires = typeof decoded.expiration === 'string' ? Date.parse(decoded.expiration) : NaN
  if (!Number.isFinite(expires) || expires <= Date.now()) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS policy is expired or has an invalid expiration')
  }
  return decoded
}

function text(value, name) {
  if (typeof value !== 'string' || value.trim() === '') throw new VibbitError('protocol', `MATERIAL_UPLOAD response is missing ${name}`)
  return value
}

function normalizeRegion(region) {
  return typeof region === 'string' && region.startsWith('oss-') ? region.slice(4) : region
}

function regionFromHost(host) {
  try {
    const hostname = new URL(host).hostname
    const match = hostname.match(/\.oss-([a-z0-9-]+?)(?:-internal)?\.aliyuncs\.com$/i)
    return match ? match[1] : undefined
  } catch {
    return undefined
  }
}

function credentialParts(credential) {
  const parts = credential.split('/')
  // Alibaba Cloud STS temporary AccessKey IDs have a literal STS. prefix.
  if (parts.length !== 5 || !/^(?:STS\.)?[A-Za-z0-9]+$/.test(parts[0]) || !/^\d{8}$/.test(parts[1]) || !/^[a-z0-9-]+$/.test(parts[2]) || parts[3] !== 'oss' || parts[4] !== 'aliyun_v4_request') return undefined
  return { accessKeyId: parts[0], date: parts[1], region: parts[2], service: parts[3], request: parts[4] }
}

function hmac(key, value) {
  return crypto.createHmac('sha256', key).update(value).digest()
}

function signPolicy(policy, secret, credential, dateText) {
  const parts = credentialParts(credential)
  if (!parts) throw new VibbitError('protocol', 'MATERIAL_UPLOAD returned an invalid x-oss-credential')
  const date = dateText || parts.date
  const dateKey = hmac(`aliyun_v4${secret}`, date.slice(0, 8))
  const dateRegionKey = hmac(dateKey, parts.region)
  const dateServiceKey = hmac(dateRegionKey, 'oss')
  const signingKey = hmac(dateServiceKey, 'aliyun_v4_request')
  return crypto.createHmac('sha256', signingKey).update(policy).digest('hex')
}

function repairSigningRegion(signature) {
  const policy = text(signature.policy, 'policy')
  const decoded = decodePolicy(policy)
  const credential = text(signature.xoss_credential || signature.xOssCredential, 'xoss_credential')
  const originalParts = credentialParts(credential)
  if (!originalParts) throw new VibbitError('protocol', 'MATERIAL_UPLOAD returned an invalid x-oss-credential')
  const signingRegion = regionFromHost(signature.host) || normalizeRegion(signature.signing_region || signature.region || originalParts.region)
  for (const region of [signature.signing_region, signature.region, originalParts.region]) {
    if (region !== undefined && normalizeRegion(region) !== signingRegion) {
      throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS host and signing regions do not match')
    }
  }
  const date = text(signature.xoss_date || signature.xOssDate, 'xoss_date')
  if (!/^\d{8}T\d{6}Z$/.test(date) || date.slice(0, 8) !== originalParts.date) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS signing dates do not match')
  }
  const accessKeyId = signature.accessKeyId || signature.access_key_id
  if (accessKeyId !== undefined && accessKeyId !== originalParts.accessKeyId) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS access key IDs do not match')
  }
  if (originalParts.region === signingRegion) return { ...signature, policy, credential, signingRegion }

  // Only normalize the known oss- prefix; never switch a credential to another region.
  const secret = text(signature.accessKeySecret || signature.access_key_secret, 'access_key_secret')
  const fixedCredential = [originalParts.accessKeyId, originalParts.date, signingRegion, originalParts.service, originalParts.request].join('/')
  let replaced = false
  decoded.conditions = decoded.conditions.map(condition => {
    if (condition && typeof condition === 'object' && !Array.isArray(condition) && condition['x-oss-credential'] !== undefined) {
      if (condition['x-oss-credential'] !== credential) throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy credential does not match')
      replaced = true
      return { ...condition, 'x-oss-credential': fixedCredential }
    }
    if (Array.isArray(condition) && condition[1] === '$x-oss-credential') {
      if (condition.length !== 3 || condition[0] !== 'eq' || condition[2] !== credential) throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy credential does not match')
      replaced = true
      return ['eq', '$x-oss-credential', fixedCredential]
    }
    return condition
  })
  if (!replaced) throw new VibbitError('protocol', 'MATERIAL_UPLOAD OSS policy has no x-oss-credential condition')
  const fixedPolicy = Buffer.from(JSON.stringify(decoded)).toString('base64')
  return {
    ...signature,
    policy: fixedPolicy,
    credential: fixedCredential,
    signature: signPolicy(fixedPolicy, secret, fixedCredential, signature.xoss_date || signature.xOssDate),
    signingRegion,
  }
}

function validatePolicy(policy, fields, hostUrl, size, fileName) {
  const decoded = decodePolicy(policy)
  const values = { ...fields, bucket: hostUrl.hostname.split('.')[0], 'content-type': contentTypeFor(fileName) }
  const exact = new Set()
  const constrained = new Set()
  let keyRestricted = false
  let sizeRestricted = false
  function check(operator, field, expected) {
    if (constrained.has(field)) throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy has duplicate form conditions')
    constrained.add(field)
    const actual = values[field]
    if (typeof actual !== 'string') throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy requires an unsupported form field')
    const ci = operator.endsWith('-ci')
    const operation = ci ? operator.slice(0, -3) : operator
    const canonical = value => ci ? value.toLowerCase() : value
    let matches = false
    if (['eq', 'starts-with'].includes(operation) && typeof expected === 'string') {
      matches = operation === 'eq' ? canonical(actual) === canonical(expected) : canonical(actual).startsWith(canonical(expected))
      if (operator === 'eq') exact.add(field)
      if (field === 'key' && !ci && expected.length > 0) keyRestricted = true
    } else if (['in', 'not-in'].includes(operation) && Array.isArray(expected) && expected.every(value => typeof value === 'string')) {
      matches = expected.map(canonical).includes(canonical(actual))
      if (operation === 'not-in') matches = !matches
    }
    if (!matches) throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy does not match the upload form')
  }
  for (const condition of decoded.conditions) {
    if (Array.isArray(condition)) {
      if (condition.length !== 3) throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy has an invalid condition')
      const [operator, field, expected] = condition
      if (operator === 'content-length-range') {
        if (sizeRestricted || !Number.isSafeInteger(field) || !Number.isSafeInteger(expected) || field < 0 || expected < field || size < field || size > expected) {
          throw new VibbitError('protocol', 'Upload file does not satisfy the OSS policy size limit')
        }
        sizeRestricted = true
      } else {
        if (typeof operator !== 'string' || typeof field !== 'string' || !field.startsWith('$')) throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy has an invalid condition')
        check(operator, field.slice(1), expected)
      }
    } else if (condition && typeof condition === 'object' && Object.keys(condition).length) {
      for (const [field, expected] of Object.entries(condition)) check('eq', field, expected)
    } else throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy has an invalid condition')
  }
  if (!keyRestricted || !sizeRestricted || !['x-oss-signature-version', 'x-oss-credential', 'x-oss-date', 'x-oss-security-token'].every(field => exact.has(field))) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD policy must constrain the object key, file size, and temporary signing fields')
  }
}

function safeFileName(file) {
  const name = path.basename(file).normalize('NFC').replace(/[\u0000-\u001f\u007f]/g, '_').trim()
  if (!name || name === '.' || name === '..') throw new VibbitError('input', 'Upload file name is empty')
  return name.slice(-240)
}

function contentTypeFor(fileName) {
  const extension = path.extname(fileName).toLowerCase()
  return {
    '.mp4': 'video/mp4', '.mov': 'video/quicktime', '.webm': 'video/webm', '.mkv': 'video/x-matroska',
    '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.m4a': 'audio/mp4', '.aac': 'audio/aac',
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp',
  }[extension] || 'application/octet-stream'
}

async function prepareUpload(file, signature) {
  const filePath = path.resolve(file)
  let stat
  try { stat = await fsp.stat(filePath) } catch { throw new VibbitError('input', 'Upload file does not exist or is not readable') }
  if (!stat.isFile()) throw new VibbitError('input', 'Upload file must be a regular file')
  if (stat.size > MAX_UPLOAD_BYTES) throw new VibbitError('input', `Upload file exceeds ${MAX_UPLOAD_BYTES} byte OSS limit`)
  const hostUrl = uploadDestination(signature.host)
  if (signature.bucket !== undefined && signature.bucket !== hostUrl.hostname.split('.')[0]) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD bucket does not match the OSS host')
  }
  if (signature.expire !== undefined && (!Number.isFinite(Number(signature.expire)) || Number(signature.expire) * 1000 <= Date.now())) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD temporary credentials are expired or have an invalid expiry')
  }
  const repaired = repairSigningRegion(signature)
  const dir = `${text(repaired.dir, 'dir').replace(/\/$/, '')}/`
  if (/[\\\u0000-\u001f\u007f]/.test(dir) || dir.slice(0, -1).split('/').some(part => !part || part === '.' || part === '..')) {
    throw new VibbitError('protocol', 'MATERIAL_UPLOAD returned an invalid object directory')
  }
  const fileName = safeFileName(filePath)
  const objectKey = `${dir}${Date.now()}_${crypto.randomUUID().slice(0, 8)}_${fileName}`
  const fields = {
    key: objectKey,
    policy: repaired.policy,
    'x-oss-signature-version': text(repaired.version, 'version'),
    'x-oss-credential': repaired.credential,
    'x-oss-date': text(repaired.xoss_date || repaired.xOssDate, 'xoss_date'),
    'x-oss-signature': text(repaired.signature || repaired.xOssSignature, 'signature'),
    'x-oss-security-token': text(repaired.security_token || repaired.securityToken, 'security_token'),
    success_action_status: '201',
  }
  if (fields['x-oss-signature-version'] !== 'OSS4-HMAC-SHA256') throw new VibbitError('protocol', 'MATERIAL_UPLOAD requires OSS V4 signing')
  validatePolicy(repaired.policy, fields, hostUrl, stat.size, fileName)
  const objectUrl = `${hostUrl.origin.replace(/\/$/, '')}/${objectKey.split('/').map(encodeURIComponent).join('/')}`
  return { filePath, stat, hostUrl, objectKey, objectUrl, fields, signingRegion: repaired.signingRegion, originalFileName: fileName }
}

function fieldPart(boundary, name, value) {
  return Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="${name}"\r\n\r\n${value}\r\n`)
}

function filePartHeader(boundary, fileName, contentType) {
  return Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName.replace(/"/g, '')}"\r\nContent-Type: ${contentType}\r\n\r\n`)
}

function postMultipart(plan) {
  const boundary = `----vibbit-${crypto.randomUUID()}`
  const parts = Object.entries(plan.fields).map(([name, value]) => fieldPart(boundary, name, value))
  const contentType = contentTypeFor(plan.originalFileName)
  const fileHeader = filePartHeader(boundary, plan.originalFileName, contentType)
  const trailer = Buffer.from(`\r\n--${boundary}--\r\n`)
  const contentLength = parts.reduce((sum, part) => sum + part.length, 0) + fileHeader.length + plan.stat.size + trailer.length
  return new Promise((resolve, reject) => {
    const request = https.request(plan.hostUrl, {
      method: 'POST',
      rejectUnauthorized: true,
      headers: {
        Accept: 'application/xml, text/plain, */*',
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': contentLength,
      },
    }, response => {
      // Consume without retaining or reflecting a body that may echo credentials.
      response.resume()
      response.on('error', () => reject(new VibbitError('transport', 'OSS upload response could not be read')))
      response.on('end', () => {
        if (![200, 201, 204].includes(response.statusCode)) {
          reject(new VibbitError('api', `OSS upload failed (HTTP ${response.statusCode})`, { http_status: response.statusCode }))
          return
        }
        resolve({ status: response.statusCode })
      })
    })
    request.setTimeout(30000, () => request.destroy(new Error('OSS upload timed out')))
    request.on('error', () => reject(new VibbitError('transport', 'OSS upload failed; check the network and TLS connection before retrying')))
    for (const part of parts) request.write(part)
    request.write(fileHeader)
    const stream = fs.createReadStream(plan.filePath)
    stream.on('error', error => { request.destroy(error) })
    stream.on('end', () => request.end(trailer))
    stream.pipe(request, { end: false })
  })
}

async function uploadLocalFile(file, signature) {
  const plan = await prepareUpload(file, signature)
  const response = await postMultipart(plan)
  return {
    ok: true,
    file: plan.filePath,
    file_name: plan.originalFileName,
    bytes: plan.stat.size,
    object_key: plan.objectKey,
    object_url: plan.objectUrl,
    signing_region: plan.signingRegion,
    oss_http_status: response.status,
    material_id: null,
    material_registration: 'not_available_from_public_openapi',
  }
}

function summarizeInstructions(signature) {
  return Object.fromEntries(['host', 'dir', 'bucket', 'region', 'expire'].filter(key => signature?.[key] !== undefined).map(key => [key, signature[key]]))
}

module.exports = { MAX_UPLOAD_BYTES, normalizeRegion, regionFromHost, repairSigningRegion, prepareUpload, uploadLocalFile, summarizeInstructions, contentTypeFor }
