import { defineConfig } from 'tsup';

export default defineConfig({
  entry: {
    'adapters/longmemeval-adapter': 'src/adapters/longmemeval-adapter.ts',
    'adapters/locomo-adapter': 'src/adapters/locomo-adapter.ts',
    'adapters/convomem-adapter': 'src/adapters/convomem-adapter.ts',
    'adapters/mimir-judge': 'src/adapters/mimir-judge.ts',
    'scripts/run-all': 'src/scripts/run-all.ts',
    'scripts/report': 'src/scripts/report.ts',
  },
  format: ['esm'],
  external: ['better-sqlite3'],
  clean: true,
});
