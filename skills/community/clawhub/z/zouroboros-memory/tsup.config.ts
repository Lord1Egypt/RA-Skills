import { defineConfig } from 'tsup';

export default defineConfig([
  {
    entry: { index: 'src/index.ts' },
    format: ['esm'],
    dts: true,
    clean: true,
    external: ['better-sqlite3'],
  },
  {
    entry: { cli: 'src/cli.ts', 'mcp-server': 'src/mcp-server.ts' },
    format: ['esm'],
    external: ['better-sqlite3'],
  },
]);
