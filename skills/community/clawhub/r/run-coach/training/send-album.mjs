// send-album.mjs — Send PNG(s) as Telegram photo(s)
//
// Single image: sendPhoto (appears in Telegram Photos tab).
//   Falls back to sendDocument if image exceeds Telegram's dimension limit.
// Multiple images: sendMediaGroup (album, up to 10 photos).
//
// Usage: node send-album.mjs <caption> <chatId> <botToken> <img1.png> [img2.png ...]

import { readFileSync } from 'fs';

const [,, caption, chatId, botToken, ...pngFiles] = process.argv;

if (!pngFiles.length) {
  console.log('Usage: node send-album.mjs <caption> <chatId> <botToken> <img1.png> [img2.png ...]');
  process.exit(1);
}

const API = `https://api.telegram.org/bot${botToken}`;

if (pngFiles.length === 1) {
  // Single image: try sendPhoto, fallback to sendDocument
  const form = new FormData();
  form.append('chat_id', chatId);
  form.append('caption', caption);
  form.append('photo', new Blob([readFileSync(pngFiles[0])], { type: 'image/png' }), 'photo.png');

  const res = await fetch(`${API}/sendPhoto`, { method: 'POST', body: form });
  const data = await res.json();

  if (!data.ok) {
    if (data.description?.includes('PHOTO_INVALID_DIMENSIONS') || data.description?.includes('photo is too big')) {
      console.log('Photo too large, sending as document...');
      const fallbackForm = new FormData();
      fallbackForm.append('chat_id', chatId);
      fallbackForm.append('caption', caption);
      fallbackForm.append('document', new Blob([readFileSync(pngFiles[0])], { type: 'image/png' }), 'plan.png');
      const fallbackRes = await fetch(`${API}/sendDocument`, { method: 'POST', body: fallbackForm });
      const fallbackData = await fallbackRes.json();
      if (!fallbackData.ok) throw new Error(fallbackData.description);
      console.log('Sent as document (full quality)');
    } else {
      throw new Error(data.description);
    }
  } else {
    console.log('Photo sent');
  }
} else {
  // Multiple images: sendMediaGroup
  const form = new FormData();
  form.append('chat_id', chatId);
  const mediaJson = pngFiles.map((f, i) => ({
    type: 'photo',
    media: `attach://photo${i}`,
    ...(i === 0 ? { caption } : {})
  }));
  form.append('media', JSON.stringify(mediaJson));
  pngFiles.forEach((f, i) => {
    form.append(`photo${i}`, new Blob([readFileSync(f)], { type: 'image/png' }), `photo${i}.png`);
  });

  const res = await fetch(`${API}/sendMediaGroup`, { method: 'POST', body: form });
  const data = await res.json();
  if (!data.ok) throw new Error(data.description);
  console.log(`Album sent (${pngFiles.length} photos)`);
}
