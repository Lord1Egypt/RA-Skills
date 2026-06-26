/** 安全转整数 */
function int(v, def = 0) {
  const n = parseInt(v);
  return isNaN(n) ? def : n;
}

/** 断言必填参数存在 */
function requireParams(params, fields) {
  const missing = fields.filter(f => params[f] === undefined || params[f] === '');
  if (missing.length > 0) throw new Error(`缺少必填参数：${missing.join(', ')}`);
}

/** 成功输出 */
function ok(label, data) {
  console.log(`\n✅ ${label}`);
  console.log(JSON.stringify(data, null, 2));
}

module.exports = { int, requireParams, ok };
