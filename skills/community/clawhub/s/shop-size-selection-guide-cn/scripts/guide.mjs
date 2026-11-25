import fs from 'node:fs';

const toCm = (value, unit) => {
  if (!Number.isFinite(value)) return null;
  const factors = { cm: 1, '厘米': 1, mm: 0.1, '毫米': 0.1, m: 100, '米': 100, in: 2.54, inch: 2.54, inches: 2.54, '英寸': 2.54 };
  return factors[unit] == null ? null : value * factors[unit];
};
const stopped = missing => ({ status: 'stopped', missing: [...new Set(missing)], eligibleSizes: [], message: '资料不足或规则无效，停止推荐；不依据身高体重推造尺码。' });
const fieldTerms = {
  bust: ['胸围', '胸部', '胸宽'], chest: ['胸围', '胸部', '胸宽'], chestwidth: ['胸围', '胸部', '胸宽'],
  waist: ['腰围', '腰部', '腰宽'], waistcircumference: ['腰围', '腰部', '腰宽'], hip: ['臀围', '臀部', '臀宽'],
  shoulder: ['肩宽', '肩部', '肩点'], sleeve: ['袖长', '袖子'],
  length: ['衣长', '裤长', '身长'], inseam: ['裤内长', '内长']
};
function termsFor(field) {
  const key = field.toLowerCase().replace(/[^a-z]/g, '');
  return fieldTerms[key] || [field];
}
function fieldMatches(text, field) {
  return typeof text === 'string' && termsFor(field).some(term => text.includes(term));
}
function fieldApplies(area, field) {
  if (typeof area !== 'string') return false;
  const terms = termsFor(field);
  const escapedTerms = terms.map(term => term.replace(/[.*+?^${}()|[\]\\]/gu, '\\$&')).join('|');
  // 不能只靠“包含部位”判定适用：部位可能出现在排除说明中，且否定词
  // 既会写在部位前，也会写在部位后（如“胸围不适用”“除胸围外”）。
  const denied = new RegExp([
    `(?:不适用(?:于)?|不适合|排除|不含|不包括|不计)\\s*(?:${escapedTerms})`,
    `(?:${escapedTerms})\\s*(?:不适用|不适合|排除|不含|不包括|不计)`,
    `除(?:了)?\\s*(?:${escapedTerms})\\s*(?:外|之外)`,
    `(?:${escapedTerms})\\s*(?:除外|除之外|以外|之外)`,
    `不包括\\s*(?:${escapedTerms})`
  ].join('|'), 'u');
  if (denied.test(area)) return false;
  const exclusive = [...area.matchAll(/(?:仅|只)适用(?:于)?\s*([^，,；;。]+)/gu)].map(match => match[1]);
  if (exclusive.length) return exclusive.some(segment => terms.some(term => segment.includes(term)));
  return fieldMatches(area, field);
}
function measurementMethodUnavailable(method) {
  if (typeof method !== 'string') return false;
  const text = method.replace(/\s+/gu, ' ').trim();
  const unavailable = '(?:未提供|未说明|没有(?:提供|说明)?|未能提供|暂无|待确认|未知|不详|不明确|缺少|未见|未有|待补|没说|未说|没提|未告知|没给|未写|没写)';
  const measurement = '(?:胸围|腰围|臀围|肩宽|袖长|衣长|裤长|测量方法|量法)';
  // 缺失表述可能在部位之前（“暂无胸围测量方法”）或之后
  // （“胸围测量方法不详”）。两种写法都不是可执行量法，必须停止推荐。
  return new RegExp(`(?:${unavailable}.{0,12}${measurement}|${measurement}.{0,12}${unavailable}|商家.{0,12}${unavailable}|^${unavailable})`, 'u').test(text);
}
function measurementClauses(method) {
  return typeof method === 'string'
    ? method.split(/[；;。\n]/u).map(clause => clause.trim()).filter(Boolean)
    : [];
}
function clauseHasConcreteMeasurementMethod(clause) {
  if (typeof clause !== 'string') return false;
  // “平量”或“围量”只是标签，不能说明实际怎样量。量法必须至少交代
  // 可复现的工具、路径/范围或起止基准；仅写“胸围围量”不能通过。
  const action = '(?:横量|直量|测量|量取|测|量)';
  return new RegExp([
    // 平铺成衣后实际量取，或在可辨认的裁片基准处量取。
    `(?:成衣|衣服|上衣|裤子|服装).{0,16}(?:平铺|铺平).{0,16}${action}`,
    `(?:沿|在).{1,16}(?:腋下|最宽处|腰部|臀部|肩点|肩缝|领口|裤腰|裆部|袖山|下摆).{0,16}${action}`,
    // 给出量具和实际动作/路径。
    `(?:用|使用|借助).{0,8}(?:软尺|皮尺|卷尺|尺子).{0,24}(?:绕|沿|从|至|到|${action})`,
    `(?:绕|围绕).{0,12}(?:胸围|胸部|腰围|腰部|臀围|臀部).{0,12}(?:一周|一圈)`,
    // “围度一周测量”本身定义了完整的测量范围；没有“一周/一圈”则不够。
    `(?:胸围|胸部|腰围|腰部|臀围|臀部).{0,8}(?:一周|一圈).{0,8}${action}`,
    // 明确的起止点或双端量取同样可执行。
    `(?:从|由).{1,12}(?:到|至).{1,12}${action}`,
    `(?:两端|沿着).{0,12}${action}`,
    `拉直后${action}`
  ].join('|'), 'u').test(clause);
}
function executableMeasurementClauses(method) {
  // 量法是否具体只在这里判定一次。后续规则校验只把字段与这份已判定
  // 的可执行分句对应，避免一条胸围量法替另一条腰围规则背书。
  return measurementClauses(method).filter(clauseHasConcreteMeasurementMethod);
}
function hasExecutableMethodForField(executableClauses, field) {
  const ownTerms = termsFor(field);
  const terms = ownTerms.map(term => term.replace(/[.*+?^${}()|[\]\\]/gu, '\\$&')).join('|');
  const otherTerms = [...new Set(Object.values(fieldTerms).flat())]
    .filter(term => !ownTerms.includes(term))
    .map(term => term.replace(/[.*+?^${}()|[\]\\]/gu, '\\$&')).join('|');
  const action = '(?:横量|直量|测量|量取|测|量)';
  // 字段到量取动作之间若已切换到另一已知部位，不能再把该动作算给前一字段。
  const withoutOtherField = otherTerms ? `(?:(?!(?:${otherTerms})).)` : '.';
  // 先确认分句本身可执行，再要求规则字段落在同一个“量取动作”内。
  // 不能让“胸围和腰围分别测量，用软尺绕腰部一周测量腰围”中的腰围动作
  // 为胸围规则背书。这里特意不以分句里出现过字段名作为充分条件。
  const boundToField = new RegExp([
    // 围度类：字段和“一周/一圈”的动作必须在同一段。
    `(?:${terms})${withoutOtherField}{0,10}(?:一周|一圈).{0,8}${action}`,
    `(?:绕|围绕).{0,12}(?:${terms}).{0,12}(?:一周|一圈).{0,8}${action}`,
    `(?:绕|围绕).{0,12}(?:${terms}).{0,12}(?:一周|一圈)`,
    // 平铺或基准点量取：动作后明确给出该字段，例如“横量胸宽”。
    `(?:横量|直量|量取|测量).{0,12}(?:${terms})`,
    `(?:从|由).{0,8}(?:${terms}).{0,6}(?:量|测).{0,8}(?:到|至).{0,8}(?:${terms})`,
    // 字段先出现时，必须紧接可复现的路径/基准，而非笼统“分别测量”。
    `(?:${terms})${withoutOtherField}{0,12}(?:沿|从|由|在).{0,16}${action}`
  ].join('|'), 'u');
  return executableClauses.some(clause =>
    clauseHasConcreteMeasurementMethod(clause) && boundToField.test(clause)
  );
}
function atLeastWithConversionTolerance(actual, required) {
  // 单位换算可能产生 101.59999999999998 这类 IEEE 754 尾差；
  // 只容忍与当前数值尺度相称的机器精度，不使用会放宽业务条件的固定余量。
  const scale = Math.max(1, Math.abs(actual), Math.abs(required));
  return actual >= required - Number.EPSILON * scale * 8;
}

