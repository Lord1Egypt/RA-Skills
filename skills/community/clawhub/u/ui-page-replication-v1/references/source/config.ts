export const UIReplicationSkillConfig = {
  name: "ui-page-replication-v1",

  version: "1.0.0",

  // 只在命中这些场景才启用
  triggers: [
    "复刻页面",
    "页面还原",
    "UI还原",
    "后台系统复刻",
    "playwright采集页面",
    "二开页面开发",
    "100%还原页面"
  ],

  strictMode: true,

  rules: {
    noSimplify: true,
    noOmitTabs: true,
    noOmitModal: true,
    requireFullTraversal: true,
    requireMockModeling: true,
    requireApiLayer: true
  }
}