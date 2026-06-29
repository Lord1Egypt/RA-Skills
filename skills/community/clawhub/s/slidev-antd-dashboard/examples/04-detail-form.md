---
layout: full
---

<script setup>
import { reactive } from 'vue'

const form = reactive({
  customer: 'mia',
  status: 'paid',
  amount: 340,
  ship: undefined,
  priority: 'Normal',
  notes: 'Gift wrap requested.',
  notify: true,
})

const customers = [
  { value: 'mia', label: 'Mia Wong' },
  { value: 'leo', label: 'Leo Park' },
  { value: 'ada', label: 'Ada Klein' },
]
const statuses = [
  { value: 'paid', label: 'Paid' },
  { value: 'pending', label: 'Pending' },
  { value: 'refunded', label: 'Refunded' },
]
</script>

<DashboardShell selected-key="orders" :crumbs="['Home', 'Orders', '#ORD-1042']" title="Order #ORD-1042">
  <template #actions>
    <a-space>
      <a-tag color="green">Paid</a-tag>
      <a-button danger>Cancel order</a-button>
      <a-button type="primary">Save changes</a-button>
    </a-space>
  </template>

  <a-steps :current="2" size="small" style="margin-bottom: 16px">
    <a-step title="Placed" />
    <a-step title="Paid" />
    <a-step title="Packed" />
    <a-step title="Shipped" />
    <a-step title="Delivered" />
  </a-steps>

  <a-row :gutter="[16, 16]">
    <!-- edit form -->
    <a-col :span="16">
      <a-card title="Edit order" :bordered="false">
        <a-form layout="vertical" :model="form">
          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item label="Customer">
                <a-select v-model:value="form.customer" :options="customers" />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item label="Status">
                <a-select v-model:value="form.status" :options="statuses" />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="Amount (USD)">
                <a-input-number v-model:value="form.amount" :min="0" style="width: 100%" />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="Ship date">
                <a-date-picker v-model:value="form.ship" style="width: 100%" />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="Priority">
                <a-segmented v-model:value="form.priority" :options="['Low', 'Normal', 'High']" block />
              </a-form-item>
            </a-col>
            <a-col :span="24">
              <a-form-item label="Notes">
                <a-textarea v-model:value="form.notes" :rows="3" />
              </a-form-item>
            </a-col>
            <a-col :span="24">
              <a-form-item label="Notify customer">
                <a-switch v-model:checked="form.notify" />
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </a-card>
    </a-col>

    <!-- summary + activity -->
    <a-col :span="8">
      <a-descriptions title="Summary" :column="1" size="small" bordered>
        <a-descriptions-item label="Order">#ORD-1042</a-descriptions-item>
        <a-descriptions-item label="Customer">Mia Wong</a-descriptions-item>
        <a-descriptions-item label="Total">$340.00</a-descriptions-item>
        <a-descriptions-item label="Payment"><a-tag color="green">Paid</a-tag></a-descriptions-item>
        <a-descriptions-item label="Created">2026-06-21</a-descriptions-item>
      </a-descriptions>

      <a-card title="Activity" :bordered="false" style="margin-top: 16px">
        <a-timeline>
          <a-timeline-item color="green">Order placed · Jun 21, 10:24</a-timeline-item>
          <a-timeline-item color="green">Payment captured · Jun 21, 10:25</a-timeline-item>
          <a-timeline-item color="blue">Packed · Jun 22, 09:10</a-timeline-item>
          <a-timeline-item>Awaiting carrier pickup</a-timeline-item>
        </a-timeline>
      </a-card>
    </a-col>
  </a-row>
</DashboardShell>
