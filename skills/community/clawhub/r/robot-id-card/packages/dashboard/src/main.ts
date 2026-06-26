import './style.css'
import { fetchBots, fetchBot, fetchAuditLog, type BotsResponse } from './api.js'
import {
  renderBotCard,
  renderBotDetail,
  renderAuditLog,
  renderSkeleton,
  renderError,
  renderEmpty,
} from './components.js'
import type { BotSummary } from './types.js'

// ── App state ────────────────────────────────────────────────────────────────

let allBots: BotSummary[] = []
let totalBots = 0
let currentPage = 1
let totalPages = 1
let searchQuery = ''
let currentView: 'list' | 'detail' = 'list'

// ── DOM refs ─────────────────────────────────────────────────────────────────

const app = document.getElementById('app')!

// ── Render ───────────────────────────────────────────────────────────────────

function renderApp() {
  app.innerHTML = `
    <header class="site-header">
      <a href="#" class="logo" id="logo">
        <span class="logo-icon">🤖</span>
        <span>Robot ID Card</span>
      </a>
      <nav class="header-nav">
        <a href="https://github.com/Cosmofang/robot-id-card" target="_blank" rel="noopener">GitHub</a>
        <a href="https://github.com/Cosmofang/robot-id-card/blob/main/docs/spec-v1.md" target="_blank" rel="noopener">Spec</a>
      </nav>
    </header>

    <main class="main-content" id="main-content">
      ${currentView === 'list' ? renderListView() : ''}
    </main>

    <footer class="site-footer">
      <p>Robot ID Card — Universal identity standard for AI agents &amp; bots.</p>
      <p><a href="https://github.com/Cosmofang/robot-id-card" target="_blank" rel="noopener">Open source on GitHub</a></p>
    </footer>`

  bindEvents()
}

function renderListView(): string {
  const filtered = filterBots(allBots, searchQuery)
  return `
    <div class="list-view">
      <div class="hero">
        <h1>Bot Registry</h1>
        <p>Publicly registered AI agents &amp; bots with verified identities.</p>
      </div>

      <div class="controls">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            type="search"
            id="search-input"
            placeholder="Search by name, org, or purpose…"
            value="${searchQuery}"
            autocomplete="off"
          />
        </div>
        <div class="grade-filters">
          <button class="filter-btn active" data-grade="all">All</button>
          <button class="filter-btn" data-grade="healthy">✓ Healthy</button>
          <button class="filter-btn" data-grade="unknown">? Unknown</button>
          <button class="filter-btn" data-grade="dangerous">✗ Dangerous</button>
        </div>
      </div>

      <div class="stats-bar">
        <span>${totalBots} registered bots</span>
        <span>${allBots.filter(b => b.grade === 'healthy').length} healthy</span>
        <span>${allBots.filter(b => b.grade === 'dangerous').length} flagged</span>
      </div>

      <div class="bot-grid" id="bot-grid">
        ${renderGrid(filtered)}
      </div>

      ${totalPages > 1 ? `
      <div class="pagination" id="pagination">
        <button class="page-btn" id="prev-page" ${currentPage <= 1 ? 'disabled' : ''}>← Prev</button>
        <span class="page-info">Page ${currentPage} / ${totalPages}</span>
        <button class="page-btn" id="next-page" ${currentPage >= totalPages ? 'disabled' : ''}>Next →</button>
      </div>` : ''}
    </div>`
}

function renderGrid(bots: BotSummary[]): string {
  if (bots.length === 0 && searchQuery) {
    return `<div class="empty-state"><p>No bots match "<strong>${searchQuery}</strong>"</p></div>`
  }
  if (bots.length === 0) return renderEmpty()
  return bots.map(renderBotCard).join('')
}

function filterBots(bots: BotSummary[], query: string, grade?: string): BotSummary[] {
  let result = bots
  if (grade && grade !== 'all') {
    result = result.filter(b => b.grade === grade)
  }
  if (!query.trim()) return result
  const q = query.toLowerCase()
  return result.filter(b =>
    b.name.toLowerCase().includes(q) ||
    b.developer_org.toLowerCase().includes(q) ||
    b.purpose.toLowerCase().includes(q) ||
    b.id.toLowerCase().includes(q)
  )
}