export function guide(input) {
  const missing = [];
  for (const key of ['unit', 'measurementMethod', 'applicableArea']) if (typeof input[key] !== 'string' || !input[key].trim()) missing.push(key);
  const unit = typeof input.unit === 'string' ? input.unit.trim().toLowerCase() : '';
  const factors = { cm: 1, '厘米': 1, mm: 0.1, '毫米': 0.1, m: 100, '米': 100, in: 2.54, inch: 2.54, inches: 2.54, '英寸': 2.54 };
  if (unit && factors[unit] == null) missing.push(`不支持的单位：${input.unit}`);
  const rows = Array.isArray(input.sizeChart) ? input.sizeChart : [];
  if (!rows.length) missing.push('sizeChart（每个尺码对应的关键尺寸及单位）');
  if (rows.length > 20) missing.push('尺码档数不得超过20');
  const rules = Array.isArray(input.selectionRules) ? input.selectionRules : [];
  const groups = input.customerMeasurements === undefined ? [] : input.customerMeasurements;
  if (!Array.isArray(groups)) missing.push('customerMeasurements 必须是最多5组的列表，每组包含 name 与 measurements 字段');
  else if (groups.length > 5) missing.push('顾客测量组不得超过5组');
  else groups.forEach((group, index) => {
    if (!group || typeof group !== 'object' || Array.isArray(group) || typeof group.name !== 'string' || !group.name.trim() || !group.measurements || typeof group.measurements !== 'object' || Array.isArray(group.measurements)) {
      missing.push(`第${index + 1}组顾客测量须含 name 与 measurements 对象`);
      return;
    }
    for (const [field, value] of Object.entries(group.measurements)) {
      if (!Number.isFinite(value) || value <= 0) missing.push(`第${index + 1}组顾客测量${field}须为正数`);
    }
  });
  if (!rules.length) missing.push('selectionRules；请说明要核对的关键尺寸字段，并提供每个尺码对应的尺寸与单位');
  const validRules = new Set(['min_ease']);
  // 选码规则只能基于商家给出的关键部位尺寸。这里刻意按“人体指标”而非
  // “含身字的字段”判断：中文“身长”在本 Skill 中是成衣长度字段，不能被
  // 误当成人体身高；“身高范围”“参考体重”和 weight_range 等修饰名仍须拦截。
  const isForbiddenAnthropometricField = field => {
    if (typeof field !== 'string') return false;
    const normalized = field.normalize('NFKC').toLowerCase().replace(/[\s_\-‐–—()（）.【】\[\]:：]/gu, '');
    const chineseHumanMetric = /(?:身高|体高|人體?高度|體高|体重|體重)/u;
    const englishHumanMetric = /(?:height|stature|bodyheight|weight|bodyweight|bodymass|mass)/u;
    return chineseHumanMetric.test(normalized) || englishHumanMetric.test(normalized);
  };
  const sizeNames = rows.map(row => ((typeof row?.size === 'string' && row.size.trim()) || (typeof row?.size === 'number' && Number.isFinite(row.size)) ? String(row.size).trim() : ''));
  if (sizeNames.some(name => !name) || new Set(sizeNames).size !== sizeNames.length) missing.push('每档必须提供唯一且有效的尺码名称');
  const methodUnavailable = measurementMethodUnavailable(input.measurementMethod);
  const executableMethodClauses = methodUnavailable ? [] : executableMeasurementClauses(input.measurementMethod);
  if (methodUnavailable) missing.push('商家平铺/围量的测量方法');
  else if (!executableMethodClauses.length) missing.push('商家提供具体测量方法（仅有部位名称不足以推荐）');
  for (const rule of rules) {
    if (!rule || typeof rule.field !== 'string' || !rule.field.trim()) missing.push('规则缺少关键尺寸字段');
    if (isForbiddenAnthropometricField(rule?.field)) missing.push(`禁止使用身高或体重选码：${rule.field}`);
    if (!validRules.has(rule?.operator)) missing.push(`无效选码操作符：${rule?.operator ?? '缺失'}`);
    if ((!Number.isFinite(rule?.customerValue) || rule.customerValue <= 0) && (!Array.isArray(groups) || !groups.length)) missing.push(`规则缺少有效正数顾客测量值：${rule?.field ?? '未知字段'}`);
    if (Number.isFinite(rule?.customerValue) && rule.customerValue <= 0) missing.push(`顾客测量值须为正数：${rule?.field ?? '未知字段'}`);
    if (!Number.isFinite(rule?.ease) || rule.ease < 0) missing.push(`规则缺少有效余量：${rule?.field ?? '未知字段'}`);
    if (typeof rule?.field === 'string' && !isForbiddenAnthropometricField(rule.field)) {
      if (!methodUnavailable && !hasExecutableMethodForField(executableMethodClauses, rule.field)) missing.push(`测量方法须与规则字段一致且可执行：${rule.field}`);
      if (!fieldApplies(input.applicableArea, rule.field)) missing.push(`适用部位须与规则字段一致：${rule.field}`);
    }
    if (typeof rule?.field === 'string' && !isForbiddenAnthropometricField(rule.field)) {
      for (const row of rows) {
        if (!Number.isFinite(row?.[rule.field])) missing.push(`尺码${row?.size ?? '(未命名)'}缺少关键尺寸：${rule.field}`);
        else if (row[rule.field] <= 0) missing.push(`尺码${row?.size ?? '(未命名)'}关键尺寸须为正数：${rule.field}`);
      }
    }
  }
  if (Array.isArray(groups)) {
    for (const group of groups) {
      if (!group || typeof group !== 'object' || Array.isArray(group) || typeof group.name !== 'string' || !group.name.trim() || !group.measurements || typeof group.measurements !== 'object' || Array.isArray(group.measurements)) continue;
      for (const rule of rules) {
        if (typeof rule?.field === 'string' && !isForbiddenAnthropometricField(rule.field)
            && !Number.isFinite(group.measurements[rule.field])) {
          missing.push(`${group.name}：补充顾客测量：${rule.field}`);
        }
      }
    }
  }
  if (missing.length) return stopped(missing);

  const chartFields = [...new Set(rows.flatMap(row => Object.entries(row).filter(([key, value]) => key !== 'size' && Number.isFinite(value)).map(([key]) => key)))];
  const normalizedSizeChart = rows.map(row => ({
    size: row.size,
    measurements: Object.fromEntries(chartFields.filter(field => Number.isFinite(row[field])).map(field => [field, toCm(row[field], unit)]))
  }));
  const selectSizes = (measurements, fromRuleValues = false) => rows.filter(row => rules.every(rule => {
    const customerValue = fromRuleValues ? rule.customerValue : measurements[rule.field];
    const chartValue = toCm(row[rule.field], unit), bodyValue = toCm(customerValue, unit), easeValue = toCm(rule.ease, unit);
    const requiredValue = bodyValue + easeValue;
    return Number.isFinite(customerValue) && rule.operator === 'min_ease' &&
      atLeastWithConversionTolerance(chartValue, requiredValue);
  })).map(row => row.size);
  const defaultComplete = rules.every(rule => Number.isFinite(rule.customerValue));
  const defaultEligibleSizes = defaultComplete ? selectSizes({}, true) : [];
  const customerResults = groups.map(group => {
    const missingMeasurements = rules
      .filter(rule => !Number.isFinite(group.measurements[rule.field]))
      .map(rule => rule.field).filter((field, index, fields) => fields.indexOf(field) === index);
    const eligibleSizes = selectSizes(group.measurements);
    return { name: group.name, eligibleSizes, missingMeasurements };
  });
  // 顾客组一旦被提交，就必须能按同一组商家规则核验；不能用顶层默认值
  // 掩盖某位顾客只给了身高、体重等非关键数据的情况。
  if (customerResults.some(result => result.missingMeasurements.length)) {
    return stopped(customerResults.flatMap(result => result.missingMeasurements.map(field => `${result.name}：补充顾客测量：${field}`)));
  }
  const completeCustomers = customerResults.filter(result => result.missingMeasurements.length === 0);
  const customerUnion = new Set(completeCustomers.flatMap(result => result.eligibleSizes));
  const eligibleSizes = defaultComplete ? defaultEligibleSizes
    : completeCustomers.length ? rows.map(row => row.size).filter(size => customerUnion.has(size))
      : defaultEligibleSizes;
  // 分组输入没有默认顾客值时，顶层范围是所有测量完整分组的并集；
  // 待确认项也必须保留到对应分组，不能因为另一组有候选尺码而被吞掉。
  const groupConfirmationItems = customerResults.flatMap(result => {
    if (result.missingMeasurements.length) {
      return result.missingMeasurements.map(field => `${result.name}：补充顾客测量：${field}`);
    }
    return result.eligibleSizes.length ? [] : [`${result.name}：没有尺码满足商家给定规则`];
  });
  const defaultConfirmationItems = defaultComplete && !defaultEligibleSizes.length ? ['没有尺码满足商家给定规则'] : [];
  const confirmationItems = [...defaultConfirmationItems, ...groupConfirmationItems];
  return {
    status: 'recommended', normalizedUnit: 'cm', normalizedSizeChart,
    measurementSteps: [input.measurementMethod], eligibleSizes,
    ...(customerResults.length ? { customerResults } : {}),
    confirmationItems
  };
}

if (process.argv[1]?.endsWith('guide.mjs')) console.log(JSON.stringify(guide(JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))), null, 2));
