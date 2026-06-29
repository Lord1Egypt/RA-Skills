<!--
  DashPanel — a titled DataV border-box panel.
  Wraps any Dv border box and provides a title row + a flex body that correctly passes height down
  to the DataV chart inside (so it won't render at 0px). Auto-imported by Slidev.

  Usage:
    <DashPanel title="趋势分析" style="grid-column:8/18; grid-row:3/9">
      <DvCharts :option="trend" style="width:100%;height:100%" />
    </DashPanel>

  Props:
    title           panel title text (or use the #title slot)
    box             which border box, e.g. 'DvBorderBox13' (default) | 'DvBorderBox8' | 'dv-border-box-9'
    color           [main, secondary] colors for the border box
    backgroundColor fill behind the panel content
-->
<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  box?: string
  color?: string[]
  backgroundColor?: string
}>(), {
  box: 'DvBorderBox13',
  backgroundColor: 'transparent',
})
</script>

<template>
  <component :is="box" :color="color" :background-color="backgroundColor" class="dash-panel">
    <div class="dash-panel__inner">
      <div v-if="title || $slots.title" class="dv-panel-title">
        <slot name="title">{{ title }}</slot>
      </div>
      <div class="dash-panel__body">
        <slot />
      </div>
    </div>
  </component>
</template>

<style scoped>
.dash-panel {
  width: 100%;
  height: 100%;
}

/* DataV drops slot content into `.border-box-content`. Force it to fill the box so our flex body
   gets a real height (the #1 cause of blank DataV charts). */
.dash-panel :deep(.border-box-content) {
  position: absolute;
  inset: 0;
  display: flex;
}

.dash-panel__inner {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  height: 100%;
  padding: 12px 16px;
  box-sizing: border-box;
}

/* The chart goes here. position:relative + min-height:0 lets a 100%-height child measure correctly. */
.dash-panel__body {
  flex: 1;
  min-height: 0;
  position: relative;
}
</style>
