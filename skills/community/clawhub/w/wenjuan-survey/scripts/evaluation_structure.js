"use strict";

const DEFAULT_EVALUATION_LABEL_DATA = {
  "1": { score_desc: "非常不满意", label_list: ["态度冷淡", "推销多", "技术差"] },
  "2": { score_desc: "比较不满意", label_list: ["速度慢", "仪表乱", "不专业"] },
  "3": { score_desc: "一般", label_list: ["无互动", "不积极", "业务不精"] },
  "4": { score_desc: "比较满意", label_list: ["文明礼貌", "速度快", "较专业"] },
  "5": { score_desc: "非常满意", label_list: ["热情好客", "敬业精神", "技能专业"] },
};

const STALE_EVAL_SCORE_DESCS = new Set(["很差", "差", "好", "很好"]);

function cloneEvaluationLabelData(source = DEFAULT_EVALUATION_LABEL_DATA) {
  const out = {};
  for (let i = 1; i <= 5; i += 1) {
    const key = String(i);
    const item = (source && source[key]) || DEFAULT_EVALUATION_LABEL_DATA[key];
    out[key] = {
      score_desc: String(item.score_desc || ""),
      label_list: Array.isArray(item.label_list) ? [...item.label_list] : [],
    };
  }
  return out;
}

function isIncompleteEvaluationLabelData(labelData) {
  if (!labelData || typeof labelData !== "object") return true;
  for (let i = 1; i <= 5; i += 1) {
    const item = labelData[String(i)];
    if (!item || typeof item !== "object") return true;
    if (!String(item.score_desc || "").trim()) return true;
    if (!Array.isArray(item.label_list) || item.label_list.length === 0) return true;
  }
  return false;
}

function resolveEvaluationLabelData(existing, scoreDescs) {
  const incoming = Array.isArray(scoreDescs)
    ? scoreDescs.map((s) => String(s).trim()).filter(Boolean)
    : [];
  const staleIncoming = incoming.length > 0 && STALE_EVAL_SCORE_DESCS.has(incoming[0]);

  if (!isIncompleteEvaluationLabelData(existing) && (incoming.length === 0 || staleIncoming)) {
    return cloneEvaluationLabelData(existing);
  }

  const base = cloneEvaluationLabelData();
  if (incoming.length > 0 && !staleIncoming) {
    incoming.slice(0, 5).forEach((desc, idx) => {
      base[String(idx + 1)].score_desc = desc;
    });
  }
  return base;
}

function applyEvaluationCustomAttr(customAttr = {}) {
  const next = { ...customAttr };
  next.disp_type = "evaluation";
  next.score_display = "star";
  next.open_eval = "on";
  next.min_answer_num = 1;
  next.max_answer_num = 5;
  next.show_seq = "off";
  next.base_on = next.base_on || "service";
  delete next.magnitude_scale;
  delete next.score_total;
  return next;
}

module.exports = {
  DEFAULT_EVALUATION_LABEL_DATA,
  cloneEvaluationLabelData,
  isIncompleteEvaluationLabelData,
  resolveEvaluationLabelData,
  applyEvaluationCustomAttr,
};
