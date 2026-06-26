---
number: 324
title: "Incorrect generated types & fix for \"eslint@typescript-eslint/unbound-method\" error"
type: question
state: closed
created: 2021-01-26
url: "https://github.com/intlify/vue-i18n/issues/324"
reactions: 10
comments: 8
labels: "[help wanted, Type: Improvement]"
---

# Incorrect generated types & fix for "eslint@typescript-eslint/unbound-method" error


### vue & vue-i18n version
ex:
- vue: 3.0.5
- vue-i18n: 9.0.0-rc.4

### What is actually happening?
Hi there!
I'm testing the new package version and I got stuck for a while on a couple of problems related to the generated types:
- `declare` keyword used on `type` and `interface` exports, which has no effect (AFAIK)
- declaration of `useI18n` functions using method style (`t(): string`) instead of property style (`t: () => string`), which causes a "eslint@typescript-eslint/unbound-method" linting error when destructured

The first problem shouldn't have any side effect, it's just pointless: `declare` keyword has no effect when used in that way. You should probably remove those anyway, just to be sure.

The second one would force anyone using TypeScript linter to disable an error every time the composable is used.
I guess you defined those using the method notation to be able to add overloads, but TS assume that functions on object defined with method notation MIGHT be using the local context, that's why the linter then complains about this.
You can accomplish the same thing by declaring those functions and overloads at root level, then adding a property with the function name and with type as the `typeof` of the declared function.

Example: 
```ts
declare function t(key: Path | number): string;
declare  function t(key: Path | number, plural: number, options?: TranslateOptions): string;
declare function t(key: Path | number, defaultMsg: string, options?: TranslateOptions): string;
// Other overloads

export interface Composer<Messages = {}, DateTimeFormats = {}, NumberFormats = {}, Message = VueMessageType> {
    // other properties
    t: typeof t;
    // other properties
}
```

I tried this out on-the-fly and it seems to work correctly.
Other Vue3-ready packages I used doesn't seem to share this problem

---

## Top Comments

**@kazupon** [maintainer]:

Hmm,  
The `*.d.ts` of  vue-i18n-next is generated with api-extractor.
https://github.com/microsoft/rushstack/tree/master/apps/api-extractor

I think that api-extractor have problems.

**@kazupon** [maintainer]:

Yeah, we can solve the second problem, but we run into the problem of not being able to generate API references automatically.

The API references in vue-i18n-next use api-extractor and api-docs-gen and generator.
For cases like `t: typeof t`, We can use `@inheritDoc` to copy from another comment.
However, it is not currently working. The issue has been registered in an issue...
https://github.com/microsoft/rushstack/issues/2062

As we are planning to release v9 officially soon, I want to avoid stopping the automatic generation of API reference.

Acturally, I also checked about `@type...

**@IlCallo** (+1):

> I prefer that you would like to use eslint-disable (e.g. /* eslint-disable-line @typescript-eslint/unbound-method */) to work around it.

We surely can, but this means everyone using this package with Composition API and TypeScript will have to disable that rule **every time** it's destructured (or disable it altogether, which isn't really acceptable). This translates to using it nearly many times as the number of your components (if you're using pure Composition API style you suggest).

It seems strange all composables from other Vue ecosystem packages don't have this problems, and some...