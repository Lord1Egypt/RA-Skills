# User Events Reference

`@testing-library/user-event` API 전체 가이드. 실제 사용자 행동을 시뮬레이션하는 권장 방법.

## 기본 설정

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('example', async () => {
  const user = userEvent.setup();
  render(<MyComponent />);

  // 모든 user 메서드는 await 필수
  await user.click(screen.getByRole('button'));
});
```

**핵심**:
- `userEvent.setup()` 호출 필수
- 모든 메서드는 `Promise` 반환 → `await` 사용

## 마우스 상호작용

### click

```typescript
await user.click(element);
await user.click(element, { skipHover: true }); // hover 건너뛰기
```

**시뮬레이션 순서**:
1. `mouseover`
2. `mouseenter`
3. `mousemove`
4. `mousedown`
5. `focus` (focusable 요소)
6. `mouseup`
7. `click`

### dblClick (더블클릭)

```typescript
await user.dblClick(element);
```

### tripleClick (트리플클릭 - 텍스트 선택)

```typescript
await user.tripleClick(element);
```

### hover

```typescript
await user.hover(element);
await user.unhover(element);
```

### pointer (고급 마우스 제어)

```typescript
// 우클릭
await user.pointer({ keys: '[MouseRight]', target: element });

// 마우스 이동
await user.pointer({ coords: { x: 100, y: 200 } });

// 드래그 앤 드롭
await user.pointer([
  { keys: '[MouseLeft>]', target: dragElement },
  { coords: { x: 100, y: 200 } },
  { keys: '[/MouseLeft]' },
]);
```

## 키보드 상호작용

### type (텍스트 입력)

```typescript
await user.type(element, 'Hello World');

// 특수 키 조합
await user.type(element, '{Shift}hello{/Shift}'); // "HELLO"
await user.type(element, 'foo{Backspace}{Backspace}'); // "f"

// delay 옵션 (기본: 0ms)
await user.type(element, 'slow typing', { delay: 100 });

// skipClick (초기 클릭 건너뛰기)
await user.type(element, 'text', { skipClick: true });
```

**특수 키 목록**:
- `{Enter}` - 엔터
- `{Backspace}` - 백스페이스
- `{Delete}` - 삭제
- `{Escape}` - ESC
- `{Space}` - 스페이스
- `{Tab}` - 탭
- `{Shift}text{/Shift}` - Shift 누른 상태로 입력
- `{Control}a{/Control}` - Ctrl+A
- `{Alt}` - Alt
- `{Meta}` - Command (Mac) / Windows (Win)

### keyboard (키보드 직접 제어)

```typescript
// 단일 키
await user.keyboard('a');

// 특수 키
await user.keyboard('{Enter}');
await user.keyboard('{Escape}');

// 키 조합
await user.keyboard('{Control>}a{/Control}'); // Ctrl+A (전체 선택)
await user.keyboard('{Meta>}c{/Meta}'); // Cmd+C (복사)

// 여러 키 순차 입력
await user.keyboard('hello{Enter}world');
```

**키 유지 문법**:
- `{Shift>}` - Shift 누르기 시작
- `{/Shift}` - Shift 떼기
- `{Shift>}text{/Shift}` - Shift 누른 상태로 "text" 입력

### clear (입력값 지우기)

```typescript
await user.clear(element);
```

**동작**:
1. 요소 클릭
2. Ctrl+A (전체 선택)
3. Backspace

## 폼 상호작용

### selectOptions (select 요소)

```typescript
// <select>
//   <option value="1">옵션 1</option>
//   <option value="2">옵션 2</option>
// </select>

// value로 선택
await user.selectOptions(screen.getByRole('combobox'), '1');

// 텍스트로 선택
await user.selectOptions(screen.getByRole('combobox'), '옵션 2');

// 복수 선택 (multiple select)
await user.selectOptions(screen.getByRole('listbox'), ['1', '2']);
```

### deselectOptions (다중 선택 해제)

```typescript
await user.deselectOptions(screen.getByRole('listbox'), '1');
```

### upload (파일 업로드)

```typescript
const file = new File(['hello'], 'hello.png', { type: 'image/png' });

