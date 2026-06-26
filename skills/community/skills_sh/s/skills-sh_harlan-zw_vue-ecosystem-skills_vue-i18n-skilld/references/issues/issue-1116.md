---
number: 1116
title: Typescript allows passing any string as t() argument
type: feature
state: open
created: 2022-08-09
url: "https://github.com/intlify/vue-i18n/issues/1116"
reactions: 19
comments: 8
labels: "[Status: Proposal,  p4-important, typescript]"
---

# Typescript allows passing any string as t() argument

### Clear and concise description of the problem

I followed all the steps from the Typescript support page but it does not give an error when I use the `t` function with a missing key.

It does show autocomplete suggestions in the template though.

### Suggested solution

Typescript should give an error when trying to use a key that is not in the schema

### Alternative

_No response_

### Additional context

_No response_

### Validations

- [X] Read the Contributing Guidelines
- [X] Read the Documentation
- [X] Check that there isn't already an issue that request the same feature to avoid creating a duplicate.

---

## Top Comments

**@larrifax** (+4):

Think I got this working by creating my own wrapper composable returning a `t()` function with custom types:
```
type Translations = Messages["en"];

type PathToLeaves<T, Cache extends string = ""> = T extends PropertyKey
  ? Cache
  : {
      [P in keyof T]: P extends string
        ? Cache extends ""
          ? PathToLeaves<T[P], `${P}`>
          : PathToLeaves<T[P], `${Cache}.${P}`>
        : never;
    }[keyof T];

type TranslationPaths = PathToLeaves<Translations>;

export const useTranslation = () => {
  const { t } = useI18n<{ messages: Messages }>();

  return { t: (path: TranslationPaths, named?: NamedValue) => (named ? t(path, named) : t(path)) } as const;
};
```...

**@Vissie2** (+2):

Even though the workaround from @larrifax is somewhat helpful. I'm having a difficult time taking into account all overloads of `t()` to make usage possible for all parameters. Especially because we can't just make a type of the function overloads due to a design limitation of TypeScript (https://github.com/microsoft/TypeScript/issues/32164).

This is also a problem for other translation functions like `tm()` and `rt()`.

**@OfekA-IAI** (+2):

> Even though the workaround from @larrifax is somewhat helpful. I'm having a difficult time taking into account all overloads of `t()` to make usage possible for all parameters. Especially because we can't just make a type of the function overloads due to a design limitation of TypeScript ([microsoft/TypeScript#32164](https://github.com/microsoft/TypeScript/issues/32164)).
> 
> This is also a problem for other translation functions like `tm()` and `rt()`.

Agree, it's working but a pain to do and configure. This should be built in 