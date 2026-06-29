<!--
  Copy to <your-slidev-project>/components/DashboardShell.vue

  The reusable admin frame: dark sider + menu, header (breadcrumb · search · bell · user),
  and a content area. It already wraps content in AntdThemeProvider (theme + dark sync),
  so a page slide is just:

    <DashboardShell selected-key="orders" :crumbs="['Home','Orders']" title="Orders">
      <template #actions><a-button type="primary"><plus-outlined/> New</a-button></template>
      ...page content (a-row/a-col, cards, table)...
    </DashboardShell>

  Props:
    selectedKey  string   key of the active menu item (drives the highlight + breadcrumb context)
    openKey      string   key of the sub-menu to expand (default 'commerce')
    crumbs       string[] breadcrumb trail, e.g. ['Home','Orders','Refunds']
    title        string   page H2
    user         string   account name in the header
    size         'small'|'middle'|'large'  component density (default 'small')
  Slots:
    default   page content
    actions   right-aligned controls next to the page title
-->
<script setup lang="ts">
import { ref, computed } from 'vue'

const props = withDefaults(
  defineProps<{
    selectedKey?: string
    openKey?: string
    crumbs?: string[]
    title?: string
    user?: string
    size?: 'small' | 'middle' | 'large'
  }>(),
  { selectedKey: 'overview', openKey: 'commerce', crumbs: () => [], title: '', user: 'Jane Doe', size: 'small' },
)

const collapsed = ref(false)
const selected = computed(() => [props.selectedKey])
const open = ref([props.openKey])
</script>

<template>
  <AntdThemeProvider :size="size">
    <a-layout style="height: 100%">
      <a-layout-sider v-model:collapsed="collapsed" collapsible :width="220" theme="dark">
        <div class="ds-logo">▦ <span v-show="!collapsed">Acme Admin</span></div>
        <a-menu :selected-keys="selected" v-model:open-keys="open" mode="inline" theme="dark">
          <a-menu-item key="overview"><dashboard-outlined /><span>Overview</span></a-menu-item>

          <a-menu-item-group key="commerce-g" title="COMMERCE">
            <a-sub-menu key="commerce">
              <template #title><shopping-cart-outlined /><span>Orders</span></template>
              <a-menu-item key="orders">All orders</a-menu-item>
              <a-menu-item key="refunds">Refunds</a-menu-item>
            </a-sub-menu>
            <a-menu-item key="customers"><team-outlined /><span>Customers</span></a-menu-item>
            <a-menu-item key="products"><appstore-outlined /><span>Products</span></a-menu-item>
          </a-menu-item-group>

          <a-menu-item-group key="insights-g" title="INSIGHTS">
            <a-menu-item key="analytics"><line-chart-outlined /><span>Analytics</span></a-menu-item>
          </a-menu-item-group>

          <a-menu-divider />
          <a-menu-item key="settings"><setting-outlined /><span>Settings</span></a-menu-item>
        </a-menu>
      </a-layout-sider>

      <a-layout>
        <a-layout-header class="ds-header">
          <a-breadcrumb>
            <a-breadcrumb-item v-for="(c, i) in crumbs" :key="i">{{ c }}</a-breadcrumb-item>
          </a-breadcrumb>
          <a-space :size="16">
            <a-input-search placeholder="Search…" style="width: 200px" />
            <a-badge :count="5" size="small"><bell-outlined style="font-size:16px" /></a-badge>
            <a-dropdown>
              <a-space :size="8" style="cursor:pointer">
                <a-avatar size="small"><template #icon><user-outlined /></template></a-avatar>
                <span>{{ user }}</span>
              </a-space>
              <template #overlay>
                <a-menu>
                  <a-menu-item key="profile">Profile</a-menu-item>
                  <a-menu-item key="acct">Settings</a-menu-item>
                  <a-menu-divider />
                  <a-menu-item key="logout">Log out</a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </a-space>
        </a-layout-header>

        <a-layout-content class="ds-content">
          <div v-if="title || $slots.actions" class="ds-titlebar">
            <h2 style="margin:0">{{ title }}</h2>
            <div><slot name="actions" /></div>
          </div>
          <slot />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </AntdThemeProvider>
</template>

<style scoped>
.ds-logo {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 20px;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
  letter-spacing: 0.3px;
}
.ds-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 20px;
  background: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.ds-content {
  padding: 20px;
  overflow: auto;
  background: #f5f6f8;
}
.ds-titlebar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
/* dark-mode header surface */
:global(.dark) .ds-header {
  background: #141414;
  border-bottom-color: rgba(255, 255, 255, 0.08);
}
:global(.dark) .ds-content {
  background: #000;
}
</style>
