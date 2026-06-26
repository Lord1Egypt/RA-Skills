/**
 * `voiceai-vo voices` — discover available Voice.ai voices.
 */
import chalk from 'chalk';
import { VoiceAIClient, getApiKey } from '../api.js';

/* ------------------------------------------------------------------ */
/*  Option types                                                       */
/* ------------------------------------------------------------------ */

export interface VoicesOptions {
  limit?: string;
  query?: string;
  mock?: boolean;
}

/* ------------------------------------------------------------------ */
/*  Command handler                                                    */
/* ------------------------------------------------------------------ */

export async function voicesCommand(opts: VoicesOptions): Promise<void> {
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

  const client = new VoiceAIClient({ apiKey, mock: isMock });
  const limit = opts.limit ? parseInt(opts.limit, 10) : 20;
  const query = opts.query;

  console.log(chalk.bold('\n╔══════════════════════════════════════════════════╗'));
  console.log(chalk.bold('║') + chalk.cyan.bold('   Voice.ai — Available Voices                     ') + chalk.bold('║'));
  console.log(chalk.bold('╚══════════════════════════════════════════════════╝'));
  if (isMock) console.log(chalk.yellow('   ⚡ Mock mode\n'));

  try {
    const { voices, total } = await client.listVoices({ limit, query });

    if (voices.length === 0) {
      console.log(chalk.yellow('   No voices found.'));
      if (query) console.log(chalk.gray(`   Try a different search: --query "narrator"`));
      console.log('');
      return;
    }

    // Column widths
    const idW = Math.max(4, ...voices.map((v) => v.id.length));
    const nameW = Math.max(4, ...voices.map((v) => v.name.length));

    // Header
    console.log(
      chalk.gray(
        `   ${'ID'.padEnd(idW)}  ${'NAME'.padEnd(nameW)}  LANG  DESCRIPTION`,
      ),
    );
    console.log(chalk.gray(`   ${'─'.repeat(idW)}  ${'─'.repeat(nameW)}  ────  ─────────────`));

    // Rows
    for (const v of voices) {
      const id = chalk.cyan(v.id.padEnd(idW));
      const name = chalk.white.bold(v.name.padEnd(nameW));
      const lang = chalk.gray((v.language ?? '').padEnd(4));
      const desc = chalk.gray(v.description ?? v.style ?? '');
      console.log(`   ${id}  ${name}  ${lang}  ${desc}`);
    }

    console.log(chalk.gray(`\n   Showing ${voices.length} of ${total} voices.`));
    if (query) console.log(chalk.gray(`   Filter: "${query}"`));
    console.log(
      chalk.gray('\n   💡 Use a voice ID with: voiceai-vo build --voice <ID> --input <script>'),
    );
  } catch (err) {
    console.error(chalk.red(`\n✗ Failed to fetch voices: ${err}`));
    console.error(chalk.yellow('   Try --mock to see available mock voices.'));
    process.exit(1);
  }
  console.log('');
}
