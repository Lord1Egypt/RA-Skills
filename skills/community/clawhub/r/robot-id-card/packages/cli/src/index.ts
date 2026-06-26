#!/usr/bin/env node
/**
 * RIC CLI — Developer tool for managing bot identities
 *
 * Usage:
 *   ric keygen    — Generate a new Ed25519 keypair (step 1)
 *   ric register  — Register a new bot (step 2)
 *   ric status    — Check your bot's current grade
 *   ric verify    — Verify a bot by RIC ID
 *   ric report    — Report a bad bot
 */

import { Command } from 'commander'
import * as ed from '@noble/ed25519'
import { sha512 } from '@noble/hashes/sha2.js'
import { randomBytes } from 'crypto'
import * as fs from 'fs'

// @noble/ed25519 v2 requires sha512Sync to be set for Node.js
ed.etc.sha512Sync = (...m: Parameters<typeof sha512>) => sha512(...m)

const REGISTRY = process.env.RIC_REGISTRY || 'https://registry.robotidcard.dev'

const program = new Command()

// ──────────────────────────────────────────────
// ric keygen
// ──────────────────────────────────────────────
program
  .command('keygen')
  .description('Generate a new Ed25519 keypair for your bot')
  .option('--out <file>', 'Output key file', './bot.key.json')
  .action(async (opts) => {
    const privateKey = randomBytes(32)
    const publicKey = await ed.getPublicKey(privateKey)

    const keyFile = {
      private_key_hex: privateKey.toString('hex'),
      public_key: `ed25519:${Buffer.from(publicKey).toString('hex')}`,
      generated_at: new Date().toISOString(),
    }

    fs.writeFileSync(opts.out, JSON.stringify(keyFile, null, 2))

    console.log(`\n🔑 New Ed25519 keypair generated`)
    console.log(`   Public key: ${keyFile.public_key}`)
    console.log(`   Saved to:   ${opts.out}`)
    console.log(`\n⚠️  Keep ${opts.out} safe — it contains your private key!`)
    console.log(`   Next step: ric register --key ${opts.out} --name "MyBot" ...`)
  })

program.name('ric').description('Robot ID Card CLI').version('0.4.0')

