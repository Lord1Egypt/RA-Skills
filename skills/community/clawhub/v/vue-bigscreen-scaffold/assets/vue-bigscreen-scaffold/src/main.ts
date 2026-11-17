import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import App from './App.vue'
import { theme } from '@/theme'
import './styles/theme.css'

// 开启 Element Plus 暗色模式（配合大屏深色主题）
document.documentElement.classList.add('dark')

// 主题配置 → CSS 变量（theme.css 消费）
const root = document.documentElement.style
root.setProperty('--bg-start', theme.background.start)
root.setProperty('--bg-mid', theme.background.mid)
root.setProperty('--bg-end', theme.background.end)
root.setProperty('--page-bg', theme.pageBg)
root.setProperty('--panel-bg', theme.panel.bg)
root.setProperty('--panel-border', theme.panel.border)
root.setProperty('--accent', theme.accent)
root.setProperty('--text-primary', theme.text.primary)
root.setProperty('--text-secondary', theme.text.secondary)
root.setProperty('--footer', theme.footer)

const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus)
app.mount('#app')
