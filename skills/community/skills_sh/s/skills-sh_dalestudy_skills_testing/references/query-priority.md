# Query Priority Guide

Testing Library 쿼리 선택 상세 가이드. 접근성과 사용자 경험을 최우선으로 고려한 순서.

## 1. getByRole (최우선)

**사용 시기**: 거의 모든 요소 (버튼, 링크, 폼 요소, 헤딩 등)

스크린 리더가 요소를 인식하는 방식과 동일. **가장 강력하고 권장되는 쿼리**.

### 기본 사용

```typescript
// 버튼
screen.getByRole('button', { name: /제출/i });
screen.getByRole('button', { name: /취소/i });

// 링크
screen.getByRole('link', { name: /더 보기/i });

// 입력 필드
screen.getByRole('textbox', { name: /이메일/i });
screen.getByRole('checkbox', { name: /약관 동의/i });
screen.getByRole('combobox', { name: /국가 선택/i });

// 헤딩
screen.getByRole('heading', { name: /사용자 설정/i, level: 1 });

// 기타
screen.getByRole('alert');
screen.getByRole('dialog');
screen.getByRole('navigation');
```

### 주요 Role 목록

| 요소 | Role | 예시 |
|------|------|------|
| `<button>` | `button` | `getByRole('button')` |
| `<a>` | `link` | `getByRole('link')` |
| `<input type="text">` | `textbox` | `getByRole('textbox')` |
| `<input type="checkbox">` | `checkbox` | `getByRole('checkbox')` |
| `<input type="radio">` | `radio` | `getByRole('radio')` |
| `<select>` | `combobox` | `getByRole('combobox')` |
| `<textarea>` | `textbox` | `getByRole('textbox')` |
| `<h1>` ~ `<h6>` | `heading` | `getByRole('heading', { level: 1 })` |
| `<img alt="...">` | `img` | `getByRole('img')` |
| `<nav>` | `navigation` | `getByRole('navigation')` |
| `<main>` | `main` | `getByRole('main')` |
| `<ul>`, `<ol>` | `list` | `getByRole('list')` |
| `<li>` | `listitem` | `getByRole('listitem')` |

### 고급 옵션

```typescript
// name: 접근 가능한 이름 (텍스트, aria-label, aria-labelledby 등)
screen.getByRole('button', { name: /저장/i });

// level: 헤딩 레벨
screen.getByRole('heading', { level: 2, name: /제목/i });

// checked: 체크 상태
screen.getByRole('checkbox', { checked: true });

// pressed: 토글 버튼 상태
screen.getByRole('button', { pressed: true });

// expanded: 확장/축소 상태
screen.getByRole('button', { expanded: false });

// hidden: 숨겨진 요소 포함
screen.getByRole('button', { hidden: true, name: /숨김/i });
```

## 2. getByLabelText

**사용 시기**: 폼 요소 (input, textarea, select)가 `<label>`과 연결된 경우

```typescript
// <label htmlFor="email">이메일</label>
// <input id="email" type="email" />
screen.getByLabelText(/이메일/i);

// aria-label 사용
// <input aria-label="검색어 입력" />
screen.getByLabelText(/검색어 입력/i);

// aria-labelledby 사용
// <span id="username-label">사용자명</span>
// <input aria-labelledby="username-label" />
screen.getByLabelText(/사용자명/i);
```

**언제 사용하지 말아야 하나?**
- `getByRole('textbox', { name: /.../ })`이 더 명시적이므로 보통 role 쿼리 선호
- 하지만 label이 명확한 폼 요소에는 여전히 유용

## 3. getByPlaceholderText

**사용 시기**: placeholder가 명확하고 유일한 경우 (권장하지 않음)

```typescript
// <input placeholder="이메일을 입력하세요" />
screen.getByPlaceholderText(/이메일을 입력하세요/i);
```

**주의사항**:
- placeholder는 접근성이 떨어지므로 **label을 대체할 수 없음**
- 가능하면 `getByRole` 또는 `getByLabelText` 사용 권장

## 4. getByText

**사용 시기**: 텍스트 콘텐츠로 요소를 찾을 때 (버튼, 링크, 헤딩 제외)

```typescript
// 단락, div, span 등
screen.getByText(/환영합니다/i);
screen.getByText(/사용자 목록/i);

// 정확한 매칭
screen.getByText('Hello World', { exact: true });

// 부분 매칭 (함수)
screen.getByText((content, element) => {
  return content.startsWith('Error:');
});
```

**버튼/링크는 getByRole 사용**:
```typescript
// ❌ 나쁜 예
screen.getByText(/제출/i);

// ✅ 좋은 예
screen.getByRole('button', { name: /제출/i });
```

## 5. getByDisplayValue

**사용 시기**: 현재 입력된 값으로 폼 요소를 찾을 때

```typescript
// <input value="John Doe" />
screen.getByDisplayValue(/John Doe/i);

// <select>
//   <option value="kr" selected>한국</option>
// </select>
screen.getByDisplayValue(/한국/i);
```

**주의**: 초기값이 아닌 **현재 값**으로 검색함

## 6. getByAltText

**사용 시기**: 이미지의 alt 속성으로 검색

```typescript
// <img alt="프로필 사진" src="..." />
screen.getByAltText(/프로필 사진/i);
```