// ──────────────────────────────────────────────
// ric register
// ──────────────────────────────────────────────
program
  .command('register')
  .description('Register a new bot and get your RIC certificate')
  .requiredOption('--name <name>', 'Bot name')
  .requiredOption('--purpose <purpose>', 'What your bot does (min 10 chars)')
  .requiredOption('--developer <email>', 'Developer email')
  .option('--org <org>', 'Organization name')
  .option('--version <ver>', 'Bot version', '1.0.0')
  .option('--capabilities <caps>', 'Comma-separated capabilities (read_articles,follow_links,...)', 'read_articles')
  .option('--key <file>', 'Use existing key file from `ric keygen`')
  .option('--out <file>', 'Output certificate file', './bot.ric.json')
  .action(async (opts) => {
    console.log('\n🤖 Robot ID Card — Bot Registration\n')

    // Load or generate keypair
    let privateKeyHex: string
    let publicKey: string

    if (opts.key) {
      if (!fs.existsSync(opts.key)) {
        console.error(`Key file not found: ${opts.key}`)
        console.error(`Generate one with: ric keygen --out ${opts.key}`)
        process.exit(1)
      }
      const keyFile = JSON.parse(fs.readFileSync(opts.key, 'utf8'))
      privateKeyHex = keyFile.private_key_hex
      publicKey = keyFile.public_key
    } else {
      const privBytes = randomBytes(32)
      const pubBytes = await ed.getPublicKey(privBytes)
      privateKeyHex = privBytes.toString('hex')
      publicKey = `ed25519:${Buffer.from(pubBytes).toString('hex')}`
    }

    const capabilities = opts.capabilities.split(',').map((c: string) => c.trim())
    const botName = opts.name

    const payload = {
      developer: {
        name: opts.developer.split('@')[0],
        email: opts.developer,
        org: opts.org,
      },
      bot: {
        name: botName,
        version: opts.version,
        purpose: opts.purpose,
        capabilities,
        user_agent: `${botName}/${opts.version} (RIC:pending)`,
      },
      public_key: publicKey,
    }

    try {
      const res = await fetch(`${REGISTRY}/v1/bots/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await res.json() as any

      if (!res.ok) {
        if (res.status === 409) {
          console.error(`\n❌ ${data.error}`)
          if (data.existing_id) console.error(`   Existing RIC ID: ${data.existing_id}`)
          if (data.hint) console.error(`   Hint: ${data.hint}`)
        } else {
          console.error('Registration failed:', data)
        }
        process.exit(1)
      }

      const { certificate } = data

      const config = { ...certificate, private_key_hex: privateKeyHex }
      fs.writeFileSync(opts.out, JSON.stringify(config, null, 2))

      console.log(`✅ Bot registered successfully!\n`)
      console.log(`   RIC ID:      ${certificate.id}`)
      console.log(`   Grade:       🟡 UNKNOWN (pending weekly review)`)
      console.log(`   Certificate: ${opts.out}`)
      console.log(`\n⚠️  Keep ${opts.out} safe — it contains your private key!`)
    } catch (e) {
      console.error('Failed to connect to registry:', e)
      process.exit(1)
    }
  })

// ──────────────────────────────────────────────
// ric status <ric_id>
// ──────────────────────────────────────────────
program
  .command('status [ric_id]')
  .description('Check a bot\'s current grade and certificate')
  .option('--cert <file>', 'Load RIC ID from certificate file')
  .action(async (ricId, opts) => {
    if (!ricId && opts.cert) {
      const cert = JSON.parse(fs.readFileSync(opts.cert, 'utf8'))
      ricId = cert.id
    }
    if (!ricId) {
      console.error('Provide a RIC ID or --cert file')
      process.exit(1)
    }

    const res = await fetch(`${REGISTRY}/v1/bots/${ricId}`)
    if (!res.ok) {
      console.error('Bot not found:', ricId)
      process.exit(1)
    }

    const cert = await res.json()
    const gradeEmoji = { healthy: '🟢', unknown: '🟡', dangerous: '🔴' }[cert.grade as string] || '⚪'

    console.log(`\n${gradeEmoji} ${cert.bot.name}  [${cert.grade.toUpperCase()}]\n`)
    console.log(`   ID:          ${cert.id}`)
    console.log(`   Developer:   ${cert.developer.name} <${cert.developer.email}>`)
    console.log(`   Purpose:     ${cert.bot.purpose}`)
    console.log(`   Created:     ${new Date(cert.created_at).toLocaleDateString()}`)
    console.log(`   Grade since: ${new Date(cert.grade_updated_at).toLocaleDateString()}\n`)
  })

// ──────────────────────────────────────────────
// ric report <ric_id>
// ──────────────────────────────────────────────
program
  .command('report <ric_id>')
  .description('Report a bot for bad behavior')
  .option('--reason <reason>', 'Reason: spam|scraping_violation|rate_limit_abuse|tos_violation')
  .option('--domain <domain>', 'Your domain (reporter)')
  .option('--desc <desc>', 'Description of the incident')
  .action(async (ricId, opts) => {
    const res = await fetch(`${REGISTRY}/v1/audit/report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ric_id: ricId,
        reporter_domain: opts.domain || 'unknown',
        reason: opts.reason || 'other',
        description: opts.desc || '',
      }),
    })

    const data = await res.json()
    if (res.ok) {
      console.log(`✅ Report submitted. ID: ${data.report_id}`)
    } else {
      console.error('Report failed:', data)
    }
  })