await user.upload(
  screen.getByLabelText(/파일 선택/i),
  file
);

// 복수 파일
await user.upload(input, [file1, file2]);
```

**검증**:
```typescript
const input = screen.getByLabelText(/파일 선택/i) as HTMLInputElement;
expect(input.files).toHaveLength(1);
expect(input.files?.[0]).toBe(file);
```

## 클립보드

### copy, cut, paste

```typescript
// 복사
await user.copy();

// 잘라내기
await user.cut();

// 붙여넣기
await user.paste('pasted text');
```

**예시**:
```typescript
await user.type(screen.getByRole('textbox'), 'Hello');
await user.keyboard('{Control>}a{/Control}'); // 전체 선택
await user.copy();

const otherInput = screen.getByRole('textbox', { name: /다른 입력/i });
await user.click(otherInput);
await user.paste(); // "Hello" 붙여넣기
```

## 탭 이동

### tab

```typescript
// 다음 요소로 tab
await user.tab();

// 이전 요소로 tab (Shift+Tab)
await user.tab({ shift: true });
```

**예시**:
```typescript
render(
  <>
    <input aria-label="첫 번째" />
    <input aria-label="두 번째" />
    <button>제출</button>
  </>
);

const first = screen.getByLabelText(/첫 번째/i);
first.focus();

await user.tab(); // 두 번째 input으로 이동
expect(screen.getByLabelText(/두 번째/i)).toHaveFocus();

await user.tab(); // 버튼으로 이동
expect(screen.getByRole('button')).toHaveFocus();

await user.tab({ shift: true }); // 다시 두 번째 input으로
expect(screen.getByLabelText(/두 번째/i)).toHaveFocus();
```

## userEvent vs fireEvent

### userEvent 사용 (권장)

```typescript
const user = userEvent.setup();

