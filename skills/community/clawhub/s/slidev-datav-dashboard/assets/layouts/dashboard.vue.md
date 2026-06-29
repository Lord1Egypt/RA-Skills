<!--
  Slidev custom layout: `layout: dashboard`
  A full-bleed, dark, edge-to-edge canvas for 大屏 dashboards. Replaces the default theme's
  padding/light background. Drop your <DashGrid> (or absolutely-positioned panels) into the slot.
  Designed to be used with headmatter `canvasWidth: 1920` + `aspectRatio: '16/9'`.
-->
<template>
  <div class="dv-dashboard">
    <div class="dv-dashboard__bg" />
    <div class="dv-dashboard__content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
/* Fill the whole slide. `inset:0` anchors to the slide container (the nearest positioned ancestor),
   guaranteeing full bleed regardless of theme padding. */
.dv-dashboard {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: var(--dv-bg, #07142b);
  color: var(--dv-text, #c9e0ff);
  font-family: var(--dv-font-sans, ui-sans-serif, 'Source Han Sans SC', 'Microsoft YaHei', system-ui, sans-serif);
}

/* Ambient depth: brighter toward the focal center-top, fading to the dark base. */
.dv-dashboard__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(1200px 620px at 50% -8%, color-mix(in srgb, var(--dv-primary, #00baff) 16%, transparent), transparent 62%),
    radial-gradient(900px 520px at 102% 112%, color-mix(in srgb, var(--dv-secondary, #3de7c9) 10%, transparent), transparent 60%),
    linear-gradient(180deg, var(--dv-bg-2, #0b1a2c), var(--dv-bg, #07142b));
}

/* Optional faint grid texture — comment out for a cleaner base. */
.dv-dashboard__bg::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.25;
  background-image:
    linear-gradient(var(--dv-line, #16314e) 1px, transparent 1px),
    linear-gradient(90deg, var(--dv-line, #16314e) 1px, transparent 1px);
  background-size: 80px 80px;
  mask-image: radial-gradient(120% 120% at 50% 30%, #000 40%, transparent 85%);
}

.dv-dashboard__content {
  position: absolute;
  inset: 0;
  padding: 16px;
}
</style>
