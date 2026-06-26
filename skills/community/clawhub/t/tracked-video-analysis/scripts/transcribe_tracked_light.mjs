import { pipeline } from '@xenova/transformers';
import { execFileSync } from 'child_process';
import ffmpegPath from 'ffmpeg-static';
import fs from 'fs';
import pkg from 'wavefile';
const { WaveFile } = pkg;

const BASE = process.argv[2] || process.cwd();
const VIDEO = `${BASE}/video.mp4`;
const OUTPUT = `${BASE}/transcript.jsonl`;
const STATUS = `${BASE}/status.json`;
const ANALYSIS = `${BASE}/analysis.md`;
const LOG = `${BASE}/progress.log`;
const CHUNK = 15;
const MODEL = 'Xenova/whisper-tiny';

function writeStatus(patch) {
  let current = {};
  try { current = JSON.parse(fs.readFileSync(STATUS, 'utf8')); } catch {}
  fs.writeFileSync(STATUS, JSON.stringify({ ...current, ...patch, updatedAt: new Date().toISOString() }, null, 2));
}
function log(line) { fs.appendFileSync(LOG, line + '\n'); }
function probeDuration() {
  const ffprobe = require('ffprobe-static').path;
  const out = execFileSync(ffprobe, ['-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1', VIDEO], {encoding:'utf8'}).trim();
  return Math.ceil(Number(out));
}

fs.writeFileSync(OUTPUT, '');
fs.writeFileSync(LOG, '');
fs.writeFileSync(ANALYSIS, '# Video analysis\n\n_In progress..._\n');
writeStatus({ stage: 'starting', percent: 0, message: `Loading ${MODEL}` });
log(`Loading ${MODEL}`);
const transcriber = await pipeline('automatic-speech-recognition', MODEL, { quantized: true });
const DURATION = probeDuration();
const totalChunks = Math.ceil(DURATION / CHUNK);
writeStatus({ stage: 'transcribing', percent: 1, message: 'Model loaded', durationSeconds: DURATION, totalChunks, completedChunks: 0 });
log(`Model loaded, duration=${DURATION}, totalChunks=${totalChunks}`);

for (let i = 0, start = 0; start < DURATION; i++, start += CHUNK) {
  const end = Math.min(start + CHUNK, DURATION);
  const chunkFile = `${BASE}/chunk_${start}.wav`;
  try {
    log(`Extracting ${start}-${end}s`);
    execFileSync(ffmpegPath, ['-v','error','-y','-i', VIDEO, '-ss', String(start), '-t', String(end - start), '-ar','16000','-ac','1','-f','wav', chunkFile], { stdio: 'pipe' });
    const wav = new WaveFile(fs.readFileSync(chunkFile));
    wav.toBitDepth('32f');
    wav.toSampleRate(16000);
    const samples = wav.getSamples(false, Float32Array);
    const result = await transcriber(samples, { language: 'russian', task: 'transcribe' });
    fs.appendFileSync(OUTPUT, JSON.stringify({ start, end, text: result.text }) + '\n');
    fs.unlinkSync(chunkFile);
    const completedChunks = i + 1;
    const percent = Math.min(95, Math.round((completedChunks / totalChunks) * 95));
    writeStatus({ stage: 'transcribing', percent, completedChunks, currentRange: `${start}-${end}s`, message: result.text.slice(0, 100) });
    log(`[${start}-${end}s] ${result.text}`);
  } catch (error) {
    try { if (fs.existsSync(chunkFile)) fs.unlinkSync(chunkFile); } catch {}
    log(`ERROR ${start}-${end}s :: ${String(error)}`);
    writeStatus({ stage: 'error', currentRange: `${start}-${end}s`, message: 'Chunk failed', lastError: String(error), completedChunks: i });
    process.exit(1);
  }
}

const lines = fs.readFileSync(OUTPUT, 'utf8').trim().split('\n').filter(Boolean).map(x => JSON.parse(x));
const draft = lines.slice(0, 40).map(x => `- [${x.start}-${x.end}s] ${x.text}`).join('\n');
fs.writeFileSync(ANALYSIS, `# Video analysis\n\n## Transcript draft\n\n${draft}\n`);
writeStatus({ stage: 'extraction_done', percent: 100, completedChunks: totalChunks, message: 'Content extraction finished' });
log('Extraction finished');
