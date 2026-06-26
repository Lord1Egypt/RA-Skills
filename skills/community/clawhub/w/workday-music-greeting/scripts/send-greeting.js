#!/usr/bin/env node
'use strict';

/**
 * Standalone greeting email sender.
 * Usage:
 *   node send-greeting.js --slot morning
 *   node send-greeting.js --test
 */

const path = require('path');
try { require('dotenv').config({ path: path.resolve(__dirname, '..', '.env') }); } catch {}

const gifs = require('./gifs.json');

const GREETINGS = {
  morning:  { emoji: '🌅', title: 'Good Morning!',  body: 'Time to rise and shine ☀️',       signoff: 'Have a wonderful day! 🎶' },
  focus:    { emoji: '🔥', title: 'Focus Time!',     body: 'Deep work mode activated 🎯',     signoff: 'Stay in the zone! 🎶' },
  working:  { emoji: '💪', title: 'Keep Going!',     body: 'You\'re crushing it today 🚀',    signoff: 'Power through! 🎶' },
  chill:    { emoji: '🍵', title: 'Wind Down',       body: 'Time to relax and recharge 🧘',   signoff: 'Take it easy! 🎶' },
  off:      { emoji: '🌙', title: 'Good Evening!',   body: 'Great work today. Rest well 💤',  signoff: 'See you tomorrow! 🎶' },
};

async function send(slot) {
  const nodemailer = require('nodemailer');
  const g = GREETINGS[slot];
  if (!g) throw new Error(`Unknown slot: ${slot}`);

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
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
  });

  if (process.argv.includes('--test')) {
    await transporter.verify();
    console.log('✅ SMTP connection OK');
    return;
  }

  const to = process.env.GREETING_TO;
  if (!to) throw new Error('GREETING_TO env var is required');

  await transporter.sendMail({
    from: process.env.GREETING_FROM || process.env.SMTP_USER,
    to,
    subject,
    html,
  });

  console.log(`✅ Sent: ${subject}`);
}

const args = process.argv.slice(2);
const slotIdx = args.indexOf('--slot');
const slot = slotIdx >= 0 ? args[slotIdx + 1] : 'morning';

send(slot).catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
