---
number: 3087
title: 解决 vue2.7使用 pnpm 和 pinia 2.x  hasInjectionContext 报错
category: Help and Questions
created: 2025-12-17
url: "https://github.com/vuejs/pinia/discussions/3087"
upvotes: 1
comments: 1
answered: true
---

# 解决 vue2.7使用 pnpm 和 pinia 2.x  hasInjectionContext 报错


看了很多帖子，都说和vue2.7 不兼容，需要降级到2.0.x,但还是没有效果，pinia 2.x的最后更新版本也支持2.7,使用yarn可以运行，使用pnpm就报错

> https://github.com/vuejs/pinia/blob/v2/packages/pinia/CHANGELOG.md
```md
2.3.1 (2025-01-20)
Bug Fixes
types: support for Vue 2.7 (d14e1a7)

```

## 环境说明
package.json
```json
 "dependencies": {
    "pinia": "2.3.1",
    "vue": "2.7.16"
  }

```

## 报错信息

报错关键字：`export 'hasInjectionContext' (imported as 'hasInjectionContext')`
报错信息：
...

---

## Accepted Answer

**@posva** [maintainer]:

Because `hasInjectionContext` is only available through vue-demi.