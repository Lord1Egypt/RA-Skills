'use strict'

const { normalizeBase, VibbitError } = require('./client')

const profiles = {
  cn: { region: 'cn', apiBase: 'https://openapi.vibbit.cn/openapi/v1', webBase: 'https://app.vibbit.cn' },
  global: { region: 'global', apiBase: 'https://openapi.vibbit.ai/openapi/v1', webBase: 'https://app.vibbit.ai' },
}
const texts = {
  en: {
    title: 'Set up your Vibbit API key',
    intro: 'Set it up once, then return to your conversation and keep creating.',
    site: 'Your Vibbit site', china: 'China site', international: 'International site',
    separate: 'Each site has its own account, API keys, credits, products and assets. Choose the site you normally use.',
    step1: 'Create a key', create: 'Open Vibbit API Keys', step2: 'Paste and verify', label: 'API key',
    placeholder: 'Paste your key here',
    privacy: 'Your key is verified only with the selected Vibbit site. It stays out of the conversation.',
    storageTitle: 'How is my key stored?',
    storage: 'Stored in a private file for this OS user on this computer. The file is not encrypted. On shared devices, use the host credential manager.',
    submit: 'Verify and save', pending: 'Verifying…',
    success: 'Setup complete. Switch back to your chat window to continue your task.',
    cancel: 'Cancel', cancelled: 'Cancelled. Your previous configuration is unchanged.',
    expired: 'This page has expired. Return to your conversation to open a new setup page.',
    authentication: 'The key was not accepted. Check the complete key and selected Vibbit site.',
    forbidden: 'Access was denied. Check the IP allowlist and account permissions.',
    transport: 'Cannot reach the service. Check your connection and retry. Your previous configuration is unchanged.',
    saveFailed: 'Cannot save to the private user directory. Use your host credential settings.',
    invalid: 'Enter a valid API key and select a Vibbit site.',
  },
  'zh-CN': {
    title: '配置 Vibbit API Key', intro: '只需配置一次，验证成功后回到对话继续创作。',
    site: '你的 Vibbit 站点', china: '中国站', international: '国际站',
    separate: '两站的账号、API Key、积分、商品和素材相互独立，请选择你平时使用的站点。',
    step1: '创建密钥', create: '打开 Vibbit 密钥页面', step2: '粘贴并验证', label: 'API Key',
    placeholder: '在这里粘贴密钥', privacy: '密钥仅向所选 Vibbit 站点验证，不会出现在对话中。',
    storageTitle: '密钥如何保存？',
    storage: '保存于当前电脑的用户私有文件，仅当前系统用户可读写；文件不加密。公用设备请使用宿主凭证管理。',
    submit: '验证并保存', pending: '正在验证…', success: '配置成功。请切回刚才的对话窗口，继续任务。',
    cancel: '取消', cancelled: '已取消。原来的配置保持不变。',
    expired: '页面已失效。请回到对话重新打开配置入口。',
    authentication: '密钥未通过验证，请检查复制是否完整，以及所选站点是否正确。',
    forbidden: '访问被拒绝，请检查 IP 白名单和账号权限。',
    transport: '暂时无法连接服务。请检查网络后重试，原来的配置保持不变。',
    saveFailed: '无法保存到用户私有目录。请改用宿主的凭证设置。', invalid: '请输入有效的密钥并选择 Vibbit 站点。',
  },
}

function getProfile(region = 'global') {
  if (!Object.hasOwn(profiles, region)) throw new VibbitError('configuration', 'Choose a Vibbit region: cn or global')
  return profiles[region]
}
function profileForBase(base) {
  return Object.values(profiles).find(profile => profile.apiBase === normalizeBase(base))
}
function regionFromSite(site) {
  if (!site) return undefined
  let url
  try { url = new URL(site) } catch { throw new VibbitError('configuration', 'Use an official Vibbit site URL: https://app.vibbit.cn or https://app.vibbit.ai') }
  const profile = Object.values(profiles).find(item => item.webBase === url.origin)
  if (!profile || url.username || url.password) throw new VibbitError('configuration', 'Use an official Vibbit site URL: https://app.vibbit.cn or https://app.vibbit.ai')
  return profile.region
}
function pageProfile(region, lang = 'en') {
  lang = /^zh(?:-|$)/i.test(lang) ? 'zh-CN' : 'en'
  return { ...getProfile(region), lang, text: texts[lang] }
}

module.exports = { ...profiles.global, profiles, getProfile, profileForBase, regionFromSite, pageProfile }
