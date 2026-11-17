/* vibe-ledger file flowchart: dagre layout, drawing, pan/zoom/pinch, selection, explanation panel. */
(function () {
  "use strict";
  var dataEl = document.getElementById("vl-data");
  if (!dataEl || typeof dagre === "undefined") return;
  var data = JSON.parse(dataEl.textContent);
  var S = data.strings;
  var NS = "http://www.w3.org/2000/svg";
  var W = 236, H = 58, EXT_GAP = 100, ROW_GAP = 22, RANK_GAP = 72;
  var ICON = { entry: "▶", logic: "ƒ", data: "⛁", paid: "✦", folder: "▤", item: "◆" };
  var svg = document.getElementById("vlg-svg");
  var viewport = document.getElementById("vlg-viewport");
  var panel = document.getElementById("vlg-panel");
  var byId = {}, folderOf = {}, folderById = {};
  data.nodes.forEach(function (n) { byId[n.id] = n; });
  // a function map (explain.json `areas`): the page opens on the areas, and the data view draws what they read and write
  var AREAS = !!(data.areas && data.areas.length), flowArea = {};
  if (AREAS) {
    data.flow.items.forEach(function (it) { byId[it.id] = it; });
    data.flow.areas.forEach(function (a) { flowArea[a] = true; });
  }
  var BASE = AREAS ? "map" : "files";
  var expanded = {}, selected = null, view = { s: 1, x: 0, y: 0 }, layout = null, fitted = false;
  // the view: "files" (folders only collapse in big projects), "modules" (everything folded into its module) or
  // "data" (only the files on a path from an entry to a data store or outside service)
  var mode = BASE, groups = [], grouped = false, seq = false, seqBox = null;
  var inFlow = {};
  ((data.data_flow || {}).files || []).forEach(function (id) { inFlow[id] = true; });
  function setGroups(list, on) {
    groups = list || [];
    grouped = on;
    folderOf = {};
    folderById = {};
    expanded = {};
    groups.forEach(function (f) { folderById[f.id] = f; f.files.forEach(function (id) { folderOf[id] = f.id; }); });
  }
  if (AREAS) setGroups(data.areas, true); else setGroups(data.folders, data.collapsed);
  function isItem(id) { return id.indexOf("item:") === 0; }
  function inView(id) {
    if (isItem(id)) return AREAS && mode === "data";
    if (AREAS && mode === "data") return isExt(id) || !!flowArea[folderOf[id]];
    return mode !== "data" || isExt(id) || !!inFlow[id];
  }
  var journey = null, journeyById = {}, hover = null, compare = false;
  (data.journeys || []).forEach(function (j) { journeyById[j.id] = j; });
  var pointers = {}, drag = null, pinch = null, moved = false;

  function fmt(s, kv) {  // "{n|file|files}" picks the word for one or for others (same rule as i18n.t)
    return String(s).replace(/\{(\w+)\|([^|{}]*)\|([^{}]*)\}/g, function (_, k, one, many) { return kv[k] === 1 ? one : many; })
      .replace(/\{(\w+)\}/g, function (_, k) { return kv[k] == null ? "" : kv[k]; });
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function sv(tag, attrs) { var e = document.createElementNS(NS, tag); Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); }); return e; }
  function units(s) { var n = 0; for (var i = 0; i < s.length; i++) n += s.charCodeAt(i) > 0x2e80 ? 2 : 1; return n; }
  function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
  function isExt(id) { return id.indexOf("ext:") === 0; }
  function isFolder(id) { return id.indexOf("folder:") === 0; }
  function visibleId(id) { var f = folderOf[id]; return grouped && f && !expanded[f] ? "folder:" + f : id; }
  function entity(vid) { return isFolder(vid) ? folderById[vid.slice(7)] : byId[vid]; }
  function roleOf(vid) { return isFolder(vid) ? "folder" : byId[vid].role; }
  function areaMode() { return AREAS && (mode === "map" || mode === "data"); }
  // a function map's data view, and its map while every area is closed, are short chains of a few boxes: they read
  // top to bottom and fit the screen; an opened area brings back the left-to-right file chart, which suits many files
  function topDown() {
    if (!AREAS) return false;
    if (mode === "data") return true;
    return mode === "map" && !Object.keys(expanded).some(function (k) { return expanded[k]; });
  }

  function computeLayout() {
    var g = new dagre.graphlib.Graph();
    var tb = topDown();
    g.setGraph(tb ? { rankdir: "TB", nodesep: 34, ranksep: 44, marginx: 40, marginy: 40 }
      : { rankdir: "LR", nodesep: ROW_GAP, ranksep: RANK_GAP, marginx: 40, marginy: 40 });
    g.setDefaultEdgeLabel(function () { return {}; });
    var visible = {}, edges = {};
    var all = AREAS && mode === "data" ? data.nodes.concat(data.flow.items) : data.nodes;
    all.forEach(function (n) {
      if (isExt(n.id) || !inView(n.id)) return;
      var v = visibleId(n.id);
      if (!visible[v]) { visible[v] = true; g.setNode(v, { width: W, height: H }); }
    });
    function link(e, carries) {
      if (!inView(e.from) || !inView(e.to)) return;
      var a = visibleId(e.from), b = isExt(e.to) ? e.to : visibleId(e.to);
      if (a === b) return;
      var k = a + "\u0001" + b;
      var x = edges[k] || (edges[k] = { from: a, to: b, count: 0, risky: false, names: [], carries: [] });
      (carries || []).forEach(function (c) { if (x.carries.indexOf(c) < 0) x.carries.push(c); });
      if (carries) return x;  // a data link is not an import: it does not count as one
      x.count += 1;
      x.risky = x.risky || e.risky;
      (e.names || []).forEach(function (nm) { if (x.names.indexOf(nm) < 0 && x.names.length < 6) x.names.push(nm); });
      return x;
    }
    (AREAS && mode === "data" ? data.flow.edges : data.edges).forEach(function (e) { link(e); });
    if (AREAS && mode === "map") data.area_links.forEach(function (l) { link(l, l.carries); });
    // the map ranks its areas by where data goes (writer left of reader) when it knows any; imports only draw
    var byData = AREAS && mode === "map" && Object.keys(edges).some(function (k) { return edges[k].carries.length; });
    Object.keys(edges).forEach(function (k) {
      var e = edges[k];
      if (tb) {
        if (byData && !e.carries.length && !isExt(e.to)) return;  // an import-only link is drawn, not ranked
        [e.from, e.to].forEach(function (v) { if (!g.hasNode(v)) g.setNode(v, { width: W, height: H }); });
        g.setEdge(e.from, e.to);
      } else if (!isExt(e.to) && (!byData || e.carries.length)) g.setEdge(e.from, e.to);
    });
    if (tb) {
      // parts no data passes through (shared libraries, an engine) would all crowd the first row: they go in their
      // own rows under the chain, as the parts the others use
      var loose = byData ? g.nodes().filter(function (v) { return !g.nodeEdges(v).length; }) : [];
      if (loose.length === g.nodeCount()) loose = [];
      loose.forEach(function (v) { g.removeNode(v); });
      dagre.layout(g);
      var tbBoxes = {}, x0 = Infinity, x1 = -Infinity, y1 = 40;
      g.nodes().forEach(function (v) {
        var p = g.node(v), b = { id: v, x: p.x - W / 2, y: p.y - H / 2 };
        tbBoxes[v] = b;
        x0 = Math.min(x0, b.x); x1 = Math.max(x1, b.x + W); y1 = Math.max(y1, b.y + H);
      });
      var support = null;
      if (loose.length) {
        var per = Math.min(3, loose.length), rowW = per * W + (per - 1) * 34;
        if (x0 === Infinity) { x0 = 40; x1 = 40 + rowW; }
        var left = (x0 + x1) / 2 - rowW / 2, top = y1 + 86;
        loose.sort().forEach(function (v, i) {
          tbBoxes[v] = { id: v, x: left + (i % per) * (W + 34), y: top + Math.floor(i / per) * (H + 26) };
        });
        support = { x: left, w: rowW, y: top - 30 };
      }
      return { g: g, edges: edges, boxes: tbBoxes, tb: true, support: support };
    }
    if (data.entries.length && !byData) {
      g.setNode("__src", { width: 1, height: 1 });
      var isEntry = {}, hasIn = {};
      data.entries.forEach(function (id) { var v = visibleId(id); isEntry[v] = true; if (visible[v]) g.setEdge("__src", v); });
      Object.keys(edges).forEach(function (k) { hasIn[edges[k].to] = true; });
      // a file nothing imports that is not an entry belongs in the logic column, never left of the entries
      Object.keys(visible).forEach(function (v) { if (!isEntry[v] && !hasIn[v]) g.setEdge("__src", v, { minlen: 2 }); });
    }
    dagre.layout(g);
    var boxes = {}, ids = Object.keys(visible), maxRight = 0, minY = Infinity, maxY = -Infinity;
    ids.forEach(function (v) {
      var p = g.node(v), b = { id: v, x: p.x - W / 2, y: p.y - H / 2 };
      boxes[v] = b;
      maxRight = Math.max(maxRight, b.x + W);
      minY = Math.min(minY, b.y);
      maxY = Math.max(maxY, b.y + H);
    });
    if (!ids.length) { minY = 40; maxY = 40; }
    // outside services get their own column on the right, ordered by where their callers sit
    var exts = data.nodes.filter(function (n) { return isExt(n.id); }).map(function (n) {
      var ys = Object.keys(edges).filter(function (k) { return edges[k].to === n.id && boxes[edges[k].from]; })
        .map(function (k) { return boxes[edges[k].from].y; });
      return { id: n.id, n: ys.length, order: ys.length ? ys.reduce(function (a, b) { return a + b; }, 0) / ys.length : 0 };
    }).filter(function (x) { return x.n || mode !== "data"; }).sort(function (a, b) { return a.order - b.order || (a.id < b.id ? -1 : 1); });
    var colX = (ids.length ? maxRight : 40) + EXT_GAP;
    var total = exts.length * H + Math.max(0, exts.length - 1) * ROW_GAP;
    var y0 = (minY + maxY) / 2 - total / 2;
    exts.forEach(function (x, i) { boxes[x.id] = { id: x.id, x: colX, y: y0 + i * (H + ROW_GAP) }; });
    return { g: g, edges: edges, boxes: boxes };
  }

  function drawBands(list) {
    if (!list.length || areaMode()) return;
    var minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    list.forEach(function (b) { minX = Math.min(minX, b.x); maxX = Math.max(maxX, b.x + W); minY = Math.min(minY, b.y); maxY = Math.max(maxY, b.y + H); });
    var entryX = list.filter(function (b) { return !isExt(b.id) && roleOf(b.id) === "entry"; }).map(function (b) { return b.x; });
    var extX = list.filter(function (b) { return isExt(b.id); }).map(function (b) { return b.x; });
    var top = minY - 56, height = maxY - minY + 80, bands = [];
    var entryEnd = entryX.length ? Math.min.apply(null, entryX) + W + 18 : null;
    var dataStart = extX.length ? Math.min.apply(null, extX) - 18 : null;
    if (entryEnd !== null) bands.push([minX - 18, entryEnd, S.g_band_entry]);
    var ls = entryEnd !== null ? entryEnd + 10 : minX - 18, le = dataStart !== null ? dataStart - 10 : maxX + 18;
    if (le - ls > 40) bands.push([ls, le, S.g_band_logic]);
    if (dataStart !== null) bands.push([dataStart, maxX + 18, S.g_band_data]);
    var layer = sv("g", { "class": "vlg-bands" });
    bands.forEach(function (b) {
      layer.appendChild(sv("rect", { "class": "vlg-band", x: b[0], y: top, width: b[1] - b[0], height: height, rx: 16 }));
      var t = sv("text", { "class": "vlg-band-label", x: (b[0] + b[1]) / 2, y: top + 24, "text-anchor": "middle" });
      t.textContent = b[2];
      layer.appendChild(t);
    });
    viewport.appendChild(layer);
  }

  function drawNode(b) {
    var ent = entity(b.id), role = roleOf(b.id), state = ent.state || "ok";
    var g = sv("g", { "class": "vlg-node r-" + role + " s-" + state, "data-id": b.id, "data-x": b.x.toFixed(1),
      "data-y": b.y.toFixed(1), "data-w": W, "data-h": H, "data-dim": "0",
      transform: "translate(" + b.x.toFixed(1) + "," + b.y.toFixed(1) + ")", tabindex: "0" });
    g.appendChild(sv("rect", { "class": "vlg-card", width: W, height: H, rx: 14 }));
    g.appendChild(sv("circle", { "class": "vlg-icon-bg", cx: 24, cy: H / 2, r: 14 }));
    var icon = sv("text", { "class": "vlg-icon", x: 24, y: H / 2 + 5, "text-anchor": "middle" });
    icon.textContent = ICON[role] || "";
    g.appendChild(icon);
    var label = sv("text", { "class": "vlg-label", x: 46, y: 24 });
    label.textContent = ent.short || ent.label;
    g.appendChild(label);
    var sub = sv("text", { "class": "vlg-sub", x: 46, y: 42 });
    // in the data view a folder counts only the files the view draws
    sub.textContent = isFolder(b.id) && mode === "data" && !AREAS
      ? fmt(S.g_folder_files, { n: ent.files.filter(inView).length }) : ent.sub || "";
    g.appendChild(sub);
    if (ent.badge) {
      var bw = units(ent.badge) * 6.2 + 16;
      g.appendChild(sv("rect", { "class": "vlg-badge-bg", x: W - bw + 8, y: -9, width: bw, height: 18, rx: 9 }));
      var bt = sv("text", { "class": "vlg-badge", x: W - bw / 2 + 8, y: 4, "text-anchor": "middle" });
      bt.textContent = ent.badge;
      g.appendChild(bt);
    }
    var title = sv("title", {});
    title.textContent = isFolder(b.id) ? (ent.plain ? ent.label + " — " + ent.plain : b.id.slice(7)) : isItem(b.id) ? ent.label : b.id;
    g.appendChild(title);
    g.addEventListener("click", function (ev) { ev.stopPropagation(); if (!moved) onNodeClick(b.id); });
    g.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); onNodeClick(b.id); }  // a card acts like a button
    });
    // hovering previews a file's neighbours without opening it (Obsidian-style); a selection or a route wins
    g.addEventListener("mouseenter", function () { if (!selected && !journey) { hover = b.id; applySelection(); } });
    g.addEventListener("mouseleave", function () { if (hover) { hover = null; applySelection(); } });
    return g;
  }

  function draw() {
    seq = false;  // the flowchart replaces a sequence view, so its box no longer applies
    seqBox = null;
    hover = null;  // the hovered card may be the folder this redraw replaces: its mouseleave never comes
    layout = computeLayout();
    while (viewport.firstChild) viewport.removeChild(viewport.firstChild);
    var boxes = layout.boxes, ids = Object.keys(boxes);
    drawBands(ids.map(function (v) { return boxes[v]; }));
    if (layout.support) {  // the row of shared parts under the chain says what it is
      var st = sv("text", { "class": "vlg-band-label", x: (layout.support.x + layout.support.w / 2).toFixed(1),
        y: layout.support.y.toFixed(1), "text-anchor": "middle" });
      st.textContent = S.g_support;
      viewport.appendChild(st);
    }
    var edgeLayer = sv("g", { "class": "vlg-edges" }), nodeLayer = sv("g", { "class": "vlg-nodes" });
    var labelLayer = sv("g", { "class": "vlg-edge-labels" });
    layout.cols = columnsOf(boxes);
    var routed = Object.keys(layout.edges).map(function (k) {
      var e = layout.edges[k], a = boxes[e.from], b = boxes[e.to];
      return a && b ? { e: e, a: a, b: b, fwd: b.x > a.x, pa: a.y + H / 2, pb: b.y + H / 2 } : null;
    }).filter(Boolean);
    if (!layout.tb) assignPorts(routed.filter(function (r) { return Math.abs(r.a.x - r.b.x) > 1; }));
    routed.forEach(function (r) {
      var e = r.e, a = r.a, b = r.b, d, mid, ends;
      if (layout.tb) {
        var tp = layout.g.hasEdge(e.from, e.to) ? layout.g.edge(e.from, e.to).points : straight(a, b), f1 = function (v) { return v.toFixed(1); };
        d = "M" + tp.map(function (q) { return f1(q.x) + "," + f1(q.y); }).join(" L");
        mid = tp[Math.floor(tp.length / 2)];
        ends = [tp[0], tp[tp.length - 1]];
      } else if (Math.abs(a.x - b.x) <= 1) {
        d = sideLoop(a, b);
        mid = { x: a.x + W + 30, y: (a.y + b.y + H) / 2 };
        ends = [{ x: a.x + W, y: a.y + H / 2 }, { x: b.x + W, y: b.y + H / 2 }];
      } else {
        // out of one side, into the facing side, crossing columns through the gaps between cards
        var ge = !isExt(e.to) && layout.g.hasEdge(e.from, e.to) ? layout.g.edge(e.from, e.to) : null;
        var pts = routePoints(a, b, r.pa, r.pb, ge ? ge.points : null);
        d = pathOf(pts);
        var m0 = pts[Math.floor((pts.length - 1) / 2)], m1 = pts[Math.ceil((pts.length - 1) / 2)];
        mid = { x: (m0.x + m1.x) / 2, y: (m0.y + m1.y) / 2 };
        ends = [pts[0], pts[pts.length - 1]];
      }
      var dataOnly = mode === "map" && e.carries && e.carries.length && !e.count;
      var importOnly = mode === "map" && AREAS && !(e.carries && e.carries.length) && !isExt(e.to);
      edgeLayer.appendChild(sv("path", { d: d, "class": "vlg-edge" + (e.risky ? " risky" : "") + (dataOnly ? " data" : "") + (importOnly ? " imp" : ""), "data-from": e.from,
        "data-to": e.to, "marker-end": "url(#vlg-arrow" + (e.risky ? "-risky" : "") + ")" }));
      var carries = mode === "map" && e.carries && e.carries.length ? e.carries.slice(0, 2).join(" · ") + (e.carries.length > 2 ? " …" : "")
        : mode === "data" && !AREAS && (data.data_flow.labels || {})[e.from + "\u0001" + e.to];
      if (carries) {  // what this link sends, from the verified app map
        // two parts sending data both ways share one line: each label takes its own side of it, not the middle
        var back = layout.edges[e.to + "\u0001" + e.from], twoWay = mode === "map" && back && back.carries && back.carries.length,
          side = e.from < e.to ? -1 : 1;
        var c = mode === "map"
          ? sv("text", { x: (mid.x + (twoWay ? side * 10 : 0)).toFixed(1), y: (mid.y - 6).toFixed(1), "class": "vlg-edge-label carries",
              "text-anchor": twoWay ? (side < 0 ? "end" : "start") : "middle", "data-from": e.from, "data-to": e.to })
          : sv("text", { x: (ends[1].x - 10).toFixed(1), y: (ends[1].y - 7).toFixed(1), "class": "vlg-edge-label carries",
              "text-anchor": "end", "data-from": e.from, "data-to": e.to });
        c.textContent = carries;
        labelLayer.appendChild(c);
      }
      // a link between folders stands for several imports: say how many in both views; names are for developers
      var merged = (isFolder(e.from) || isFolder(e.to)) && e.count > 1 && !carries && !(AREAS && mode === "data");
      if (merged || e.names.length) {
        // imported names (developer view) appear only on the links of the file in focus — see placeNameLabel
        var t = sv("text", { x: mid.x.toFixed(1), y: (mid.y - 6).toFixed(1),
          "class": "vlg-edge-label" + (merged ? (mode === "map" ? " dev-only" : "") : " names dev-only"), "text-anchor": "middle", "data-from": e.from,
          "data-to": e.to, "data-sx": ends[0].x.toFixed(1), "data-sy": ends[0].y.toFixed(1),
          "data-ex": ends[1].x.toFixed(1), "data-ey": ends[1].y.toFixed(1) });
        t.textContent = merged ? fmt(S.g_merged, { n: e.count }) : shortNames(e.names);
        labelLayer.appendChild(t);
      }
    });
    viewport.appendChild(edgeLayer);
    viewport.appendChild(nodeLayer);
    viewport.appendChild(labelLayer);
    ids.forEach(function (v) { nodeLayer.appendChild(drawNode(boxes[v])); });
    applySelection();
    document.body.setAttribute("data-layout", "done");
  }

  function neighborsOf(vid) {
    var set = {};
    set[vid] = true;
    Object.keys(layout.edges).forEach(function (k) {
      var e = layout.edges[k];
      if (e.from === vid) set[e.to] = true;
      if (e.to === vid) set[e.from] = true;
    });
    return set;
  }

  function applySelection() {
    var vid = selected ? visibleId(selected) : null, fid = vid || (hover && layout.boxes[hover] ? hover : null);
    var nb = fid ? neighborsOf(fid) : null;
    var jset = null, jpairs = {};
    if (journey) {
      jset = {};
      journey.steps.forEach(function (st, k) {
        var v = visibleId(st.file);
        jset[v] = true;
        if (k) {
          var p = visibleId(sourceStep(k).file);
          jpairs[p + "\u0001" + v] = true;
          jpairs[v + "\u0001" + p] = true;
        }
      });
    }
    var cmp = compare && !!data.diff && !jset && !fid, added = {};
    if (cmp) data.diff.added_links.forEach(function (l) { added[visibleId(l[0]) + "\u0001" + visibleId(l[1])] = true; });
    viewport.querySelectorAll(".vlg-node").forEach(function (g) {
      var id = g.getAttribute("data-id"), df = cmp ? diffOf(id) : null;
      var dim = jset ? !jset[id] : nb ? !nb[id] : (cmp && !df);
      g.classList.toggle("sel", id === vid);
      g.classList.toggle("jstep", !!jset && !!jset[id]);
      g.classList.toggle("d-new", df === "new");
      g.classList.toggle("d-changed", df === "changed");
      g.classList.toggle("dim", dim);
      g.setAttribute("data-dim", dim ? "1" : "0");
    });
    viewport.querySelectorAll("[data-from]").forEach(function (e) {
      var f = e.getAttribute("data-from"), to = e.getAttribute("data-to");
      var hot = jset ? !!jpairs[f + "\u0001" + to] : (!!fid && (f === fid || to === fid));
      var fresh = cmp && !!added[f + "\u0001" + to];
      e.classList.toggle("hot", hot);
      e.classList.toggle("d-new", fresh);
      e.classList.toggle("flow", hot && !!jset);  // a route's arrows run in the direction of travel
      e.classList.toggle("dim", ((!!fid || !!jset) && !hot) || (cmp && !fresh));
      if (e.tagName.toLowerCase() === "path") {
        e.setAttribute("marker-end", "url(#vlg-arrow" + (hot ? "-hot" : e.classList.contains("risky") ? "-risky" : "") + ")");
      } else if (hot && e.classList.contains("names")) {
        placeNameLabel(e, fid === to);
      }
    });
    drawJourney();
    drawDiff(cmp);
  }

  // a card's change since the last run; a folder shows "changed" when anything inside it is new or changed
  function diffOf(vid) {
    if (!isFolder(vid)) return byId[vid] ? byId[vid].diff : null;
    return folderById[vid.slice(7)].files.some(function (id) { return inView(id) && byId[id] && byId[id].diff; }) ? "changed" : null;
  }

  // compare view: a "new"/"changed" tag on each card, and the links that are gone drawn as red dashes
  function drawDiff(on) {
    var old = document.getElementById("vlg-dlayer");
    if (old) old.parentNode.removeChild(old);
    if (!on || !layout || seq) return;
    var layer = sv("g", { id: "vlg-dlayer" });
    data.diff.removed_links.forEach(function (l) {
      var a = layout.boxes[visibleId(l[0])], b = layout.boxes[visibleId(l[1])];
      if (a && b && a !== b) layer.appendChild(sv("path", { "class": "vlg-dgone", d: connector(a, b) }));
    });
    Object.keys(layout.boxes).forEach(function (vid) {
      var df = diffOf(vid), b = layout.boxes[vid];
      if (!df) return;
      var label = df === "new" ? S.g_diff_tag_new : S.g_diff_tag_changed, w = units(label) * 6.5 + 16;
      var g = sv("g", { "class": "vlg-dtag d-" + df, transform: "translate(" + (b.x + W - w - 8).toFixed(1) + "," + (b.y + H - 9).toFixed(1) + ")" });
      g.appendChild(sv("rect", { width: w, height: 18, rx: 9 }));
      var tx = sv("text", { x: w / 2, y: 12.5, "text-anchor": "middle" });
      tx.textContent = label;
      g.appendChild(tx);
      layer.appendChild(g);
    });
    viewport.appendChild(layer);
  }

  // a focused link's label: two names when they are short, else the first one; never wider than LABEL_MAX
  var LABEL_MAX = 28;
  function shortNames(names) {
    var two = names.slice(0, 2).join(", "), rest = names.length - 2;
    if (two.length <= LABEL_MAX) return two + (rest > 0 ? " +" + rest : "");
    var first = names[0].length > LABEL_MAX ? names[0].slice(0, LABEL_MAX - 1) + "\u2026" : names[0];
    return first + (names.length > 1 ? " +" + (names.length - 1) : "");
  }

  // a name label sits beside the far end of a focused link (by the other file, not the one in focus), so the
  // labels of one file's links spread over its neighbours instead of piling up beside it
  function placeNameLabel(t, focusIsTarget) {
    var near = focusIsTarget ? "s" : "e", out = (near === "s") === (+t.getAttribute("data-ex") >= +t.getAttribute("data-sx"));
    t.setAttribute("x", (+t.getAttribute("data-" + near + "x") + (out ? 10 : -10)).toFixed(1));
    t.setAttribute("y", (+t.getAttribute("data-" + near + "y") - 6).toFixed(1));
    t.setAttribute("text-anchor", out ? "start" : "end");
  }

  // ---- routing: a link crosses each column through a gap between cards and bends only in the gutters ----
  function columnsOf(boxes) {
    var cols = {};
    Object.keys(boxes).forEach(function (id) { var b = boxes[id], k = Math.round(b.x); (cols[k] = cols[k] || []).push(b); });
    return Object.keys(cols).map(Number).sort(function (p, q) { return p - q; }).map(function (x) {
      return { x: x, cards: cols[x].sort(function (p, q) { return p.y - q.y; }) };
    });
  }

  // the y nearest to `want` where a line crosses this column without touching a card
  function freeY(col, want) {
    var M = 7, cards = col.cards;
    if (!cards.some(function (c) { return want > c.y - M && want < c.y + H + M; })) return want;
    var cands = [cards[0].y - M - 6, cards[cards.length - 1].y + H + M + 6];
    for (var i = 0; i + 1 < cards.length; i++) {
      var top = cards[i].y + H, bottom = cards[i + 1].y;
      if (bottom - top >= 6) cands.push((top + bottom) / 2);
    }
    return cands.reduce(function (best, y) { return Math.abs(y - want) < Math.abs(best - want) ? y : best; });
  }

  // waypoints from box a (port pa) to box b (port pb); dagre's own points, when it has them, pick the gap to use
  function routePoints(a, b, pa, pb, hints) {
    var fwd = b.x > a.x, x0 = fwd ? a.x + W : a.x, x3 = fwd ? b.x : b.x + W, pts = [{ x: x0, y: pa }];
    var lo = Math.min(a.x, b.x), hi = Math.max(a.x, b.x);
    var cols = layout.cols.filter(function (c) { return c.x > lo + 1 && c.x < hi - 1; });
    if (!fwd) cols.reverse();
    cols.forEach(function (c) {
      var want = pa + (pb - pa) * (c.x + W / 2 - x0) / ((x3 - x0) || 1);
      (hints || []).forEach(function (h) { if (Math.abs(h.x - (c.x + W / 2)) < W / 2) want = h.y; });
      var y = freeY(c, want);
      pts.push({ x: fwd ? c.x : c.x + W, y: y }, { x: fwd ? c.x + W : c.x, y: y });
    });
    pts.push({ x: x3, y: pb });
    return pts;
  }

  // straight through a column, an S-curve with level ends in a gutter: arrows always arrive horizontally
  function straight(a, b) {  // a link the top-down layout did not rank: border to border, the shortest way
    if (b.y >= a.y + H) return [{ x: a.x + W / 2, y: a.y + H }, { x: b.x + W / 2, y: b.y }];
    if (b.y + H <= a.y) return [{ x: a.x + W / 2, y: a.y }, { x: b.x + W / 2, y: b.y + H }];
    return b.x > a.x ? [{ x: a.x + W, y: a.y + H / 2 }, { x: b.x, y: b.y + H / 2 }] : [{ x: a.x, y: a.y + H / 2 }, { x: b.x + W, y: b.y + H / 2 }];
  }

  function pathOf(pts) {
    var f = function (v) { return v.toFixed(1); }, d = "M" + f(pts[0].x) + "," + f(pts[0].y);
    for (var i = 1; i < pts.length; i++) {
      var p = pts[i - 1], q = pts[i], mx = f((p.x + q.x) / 2);
      d += Math.abs(p.y - q.y) < 0.5 ? " L" + f(q.x) + "," + f(q.y)
        : " C" + mx + "," + f(p.y) + " " + mx + "," + f(q.y) + " " + f(q.x) + "," + f(q.y);
    }
    return d;
  }

  // links meeting one side of a card get their own ports, ordered by where the other end sits
  function assignPorts(list) {
    var sides = {};
    list.forEach(function (r) {
      var out = r.e.from + (r.fwd ? "|R" : "|L"), inn = r.e.to + (r.fwd ? "|L" : "|R");
      (sides[out] = sides[out] || []).push({ r: r, end: "pa", box: r.a, other: r.b });
      (sides[inn] = sides[inn] || []).push({ r: r, end: "pb", box: r.b, other: r.a });
    });
    Object.keys(sides).forEach(function (k) {
      var arr = sides[k].sort(function (p, q) { return p.other.y - q.other.y || p.other.x - q.other.x; });
      var n = arr.length, step = n > 1 ? Math.min(9, (H - 22) / (n - 1)) : 0;
      arr.forEach(function (s, i) { s.r[s.end] = s.box.y + H / 2 + (i - (n - 1) / 2) * step; });
    });
  }

  // two cards in one column: loop out into the gutter on the right
  function sideLoop(a, b) {
    var ya = a.y + H / 2, yb = b.y + H / 2, x = Math.max(a.x, b.x) + W;
    return "M" + x + "," + ya + " C" + (x + 40) + "," + ya + " " + (x + 40) + "," + yb + " " + x + "," + yb;
  }

  function connector(a, b) {
    return Math.abs(a.x - b.x) <= 1 ? sideLoop(a, b) : pathOf(routePoints(a, b, a.y + H / 2, b.y + H / 2, null));
  }

  // where step k really comes from: the earlier step that calls it (check worked it out), else the one before
  function sourceStep(k) {
    var st = journey.steps[k];
    return journey.steps[st.linked !== false && st.from != null ? st.from : k - 1];
  }

  // numbered badges on the route's cards, and a dashed line where no import links two steps
  function drawJourney() {
    var old = document.getElementById("vlg-jlayer");
    if (old) old.parentNode.removeChild(old);
    if (!journey || !layout || seq) return;
    var layer = sv("g", { id: "vlg-jlayer" }), numbers = {}, order = [];
    journey.steps.forEach(function (st, k) {
      var v = visibleId(st.file);
      if (!numbers[v]) { numbers[v] = []; order.push(v); }
      numbers[v].push(k + 1);
      if (!k) return;
      var p = visibleId(sourceStep(k).file), a = layout.boxes[p], b = layout.boxes[v];
      if (p === v || !a || !b || layout.edges[p + "\u0001" + v] || layout.edges[v + "\u0001" + p]) return;
      layer.appendChild(sv("path", { "class": "vlg-jlink" + (st.linked === false ? " unlinked" : ""),
        d: connector(a, b), "marker-end": "url(#vlg-arrow-hot)" }));
    });
    order.forEach(function (v) {
      var b = layout.boxes[v];
      if (!b) return;
      var label = numbers[v].join("·"), w = Math.max(24, units(label) * 7 + 12);
      var g = sv("g", { "class": "vlg-jbadge", transform: "translate(" + (b.x - 6).toFixed(1) + "," + (b.y - 6).toFixed(1) + ")" });
      g.appendChild(sv("rect", { x: -w / 2, y: -12, width: w, height: 24, rx: 12 }));
      var tx = sv("text", { x: 0, y: 4.5, "text-anchor": "middle" });
      tx.textContent = label;
      g.appendChild(tx);
      layer.appendChild(g);
    });
    viewport.appendChild(layer);
  }

  function apply() {
    viewport.setAttribute("transform", "translate(" + view.x.toFixed(1) + "," + view.y.toFixed(1) + ") scale(" + view.s.toFixed(4) + ")");
  }

  function bbox() {
    if (seq && seqBox) return seqBox;
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    Object.keys(layout.boxes).forEach(function (k) {
      var b = layout.boxes[k];
      minX = Math.min(minX, b.x); minY = Math.min(minY, b.y); maxX = Math.max(maxX, b.x + W); maxY = Math.max(maxY, b.y + H);
    });
    if (minX === Infinity) return { x: 0, y: 0, w: 400, h: 300 };
    return { x: minX - 30, y: minY - 70, w: maxX - minX + 60, h: maxY - minY + 100 };
  }

  // The first view keeps cards readable and starts where reading starts (the entries, on the left);
  // the "fit" button shows the whole map however small it gets.
  function fit(whole) {
    var r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var b = bbox(), s = Math.min((r.width - 40) / b.w, (r.height - 40) / b.h, 1.25);
    s = Math.max(s, whole ? 0.15 : r.width < 560 ? 0.55 : areaMode() ? 0.6 : 0.7);
    var gw = b.w * s, gh = b.h * s;
    view.s = s;
    view.x = gw <= r.width ? (r.width - gw) / 2 - b.x * s : 12 - b.x * s;
    if (gh <= r.height) {
      view.y = (r.height - gh) / 2 - b.y * s;
    } else if (seq || (layout && layout.tb)) {
      view.y = 12 - b.y * s;  // a sequence reads from its top
    } else {
      var ys = data.entries.map(function (id) { return layout.boxes[visibleId(id)]; }).filter(Boolean)
        .map(function (e) { return e.y + H / 2; });
      var cy = ys.length ? ys.reduce(function (a, c) { return a + c; }, 0) / ys.length : b.y + b.h / 2;
      view.y = Math.min(12 - b.y * s, Math.max(r.height - 12 - (b.y + b.h) * s, r.height / 2 - cy * s));
    }
    apply();
    fitted = true;
  }

  function zoomTo(ns, cx, cy) {
    ns = Math.max(0.15, Math.min(3, ns));
    view.x = cx - (cx - view.x) * (ns / view.s);
    view.y = cy - (cy - view.y) * (ns / view.s);
    view.s = ns;
    apply();
  }

  function zoomBy(f) { var r = svg.getBoundingClientRect(); zoomTo(view.s * f, r.width / 2, r.height / 2); }

  function centerOn(id) {
    var b = layout.boxes[visibleId(id)], r = svg.getBoundingClientRect();
    if (!b || !r.width) return;
    view.x = r.width / 2 - (b.x + W / 2) * view.s;
    view.y = r.height / 2 - (b.y + H / 2) * view.s;
    apply();
  }

  function onNodeClick(vid) {
    if (isFolder(vid)) {
      expanded[vid.slice(7)] = true;
      draw();
      fit();
      return;
    }
    select(vid, false);
  }

  function select(id, center) {
    if (!byId[id]) return;
    leaveSequence();
    if (!inView(id)) setMode(BASE);  // a file the data view leaves out opens where it is drawn
    if (visibleId(id) !== id) { expanded[folderOf[id]] = true; draw(); }
    journey = null;
    selected = id;
    applySelection();
    renderPanel();
    if (center) centerOn(id);
  }

  function clearSelection() { leaveSequence(); selected = null; journey = null; applySelection(); renderPanel(); }

  function openJourney(id) {
    var j = journeyById[id];
    if (!j) return;
    leaveSequence();
    if (j.steps.some(function (st) { return !inView(st.file); })) setMode(BASE);
    var grew = false;
    j.steps.forEach(function (st) {
      var f = folderOf[st.file];
      if (grouped && f && !expanded[f]) { expanded[f] = true; grew = true; }
    });
    if (grew) draw();
    selected = null;
    journey = j;
    applySelection();
    renderPanel();
    focusJourney();
  }

  // show the whole route, as large as fits, without going below a readable size
  function focusJourney() {
    var r = svg.getBoundingClientRect();
    var list = journey.steps.map(function (st) { return layout.boxes[visibleId(st.file)]; }).filter(Boolean);
    if (!r.width || !list.length) return;
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    list.forEach(function (b) {
      minX = Math.min(minX, b.x); minY = Math.min(minY, b.y); maxX = Math.max(maxX, b.x + W); maxY = Math.max(maxY, b.y + H);
    });
    var w = maxX - minX + 80, h = maxY - minY + 80;
    var fit = Math.min((r.width - 40) / w, (r.height - 40) / h, 1.1), floor = r.width < 560 ? 0.45 : 0.55;
    var s = Math.max(fit, floor);
    view.s = s;
    if (fit >= floor) {
      view.x = r.width / 2 - (minX + maxX) / 2 * s;
      view.y = r.height / 2 - (minY + maxY) / 2 * s;
    } else {
      // the route is wider or taller than the screen at a readable size: centring the whole route
      // would show the empty middle of a big folder, so start where the route starts
      var first = list[0];
      view.x = 40 - first.x * s;
      view.y = r.height / 2 - (first.y + H / 2) * s;
    }
    apply();
  }
  function chip(id) {
    var n = byId[id], b = el("button", "vlg-chip r-" + (n ? n.role : "logic"), n ? n.label : id);
    b.type = "button";
    b.title = id;
    b.addEventListener("click", function () { select(id, true); });
    return b;
  }

  function section(title) {
    var s = el("div", "vlg-sec");
    s.appendChild(el("h3", null, title));
    panel.appendChild(s);
    return s;
  }

  // in the developer view each linked file is a row with the names that link imports
  function namedChips(parent, ids, names, dev) {
    if (!dev) { chips(parent, ids); return; }
    ids.forEach(function (id) {
      var row = el("div", "vlg-namerow"), ns = (names || {})[id];
      row.appendChild(chip(id));
      if (ns && ns.length) row.appendChild(el("span", "vlg-names", ns.join(", ")));
      parent.appendChild(row);
    });
  }

  function chips(parent, ids) {
    var box = el("div", "vlg-chips");
    ids.forEach(function (id) { box.appendChild(chip(id)); });
    parent.appendChild(box);
  }

  // ---- the sequence view of a route: one lifeline for you and for each file, the steps as messages top to bottom ----
  function fitText(s, max) {
    if (units(s) <= max) return s;
    var out = "", n = 0;
    for (var i = 0; i < s.length && n < max - 1; i++) { n += s.charCodeAt(i) > 0x2e80 ? 2 : 1; out += s[i]; }
    return out + "\u2026";
  }

  function drawSequence() {
    while (viewport.firstChild) viewport.removeChild(viewport.firstChild);
    var actors = [{ id: "__you", label: S.g_seq_you }], index = { __you: 0 };
    journey.steps.forEach(function (st) {
      if (index[st.file] == null) { index[st.file] = actors.length; actors.push({ id: st.file, label: (byId[st.file] || {}).label || st.file }); }
    });
    var CW = 250, HW = 190, HH = 50, Y0 = 100, RH = 74, n = journey.steps.length;
    var bottom = Y0 + (n + (journey.outcome ? 1 : 0)) * RH;
    var g = sv("g", { "class": "vlg-seq" });
    var x = function (id) { return index[id] * CW + HW / 2; };
    actors.forEach(function (a, i) {
      g.appendChild(sv("line", { "class": "vlg-lifeline", x1: i * CW + HW / 2, y1: HH, x2: i * CW + HW / 2, y2: bottom }));
      var box = sv("g", { "class": "vlg-seq-actor" + (a.id === "__you" ? " you" : " r-" + roleOf(a.id)),
        transform: "translate(" + i * CW + ",0)", "data-id": a.id });
      box.appendChild(sv("rect", { width: HW, height: HH, rx: 12 }));
      var t = sv("text", { x: HW / 2, y: HH / 2 + 5, "text-anchor": "middle" });
      t.textContent = fitText(a.label, 24);
      box.appendChild(t);
      if (a.id !== "__you") box.addEventListener("click", function (ev) { ev.stopPropagation(); select(a.id, true); });
      g.appendChild(box);
    });
    journey.steps.forEach(function (st, k) {
      var from = k ? sourceStep(k).file : "__you";
      g.appendChild(message(x(from), x(st.file), Y0 + k * RH, k + 1, st.plain, k > 0 && st.linked === false, false));
    });
    if (journey.outcome) {
      g.appendChild(message(x(journey.steps[n - 1].file), x("__you"), Y0 + n * RH, null, journey.outcome, false, true));
    }
    viewport.appendChild(g);
    seqBox = { x: -30, y: -30, w: actors.length * CW + 60, h: bottom + 60 };
    document.body.setAttribute("data-layout", "done");
  }

  // one step: an arrow between two lifelines (a small loop when a file calls itself), its number and its sentence
  function message(x1, x2, y, num, text, unlinked, reply) {
    var g = sv("g", { "class": "vlg-msg" + (unlinked ? " unlinked" : "") + (reply ? " reply" : "") }), d, tx, anchor;
    if (x1 === x2) {
      d = "M" + x1 + "," + (y - 9) + " h44 v18 h-38";
      tx = x1 + 54; anchor = "start";
    } else {
      d = "M" + x1 + "," + y + " L" + (x2 + (x2 > x1 ? -4 : 4)) + "," + y;
      tx = (x1 + x2) / 2; anchor = "middle";
    }
    g.appendChild(sv("path", { "class": "vlg-msg-line", d: d, "marker-end": "url(#vlg-arrow-hot)" }));
    var room = x1 === x2 ? 34 : Math.max(16, Math.floor(Math.abs(x2 - x1) / 7.5) - 4);
    var t = sv("text", { "class": "vlg-msg-text", x: tx, y: x1 === x2 ? y + 4 : y - 9, "text-anchor": anchor });
    t.textContent = fitText(text, room);
    var full = sv("title", {});
    full.textContent = text;
    t.appendChild(full);
    g.appendChild(t);
    if (num != null) {
      var bx = x1 + (x2 >= x1 ? 16 : -16);
      g.appendChild(sv("circle", { "class": "vlg-msg-n", cx: bx, cy: y, r: 10 }));
      var nt = sv("text", { "class": "vlg-msg-num", x: bx, y: y + 4, "text-anchor": "middle" });
      nt.textContent = String(num);
      g.appendChild(nt);
    }
    return g;
  }

  function enterSequence() {
    seq = true;
    drawSequence();
    fit();  // readable first, from the left, like the flowchart; "fit" shows the whole sequence
    renderPanel();
  }

  function leaveSequence() {
    if (!seq) return;
    seq = false;
    seqBox = null;
    draw();
  }

  function setMode(m) {
    leaveSequence();
    mode = m;
    selected = null;
    journey = null;
    if (AREAS && (m === "map" || m === "data")) setGroups(data.areas, true);
    else if (m === "modules") setGroups(data.modules || [], true);
    else setGroups(data.folders, data.collapsed);
    document.querySelectorAll(".vlg-modes [data-mode]").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-mode") === m); });
    document.querySelectorAll('.vlg-tools [data-act="expand-all"], .vlg-tools [data-act="collapse-all"]').forEach(function (b) { b.hidden = !grouped; });
    draw();
    fit();
    renderPanel();
  }

  function renderJourney() {
    var dev = document.body.classList.contains("dev"), back = el("button", "vlg-close", "×");
    back.type = "button";
    back.title = S.g_back;
    back.addEventListener("click", clearSelection);
    panel.appendChild(back);
    panel.appendChild(el("div", "vlg-path", S.g_journeys));
    panel.appendChild(el("h2", null, journey.title));
    var sw = el("div", "vlg-seg");
    [[false, S.g_seq_flow], [true, S.g_seq_seq]].forEach(function (o) {
      var b = el("button", seq === o[0] ? "on" : "", o[1]);
      b.type = "button";
      b.addEventListener("click", function () { if (o[0] && !seq) enterSequence(); else if (!o[0] && seq) { leaveSequence(); focusJourney(); renderPanel(); } });
      sw.appendChild(b);
    });
    panel.appendChild(sw);
    var ol = el("ol", "vlg-steps");
    journey.steps.forEach(function (st, k) {
      var li = el("li", "vlg-step"), head = el("div", "vlg-step-head");
      head.appendChild(el("span", "vlg-step-n", String(k + 1)));
      head.appendChild(chip(st.file));
      li.appendChild(head);
      li.appendChild(el("p", "vlg-step-text", st.plain));
      if (dev && st.function) li.appendChild(el("code", "vlg-step-fn", st.function + ":" + st.line));
      if (k && st.linked === false) li.appendChild(el("p", "vlg-warnnote", S.g_unlinked));
      ol.appendChild(li);
    });
    panel.appendChild(ol);
    if (journey.outcome) panel.appendChild(el("p", "vlg-outcome", fmt(S.g_journey_outcome, { outcome: journey.outcome })));
  }

  function journeyButton(j, cls, text) {
    var b = el("button", cls);
    b.type = "button";
    b.appendChild(el("span", null, text));
    b.addEventListener("click", function () { openJourney(j.id); });
    return b;
  }

  function renderDiff() {
    var dd = data.diff, sec = section(dd.title);
    sec.appendChild(el("p", null, dd.counts_text));
    if (!dd.sha_known) sec.appendChild(el("p", "vlg-muted", S.g_diff_sha_unknown));
    if (dd.services) sec.appendChild(el("p", null, dd.services));
    if (dd.quiet) { sec.appendChild(el("p", "vlg-ok", S.g_diff_nothing)); return; }
    var toggle = el("button", "vlg-chip" + (compare ? " on" : ""), S.g_compare);
    toggle.type = "button";
    toggle.addEventListener("click", function () { setCompare(!compare); });
    sec.appendChild(toggle);
    if (dd.removed.length) {
      sec.appendChild(el("h4", null, S.g_diff_removed));
      dd.removed.forEach(function (p) { sec.appendChild(el("div", "vlg-path vlg-gone", p)); });
    }
    [["new_risks", S.g_diff_new_risks, ""], ["resolved_risks", S.g_diff_resolved, " resolved"]].forEach(function (k) {
      if (!dd[k[0]].length) return;
      sec.appendChild(el("h4", null, k[1]));
      dd[k[0]].forEach(function (r) {
        var row = el("div", "vlg-risk " + r.level + k[2], r.text);
        row.appendChild(el("div", "vlg-path", r.path));
        sec.appendChild(row);
      });
    });
    if (dd.promises.length) {
      sec.appendChild(el("h4", null, S.g_diff_promises));
      dd.promises.forEach(function (line) { sec.appendChild(el("div", "vlg-promise", line)); });
    }
  }

  function setCompare(on) {
    leaveSequence();
    compare = on;
    selected = null;
    journey = null;
    document.querySelectorAll('.vlg-tools [data-act="compare"]').forEach(function (b) { b.classList.toggle("on", on); });
    var legend = document.querySelector(".vlg-legend"), item = document.getElementById("vlg-legend-diff");
    if (on && legend && !item) { item = el("span", "vlg-legend-item k-diff", S.g_diff_legend); item.id = "vlg-legend-diff"; legend.appendChild(item); }
    if (!on && item) item.parentNode.removeChild(item);
    applySelection();
    renderPanel();
  }

  function renderOverview() {
    if (!data.nodes.some(function (n) { return !isExt(n.id); })) panel.appendChild(el("p", "vlg-warnnote", S.g_no_files));
    if (mode === "modules") panel.appendChild(el("p", "vlg-modehint", S.g_modules_hint));
    if (AREAS && mode === "map") panel.appendChild(el("p", "vlg-modehint", S.g_map_hint));
    else if (AREAS && mode === "data") panel.appendChild(el("p", "vlg-modehint", data.flow.items.length ? S.g_flow_hint : S.g_flow_empty));
    else if (mode === "data") panel.appendChild(el("p", "vlg-modehint", (data.data_flow.files || []).length ? S.g_data_hint : S.g_data_empty));
    panel.appendChild(el("p", "vlg-purpose", data.summary));
    if (!AREAS) {  // the folder chart's reading guide; the map's own hint above replaces it
      var ul = el("ul", "vlg-howto");
      data.howto.forEach(function (line) { ul.appendChild(el("li", null, line)); });
      panel.appendChild(ul);
    }
    if (AREAS) renderAreas();
    if (data.diff) renderDiff();
    if (data.requirements) {
      var rq = section(S.g_req_title);
      rq.appendChild(el("p", null, data.requirements.line));
      if (data.requirements.unaccounted) rq.appendChild(el("p", "vlg-warnnote", fmt(S.g_req_unaccounted, { n: data.requirements.unaccounted })));
      var open = el("button", "vlg-chip", S.g_req_open);
      open.type = "button";
      open.addEventListener("click", function () { showTab("requirements"); });
      rq.appendChild(open);
    }
    if (data.journeys && data.journeys.length) {
      var js = section(S.g_journeys);
      data.journeys.forEach(function (j) {
        var b = journeyButton(j, "vlg-journey-btn", j.title);
        b.appendChild(el("span", "vlg-top-badge", fmt(S.g_journey_steps, { n: j.steps.length })));
        js.appendChild(b);
      });
    }
    var sec = section(S.g_top);
    if (!data.top.length) { sec.appendChild(el("p", "vlg-ok", S.g_no_problems)); return; }
    data.top.forEach(function (id) {
      var n = byId[id], b = el("button", "vlg-top-item s-" + n.state);
      b.type = "button";
      b.appendChild(el("span", null, n.label));
      b.appendChild(el("span", "vlg-top-badge", n.badge));
      b.addEventListener("click", function () { select(id, true); });
      sec.appendChild(b);
    });
  }

  function renderAreas() {
    var sec = section(S.g_areas_title);
    data.areas.forEach(function (a) {
      var b = el("button", "vlg-area-row s-" + a.state);
      b.type = "button";
      var head = el("div", "vlg-area-head");
      head.appendChild(el("b", null, a.label));
      head.appendChild(el("span", "vlg-top-badge", a.badge || fmt(S.g_area_row, { n: a.count })));
      b.appendChild(head);
      b.appendChild(el("div", "vlg-area-plain", a.plain));
      var io = (data.area_io || {})[a.id];
      if (io) {
        [["writes", S.g_area_writes], ["reads", S.g_area_reads], ["calls", S.g_area_calls]].forEach(function (k) {
          if (io[k[0]].length) b.appendChild(el("div", "vlg-area-io", fmt(k[1], { names: io[k[0]].join("、") })));
        });
      }
      b.addEventListener("click", function () {  // open this part in the map, in place
        if (mode !== "map") setMode("map");
        expanded[a.id] = true;
        draw();
        var ids = a.files.map(function (f) { return layout.boxes[f]; }).filter(Boolean);
        if (ids.length) centerOn(ids[0].id); else fit();
      });
      sec.appendChild(b);
    });
  }

  function renderItem() {
    var it = byId[selected], close = el("button", "vlg-close", "×");
    close.type = "button";
    close.title = S.g_close;
    close.addEventListener("click", clearSelection);
    panel.appendChild(close);
    panel.appendChild(el("h2", null, it.label));
    panel.appendChild(el("span", "vlg-role r-item", S.g_role_item + " · " + it.kind));
    if (it.plain) panel.appendChild(el("p", "vlg-purpose", it.plain));
    [["writes", S.g_item_writes], ["reads", S.g_item_reads]].forEach(function (k) {
      var sec = section(k[1]);
      if (!it[k[0]].length) sec.appendChild(el("p", "vlg-muted", S.g_item_none));
      it[k[0]].forEach(function (x) {
        var row = el("details", "vlg-fn");
        var sum = el("summary");
        sum.appendChild(el("b", null, x.area + " "));
        sum.appendChild(el("code", null, x.where));
        row.appendChild(sum);
        row.appendChild(el("pre", null, x.code));
        sec.appendChild(row);
      });
    });
  }

  function renderPanel() {
    while (panel.firstChild) panel.removeChild(panel.firstChild);
    if (journey) { renderJourney(); return; }
    if (!selected) { renderOverview(); return; }
    if (isItem(selected)) { renderItem(); return; }
    var c = byId[selected].card, dev = document.body.classList.contains("dev");
    var close = el("button", "vlg-close", "×");
    close.type = "button";
    close.title = S.g_close;
    close.addEventListener("click", clearSelection);
    panel.appendChild(close);
    if (c.folder) panel.appendChild(el("div", "vlg-path", c.folder + "/"));
    panel.appendChild(el("h2", null, c.label));
    if (dev && !isExt(selected)) {
      panel.appendChild(el("div", "vlg-devmeta", c.path + " · " + c.lines + " · " + fmt(S.g_exports_n, { n: c.exports.length })));
    }
    panel.appendChild(el("span", "vlg-role r-" + c.role, c.role_label));
    if (c.area) panel.appendChild(el("p", "vlg-area-of", fmt(S.g_area_of, { name: c.area.name, plain: c.area.plain })));
    if (isExt(selected)) {
      panel.appendChild(el("p", "vlg-purpose", c.auto));
      if (c.called_by.length) chips(section(S.g_called_by), c.called_by);
      var evs = section(S.g_where);
      c.evidence.forEach(function (e) {
        evs.appendChild(el("div", "vlg-path", e.where));
        if (dev) evs.appendChild(el("pre", null, e.code));
      });
      return;
    }
    if (c.explained) {
      panel.appendChild(el("p", "vlg-purpose", c.purpose_plain));
      if (c.purpose_unverified) panel.appendChild(el("p", "vlg-warnnote", c.unverified_note));
      if (dev && c.purpose_dev) {
        var note = el("div", "vlg-devnote");
        note.appendChild(el("div", "vlg-devnote-k", S.g_dev_note));
        note.appendChild(el("p", null, c.purpose_dev));
        panel.appendChild(note);
      }
    } else {
      panel.appendChild(el("p", "vlg-muted", S.g_no_explain));
      panel.appendChild(el("p", "vlg-purpose", c.auto));
    }
    if (c.diff_notes && c.diff_notes.length) {
      var dn = el("div", "vlg-diffnotes");
      c.diff_notes.forEach(function (line) { dn.appendChild(el("p", null, line)); });
      panel.appendChild(dn);
    }
    if (data.has_journeys) {
      var pos = section(S.g_position);
      if (!c.positions.length) pos.appendChild(el("p", "vlg-muted", S.g_position_none));
      c.positions.forEach(function (p) { pos.appendChild(journeyButton(journeyById[p.journey], "vlg-pos", p.text)); });
    }
    if (c.calls.length) namedChips(section(S.g_calls), c.calls, c.call_names, dev);
    if (c.called_by.length) namedChips(section(S.g_called_by), c.called_by, c.caller_names, dev);
    if (c.functions.length) {
      var fs = section(S.g_functions);
      c.functions.forEach(function (f) {
        var snip = dev ? c.snippets.filter(function (s) { return s.name === f.name; })[0] : null;
        var row = el(snip ? "details" : "div", "vlg-fn"), head = snip ? el("summary") : row;  // code unfolds on demand
        head.appendChild(el("code", null, f.name + (dev ? ":" + f.line : "")));
        head.appendChild(document.createTextNode(" " + f.plain));
        if (snip) { row.appendChild(head); row.appendChild(el("pre", null, snip.code)); }
        fs.appendChild(row);
      });
    } else if (c.exports.length) {
      var ex = section(S.g_exports), box = el("div", "vlg-chips");
      c.exports.forEach(function (x) { box.appendChild(el("code", "vlg-export", x.name + (dev ? ":" + x.line : ""))); });
      ex.appendChild(box);
    }
    var rs = section(S.g_risks);
    if (!c.risks.length) rs.appendChild(el("p", "vlg-ok", "✅ " + S.g_no_risks));
    c.risks.forEach(function (r) {
      var row = el("details", "vlg-risk " + r.level);  // the evidence opens on click
      row.appendChild(el("summary", null, r.text));
      row.appendChild(el("div", "vlg-path", r.where));
      rs.appendChild(row);
    });
    if (c.promises.length) {
      var ps = section(S.g_promises);
      c.promises.forEach(function (p) {
        var row = el("div", "vlg-promise", p.glyph + " " + p.plain + " ");
        var a = el("a", null, S.g_in_overview);
        a.href = "#" + p.id;
        a.addEventListener("click", function () { showTab("overview"); });
        row.appendChild(a);
        ps.appendChild(row);
      });
    }
    if (c.requirements && c.requirements.length) {
      var qs = section(S.g_requirements);
      c.requirements.forEach(function (q) {
        var row = el("div", "vlg-promise", q.glyph + " " + q.plain + " ");
        var a = el("a", null, S.g_req_open);
        a.href = "#" + q.id;
        a.addEventListener("click", function () { showTab("requirements"); });
        row.appendChild(a);
        qs.appendChild(row);
      });
    }
    var hs = section(S.g_history);
    if (c.history.length) {
      c.history.forEach(function (item) {
        hs.appendChild(el("div", null, item.plain + (item.date ? " · " + item.date : "")));
        if (item.quote) hs.appendChild(el("blockquote", null, item.quote));
      });
    } else {
      hs.appendChild(el("p", "vlg-muted", c.history_note));
    }
    if (c.edits) hs.appendChild(el("p", "vlg-muted", c.edits));
    if (grouped && folderOf[selected] && expanded[folderOf[selected]]) {
      var fold = el("button", "vlg-chip", S.g_collapse);
      fold.type = "button";
      fold.addEventListener("click", function () {
        delete expanded[folderOf[selected]];
        selected = null;
        draw();
        fit();
        renderPanel();
      });
      panel.appendChild(fold);
    }
  }

  // ---- export: the whole map (not only what is on screen) in its current state, as SVG or a 2x PNG ----
  function exportSvg() {
    var b = bbox(), pad = 24, x = b.x - pad, y = b.y - pad, w = b.w + 2 * pad, h = b.h + 2 * pad;
    var clone = viewport.cloneNode(true), src = viewport.querySelectorAll("*"), dst = clone.querySelectorAll("*");
    clone.removeAttribute("transform");
    clone.removeAttribute("id");
    for (var i = src.length - 1; i >= 0; i--) {  // leave out what the page does not show (hidden labels)
      if (getComputedStyle(src[i]).display === "none" && dst[i].parentNode) dst[i].parentNode.removeChild(dst[i]);
    }
    var out = sv("svg", { xmlns: NS, id: "tab-graph", viewBox: [x, y, w, h].map(function (v) { return v.toFixed(1); }).join(" "),
      width: Math.round(w), height: Math.round(h), style: "font-family:" + getComputedStyle(svg).fontFamily });
    var style = document.createElementNS(NS, "style");
    style.textContent = Array.prototype.map.call(document.querySelectorAll("head style"), function (s) { return s.textContent; }).join("\n");
    out.appendChild(style);
    out.appendChild(svg.querySelector("defs").cloneNode(true));
    out.appendChild(sv("rect", { "class": "vlg-bg", x: x, y: y, width: w, height: h, fill: "#131317" }));
    out.appendChild(clone);
    return new XMLSerializer().serializeToString(out);
  }

  function exportPng(done) {
    var text = exportSvg(), b = bbox(), w = b.w + 48, h = b.h + 48;
    var k = Math.min(2, 16000 / Math.max(w, h));  // sharp, but inside the browser's canvas limits
    var url = URL.createObjectURL(new Blob([text], { type: "image/svg+xml" })), img = new Image();
    img.onload = function () {
      var c = document.createElement("canvas");
      c.width = Math.round(w * k);
      c.height = Math.round(h * k);
      var ctx = c.getContext("2d");
      ctx.scale(k, k);
      ctx.drawImage(img, 0, 0, w, h);
      URL.revokeObjectURL(url);
      c.toBlob(done, "image/png");
    };
    img.onerror = function () { URL.revokeObjectURL(url); done(null); };
    img.src = url;
  }

  function fileName(ext) {
    return (data.project || "vibe-ledger").replace(/[\\/:*?"<>|]/g, "_") + "-" + S.g_export_name + "." + ext;
  }

  function download(blob, ext) {
    if (!blob) return;
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = fileName(ext);
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.parentNode.removeChild(a); }, 1000);
  }

  window.vibeLedger = { exportSvg: exportSvg, exportPng: exportPng, fileName: fileName };

  function showTab(name) {
    document.querySelectorAll(".vl-tab").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-tab") === name); });
    document.querySelectorAll(".vl-tabpanel").forEach(function (p) { p.hidden = p.id !== "tab-" + name; });
    if (name === "graph" && !fitted) fit();
  }

  function findNode(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return null;
    var exact = data.nodes.filter(function (n) { return n.id.toLowerCase() === q || n.label.toLowerCase() === q; })[0];
    return exact || data.nodes.filter(function (n) {
      return n.id.toLowerCase().indexOf(q) >= 0 || n.label.toLowerCase().indexOf(q) >= 0;
    })[0] || null;
  }

  function wire() {
    var defs = sv("defs", {});
    [["vlg-arrow", ""], ["vlg-arrow-risky", " risky"], ["vlg-arrow-hot", " hot"]].forEach(function (m) {
      var mk = sv("marker", { id: m[0], viewBox: "0 0 8 8", refX: 7, refY: 4, markerWidth: 6, markerHeight: 6, orient: "auto" });
      mk.appendChild(sv("path", { d: "M0,0 L8,4 L0,8 z", "class": "vlg-arrow" + m[1] }));
      defs.appendChild(mk);
    });
    svg.insertBefore(defs, viewport);
    svg.addEventListener("pointerdown", function (ev) {
      pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      moved = false;
      var ids = Object.keys(pointers);
      if (ids.length === 1) drag = { x: ev.clientX, y: ev.clientY, vx: view.x, vy: view.y };
      else if (ids.length === 2) {
        var a = pointers[ids[0]], b = pointers[ids[1]];
        pinch = { d: dist(a, b) || 1, s: view.s, cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2 };
        drag = null;
      }
    });
    window.addEventListener("pointermove", function (ev) {
      if (!pointers[ev.pointerId]) return;
      pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      var ids = Object.keys(pointers);
      if (pinch && ids.length === 2) {
        var a = pointers[ids[0]], b = pointers[ids[1]], r = svg.getBoundingClientRect();
        zoomTo(pinch.s * dist(a, b) / pinch.d, pinch.cx - r.left, pinch.cy - r.top);
        moved = true;
      } else if (drag) {
        var dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
        if (Math.abs(dx) + Math.abs(dy) > 4) moved = true;
        view.x = drag.vx + dx;
        view.y = drag.vy + dy;
        apply();
      }
    });
    function end(ev) {
      delete pointers[ev.pointerId];
      if (Object.keys(pointers).length < 2) pinch = null;
      if (!Object.keys(pointers).length) drag = null;
    }
    window.addEventListener("pointerup", end);
    window.addEventListener("pointercancel", end);
    svg.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var r = svg.getBoundingClientRect();
      zoomTo(view.s * (ev.deltaY < 0 ? 1.12 : 1 / 1.12), ev.clientX - r.left, ev.clientY - r.top);
    }, { passive: false });
    svg.addEventListener("click", function (ev) { if (!moved && !ev.target.closest(".vlg-node")) clearSelection(); });
    document.querySelectorAll(".vlg-tools [data-act]").forEach(function (b) {
      var act = b.getAttribute("data-act");
      if (act === "expand-all" || act === "collapse-all") b.hidden = !grouped;
      if (act === "compare") b.hidden = !data.diff || data.diff.quiet;
      b.addEventListener("click", function () {
        if (act === "compare") { setCompare(!compare); return; }
        if (act === "export") { var m = document.querySelector(".vlg-export-menu"); m.hidden = !m.hidden; return; }
        if (act === "zoom-in") zoomBy(1.2);
        else if (act === "zoom-out") zoomBy(1 / 1.2);
        else if (act === "fit") fit(true);
        else if (act === "expand-all") { groups.forEach(function (f) { expanded[f.id] = true; }); draw(); fit(); }
        else if (act === "collapse-all") {
          expanded = {};
          if (selected && folderOf[selected]) selected = null;
          draw();
          fit();
          renderPanel();
        }
      });
    });
    document.querySelectorAll(".vl-tab").forEach(function (b) {
      b.addEventListener("click", function () { showTab(b.getAttribute("data-tab")); });
    });
    document.querySelectorAll(".req-file").forEach(function (b) {  // a file named under a requirement opens it in the flowchart
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-file");
        if (!byId[id]) return;
        showTab("graph");
        select(id, true);
      });
    });
    var search = document.getElementById("vlg-search"), list = document.getElementById("vlg-files");
    if (list) data.nodes.forEach(function (n) { var o = document.createElement("option"); o.value = isExt(n.id) ? n.label : n.id; list.appendChild(o); });
    if (search) {
      var go = function () { var n = findNode(search.value); if (n) { showTab("graph"); select(n.id, true); } };
      search.addEventListener("change", go);
      search.addEventListener("keydown", function (ev) { if (ev.key === "Enter") go(); });
    }
    document.querySelectorAll(".vlg-modes [data-mode]").forEach(function (b) {
      b.addEventListener("click", function () { setMode(b.getAttribute("data-mode")); });
    });
    document.querySelectorAll(".vlg-export-menu [data-fmt]").forEach(function (b) {
      b.addEventListener("click", function () {
        var fmt = b.getAttribute("data-fmt");
        b.parentNode.hidden = true;
        if (fmt === "svg") download(new Blob([exportSvg()], { type: "image/svg+xml" }), "svg");
        else exportPng(function (blob) { download(blob, "png"); });
      });
    });
    var toggle = document.getElementById("view-toggle");
    if (toggle) toggle.addEventListener("click", function () { setTimeout(renderPanel, 0); });
    document.addEventListener("keydown", function (ev) {
      // Esc while typing (the search box) only leaves the field; elsewhere it closes the file or route
      if (ev.key === "Escape" && !/^(INPUT|TEXTAREA|SELECT)$/.test((ev.target && ev.target.tagName) || "")) clearSelection();
    });
    window.addEventListener("resize", function () {
      if (!fitted) return;
      fit();
      if (seq) fit();
      else if (journey) focusJourney();
      else if (selected) centerOn(selected);  // a resize must not lose the file being read
    });
  }

  wire();
  draw();
  var params = new URLSearchParams(location.search);
  var wantTab = params.get("tab");
  showTab(wantTab && document.getElementById("tab-" + wantTab) && wantTab !== "graph" ? wantTab : "graph");
  var want = params.get("select"), wantJourney = params.get("journey");
  var wantMode = params.get("mode");
  if (AREAS ? (wantMode === "data") : (wantMode === "modules" || wantMode === "data")) setMode(wantMode);
  if (params.get("compare") === "1" && data.diff) setCompare(true);
  if (wantJourney && journeyById[wantJourney]) { openJourney(wantJourney); if (params.get("seq") === "1") enterSequence(); }
  else if (want && byId[want]) select(want, true);
  else renderPanel();
})();
