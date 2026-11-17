# TypeScript/JavaScript Code Review Guide

> TypeScript 代码审查指南，覆盖类型系统、泛型、条件类型、strict 模式、async/await 模式等核心主题。

## 目录

- [类型安全基础](#类型安全基础)
- [泛型模式](#泛型模式)
- [高级类型](#高级类型)
- [Strict 模式配置](#strict-模式配置)
- [异步处理](#异步处理)
- [不可变性](#不可变性)
- [ESLint 规则](#eslint-规则)
- [Review Checklist](#review-checklist)

---

## 类型安全基础

### 避免使用 any

```typescript
// ❌ Using any defeats type safety
function processData(data: any) {
  return data.value;  // 无类型检查，运行时可能崩溃
}

// ✅ Use proper types
interface DataPayload {
  value: string;
}
function processData(data: DataPayload) {
  return data.value;
}

// ✅ 未知类型用 unknown + 类型守卫
function processUnknown(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: string }).value;
  }
  throw new Error('Invalid data');
}
```

### 类型收窄

```typescript
// ❌ 不安全的类型断言
function getLength(value: string | string[]) {
  return (value as string[]).length;  // 如果是 string 会出错
}

// ✅ 使用类型守卫
function getLength(value: string | string[]): number {
  if (Array.isArray(value)) {
    return value.length;
  }
  return value.length;
}

// ✅ 使用 in 操作符
interface Dog { bark(): void }
interface Cat { meow(): void }

function speak(animal: Dog | Cat) {
  if ('bark' in animal) {
    animal.bark();
  } else {
    animal.meow();
  }
}
```

### 字面量类型与 as const

```typescript
// ❌ 类型过于宽泛
const config = {
  endpoint: '/api',
  method: 'GET'  // 类型是 string
};

// ✅ 使用 as const 获得字面量类型
const config = {
  endpoint: '/api',
  method: 'GET'
} as const;  // method 类型是 'GET'
```

---

## 泛型模式

### 泛型约束

```typescript
// ❌ 泛型没有约束，无法访问属性
function getProperty<T>(obj: T, key: string) {
  return obj[key];  // Error: 无法索引
}

// ✅ 使用 keyof 约束
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: 'Alice', age: 30 };
getProperty(user, 'name');  // 返回类型是 string
getProperty(user, 'foo');   // Error: 'foo' 不在 keyof User
```

### 常见泛型工具类型

```typescript
// ✅ 善用内置工具类型
interface User {
  id: number;
  name: string;
  email: string;
}

type PartialUser = Partial<User>;         // 所有属性可选
type RequiredUser = Required<User>;       // 所有属性必需
type ReadonlyUser = Readonly<User>;       // 所有属性只读
type UserKeys = keyof User;               // 'id' | 'name' | 'email'
type NameOnly = Pick<User, 'name'>;       // { name: string }
type WithoutId = Omit<User, 'id'>;        // { name: string; email: string }
type UserRecord = Record<string, User>;   // { [key: string]: User }
```

---

## 高级类型

### Discriminated Unions

```typescript
// ✅ 使用判别属性实现类型安全
type Result<T, E> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult(result: Result<User, Error>) {
  if (result.success) {
    console.log(result.data.name);  // TypeScript 知道 data 存在
  } else {
    console.log(result.error.message);  // TypeScript 知道 error 存在
  }
}

// ✅ Redux Action 模式
type Action =
  | { type: 'INCREMENT'; payload: number }
  | { type: 'DECREMENT'; payload: number }
  | { type: 'RESET' };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'INCREMENT':
      return state + action.payload;
    case 'DECREMENT':
      return state - action.payload;
    case 'RESET':
      return 0;
  }
}
```

---

## Strict 模式配置

### 推荐的 tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### noUncheckedIndexedAccess 的影响

```typescript
// tsconfig: "noUncheckedIndexedAccess": true

const arr = [1, 2, 3];
const first = arr[0];  // 类型是 number | undefined

// ❌ 直接使用可能出错
console.log(first.toFixed(2));  // Error: 可能是 undefined

// ✅ 先检查
if (first !== undefined) {
  console.log(first.toFixed(2));
}
```

---

## 异步处理

### Promise 错误处理

```typescript
// ❌ Not handling async errors
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();  // 网络错误未处理
}

// ✅ Handle errors properly
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch user: ${error.message}`);
    }
    throw error;
  }
}
```

### Promise.all vs Promise.allSettled

```typescript
// ❌ Promise.all 一个失败全部失败
async function fetchAllUsers(ids: string[]) {
  const users = await Promise.all(ids.map(fetchUser));
  return users;  // 一个失败就全部失败
}

// ✅ Promise.allSettled 获取所有结果
async function fetchAllUsers(ids: string[]) {
  const results = await Promise.allSettled(ids.map(fetchUser));

  const users: User[] = [];
  const errors: Error[] = [];

  for (const result of results) {
    if (result.status === 'fulfilled') {
      users.push(result.value);
    } else {
      errors.push(result.reason);
    }
  }

  return { users, errors };
}
```

### 竞态条件处理

```typescript
// ❌ 竞态条件：旧请求可能覆盖新请求
function useSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetch(`/api/search?q=${query}`)
      .then(r => r.json())
      .then(setResults);  // 旧请求可能后返回！
  }, [query]);
}

// ✅ 使用 AbortController
function useSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const controller = new AbortController();

    fetch(`/api/search?q=${query}`, { signal: controller.signal })
      .then(r => r.json())
      .then(setResults)
      .catch(e => {
        if (e.name !== 'AbortError') throw e;
      });

    return () => controller.abort();
  }, [query]);
}
```

---

## 不可变性

### Readonly 与 ReadonlyArray

```typescript
// ❌ 可变参数可能被意外修改
function processUsers(users: User[]) {
  users.sort((a, b) => a.name.localeCompare(b.name));  // 修改了原数组！
  return users;
}

