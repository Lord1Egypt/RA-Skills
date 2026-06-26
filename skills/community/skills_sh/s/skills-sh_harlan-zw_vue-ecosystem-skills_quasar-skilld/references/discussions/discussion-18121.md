---
number: 18121
title: NPM audit vulnerabilities on inquirer dependence of TMP package
category: CLI - SSR mode
created: 2025-09-05
url: "https://github.com/quasarframework/quasar/discussions/18121"
upvotes: 2
comments: 1
answered: true
---

# NPM audit vulnerabilities on inquirer dependence of TMP package

"@quasar/app-vite": "^2.3.0"

# npm audit report

tmp  <=0.2.3
tmp allows arbitrary temporary file / directory write via symbolic link `dir` parameter - https://github.com/advisories/GHSA-52f5-9888-hmc6

---

## Accepted Answer

Also reported here: https://github.com/quasarframework/quasar/discussions/18115