**getByRole('img')와 비교**:
```typescript
// 둘 다 가능
screen.getByAltText(/로고/i);
screen.getByRole('img', { name: /로고/i });

// getByRole이 더 명시적이므로 권장
```

## 7. getByTitle

**사용 시기**: title 속성으로 검색 (tooltip 등)

```typescript
// <button title="닫기">✕</button>
screen.getByTitle(/닫기/i);

// SVG
// <svg title="체크 아이콘"><path /></svg>
screen.getByTitle(/체크 아이콘/i);
```

**주의**: title은 접근성이 떨어지므로 가능하면 aria-label 사용 권장

## 8. getByTestId (최후 수단)

**사용 시기**: 다른 모든 방법이 불가능할 때만 사용

```typescript
// <div data-testid="custom-element">...</div>
screen.getByTestId('custom-element');
```

**사용해야 하는 경우**:
- 동적 콘텐츠로 텍스트/role이 불명확
- 서드파티 라이브러리 요소 (접근성 속성 없음)
- 시각적으로만 구분되는 요소

**피해야 하는 이유**:
- 사용자 경험 반영 안 함
- 접근성 개선에 도움 안 됨
- 리팩토링 시 테스트 깨지기 쉬움

## 쿼리 변형

모든 쿼리는 3가지 변형이 있음:

### getBy (동기, 즉시 실패)

```typescript
screen.getByRole('button'); // 없으면 즉시 에러
```

**사용 시기**: 요소가 이미 렌더링되어 있을 때

### queryBy (동기, null 반환)

```typescript
screen.queryByRole('button'); // 없으면 null 반환
```

**사용 시기**: 요소가 **없음**을 검증할 때

```typescript
expect(screen.queryByRole('alert')).not.toBeInTheDocument();
```

### findBy (비동기, Promise)

```typescript
await screen.findByRole('button'); // 나타날 때까지 대기
```

**사용 시기**: 비동기로 나타나는 요소 (API 호출, 애니메이션 후 등)

## 복수 요소 쿼리

### getAllBy, queryAllBy, findAllBy

```typescript
// 모든 버튼
const buttons = screen.getAllByRole('button');
expect(buttons).toHaveLength(3);

// 모든 리스트 아이템
const items = screen.getAllByRole('listitem');
expect(items[0]).toHaveTextContent('첫 번째');

// 비동기로 나타나는 여러 요소
const notifications = await screen.findAllByRole('alert');
```

## 실전 예시

### 폼 테스트

```typescript
test('사용자가 회원가입 폼을 작성할 수 있다', async () => {
  const user = userEvent.setup();
  render(<SignupForm />);

  // 1순위: getByRole
  await user.type(
    screen.getByRole('textbox', { name: /이메일/i }),
    'user@example.com'
  );

  // 1순위: getByRole (password는 role 없으므로 getByLabelText 사용)
  await user.type(screen.getByLabelText(/비밀번호/i), 'password123');

  // 1순위: getByRole
  await user.click(screen.getByRole('checkbox', { name: /약관 동의/i }));

  // 1순위: getByRole
  await user.click(screen.getByRole('button', { name: /가입하기/i }));

  // 3순위: findBy (비동기 결과)
  expect(await screen.findByText(/가입이 완료되었습니다/i)).toBeInTheDocument();
});
```

### 네비게이션 테스트

```typescript
test('네비게이션 메뉴가 올바르게 동작한다', async () => {
  const user = userEvent.setup();
  render(<Navigation />);

  // 1순위: getByRole (navigation)
  const nav = screen.getByRole('navigation');

  // 1순위: getByRole (link)
  const homeLink = within(nav).getByRole('link', { name: /홈/i });
  const aboutLink = within(nav).getByRole('link', { name: /소개/i });

  await user.click(aboutLink);

  // 1순위: getByRole (heading)
  expect(screen.getByRole('heading', { name: /소개/i })).toBeInTheDocument();
});
```

### 모달 테스트

```typescript
test('모달을 열고 닫을 수 있다', async () => {
  const user = userEvent.setup();
  render(<App />);

  // 모달 없음 확인 (queryBy)
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

  // 열기 버튼
  await user.click(screen.getByRole('button', { name: /설정 열기/i }));

  // 모달 나타남 (findBy 또는 getBy)
  const dialog = await screen.findByRole('dialog');
  expect(dialog).toBeVisible();

  // 닫기 버튼 (within 사용)
  await user.click(within(dialog).getByRole('button', { name: /닫기/i }));

  // 모달 사라짐 확인
  await waitFor(() => {
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
```

## 요약

**쿼리 우선순위 체크리스트**:
1. ✅ `getByRole`로 찾을 수 있는가? → 사용
2. ✅ 폼 요소 + label 있는가? → `getByLabelText` 고려
3. ✅ 일반 텍스트 콘텐츠인가? → `getByText`
4. ✅ 이미지 alt인가? → `getByAltText` (또는 `getByRole('img')`)
5. ⚠️ 다른 방법 모두 불가능한가? → `getByTestId` (최후 수단)

**비동기 처리**:
- 요소가 이미 있음 → `getBy`
- 요소가 없음을 검증 → `queryBy`
- 요소가 비동기로 나타남 → `findBy`