// ──────────────────────────────────────────────
// ric claim
// ──────────────────────────────────────────────
program
  .command('claim')
  .description('Claim your bot identity today (max 2×/day, 3 consecutive days → HEALTHY)')
  .option('--cert <file>', 'Certificate file from `ric register`', './bot.ric.json')
  .action(async (opts) => {
    if (!fs.existsSync(opts.cert)) {
      console.error(`Certificate file not found: ${opts.cert}`)
      process.exit(1)
    }

    const cert = JSON.parse(fs.readFileSync(opts.cert, 'utf8'))
    const { id, private_key_hex, public_key } = cert

    if (!id || !private_key_hex) {
      console.error('Invalid certificate file — missing id or private_key_hex')
      process.exit(1)
    }

    const date = new Date().toISOString().slice(0, 10)
    const message = `${id}:${date}`
    const msgBytes = new TextEncoder().encode(message)

    const privBytes = Buffer.from(private_key_hex, 'hex')
    const sigBytes = await ed.sign(msgBytes, privBytes)
    const signature = `ed25519:${Buffer.from(sigBytes).toString('hex')}`

    try {
      const res = await fetch(`${REGISTRY}/v1/bots/${id}/claim`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ signature, date }),
      })

      const data = await res.json() as any

      if (!res.ok) {
        console.error(`\n❌ ${data.error}`)
        if (data.message) console.error(`   ${data.message}`)
        process.exit(1)
      }

      const gradeEmoji = { healthy: '🟢', unknown: '🟡', dangerous: '🔴' }[data.grade as string] || '⚪'
      console.log(`\n${gradeEmoji} Identity claimed for ${id}`)
      console.log(`   Streak    : ${data.consecutive_days} consecutive day(s)`)
      console.log(`   Today     : ${data.today_count}/2 claims used`)
      console.log(`   Grade     : ${data.grade.toUpperCase()}`)
      if (data.grade_upgraded) {
        console.log(`\n🎉 Grade upgraded to HEALTHY!`)
      }
      if (data.certificate_type === 'code' && Array.isArray(data.award)) {
        console.log('\n' + data.award.join('\n'))
      }
    } catch (e) {
      console.error('Failed to connect to registry:', e)
      process.exit(1)
    }
  })

// ──────────────────────────────────────────────
// ric sign  (RFC 9421 — Web Bot Auth standard)
// ──────────────────────────────────────────────
program
  .command('sign')
  .description('Generate RFC 9421-compliant Signature + Signature-Input + Signature-Agent headers')
  .requiredOption('--cert <file>', 'Certificate file from `ric register`', './bot.ric.json')
  .requiredOption('--authority <authority>', 'Target host, e.g. "example.com"')
  .option('--method <method>', 'HTTP method', 'GET')
  .option('--path <path>', 'Request path, e.g. "/api/articles"', '/')
  .option('--label <label>', 'Signature label (default: ric)', 'ric')
  .option('--ttl <seconds>', 'Signature lifetime in seconds', '300')
  .action(async (opts) => {
    if (!fs.existsSync(opts.cert)) {
      console.error(`Certificate file not found: ${opts.cert}`)
      process.exit(1)
    }

    const cert = JSON.parse(fs.readFileSync(opts.cert, 'utf8'))
    const { id, private_key_hex } = cert

    if (!id || !private_key_hex) {
      console.error('Invalid certificate file — missing id or private_key_hex')
      process.exit(1)
    }

    const createdSec = Math.floor(Date.now() / 1000)
    const expiresSec = createdSec + parseInt(opts.ttl, 10)
    const nonce      = randomBytes(16).toString('base64url')
    const label      = opts.label
    const components = ['@authority', '@method', '@path']

    // Build signature params (the part after "label=" in Signature-Input)
    const sigInputParams = [
      `(${components.map((c) => `"${c}"`).join(' ')})`,
      `keyid="${id}"`,
      `created=${createdSec}`,
      `expires=${expiresSec}`,
      `nonce="${nonce}"`,
      `tag="web-bot-auth"`,
    ].join(';')

    // Build signature base (what gets signed)
    const sigBase = [
      `"@authority": ${opts.authority}`,
      `"@method": ${opts.method.toUpperCase()}`,
      `"@path": ${opts.path}`,
      `"@signature-params": ${sigInputParams}`,
    ].join('\n')

    const msgBytes  = new TextEncoder().encode(sigBase)
    const privBytes = Buffer.from(private_key_hex, 'hex')
    const sigBytes  = await ed.sign(msgBytes, privBytes)
    const sigB64    = Buffer.from(sigBytes).toString('base64')

    const signatureInput = `${label}=${sigInputParams}`
    const signature      = `${label}=:${sigB64}:`
    const signatureAgent = `"${cert.bot?.name ?? 'RIC-Bot'}"; cert="${REGISTRY}/v1/bots/${id}"`

    console.log('\n── RFC 9421 Request Headers ─────────────────────────────')
    console.log(`Signature-Input: ${signatureInput}`)
    console.log(`Signature: ${signature}`)
    console.log(`Signature-Agent: ${signatureAgent}`)
    console.log('─────────────────────────────────────────────────────────\n')
    console.log('Signature base (for debugging):')
    console.log(sigBase)
  })

program.parse()
