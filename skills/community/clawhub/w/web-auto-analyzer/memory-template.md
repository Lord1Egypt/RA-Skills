# Memory Template — Chrome DevTools Auto Analyzer

Use this template to track automated website analysis results over time.

## Memory Structure

```markdown
## Website Analysis History

### [Website Name/Domain]

**URL:** `https://example.com`
**First Analyzed:** YYYY-MM-DD
**Last Analyzed:** YYYY-MM-DD
**Device:** Mobile/Desktop/Both
**Analysis Tool:** Lighthouse Auto Analyzer v1.0.0

#### Audit Scores History

| Date | Device | Performance | Accessibility | Best Practices | SEO | Notes |
|------|--------|-------------|---------------|----------------|-----|-------|
| YYYY-MM-DD | Desktop | 00 | 00 | 00 | 00 | Initial audit |
| YYYY-MM-DD | Mobile | 00 | 00 | 00 | 00 | After [fix] |
| YYYY-MM-DD | Desktop | 00 | 00 | 00 | 00 | After [fix] |

#### Core Web Vitals History

| Date | Device | LCP | CLS | INP | FCP | TBT | SI |
|------|--------|-----|-----|-----|-----|-----|-----|
| YYYY-MM-DD | Desktop | 0.0s | 0.00 | 0ms | 0.0s | 0ms | 0.0s |
| YYYY-MM-DD | Mobile | 0.0s | 0.00 | 0ms | 0.0s | 0ms | 0.0s |

#### Current Status (Last Audit)

**Overall Health:**
- Performance: ⚪ Good / 🟡 Needs Improvement / 🔴 Poor
- Accessibility: ⚪ Good / 🟡 Needs Improvement / 🔴 Poor
- Best Practices: ⚪ Good / 🟡 Needs Improvement / 🔴 Poor
- SEO: ⚪ Good / 🟡 Needs Improvement / 🔴 Poor

**Core Web Vitals:**
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| LCP | 0.0s | <2.5s | ⚪/🟡/🔴 |
| CLS | 0.00 | <0.1 | ⚪/🟡/🔴 |
| INP | 0ms | <200ms | ⚪/🟡/🔴 |
| FCP | 0.0s | <1.8s | ⚪/🟡/🔴 |
| TBT | 0ms | <200ms | ⚪/🟡/🔴 |
| SI | 0.0s | <3.4s | ⚪/🟡/🔴 |

#### Critical Issues (Unresolved)

**Performance:**
- [ ] Issue description (impact: high/medium/low)
- [ ] Issue description (impact: high/medium/low)

**Accessibility:**
- [ ] Issue description (WCAG level: A/AA/AAA)
- [ ] Issue description (WCAG level: A/AA/AAA)

**Best Practices:**
- [ ] Issue description (severity: critical/high/medium/low)
- [ ] Issue description (severity: critical/high/medium/low)

**SEO:**
- [ ] Issue description (impact: high/medium/low)
- [ ] Issue description (impact: high/medium/low)

#### Fix Progress

- [x] Completed: [Description] - Date fixed
- [ ] In Progress: [Description]
- [ ] Planned: [Description]
- [ ] Blocked: [Description]

#### Report Files

| Date | Type | Path |
|------|------|------|
| YYYY-MM-DD | JSON | `./reports/url_YYYY-MM-DD.json` |
| YYYY-MM-DD | HTML | `./reports/url_YYYY-MM-DD.html` |

#### Trends

**Improving:**
- Metric 1: +X points from baseline
- Metric 2: -X ms from baseline

**Regressing:**
- Metric 3: -X points from baseline
- Metric 4: +X ms from baseline

**Stable:**
- Metric 5: No significant change
```

---

## When to Update Memory

### Create New Entry When:
- First analysis of a new website URL
- User requests historical tracking
- Comparing multiple environments (staging vs production)
- Analyzing competitor websites

### Update Existing Entry When:
- Re-running audits on tracked URLs (add new row to history tables)
- User fixes issues and wants to track improvements
- Scores change by >5 points
- New critical issues discovered
- Fix progress changes (update checklist)

### Ask User Before:
- Creating memory entries (always confirm)
- Deleting old entries
- Marking issues as resolved
- Sharing data externally

---

## Example Entry

```markdown
### Example E-commerce Site

**URL:** `https://shop.example.com`
**First Analyzed:** 2026-03-19
**Last Analyzed:** 2026-03-25
**Device:** Both
**Analysis Tool:** Lighthouse Auto Analyzer v1.0.0

#### Audit Scores History

| Date | Device | Performance | Accessibility | Best Practices | SEO | Notes |
|------|--------|-------------|---------------|----------------|-----|-------|
| 2026-03-19 | Desktop | 72 | 85 | 92 | 90 | Initial audit |
| 2026-03-19 | Mobile | 65 | 85 | 92 | 90 | Mobile typically slower |
| 2026-03-22 | Desktop | 78 | 88 | 95 | 92 | After image optimization |
| 2026-03-25 | Desktop | 85 | 92 | 95 | 95 | After accessibility fixes |

#### Core Web Vitals History

| Date | Device | LCP | CLS | INP | FCP | TBT | SI |
|------|--------|-----|-----|-----|-----|-----|-----|
| 2026-03-19 | Desktop | 3200ms | 0.15 | 220ms | 1800ms | 450ms | 4100ms |
| 2026-03-19 | Mobile | 4500ms | 0.22 | 350ms | 2400ms | 680ms | 5800ms |
| 2026-03-22 | Desktop | 2400ms | 0.08 | 180ms | 1400ms | 280ms | 3200ms |
| 2026-03-25 | Desktop | 2100ms | 0.05 | 150ms | 1200ms | 180ms | 2800ms |

