# Common Mistakes

Testing Library 사용 시 자주 하는 실수와 해결법.

## 1. 구현 세부사항 테스트

### ❌ 안티패턴: 내부 상태/메서드 접근

```typescript
// ❌ 나쁜 예 - React 내부 상태 테스트
const wrapper = shallow(<Counter />);
expect(wrapper.state('count')).toBe(0);
wrapper.instance().increment();
expect(wrapper.state('count')).toBe(1);

// ❌ 나쁜 예 - 클래스명으로 요소 찾기
const button = container.querySelector('.increment-button');
fireEvent.click(button);
```

### ✅ 올바른 방법: 사용자 관점 테스트

```typescript
// ✅ 좋은 예 - 사용자가 보는 결과 테스트
const user = userEvent.setup();
render(<Counter />);

expect(screen.getByText(/count: 0/i)).toBeInTheDocument();

await user.click(screen.getByRole('button', { name: /증가/i }));

expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
```

**원칙**: 사용자가 볼 수 없는 것은 테스트하지 않는다.

---

## 2. container.querySelector 사용

### ❌ 안티패턴: DOM 직접 쿼리

```typescript
// ❌ 나쁜 예
const { container } = render(<LoginForm />);
const emailInput = container.querySelector('#email');
const submitButton = container.querySelector('button[type="submit"]');
```

### ✅ 올바른 방법: screen 쿼리

```typescript
// ✅ 좋은 예
render(<LoginForm />);
const emailInput = screen.getByRole('textbox', { name: /이메일/i });
const submitButton = screen.getByRole('button', { name: /로그인/i });
```

**이유**:
- `screen` 쿼리는 접근성 기반
- 스크린 리더 사용자 경험 반영
- 리팩토링에 강함

---

## 3. data-testid 남용

### ❌ 안티패턴: testid 과도 사용

```typescript
// ❌ 나쁜 예
<button data-testid="submit-button">제출</button>
<input data-testid="email-input" aria-label="이메일" />

screen.getByTestId('submit-button');
screen.getByTestId('email-input');
```

### ✅ 올바른 방법: 접근성 쿼리 우선

```typescript
// ✅ 좋은 예
<button>제출</button>
<input aria-label="이메일" />

screen.getByRole('button', { name: /제출/i });
screen.getByRole('textbox', { name: /이메일/i });
```

**testid 사용해도 되는 경우**:
- 동적 콘텐츠로 role/text 불명확
- 서드파티 라이브러리 (접근성 속성 없음)
- 다른 모든 쿼리 불가능

---

## 4. fireEvent 사용

### ❌ 안티패턴: fireEvent로 사용자 이벤트 시뮬레이션

```typescript
// ❌ 나쁜 예
const input = screen.getByRole('textbox');
fireEvent.change(input, { target: { value: 'Hello' } });
fireEvent.click(screen.getByRole('button'));
```

### ✅ 올바른 방법: userEvent 사용

```typescript
// ✅ 좋은 예
const user = userEvent.setup();
const input = screen.getByRole('textbox');
await user.type(input, 'Hello');
await user.click(screen.getByRole('button'));
```

**차이점**:
- `fireEvent`: 단일 이벤트만 발생
- `userEvent`: 실제 사용자 행동 재현 (focus → keydown → keyup → change...)

**fireEvent 사용해도 되는 경우**:
- userEvent가 지원하지 않는 이벤트 (`scroll`, `resize` 등)

---

## 5. 임의의 timeout

### ❌ 안티패턴: setTimeout으로 대기

```typescript
// ❌ 나쁜 예
await new Promise(resolve => setTimeout(resolve, 1000));
expect(screen.getByText(/완료/i)).toBeInTheDocument();

// ❌ 나쁜 예
await sleep(500);
expect(mockFn).toHaveBeenCalled();
```

### ✅ 올바른 방법: findBy 또는 waitFor

```typescript
// ✅ 좋은 예
expect(await screen.findByText(/완료/i)).toBeInTheDocument();

// ✅ 좋은 예
await waitFor(() => {
  expect(mockFn).toHaveBeenCalled();
});
```

**이유**:
- 불필요한 대기 시간 (항상 고정 시간만큼 대기)
- 환경에 따라 불안정 (CI에서 더 느릴 수 있음)

---

## 6. act() 수동 사용

### ❌ 안티패턴: 수동 act() 래핑

```typescript
// ❌ 나쁜 예
await act(async () => {
  fireEvent.click(button);
});

// ❌ 나쁜 예
act(() => {
  render(<MyComponent />);
});
```

