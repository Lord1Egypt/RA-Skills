<!--
  Copy to <your-slidev-project>/components/AntdThemeProvider.vue

  Wrap any dashboard slide content in <AntdThemeProvider> ... </AntdThemeProvider>.
  It:
    - applies design tokens (primary color, border radius) via a-config-provider
    - sets a default component size
    - syncs Ant Design's dark algorithm to Slidev's dark mode
    - makes the dashboard fill the slide canvas

  Props:
    size          'small' | 'middle' | 'large'   (default 'middle'; use 'small' for dense dashboards)
    primaryColor  hex string                       (default Ant blue #1677ff)
    radius        number (px)                       (default 8)
-->
<script setup lang="ts">
import { computed } from 'vue'
import { theme as antdTheme } from 'ant-design-vue'
import { isDark } from '@slidev/client'
// If your Slidev version doesn't export `isDark`, swap the line above for:
//   import { useDark } from '@vueuse/core'
//   const isDark = useDark()

const props = withDefaults(
  defineProps<{
    size?: 'small' | 'middle' | 'large'
    primaryColor?: string
    radius?: number
  }>(),
  { size: 'middle', primaryColor: '#1677ff', radius: 8 },
)

const themeConfig = computed(() => ({
  algorithm: isDark.value ? antdTheme.darkAlgorithm : antdTheme.defaultAlgorithm,
  token: {
    colorPrimary: props.primaryColor,
    borderRadius: props.radius,
    fontSize: 14,
  },
}))
</script>

<template>
  <a-config-provider :theme="themeConfig" :component-size="size">
    <a-app class="antd-dashboard">
      <slot />
    </a-app>
  </a-config-provider>
</template>

<style>
/* a-app + this wrapper let antd own colors/typography inside the dashboard
   without leaking out to the rest of the deck. */
.antd-dashboard {
  height: 100%;
  width: 100%;
}
</style>
