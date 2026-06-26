---
name: component-datatable
description: DataTable with virtual scroll, remote data, sorting, filtering, fixed columns, and row selection
---

# DataTable

## Full-Featured DataTable

```vue
<template>
  <n-data-table
    ref="tableRef"
    :columns="columns"
    :data="tableData"
    :loading="loading"
    :pagination="pagination"
    :row-key="row => row.id"
    :row-class-name="rowClassName"
    :scroll-x="1800"
    remote
    striped
    @update:page="handlePageChange"
    @update:page-size="handlePageSizeChange"
    @update:sorter="handleSorterChange"
    @update:checked-row-keys="handleCheck"
  />
</template>

<script setup lang="ts">
import type { DataTableColumns, DataTableRowKey } from 'naive-ui'
import { h } from 'vue'

interface RowType {
  id: number
  name: string
  age: number
  status: string
}

const loading = ref(false)
const tableData = ref<RowType[]>([])
const checkedRowKeys = ref<DataTableRowKey[]>([])

const columns: DataTableColumns<RowType> = [
  {
    type: 'selection',
    disabled: (row) => row.status === 'disabled'
  },
  {
    title: 'Name',
    key: 'name',
    width: 150,
    fixed: 'left',
    ellipsis: { tooltip: true },
    sorter: true
  },
  {
    title: 'Age',
    key: 'age',
    width: 100,
    sorter: true,
    filter: true,
    filterMultiple: false,
    filterOptionValue: null,
    filterOptions: [
      { label: 'Adult', value: 'adult' },
      { label: 'Minor', value: 'minor' }
    ]
  },
  {
    title: 'Status',
    key: 'status',
    render(row) {
      return h(NTag, {
        type: row.status === 'active' ? 'success' : 'error'
      }, { default: () => row.status })
    }
  },
  {
    title: 'Action',
    key: 'action',
    width: 150,
    fixed: 'right',
    render(row) {
      return h(NSpace, null, {
        default: () => [
          h(NButton, {
            size: 'small',
            onClick: () => handleEdit(row)
          }, { default: () => 'Edit' })
        ]
      })
    }
  }
]

const pagination = ref({
  page: 1,
  pageSize: 20,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
})

const handlePageChange = async (page: number) => {
  pagination.value.page = page
  await fetchData()
}

const handleSorterChange = async (sorter: any) => {
  // Handle server-side sorting
  currentSorter.value = sorter
  await fetchData()
}

const rowClassName = (row: RowType) => {
  return row.status === 'error' ? 'error-row' : ''
}
</script>
```

## Virtual Scroll

```vue
<template>
  <n-data-table
    :columns="columns"
    :data="data"
    virtual-scroll
    :scroll-x="1800"
    :max-height="500"
    row-key="id"
  />
</template>
```

## Tree DataTable

```vue
<template>
  <n-data-table
    :columns="columns"
    :data="treeData"
    default-expand-all
    :row-props="rowProps"
  />
</template>

<script setup lang="ts">
const columns = [
  { title: 'Name', key: 'name', tree: true },
  { title: 'Size', key: 'size' }
]

const treeData = [
  {
    id: 1,
    name: 'Folder',
    size: '-',
    children: [
      { id: 2, name: 'File 1', size: '10KB' },
      { id: 3, name: 'File 2', size: '20KB' }
    ]
  }
]
</script>
```

## Fixed Columns

```vue
<template>
  <n-data-table
    :columns="columns"
    :data="data"
    :scroll-x="1800"
  />
</template>

<script setup lang="ts">
const columns = [
  { title: 'Name', key: 'name', width: 150, fixed: 'left' },
  { title: 'Col 1', key: 'col1', width: 200 },
  { title: 'Col 2', key: 'col2', width: 200 },
  { title: 'Action', key: 'action', width: 150, fixed: 'right' }
]
</script>
```

## Custom Cell Rendering

```vue
<script setup lang="ts">
import { h } from 'vue'

const columns = [
  {
    title: 'Progress',
    key: 'progress',
    render(row) {
      return h(NProgress, {
        type: 'line',
        percentage: row.progress,
        showIndicator: true
      })
    }
  },
  {
    title: 'Link',
    key: 'link',
    render(row) {
      return h('a', {
        href: row.url,
        target: '_blank'
      }, row.name)
    }
  }
]
</script>
```

## Server-Side Operations

```vue
<script setup lang="ts">
const fetchData = async () => {
  loading.value = true
  const { data, total } = await api.getList({
    page: pagination.value.page,
    pageSize: pagination.value.pageSize,
    sortField: currentSorter.value?.columnKey,
    sortOrder: currentSorter.value?.order,
    filters: currentFilters.value
  })
  tableData.value = data
  pagination.value.itemCount = total
  loading.value = false
}
</script>
```

