'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import * as d3 from 'd3';

// ── Replace these API paths with your own routes ────────────────────────────
const API_ATOMS    = '/api/second-brain/atoms';     // GET → { atoms: Atom[] }
const API_CLUSTERS = '/api/second-brain/clusters';  // GET → ClustersData | POST (trigger re-cluster)
const API_INSIGHT  = '/api/second-brain/insight';   // POST { atom_texts, cluster_name } → { insight: string }
// ───────────────────────────────────────────────────────────────────────────

const GOLD = '#c8a84b';
const GOLD_DIM = 'rgba(200,168,75,0.06)';
const GOLD_BORDER = 'rgba(200,168,75,0.2)';

interface Atom {
  id: string;
  ts: number;
  date: string;
  raw: string;
  type: string;
  tags: string[];
  signal: string;
  actionable: boolean;
  nextAction: string | null;
}

interface Cluster {
  id: string;
  name: string;
  insight: string;
  atom_ids: string[];
  confidence: number;
  status: 'ESTABLISHED' | 'FORMING' | 'FADING';
  time_spread: number;
  category?: string;
}

interface Tension {
  name: string;
  atom_ids: string[];
  description: string;
}

interface ClustersData {
  generated: string | null;
  atomCount: number;
  clusters: Cluster[];
  emerging_signals: string[];
  tensions: Tension[];
  absences: string[];
}

const STATUS_COLORS: Record<string, string> = {
  ESTABLISHED: GOLD,
  FORMING: '#60a5fa',
  FADING: '#6b7280',
};

const CATEGORY_COLORS: Record<string, string> = {
  IDENTITY: '#a78bfa',
  CRAFT: '#f59e0b',
  SYSTEMS: '#34d399',
  LANGUAGE: '#60a5fa',
  PHILOSOPHY: '#f472b6',
  STRATEGY: '#fb923c',
};

const NODE_RADIUS = (c: Cluster) => Math.max(55, Math.min(85, 28 + c.atom_ids.length * 4 + c.time_spread * 2));

