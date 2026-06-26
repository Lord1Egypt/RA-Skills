/**
 * `voiceai-vo build` — the main "wow" command.
 * Reads a script, chunks it, renders TTS, stitches master, generates outputs.
 */
import { resolve, extname, dirname, join } from 'node:path';
import chalk from 'chalk';
import { VoiceAIClient, getApiKey, resolveVoiceId } from '../api.js';
import { chunkScript, type ChunkMode, type TemplateName } from '../chunking.js';
import { renderSegments } from '../render.js';
import {
  checkFfmpeg,
  stitchSegments,
  encodeToMp3,
  normalizeLoudness,
  muxAudioVideo,
  generateMuxScripts,
  type SyncPolicy,
  type MuxResult,
} from '../ffmpeg.js';
import { writeAllOutputs } from '../outputs.js';
import { slugify, ensureDir, readTextFile, fileExists } from '../utils.js';

/* ------------------------------------------------------------------ */
/*  Option types                                                       */
/* ------------------------------------------------------------------ */

export interface BuildOptions {
  input: string;
  voice: string;
  title?: string;
  template?: string;
  mode?: string;
  maxChars?: string;
  language?: string;
  video?: string;
  mux?: boolean;
  sync?: string;
  force?: boolean;
  mock?: boolean;
  out?: string;
}

/* ------------------------------------------------------------------ */
/*  Command handler                                                    */
/* ------------------------------------------------------------------ */

