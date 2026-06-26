import { runImport } from './commands/import.js';
import { runAnalyze } from './commands/analyze.js';
import { runPublish } from './commands/publish.js';
import { runUpdate } from './commands/update.js';
import { runDoctor } from './commands/doctor.js';
import { renderHelp } from './lib/help.js';

export async function run(args = []) {
  const [command, ...rest] = args;

  if (!command || command === '--help' || command === '-h' || command === 'help') {
    console.log(renderHelp());
    return;
  }

  if (command === '--version' || command === '-v' || command === 'version') {
    const { createRequire } = await import('node:module');
    const require = createRequire(import.meta.url);
    const pkg = require('../../package.json');
    console.log(`@agisecurity/ustack ${pkg.version}`);
    return;
  }

  if (command === 'import') {
    await runImport({ cwd: process.cwd(), args: rest });
    return;
  }

  if (command === 'analyze') {
    await runAnalyze({ cwd: process.cwd(), args: rest });
    return;
  }

  if (command === 'publish') {
    await runPublish({ cwd: process.cwd(), args: rest });
    return;
  }

  if (command === 'update') {
    await runUpdate({ cwd: process.cwd(), args: rest });
    return;
  }

  if (command === 'doctor') {
    await runDoctor({ cwd: process.cwd(), args: rest });
    return;
  }

  console.error(`Unknown command: ${command}`);
  console.log(renderHelp());
  process.exitCode = 1;
}