// ── Events ───────────────────────────────────────────────────────────────────

let activeGrade = 'all'

function bindEvents() {
  // Logo → back to list
  document.getElementById('logo')?.addEventListener('click', (e) => {
    e.preventDefault()
    currentView = 'list'
    renderApp()
  })

  // Search
  const searchInput = document.getElementById('search-input') as HTMLInputElement | null
  searchInput?.addEventListener('input', (e) => {
    searchQuery = (e.target as HTMLInputElement).value
    const grid = document.getElementById('bot-grid')
    if (grid) grid.innerHTML = renderGrid(filterBots(allBots, searchQuery, activeGrade))
  })

  // Pagination
  document.getElementById('prev-page')?.addEventListener('click', async () => {
    if (currentPage > 1) { currentPage--; await loadPage() }
  })
  document.getElementById('next-page')?.addEventListener('click', async () => {
    if (currentPage < totalPages) { currentPage++; await loadPage() }
  })

  // Grade filters
  document.querySelectorAll<HTMLButtonElement>('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'))
      btn.classList.add('active')
      activeGrade = btn.dataset.grade ?? 'all'
      const grid = document.getElementById('bot-grid')
      if (grid) grid.innerHTML = renderGrid(filterBots(allBots, searchQuery, activeGrade))
    })
  })

  // Bot card click → detail view
  document.querySelectorAll<HTMLElement>('.bot-card:not(.skeleton)').forEach(card => {
    const openDetail = async () => {
      const id = card.dataset.id
      if (!id) return

      const main = document.getElementById('main-content')!
      main.innerHTML = `<div class="loading-detail"><div class="spinner"></div></div>`

      try {
        const bot = await fetchBot(id)
        currentView = 'detail'
        main.innerHTML = renderBotDetail(bot)
        document.getElementById('back-btn')?.addEventListener('click', () => {
          currentView = 'list'
          renderApp()
        })

        // Async load audit log after detail renders
        fetchAuditLog(id).then(log => {
          const container = document.getElementById('audit-log-container')
          if (container) container.innerHTML = renderAuditLog(log.events)
        }).catch(() => {
          const container = document.getElementById('audit-log-container')
          if (container) container.innerHTML = `<p style="color:var(--text-muted);font-size:0.875rem">Audit log unavailable.</p>`
        })
      } catch (err) {
        main.innerHTML = renderError(`Failed to load bot details: ${err instanceof Error ? err.message : 'Unknown error'}`)
        document.getElementById('retry-btn')?.addEventListener('click', () => renderApp())
      }
    }

    card.addEventListener('click', openDetail)
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDetail() }
    })
  })
}

// ── Data loading ─────────────────────────────────────────────────────────────

async function loadPage() {
  const main = document.getElementById('main-content') || document.querySelector('.main-content')!
  if (main) {
    const grid = main.querySelector('.bot-grid')
    if (grid) grid.innerHTML = renderSkeleton(6)
  }

  const data: BotsResponse = await fetchBots({ page: currentPage, limit: 50 })
  allBots = data.bots
  totalBots = data.total
  totalPages = data.pages
  renderApp()
}

// ── Bootstrap ────────────────────────────────────────────────────────────────

async function init() {
  // Render shell with skeleton
  app.innerHTML = `
    <header class="site-header">
      <a href="#" class="logo" id="logo">
        <span class="logo-icon">🤖</span>
        <span>Robot ID Card</span>
      </a>
      <nav class="header-nav">
        <a href="https://github.com/Cosmofang/robot-id-card" target="_blank" rel="noopener">GitHub</a>
        <a href="https://github.com/Cosmofang/robot-id-card/blob/main/docs/spec-v1.md" target="_blank" rel="noopener">Spec</a>
      </nav>
    </header>
    <main class="main-content">
      <div class="list-view">
        <div class="hero"><h1>Bot Registry</h1><p>Loading…</p></div>
        <div class="bot-grid">${renderSkeleton(6)}</div>
      </div>
    </main>`

  try {
    await loadPage()
  } catch {
    app.querySelector('.main-content')!.innerHTML = renderError(
      'Could not connect to the registry. Is the registry server running?'
    )
    document.getElementById('retry-btn')?.addEventListener('click', init)
  }
}

init()
