import { chromium } from 'playwright-extra'
import StealthPlugin from 'puppeteer-extra-plugin-stealth'

let stealthRegistered = false

function ensureStealth() {
  if (stealthRegistered) return
  chromium.use(StealthPlugin())
  stealthRegistered = true
}

function resolveHeadless(headless) {
  if (typeof headless === 'boolean') return headless
  if (process.env.HEADLESS === 'false') return false
  return true
}

function resolveProxy(proxy) {
  if (proxy) {
    if (typeof proxy === 'string') {
      return {
        server: proxy,
        username: process.env.PROXY_USERNAME || undefined,
        password: process.env.PROXY_PASSWORD || undefined,
      }
    }
    return proxy
  }

  if (!process.env.PROXY_SERVER) return undefined

  return {
    server: process.env.PROXY_SERVER,
    username: process.env.PROXY_USERNAME || undefined,
    password: process.env.PROXY_PASSWORD || undefined,
  }
}

/**
 * Lança Chromium com playwright-extra + StealthPlugin.
 *
 * @param {object} [options]
 * @param {boolean} [options.headless]
 * @param {number} [options.slowMo]
 * @param {string | { server: string, username?: string, password?: string }} [options.proxy]
 * @param {string} [options.userAgent]
 * @param {{ width: number, height: number }} [options.viewport]
 * @param {string} [options.locale]
 * @param {string[]} [options.args]
 * @returns {Promise<{ browser: import('playwright').Browser, context: import('playwright').BrowserContext, page: import('playwright').Page }>}
 */
export async function launchStealthBrowser(options = {}) {
  ensureStealth()

  const {
    headless,
    slowMo,
    proxy,
    userAgent,
    viewport,
    locale,
    args,
    ...rest
  } = options

  const launchOptions = {
    headless: resolveHeadless(headless),
    ...rest,
  }

  if (slowMo != null) launchOptions.slowMo = slowMo
  if (args) launchOptions.args = args

  // Playwright 1.49+ usa chrome-headless-shell no headless, que o Stealth não cobre bem.
  // channel: 'chromium' força o Chrome for Testing completo (igual ao tutorial).
  if (launchOptions.headless && !launchOptions.channel && !launchOptions.executablePath) {
    launchOptions.channel = 'chromium'
  }

  const resolvedProxy = resolveProxy(proxy)
  if (resolvedProxy?.server) {
    launchOptions.proxy = {
      server: resolvedProxy.server,
      ...(resolvedProxy.username ? { username: resolvedProxy.username } : {}),
      ...(resolvedProxy.password ? { password: resolvedProxy.password } : {}),
    }
  }

  const browser = await chromium.launch(launchOptions)

  const contextOptions = {}
  if (userAgent) contextOptions.userAgent = userAgent
  if (viewport) contextOptions.viewport = viewport
  if (locale) contextOptions.locale = locale

  const context = await browser.newContext(contextOptions)
  const page = await context.newPage()

  return { browser, context, page }
}
