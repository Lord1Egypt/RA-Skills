/* engine.js — 灵根计分引擎（JS 版，与 linggen.py 同源，--verify 对拍） */
(function (global) {
  "use strict";
  var FIVE = ["metal", "wood", "water", "fire", "earth"];

  function crc32(str) {
    var table = [];
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      table[n] = c >>> 0;
    }
    var crc = 0xFFFFFFFF;
    var bytes = unescape(encodeURIComponent(str));
    for (var i = 0; i < bytes.length; i++)
      crc = table[(crc ^ bytes.charCodeAt(i)) & 0xFF] ^ (crc >>> 8);
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }

  function rhu(x) { return Math.floor(x + 0.5); }

  function isShengPair(attrs, a, b) {
    return attrs.sheng_ring.some(function (p) {
      return (p[0] === a && p[1] === b) || (p[0] === b && p[1] === a);
    });
  }

  function mutKey(attrs, a, b) {
    for (var k in attrs.mutations) {
      var p = attrs.mutations[k].pair;
      if ((p[0] === a && p[1] === b) || (p[0] === b && p[1] === a)) return k;
    }
    return null;
  }

  function grade(scores, data) {
    var tie = data.meta.tie_break;
    var ranked = FIVE.slice().sort(function (a, b) {
      return (scores[b] - scores[a]) || (tie.indexOf(a) - tie.indexOf(b));
    });
    var s1 = scores[ranked[0]], s2 = scores[ranked[1]], s3 = scores[ranked[2]] || 0;
    var m = data.meta.mutation;
    if (s1 >= m.min_top && s2 >= m.min_top && s1 - s2 <= m.max_gap &&
        s2 - s3 >= m.min_lead && isShengPair(data.attrs, ranked[0], ranked[1])) {
      return { tier: "mutation", mutation: mutKey(data.attrs, ranked[0], ranked[1]),
               passed: [ranked[0], ranked[1]], main: ranked[0], scores: scores };
    }
    var passed = FIVE.filter(function (a) { return scores[a] >= data.meta.attr_threshold; });
    var top = scores[ranked[0]];
    if (top > 0) {
      FIVE.forEach(function (a) {
        if (scores[a] >= data.meta.fallback_ratio * top && passed.indexOf(a) < 0) passed.push(a);
      });
    }
    if (!passed.length) passed = [ranked[0]];
    var n = Math.min(passed.length, 5);
    var main = passed.slice().sort(function (a, b) {
      return (scores[b] - scores[a]) || (tie.indexOf(a) - tie.indexOf(b));
    })[0];
    return { tier: data.meta.tier_keys_by_n[String(n)], mutation: null,
             passed: passed, main: main, scores: scores };
  }

  function compute(data, letters, paperNo, configName) {
    configName = configName || "alt";
    var paper = data.papers.papers[paperNo - 1];
    var qmap = {};
    data.questions.questions.forEach(function (q) { qmap[q.id] = q; });
    var raw = { metal: 0, wood: 0, water: 0, fire: 0, earth: 0 };
    var answers = [];
    for (var i = 0; i < letters.length && i < 8; i++) {
      var qid = paper.order[i];
      var oid = paper.opt_orders[qid]["ABC".indexOf(letters[i])];
      answers.push({ qid: qid, oid: oid });
    }
    answers.forEach(function (a) {
      var opt = qmap[a.qid].options.filter(function (o) { return o.id === a.oid; })[0];
      for (var k in opt.weights) raw[k] += opt.weights[k];
    });
    var cap = 8 * data.questions.max_weight;
    var scores = {};
    FIVE.forEach(function (a) { scores[a] = raw[a] / cap; });
    var g = grade(scores, data);
    var tier = data.tiers.tiers[g.tier];
    var attrs = data.attrs, meta = data.meta;
    var verse, qualityChar, qIndex, qualityName, displayAttrs, sects;
    if (g.mutation) {
      verse = tier.verse[configName];
      var mut = attrs.mutations[g.mutation];
      qualityChar = meta.quality_chars[g.mutation];
      qIndex = meta.quality_index[g.mutation];
      qualityName = "变异灵根";
      displayAttrs = [mut.name];
      var sectOrder = FIVE.map(function (a) { return attrs.attributes[a].sect; });
      sects = [mut.sect].concat(mut.pair.map(function (p) {
        return attrs.attributes[attrs.sheng_wo[p]].sect;
      })).sort(function (x, y) { return sectOrder.indexOf(x) - sectOrder.indexOf(y); });
    } else {
      verse = tier.verse[configName];
      qualityChar = tier.quality_char;
      qIndex = tier.index;
      qualityName = (g.tier === "quad") ? "四灵根" : (g.tier === "full") ? "五行俱全" : tier.name;
      displayAttrs = FIVE.filter(function (a) { return g.passed.indexOf(a) >= 0; })
                         .map(function (a) { return attrs.attributes[a].name; });
      var mainSect = attrs.attributes[g.main].sect;
      sects = [mainSect,
               attrs.attributes[attrs.sheng_wo[g.main]].sect,
               attrs.attributes[attrs.ke_wo[g.main]].sect];
    }
    var slots = FIVE.map(function (a) { return rhu(scores[a] * 9); });
    var checksum = (qIndex + slots.reduce(function (x, y) { return x + y; }, 0)) % 10;
    var talisman = qualityChar + "·" + slots.map(function (v) { return meta.stems[v]; }).join("") + "·" + meta.branches[checksum];
    var norm = talisman.replace(/·/g, "");
    var dao = meta.dao_prefix[crc32(norm) % meta.dao_prefix.length] +
              meta.dao_suffix[crc32(norm + "x") % meta.dao_suffix.length];
    return {
      tier_key: g.tier, mutation: g.mutation, main_attr: g.main,
      quality_name: qualityName, display_attrs: displayAttrs,
      attr_str: displayAttrs.join(""),
      verse: verse, sects: sects, speed: tier.speed,
      foundation: tier.foundation, core: tier.core,
      talisman: talisman, dao: dao, paper_id: paper.paper_id
    };
  }

  var api = { compute: compute, crc32: crc32, FIVE: FIVE };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else global.LingGenEngine = api;
})(typeof window !== "undefined" ? window : globalThis);