### ✅ 올바른 방법: Testing Library 메서드 사용

```typescript
// ✅ 좋은 예 - userEvent가 자동으로 act 처리
await user.click(button);

// ✅ 좋은 예 - render가 자동으로 act 처리
render(<MyComponent />);
```

**act 경고 발생 시 해결법**:
1. `await` 누락 확인
2. `findBy` 또는 `waitFor` 사용
3. 비동기 상태 업데이트가 테스트 외부에서 발생하는지 확인

---

## 7. 동기 요소에 waitFor

### ❌ 안티패턴: 불필요한 waitFor

```typescript
// ❌ 나쁜 예 - 이미 렌더링된 요소
await waitFor(() => {
  expect(screen.getByText('Hello')).toBeInTheDocument();
});

// ❌ 나쁜 예
await waitFor(() => {
  expect(screen.getByRole('button')).toHaveTextContent('Click me');
});
```

### ✅ 올바른 방법: 즉시 검증

```typescript
// ✅ 좋은 예 - 동기 요소는 바로 검증
expect(screen.getByText('Hello')).toBeInTheDocument();
expect(screen.getByRole('button')).toHaveTextContent('Click me');
```

**waitFor 사용해야 하는 경우**:
- 비동기로 나타나는 요소
- 상태가 변경될 때까지 대기

---

## 8. waitFor 안에서 side effect

### ❌ 안티패턴: waitFor 콜백에서 이벤트 발생

```typescript
// ❌ 나쁜 예 - waitFor 콜백이 여러 번 실행됨
await waitFor(() => {
  fireEvent.click(button); // 여러 번 클릭됨!
  expect(count).toBe(1);
});
```

### ✅ 올바른 방법: waitFor 밖에서 실행

```typescript
// ✅ 좋은 예
await user.click(button);
await waitFor(() => {
  expect(count).toBe(1);
});
```

**이유**: `waitFor` 콜백은 조건이 만족될 때까지 **여러 번 재실행**됨

---

## 9. getBy로 비동기 요소 찾기

### ❌ 안티패턴: getBy로 비동기 요소 검증

```typescript
// ❌ 나쁜 예 - API 호출 후 즉시 getBy 사용
await user.click(screen.getByRole('button', { name: /불러오기/i }));
expect(screen.getByText(/John Doe/i)).toBeInTheDocument(); // 에러 발생 가능
```

### ✅ 올바른 방법: findBy 사용

```typescript
// ✅ 좋은 예
await user.click(screen.getByRole('button', { name: /불러오기/i }));
expect(await screen.findByText(/John Doe/i)).toBeInTheDocument();
```

---

## 10. queryBy로 존재 확인

### ❌ 안티패턴: queryBy로 비동기 요소 찾기

```typescript
// ❌ 나쁜 예 - queryBy는 비동기 대기 안 함
const element = screen.queryByText(/완료/i);
expect(element).toBeInTheDocument(); // null이면 실패
```

### ✅ 올바른 방법: 용도에 맞는 쿼리 사용

```typescript
// ✅ 좋은 예 - 비동기 요소는 findBy
expect(await screen.findByText(/완료/i)).toBeInTheDocument();

// ✅ 좋은 예 - 없음을 검증할 때만 queryBy
expect(screen.queryByText(/에러/i)).not.toBeInTheDocument();
```

**쿼리 선택 기준**:
- `getBy` - 요소가 이미 있음
- `queryBy` - 요소가 **없음**을 검증
- `findBy` - 요소가 비동기로 나타남

---

## 11. 접근성 무시

### ❌ 안티패턴: 접근성 속성 누락

```typescript
// ❌ 나쁜 예 - label 없는 input
<input type="text" placeholder="이메일 입력" />

// 테스트에서 placeholder로 찾아야 함 (안티패턴)
screen.getByPlaceholderText(/이메일 입력/i);
```

### ✅ 올바른 방법: 접근성 속성 추가

```typescript
// ✅ 좋은 예 - label 연결
<label htmlFor="email">이메일</label>
<input id="email" type="text" />

// 또는 aria-label
<input type="text" aria-label="이메일" />

// 테스트
screen.getByRole('textbox', { name: /이메일/i });
```

**Testing Library를 사용하면 자연스럽게 접근성 개선됨**

---

## 12. 불필요한 cleanup

### ❌ 안티패턴: 수동 cleanup

```typescript
// ❌ 나쁜 예 - 수동 cleanup
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();
});
```

