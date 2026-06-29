<!--
  DashGrid — a CSS grid that fills the slide (the 1920×1080 canvas). Place panels by setting
  `grid-column` / `grid-row` on each child. Auto-imported by Slidev.

  With :cols="24" :rows="12", grid lines run 1..25 (columns) and 1..13 (rows) — i.e. an end line is
  one past the last track. Example: a panel in the left third, lower two-thirds:
    <DashPanel style="grid-column: 1 / 9; grid-row: 5 / 13"> … </DashPanel>

  Props:
    cols  number of columns (default 24)
    rows  number of rows (default 12)
    gap   gutter between cells (default '14px')
-->
<script setup lang="ts">
withDefaults(defineProps<{
  cols?: number
  rows?: number
  gap?: string
}>(), {
  cols: 24,
  rows: 12,
  gap: '14px',
})
</script>

<template>
  <div
    class="dash-grid"
    :style="{
      gridTemplateColumns: `repeat(${cols}, 1fr)`,
      gridTemplateRows: `repeat(${rows}, 1fr)`,
      gap,
    }"
  >
    <slot />
  </div>
</template>

<style scoped>
.dash-grid {
  display: grid;
  width: 100%;
  height: 100%;
}
/* Prevent tall content from blowing out a track. */
.dash-grid > * {
  min-width: 0;
  min-height: 0;
}
</style>
