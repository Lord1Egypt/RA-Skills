<script setup lang="ts">
import { FullScreen } from '@element-plus/icons-vue'

function toggleFullscreen() {
  try {
    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      document.documentElement.requestFullscreen()
    }
  } catch {
    // 全屏 API 不可用时静默失败
  }
}
</script>

<template>
  <el-button class="fullscreen-btn" size="small" :icon="FullScreen" @click="toggleFullscreen">
    全屏
  </el-button>
</template>
