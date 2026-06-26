---
name: core-theme
description: Naive UI documentation for Create Themed Component
---

# Create Themed Component

You may not want to use only the provided components and want to write themed components.

Naive UI provides some tools for developers to create themed components easier.

## Demos

### provide-theme.vue

```vue
<script setup lang="ts">
import { darkTheme } from 'naive-ui'
import { ref } from 'vue'

const theme = ref<typeof darkTheme | null>(null)
</script>

<template>
  <n-config-provider :theme="theme">
    <n-card>
      <n-space>
        <n-button @click="theme = darkTheme">
          Dark
        </n-button>
        <n-button @click="theme = null">
          Light
        </n-button>
      </n-space>
    </n-card>
  </n-config-provider>
</template>
```

### element.vue

```vue
<script lang="ts" setup>
import { darkTheme } from 'naive-ui'
import { ref } from 'vue'

const theme = ref<typeof darkTheme | null>(null)
</script>

<template>
  <n-space vertical>
    <n-space>
      <n-button @click="theme = darkTheme">
        Dark
      </n-button>
      <n-button @click="theme = null">
        Light
      </n-button>
    </n-space>
    <n-config-provider :theme="theme">
      <n-card>
        <n-el
          tag="span"
          style="
            color: var(--primary-color);
            transition: 0.3s var(--cubic-bezier-ease-in-out);
          "
        >
          I am a Span.
        </n-el>
      </n-card>
    </n-config-provider>
  </n-space>
</template>
```

### use-theme-vars.vue

```vue
<script setup lang="ts">
import { useThemeVars } from 'naive-ui'

const themeVars = useThemeVars()
</script>

<template>
  <pre style="overflow: auto">{{ themeVars }}</pre>
</template>
```


## Theme Colors Not Applied in Dark Mode

Custom primary color works in light mode but not dark mode because `primaryColorSuppl` is required for dark mode.

**Incorrect (light mode works, dark mode doesn't):**

```vue
<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <app />
  </n-config-provider>
</template>

<script setup>
import { darkTheme } from 'naive-ui'

const themeOverrides = {
  common: {
    primaryColor: '#2080f0'  // Incorrect: Only works in light mode
  }
}
</script>
```

**Correct (set primaryColorSuppl for dark mode):**

```vue
<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <app />
  </n-config-provider>
</template>

<script setup lang="ts">
import { darkTheme } from 'naive-ui'

const themeOverrides = {
  common: {
    primaryColor: '#2080f0',
    primaryColorHover: '#4098fc',
    primaryColorPressed: '#1060c9',
    primaryColorSuppl: '#4098fc'  // Correct: Required for dark mode
  }
}
</script>
```

**Complete Dark Theme Setup:**

```vue
<script setup lang="ts">
import { darkTheme } from 'naive-ui'

const darkThemeOverrides = {
  common: {
    // Primary colors
    primaryColor: '#63e2b7',
    primaryColorHover: '#7fe7c4',
    primaryColorPressed: '#5acea7',
    primaryColorSuppl: '#4098fc',  // For dark mode

    // Background colors
    bodyColor: '#101014',
    cardColor: '#18181c',
    modalColor: '#18181c',
    popoverColor: '#18181c',

    // Text colors
    textColorBase: '#fff',
    textColor1: 'rgba(255, 255, 255, 0.9)',
    textColor2: 'rgba(255, 255, 255, 0.82)',

    // Border
    borderColor: 'rgba(255, 255, 255, 0.09)',
    dividerColor: 'rgba(255, 255, 255, 0.09)'
  }
}
</script>
```

**useThemeVars in Drawer/Modal:**

```vue
<script setup lang="ts">
import { useThemeVars } from 'naive-ui'

// Call at root level, NOT inside drawer/modal
const themeVars = useThemeVars()
</script>

<template>
  <n-drawer>
    <n-drawer-content>
      
      <div :style="{ color: themeVars.primaryColor }">
        Content
      </div>
    </n-drawer-content>
  </n-drawer>
</template>
```

**Theme Editor:**

Use the online theme editor at https://www.naiveui.com/ (bottom right icon) to visually customize themes and export the configuration.
