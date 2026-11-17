import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';

export function findPackageManagerEntry(command, directories) {
  for (const directory of directories) {
    const entry = join(directory, 'node_modules', 'npm', 'bin', `${command}-cli.js`);
    if (existsSync(entry)) return entry;
  }
  return null;
}

export function spawnPackageManager(command, args, options) {
  if (process.platform !== 'win32') return spawnSync(command, args, options);
  // Run the npm JavaScript entry with Node, avoiding .cmd execution and shell quoting.
  const directories = [dirname(process.execPath), ...(process.env.PATH || '').split(';')]
    .map(value => value.replace(/^"|"$/g, '')).filter(Boolean);
  const entry = findPackageManagerEntry(command, directories);
  if (!entry) throw new Error(`Cannot locate ${command}-cli.js in the Node/npm installation. Repair Node.js/npm and reopen the terminal.`);
  return spawnSync(process.execPath, [entry, ...args], options);
}
