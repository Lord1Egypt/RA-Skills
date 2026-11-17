"use strict";

const DEFAULT_AI_SOURCE = 12;
const DEFAULT_REG_SOURCE = "ai_skills";

function resolveAiSource(value) {
  const effective = value == null || value === "" ? DEFAULT_AI_SOURCE : value;
  const parsed = Number(effective);
  if (!Number.isInteger(parsed) || parsed < 0) {
    throw new Error("--ai-source 必须是非负整数");
  }
  return parsed;
}

function resolveRegSource(value) {
  const effective =
    value == null || String(value).trim() === "" ? DEFAULT_REG_SOURCE : value;
  const normalized = String(effective).trim();
  if (!/^[A-Za-z0-9_-]{1,64}$/.test(normalized)) {
    throw new Error("--reg-source 只能包含字母、数字、下划线或短横线，长度 1～64");
  }
  return normalized;
}

module.exports = {
  DEFAULT_AI_SOURCE,
  DEFAULT_REG_SOURCE,
  resolveAiSource,
  resolveRegSource,
};
