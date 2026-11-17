#!/usr/bin/env node
/**
 * site-publisher — Serve and package static websites
 */

const { serveSite, packageSite } = require('./scripts/site');

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (cmd === 'serve' || cmd === '--serve') {
    const port = parseInt(args[1]) || 3000;
    const dir = args[2] || process.cwd();
    serveSite(port, dir).catch(err => {
      console.error('Serve failed:', err.message);
      process.exit(1);
    });
  } else if (cmd === 'package' || cmd === '--package') {
    const dir = args[1] || process.cwd();
    const output = args[2];
    try {
      packageSite(dir, output);
    } catch (e) {
      console.error('Package failed:', e.message);
      process.exit(1);
    }
  } else {
    console.log('Usage: site-publisher <serve|package> [options]');
    console.log('  serve <port> <dir>    Serve static site (default port 3000)');
    console.log('  package <dir> <out>   Package site into tar.gz');
    process.exit(0);
  }
}

module.exports = { serveSite, packageSite };
