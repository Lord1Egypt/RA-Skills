# Shared Component CSS

CSS fragment from the standard shell. Paste inside the shell `<style>` block after the selected theme CSS.

        /* Shared Component CSS — fixed verbatim; do NOT regenerate or summarize */
        *, *::before, *::after { box-sizing: border-box; }
        .report-wrapper { max-width: 920px; margin: 0 auto; padding: 2rem 1.5rem; }
        @media (min-width: 1100px) { .report-wrapper { padding: 2.5rem 3rem; } }
        .report-meta { color: var(--text-muted); font-size: .9rem; margin-top: -.5rem; margin-bottom: 1.5rem; }

        /* Watermark footer */
        .report-footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--report-border, var(--border)); text-align: center; color: var(--text-muted); font-size: .7rem; opacity: .5; letter-spacing: .03em; }
        @media print { .report-footer { display: none; } }
        @media (max-width: 768px) { .report-footer { margin-top: 1.5rem; } }

        /* KPI */
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .75rem; margin: 1.1rem 0; }
        .kpi-card { background: var(--report-surface, var(--surface)); border: 1px solid var(--report-border, var(--border)); border-radius: var(--radius); padding: .9rem; text-align: center; border-top: 2px solid var(--report-structure, var(--primary)); display: flex; flex-direction: column; align-items: center; }
        .kpi-label { font-size: .78rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: .05em; margin-bottom: .4rem; }
        .kpi-value { font-size: 2rem; font-weight: 800; color: var(--report-text, var(--text)); line-height: 1.2; font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; font-variant-numeric: lining-nums tabular-nums; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; word-break: break-word; overflow-wrap: break-word; }
        .kpi-value .kpi-suffix { font-size: .75em; font-weight: 600; line-height: 1.3; }
        .kpi-trend { font-size: .85rem; margin-top: .3rem; }
        .kpi-trend--up { color: var(--success); } .kpi-trend--down { color: var(--danger); } .kpi-trend--neutral { color: var(--text-muted); }
        .kpi-card[data-accent] { border-top-color: var(--report-structure, var(--primary)); }
        .kpi-card[data-accent] .kpi-value { color: var(--report-text, var(--text)); }
        .kpi-delta { display: inline-block; padding: .15rem .48rem; border-radius: 999px; font-size: .74rem; font-weight: 700; margin-top: .28rem; }
        .kpi-delta--up   { background: var(--report-delta-up-bg, #E7F1EA); color: var(--report-delta-up-text, var(--success)); }
        .kpi-delta--down { background: var(--report-delta-down-bg, #F6E8E6); color: var(--report-delta-down-text, var(--danger)); }
        .kpi-delta--info { background: var(--report-delta-flat-bg, #EEE7DE); color: var(--report-delta-flat-text, var(--text-muted)); }
        .badge { display: inline-flex; align-items: center; padding: .18rem .55rem; border-radius: 999px; font-size: .75rem; font-weight: 600; letter-spacing: .01em; white-space: nowrap; border: 1px solid var(--report-chip-border, var(--report-border, var(--border))); }
        .badge--blue   { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--green  { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--purple { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--orange { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--red    { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--gray   { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--teal   { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--done   { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--wip    { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--todo   { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--ok     { background: var(--report-chip-bg, var(--surface)); color: var(--report-chip-text, var(--text-muted)); }
        .badge--warn   { background: var(--report-delta-up-bg, #E7F1EA); color: var(--report-delta-up-text, var(--success)); border-color: transparent; }
        .badge--err    { background: var(--report-delta-down-bg, #F6E8E6); color: var(--report-delta-down-text, var(--danger)); border-color: transparent; }
        [data-report-mode="comparison"] .badge--entity-a { background: rgba(47, 107, 80, .12); color: var(--entity-a, #2F6B50); border-color: rgba(47, 107, 80, .18); }
        [data-report-mode="comparison"] .badge--entity-b { background: rgba(111, 106, 124, .12); color: var(--entity-b, #6F6A7C); border-color: rgba(111, 106, 124, .18); }
        [data-report-mode="comparison"] .badge--entity-c { background: rgba(92, 118, 138, .12); color: var(--entity-c, #5C768A); border-color: rgba(92, 118, 138, .18); }

        /* Tables */
        .table-wrapper { overflow-x: auto; margin: 1.1rem 0; }
        .report-table { width: 100%; border-collapse: collapse; font-size: .9rem; }
        .report-table th { background: var(--report-surface, var(--surface)); border-bottom: 2px solid var(--report-structure, var(--primary)); padding: .7rem 1rem; text-align: left; font-weight: 600; }
        .report-table td { padding: .6rem 1rem; border-bottom: 1px solid var(--border); }
        .report-table tr:hover td { background: var(--report-surface, var(--surface)); }

        /* Callout */
        .callout { display: flex; gap: .75rem; padding: .9rem 1.1rem; border-radius: var(--radius); margin: .75rem 0; border-left: 4px solid; align-items: flex-start; }
        .callout--note { background: #EFF6FF; border-color: #3B82F6; }
        .callout--tip { background: #F0FDF4; border-color: #22C55E; }
        .callout--warning { background: #FFFBEB; border-color: #F59E0B; }
        .callout--danger { background: #FEF2F2; border-color: #EF4444; }
        .callout-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: .05rem; }
        .callout-body { flex: 1; min-width: 0; line-height: 1.6; font-size: .93rem; color: #1F2937; }
        /* Callout icon color — ensure contrast on light backgrounds regardless of theme */
        .callout--note .callout-icon { color: #3B82F6; }
        .callout--tip .callout-icon { color: #22C55E; }
        .callout--warning .callout-icon { color: #F59E0B; }
        .callout--danger .callout-icon { color: #EF4444; }

        /* Semantic highlight extraction — from design-quality.md §6 */
        .highlight-sentence { font-size: 1.15rem; font-weight: 700; color: var(--primary); border-left: 3px solid var(--primary); padding-left: 1rem; margin: 1.5rem 0; line-height: 1.5; }
        .lead-block {
          margin: 1.1rem 0 1rem;
          padding: 1rem 1.15rem;
          border-left: 4px solid var(--primary);
          border-radius: 16px;
          background: rgba(255,255,255,.72);
          font-size: 1.02rem;
          line-height: 1.72;
          max-width: 60rem;
        }
        .section-quote {
          margin: 1rem 0;
          padding: 1rem 1.15rem;
          border-radius: 18px;
          background: linear-gradient(135deg, rgba(255,255,255,.78), rgba(0,0,0,.03));
          border: 1px solid var(--border);
          font-family: var(--font-display);
          font-size: 1.18rem;
          line-height: 1.58;
        }
        .action-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: .8rem;
          margin: 1rem 0;
        }
        .action-card {
          padding: 1rem;
          border-radius: 18px;
          border: 1px solid var(--border);
          background: rgba(255,255,255,.78);
        }
        .action-card strong {
          display: block;
          margin-bottom: .45rem;
          color: var(--primary);
        }
        .action-card p {
          margin: 0;
          font-size: .92rem;
          line-height: 1.62;
          color: var(--text-muted);
        }

        /* Timeline */
        .timeline { position: relative; padding-left: 2rem; margin: 1.1rem 0; }
        .timeline::before { content: ''; position: absolute; left: .45rem; top: 0; bottom: 0; width: 2px; background: var(--border); }
        .timeline-item { position: relative; margin-bottom: 1rem; }
        .timeline-dot { position: absolute; left: -1.65rem; top: .3rem; width: 12px; height: 12px; border-radius: 50%; background: var(--report-structure, var(--primary)); border: 2px solid var(--report-bg, var(--bg)); }
        .timeline-date { font-size: .78rem; color: var(--text-muted); margin-bottom: .15rem; font-weight: 600; }
        .timeline-content { color: var(--text); line-height: 1.6; }

        /* Image */
        .report-image { margin: 1.1rem 0; } .report-image img { max-width: 100%; border-radius: var(--radius); }
        .report-image figcaption { font-size: .82rem; color: var(--text-muted); text-align: center; margin-top: .4rem; }
        .report-image--left { float: left; max-width: 40%; margin-right: 1.5rem; margin-bottom: .5rem; }
        .report-image--right { float: right; max-width: 40%; margin-left: 1.5rem; margin-bottom: .5rem; }
        .report-image--full { width: 100%; display: block; }
        .clearfix::after { content: ''; display: table; clear: both; }

        /* Code */
        .code-wrapper { margin: 1.1rem 0; border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); }
        .code-title { background: var(--surface); padding: .35rem 1rem; font-size: .78rem; color: var(--text-muted); font-family: var(--font-mono); border-bottom: 1px solid var(--border); }
        .code-wrapper pre { margin: 0; overflow-x: auto; }

        /* List */
        .report-list { margin: .75rem 0; }
        .styled-list { padding-left: 1.5rem; line-height: 1.8; }
        .styled-list li { margin-bottom: .25rem; }

        /* Diagram */
        .diagram-wrapper { margin: 1.1rem 0; text-align: center; }
        .diagram-wrapper svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }

        /* Chart */
        [data-component="chart"] { margin: 1.1rem 0; }

        /* Animations — all easing uses cubic-bezier(0.22,1,0.36,1) (ease-out-expo). Never use bounce (overshoot >1) or elastic (spring oscillation) easing — they read as dated and tacky. */
        .fade-in-up { opacity: 0; transform: translateY(18px); transition: opacity .5s cubic-bezier(0.22,1,0.36,1), transform .5s cubic-bezier(0.22,1,0.36,1); }
        .fade-in-up.visible { opacity: 1; transform: translateY(0); }
        .print-exporting .fade-in-up { opacity: 1 !important; transform: none !important; transition: none !important; }
        body.no-animations .fade-in-up { opacity: 1; transform: none; transition: none; }
        .kpi-grid.stagger-ready .kpi-card { opacity: 0; transform: translateY(20px) scale(0.95); transition: opacity .45s cubic-bezier(0.34,1.56,0.64,1), transform .45s cubic-bezier(0.34,1.56,0.64,1); }
        .kpi-grid.stagger-ready .kpi-card.visible { opacity: 1; transform: none; }
        .print-exporting .kpi-grid .kpi-card { opacity: 1 !important; transform: none !important; transition: none !important; }
        .timeline.stagger-ready .timeline-item { opacity: 0; transform: translateX(-12px); transition: opacity .4s cubic-bezier(0.22,1,0.36,1), transform .4s cubic-bezier(0.22,1,0.36,1); }
        .timeline.stagger-ready .timeline-item.visible { opacity: 1; transform: none; }
        .print-exporting .timeline .timeline-item { opacity: 1 !important; transform: none !important; transition: none !important; }
        body.no-animations .kpi-grid .kpi-card,
        body.no-animations .timeline .timeline-item { opacity: 1 !important; transform: none !important; transition: none !important; }
