import { onMounted, onUnmounted, ref } from 'vue'

/**
 * 大屏等比缩放适配。
 * 以设计稿基准尺寸（默认 1920x1080）为画布，按窗口实际尺寸取最小缩放比，
 * 保证内容不变形并居中铺满。配合 App.vue 中固定 1920x1080 的 .screen-wrapper 使用。
 */
export function useScreenScale(baseWidth = 1920, baseHeight = 1080) {
  const scale = ref(1)
  const offsetX = ref(0)
  const offsetY = ref(0)

  function calc() {
    const sw = window.innerWidth
    const sh = window.innerHeight
    const s = Math.min(sw / baseWidth, sh / baseHeight)
    scale.value = s
    // 居中偏移
    offsetX.value = (sw - baseWidth * s) / 2
    offsetY.value = (sh - baseHeight * s) / 2
  }

  let raf = 0
  function onResize() {
    cancelAnimationFrame(raf)
    raf = requestAnimationFrame(calc)
  }

  onMounted(() => {
    calc()
    window.addEventListener('resize', onResize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', onResize)
    cancelAnimationFrame(raf)
  })

  return { scale, offsetX, offsetY }
}
