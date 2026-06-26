module.exports = async function handler(context) {
  if (context && context.subagent) return null;

  return {
    role: "system",
    content:
      "[Verified Humanizer] Rewrite locally, measure before/after changes, and only verify structured metrics if verification is needed. Never send original or rewritten text to external verification."
  };
};
