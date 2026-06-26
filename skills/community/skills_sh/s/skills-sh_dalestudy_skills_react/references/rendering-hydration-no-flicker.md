---
title: Prevent Hydration Mismatch Without Flickering
impact: MEDIUM
impactDescription: avoids visual flicker and hydration errors
tags: rendering, ssr, hydration, localStorage, flicker, theme
---

## 하이드레이션 불일치 없이 깜빡임 방지

클라이언트 저장소(localStorage, cookie)에 따라 렌더링이 달라지는 경우, SSR 에러와 하이드레이션 후 깜빡임을 동시에 방지.

---

### 문제

**SSR 에러:**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // ❌ 서버에서 localStorage 접근 불가 → 에러
  const theme = localStorage.getItem("theme") || "light";
  return <div className={theme}>{children}</div>;
}
```

**깜빡임:**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    // ❌ 하이드레이션 후 실행 → light → dark 깜빡임
    const stored = localStorage.getItem("theme");
    if (stored) setTheme(stored);
  }, []);

  return <div className={theme}>{children}</div>;
}
```

---

### 인라인 스크립트 패턴

React 하이드레이션 전에 동기적으로 DOM 업데이트.

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">{children}</div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                document.getElementById('theme-wrapper').className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  );
}
```

---

### HTML 속성 패턴 (테마)

`<html>` 또는 `<body>`에 직접 설정하면 FOUC(Flash of Unstyled Content) 완전 방지.

```html
<!-- head에 삽입 (프레임워크 레이아웃 또는 index.html) -->
<script>
  (function () {
    try {
      var theme = localStorage.getItem("theme");
      if (theme === "dark") {
        document.documentElement.classList.add("dark");
      }
    } catch (e) {}
  })();
</script>
```

```css
/* CSS에서 다크 모드 처리 */
:root {
  --bg: #fff;
  --text: #000;
}
:root.dark {
  --bg: #0a0a0a;
  --text: #fafafa;
}
```

---

### cookie 기반 패턴 (SSR 완전 호환)

서버에서 cookie를 읽어 첫 렌더링부터 올바른 값 반영. 인라인 스크립트 불필요.

```tsx
// 서버: cookie에서 테마 읽기
function getThemeFromCookie(request: Request): "light" | "dark" {
  const cookie = request.headers.get("cookie") ?? "";
  const match = cookie.match(/theme=(light|dark)/);
  return (match?.[1] as "light" | "dark") ?? "light";
}

// 클라이언트: 테마 변경 시 cookie에 저장
function setThemeCookie(theme: string) {
  document.cookie = `theme=${theme};path=/;max-age=31536000;SameSite=Lax`;
}
```

---

### 적용 대상

| 데이터 | 패턴 |
|--------|------|
| 테마 (다크/라이트) | 인라인 스크립트 또는 cookie |
| 사용자 인증 상태 | cookie (서버에서 읽기) |
| 언어/로케일 설정 | cookie + Accept-Language |
| 사이드바 열림/닫힘 | 인라인 스크립트 (localStorage) |

> 깜빡임이 허용되는 경우(비중요 UI 상태)에는 `useEffect` + `useState`로 충분.

> 원본: [vercel-react-best-practices: rendering-hydration-no-flicker](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-hydration-no-flicker.md)
