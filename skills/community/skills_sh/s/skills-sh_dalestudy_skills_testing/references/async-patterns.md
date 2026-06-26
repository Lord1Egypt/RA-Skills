# Async Patterns

Testing Library 비동기 처리 패턴 및 안티패턴 가이드.

## 핵심 원칙

1. **findBy 쿼리 우선** - `getBy` + `waitFor` 조합을 자동화
2. **waitFor 사용** - 복잡한 비동기 조건 검증
3. **임의의 timeout 금지** - `setTimeout`, `sleep` 등 사용 지양
4. **act() 수동 사용 지양** - Testing Library가 자동 처리

## findBy 쿼리 (권장)

비동기로 나타나는 요소를 기다리는 가장 간단한 방법.

### 기본 사용

```typescript
// ✅ 좋은 예 - findBy 사용
const successMessage = await screen.findByText(/저장되었습니다/i);
expect(successMessage).toBeInTheDocument();

// ❌ 나쁜 예 - getBy + waitFor
await waitFor(() => {
  expect(screen.getByText(/저장되었습니다/i)).toBeInTheDocument();
});
```

### findBy = getBy + waitFor

`findBy`는 내부적으로 다음과 같이 동작:

```typescript
// findByText는 이것과 동일
await waitFor(() => screen.getByText(/텍스트/i));
```

**기본 타임아웃**: 1000ms (1초)

### 복수 요소 - findAllBy

```typescript
// 비동기로 나타나는 여러 요소
const items = await screen.findAllByRole('listitem');
expect(items).toHaveLength(3);
```

## waitFor

복잡한 비동기 조건을 검증할 때 사용.

### 기본 사용

```typescript
await waitFor(() => {
  expect(mockFn).toHaveBeenCalledTimes(1);
});

await waitFor(() => {
  expect(screen.getByRole('alert')).toHaveTextContent('성공');
});
```

### 여러 조건 검증

```typescript
await waitFor(() => {
  // 모든 조건이 true가 될 때까지 대기
  expect(screen.getByRole('button')).not.toBeDisabled();
  expect(screen.queryByText(/로딩 중/i)).not.toBeInTheDocument();
  expect(mockApi).toHaveBeenCalled();
});
```

### 옵션

```typescript
await waitFor(
  () => {
    expect(element).toBeInTheDocument();
  },
  {
    timeout: 3000, // 최대 대기 시간 (기본: 1000ms)
    interval: 50,  // 재시도 간격 (기본: 50ms)
  }
);
```

## 사용 사례별 패턴

### 1. API 호출 후 UI 업데이트

```typescript
test('데이터를 불러와서 화면에 표시한다', async () => {
  const user = userEvent.setup();
  render(<UserList />);

  await user.click(screen.getByRole('button', { name: /불러오기/i }));

  // ✅ findBy 사용
  expect(await screen.findByText(/John Doe/i)).toBeInTheDocument();

  // ❌ 임의의 timeout 사용 금지
  // await new Promise(resolve => setTimeout(resolve, 1000));
  // expect(screen.getByText(/John Doe/i)).toBeInTheDocument();
});
```

### 2. 로딩 상태 → 성공 상태

```typescript
test('로딩 후 데이터를 표시한다', async () => {
  render(<AsyncComponent />);

  // 초기 로딩 상태 확인
  expect(screen.getByText(/로딩 중/i)).toBeInTheDocument();

  // ✅ 로딩이 사라질 때까지 대기
  await waitFor(() => {
    expect(screen.queryByText(/로딩 중/i)).not.toBeInTheDocument();
  });

  // 데이터 표시 확인
  expect(screen.getByText(/데이터/i)).toBeInTheDocument();
});
```

**또는 waitForElementToBeRemoved 사용**:

```typescript
import { waitForElementToBeRemoved } from '@testing-library/react';

test('로딩 후 데이터를 표시한다', async () => {
  render(<AsyncComponent />);

  const loader = screen.getByText(/로딩 중/i);

  // ✅ 요소가 DOM에서 제거될 때까지 대기
  await waitForElementToBeRemoved(loader);

  expect(screen.getByText(/데이터/i)).toBeInTheDocument();
});
```

