<script setup lang="ts">
import { computed } from 'vue'
import { VueDigitalFlop } from 'vue3-digital-flop'
import type { KpiItem } from '@/types'

const props = defineProps<{ item: KpiItem }>()

const flopConfig = computed(() => ({
  start: 0,
  end: props.item.value,
  duration: 1500,
  separator: props.item.separator ?? ',',
  decimal: props.item.decimal ?? '.',
  prefix: '',
  suffix: props.item.suffix ?? '',
  toFixedNum: props.item.toFixedNum ?? 0,
}))
</script>

<template>
  <div class="kpi-card">
    <div class="label">{{ item.label }}</div>
    <div class="value">
      <VueDigitalFlop v-bind="flopConfig" />
    </div>
    <div class="delta">{{ item.delta }}</div>
  </div>
</template>
