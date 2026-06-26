---
number: 1198
title: typescript 4.8 support
type: other
state: closed
created: 2022-10-14
url: "https://github.com/intlify/vue-i18n/issues/1198"
reactions: 9
comments: 7
resolvedIn: 9.3.0
labels: "[ p4-important, typescript]"
---

# typescript 4.8 support

### Reporting a bug?

With a simple vue 3 and vue-i18n (e.g. v9.2+) typescript (v4.8+) setup, hundreds of circular constraints and index errors are thrown when building (tsc -c)
```
node_modules/.pnpm/@intlify+core-base@9.3.0-beta.6/node_modules/@intlify/core-base/dist/core-base.d.ts:791:51 - error TS2313: Type parameter 'Context' has a circular constraint.

791 export declare function translate, Key extends string = string, ResourceKeys extends PickupKeys<Context['messages']> = PickupKeys<Context['messages']>, Message = string>(context: Context, key: Key | ResourceKeys | number | MessageFunction<Message>, defaultMsg: string): MessageType<Message> | number;
                                                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

node_modules/.pnpm/@intlify+core-base@9.3.0-beta.6/node_modules/@intlify/core-base/dist/core-base.d.ts:791:72 - error TS2536: Type '"messages"' cannot be used to index type 'Context'.

791 export declare function translate, Key extends string = string, ResourceKeys extends PickupKeys<Context['messages']> = PickupKeys<Context['messages']>, Message = string>(context: Context, key: Key | ResourceKeys | number | MessageFunction<Message>, defaultMsg: string): MessageType<Message> | number;
```
This does not happen in <4.7.4.
As a workaround, it is possible to `"skipLibCheck": true` i...

---

## Top Comments

**@kazupon** [maintainer] (+4):

I've just released out vue-i18n v9.3.0-beta.11 
You can install `next` dist tag!

Thanks!

**@ameinhardt** (+5):

@kazupon : that looks promising, thanks! With updated dependencies, I 'only' get a different  error on `npm run build`:
```bash
src/App.vue:19:8 - error TS2339: Property '$t' does not exist on type '{ $: ComponentInternalInstance; $data: {}; $props: Partial<{}> & Omit<Readonly<ExtractPropTypes<{}>> & VNodeProps & AllowedComponentProps & ComponentCustomProps, never>; ... 10 more ...; $watch<T extends string | ((...args: any) => any)>(source: T, cb: T extends (...args: any) => infer R ? (args_0: R, args_1: R) => ...'.

19     {{ $t('hello') }}
          ~~
Found 1 error in src/App.vue:19
```...

**@Shinigami92** (+2):

Tested with `9.2.2` and `9.3.0-beta.6`
With both + TS 4.8 I get around 160 compile-time issues
I don't want to set `"skipLibCheck": true`, because this disables **all** checks for every dependency, not just `vue-i18n`