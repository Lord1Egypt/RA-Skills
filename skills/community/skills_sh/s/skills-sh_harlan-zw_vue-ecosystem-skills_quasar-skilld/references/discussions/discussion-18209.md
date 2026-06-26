---
number: 18209
title: "[Feature Request] Update SSR template to Express 5"
category: CLI - SSR mode
created: 2026-01-08
url: "https://github.com/quasarframework/quasar/discussions/18209"
upvotes: 2
comments: 0
answered: false
---

# [Feature Request] Update SSR template to Express 5

### Title: [Feature Request] Update SSR Scaffold to Express 5.0
### Description
Since **Express 5.0.0** was officially released as stable (October 2024), it is now the current industry standard. However, the current Quasar SSR starter template (via `@quasar/app-vite` / `@quasar/app-webpack`) still scaffolds projects using Express 4.

Currently, new users starting a Quasar SSR project are encountering a breaking change error:
`error: Missing parameter name at index 1: *; visit https://git.new/pathToRegexpError for info`

### Why upgrade to Express 5?
* **Native Async Support:** Express 5 now handles rejected promises automatically. This simplifies SSR middlewares by removing the need for manual `try/catch` or helper packages like `express-async-errors`.
* **Path Matching:** The upg...