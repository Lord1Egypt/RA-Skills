// Shared by the independently installable Uydi Skill and MCP distributions.
import { spawn } from 'node:child_process';
import { open } from 'node:fs/promises';
import { resolve } from 'node:path';

export const asrModels = {
  message: 'uydi-audio-3.1-asr-flash-message',
  file: 'uydi-audio-3.1-asr-flash-filetrans',
};

export function asrModelId(model) {
  const id = Object.hasOwn(asrModels, model) ? asrModels[model] : model;
  if (!Object.values(asrModels).includes(id)) throw new Error('Choose message or file, or use its full Uydi ASR model ID.');
  return id;
}

function canonicalWav(pcm) {
  const header = Buffer.alloc(44);
  header.write('RIFF', 0);
  header.writeUInt32LE(36 + pcm.length, 4);
  header.write('WAVEfmt ', 8);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(16000, 24);
  header.writeUInt32LE(32000, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write('data', 36);
  header.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([header, pcm]);
}

function readPcmWav(bytes) {
  if (bytes.length < 44 || bytes.toString('ascii', 0, 4) !== 'RIFF' ||
      bytes.toString('ascii', 8, 12) !== 'WAVE' || bytes.readUInt32LE(4) + 8 !== bytes.length) return null;
  let formatValid = false;
  let pcm = null;
  for (let offset = 12; offset + 8 <= bytes.length;) {
    const tag = bytes.toString('ascii', offset, offset + 4);
    const size = bytes.readUInt32LE(offset + 4);
    const start = offset + 8;
    if (start + size > bytes.length) return null;
    if (tag === 'fmt ') {
      formatValid = size >= 16 && bytes.readUInt16LE(start) === 1 && bytes.readUInt16LE(start + 2) === 1 &&
        bytes.readUInt32LE(start + 4) === 16000 && bytes.readUInt16LE(start + 14) === 16;
    } else if (tag === 'data') {
      if (pcm !== null || size % 2) return null;
      pcm = bytes.subarray(start, start + size);
    }
    offset = start + size + (size % 2);
  }
  return formatValid && pcm?.length ? pcm : null;
}

export async function asrAudio(path, model, signal) {
  if (typeof path !== 'string' || !path.trim()) throw new Error('Choose a local audio or video file.');
  const maxSeconds = asrModelId(model) === asrModels.message ? 60 : 1800;
  const maxBytes = maxSeconds * 32000;
  const tooLong = () => new Error('The recording exceeds this model’s ' + maxSeconds + '-second limit.');
  const localPath = resolve(path);
  const file = await open(localPath, 'r');
  try {
    const stat = await file.stat();
    if (!stat.isFile() || !stat.size) throw new Error('Choose a nonempty, regular media file.');
    if (stat.size <= maxBytes + 1024 * 1024) {
      const header = Buffer.alloc(12);
      await file.read(header, 0, header.length, 0);
      if (header.toString('ascii', 0, 4) === 'RIFF' && header.toString('ascii', 8, 12) === 'WAVE') {
        const pcm = readPcmWav(await file.readFile({ signal }));
        if (pcm) {
          if (pcm.length > maxBytes) throw tooLong();
          return canonicalWav(pcm);
        }
      }
    }
  } finally { await file.close(); }

  // Read the local container with seek support and output plain PCM so the WAV has real length fields.
  const child = spawn('ffmpeg', ['-nostdin', '-xerror', '-hide_banner', '-loglevel', 'error', '-protocol_whitelist', 'file,pipe',
    '-format_whitelist', 'wav,mp3,mov,matroska,webm,ogg,aac,flac,aiff,asf,avi,amr,mpeg,mpegts,ac3,eac3',
    '-i', localPath, '-map', '0:a:0', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', '-f', 's16le', 'pipe:1'],
    { stdio: ['ignore', 'pipe', 'ignore'], signal });
  return new Promise((done, reject) => {
    let size = 0;
    const chunks = [];
    child.stdout.on('data', chunk => {
      size += chunk.length;
      if (size > maxBytes) {
        child.kill('SIGKILL');
        reject(tooLong());
      } else chunks.push(chunk);
    });
    child.on('error', err => reject(err.code === 'ENOENT'
      ? new Error('Install ffmpeg for this format, or provide a 16 kHz mono 16-bit PCM WAV file.')
      : err));
    child.on('close', code => {
      if (code !== 0 || !size || size % 2) reject(new Error('Could not decode an audio track. Supply a valid recording or a 16 kHz mono PCM16 WAV.'));
      else done(canonicalWav(Buffer.concat(chunks, size)));
    });
  });
}
