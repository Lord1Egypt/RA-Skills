// nuxt.config.ts — copy this, then delete every block whose module wasn't
// selected in SKILL.md §1/§3. Comments mark which blocks are conditional.
// https://nuxt.com/docs/api/configuration/nuxt-config

// --- Only if i18n is in scope ---
const LOCALES = [
  { code: 'en', language: 'en-US', name: 'English', file: 'en.json' }
  // { code: 'es', language: 'es-ES', name: 'Español', file: 'es.json' },
]
const DEFAULT_LOCALE = 'en'

export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/image',              // if images in scope
    '@nuxt/ui',                 // UI kit option A — swap for '@antdv-next/nuxt' if Antdv Next was chosen instead (see SKILL.md §4); never both
    '@nuxtjs/seo',
    '@nuxt/content',            // if content in scope
    '@vueuse/nuxt',
    'motion-v/nuxt',            // if animation in scope
    '@nuxtjs/i18n',             // if i18n in scope
    'nuxt-llms',                // if AI-agent discoverability in scope
    'nuxt-ai-ready',            // if AI-agent discoverability in scope
    'nuxt-gtag',                // if analytics in scope
    '@nuxt/scripts',            // if ads/third-party scripts in scope
    'nuxt-simple-cookie-consent', // if consent management in scope
    '@nuxthub/core',            // always, for Cloudflare D1/KV/Blob bindings + local dev — NOT the deploy mechanism
    '@stefanobartoletti/nuxt-social-share' // if social share in scope
  ],

  devtools: { enabled: true },

  // Nuxt UI: main.css does the `@import "tailwindcss"; @import "@nuxt/ui";` (see SKILL.md §4).
  // Antdv Next: swap this for css: ['antdv-next/dist/reset.css', 'antdv-next/dist/antd.css']
  // instead — no main.css/Tailwind import needed for that kit.
  css: ['~/assets/css/main.css'],

  // --- Only if Antdv Next was chosen as the UI kit (see SKILL.md §4 Option B) ---
  // antd: { icon: true },

  // Real domain — drives sitemap, OG image, schema.org, canonical URLs.
  site: {
    url: 'https://<app-domain>',
    name: '<App Name>'
  },

  routeRules: {
    // Only add CORS-open blocks for routes deliberately meant as a public API.
    // Everything else stays same-origin by default — don't open CORS globally.
    // '/api/tools/**': {
    //   cors: false,
    //   headers: {
    //     'Access-Control-Allow-Origin': '*',
    //     'Access-Control-Allow-Methods': 'GET, OPTIONS',
    //     'Access-Control-Allow-Headers': '*'
    //   }
    // }
  },

  sourcemap: {
    client: false,
    server: false
  },

  compatibilityDate: '<today-YYYY-MM-DD>',

  nitro: {
    preset: 'cloudflare_module', // required so `nuxt build` emits Cloudflare Workers output for `wrangler deploy`
    prerender: {
      routes: ['/'],
      crawlLinks: true
    }
  },

  // --- Only if a database is in scope ---
  // NuxtHub binding config only — resolves the `hub:db` import to D1 locally
  // (via Miniflare) and in production. Has no effect on how the app is
  // deployed. This minimal shape assumes a hand-maintained wrangler.jsonc
  // (see wrangler.example.jsonc); NuxtHub also accepts a fuller
  // `db: { dialect, driver: 'd1', connection: { databaseId } }` shape that
  // lets it auto-generate wrangler.json instead — see nuxthub-deployment.md.
  hub: {
    db: {
      dialect: 'sqlite',
      applyMigrationsDuringBuild: false // migrations run as an explicit step, not every build
    }
  },

  // --- Only if i18n is in scope ---
  i18n: {
    strategy: 'prefix_except_default',
    defaultLocale: DEFAULT_LOCALE,
    locales: LOCALES,
    langDir: 'locales',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    }
  },

  // --- Only if nuxt-llms is in scope ---
  llms: {
    domain: 'https://<app-domain>',
    title: '<App Name>',
    description: '<one-line description>',
    contentRawMarkdown: false,
    sections: []
  },

  ogImage: {
    zeroRuntime: true
  },

  sitemap: {
    zeroRuntime: true
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }

  // --- Only if analytics/ads are in scope ---
  // Every ID below is a placeholder — always the new app's own account IDs,
  // never carried over from another project.
  // gtag: {
  //   id: '<GA-MEASUREMENT-ID>',
  //   loadingStrategy: 'async',
  //   config: { anonymize_ip: true }
  // },
  // scripts: {
  //   registry: {
  //     googleAdsense: { client: '<ADSENSE-CLIENT-ID>', autoAds: true }
  //   }
  // },
  // cookieConsent: {
  //   expiresInDays: 180,
  //   consentVersion: '1.0.0',
  //   cookieName: 'cookie_consent',
  //   categories: {
  //     analytics: { label: 'Analytics', description: 'Used to improve site performance.', required: false },
  //     ads: { label: 'Advertisement', description: 'Used for ad personalization.' }
  //   }
  // },
  // app: {
  //   head: {
  //     meta: [{ name: 'google-adsense-account', content: '<ADSENSE-CLIENT-ID>' }]
  //   }
  // }
})