export default function SecondBrainVisualizer() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [clusters, setClusters] = useState<ClustersData | null>(null);
  const [atoms, setAtoms] = useState<Atom[]>([]);
  const [loading, setLoading] = useState(true);
  const [clustering, setClustering] = useState(false);
  const [selected, setSelected] = useState<Cluster | null>(null);
  const [insight, setInsight] = useState<string | null>(null);
  const [insightLoading, setInsightLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(API_ATOMS).then(r => r.json()),
      fetch(API_CLUSTERS).then(r => r.json()),
    ]).then(([atomsData, clustersData]) => {
      setAtoms(atomsData.atoms ?? []);
      if (clustersData.clusters?.length) setClusters(clustersData);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const atomMap = Object.fromEntries(atoms.map(a => [a.id, a]));
  const atomMapRef = useRef<Record<string, Atom>>({});
  useEffect(() => { atomMapRef.current = atomMap; }, [atoms]);

  // ── D3 graph ──────────────────────────────────────────────────────────────
  const selectedIdRef = useRef<string | null>(null);

  const handleNodeClick = useCallback((cluster: Cluster) => {
    setSelected(prev => {
      const next = prev?.id === cluster.id ? null : cluster;
      selectedIdRef.current = next?.id ?? null;
      return next;
    });
    setInsight(null);
  }, []);

  const handleNodeClickRef = useRef(handleNodeClick);
  useEffect(() => { handleNodeClickRef.current = handleNodeClick; }, [handleNodeClick]);

  const updateD3Selection = useCallback((selectedId: string | null) => {
    if (!svgRef.current) return;
    const svg = d3.select(svgRef.current);

    if (!selectedId) {
      svg.selectAll<SVGGElement, any>('g.node-group').each(function(d: any) {
        const statusOpacity: Record<string, number> = { ESTABLISHED: 1.0, FORMING: 0.82, FADING: 0.55 };
        const glowOpacity: Record<string, number> = { ESTABLISHED: 0.22, FORMING: 0.13, FADING: 0.06 };
        const strokeW: Record<string, number> = { ESTABLISHED: 2, FORMING: 1.5, FADING: 1 };
        d3.select(this).select('.node-main-circle')
          .attr('opacity', statusOpacity[d.status] ?? 1.0)
          .attr('stroke-width', strokeW[d.status] ?? 1.5);
        d3.select(this).select('.node-glow-ring')
          .attr('opacity', glowOpacity[d.status] ?? 0.15);
        d3.select(this).selectAll('.node-label-name, .node-label-count').attr('opacity', 1);
      });
      svg.selectAll<SVGLineElement, any>('line').attr('opacity', 0.6);
      return;
    }

    const linkedIds = new Set<string>();
    svg.selectAll<SVGLineElement, any>('line').each((d: any) => {
      const s = typeof d.source === 'object' ? d.source.id : d.source;
      const t = typeof d.target === 'object' ? d.target.id : d.target;
      if (s === selectedId) linkedIds.add(t);
      if (t === selectedId) linkedIds.add(s);
    });

    svg.selectAll<SVGGElement, any>('g.node-group').each(function(d: any) {
      const isSelected = d.id === selectedId;
      const isConnected = linkedIds.has(d.id);
      const dimOpacity = isSelected ? 1 : isConnected ? 0.65 : 0.18;
      d3.select(this).select('.node-main-circle')
        .attr('opacity', dimOpacity)
        .attr('stroke-width', isSelected ? 3 : 1.5);
      d3.select(this).select('.node-glow-ring')
        .attr('opacity', isSelected ? 0.5 : isConnected ? 0.18 : 0.04);
      d3.select(this).selectAll('.node-label-name, .node-label-count')
        .attr('opacity', isSelected ? 1 : isConnected ? 0.7 : 0.2);
    });

    svg.selectAll<SVGLineElement, any>('line').each(function(d: any) {
      const s = typeof d.source === 'object' ? d.source.id : d.source;
      const t = typeof d.target === 'object' ? d.target.id : d.target;
      const relevant = s === selectedId || t === selectedId;
      d3.select(this).attr('opacity', relevant ? 0.85 : 0.05);
    });
  }, []);

  useEffect(() => {
    updateD3Selection(selected?.id ?? null);
  }, [selected, updateD3Selection]);

  useEffect(() => {
    if (!svgRef.current || !clusters?.clusters?.length) return;

    const el = svgRef.current;
    const W = el.clientWidth || 900;
    const H = 500;
    el.setAttribute('height', String(H));

    d3.select(el).selectAll('*').remove();

    const nodes = clusters.clusters.map(c => ({ ...c, r: NODE_RADIUS(c) }));

    const links: { source: string; target: string; weight: number }[] = [];
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const shared = nodes[i].atom_ids.filter(id => nodes[j].atom_ids.includes(id)).length;
        if (shared > 0) links.push({ source: nodes[i].id, target: nodes[j].id, weight: shared });
      }
    }

    const sim = d3.forceSimulation(nodes as any)
      .force('link', d3.forceLink(links as any).id((d: any) => d.id).distance(160).strength(0.25))
      .force('charge', d3.forceManyBody().strength(-400))
      .force('center', d3.forceCenter(W / 2, H / 2))
      .force('collide', d3.forceCollide().radius((d: any) => d.r + 22))
      .force('x', d3.forceX(W / 2).strength(0.05))
      .force('y', d3.forceY(H / 2).strength(0.07));

    const svg = d3.select(el);

    // ── Defs: glow filter + animations ────────────────────────────────────
    const defs = svg.append('defs');
    const filter = defs.append('filter').attr('id', 'sbv-glow');
    filter.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'coloredBlur');
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    defs.append('style').text(`
      @keyframes sbv-float {
        0%   { transform: translateY(0px);  }
        50%  { transform: translateY(-5px); }
        100% { transform: translateY(0px);  }
      }
      @keyframes sbv-tension-crawl {
        from { stroke-dashoffset: 0; }
        to   { stroke-dashoffset: -24; }
      }
      .sbv-tension-arc { animation: sbv-tension-crawl 1.6s linear infinite; }
    `);

    // ── Links ──────────────────────────────────────────────────────────────
    const link = svg.append('g').selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#252525')
      .attr('stroke-width', (d: any) => Math.max(1, d.weight * 0.7))
      .attr('stroke-dasharray', '3 5')
      .attr('opacity', 0.6);

    // ── Tension arcs ───────────────────────────────────────────────────────
    const atomToCluster: Record<string, string> = {};
    nodes.forEach(n => n.atom_ids.forEach((id: string) => { atomToCluster[id] = n.id; }));

    type TensionArc = { source: string; target: string; name: string };
    const tensionArcs: TensionArc[] = [];
    (clusters.tensions ?? []).forEach(t => {
      const cIds = Array.from(new Set(t.atom_ids.map((id: string) => atomToCluster[id]).filter(Boolean))) as string[];
      for (let i = 0; i < cIds.length; i++) {
        for (let j = i + 1; j < cIds.length; j++) {
          if (!tensionArcs.some(a => (a.source === cIds[i] && a.target === cIds[j]) || (a.source === cIds[j] && a.target === cIds[i]))) {
            tensionArcs.push({ source: cIds[i], target: cIds[j], name: t.name });
          }
        }
      }
    });

    const nodeById = Object.fromEntries(nodes.map(n => [n.id, n]));

    function arcPath(s: any, t: any): string {
      const mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2;
      const dx = t.x - s.x, dy = t.y - s.y;
      const len = Math.sqrt(dx * dx + dy * dy) || 1;
      const bow = 40;
      return `M ${s.x} ${s.y} Q ${mx + (-dy / len) * bow} ${my + (dx / len) * bow} ${t.x} ${t.y}`;
    }

    const tensionArcGroup = svg.append('g');
    const tensionPaths = tensionArcGroup.selectAll('path')
      .data(tensionArcs)
      .join('path')
      .attr('class', 'sbv-tension-arc')
      .attr('fill', 'none')
      .attr('stroke', '#7f1d1d')
      .attr('stroke-width', 1.2)
      .attr('stroke-dasharray', '6 5')
      .attr('opacity', 0.4);

    // ── Shared hover tooltip ───────────────────────────────────────────────
    const tooltip = svg.append('g').attr('class', 'sbv-tooltip').attr('opacity', 0).attr('pointer-events', 'none');
    const tooltipBg = tooltip.append('rect').attr('rx', 6).attr('fill', '#111').attr('stroke', '#2a2a2a').attr('stroke-width', 1);
    const tooltipCat = tooltip.append('text').attr('font-size', 9).attr('font-family', 'monospace').attr('letter-spacing', '0.08em').attr('text-anchor', 'middle');
    const tooltipName = tooltip.append('text').attr('font-size', 13).attr('font-weight', '700').attr('font-family', 'system-ui, sans-serif').attr('fill', '#e8e8e8').attr('text-anchor', 'middle');
    const tooltipInsight = tooltip.append('text').attr('font-size', 10).attr('font-family', 'system-ui, sans-serif').attr('fill', '#888').attr('text-anchor', 'middle');

    function showTooltip(d: any, nx: number, ny: number) {
      const color = CATEGORY_COLORS[(d as any).category ?? ''] ?? GOLD;
      const insightText = (d.insight ?? '').length > 80 ? (d.insight as string).slice(0, 77) + '…' : (d.insight ?? '');
      tooltipCat.attr('fill', color).text(((d as any).category ?? '') + ' · ' + d.atom_ids.length + ' atoms · ' + Math.round(d.confidence * 100) + '% confidence');
      tooltipName.text(d.name);
      tooltipInsight.text(insightText);
      const ty = ny - d.r - 80;
      tooltipCat.attr('x', nx).attr('y', ty);
      tooltipName.attr('x', nx).attr('y', ty + 18);
      tooltipInsight.attr('x', nx).attr('y', ty + 34);
      const nameBbox = (tooltipName.node() as SVGTextElement)?.getBBox?.() ?? { x: nx - 100, y: ty + 5, width: 200, height: 15 };
      const insightBbox = (tooltipInsight.node() as SVGTextElement)?.getBBox?.() ?? { x: nx - 100, y: ty + 18, width: 200, height: 12 };
      const bw = Math.max(nameBbox.width, insightBbox.width) + 32;
      const bh = insightText ? 52 : 36;
      tooltipBg.attr('x', nx - bw / 2).attr('y', ty - 12).attr('width', bw).attr('height', bh);
      tooltip.transition().duration(120).attr('opacity', 1);
    }

    function hideTooltip() {
      tooltip.transition().duration(160).attr('opacity', 0);
    }

    // ── Recency scoring ────────────────────────────────────────────────────
    const tsList = nodes.map((n: any) => {
      const ca = n.atom_ids.map((id: string) => atomMapRef.current[id]).filter(Boolean);
      return ca.length ? Math.max(...ca.map((a: Atom) => a.ts)) : 0;
    });
    const tsMax = Math.max(...tsList) || 1;
    const tsMin = Math.min(...tsList) || 0;
    const tsRange = tsMax - tsMin || 1;
    nodes.forEach((n: any, i: number) => { (n as any)._recency = (tsList[i] - tsMin) / tsRange; });

    // ── Node groups ────────────────────────────────────────────────────────
    const node = svg.append('g').selectAll('g')
      .data(nodes)
      .join('g')
      .attr('class', 'node-group')
      .attr('cursor', 'pointer')
      .call(d3.drag<any, any>()
        .on('start', (event, d) => { if (!event.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
        .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
        .on('end', (event, d) => { if (!event.active) sim.alphaTarget(0); d.fx = null; d.fy = null; })
      )
      .on('click', (_event, d) => handleNodeClickRef.current(d))
      .on('mouseover', function(_event, d: any) {
        showTooltip(d, d.x ?? 0, d.y ?? 0);
        d3.select(this).select('.node-main-circle').transition().duration(120).attr('stroke-width', 3);
        d3.select(this).select('.node-glow-ring').transition().duration(120).attr('opacity', 0.5);
      })
      .on('mouseout', function(_event, d: any) {
        hideTooltip();
        const swMap: Record<string, number> = { ESTABLISHED: 2, FORMING: 1.5, FADING: 1 };
        const goMap: Record<string, number> = { ESTABLISHED: 0.22, FORMING: 0.13, FADING: 0.06 };
        d3.select(this).select('.node-main-circle').transition().duration(180).attr('stroke-width', swMap[d.status] ?? 1.5);
        d3.select(this).select('.node-glow-ring').transition().duration(180).attr('opacity', goMap[d.status] ?? 0.15);
      });

    // ── Float wrapper (temporal float — each node breathes at its own pace) ─
    const floatGroup = node.append('g')
      .attr('class', 'node-float')
      .style('animation', (_d: any, i: number) => {
        const dur = 4.0 + i * 0.3;
        return `sbv-float ${dur}s ease-in-out ${-(i * 0.6)}s infinite`;
      });

    // Glow ring
    floatGroup.append('circle')
      .attr('class', 'node-glow-ring')
      .attr('r', (d: any) => d.r + 7)
      .attr('fill', 'none')
      .attr('stroke', (d: any) => CATEGORY_COLORS[(d as any).category ?? ''] ?? GOLD)
      .attr('stroke-width', 1)
      .attr('opacity', (d: any) => ({ ESTABLISHED: 0.22, FORMING: 0.13, FADING: 0.06 })[d.status as string] ?? 0.15)
      .attr('filter', 'url(#sbv-glow)');

    // Main circle — status as texture (ESTABLISHED=solid, FORMING=dashed, FADING=sparse dots)
    const STATUS_FILL_OPACITY: Record<string, string> = { ESTABLISHED: '20', FORMING: '10', FADING: '07' };
    const STATUS_STROKE_DASH: Record<string, string | null> = { ESTABLISHED: null, FORMING: '5 4', FADING: '2 8' };
    const STATUS_OPACITY: Record<string, number> = { ESTABLISHED: 1.0, FORMING: 0.82, FADING: 0.55 };
    const STATUS_STROKE_W: Record<string, number> = { ESTABLISHED: 2, FORMING: 1.5, FADING: 1 };

    floatGroup.append('circle')
      .attr('class', 'node-main-circle')
      .attr('r', (d: any) => d.r)
      .attr('fill', (d: any) => (CATEGORY_COLORS[(d as any).category ?? ''] ?? GOLD) + (STATUS_FILL_OPACITY[d.status] ?? '18'))
      .attr('stroke', (d: any) => CATEGORY_COLORS[(d as any).category ?? ''] ?? GOLD)
      .attr('stroke-width', (d: any) => STATUS_STROKE_W[d.status] ?? 1.5)
      .attr('stroke-dasharray', (d: any) => STATUS_STROKE_DASH[d.status] ?? null)
      .attr('opacity', (d: any) => STATUS_OPACITY[d.status] ?? 1.0);

    // Confidence arc
    floatGroup.append('circle')
      .attr('r', (d: any) => d.r - 5)
      .attr('fill', 'none')
      .attr('stroke', (d: any) => CATEGORY_COLORS[(d as any).category ?? ''] ?? GOLD)
      .attr('stroke-width', 1.5)
      .attr('stroke-dasharray', (d: any) => {
        const circ = 2 * Math.PI * (d.r - 5);
        return `${circ * d.confidence} ${circ}`;
      })
      .attr('opacity', (d: any) => d.status === 'FADING' ? 0.15 : 0.35)
      .attr('transform', 'rotate(-90)');

    // ── Node labels ────────────────────────────────────────────────────────
    floatGroup.each(function(d: any) {
      const g = d3.select(this);
      const color = CATEGORY_COLORS[(d as any).category ?? ''] ?? GOLD;
      const words = d.name.split(' ');
      const lines: string[] = [];
      let cur: string[] = [];
      for (const w of words) {
        cur.push(w);
        if (cur.join(' ').length > 12) { lines.push(cur.join(' ')); cur = []; }
      }
      if (cur.length) lines.push(cur.join(' '));
      const lh = 14;
      const totalH = lines.length * lh;
      const startY = -(totalH / 2) + lh * 0.4;
      const nameEl = g.append('text')
        .attr('class', 'node-label-name')
        .attr('text-anchor', 'middle')
        .attr('fill', '#f0f0f0')
        .attr('font-size', 11)
        .attr('font-weight', '700')
        .attr('font-family', 'system-ui, sans-serif')
        .attr('pointer-events', 'none')
        .attr('opacity', 1);
      lines.forEach((line, i) => {
        nameEl.append('tspan').attr('x', 0).attr('dy', i === 0 ? `${startY}px` : `${lh}px`).text(line);
      });
      g.append('text')
        .attr('class', 'node-label-count')
        .attr('text-anchor', 'middle')
        .attr('y', totalH / 2 + 14)
        .attr('fill', color)
        .attr('font-size', 9)
        .attr('font-family', 'monospace')
        .attr('opacity', 0.8)
        .attr('pointer-events', 'none')
        .text(d.atom_ids.length + ' atoms');
    });

    // ── Category legend ────────────────────────────────────────────────────
    const uniqueCats = Array.from(new Set((clusters.clusters ?? []).map((c: any) => c.category).filter(Boolean))) as string[];
    const legend = svg.append('g').attr('transform', 'translate(16, 16)');
    uniqueCats.forEach((cat, i) => {
      const color = CATEGORY_COLORS[cat] ?? GOLD;
      const g = legend.append('g').attr('transform', `translate(0, ${i * 17})`);
      g.append('circle').attr('r', 4).attr('cx', 4).attr('cy', 0)
        .attr('fill', color + '28').attr('stroke', color).attr('stroke-width', 1.2);
      g.append('text').attr('x', 13).attr('y', 4)
        .attr('fill', color).attr('font-size', 9).attr('font-family', 'monospace')
        .attr('letter-spacing', '0.06em').text(cat);
    });

    // ── Tick ───────────────────────────────────────────────────────────────
    sim.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x).attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x).attr('y2', (d: any) => d.target.y);
      node.attr('transform', (d: any) => `translate(${
        Math.max(d.r + 6, Math.min(W - d.r - 6, d.x))
      },${
        Math.max(d.r + 6, Math.min(H - d.r - 6, d.y))
      })`);
      tensionPaths.attr('d', (d: any) => {
        const s = nodeById[d.source] as any;
        const t = nodeById[d.target] as any;
        return (s && t) ? arcPath(s, t) : '';
      });
    });

    sim.on('end', () => {
      if (selectedIdRef.current) updateD3Selection(selectedIdRef.current);
    });

    return () => { sim.stop(); };
  }, [clusters, handleNodeClick, updateD3Selection]);

  // ── Insight generator ──────────────────────────────────────────────────
  useEffect(() => {
    if (!selected) return;
    setInsight(null);
    setInsightLoading(true);
    const atom_texts = selected.atom_ids.map(id => atomMap[id]).filter(Boolean).map(a => a.raw);
    fetch(API_INSIGHT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ atom_texts, cluster_name: selected.name }),
    })
      .then(r => r.json())
      .then(d => setInsight(d.insight ?? null))
      .catch(() => setInsight(null))
      .finally(() => setInsightLoading(false));
  }, [selected]);

  async function runClustering() {
    setClustering(true);
    setError(null);
    setSelected(null);
    selectedIdRef.current = null;
    try {
      const res = await fetch(API_CLUSTERS, { method: 'POST' });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setClusters(data);
    } catch (e: any) {
      setError(e.message);
    }
    setClustering(false);
  }

  const fmt = (iso: string) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  return (
    <div style={{ background: '#0d0d0d', minHeight: '100%', fontFamily: 'system-ui, sans-serif' }}>

      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', padding: '20px 28px 0' }}>
        <div>
          <p style={{ fontSize: 11, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#555' }}>Second Brain</p>
          <p style={{ fontSize: 10, color: '#333', marginTop: 3 }}>
            {atoms.length} atoms · {clusters?.clusters?.length ?? 0} clusters
            {clusters?.generated && ` · clustered ${fmt(clusters.generated)}`}
          </p>
        </div>
        <button
          onClick={runClustering}
          disabled={clustering}
          style={{
            fontSize: 11, padding: '6px 16px', borderRadius: 6,
            background: clustering ? 'transparent' : GOLD_DIM,
            border: `1px solid ${GOLD_BORDER}`,
            color: clustering ? '#555' : GOLD,
            cursor: clustering ? 'not-allowed' : 'pointer',
          }}
        >
          {clustering ? 'Clustering…' : clusters?.clusters?.length ? '↻ Re-cluster' : 'Run Clustering'}
        </button>
      </div>

      {error && (
        <div style={{ margin: '12px 28px', background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: 8, padding: '10px 14px', fontSize: 12, color: '#ef4444' }}>
          {error}
        </div>
      )}

      {loading && <p style={{ color: '#333', fontSize: 13, padding: '40px 28px' }}>Loading…</p>}

      {!loading && !clusters?.clusters?.length && !clustering && (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <p style={{ color: '#444', fontSize: 13, marginBottom: 8 }}>No clusters yet.</p>
          <p style={{ color: '#333', fontSize: 11 }}>Run clustering to analyze {atoms.length} atoms.</p>
        </div>
      )}

      {/* D3 force graph */}
      {clusters?.clusters?.length ? (
        <div style={{ margin: '16px 0 0', borderBottom: '1px solid #1a1a1a' }}>
          <svg ref={svgRef} width="100%" height="500" style={{ display: 'block', background: '#0a0a0a' }} />
        </div>
      ) : null}

      {clusters?.clusters?.length ? (
        <div style={{ padding: '6px 28px', borderBottom: '1px solid #111' }}>
          <span style={{ fontSize: 9, color: '#2a2a2a', letterSpacing: '0.08em' }}>
            Node size = atoms × time spread · Dashed border = FORMING · Sparse dots = FADING · Red arcs = tensions · Click to explore
          </span>
        </div>
      ) : null}

      {/* Selected cluster detail */}
      {selected && (
        <div style={{ padding: '24px 28px', borderBottom: '1px solid #1a1a1a', background: '#0f0f0f' }}>
          <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 12 }}>
            <div>
              <p style={{ fontSize: 16, fontWeight: 700, color: '#e0e0e0', marginBottom: 6 }}>{selected.name}</p>
              <div style={{ display: 'flex', gap: 14 }}>
                <span style={{ fontSize: 10, color: STATUS_COLORS[selected.status] ?? GOLD, letterSpacing: '0.08em' }}>{selected.status}</span>
                <span style={{ fontSize: 10, color: '#555' }}>{selected.atom_ids.length} atoms</span>
                <span style={{ fontSize: 10, color: '#555' }}>{selected.time_spread}w spread</span>
                <span style={{ fontSize: 10, color: '#555' }}>{Math.round(selected.confidence * 100)}% confidence</span>
              </div>
            </div>
            <button onClick={() => { setSelected(null); setInsight(null); }} style={{ fontSize: 11, color: '#555', background: 'none', border: 'none', cursor: 'pointer' }}>✕</button>
          </div>

          <p style={{ fontSize: 12, color: '#666', lineHeight: 1.6, marginBottom: 16, fontStyle: 'italic' }}>{selected.insight}</p>

          {insightLoading && (
            <div style={{ background: GOLD_DIM, border: `1px solid ${GOLD_BORDER}`, borderRadius: 8, padding: '14px 16px', marginBottom: 20 }}>
              <p style={{ fontSize: 12, color: '#666', fontStyle: 'italic' }}>Reading your atoms…</p>
            </div>
          )}

          {insight && !insightLoading && (
            <div style={{ background: GOLD_DIM, border: `1px solid ${GOLD_BORDER}`, borderRadius: 8, padding: '14px 16px', marginBottom: 20 }}>
              <p style={{ fontSize: 10, color: '#555', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 8 }}>Deeper Read</p>
              <p style={{ fontSize: 14, color: GOLD, lineHeight: 1.7, fontStyle: 'italic' }}>{insight}</p>
            </div>
          )}

          <p style={{ fontSize: 10, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#444', marginBottom: 12 }}>Atoms in this cluster</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {selected.atom_ids.map(id => {
              const atom = atomMap[id];
              if (!atom) return null;
              return (
                <div key={id} style={{ background: '#111', border: '1px solid #1a1a1a', borderRadius: 8, padding: '10px 14px' }}>
                  <div style={{ display: 'flex', gap: 12, marginBottom: 5 }}>
                    <span style={{ fontSize: 10, color: '#444' }}>{atom.date?.slice(0, 10)}</span>
                    <span style={{ fontSize: 10, color: atom.signal === 'hot' ? GOLD : atom.signal === 'warm' ? '#60a5fa' : '#444' }}>● {atom.signal}</span>
                  </div>
                  <p style={{ fontSize: 12, color: '#d0d0d0', lineHeight: 1.6 }}>{atom.raw}</p>
                  {atom.nextAction && <p style={{ fontSize: 10, color: '#555', marginTop: 6, fontStyle: 'italic' }}>→ {atom.nextAction}</p>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Cluster directory */}
      {clusters?.clusters?.length ? (
        <div style={{ padding: '20px 28px', borderBottom: '1px solid #111' }}>
          <p style={{ fontSize: 10, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#555', marginBottom: 16 }}>Cluster Directory</p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 10 }}>
            {clusters.clusters.map(c => {
              const catColor = CATEGORY_COLORS[(c as any).category ?? ''] ?? GOLD;
              const isSelected = selected?.id === c.id;
              return (
                <div key={c.id} onClick={() => handleNodeClick(c)} style={{
                  background: isSelected ? '#1a1500' : '#111',
                  border: `1px solid ${isSelected ? catColor : catColor + '30'}`,
                  borderLeft: `3px solid ${catColor}`,
                  borderRadius: 8, padding: '12px 14px', cursor: 'pointer',
                }}>
                  <p style={{ fontSize: 12, fontWeight: 700, color: isSelected ? '#fff' : '#e0e0e0', marginBottom: 4 }}>{c.name}</p>
                  <p style={{ fontSize: 11, color: '#666', lineHeight: 1.5, fontStyle: 'italic' }}>{c.insight}</p>
                  <div style={{ display: 'flex', gap: 10, marginTop: 8 }}>
                    <span style={{ fontSize: 9, color: catColor, letterSpacing: '0.08em', textTransform: 'uppercase' }}>{(c as any).category}</span>
                    <span style={{ fontSize: 9, color: '#333' }}>{c.atom_ids.length} atoms</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : null}

      {/* Tensions */}
      {clusters?.tensions?.length ? (
        <div style={{ padding: '20px 28px', borderBottom: '1px solid #111' }}>
          <p style={{ fontSize: 10, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#888', marginBottom: 12 }}>Tensions</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {clusters.tensions.map((t, i) => (
              <div key={i} style={{ background: '#111', border: '1px solid #1e1e1e', borderRadius: 8, padding: '12px 14px' }}>
                <p style={{ fontSize: 12, fontWeight: 600, color: '#d4a843', marginBottom: 4 }}>{t.name}</p>
                <p style={{ fontSize: 11, color: '#aaa', lineHeight: 1.5 }}>{t.description}</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Emerging signals */}
      {clusters?.emerging_signals?.length ? (
        <div style={{ padding: '20px 28px', borderBottom: '1px solid #111' }}>
          <p style={{ fontSize: 10, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#555', marginBottom: 12 }}>Emerging Signals</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {clusters.emerging_signals.map(id => {
              const atom = atomMap[id];
              if (!atom) return null;
              return (
                <div key={id} style={{ display: 'flex', gap: 12, alignItems: 'baseline', padding: '8px 12px', background: '#111', borderRadius: 6, border: '1px solid #1a1a1a' }}>
                  <span style={{ fontSize: 10, color: '#4ade80', flexShrink: 0 }}>{atom.date?.slice(0, 10)}</span>
                  <p style={{ fontSize: 12, color: '#ccc' }}>{atom.raw}</p>
                </div>
              );
            })}
          </div>
        </div>
      ) : null}

      {/* Notable absences */}
      {clusters?.absences?.length ? (
        <div style={{ padding: '20px 28px' }}>
          <p style={{ fontSize: 10, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#888', marginBottom: 10 }}>Notable Absences</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {clusters.absences.map((a, i) => (
              <span key={i} style={{ fontSize: 11, color: '#bbb', background: '#111', border: '1px solid #2a2a2a', borderRadius: 4, padding: '4px 10px' }}>{a}</span>
            ))}
          </div>
        </div>
      ) : null}

    </div>
  );
}