export async function buildCommand(opts: BuildOptions): Promise<void> {
  const startTime = Date.now();

  // ── Validate inputs ────────────────────────────────────────────────
  if (!opts.input) {
    console.error(chalk.red('✗ --input is required. Pass a .txt or .md script file.'));
    process.exit(1);
  }

  const inputPath = resolve(opts.input);
  if (!(await fileExists(inputPath))) {
    console.error(chalk.red(`✗ Script not found: ${inputPath}`));
    process.exit(1);
  }

  const rawVoice = opts.voice;
  if (!rawVoice) {
    console.error(chalk.red('✗ --voice is required. Run `voiceai-vo voices` to see options.'));
    process.exit(1);
  }
  // Resolve alias ("ellie") or pass through UUID
  const voiceId = resolveVoiceId(rawVoice);

  const isMock = opts.mock ?? false;

  // API key check (only when not in mock mode)
  const apiKey = getApiKey();
  if (!isMock && !apiKey) {
    console.error(
      chalk.red('✗ VOICE_AI_API_KEY not set.\n') +
        chalk.yellow('  Set it in .env or your environment, or use --mock for testing.\n') +
        chalk.gray('  Get your key at https://voice.ai/dashboard'),
    );
    process.exit(1);
  }

  // ── Resolve settings ──────────────────────────────────────────────
  const ext = extname(inputPath).toLowerCase();
  const template = opts.template as TemplateName | undefined;
  const mode: ChunkMode = (opts.mode as ChunkMode) ?? (ext === '.md' ? 'headings' : 'auto');
  const maxChars = parseInt(opts.maxChars ?? '1500', 10);
  const language = opts.language ?? 'en';
  const force = opts.force ?? false;
  const syncPolicy: SyncPolicy = (opts.sync as SyncPolicy) ?? 'shortest';

  // Title → slug → output dir
  const rawTitle = opts.title ?? inputPath.replace(/^.*[\\/]/, '').replace(/\.[^.]+$/, '');
  const titleSlug = slugify(rawTitle);
  const outputDir = opts.out ? resolve(opts.out) : resolve('out', titleSlug);
  await ensureDir(outputDir);

  // Template directory (look for templates/ relative to cwd, or fallback to script location)
  const templateDir = resolve(process.cwd(), 'templates');

  // ── Print header ──────────────────────────────────────────────────
  console.log(chalk.bold('\n╔══════════════════════════════════════════════════╗'));
  console.log(chalk.bold('║') + chalk.cyan.bold('   Voice.ai Creator Voiceover Pipeline             ') + chalk.bold('║'));
  console.log(chalk.bold('╚══════════════════════════════════════════════════╝'));
  if (isMock) console.log(chalk.yellow.bold('   ⚡ Mock mode — no API calls will be made\n'));

  console.log(chalk.gray(`   Script:   ${inputPath}`));
  console.log(chalk.gray(`   Voice:    ${voiceId}`));
  console.log(chalk.gray(`   Mode:     ${mode} (max ${maxChars} chars)`));
  if (template) console.log(chalk.gray(`   Template: ${template}`));
  console.log(chalk.gray(`   Output:   ${outputDir}`));
  if (opts.video) console.log(chalk.gray(`   Video:    ${opts.video}`));

  // ── Initialize client ─────────────────────────────────────────────
  const client = new VoiceAIClient({ apiKey: apiKey ?? undefined, mock: isMock });

  // ── Read & chunk script ───────────────────────────────────────────
  console.log(chalk.cyan('\n📄 Reading script…'));
  const scriptContent = await readTextFile(inputPath);

  const segments = await chunkScript(scriptContent, {
    mode,
    maxChars,
    language,
    template,
    templateDir,
    voiceId,
  });

  console.log(chalk.green(`   ✅ ${segments.length} segments extracted`));
  for (const seg of segments) {
    const tag = seg.source === 'template' ? chalk.yellow(' [template]') : '';
    console.log(chalk.gray(`      ${String(seg.index).padStart(2)}. ${seg.title}${tag}`));
  }

  // ── Render segments via TTS ───────────────────────────────────────
  const results = await renderSegments(segments, client, {
    voiceId,
    outputDir,
    force,
    mock: isMock,
    language,
  });

  // ── Check ffmpeg availability ─────────────────────────────────────
  const ffAvail = await checkFfmpeg();
  let hasMaster = false;

  // ── Stitch master ─────────────────────────────────────────────────
  if (ffAvail.ffmpeg) {
    console.log(chalk.cyan('\n🎶 Stitching master audio…'));
    const segPaths = results.map((r) => r.filePath);
    const masterWav = join(outputDir, 'master.wav');

    const stitched = await stitchSegments(segPaths, masterWav);
    if (stitched) {
      hasMaster = true;
      console.log(chalk.green(`   ✅ master.wav`));

      // Try mp3 encode
      const masterMp3 = join(outputDir, 'master.mp3');
      const mp3Ok = await encodeToMp3(masterWav, masterMp3);
      if (mp3Ok) console.log(chalk.green(`   ✅ master.mp3`));

      // Try loudness normalization
      const normalizedWav = join(outputDir, 'master_normalized.wav');
      const normOk = await normalizeLoudness(masterWav, normalizedWav);
      if (normOk) console.log(chalk.green(`   ✅ master_normalized.wav (loudnorm -16 LUFS)`));
    } else {
      console.log(chalk.yellow('   ⚠ Stitching failed — segments are still available individually.'));
    }
  } else {
    console.log(
      chalk.yellow('\n⚠ ffmpeg not found — skipping master stitch.') +
        chalk.gray('\n   Segments are available individually in segments/.') +
        chalk.gray('\n   Install ffmpeg for stitching: https://ffmpeg.org/download.html'),
    );
  }

  // ── Video muxing (if requested) ──────────────────────────────────
  let muxResult: MuxResult | undefined;

  if (opts.video || opts.mux) {
    const videoPath = opts.video ? resolve(opts.video) : undefined;

    if (!videoPath || !(await fileExists(videoPath))) {
      console.error(chalk.red(`\n✗ Video file not found: ${videoPath ?? '(not specified)'}`));
    } else if (!hasMaster) {
      console.log(chalk.yellow('\n⚠ No master audio to mux. Skipping video muxing.'));
    } else if (ffAvail.ffmpeg) {
      const muxedPath = join(outputDir, 'muxed.mp4');
      muxResult = await muxAudioVideo({
        videoPath,
        audioPath: join(outputDir, 'master.wav'),
        outputPath: muxedPath,
        syncPolicy,
      });
    } else {
      console.log(chalk.yellow('\n⚠ ffmpeg required for muxing. Generating helper scripts…'));
      const masterPath = join(outputDir, 'master.wav');
      const muxedPath = join(outputDir, 'muxed.mp4');
      await generateMuxScripts(videoPath, masterPath, muxedPath, syncPolicy, outputDir);
      console.log(chalk.green('   ✅ Helper scripts generated in ffmpeg/'));
    }
  }

  // ── Generate all output files ─────────────────────────────────────
  console.log(chalk.cyan('\n📦 Generating output files…'));

  await writeAllOutputs({
    outputDir,
    title: rawTitle,
    voiceId,
    template: template,
    language,
    mock: isMock,
    results,
    segments,
    hasMaster,
    muxResult,
  });

  console.log(chalk.green('   ✅ manifest.json'));
  console.log(chalk.green('   ✅ timeline.json'));
  console.log(chalk.green('   ✅ review.html'));
  console.log(chalk.green('   ✅ description.txt'));
  if (results.some((r) => r.duration > 0)) {
    console.log(chalk.green('   ✅ chapters.txt'));
    console.log(chalk.green('   ✅ captions.srt'));
  }

  // ── Summary ───────────────────────────────────────────────────────
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  const totalDur = results.reduce((s, r) => s + r.duration, 0).toFixed(1);

  console.log(chalk.bold('\n╔══════════════════════════════════════════════════╗'));
  console.log(chalk.bold('║') + chalk.green.bold('   ✅ Build complete!                              ') + chalk.bold('║'));
  console.log(chalk.bold('╚══════════════════════════════════════════════════╝'));
  console.log(chalk.gray(`   Output:    ${outputDir}`));
  console.log(chalk.gray(`   Segments:  ${results.length}`));
  console.log(chalk.gray(`   Duration:  ${totalDur}s`));
  console.log(chalk.gray(`   Time:      ${elapsed}s`));
  if (muxResult?.success) console.log(chalk.gray(`   Video:     ${muxResult.outputPath}`));
  console.log(chalk.gray(`   Review:    ${join(outputDir, 'review.html')}`));
  console.log('');
}
