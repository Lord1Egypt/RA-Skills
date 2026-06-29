// Slidev app setup — runs (client-side) before the deck mounts.
// Registers the entire DataV component library globally and loads the dashboard styles.
// Docs: https://sli.dev/custom/config-vue
import { defineAppSetup } from '@slidev/types'
import DataVVue3 from '@kjgl77/datav-vue3'
import '../styles/dashboard.css'

export default defineAppSetup(({ app /*, router */ }) => {
  // After this, every DataV component is available in all slides as <DvBorderBox13>,
  // <DvScrollBoard>, <DvDigitalFlop>, <DvCharts>, … (kebab-case <dv-border-box-13> also works).
  app.use(DataVVue3)
})
