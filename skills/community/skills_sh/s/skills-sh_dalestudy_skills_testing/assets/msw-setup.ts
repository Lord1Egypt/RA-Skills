// MSW (Mock Service Worker) 설정
// tests/mocks/server.ts

import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// API 핸들러 정의
export const handlers = [
  // 예시: GET /api/users
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ]);
  }),

  // 예시: POST /api/login
  http.post('/api/login', async ({ request }) => {
    const { email, password } = await request.json();

    if (email === 'user@example.com' && password === 'password123') {
      return HttpResponse.json({
        token: 'fake-jwt-token',
        user: { id: 1, email },
      });
    }

    return HttpResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    );
  }),

  // 예시: 에러 응답
  http.get('/api/error', () => {
    return HttpResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }),
];

// MSW 서버 생성
export const server = setupServer(...handlers);

// 테스트 내에서 핸들러 오버라이드 예시:
// import { server } from './mocks/server';
// import { http, HttpResponse } from 'msw';
//
// test('에러 처리', async () => {
//   server.use(
//     http.get('/api/users', () => {
//       return HttpResponse.json({ error: 'Failed' }, { status: 500 });
//     })
//   );
//
//   render(<UserList />);
//   expect(await screen.findByRole('alert')).toHaveTextContent(/오류/i);
// });
