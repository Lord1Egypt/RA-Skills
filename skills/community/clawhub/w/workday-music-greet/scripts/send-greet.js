#!/usr/bin/env node
'use strict';

const path = require('path');
const fs = require('fs');
const nodemailer = require('nodemailer');
require('dotenv').config({ path: path.resolve(__dirname, '..', '.env') });

const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8'));
const template = fs.readFileSync(path.join(__dirname, '..', 'assets', 'email-template.html'), 'utf8');

async function sendGreet(sceneKey) {
  const scene = config.scenes[sceneKey];
  if (!scene) {
    console.error(`Unknown scene: ${sceneKey}. Available: ${Object.keys(config.scenes).join(', ')}`);
    process.exit(1);
  }

  const html = template
    .replace(/\{\{GIF_URL\}\}/g, scene.gif)
    .replace(/\{\{SUBJECT\}\}/g, scene.subject)
    .replace(/\{\{GREETING\}\}/g, scene.greeting)
    .replace(/\{\{SCENE\}\}/g, sceneKey);

  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT) || 587,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  const to = process.env.GREET_TO || process.env.SMTP_USER;
  const info = await transporter.sendMail({
    from: process.env.SMTP_FROM || process.env.SMTP_USER,
    to,
    subject: scene.subject,
    html,
  });

  console.log(`✅ Greeting email sent for "${sceneKey}" → ${to} (id: ${info.messageId})`);
}

const sceneKey = process.argv[2];
if (!sceneKey) {
  console.error('Usage: node send-greet.js <scene-key>');
  process.exit(1);
}

sendGreet(sceneKey).catch(err => {
  console.error('❌ Failed to send greeting:', err.message);
  process.exit(1);
});