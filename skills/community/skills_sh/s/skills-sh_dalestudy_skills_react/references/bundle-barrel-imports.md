---
title: Avoid Barrel File Imports
impact: CRITICAL
impactDescription: 200-800ms import cost, slow builds
tags: bundle, imports, tree-shaking, barrel-files, performance
---

## Barrel file import 지양

소스 파일에서 직접 import하여 수천 개의 미사용 모듈 로드 방지. **Barrel file**은 여러 모듈을 re-export하는 진입점 (`index.js`에서 `export * from './module'`).

**Incorrect (전체 라이브러리 로드):**

```tsx
import { Check, X, Menu } from "lucide-react";
// 1,583 모듈 로드, dev에서 ~2.8s 추가
// 런타임 비용: cold start마다 200-800ms

import { Button, TextField } from "@mui/material";
// 2,225 모듈 로드, dev에서 ~4.2s 추가
```

**Correct (필요한 모듈만 로드):**

```tsx
import Check from "lucide-react/dist/esm/icons/check";
import X from "lucide-react/dist/esm/icons/x";
import Menu from "lucide-react/dist/esm/icons/menu";
// 3개 모듈만 로드 (~2KB vs ~1MB)

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
```

**효과:** dev 부팅 15-70% 빨라짐, 빌드 28% 빨라짐, cold start 40% 빨라짐.

**주요 대상 라이브러리:** `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `ramda`, `date-fns`, `rxjs`, `react-use`

> 원본: [vercel-react-best-practices: bundle-barrel-imports](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/bundle-barrel-imports.md)
