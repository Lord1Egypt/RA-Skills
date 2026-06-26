---
number: 14189
title: Specific Build/Run Errors in Vue Web Game Project
category: Help/Questions
created: 2025-12-10
url: "https://github.com/orgs/vuejs/discussions/14189"
upvotes: 1
comments: 1
answered: true
---

# Specific Build/Run Errors in Vue Web Game Project

Hi,
I’m getting the following errors when trying to run my Vue game project.

Commands:
```
npm install
npm run dev
```
Error Output:
```
[vite] Internal server error: Failed to resolve import "@/components/GameBoard.vue"
Error: Cannot find module '/src/components/GameBoard.vue'
    at resolve (node:internal/modules/esm/resolve:1233)
```

And during build:
```
Error: Cannot read properties of undefined (reading 'hooks')
    at createPluginContainer (vite/dist/node/chunks/dep-56f75469.js:5321)
```
Does anyone know how to fix these module resolution issues?

Thanks!

---

## Accepted Answer

The error indicates that Vite can't resolve the file at @/components/GameBoard.vue.
Please verify that:
The file actually exists in src/components/.
The filename matches exactly, including capitalization.
Your vite.config.js includes the correct alias:
`resolve: { alias: { '@': '/src' } }`
Fixing the path or alias should resolve both errors.