### ✅ 올바른 방법: 자동 cleanup (기본값)

```typescript
// ✅ 좋은 예 - cleanup은 자동으로 실행됨
// 아무것도 안 해도 됨
```

**이유**: Testing Library가 각 테스트 후 자동으로 cleanup 실행

---

## 13. wrapper 재사용

### ❌ 안티패턴: render 결과 재사용

```typescript
// ❌ 나쁜 예
const { rerender } = render(<Counter initialCount={0} />);
rerender(<Counter initialCount={5} />);
```

### ✅ 올바른 방법: 새로 render

```typescript
// ✅ 좋은 예 - 대부분의 경우
render(<Counter initialCount={0} />);
// ... 테스트 ...

// 새 테스트
render(<Counter initialCount={5} />);
```

**rerender 사용해도 되는 경우**:
- props 변경 시 컴포넌트 동작 테스트 (드문 경우)

---

## 14. waitFor에서 getBy 사용

### ❌ 안티패턴: waitFor + getBy 조합

```typescript
// ❌ 나쁜 예 - 장황함
await waitFor(() => {
  expect(screen.getByText(/완료/i)).toBeInTheDocument();
});
```

### ✅ 올바른 방법: findBy 사용

```typescript
// ✅ 좋은 예 - 간결함
expect(await screen.findByText(/완료/i)).toBeInTheDocument();
```

---

## 15. 스냅샷 테스트 과용

### ❌ 안티패턴: 모든 컴포넌트 스냅샷

```typescript
// ❌ 나쁜 예 - 의미 없는 스냅샷
test('renders correctly', () => {
  const { container } = render(<MyComponent />);
  expect(container).toMatchSnapshot();
});
```

### ✅ 올바른 방법: 의미 있는 검증

```typescript
// ✅ 좋은 예 - 실제 동작 테스트
test('사용자가 버튼을 클릭하면 카운트가 증가한다', async () => {
  const user = userEvent.setup();
  render(<Counter />);

  expect(screen.getByText(/count: 0/i)).toBeInTheDocument();

  await user.click(screen.getByRole('button', { name: /증가/i }));

  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});
```

**스냅샷 테스트 사용해도 되는 경우**:
- 복잡한 데이터 구조 (JSON, config 등)
- 에러 메시지 형식

---

## 16. 비동기 테스트에서 await 누락

### ❌ 안티패턴: await 누락

```typescript
// ❌ 나쁜 예 - await 없음
test('example', () => {
  const user = userEvent.setup();
  user.click(button); // await 누락!
  expect(screen.getByText(/완료/i)).toBeInTheDocument();
});
```

### ✅ 올바른 방법: async/await

```typescript
// ✅ 좋은 예
test('example', async () => {
  const user = userEvent.setup();
  await user.click(button);
  expect(await screen.findByText(/완료/i)).toBeInTheDocument();
});
```

---

## 17. 잘못된 쿼리 우선순위

### ❌ 안티패턴: getByText로 버튼 찾기

```typescript
// ❌ 나쁜 예
const submitButton = screen.getByText(/제출/i);
const emailInput = screen.getByPlaceholderText(/이메일/i);
```

### ✅ 올바른 방법: getByRole 우선

```typescript
// ✅ 좋은 예
const submitButton = screen.getByRole('button', { name: /제출/i });
const emailInput = screen.getByRole('textbox', { name: /이메일/i });
```

**쿼리 우선순위**:
1. `getByRole`
2. `getByLabelText`
3. `getByPlaceholderText`
4. `getByText`
5. `getByTestId` (최후 수단)

---

## 요약 체크리스트

**피해야 할 것**:
- ❌ 구현 세부사항 테스트 (state, 클래스명)
- ❌ `container.querySelector` 사용
- ❌ `data-testid` 남용
- ❌ `fireEvent` 사용 (userEvent 대신)
- ❌ 임의의 `setTimeout`
- ❌ 수동 `act()` 호출
- ❌ 동기 요소에 `waitFor`
- ❌ `waitFor` 안에서 side effect
- ❌ 비동기 요소에 `getBy` 사용
- ❌ 접근성 속성 누락

**권장 사항**:
- ✅ 사용자 관점 테스트
- ✅ `screen` 쿼리 사용
- ✅ `getByRole` 우선 사용
- ✅ `userEvent` 사용
- ✅ `findBy` 또는 `waitFor` 사용
- ✅ Testing Library 자동 기능 활용
- ✅ 접근성 개선

**핵심 원칙**:
> "사용자가 사용하는 방식대로 테스트하라"
