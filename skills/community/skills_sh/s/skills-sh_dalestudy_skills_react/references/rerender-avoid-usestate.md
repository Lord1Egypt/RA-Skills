---
title: Avoid Overusing useState
impact: MEDIUM
impactDescription: reduces complexity, prevents impossible states, improves UX
tags: react, useState, state-management, decision-guide
---

## useState 과다 사용 방지

`useState`는 순수한 로컬 UI 상태(모달 열림, 토글, 입력 포커스 등)에만 사용. 아래 판단 기준에 따라 더 적합한 패턴 선택.

### 판단 기준

| 상황 | useState 대신 | 레퍼런스 |
|------|--------------|---------|
| 새로고침/공유 필요한 상태 | URL 검색 매개변수 | [`rerender-url-state`](rerender-url-state.md) |
| 서버 데이터 (목록, 상세) | 데이터 페칭 라이브러리 / Suspense | [`client-data-dedup`](client-data-dedup.md) / [`async-suspense-boundaries`](async-suspense-boundaries.md) |
| 폼 입력값 수집 | 폼 라이브러리 / Action | [`rerender-form-libraries`](rerender-form-libraries.md) |
| 여러 boolean 플래그 | discriminated union | [`rerender-discriminated-union`](rerender-discriminated-union.md) |
| 다른 상태에서 도출 가능한 값 | 변수로 직접 계산 | [`rerender-derived-state-no-effect`](rerender-derived-state-no-effect.md) |
| UI 업데이트 불필요한 값 추적 | useRef | [`rerender-use-ref-transient-values`](rerender-use-ref-transient-values.md) |
| 복잡한 상태 전이 로직 | useReducer | [`rerender-use-reducer`](rerender-use-reducer.md) |
| 여러 컴포넌트 공유 + 외부 API | useSyncExternalStore | [`client-sync-external-store`](client-sync-external-store.md) |

> 원본: [David Khourshid - Goodbye, useState (BeJS Conference)](https://www.youtube.com/watch?v=aGkscOKWQvQ)
