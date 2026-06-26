---
name: core-experimental-features
description: Naive UI documentation for Experimental Features
---

# Experimental Features

> [!WARNING]
> **Caveats**
> 
> The following features are **unstable**. Use them if you really need and prepare to follow the API changes.

## Use TuSimple Theme

```vue
<script>
  import { TsConfigProvider, useDialog, useMessage } from '@naive-ui/tusimple-theme'

  // danger typed api
  const dialog = useDialog()
  dialog.danger(...)

  const message = useMessage()
  message.danger(...)
</script>

<template>
  <ts-config-provider>
    <my-app />
  </ts-config-provider>
</template>
```
