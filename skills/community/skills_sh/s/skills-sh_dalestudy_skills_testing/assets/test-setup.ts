// Vitest 글로벌 테스트 설정
// tests/setup.ts

import { expect, afterEach, beforeAll, afterAll } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';
import { server } from './mocks/server';

// jest-dom matchers 확장
expect.extend(matchers);

// 각 테스트 후 cleanup (자동이지만 명시적으로 설정)
afterEach(() => {
  cleanup();
});

// MSW 서버 설정
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