#### Current Status (Last Audit: 2026-03-25)

**Overall Health:**
- Performance: ⚪ Good (85/100)
- Accessibility: ⚪ Good (92/100)
- Best Practices: ⚪ Good (95/100)
- SEO: ⚪ Good (95/100)

**Core Web Vitals:**
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| LCP | 2100ms | <2.5s | ⚪ Good |
| CLS | 0.05 | <0.1 | ⚪ Good |
| INP | 150ms | <200ms | ⚪ Good |
| FCP | 1200ms | <1.8s | ⚪ Good |
| TBT | 180ms | <200ms | ⚪ Good |
| SI | 2800ms | <3.4s | ⚪ Good |

#### Critical Issues (Unresolved)

**Performance:**
- [ ] Third-party analytics script adds 80ms TBT (impact: low)

**Accessibility:**
- [ ] Skip link not visible on focus (WCAG AA) (impact: medium)

**Best Practices:**
- [x] Resolved: jQuery updated to 3.7.1

**SEO:**
- [x] Resolved: Meta description extended to 155 characters

#### Fix Progress

- [x] Completed: Added explicit width/height to product images - 2026-03-20
- [x] Completed: Implemented lazy loading for below-fold images - 2026-03-21
- [x] Completed: Updated jQuery to 3.7.1 - 2026-03-22
- [x] Completed: Fixed color contrast on CTA buttons - 2026-03-24
- [x] Completed: Added alt text to all product images - 2026-03-24
- [ ] In Progress: Implement skip link functionality
- [ ] Planned: Defer non-critical third-party scripts
- [ ] Planned: Implement service worker for caching

#### Report Files

| Date | Type | Path |
|------|------|------|
| 2026-03-19 | JSON | `./reports/shop-example-com_2026-03-19.json` |
| 2026-03-19 | HTML | `./reports/shop-example-com_2026-03-19.html` |
| 2026-03-22 | JSON | `./reports/shop-example-com_2026-03-22.json` |
| 2026-03-25 | JSON | `./reports/shop-example-com_2026-03-25.json` |
| 2026-03-25 | HTML | `./reports/shop-example-com_2026-03-25.html` |

#### Trends

**Improving:**
- Performance: +13 points from baseline (72 → 85)
- LCP: -1100ms from baseline (3200ms → 2100ms)
- CLS: -0.10 from baseline (0.15 → 0.05)
- Accessibility: +7 points from baseline (85 → 92)

**Regressing:**
- None

**Stable:**
- SEO: Consistent 90-95 range
- Best Practices: Consistent 92-95 range
```

---

## Comparison Template

When comparing multiple URLs or environments:

```markdown
### Comparison: Production vs Staging

| Metric | Production | Staging | Difference | Target |
|--------|------------|---------|------------|--------|
| Performance | 00 | 00 | +/-0 | >80 |
| Accessibility | 00 | 00 | +/-0 | >90 |
| Best Practices | 00 | 00 | +/-0 | >90 |
| SEO | 00 | 00 | +/-0 | >90 |
| LCP | 0.0s | 0.0s | +/-0.0s | <2.5s |
| CLS | 0.00 | 0.00 | +/-0.00 | <0.1 |
| INP | 0ms | 0ms | +/-0ms | <200ms |

**Analysis:**
- Staging performs [better/worse] than production
- Key differences: [Summary]
- Recommendation: [Action items]
```

---

## Competitor Analysis Template

```markdown
### Competitor Analysis - E-commerce Sites

| Site | Performance | Accessibility | Best Practices | SEO | LCP | CLS | Notes |
|------|-------------|---------------|----------------|-----|-----|-----|-------|
| shop.example.com | 85 | 92 | 95 | 95 | 2.1s | 0.05 | Our site |
| competitor-a.com | 78 | 88 | 90 | 92 | 2.8s | 0.12 | Larger images |
| competitor-b.com | 92 | 95 | 98 | 98 | 1.5s | 0.02 | Industry leader |
| competitor-c.com | 65 | 75 | 85 | 88 | 3.5s | 0.18 | Poor optimization |

**Industry Benchmarks:**
- Average Performance: 78
- Average LCP: 2.6s
- Average CLS: 0.10

**Our Position:**
- Performance: Above average (+7)
- LCP: Better than average (-0.5s)
- CLS: Better than average (-0.05)
```

---

## Status Indicators

Use consistently across all entries:

| Symbol | Meaning |
|--------|---------|
| ⚪ | Good (meets target) |
| 🟡 | Needs Improvement (close to target) |
| 🔴 | Poor (far from target) |
| ⬆️ | Improved from previous |
| ⬇️ | Regressed from previous |
| ➡️ | No significant change |
| ✅ | Issue resolved |
| [ ] | Issue pending |
| [~] | Issue in progress |
| [!] | Issue blocked |

---

## Automated Update Script

Use this script to append results to memory:

```javascript
function appendToMemory(url, results, memoryPath) {
  const date = new Date().toISOString().split('T')[0];
  const scores = results.scores;
  const metrics = results.performanceMetrics;
  
  const entry = `
| ${date} | ${results.device} | ${scores.Performance} | ${scores.Accessibility} | ${scores['Best Practices']} | ${scores.SEo} | ${metrics.LCP}ms | ${metrics.CLS} | ${metrics.INP}ms |
`;
  
  // Append to markdown table in memory file
  // Implementation depends on your memory system
}
```
