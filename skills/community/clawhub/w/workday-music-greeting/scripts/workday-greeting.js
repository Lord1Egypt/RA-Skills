#!/usr/bin/env node
'use strict';

const path = require('path');
const { execSync } = require('child_process');

// Load .env if present
try { require('dotenv').config({ path: path.resolve(__dirname, '..', '.env') }); } catch {}

const slots = require('./slots.json');
const gifs = require('./gifs.json');

// ── Greeting templates ──────────────────────────────────────────────
const GREETINGS = {
  morning:  { emoji: '🌅', title: 'Good Morning!',  body: 'Time to rise and shine ☀️',       signoff: 'Have a wonderful day! 🎶' },
  focus:    { emoji: '🔥', title: 'Focus Time!',     body: 'Deep work mode activated 🎯',     signoff: 'Stay in the zone! 🎶' },
  working:  { emoji: '💪', title: 'Keep Going!',     body: 'You\'re crushing it today 🚀',    signoff: 'Power through! 🎶' },
  chill:    { emoji: '🍵', title: 'Wind Down',       body: 'Time to relax and recharge 🧘',   signoff: 'Take it easy! 🎶' },
  off:      { emoji: '🌙', title: 'Good Evening!',   body: 'Great work today. Rest well 💤',  signoff: 'See you tomorrow! 🎶' },
};

// ── Detect current slot ─────────────────────────────────────────────
function detectSlot() {
  const hour = new Date().getHours();
  for (const [name, range] of Object.entries(slots)) {
    if (range.start <= range.end) {
      if (hour >= range.start && hour < range.end) return name;
    } else {
      // wraps midnight (e.g. 18–6)
      if (hour >= range.start || hour < range.end) return name;
    }
  }
  return 'off';
}

// ── Switch music scene ──────────────────────────────────────────────
function switchScene(slot) {
  const cmd = process.env.MUSIC_CMD || 'home-music';
  try {
    execSync(`${cmd} ${slot}`, { stdio: 'inherit', timeout: 15000 });
    console.log(`✅ Music scene switched to: ${slot}`);
  } catch (err) {
    console.warn(`⚠️  Music scene switch failed: ${err.message}`);
  }
}

// ── Send greeting email ─────────────────────────────────────────────
async function sendGreeting(slot) {
  const nodemailer = require('nodemailer');
  const g = GREETINGS[slot];
  const gifUrl = gifs[slot] || '';

  const subject = `${g.emoji} ${g.title}`;
  const html = `
    <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
      <h2 style="color: #333;">${g.emoji} ${g.title}</h2>
      <p style="font-size: 16px;">${g.body}</p>
      <p style="font-size: 16px;">Switching to <strong>${slot}</strong> music scene.</p>
      ${gifUrl ? `<p><img src="${gifUrl}" alt="${g.title}" width="400" style="border-radius: 8px;" /></p>` : ''}
      <p style="font-size: 14px; color: #666;">${g.signoff}</p>
      <hr style="border: none; border-top: 1px solid #eee;" />
      <p style="font-size: 12px; color: #999;"><em>— Sent by Workday Music Greeting 🎶</em></p>
    </div>`;

  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT) || 587,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  const to = process.env.GREETING_TO;
  if (!to) throw new Error('GREETING_TO env var is required');

  await transporter.sendMail({
    from: process.env.GREETING_FROM || process.env.SMTP_USER,
    to,
    subject,
    html,
  });

  console.log(`✅ Greeting email sent: ${subject}`);
}

// ── Main ────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const forceSlot = args.includes('--slot') ? args[args.indexOf('--slot') + 1] : null;
  const musicOnly = args.includes('--music-only');
  const emailOnly = args.includes('--email-only');
  const dryRun = args.includes('--dry-run');

  const slot = forceSlot || detectSlot();
  const g = GREETINGS[slot];

  console.log(`\n🎶 Workday Music Greeting`);
  console.log(`   Slot: ${g.emoji} ${slot}`);
  console.log(`   Time: ${new Date().toLocaleTimeString()}\n`);

  if (dryRun) {
    console.log(`[DRY RUN] Would switch music to: ${slot}`);
    console.log(`[DRY RUN] Would send email: ${g.emoji} ${g.title}`);
    if (gifs[slot]) console.log(`[DRY RUN] GIF: ${gifs[slot]}`);
    return;
  }

  if (!emailOnly) switchScene(slot);
  if (!musicOnly) await sendGreeting(slot);

  console.log(`\n🎉 Done! ${g.signoff}\n`);
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
