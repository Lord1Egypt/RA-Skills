#!/usr/bin/env node

const path = require('path');

const { enable, disable } = require('./hooks/flag');

function showHelp() {
  console.log(`fasterizy — direct prose for agent planning and docs

Usage:
  npx fasterizy install           Interactive multi-agent install
  npx fasterizy install --agents opencode,openclaw,cursor
  npx fasterizy update            Refresh npx-skills installs from GitHub; print plugin update hints
  npx fasterizy start             Enable runtime flag in the Claude config dir
  npx fasterizy stop              Disable runtime flag
  npx fasterizy status            Flag state, version, detected installs
  npx fasterizy promote-to-plugin Install fasterizy as native Claude Code plugin (visible in /plugin)
  npx fasterizy uninstall-hooks   Remove Claude Code hook entries (use after promote-to-plugin)
`);
}

async function main() {
  const cmd = process.argv[2];
  const args = process.argv.slice(3);

  switch (cmd) {
    case 'install':
      await require('./cli/install')(args);
      break;
    case 'update':
      require('./cli/update')();
      break;
    case 'start':
      enable();
      console.log('fasterizy: ON');
      break;
    case 'stop':
      disable();
      console.log('fasterizy: OFF');
      break;
    case 'status':
      require('./cli/status')();
      break;
    case 'promote-to-plugin': {
      const { installAsClaudePlugin } = require('./cli/install-plugin');
      const r = installAsClaudePlugin();
      console.log('fasterizy installed as a native Claude Code plugin.');
      console.log('  marketplace:', r.marketplacePath);
      console.log('  installPath:', r.installPath);
      console.log('  version:    ', r.shortSha, '(', r.fullSha, ')');
      if (r.strippedHooksFromSettings) {
        console.log('  stripped fasterizy hook entries from settings.json');
      }
      if (r.removedHookFiles.length) {
        console.log('  removed old hook files:');
        for (const f of r.removedHookFiles) console.log('    ' + f);
      }
      console.log('Restart Claude Code. fasterizy will appear in /plugin and load via the plugin path.');
      break;
    }
    case 'uninstall-hooks': {
      const { uninstallClaudeCodeHooks } = require('./cli/install-hooks');
      const r = uninstallClaudeCodeHooks();
      if (r.removedFiles.length) {
        console.log('Removed hook files:');
        for (const f of r.removedFiles) console.log('  ' + f);
      } else {
        console.log('No fasterizy hook files found in ~/.claude/hooks/.');
      }
      if (r.settingsChanged) {
        console.log('Stripped fasterizy entries from settings.json.');
        if (r.backup) console.log('  backup:', r.backup);
      } else {
        console.log('No fasterizy entries in settings.json.');
      }
      console.log('Restart Claude Code for changes to take effect.');
      break;
    }
    case '-h':
    case '--help':
    case undefined:
      showHelp();
      process.exit(cmd === undefined ? 1 : 0);
      break;
    default:
      console.error('Unknown command:', cmd);
      showHelp();
      process.exit(1);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
