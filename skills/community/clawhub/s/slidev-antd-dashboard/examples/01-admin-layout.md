---
layout: full
---

<DashboardShell selected-key="overview" :crumbs="['Home', 'Overview']" title="Overview">
  <template #actions>
    <a-space>
      <a-button><reload-outlined /> Refresh</a-button>
      <a-button type="primary"><plus-outlined /> New report</a-button>
    </a-space>
  </template>

  <a-alert
    banner
    type="info"
    show-icon
    message="Welcome back, Jane — 3 orders need review today."
    style="margin-bottom: 16px"
  />

  <a-row :gutter="[16, 16]">
    <a-col :span="12">
      <a-card title="Getting started" :bordered="false">
        <a-steps :current="1" size="small" direction="vertical">
          <a-step title="Connect a data source" description="Connected to Postgres" />
          <a-step title="Invite your team" description="In progress" />
          <a-step title="Publish your first dashboard" />
        </a-steps>
      </a-card>
    </a-col>
    <a-col :span="12">
      <a-card title="System status" :bordered="false">
        <a-space direction="vertical" :size="12" style="width: 100%">
          <a-badge status="success" text="API — operational" />
          <a-badge status="success" text="Billing — operational" />
          <a-badge status="warning" text="Email delivery — degraded" />
          <a-badge status="processing" text="Nightly sync — running" />
        </a-space>
      </a-card>
    </a-col>
  </a-row>
</DashboardShell>
