import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import VueDigitalFlop from 'vue3-digital-flop'
import App from './App.vue'
import { applyTheme, DEFAULT_THEME } from '@/theme'
import './style.css'

// 应用大屏主题（CSS 变量 + ECharts 暗色主题）
applyTheme(DEFAULT_THEME)

const app = createApp(App)

app.use(createPinia())
app.use(naive)
app.use(VueDigitalFlop)

app.mount('#app')
