#!/usr/bin/env node
/**
 * SafeHub — OpenClaw skill that scans other skills for malware and security issues.
 * Entry point: wires CLI commands (scan, report, update) via commander.
 */

const { Command } = require('commander');
const { runScan } = require('./commands/scan');
const { showReport } = require('./commands/report');
const { updateRules } = require('./commands/update');
const { typeOut, runWithLoading } = require('./lib/cliEffects');

const useTypingEffect = process.env.SAFEHUB_NO_TYPING !== '1' && process.stdout.isTTY;

const program = new Command();

program
  .name('safehub')
  .description('Scan OpenClaw skills for malware and security issues before installing')
  .version(require('./package.json').version);

/** Registers the scan command: openclaw run safehub scan <target> */
program
  .command('scan <target>')
  .description('Scan a skill by name, path, or GitHub URL')
  .option('--no-sandbox', 'Skip Docker sandbox (static analysis only)')
  .action(async (target, opts) => {
    try {
      const run = () => runScan(target, { skipSandbox: opts.sandbox === false });
      const result = useTypingEffect
        ? await runWithLoading(run(), 'Scanning', target)
        : await run();

      if (useTypingEffect) {
        await typeOut(result.formatted, { chunkSize: 3, delayMs: 6 });
      } else {
        console.log(result.formatted);
      }
    } catch (err) {
      console.error('Error:', err.message);
      process.exitCode = 1;
    }
  });

/** Registers the report command: openclaw run safehub report <skill-name> */
program
  .command('report <skill-name>')
  .description('Show last scan report for a skill without rescanning')
  .action(async (skillName) => {
    try {
      const report = await showReport(skillName);
      if (report) {
        if (useTypingEffect) {
          await typeOut(report, { chunkSize: 3, delayMs: 6 });
        } else {
          console.log(report);
        }
      } else {
        console.log(`No cached report for "${skillName}". Run 'safehub scan ${skillName}' first.`);
      }
    } catch (err) {
      console.error('Error:', err.message);
      process.exitCode = 1;
    }
  });

/** Registers the update command: openclaw run safehub update */
program
  .command('update')
  .description('Pull latest Semgrep scanner rules from SafeHub repo')
  .action(async () => {
    try {
      const result = await updateRules();
      if (result.updated) {
        const fileList = result.files && result.files.length ? ` (${result.files.length} rules)` : '';
        console.log(`Rules updated successfully${fileList}.`);
      } else {
        console.log(result.message || 'No updates. Rules are in ./rules');
      }
    } catch (err) {
      console.error('Error:', err.message);
      process.exitCode = 1;
    }
  });

program.parse();
