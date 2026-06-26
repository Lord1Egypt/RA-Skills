export {};

// Inject --format messenger before briefReconcile reads argv
if (!process.argv.includes('--format')) {
  process.argv.push('--format', 'messenger');
}

// eslint-disable-next-line @typescript-eslint/no-require-imports
require('./briefReconcile');