### 3. 에러 상태 표시

```typescript
test('에러가 발생하면 에러 메시지를 표시한다', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ error: 'Server Error' }, { status: 500 });
    })
  );

  const user = userEvent.setup();
  render(<UserList />);

  await user.click(screen.getByRole('button', { name: /불러오기/i }));

  // ✅ findBy로 에러 메시지 대기
  const errorAlert = await screen.findByRole('alert');
  expect(errorAlert).toHaveTextContent(/오류가 발생했습니다/i);
});
```

### 4. 폼 제출 후 리다이렉트

```typescript
test('로그인 성공 시 대시보드로 이동한다', async () => {
  const user = userEvent.setup();
  render(<LoginPage />);

  await user.type(screen.getByRole('textbox', { name: /이메일/i }), 'user@example.com');
  await user.type(screen.getByLabelText(/비밀번호/i), 'password');
  await user.click(screen.getByRole('button', { name: /로그인/i }));

  // ✅ 새 페이지 요소 대기
  expect(await screen.findByRole('heading', { name: /대시보드/i })).toBeInTheDocument();
});
```

### 5. 디바운스 입력

```typescript
test('디바운스된 검색이 동작한다', async () => {
  const user = userEvent.setup();
  render(<SearchBar debounceMs={500} />);

  const searchInput = screen.getByRole('searchbox');

  // 빠르게 입력
  await user.type(searchInput, 'React');

  // ✅ 디바운스 후 결과 대기
  expect(await screen.findByText(/검색 결과: React/i)).toBeInTheDocument();
});
```

### 6. 애니메이션 후 상태 변경

```typescript
test('모달이 애니메이션 후 닫힌다', async () => {
  const user = userEvent.setup();
  render(<Modal />);

  await user.click(screen.getByRole('button', { name: /닫기/i }));

  // ✅ 애니메이션 후 DOM에서 제거 대기
  await waitFor(() => {
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
```

## MSW (Mock Service Worker) 통합

### 설정

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John Doe' },
      { id: 2, name: 'Jane Smith' },
    ]);
  }),
];

// tests/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```typescript
// tests/setup.ts
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### 사용 예시

```typescript
import { server } from './mocks/server';
import { http, HttpResponse } from 'msw';

test('사용자 목록을 불러온다', async () => {
  render(<UserList />);

  // ✅ MSW가 모킹한 데이터가 나타날 때까지 대기
  expect(await screen.findByText(/John Doe/i)).toBeInTheDocument();
  expect(await screen.findByText(/Jane Smith/i)).toBeInTheDocument();
});

test('에러 발생 시 에러 메시지를 표시한다', async () => {
  // 특정 테스트에서만 에러 응답 반환
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ error: 'Failed' }, { status: 500 });
    })
  );

  render(<UserList />);

  // ✅ 에러 알림 대기
  expect(await screen.findByRole('alert')).toHaveTextContent(/오류/i);
});
```

### 지연 시뮬레이션

```typescript
import { delay, http, HttpResponse } from 'msw';

test('로딩 상태가 표시된다', async () => {
  server.use(
    http.get('/api/users', async () => {
      await delay(200); // 200ms 지연
      return HttpResponse.json([{ id: 1, name: 'John' }]);
    })
  );

  render(<UserList />);

  // 로딩 표시 확인
  expect(screen.getByText(/로딩 중/i)).toBeInTheDocument();

  // ✅ 데이터 로딩 후 대기
  expect(await screen.findByText(/John/i)).toBeInTheDocument();

  // 로딩 사라짐 확인
  expect(screen.queryByText(/로딩 중/i)).not.toBeInTheDocument();
});
```

## 안티패턴

### ❌ 임의의 timeout

```typescript
// ❌ 나쁜 예 - 임의의 대기 시간
await new Promise(resolve => setTimeout(resolve, 1000));
expect(screen.getByText(/완료/i)).toBeInTheDocument();

// ✅ 좋은 예 - findBy 사용
expect(await screen.findByText(/완료/i)).toBeInTheDocument();
```

