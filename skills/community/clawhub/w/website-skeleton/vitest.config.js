import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tests/**/*.test.js'],
    exclude: [
      'node_modules',
      'packages',
      'edge-functions',
      'cloud-functions',
      'tests/integration',
    ],
    globals: true,
    environment: 'node',
  },
});
