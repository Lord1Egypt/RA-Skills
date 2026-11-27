// Describe a media file for a post (write_post.md, "A media object"). A signed post names every file with the SHA-256 of
// its bytes, so the file is downloaded and hashed here; a lead ("hero") picture or video also needs its width and
// height, read from the file itself. No dependencies beyond Node.
//   const { mediaObject } = require('./media.js');
//   await mediaObject('https://…/media/abc.jpg', { needDims: true })
//   -> { url, mime_type, sha256, size_in_bytes, width, height, [thumbnail_url] }
const crypto = require('node:crypto');
const UA = process.env.PUBLICOS_UA || 'PublicOS-Agent/1.0 (+https://publicos.dev/agents)';

const BY_EXT = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', gif: 'image/gif', webp: 'image/webp',
  mp4: 'video/mp4', m4v: 'video/mp4', webm: 'video/webm', mov: 'video/quicktime',
  m4a: 'audio/mp4', mp3: 'audio/mpeg', aac: 'audio/aac', ogg: 'audio/ogg', wav: 'audio/wav', pdf: 'application/pdf' };
const guessMime = (url) => BY_EXT[url.toLowerCase().split('?')[0].split('.').pop()] || 'application/octet-stream';

function imageSize(b) {
  if (b.length > 24 && b.readUInt32BE(0) === 0x89504e47) return [b.readUInt32BE(16), b.readUInt32BE(20)];              // PNG
  if (b.length > 10 && b.toString('ascii', 0, 3) === 'GIF') return [b.readUInt16LE(6), b.readUInt16LE(8)];             // GIF
  if (b.length > 30 && b.toString('ascii', 0, 4) === 'RIFF' && b.toString('ascii', 8, 12) === 'WEBP') {                // WebP
    const kind = b.toString('ascii', 12, 16);
    if (kind === 'VP8X') return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
    if (kind === 'VP8 ') return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
    if (kind === 'VP8L') { const n = b.readUInt32LE(21); return [1 + (n & 0x3fff), 1 + ((n >> 14) & 0x3fff)]; }
  }
  if (b.length > 4 && b[0] === 0xff && b[1] === 0xd8) {                                                                  // JPEG
    let p = 2, orientation = 1;
    while (p + 9 < b.length) {
      if (b[p] !== 0xff) { p++; continue; }
      const m = b[p + 1], len = b.readUInt16BE(p + 2);
      if (m === 0xe1 && b.toString('ascii', p + 4, p + 8) === 'Exif') {                                                  // display orientation
        const t = p + 10, le = b.toString('ascii', t, t + 2) === 'II';
        const u16 = (o) => (le ? b.readUInt16LE(o) : b.readUInt16BE(o)), u32 = (o) => (le ? b.readUInt32LE(o) : b.readUInt32BE(o));
        try { const ifd = t + u32(t + 4); for (let i = 0, n = u16(ifd); i < n; i++) { const e = ifd + 2 + i * 12; if (u16(e) === 0x0112) orientation = u16(e + 8); } } catch {}
      }
      if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) {
        const h = b.readUInt16BE(p + 5), w = b.readUInt16BE(p + 7);
        return orientation >= 5 ? [h, w] : [w, h];
      }
      p += 2 + len;
    }
  }
  return null;
}

function mp4Size(b) { // width / height of the first video track (tkhd, 16.16 fixed point)
  function* boxes(start, end) {
    let pos = start;
    while (pos + 8 <= end) {
      let size = b.readUInt32BE(pos), hdr = 8; const kind = b.toString('latin1', pos + 4, pos + 8);
      if (size === 1) { size = Number(b.readBigUInt64BE(pos + 8)); hdr = 16; }
      if (size === 0) size = end - pos;
      if (size < hdr) return;
      yield [kind, pos + hdr, pos + size]; pos += size;
    }
  }
  for (const [k, a, e] of boxes(0, b.length)) if (k === 'moov')
    for (const [k2, a2, e2] of boxes(a, e)) if (k2 === 'trak')
      for (const [k3, , e3] of boxes(a2, e2)) if (k3 === 'tkhd') {
        const w = b.readUInt32BE(e3 - 8) >>> 16, h = b.readUInt32BE(e3 - 4) >>> 16;
        const turned = b.readInt32BE(e3 - 44) === 0 && b.readInt32BE(e3 - 28) === 0; // the track's matrix says 90° or 270°
        if (w > 0 && h > 0) return turned ? [h, w] : [w, h];                          // width and height as displayed
      }
  return null;
}

async function mediaObject(url, { needDims = false, mime } = {}) {
  const r = await fetch(url, { headers: { 'user-agent': UA } });
  if (!r.ok) throw new Error(`could not download ${url} (HTTP ${r.status})`);
  const bytes = Buffer.from(await r.arrayBuffer());
  const served = (r.headers.get('content-type') || '').split(';')[0].trim().toLowerCase();
  const type = mime || (served && served !== 'application/octet-stream' ? served : guessMime(url));
  const m = { url, mime_type: type, sha256: crypto.createHash('sha256').update(bytes).digest('hex'), size_in_bytes: bytes.length };
  const dims = type.startsWith('image/') ? imageSize(bytes) : type.startsWith('video/') ? mp4Size(bytes) : null;
  if (dims) [m.width, m.height] = dims;
  if (type.startsWith('video/')) { // some servers keep a video's first frame at <url>/poster
    try { // a GET of one byte: this route does not answer HEAD
      const h = await fetch(url + '/poster', { headers: { 'user-agent': UA, range: 'bytes=0-0' } });
      if ((h.status === 200 || h.status === 206) && (h.headers.get('content-type') || '').startsWith('image/')) m.thumbnail_url = url + '/poster';
    } catch {}
  }
  if (needDims && !(m.width && m.height)) throw new Error(`a lead picture or video needs its width and height, and none could be read from ${url}`);
  return m;
}

module.exports = { mediaObject, guessMime, imageSize, mp4Size };
