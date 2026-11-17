# Svelte / SvelteKit Code Review Guide

Svelte 5 / SvelteKit 审查重点：Runes 响应式系统、Server/Client 边界、Form Actions、Store 迁移、以及安全性。

## 目录

- [Runes: $state / $derived / $effect](#runes-state--derived--effect)
- [Load 函数（Server vs Client）](#load-函数server-vs-client)
- [Form Actions](#form-actions)
- [Store 迁移（→ $state）](#store-迁移)
- [SSR vs CSR 边界](#ssr-vs-csr-边界)
- [响应式语句迁移（$: → Runes）](#响应式语句迁移)
- [性能优化](#性能优化)
- [安全审查](#安全审查)
- [Review Checklist](#review-checklist)

---

## Runes: $state / $derived / $effect

### $state 基础用法

```svelte
<!-- ❌ $state 用于永远不会变化的值 -->
<script lang="ts">
  let config = $state({ timeout: 5000 });  // 不需要响应式
  const API_URL = $state('/api');           // 常量不需要 $state
</script>

<!-- ✅ 常量直接声明 -->
<script lang="ts">
  const config = { timeout: 5000 };
  const API_URL = '/api';

  // $state 只用于会变化的值
  let count = $state(0);
  let user = $state<User | null>(null);
</script>
```

### $state.raw 与大型对象

```svelte
<!-- ✅ $state.raw 避免深度代理 -->
<script lang="ts">
  let data = $state.raw(hugeApiResponse);

  async function refresh() {
    data = await fetchLatestData();  // ✅ triggers reactivity
  }
</script>
```

### 解构 $state 丢失响应性

```svelte
<!-- ❌ 解构 $state 对象丢失响应性 -->
<script lang="ts">
  let state = $state({ count: 0, name: 'Svelte' });
  let { count, name } = state;  // count and name are plain values!
</script>
<p>{count}</p>  <!-- ❌ will NOT update -->

<!-- ✅ 直接访问 $state 属性 -->
<script lang="ts">
  let state = $state({ count: 0, name: 'Svelte' });
</script>
<p>{state.count}</p>  <!-- ✅ stays reactive -->
```

---

### $derived 正确用法

```svelte
<!-- ❌ 反模式：用 $effect 做状态同步 -->
<script lang="ts">
  let firstName = $state('John');
  let lastName = $state('Doe');
  let fullName = $state('');

  $effect(() => {
    fullName = `${firstName} ${lastName}`;  // unnecessary effect
  });
</script>

<!-- ✅ 使用 $derived 计算派生值 -->
<script lang="ts">
  let firstName = $state('John');
  let lastName = $state('Doe');
  let fullName = $derived(`${firstName} ${lastName}`);
</script>
```

---

### $effect 正确用法

#### 无限循环

```svelte
<!-- ❌ $effect 中更新自身依赖 → 无限循环 -->
<script lang="ts">
  let count = $state(0);

  $effect(() => {
    console.log(count);
    count++;  // modifying dependency inside effect → infinite loop!
  });
</script>
```

#### 清理函数

```svelte
<!-- ✅ 返回清理函数 -->
<script lang="ts">
  let roomId = $state('');

  $effect(() => {
    const ws = new WebSocket(`ws://example.com/${roomId}`);
    ws.onmessage = (e) => {
      messages = [...messages, JSON.parse(e.data)];
    };
    return () => ws.close();  // cleanup on re-run
  });
</script>
```

#### async $effect 的追踪陷阱

```svelte
<!-- ❌ await 后读取的状态不会被追踪 -->
<script lang="ts">
  $effect(async () => {
    const user = await fetchUser(userId);   // userId IS tracked
    const theme = preference;               // NOT tracked (read after await)!
    applyTheme(user, theme);
  });
</script>

<!-- ✅ 在 await 前读取所有依赖 -->
<script lang="ts">
  $effect(async () => {
    const currentPref = preference;  // read before await
    const user = await fetchUser(userId);
    applyTheme(user, currentPref);
  });
</script>
```

#### untrack 排除依赖

```svelte
<!-- ✅ untrack 排除不相关的依赖 -->
<script lang="ts">
  import { untrack } from 'svelte';

  $effect(() => {
    if (untrack(() => debugMode)) {  // debugMode is NOT tracked
      console.log('data changed', data);
    }
  });
</script>
```

---

## Load 函数（Server vs Client）

### +page.server.js vs +page.js

```typescript
// ❌ 在 +page.js 中访问数据库或 secrets
// src/routes/admin/+page.js
export async function load({ fetch }) {
  const data = await db.query('SELECT * FROM users');  // db not available in browser!
  return { users: data };
}

// ✅ 服务端逻辑放在 +page.server.js
// src/routes/admin/+page.server.js
import { db } from '$lib/server/db';

export async function load() {
  const users = await db.query('SELECT * FROM users');
  return { users };
}
```

### await parent() 瀑布流

```typescript
// ❌ 顺序 await parent → 瀑布流
export async function load({ parent, fetch }) {
  const parentData = await parent();  // wait for parent
  const post = await fetch(`/api/posts/${parentData.blogId}`);
  return { post };
}

// ✅ 尽可能并行，避免不必要的 parent await
export async function load({ parent, fetch }) {
  const post = await fetch('/api/posts/slug');
  return { post };
}
```

---

## Form Actions

### 使用 POST 处理副作用

```typescript
// src/routes/users/+page.server.js
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
  delete: async ({ request, locals }) => {
    const formData = await request.formData();
    const id = formData.get('id');

    if (!id) return fail(400, { message: 'Missing id' });

    await locals.db.users.delete(id);
    throw redirect(303, '/users');
  }
};
```

```svelte
<!-- form with progressive enhancement -->
<script lang="ts">
  import { enhance } from '$app/forms';
</script>

<form method="POST" action="?/delete" use:enhance>
  <input type="hidden" name="id" value={user.id} />
  <button type="submit">Delete</button>
</form>
```

### fail() 中不暴露敏感信息

```typescript
// ❌ fail() 中返回敏感信息
return fail(401, {
  password: formData.get('password'),  // ❌ exposes password!
  hint: user.passwordHint,             // ❌ leaks internal data!
});

// ✅ 只返回安全的错误信息
return fail(401, {
  email,                    // ✅ safe to echo back
  incorrect: true,          // ✅ generic error flag
});
```

---

## Store 迁移（→ $state）

### writable/readable → $state

```typescript
// ❌ Legacy store pattern (Svelte 4)
import { writable, derived } from 'svelte/store';

export const user = writable(null);
export const isLoggedIn = derived(user, $user => !!$user);

// ✅ Svelte 5: shared state in .svelte.js files
// src/lib/stores/user.svelte.js
let currentUser = $state<User | null>(null);

export function getUser() {
  return currentUser;
}

export function setUser(user: User | null) {
  currentUser = user;
}
```

### .svelte.js / .svelte.ts 扩展名

```typescript
// ❌ 在普通 .js 文件中使用 runes → 编译错误
// src/lib/utils.js
let state = $state(0);  // runes only work in .svelte.js files!

// ✅ 使用 .svelte.js 扩展名
// src/lib/utils.svelte.js
let state = $state(0);
```

---

## SSR vs CSR 边界

### 浏览器全局变量在 SSR 中

```svelte
<!-- ❌ 在模块顶层访问浏览器 API -->
<script lang="ts">
  const height = window.innerHeight;        // ReferenceError during SSR!
</script>

<!-- ✅ 在 onMount 或 browser guard 中访问 -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  let height = $state(0);

  onMount(() => {
    height = window.innerHeight;
  });
</script>
```

---

## 响应式语句迁移

### $: → $derived / $effect

```svelte
<!-- ❌ Svelte 4 响应式语句 -->
<script lang="ts">
  let count = 0;
  let doubled = 0;

  $: doubled = count * 2;
  $: if (count > 10) console.log('big');
</script>

<!-- ✅ Svelte 5 runes -->
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);

  $effect(() => {
    if (count > 10) console.log('big');
  });
</script>
```

### slot → @render children()

```svelte
<!-- ❌ Svelte 4 slot -->
<div class="card">
  <slot />
</div>

<!-- ✅ Svelte 5 snippets -->
<script lang="ts">
  let { children } = $props();
</script>
<div class="card">
  {@render children()}
</div>
```

---

## 性能优化

### $state.raw 用于大型不可变数据

```svelte
<!-- ✅ $state.raw 避免深度代理 -->
<script lang="ts">
  let searchResults = $state.raw<SearchResult[]>([]);

  async function search(query: string) {
    searchResults = await fetchResults(query);  // whole-array replacement
  }
</script>
```

### Streaming 与 load 中的 Promise

```typescript
// ❌ 串行等待所有数据 → 页面阻塞
export async function load({ params }) {
  const posts = await getPosts();       // slow
  const comments = await getComments(); // slow
  const tags = await getTags();         // slow
  return { posts, comments, tags };
}

// ✅ 并行加载独立数据
export async function load({ params }) {
  return {
    posts: getPosts(),       // return promises directly for streaming
    comments: getComments(),
    tags: getTags(),
  };
}
```

---

## 安全审查

### 不暴露私有环境变量

```typescript
// ❌ 在 universal load 中暴露服务端 secrets
export async function load() {
  return {
    apiKey: process.env.SECRET_API_KEY,    // exposed to client bundle!
  };
}

// ✅ 私有环境变量只在 server load 中使用
// +page.server.js (server-only)
export async function load({ locals }) {
  const data = await fetch(process.env.SECRET_API_KEY + '/admin');
  return { data };  // only derived data is sent to client
}
```

### Cookie 安全设置

```typescript
// ✅ 安全的 Cookie 配置
import { dev } from '$app/environment';

event.cookies.set('session', token, {
  path: '/',
  httpOnly: true,          // not accessible via JS
  secure: !dev,            // HTTPS only in production
  sameSite: 'lax',         // CSRF protection
  maxAge: 60 * 60 * 24 * 7 // 1 week, explicit expiry
});
```

---

## Review Checklist

### Runes
- [ ] $state 只用于会变化的值，常量直接声明
- [ ] 大型不可变数据使用 $state.raw
- [ ] 没有解构 $state 对象（会丢失响应性）
- [ ] $derived 中没有副作用
- [ ] 没有用 $effect 替代 $derived 做状态同步
- [ ] $effect 中不修改被追踪的状态（避免无限循环）
- [ ] $effect 有清理函数（订阅、定时器、WebSocket）
- [ ] async $effect 在 await 前读取所有需要追踪的状态

### Load 函数
- [ ] 服务端逻辑放在 +page.server.js（不是 +page.js）
- [ ] 避免不必要的 await parent() 瀑布流
- [ ] 独立数据并行加载（Promise.all 或直接返回 Promise）

### Form Actions
- [ ] 副作用操作（增删改）使用 form actions + POST
- [ ] fail() 不返回敏感信息
- [ ] 使用 use:enhance 实现渐进增强

### Store 迁移
- [ ] writable/readable → $state 在 .svelte.js 文件中
- [ ] 不在普通 .js 文件中使用 runes
- [ ] 不使用遗留的 $ 前缀 store 语法

### SSR vs CSR 边界
- [ ] 不在根 layout 中全局禁用 SSR
- [ ] 浏览器 API 在 onMount 或 browser guard 中使用

### 安全审查
- [ ] 私有环境变量只在 server load 中使用
- [ ] 服务端代码放在 $lib/server/ 目录
- [ ] Cookie 设置 httpOnly、secure、sameSite