// ✅ 使用 readonly 防止修改
function processUsers(users: readonly User[]): User[] {
  return [...users].sort((a, b) => a.name.localeCompare(b.name));
}
```

---

## ESLint 规则

### 推荐的 @typescript-eslint 规则

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:@typescript-eslint/strict'
  ],
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unsafe-assignment': 'error',
    '@typescript-eslint/no-unsafe-member-access': 'error',
    '@typescript-eslint/no-unsafe-call': 'error',
    '@typescript-eslint/no-unsafe-return': 'error',
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/await-thenable': 'error',
    '@typescript-eslint/no-misused-promises': 'error',
    '@typescript-eslint/consistent-type-imports': 'error',
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error'
  }
};
```

---

## Review Checklist

### 类型系统
- [ ] 没有使用 `any`（使用 `unknown` + 类型守卫代替）
- [ ] 接口和类型定义完整且有意义的命名
- [ ] 使用泛型提高代码复用性
- [ ] 联合类型有正确的类型收窄
- [ ] 善用工具类型（Partial、Pick、Omit 等）

### 泛型
- [ ] 泛型有适当的约束（extends）
- [ ] 泛型参数有合理的默认值
- [ ] 避免过度泛型化（KISS 原则）

### Strict 模式
- [ ] tsconfig.json 启用了 strict: true
- [ ] 启用了 noUncheckedIndexedAccess
- [ ] 没有使用 @ts-ignore（改用 @ts-expect-error）

### 异步代码
- [ ] async 函数有错误处理
- [ ] Promise rejection 被正确处理
- [ ] 没有 floating promises
- [ ] 并发请求使用 Promise.all 或 Promise.allSettled
- [ ] 竞态条件使用 AbortController 处理

### 不可变性
- [ ] 不直接修改函数参数
- [ ] 使用 spread 操作符创建新对象/数组
- [ ] 考虑使用 readonly 修饰符

### ESLint
- [ ] 使用 @typescript-eslint/recommended
- [ ] 没有 ESLint 警告或错误
- [ ] 使用 consistent-type-imports