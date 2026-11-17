"use strict";

function parseBound(v, fallback) {
  if (v == null || v === "") return fallback;
  const n = parseInt(String(v), 10);
  return Number.isFinite(n) ? n : fallback;
}

function plainTitle(value) {
  return String(value || "")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function matrixRowCount(question = {}) {
  return Array.isArray(question.matrixrow_list) ? question.matrixrow_list.length : 0;
}

function isScaleQuestionLike(question = {}, customAttr = {}) {
  const attr = customAttr && typeof customAttr === "object" ? customAttr : {};
  const disp = String(attr.disp_type || "").toLowerCase();
  if (disp === "evaluation" || disp === "nps_score") return false;
  if (disp === "scale") return true;
  if (attr.scale_tag != null && String(attr.scale_tag) !== "") return true;
  if (String(attr.score_display || "").toLowerCase() === "circle") return true;
  if (String(attr.desc_left || "").trim() && String(attr.desc_right || "").trim()) return true;

  const title = plainTitle(question.title);
  if (/量表题/.test(title)) return true;
  if (!/量表/.test(title)) return false;
  return matrixRowCount(question) < 2;
}

function applyScaleCustomAttr(customAttr = {}, optionList = []) {
  const next = { ...customAttr };
  next.scale_tag = parseBound(next.scale_tag, 2);
  next.score_display = next.score_display || "circle";
  next.min_answer_num = parseBound(next.min_answer_num, 1);
  next.max_answer_num = parseBound(next.max_answer_num, 5);
  if (next.max_answer_num <= next.min_answer_num) next.max_answer_num = 5;
  next.answer_score = next.answer_score || "off";
  next.magnitude_scale = parseBound(next.magnitude_scale, 1);
  next.disp_type = "scale";
  next.show_seq = "off";

  const titles = (Array.isArray(optionList) ? optionList : [])
    .map((opt) => String(opt?.title || "").trim())
    .filter((t) => t && t !== "选项1" && t !== "分数" && t !== "标签");
  if (!String(next.desc_left || "").trim()) {
    next.desc_left = titles[0] || "非常不满意";
  }
  if (!String(next.desc_right || "").trim()) {
    next.desc_right = titles.length >= 2 ? titles[titles.length - 1] : "非常满意";
  }
  delete next.open_eval;
  delete next.base_on;
  delete next.score_total;
  return next;
}

function buildScaleOptions(optionList = []) {
  const first = Array.isArray(optionList) && optionList.length === 1 ? optionList[0] : null;
  const title =
    first && String(first.title || "").trim() ? String(first.title).trim() : "选项1";
  return [
    {
      title,
      is_open: false,
      custom_attr: { ...(first?.custom_attr || {}) },
    },
  ];
}

module.exports = {
  isScaleQuestionLike,
  applyScaleCustomAttr,
  buildScaleOptions,
};
