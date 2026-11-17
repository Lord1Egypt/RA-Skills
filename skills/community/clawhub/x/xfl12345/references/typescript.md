---
name: typescript
description: TypeScript 编码规范。编写任何 TypeScript 源码时都应触发。
---

# TypeScript

> 本规范继承 [javascript.md](./javascript.md) 全部约定，后文仅列 TS 的差异与补充。

## Coding Practices

### 类型系统

- 让类型「从源头正确」，而不是事后用 `as` 矫直——编译器全程参与校验：对象类型、联合/交叉类型的变量在定义处就给足类型信息（显式注解 / 泛型参数 / 从 schema 推断皆可）；因为 `as` 断言会把检查降级为沉默，所以除非 `as const` 尽量少用 `as`：

  ```typescript
  import { z } from 'zod'

  // schema 即类型源头：运行时校验 + 静态类型一次搞定，单一真源
  const UserSchema = z.object({
    id: z.number(),
    name: z.string(),
  })
  type User = z.infer<typeof UserSchema>

  const raw = '{"id":1,"name":"Ann"}'
  const data: unknown = JSON.parse(raw)

  // ❌ BAD: as 直接断言，编译器闭嘴——形状错了运行时才炸
  const badUser = data as User
  const badInput = document.querySelector('#app') as HTMLInputElement

  // ✅ GOOD：让类型「从源头正确」，编译器全程参与校验
  const user2: User = { id: 2, name: 'Ben' }
  const input = document.querySelector<HTMLInputElement>('#app') // 泛型从源头带类型

  // ❌ BAD：在顶层 as，产物会外泄到后续代码，骗编译器的影响面扩大
  const badRecord = data as Record<string, unknown>

  // ✅ GOOD：不信任的外部数据（JSON / 接口返回）首选 zod：safeParse 校验通过才拿到 User
  const parsed = UserSchema.safeParse(data)
  if (parsed.success) {
    parsed.data // User
  }

  //   手写类型守卫也行（无 zod 依赖时），但值类型要查全——只查键的话 x is User 就是半句谎话，等于换个地方骗编译器
  function isUser(x: unknown): x is User {
    if (typeof x !== 'object' || x === null) return false
    const o = x as Record<string, unknown> // 守卫内部受控的 as，不外泄污染到外部世界
    return typeof o.id === 'number' && typeof o.name === 'string'
  }
  const maybeUser = isUser(data) ? data : null

  // ✅ 例外：as const 把字面量「收紧」成字面量类型，是收紧不是放松，放心用
  const EXAMPLE_USER = { id: 999, name: 'Foo' } as const satisfies User
  ```

- `as const` 常量必须以 `satisfies`（TS 4.9+）补齐类型约束：`as const` 与类型注解（Type Annotation）在同一声明中不可兼得——变量类型随注解而定，字面量收窄随之失效；`satisfies` 只做赋值兼容性校验、不改变推断结果，恰好承担注解本应提供的三项职责：校验常量自身形状、匹配消费者类型签名、同步上游类型约束：

  ```typescript
  import type { RouteNamedMap } from 'vue-router/auto-routes'
  export const ROUTER_NAMES = {
    INDEX: '/',
    ADMIN: '/admin',
    LOGIN: '/login',
    PLAYGROUND_INDEX: '/playground/',
    ROUTES: '/routes',
  } as const satisfies Record<string, keyof RouteNamedMap>

  export interface Foo { a: number, b: boolean, c: string }
  export const DEFAULT_FOO = { a: 1, b: true, c: 'Hello' } as const satisfies Foo
  ```

- 非空断言（Non-null Assertion）`!` 默认禁用——与 `as` 同属「让编译器闭嘴」，且断错即运行时炸。缺失场景一律用可选链 / 显式收窄表达；仅当「存在性刚被保证、编译器却推不出」时可用，且必须注释缘由：

  ```typescript
  // ❌ BAD: 断言抹掉 null | undefined，元素不存在就是 undefined.value 运行时炸
  const badName = document.querySelector<HTMLInputElement>('#app')!.value

  // ✅ GOOD: 可选链 + ?? 兜底，缺失是可处理的正常分支
  const safeName = document.querySelector<HTMLInputElement>('#app')?.value ?? ''

  // ✅ 可接受：同一同步块内刚做完存在性守卫，编译器却推不出——注释写明依据
  if (sessions.has(id)) {
    return sessions.get(id)! // 上方 has 守卫过；TS 不联动收窄 get 的返回值
  }
  ```

- 除非万不得已，严禁 `any`。除不信任数据的入口边界外，尽量避免 `unknown`，优先提供确切的类型。`unknown` 仅用于不信任数据的边界，接住即收窄，勿偷懒当作万能类型
- 善用 `enum` 做枚举（限 string 枚举：数字枚举存在反向映射，`Object.values()` 会混入镜像数字成员），并从中取常量数组（`Object.values()` / `Object.keys()`）：

  ```typescript
  // TheConst.ts
  export enum NginxNjsDirective {
    JS_IMPORT = 'js_import',
    JS_PRELOAD_OBJECT = 'js_preload_object',
    JS_ACCESS = 'js_access',
  }
  export const NGINX_NJS_DIRECTIVES: ReadonlyArray<NginxNjsDirective> = Object.values(NginxNjsDirective)
  export const NGINX_NJS_DIRECTIVE_SET: ReadonlySet<NginxNjsDirective> = new Set(NGINX_NJS_DIRECTIVES)
  ```

