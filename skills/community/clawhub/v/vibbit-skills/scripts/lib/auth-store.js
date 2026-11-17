'use strict'

const fs = require('node:fs/promises')
const { constants } = require('node:fs')
const path = require('node:path')
const os = require('node:os')
const crypto = require('node:crypto')
const { normalizeBase, VibbitError } = require('./client')
const { profiles, getProfile, profileForBase, regionFromSite } = require('./account-profile')

const configError = () => new VibbitError('configuration', 'Credential storage must be a private, owned directory and regular file. Use host credential settings if private file storage is unavailable.')
function validKey(key) {
  return typeof key === 'string' && /^[\x21-\x7e]{1,4096}$/.test(key)
}
function environmentKey(env = process.env) {
  return (env.VIBBIT_API_KEY || env.VIBBIT_OPENAPI_KEY || '').trim()
}
function storageDirectory(env = process.env) {
  if (env.VIBBIT_CONFIG_DIR && !path.isAbsolute(env.VIBBIT_CONFIG_DIR)) throw configError()
  return env.VIBBIT_CONFIG_DIR || path.join(os.homedir(), '.vibbit', 'credentials')
}
function checkPrivate(stat, directory = false) {
  if (process.platform === 'win32' || stat.uid !== process.getuid?.() || (stat.mode & 0o077) !== 0 ||
    (directory ? !stat.isDirectory() : !stat.isFile() || stat.nlink !== 1 || stat.size > 16384)) throw configError()
}
async function privateDirectory(dir, create) {
  if (process.platform === 'win32') throw configError()
  if (create) await fs.mkdir(dir, { recursive: true, mode: 0o700 })
  checkPrivate(await fs.lstat(dir), true)
}
async function readPrivate(name, env) {
  if (process.platform === 'win32') return undefined
  const dir = storageDirectory(env)
  let handle
  try {
    await privateDirectory(dir, false)
    handle = await fs.open(path.join(dir, name), constants.O_RDONLY | constants.O_NOFOLLOW)
    checkPrivate(await handle.stat())
    return JSON.parse(await handle.readFile('utf8'))
  } catch (error) {
    if (error.code === 'ENOENT') return undefined
    throw configError()
  } finally { await handle?.close() }
}
async function writePrivate(name, data, env) {
  const dir = storageDirectory(env), file = path.join(dir, name)
  let temporary
  try {
    await privateDirectory(dir, true)
    try { checkPrivate(await fs.lstat(file)) } catch (error) { if (error.code !== 'ENOENT') throw error }
    temporary = path.join(dir, crypto.randomUUID() + '.tmp')
    const handle = await fs.open(temporary, 'wx', 0o600)
    try {
      await handle.writeFile(JSON.stringify(data) + '\n')
      await handle.sync()
    } finally { await handle.close() }
    await fs.rename(temporary, file)
  } catch { throw configError() }
  finally { if (temporary) await fs.rm(temporary, { force: true }).catch(() => {}) }
}
async function savedRegion(env) {
  const data = await readPrivate('account.json', env)
  if (!data) return undefined
  if (data.version !== 1 || !Object.hasOwn(profiles, data.region)) throw configError()
  return data.region
}
async function saveSelection(region, { env = process.env } = {}) {
  getProfile(region)
  await writePrivate('account.json', { version: 1, region }, env)
  return { region, selected: true }
}
async function readStored({ env = process.env, base = normalizeBase() } = {}) {
  // Saved credentials are never forwarded to a custom base or another region.
  const profile = profileForBase(base)
  if (!profile) return undefined
  const data = await readPrivate(profile.region + '.json', env)
  if (!data) return undefined
  if (data.version !== 1 || data.base !== base || !validKey(data.key)) throw configError()
  return { key: data.key, base, source: 'private_file' }
}
async function resolveAccount({ env = process.env, region, site } = {}) {
  const explicit = region || env.VIBBIT_REGION || undefined
  if (explicit) getProfile(explicit)
  const hint = regionFromSite(site)
  if (env.VIBBIT_BASE_URL) {
    const base = normalizeBase(env.VIBBIT_BASE_URL), profile = profileForBase(base)
    if (explicit && profile?.region !== explicit) throw new VibbitError('configuration', 'VIBBIT_BASE_URL does not match the selected region; update the host environment explicitly')
    return { base, region: profile?.region || 'custom', selection_source: 'environment' }
  }
  if (explicit) return { base: getProfile(explicit).apiBase, region: explicit, selection_source: 'explicit' }
  const saved = await savedRegion(env)
  if (saved) return { base: getProfile(saved).apiBase, region: saved, selection_source: 'saved' }
  // Version 2.15 credentials have no account.json. Preserve a single existing site.
  {
    const existing = []
    for (const profile of Object.values(profiles)) {
      if (await readStored({ env, base: profile.apiBase })) existing.push(profile.region)
    }
    if (existing.length === 1) return { base: getProfile(existing[0]).apiBase, region: existing[0], selection_source: 'legacy_saved' }
    if (existing.length > 1) throw new VibbitError('configuration', 'Both Vibbit sites have saved keys. Select one explicitly with --region cn or --region global; no request has been sent.')
  }
  const selected = hint || 'global'
  return { base: getProfile(selected).apiBase, region: selected, selection_source: hint ? 'site' : 'default' }
}
async function resolveCredential({ env = process.env, region, site, account } = {}) {
  const { base } = account || await resolveAccount({ env, region, site })
  const key = environmentKey(env)
  if (key) {
    if (!validKey(key)) throw new VibbitError('configuration', 'The configured API key has an invalid format')
    return { base, key, source: 'environment' }
  }
  return await readStored({ env, base }) || { base, source: 'missing' }
}
async function saveCredential(key, { env = process.env, region } = {}) {
  key = typeof key === 'string' ? key.trim() : key
  if (!validKey(key)) throw new VibbitError('input', 'Invalid API key format')
  const account = await resolveAccount({ env, region })
  const profile = getProfile(account.region)
  // Validate selection storage before replacing a previously verified key.
  await savedRegion(env)
  await writePrivate(profile.region + '.json', { version: 1, base: profile.apiBase, key }, env)
  await saveSelection(profile.region, { env })
  return { saved: true, source: 'private_file', base: profile.apiBase }
}
async function clearCredential({ env = process.env, region, account } = {}) {
  const selected = account || await resolveAccount({ env, region })
  getProfile(selected.region)
  const dir = storageDirectory(env)
  try {
    await privateDirectory(dir, false)
    const file = path.join(dir, selected.region + '.json')
    checkPrivate(await fs.lstat(file))
    await fs.unlink(file)
  } catch (error) { if (error.code !== 'ENOENT') throw configError() }
  return { ok: true, cleared: 'private_file', region: selected.region, environment_still_configured: !!environmentKey(env), server_key_revoked: false }
}

module.exports = { resolveAccount, resolveCredential, readStored, saveCredential, saveSelection, clearCredential, environmentKey, storageDirectory, validKey }
