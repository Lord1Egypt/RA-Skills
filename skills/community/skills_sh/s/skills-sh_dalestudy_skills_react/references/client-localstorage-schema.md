---
title: Version and Minimize localStorage Data
impact: MEDIUM
impactDescription: prevents schema conflicts, reduces storage size
tags: client, localStorage, storage, versioning, schema
---

## localStorage 버전 관리

키에 버전 접두사 추가, 필요한 필드만 저장. 스키마 충돌 방지, 민감 데이터 저장 방지.

**Incorrect:**

```typescript
localStorage.setItem("userConfig", JSON.stringify(fullUserObject));
const data = localStorage.getItem("userConfig");
```

**Correct:**

```typescript
const VERSION = "v2";

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config));
  } catch {} // incognito/quota 초과 대응
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}
```

**마이그레이션 패턴:**

```typescript
function migrate() {
  try {
    const v1 = localStorage.getItem("userConfig:v1");
    if (v1) {
      const old = JSON.parse(v1);
      saveConfig({ theme: old.darkMode ? "dark" : "light", language: old.lang });
      localStorage.removeItem("userConfig:v1");
    }
  } catch {}
}
```

**서버 응답에서 최소 필드만 저장:**

```typescript
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem(
      "prefs:v1",
      JSON.stringify({
        theme: user.preferences.theme,
        notifications: user.preferences.notifications,
      }),
    );
  } catch {}
}
```

**반드시 try-catch:** incognito/private 브라우징(Safari, Firefox), quota 초과, 비활성화 시 throw.

> 원본: [vercel-react-best-practices: client-localstorage-schema](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/client-localstorage-schema.md)
