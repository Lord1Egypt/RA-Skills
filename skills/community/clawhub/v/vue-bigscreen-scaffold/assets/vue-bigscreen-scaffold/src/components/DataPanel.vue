<script setup lang="ts">
import { ref } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const updatedAt = ref(new Date().toLocaleString('zh-CN', { hour12: false }))

function refresh() {
  updatedAt.value = new Date().toLocaleString('zh-CN', { hour12: false })
  void store.loadAll()
}
</script>

<template>
  <div class="panel data-panel">
    <div class="pt">数据面板</div>
    <div class="data-body">
      <div class="info">
        <p>示例数据（演示用）</p>
        <p>初始化 JSON：public/data/</p>
        <p>更新时间：{{ updatedAt }}</p>
      </div>
      <el-button size="small" type="primary" round :icon="Refresh" @click="refresh">
        刷新数据
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.data-panel {
  display: flex;
  flex-direction: column;
}

.data-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
  padding: 0 4px;
}

.info p {
  font-size: 12px;
  line-height: 1.9;
  color: var(--text-secondary);
}
</style>