// ✅ 실제 사용자 행동 시뮬레이션
await user.click(button);
await user.type(input, 'text');
```

**장점**:
- 실제 브라우저 이벤트 순서 재현
- focus, blur, hover 자동 처리
- 접근성 검증 (disabled 요소 클릭 불가 등)

### fireEvent 지양

```typescript
// ❌ 저수준 이벤트만 발생
fireEvent.click(button);
fireEvent.change(input, { target: { value: 'text' } });
```

**문제점**:
- 실제 사용자 행동과 다름
- focus, hover 등 자동 처리 안 됨
- 접근성 검증 없음

**예외적으로 fireEvent 사용해야 하는 경우**:
- userEvent가 지원하지 않는 특수 이벤트 (예: `scroll`, `resize`)

```typescript
// scroll 이벤트
fireEvent.scroll(window, { target: { scrollY: 100 } });
```

## 실전 예시

### 로그인 폼

```typescript
test('사용자가 로그인할 수 있다', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.type(
    screen.getByRole('textbox', { name: /이메일/i }),
    'user@example.com'
  );

  await user.type(
    screen.getByLabelText(/비밀번호/i),
    'password123'
  );

  await user.click(screen.getByRole('button', { name: /로그인/i }));

  expect(await screen.findByText(/환영합니다/i)).toBeInTheDocument();
});
```

### 검색 기능

```typescript
test('사용자가 검색할 수 있다', async () => {
  const user = userEvent.setup();
  render(<SearchBar />);

  const searchInput = screen.getByRole('searchbox');

  await user.type(searchInput, 'React');
  await user.keyboard('{Enter}');

  expect(await screen.findByText(/검색 결과/i)).toBeInTheDocument();
});
```

### 체크박스 토글

```typescript
test('사용자가 체크박스를 토글할 수 있다', async () => {
  const user = userEvent.setup();
  render(<TodoItem />);

  const checkbox = screen.getByRole('checkbox', { name: /완료 표시/i });

  expect(checkbox).not.toBeChecked();

  await user.click(checkbox);
  expect(checkbox).toBeChecked();

  await user.click(checkbox);
  expect(checkbox).not.toBeChecked();
});
```

### 드롭다운 선택

```typescript
test('사용자가 국가를 선택할 수 있다', async () => {
  const user = userEvent.setup();
  render(<CountrySelector />);

  const select = screen.getByRole('combobox', { name: /국가/i });

  await user.selectOptions(select, '한국');

  expect(select).toHaveValue('kr');
  expect(screen.getByRole('option', { name: /한국/i })).toBeInTheDocument();
});
```

### 파일 업로드

```typescript
test('사용자가 파일을 업로드할 수 있다', async () => {
  const user = userEvent.setup();
  render(<FileUploader />);

  const file = new File(['content'], 'example.txt', { type: 'text/plain' });
  const input = screen.getByLabelText(/파일 선택/i);

  await user.upload(input, file);

  expect(await screen.findByText(/example.txt/i)).toBeInTheDocument();
});
```

### 키보드 단축키

```typescript
test('Ctrl+S로 저장할 수 있다', async () => {
  const user = userEvent.setup();
  const onSave = vi.fn();
  render(<Editor onSave={onSave} />);

  const textarea = screen.getByRole('textbox');
  await user.type(textarea, 'Some content');

  await user.keyboard('{Control>}s{/Control}');

  expect(onSave).toHaveBeenCalledWith('Some content');
});
```

### 탭 네비게이션

```typescript
test('Tab으로 폼 요소 간 이동이 가능하다', async () => {
  const user = userEvent.setup();
  render(<ContactForm />);

  const nameInput = screen.getByRole('textbox', { name: /이름/i });
  const emailInput = screen.getByRole('textbox', { name: /이메일/i });
  const submitButton = screen.getByRole('button', { name: /제출/i });

  nameInput.focus();
  expect(nameInput).toHaveFocus();

  await user.tab();
  expect(emailInput).toHaveFocus();

  await user.tab();
  expect(submitButton).toHaveFocus();
});
```

### 복사/붙여넣기

```typescript
test('텍스트를 복사하여 다른 입력창에 붙여넣을 수 있다', async () => {
  const user = userEvent.setup();
  render(
    <>
      <input aria-label="원본" defaultValue="Hello World" />
      <input aria-label="대상" />
    </>
  );

  const source = screen.getByLabelText(/원본/i);
  const target = screen.getByLabelText(/대상/i);

  // 원본 텍스트 전체 선택 및 복사
  await user.click(source);
  await user.keyboard('{Control>}a{/Control}');
  await user.copy();

  // 대상에 붙여넣기
  await user.click(target);
  await user.paste();

  expect(target).toHaveValue('Hello World');
});
```

## 옵션 및 설정

### setup 옵션

```typescript
const user = userEvent.setup({
  // 이벤트 간 기본 지연 (ms)
  delay: null,

  // 문서 객체 (기본: global.document)
  document: customDocument,

  // 포인터 맵
  pointerMap: customPointerMap,

  // 포인터 이벤트 비활성화
  pointerEventsCheck: 0,

  // Clipboard API 사용 여부
  writeToClipboard: false,
});
```

### delay 옵션

```typescript
// 모든 이벤트에 100ms 지연
const user = userEvent.setup({ delay: 100 });

// 특정 메서드만 지연
await user.type(input, 'text', { delay: 50 });
```

**사용 사례**:
- 디바운스/쓰로틀 로직 테스트
- 애니메이션 중 상호작용 테스트

## 요약

**기본 패턴**:
```typescript
const user = userEvent.setup();
await user.[method](element, ...args);
```

**자주 사용하는 메서드**:
- `click` - 클릭
- `type` - 텍스트 입력
- `keyboard` - 키보드 직접 제어
- `selectOptions` - 드롭다운 선택
- `upload` - 파일 업로드
- `tab` - 탭 이동

**핵심 원칙**:
1. 항상 `userEvent.setup()` 호출
2. 모든 메서드에 `await` 사용
3. `fireEvent` 대신 `userEvent` 사용
4. 실제 사용자 행동 시뮬레이션
