---
layout: full
---

<script setup>
import { ref, computed } from 'vue'

const status = ref(undefined)
const statusOptions = [
  { value: 'paid', label: 'Paid' },
  { value: 'pending', label: 'Pending' },
  { value: 'refunded', label: 'Refunded' },
  { value: 'failed', label: 'Failed' },
]

const selectedRowKeys = ref([])
const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys) => (selectedRowKeys.value = keys),
}))

const statusBadge = { paid: 'success', pending: 'processing', refunded: 'default', failed: 'error' }

const columns = [
  { title: 'Order', dataIndex: 'id', key: 'id' },
  { title: 'Customer', key: 'customer' },
  { title: 'Date', dataIndex: 'date', key: 'date' },
  { title: 'Amount', dataIndex: 'amount', key: 'amount', align: 'right' },
  { title: 'Status', key: 'status' },
  { title: '', key: 'action', align: 'right' },
]
const data = [
  { key: 1, id: '#ORD-1042', customer: 'Mia Wong', date: '2026-06-21', amount: '$340.00', status: 'paid' },
  { key: 2, id: '#ORD-1041', customer: 'Leo Park', date: '2026-06-21', amount: '$128.00', status: 'pending' },
  { key: 3, id: '#ORD-1040', customer: 'Ada Klein', date: '2026-06-20', amount: '$1,204.00', status: 'paid' },
  { key: 4, id: '#ORD-1039', customer: 'Tom Reyes', date: '2026-06-20', amount: '$72.50', status: 'failed' },
  { key: 5, id: '#ORD-1038', customer: 'Nina Sato', date: '2026-06-19', amount: '$560.00', status: 'refunded' },
  { key: 6, id: '#ORD-1037', customer: 'Omar Diaz', date: '2026-06-19', amount: '$96.00', status: 'paid' },
]
const initials = (name) => name.split(' ').map((w) => w[0]).join('')
</script>

<DashboardShell selected-key="orders" :crumbs="['Home', 'Orders']" title="Orders">
  <template #actions>
    <a-space>
      <a-button><export-outlined /> Export</a-button>
      <a-button type="primary"><plus-outlined /> New order</a-button>
    </a-space>
  </template>

  <a-card :bordered="false">
    <!-- filter bar -->
    <a-form layout="inline" style="margin-bottom: 16px">
      <a-form-item>
        <a-input-search placeholder="Search orders…" style="width: 220px" />
      </a-form-item>
      <a-form-item>
        <a-select v-model:value="status" :options="statusOptions" placeholder="Status"
                  allow-clear style="width: 150px" />
      </a-form-item>
      <a-form-item>
        <a-range-picker />
      </a-form-item>
      <a-form-item>
        <a-button type="primary"><filter-outlined /> Apply</a-button>
      </a-form-item>
    </a-form>

    <!-- bulk-action bar -->
    <a-alert v-if="selectedRowKeys.length" type="info" show-icon style="margin-bottom: 12px"
             :message="`${selectedRowKeys.length} selected`">
      <template #action>
        <a-space>
          <a-button size="small">Mark as paid</a-button>
          <a-button size="small" danger>Cancel</a-button>
        </a-space>
      </template>
    </a-alert>

    <a-table :columns="columns" :data-source="data" :row-selection="rowSelection"
             size="small" :pagination="{ pageSize: 6, size: 'small' }">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'id'">
          <a>{{ record.id }}</a>
        </template>
        <template v-else-if="column.key === 'customer'">
          <a-space :size="8">
            <a-avatar size="small">{{ initials(record.customer) }}</a-avatar>
            {{ record.customer }}
          </a-space>
        </template>
        <template v-else-if="column.key === 'status'">
          <a-badge :status="statusBadge[record.status]" :text="record.status" />
        </template>
        <template v-else-if="column.key === 'action'">
          <a-space :size="4">
            <a>View</a>
            <a-divider type="vertical" />
            <a>Edit</a>
            <a-divider type="vertical" />
            <a-popconfirm title="Delete this order?" ok-text="Delete" ok-type="danger">
              <a style="color: #ff4d4f">Delete</a>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>
  </a-card>
</DashboardShell>