**문제점**:
- 불필요한 테스트 지연 (항상 1초 대기)
- 환경에 따라 실패 가능 (느린 CI에서 1초로 부족할 수 있음)

### ❌ act() 수동 사용

```typescript
// ❌ 나쁜 예 - 수동 act() 사용
await act(async () => {
  fireEvent.click(button);
});

// ✅ 좋은 예 - userEvent 사용 (자동으로 act 처리)
await user.click(button);
```

**언제 act 경고가 발생하나?**
- 상태 업데이트가 테스트 외부에서 발생할 때
- 보통 Testing Library 메서드가 자동 처리하므로 수동 사용 불필요

**act 경고 해결법**:
1. `await` 누락 확인
2. `findBy` 또는 `waitFor` 사용
3. 여전히 발생하면 코드 문제 확인 (테스트 외부 상태 업데이트 등)

### ❌ 동기 요소에 waitFor

```typescript
// ❌ 나쁜 예 - 이미 렌더링된 요소에 waitFor
await waitFor(() => {
  expect(screen.getByText('Hello')).toBeInTheDocument();
});

// ✅ 좋은 예 - 즉시 검증
expect(screen.getByText('Hello')).toBeInTheDocument();
```

### ❌ waitFor 안에서 side effect

```typescript
// ❌ 나쁜 예 - waitFor 콜백 안에서 클릭
await waitFor(() => {
  fireEvent.click(button); // side effect!
  expect(something).toBe(true);
});

// ✅ 좋은 예 - waitFor 밖에서 실행
await user.click(button);
await waitFor(() => {
  expect(something).toBe(true);
});
```

**waitFor는 여러 번 재실행됨** → side effect 있으면 여러 번 발생

### ❌ queryBy로 존재 확인

```typescript
// ❌ 나쁜 예 - queryBy로 비동기 요소 찾기
const element = screen.queryByText(/완료/i);
expect(element).toBeInTheDocument(); // null이면 실패

// ✅ 좋은 예 - findBy 사용
expect(await screen.findByText(/완료/i)).toBeInTheDocument();
```

## 디버깅

### screen.debug()

```typescript
test('디버깅', async () => {
  render(<MyComponent />);

  // 현재 DOM 출력
  screen.debug();

  await user.click(button);

  // 변경 후 DOM 출력
  screen.debug();
});
```

### logRoles

```typescript
import { logRoles } from '@testing-library/react';

test('role 디버깅', () => {
  const { container } = render(<MyComponent />);

  // 모든 role 출력
  logRoles(container);
});
```

### waitFor 디버깅

```typescript
await waitFor(
  () => {
    console.log('Checking...');
    expect(element).toBeInTheDocument();
  },
  { timeout: 3000, interval: 100 }
);
```

## 타임아웃 설정

### 전역 설정

```typescript
// tests/setup.ts
import { configure } from '@testing-library/react';

configure({ asyncUtilTimeout: 3000 }); // 기본: 1000ms
```

### 개별 설정

```typescript
// 특정 findBy
await screen.findByText(/텍스트/i, {}, { timeout: 3000 });

// waitFor
await waitFor(
  () => expect(element).toBeInTheDocument(),
  { timeout: 5000 }
);
```

## 요약

**비동기 처리 우선순위**:
1. ✅ `findBy` - 요소가 나타날 때까지 대기
2. ✅ `waitFor` - 복잡한 조건 검증
3. ✅ `waitForElementToBeRemoved` - 요소 제거 대기

**피해야 할 것**:
1. ❌ `setTimeout`, `sleep` 등 임의 대기
2. ❌ 수동 `act()` 호출
3. ❌ 동기 요소에 `waitFor` 사용
4. ❌ `waitFor` 콜백 내 side effect

**핵심 원칙**:
- 실제 사용자처럼 대기 (요소가 나타날 때까지)
- Testing Library가 자동 처리하므로 수동 최적화 불필요
- MSW로 API 모킹하면 일관된 비동기 테스트 가능
