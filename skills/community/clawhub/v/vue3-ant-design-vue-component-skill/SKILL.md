---
name: Vue3+AntDesignVue组件封装
description: 用于封装基于 Vue 3 + Ant Design Vue 的通用业务组件，提供标准化组件封装模板和最佳实践。
---

## 一、核心规范

### 1. 技术栈
- 框架：Vue 3.4+
- UI库：Ant Design Vue
- 语言：JavaScript
- 样式：Less
- 构建：Vite

### 2. 命名规范
- 文件夹：kebab-case（search-form）
- 组件名：PascalCase（SearchForm）
- Props/Events：camelCase
- 样式类：kebab-case（.search-form-container）

### 3. 文件结构

ComponentName/
├── index.vue
├── types.js（可选）
├── composables/
├── components/
└── index.js


---

## 二、基础组件模板（Card容器）

```vue
<template>
  <div class="base-card-container">
    <a-card :loading="loading">
      <template #title>
        <div class="card-header">
          <span>{{ title }}</span>
          <div class="header-actions">
            <slot name="header-actions" />
          </div>
        </div>
      </template>

      <div class="card-content">
        <slot />
      </div>

      <div v-if="showFooter" class="card-footer">
        <slot name="footer">
          <a-button @click="handleCancel">取消</a-button>
          <a-button type="primary" :loading="submitLoading" @click="handleSubmit">
            确定
          </a-button>
        </slot>
      </div>
    </a-card>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  title: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  showFooter: { type: Boolean, default: true },
  submitLoading: { type: Boolean, default: false },
  data: { type: Object, default: () => ({}) }
});

const emit = defineEmits(['update:loading', 'submit', 'cancel', 'change']);

const internalLoading = ref(false);

const actualLoading = computed({
  get: () => props.loading ?? internalLoading.value,
  set: (val) => {
    internalLoading.value = val;
    emit('update:loading', val);
  }
});

const handleSubmit = async () => {
  try {
    actualLoading.value = true;
    emit('submit', props.data);
  } finally {
    actualLoading.value = false;
  }
};

const handleCancel = () => {
  emit('cancel');
};

watch(
  () => props.data,
  (val) => emit('change', val),
  { deep: true }
);

defineExpose({
  loading: actualLoading,
  handleSubmit,
  handleCancel
});
</script>

<style lang="less" scoped>
.base-card-container {
  width: 100%;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .header-actions {
    display: flex;
    gap: 8px;
  }

  .card-footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 16px;
    border-top: 1px solid var(--ant-border-color-split);
    padding-top: 12px;
  }
}
</style>

三、表单组件（DynamicForm）

<template>
  <div class="dynamic-form-container">
    <a-form
      ref="formRef"
      :model="formData"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
    >
      <a-row :gutter="16">
        <a-col
          v-for="field in fields"
          :key="field.prop"
          :span="field.span || 24"
        >
          <a-form-item :label="field.label" :name="field.prop" :rules="field.rules">
            
            <!-- input -->
            <a-input
              v-if="field.type === 'input'"
              v-model:value="formData[field.prop]"
              :placeholder="field.placeholder"
              @change="e => handleChange(field.prop, e.target.value)"
            />

            <!-- select -->
            <a-select
              v-else-if="field.type === 'select'"
              v-model:value="formData[field.prop]"
              :options="field.options"
              @change="val => handleChange(field.prop, val)"
            />

            <!-- date -->
            <a-date-picker
              v-else-if="field.type === 'date'"
              v-model:value="formData[field.prop]"
              style="width: 100%"
              @change="val => handleChange(field.prop, val)"
            />

            <!-- slot -->
            <slot
              v-else
              :name="`field-${field.prop}`"
              :value="formData[field.prop]"
              :onChange="val => handleChange(field.prop, val)"
            />
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>

    <div v-if="showActions" class="form-actions">
      <a-button @click="handleReset">重置</a-button>
      <a-button type="primary" :loading="loading" @click="handleSubmit">
        {{ submitText }}
      </a-button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';

const props = defineProps({
  fields: { type: Array, required: true },
  modelValue: { type: Object, default: () => ({}) },
  showActions: { type: Boolean, default: true },
  submitText: { type: String, default: '提交' },
  loading: Boolean
});

const emit = defineEmits(['update:modelValue', 'submit', 'reset', 'change']);

const formRef = ref();

const formData = reactive({});

const init = () => {
  props.fields.forEach(f => {
    formData[f.prop] = props.modelValue[f.prop] ?? '';
  });
};

const handleChange = (prop, val) => {
  formData[prop] = val;
  emit('update:modelValue', { ...formData });
  emit('change', prop, val);
};

const handleSubmit = async () => {
  await formRef.value.validate();
  emit('submit', { ...formData });
};

const handleReset = () => {
  formRef.value.resetFields();
  emit('reset');
};

watch(() => props.modelValue, val => Object.assign(formData, val), { deep: true, immediate: true });

init();
</script>

<style lang="less" scoped>
.dynamic-form-container {
  .form-actions {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
  }
}
</style>

四、表格组件（DataTable）

<template>
  <div class="data-table-container">
    
    <!-- toolbar -->
    <div class="toolbar" v-if="showToolbar">
      <div><slot name="toolbar-left" /></div>
      <div>
        <slot name="toolbar-right" />
        <a-button size="small" @click="emit('refresh')">刷新</a-button>
      </div>
    </div>

    <!-- table -->
    <a-table
      :columns="innerColumns"
      :data-source="data"
      :loading="loading"
      :row-key="rowKey"
      :pagination="false"
    >
      <template
        v-for="col in columns"
        #[col.prop]="{ record, index }"
        v-if="col.slot"
      >
        <slot :name="col.prop" :row="record" :index="index" />
      </template>

      <template #operation="{ record }">
        <a-button type="link" @click="emit('edit', record)">编辑</a-button>
        <a-button type="link" danger @click="emit('delete', record)">删除</a-button>
      </template>
    </a-table>

    <!-- pagination -->
    <a-pagination
      v-if="showPagination"
      v-model:current="currentPage"
      v-model:pageSize="pageSize"
      :total="total"
      show-size-changer
      style="margin-top: 16px; text-align: right"
      @change="val => emit('current-change', val)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  data: Array,
  columns: Array,
  loading: Boolean,
  rowKey: { type: String, default: 'id' },
  showToolbar: { type: Boolean, default: true },
  showPagination: { type: Boolean, default: true },
  currentPage: Number,
  pageSize: Number,
  total: Number
});

const emit = defineEmits([
  'refresh',
  'edit',
  'delete',
  'current-change',
  'update:currentPage',
  'update:pageSize'
]);

const currentPage = computed({
  get: () => props.currentPage,
  set: val => emit('update:currentPage', val)
});

const pageSize = computed({
  get: () => props.pageSize,
  set: val => emit('update:pageSize', val)
});

const innerColumns = computed(() => {
  return [
    ...props.columns.map(col => ({
      title: col.label,
      dataIndex: col.prop,
      key: col.prop,
      customRender: col.slot ? undefined : ({ text }) => text ?? '-'
    })),
    {
      title: '操作',
      key: 'operation',
      slots: { customRender: 'operation' }
    }
  ];
});
</script>

<style lang="less" scoped>
.data-table-container {
  .toolbar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
  }
}
</style>

五、使用示例

<template>
  <DataTable
    :data="list"
    :columns="columns"
    :total="total"
    v-model:currentPage="page"
    v-model:pageSize="pageSize"
    @refresh="loadData"
  >
    <template #status="{ row }">
      <a-tag :color="row.status ? 'green' : 'red'">
        {{ row.status ? '启用' : '禁用' }}
      </a-tag>
    </template>
  </DataTable>
</template>