- 别把 enum 重构成 `as const` 对象 + `keyof typeof` 字符串联合——那不是优化，是降级：联合类型只是裸字符串并集，任何匹配的字面值都能直接塞进来，与枚举对象的强绑定随之消失（函数参数一旦收窄成字符串联合，调用点就开始散落魔法字符串，枚举对象被架空）；string enum 是封闭类型，裸字符串赋不进去，成员引用与重命名重构始终锚定在枚举上
- 「避免 enum」的官方忠告只针对库作者：对外发布的 `.ts` 源码可能被消费方开启 `erasableSyntaxOnly`（纯 Node 原生跑 TS 必配）直接运行，enum 这类不可擦除语法才会报错。项目内部使用有编译/打包转换兜底，不受此影响。仅当源码原样对外发布、或项目本身强制 `erasableSyntaxOnly` 时，才降级为 `as const` 对象 + `type X = typeof M[keyof typeof M]` 等价实现

- 尽量复用已有类型——优先使用第三方库导出/推导的类型（如 `z.infer`、vue-router 的 `RouteNamedMap`、索引取型的 `CSSProperties['width']` / `HTMLAudioElement['textTracks']`），再善用 `Omit` / `Pick` / `Exclude` / `Extract` / `Parameters` / `ReturnType` / `InstanceType` / `Required` / `Partial` / `Readonly` / `Record` 等工具类型对其加工，勿手写复刻：

  ```typescript
  import type { Writable } from 'type-fest'

  // 从浏览器只读契约中提取可写镜像——Pick 选字段、Writable 解除只读，零手写字段类型
  interface FoxyScreenState extends Writable<
    Pick<Screen, 'width' | 'height' | 'availWidth' | 'availHeight'>
  > {}
  const foxyScreenState: FoxyScreenState = {
    width: window.screen.width,
    height: window.screen.height,
    availWidth: window.screen.availWidth,
    availHeight: window.screen.availHeight,
  }
  ```
- 声明对象形状一律用 `interface`，勿用 `type`（反模式）——interface 报错信息更友好、可被声明合并扩充、`extends` 有编译期缓存优势；`type` 只留给 interface 表达不了的形状：

  ```typescript
  import type { CSSProperties } from 'vue'

  // ❌ BAD: 对象形状用 type 别名
  type BadgeStatus = { text: string, color: string }

  // ✅ GOOD: 对象形状一律 interface；上游有现成契约就按键取型，不自造
  interface AudioPlayerProps {
    width?: CSSProperties['width']            // 样式值：从 Vue 的 CSS 契约按键取型，勿手写 string | number
    tracks?: HTMLAudioElement['textTracks']   // 轨道列表：从 DOM 接口按键取型，勿手写 TextTrackList
  }

  // ✅ type 的领地：跨类型联合 / 源头推导 / 工具类型加工——interface 与 enum 均表达不了
  type User = z.infer<typeof UserSchema>
  type CacheKey = string | number   // 跨类型联合；同族字面量互斥态（如 'idle' | 'done'）是 string enum 的辖区，勿在此处用裸联合
  type RouteName = keyof RouteNamedMap
  ```
- object key 有范围约束时，用 `keyof` 从源头对象推导键类型，避免 `string` / `Record<string, …>` 式宽松匹配：

  ```typescript
  // 源头：频道事件名的唯一出处
  const CHANNEL_EVENTS = {
    MESSAGE: 'message',
    TYPING: 'typing',
    REACTION: 'reaction',
  } as const satisfies Record<string, string>

  // 各事件的载荷类型，键与 CHANNEL_EVENTS 一一对应
  interface ChannelEventPayloadMap {
    MESSAGE: { id: string, text: string }
    TYPING: { userId: string }
    REACTION: { messageId: string, emoji: string }
  }

  // ❌ BAD: 键放宽为 string——'messge'（手滑）照样注册成功，监听器永不触发且无任何报错；
  //        payload 也只能含糊成 unknown，消费侧还得自行断言
  const badHandlers: Record<string, (payload: unknown) => void> = {}

  // ✅ GOOD: 键域从源头 keyof 推导、载荷按键精确查找——事件增删自动跟随，
  //         拼错键直接编译报错，每个 handler 的 payload 都是确切类型
  type ChannelHandlerTable = {
    [K in keyof typeof CHANNEL_EVENTS]: (payload: ChannelEventPayloadMap[K]) => void
  }
  const goodHandlers: ChannelHandlerTable = {
    MESSAGE: (msg) => msg.text,
    TYPING: (t) => t.userId,
    REACTION: (r) => r.emoji,
  }

  // 线上事件名值域同理可推：
  type ChannelEventName = typeof CHANNEL_EVENTS[keyof typeof CHANNEL_EVENTS]
  ```
- 如遇深层结构、过于复杂的类型时，尽量使用 `type-fest` 完成类型体操
- undefined 规范继承自 [javascript.md](./javascript.md)，TS 的唯一例外：作「类型」用时照写 `undefined`——类型位置不存在遮蔽问题：

  ```typescript
  type Status = 'idle' | 'done' | undefined
  ```

### 模块导入

模块导入规范见 [typescript-esm.md](./typescript-esm.md)，按下述条件触发：

- **适用场景**：打包器项目（Vite / webpack 等——模块说明符由打包器解析）中写、改、审任何 `import` 语句。后缀省略、index 目录别名、引用具体度、相对/绝对层级阈值、barrel、内联 type 拆分等全部以该文件为准
- **不适用场景**：纯 Node 原生环境（node 解释器直接执行 `.ts`：type stripping / nodenext）——该文件的规范与之相反，勿套用
