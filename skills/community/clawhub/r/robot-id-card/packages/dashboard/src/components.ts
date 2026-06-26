import type { BotSummary, BotDetail, Grade } from './types.js'
import type { AuditEvent } from './api.js'

const GRADE_CONFIG: Record<Grade, { label: string; color: string; icon: string }> = {
  healthy:   { label: 'Healthy',   color: '#22c55e', icon: '✓' },
  unknown:   { label: 'Unknown',   color: '#f59e0b', icon: '?' },
  dangerous: { label: 'Dangerous', color: '#ef4444', icon: '✗' },
}

const CAP_LABELS: Record<string, string> = {
  read_articles: 'Read Articles',
  read_images:   'Read Images',
  follow_links:  'Follow Links',
  view_threads:  'View Threads',
  react:         'React / Like',
  post_content:  'Post Content',
  direct_chat:   'Direct Chat',
}

export function gradeBadge(grade: Grade): string {
  const cfg = GRADE_CONFIG[grade]
  return `<span class="grade-badge grade-${grade}">
    <span class="grade-icon">${cfg.icon}</span>
    ${cfg.label}
  </span>`
}

export function capabilityTag(cap: string): string {
  return `<span class="cap-tag">${CAP_LABELS[cap] ?? cap}</span>`
}

export function relativeTime(isoDate: string): string {
  const diff = Date.now() - new Date(isoDate).getTime()
  const days = Math.floor(diff / 86_400_000)
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 30) return `${days} days ago`
  const months = Math.floor(days / 30)
  return months === 1 ? '1 month ago' : `${months} months ago`
}

export function renderBotCard(bot: BotSummary): string {
  return `
    <article class="bot-card" data-id="${bot.id}" role="button" tabindex="0">
      <div class="bot-card-header">
        <div class="bot-avatar">${bot.name.charAt(0).toUpperCase()}</div>
        <div class="bot-card-title">
          <h3>${escapeHtml(bot.name)}</h3>
          <span class="bot-org">${escapeHtml(bot.developer_org)}</span>
        </div>
        ${gradeBadge(bot.grade)}
      </div>
      <p class="bot-purpose">${escapeHtml(truncate(bot.purpose, 120))}</p>
      <div class="bot-card-footer">
        <code class="ric-id">${bot.id}</code>
        <span class="bot-age">${relativeTime(bot.created_at)}</span>
      </div>
    </article>`
}

export function renderBotDetail(bot: BotDetail): string {
  const caps = bot.bot.capabilities.map(capabilityTag).join('')
  return `
    <div class="detail-panel">
      <button class="back-btn" id="back-btn">← Back to registry</button>

      <div class="detail-header">
        <div class="detail-avatar">${bot.bot.name.charAt(0).toUpperCase()}</div>
        <div>
          <h2>${escapeHtml(bot.bot.name)}</h2>
          <span class="detail-version">v${escapeHtml(bot.bot.version)}</span>
          ${gradeBadge(bot.grade)}
        </div>
      </div>

      <section class="detail-section">
        <h4>Purpose</h4>
        <p>${escapeHtml(bot.bot.purpose)}</p>
      </section>

      <section class="detail-section">
        <h4>Capabilities</h4>
        <div class="cap-tags">${caps}</div>
      </section>

      <section class="detail-section">
        <h4>Developer</h4>
        <dl class="detail-dl">
          <dt>Name</dt><dd>${escapeHtml(bot.developer.name)}</dd>
          ${bot.developer.org ? `<dt>Org</dt><dd>${escapeHtml(bot.developer.org)}</dd>` : ''}
          ${bot.developer.website ? `<dt>Website</dt><dd><a href="${escapeHtml(bot.developer.website)}" target="_blank" rel="noopener">${escapeHtml(bot.developer.website)}</a></dd>` : ''}
          <dt>Verified</dt><dd>${bot.developer.verified ? '✓ Yes' : '✗ No'}</dd>
        </dl>
      </section>

      <section class="detail-section">
        <h4>Identity</h4>
        <dl class="detail-dl">
          <dt>RIC ID</dt><dd><code>${bot.id}</code></dd>
          <dt>Public Key</dt><dd><code class="pubkey">${bot.public_key}</code></dd>
          <dt>Registered</dt><dd>${new Date(bot.created_at).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })}</dd>
          <dt>Grade Updated</dt><dd>${relativeTime(bot.grade_updated_at)}</dd>
        </dl>
      </section>

      <section class="detail-section">
        <h4>User Agent</h4>
        <code class="user-agent">${escapeHtml(bot.bot.user_agent)}</code>
      </section>

      <section class="detail-section">
        <h4>Audit Log</h4>
        <div id="audit-log-container">
          <div class="audit-loading">
            <div class="spinner" style="width:20px;height:20px;border-width:2px"></div>
          </div>
        </div>
      </section>
    </div>`
}

const EVENT_LABELS: Record<string, { icon: string; label: string; color: string }> = {
  registered:       { icon: '🆕', label: 'Registered',       color: '#6366f1' },
  grade_changed:    { icon: '⚡', label: 'Grade Changed',     color: '#f59e0b' },
  violation_report: { icon: '🚨', label: 'Violation Report',  color: '#ef4444' },
}

export function renderAuditLog(events: AuditEvent[]): string {
  if (events.length === 0) {
    return `<p style="color:var(--text-muted);font-size:0.875rem">No audit events recorded.</p>`
  }
  return `<ol class="audit-list">
    ${events.map(e => {
      const cfg = EVENT_LABELS[e.event] ?? { icon: '📋', label: e.event, color: '#64748b' }
      const gradeChange = e.old_grade && e.new_grade
        ? ` <span style="color:var(--text-muted)">${e.old_grade} → ${e.new_grade}</span>` : ''
      return `<li class="audit-item">
        <span class="audit-icon">${cfg.icon}</span>
        <div class="audit-body">
          <div class="audit-title" style="color:${cfg.color}">${cfg.label}${gradeChange}</div>
          ${e.reason ? `<div class="audit-reason">${escapeHtml(e.reason)}</div>` : ''}
          ${e.reporter ? `<div class="audit-meta">Reported by: ${escapeHtml(e.reporter)}</div>` : ''}
          <div class="audit-meta">${new Date(e.timestamp).toLocaleString()}</div>
        </div>
      </li>`
    }).join('')}
  </ol>`
}

export function renderSkeleton(count = 6): string {
  return Array(count).fill(0).map(() => `
    <div class="bot-card skeleton">
      <div class="skeleton-line w-60"></div>
      <div class="skeleton-line w-100 mt8"></div>
      <div class="skeleton-line w-80 mt4"></div>
      <div class="skeleton-line w-40 mt8"></div>
    </div>`).join('')
}

export function renderError(message: string): string {
  return `<div class="error-state">
    <div class="error-icon">⚠</div>
    <p>${escapeHtml(message)}</p>
    <button class="retry-btn" id="retry-btn">Retry</button>
  </div>`
}

export function renderEmpty(): string {
  return `<div class="empty-state">
    <div class="empty-icon">🤖</div>
    <p>No bots registered yet.</p>
    <p>Be the first — <code>ric register</code></p>
  </div>`
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function truncate(s: string, max: number): string {
  return s.length <= max ? s : s.slice(0, max) + '…'
}
