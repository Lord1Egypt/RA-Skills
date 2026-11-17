// Jest / Vitest 覆盖率配置模板
// Jest 用法：jest.config.js；Vitest 用法：vitest.config.ts（字段基本兼容）
module.exports = {
  testEnvironment: 'node',           // 前端用 'jsdom'
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
    '!src/**/index.{js,ts}',
  ],
  coverageThreshold: {
    // 核心模块高门槛；未达标则非零退出
    './src/core/': { lines: 90, branches: 85 },
    './src/': { lines: 80, branches: 70 },
  },
  coverageReporters: ['text', 'text-summary', 'lcov'],
};
