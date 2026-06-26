---
title: Use Form Libraries Instead of useState
impact: MEDIUM
impactDescription: eliminates per-field useState, handles validation and submission
tags: react, form, react-hook-form, tanstack-form, conform, react-router, zod
---

## 폼 라이브러리로 useState 제거

모든 입력에 `onChange` + `useState`를 연결하지 않기. 폼 라이브러리 또는 프레임워크 Action 사용.

**Incorrect (모든 필드에 useState):**

```tsx
function SignupForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    submit({ name, email, password });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

---

### React Hook Form

가장 널리 사용. `register`로 입력 연결, `useState` 없이 검증/에러/제출 처리.

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(1, "이름을 입력하세요"),
  email: z.string().email("올바른 이메일을 입력하세요"),
  password: z.string().min(8, "8자 이상 입력하세요"),
});

type FormData = z.infer<typeof schema>;

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  async function onSubmit(data: FormData) {
    await submit(data);
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("name")} />
      {errors.name && <p>{errors.name.message}</p>}

      <input {...register("email")} type="email" />
      {errors.email && <p>{errors.email.message}</p>}

      <input {...register("password")} type="password" />
      {errors.password && <p>{errors.password.message}</p>}

      <button type="submit" disabled={isSubmitting}>
        Sign Up
      </button>
    </form>
  );
}
```

---

### TanStack Form

프레임워크 비종속. 타입 안전한 필드 API와 내장 검증.

```tsx
import { useForm } from "@tanstack/react-form";
import { z } from "zod";

function SignupForm() {
  const form = useForm({
    defaultValues: { name: "", email: "", password: "" },
    onSubmit: async ({ value }) => {
      await submit(value);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      <form.Field
        name="name"
        validators={{
          onChange: z.string().min(1, "이름을 입력하세요"),
        }}
      >
        {(field) => (
          <>
            <input
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.errors.length > 0 && (
              <p>{field.state.meta.errors[0]}</p>
            )}
          </>
        )}
      </form.Field>
      {/* email, password 필드도 동일 패턴 */}

      <button type="submit">Sign Up</button>
    </form>
  );
}
```

---

### React Router v7: Action

라우트 `action`에서 폼 처리. 컴포넌트에 상태 없음.

```tsx
// routes/signup.tsx
import type { Route } from "./+types/signup";
import { Form, redirect } from "react-router";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  password: z.string().min(8),
});

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const result = schema.safeParse(Object.fromEntries(formData));

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  await createUser(result.data);
  return redirect("/welcome");
}

export default function SignupPage({ actionData }: Route.ComponentProps) {
  return (
    <Form method="post">
      <input name="name" required />
      {actionData?.errors?.name && <p>{actionData.errors.name[0]}</p>}

      <input name="email" type="email" required />
      {actionData?.errors?.email && <p>{actionData.errors.email[0]}</p>}

      <input name="password" type="password" required />
      {actionData?.errors?.password && <p>{actionData.errors.password[0]}</p>}

      <button type="submit">Sign Up</button>
    </Form>
  );
}
```

> `Form`은 제출 시 자동으로 `action` 호출. `useNavigation().state`로 pending 상태 확인 가능.

---

### Conform (React 19 / React Router)

서버 검증과 점진적 향상(progressive enhancement)에 최적화. `useActionState`와 통합.

```tsx
import { useForm, getFormProps, getInputProps } from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  password: z.string().min(8),
});

function SignupForm() {
  const [lastResult, formAction] = useActionState(serverAction, null);

  const [form, { name, email, password }] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
    shouldValidate: "onBlur",
    shouldRevalidate: "onInput",
  });

  return (
    <form {...getFormProps(form)} action={formAction}>
      <input {...getInputProps(name, { type: "text" })} />
      {name.errors && <p>{name.errors[0]}</p>}

      <input {...getInputProps(email, { type: "email" })} />
      {email.errors && <p>{email.errors[0]}</p>}

      <input {...getInputProps(password, { type: "password" })} />
      {password.errors && <p>{password.errors[0]}</p>}

      <button type="submit">Sign Up</button>
    </form>
  );
}
```

> JS 비활성화 시에도 서버 검증으로 폼 동작. React Router v7의 action과도 통합 가능.

---

### 접근성: useId로 폼 요소 ID 생성

`<label htmlFor>`과 `<input id>`를 연결할 때 하드코딩된 문자열 대신 `useId` 사용. SSR 하이드레이션 안전하고 ID 충돌 없음.

**Incorrect (하드코딩 ID):**

```tsx
function EmailField() {
  return (
    <>
      <label htmlFor="email">Email</label>
      <input id="email" type="email" />
    </>
  );
}
// ❌ 같은 컴포넌트를 2번 렌더링하면 ID 충돌
```

**Correct (useId):**

```tsx
import { useId } from "react";

function EmailField() {
  const id = useId();
  return (
    <>
      <label htmlFor={`${id}-email`}>Email</label>
      <input id={`${id}-email`} type="email" />
    </>
  );
}
```

**여러 필드에 적용:**

```tsx
function SignupForm() {
  const id = useId();

  return (
    <form>
      <label htmlFor={`${id}-name`}>Name</label>
      <input id={`${id}-name`} name="name" />

      <label htmlFor={`${id}-email`}>Email</label>
      <input id={`${id}-email`} name="email" type="email" />

      <label htmlFor={`${id}-password`}>Password</label>
      <input id={`${id}-password`} name="password" type="password" />
    </form>
  );
}
```

**React 18 미만: 커스텀 useId:**

```tsx
let globalId = 0;

function useId() {
  const [id] = useState(() => `field-${++globalId}`);
  return id;
}
```

> `useId`는 CSS 선택자에 사용하지 않기 (`:` 포함). `aria-describedby`, `htmlFor` 등 접근성 속성 전용.

---

### 선택 기준

| 상황 | 추천 |
|------|------|
| 범용, 생태계 넓음 | React Hook Form |
| 프레임워크 비종속, 타입 안전 | TanStack Form |
| React Router v7 사용 | Route action + `Form` |
| 서버 검증, 점진적 향상 | Conform |
| 단순 폼 (2-3개 필드) | 네이티브 FormData |

> 원본: [David Khourshid - Goodbye, useState (BeJS Conference)](https://www.youtube.com/watch?v=aGkscOKWQvQ)
