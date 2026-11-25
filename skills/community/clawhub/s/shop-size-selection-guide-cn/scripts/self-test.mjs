import assert from 'node:assert/strict';
import fs from 'node:fs';
import { guide } from './guide.mjs';
const root = new URL('..', import.meta.url);
for (const name of ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'icon-512.png']) assert.ok(fs.existsSync(new URL(name, root)));
const success = JSON.parse(fs.readFileSync(new URL('fixtures/success.json', root)));
const successResult = guide(success);
assert.equal(successResult.status, 'recommended');
assert.deepEqual(successResult.eligibleSizes, ['L']);
assert.deepEqual(successResult.normalizedSizeChart, success.referenceDelivery.normalizedSizeChart);
const failure = JSON.parse(fs.readFileSync(new URL('fixtures/failure.json', root)));
const failureResult = guide(failure);
assert.equal(failureResult.status, 'stopped');
assert.ok(failureResult.missing.includes('尺码M缺少关键尺寸：bust'));
assert.ok(failureResult.missing.includes('尺码L缺少关键尺寸：bust'));
assert.ok(failureResult.missing.includes('商家平铺/围量的测量方法'));
assert.ok(failureResult.missing.includes('顾客A：补充顾客测量：bust'));
assert.ok(!failureResult.missing.includes('applicableArea'));
assert.ok(!failureResult.missing.some(item => item.includes('规则缺少有效顾客测量值')));
assert.deepEqual(failure.referenceDelivery.requestForInformation, failureResult.missing);
const convert = guide({unit:'mm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'A',bust:960},{size:'B',bust:1000}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:900,ease:70}]});
assert.equal(convert.normalizedSizeChart[0].measurements.bust, 96);
assert.deepEqual(convert.eligibleSizes, ['B']);
for (const [unit, value, customerValue, ease, expected] of [['厘米',96,90,4,96],['毫米',960,900,40,96],['米',0.96,0.9,0.04,96]]) {
  const localized = guide({unit,measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:36,bust:value}],selectionRules:[{field:'bust',operator:'min_ease',customerValue,ease}]});
  assert.deepEqual(localized.eligibleSizes, [36]);
  assert.equal(localized.normalizedSizeChart[0].measurements.bust, expected);
}
for (const bad of [
  {unit:'cm',measurementMethod:'平量',applicableArea:'胸围',sizeChart:[{size:'S',bust:90},{size:'M'}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}]},
  {unit:'cm',measurementMethod:'平量',applicableArea:'胸围',sizeChart:[{size:'S',bust:90}],selectionRules:[{field:'bust',operator:'magic',customerValue:80,ease:4}]},
  {unit:'cm',measurementMethod:'平量',applicableArea:'胸围',sizeChart:[{size:'S',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80}]}
]) assert.equal(guide(bad).status, 'stopped');
const anthropometric = guide({unit:'cm',measurementMethod:'围量',applicableArea:'上衣',sizeChart:[{size:'S',height:160,weight:50},{size:'M',height:170,weight:60}],selectionRules:[{field:'height',operator:'min_ease',customerValue:165,ease:2}]});
assert.equal(anthropometric.status, 'stopped');
assert.ok(anthropometric.missing.some(x => x.includes('禁止使用身高或体重选码')));
assert.equal(guide({unit:'cm',measurementMethod:'围量',applicableArea:'上衣',sizeChart:[{size:'S',body_weight:50}],selectionRules:[{field:'body_weight',operator:'min_ease',customerValue:50,ease:1}]}).status, 'stopped');
for (const field of ['身 高', '身高范围', '参考体重', '参考：体重', '体高', '体高_cm', '體高', '体 重', 'body_weight', 'body_height_cm', 'weight_range', 'stature', 'stature_cm']) {
  // 完整量法、适用部位和尺码表均不能为人体指标规则背书，更不能产生候选尺码。
  const blocked = guide({unit:'cm',measurementMethod:'成衣平铺后沿衣身直量胸围',applicableArea:'胸围',sizeChart:[{size:'S',[field]:160}],selectionRules:[{field,operator:'min_ease',customerValue:150,ease:2}]});
  assert.equal(blocked.status, 'stopped', field);
  assert.deepEqual(blocked.eligibleSizes, [], field);
  assert.ok(blocked.missing.some(x => x.includes('禁止使用身高或体重选码')), field);
}
// 回归：stature 不能绕过 height/身高保护并产出候选尺码。
const statureOnly = guide({unit:'cm',measurementMethod:'围量',applicableArea:'上衣',sizeChart:[{size:'S',stature:160},{size:'M',stature:170}],selectionRules:[{field:'stature',operator:'min_ease',customerValue:165,ease:2}]});
assert.equal(statureOnly.status, 'stopped');
assert.deepEqual(statureOnly.eligibleSizes, []);
assert.ok(statureOnly.missing.includes('禁止使用身高或体重选码：stature'));
const aliasHeight = guide({unit:'cm',measurementMethod:'从头顶到脚底直量体高',applicableArea:'体高',sizeChart:[{size:'S',体高:160},{size:'M',体高:170}],selectionRules:[{field:'体高',operator:'min_ease',customerValue:165,ease:2}]});
assert.equal(aliasHeight.status, 'stopped');
assert.deepEqual(aliasHeight.eligibleSizes, []);
assert.ok(aliasHeight.missing.some(item => item.includes('禁止使用身高或体重选码')));
// “身长”是商家常用的成衣长度名：字段、适用部位和可执行量法均完整时可正常筛选。
const garmentLength = guide({unit:'cm',measurementMethod:'成衣平铺后从肩点到下摆直量身长',applicableArea:'身长',sizeChart:[{size:'M',身长:100},{size:'L',身长:108}],selectionRules:[{field:'身长',operator:'min_ease',customerValue:90,ease:5}]});
assert.equal(garmentLength.status, 'recommended');
assert.deepEqual(garmentLength.eligibleSizes, ['M', 'L']);
const unnamed = guide({unit:'cm',measurementMethod:'围量',applicableArea:'胸围',sizeChart:[{bust:90}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}]});
assert.equal(unnamed.status, 'stopped');
assert.ok(unnamed.missing.includes('每档必须提供唯一且有效的尺码名称'));
const fieldMismatch = guide({unit:'cm',measurementMethod:'腰围一周',applicableArea:'腰围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}]});
assert.equal(fieldMismatch.status, 'stopped');
assert.ok(fieldMismatch.missing.some(item => item.includes('须与规则字段一致')));
const partiallyDocumentedMethods = guide({unit:'cm',measurementMethod:'胸围一周测量；腰围',applicableArea:'胸围和腰围',sizeChart:[{size:'M',bust:90,waist:70}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4},{field:'waist',operator:'min_ease',customerValue:60,ease:4}]});
assert.equal(partiallyDocumentedMethods.status, 'stopped');
assert.deepEqual(partiallyDocumentedMethods.eligibleSizes, []);
assert.ok(partiallyDocumentedMethods.missing.some(item => item.includes('可执行：waist')));
const wrongMethodBorrow = guide({unit:'cm',measurementMethod:'胸围和腰围需分别测量，用软尺绕腰部一周测量腰围',applicableArea:'胸围和腰围',sizeChart:[{size:'L',bust:96,waist:76}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:88,ease:4}]});
assert.equal(wrongMethodBorrow.status,'stopped');
assert.deepEqual(wrongMethodBorrow.eligibleSizes,[]);
assert.ok(wrongMethodBorrow.missing.some(item=>item.includes('须与规则字段一致且可执行：bust')));
// 同一分句也不能把腰围的具体量法错误归给胸围。
const wrongMethodBorrowSameClause = guide({unit:'cm',measurementMethod:'胸围和腰围绕腰部一周测量腰围',applicableArea:'胸围和腰围',sizeChart:[{size:'L',bust:96,waist:76}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:88,ease:4}]});
assert.equal(wrongMethodBorrowSameClause.status,'stopped');
assert.ok(wrongMethodBorrowSameClause.missing.some(item=>item.includes('须与规则字段一致且可执行：bust')));
const excludedApplicableArea = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'不适用于胸围，仅适用于腰围',sizeChart:[{size:'L',bust:96}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:88,ease:4}]});
assert.equal(excludedApplicableArea.status,'stopped');
assert.deepEqual(excludedApplicableArea.eligibleSizes,[]);
assert.ok(excludedApplicableArea.missing.some(item=>item.includes('适用部位须与规则字段一致：bust')));
for (const applicableArea of ['胸围除外，仅适用于腰围', '不包括胸围，仅适用于腰围', '胸围不包括在适用部位内', '胸围以外均适用']) {
  const excluded = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea,sizeChart:[{size:'L',bust:96}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:88,ease:4}]});
  assert.equal(excluded.status,'stopped',applicableArea);
  assert.ok(excluded.missing.some(item=>item.includes('适用部位须与规则字段一致：bust')),applicableArea);
}
for (const measurementMethod of ['用软尺绕胸部一周','用软尺，从左肩点量到右肩点']) {
  const field = measurementMethod.includes('肩点') ? 'shoulder' : 'bust';
  const applicableArea = field === 'shoulder' ? '肩宽' : '胸围';
  const complete = guide({unit:'cm',measurementMethod,applicableArea,sizeChart:[{size:'L',[field]:96}],selectionRules:[{field,operator:'min_ease',customerValue:88,ease:4}]});
  assert.equal(complete.status,'recommended',measurementMethod);
  assert.deepEqual(complete.eligibleSizes,['L'],measurementMethod);
}
for (const applicableArea of ['胸围不适用，仅适用于腰围', '除胸围外，适用于腰围']) {
  const excluded = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea,sizeChart:[{size:'L',bust:96}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:88,ease:4}]});
  assert.equal(excluded.status, 'stopped', applicableArea);
  assert.ok(excluded.missing.some(item=>item.includes('适用部位须与规则字段一致：bust')), applicableArea);
}
const group = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',ease:4}],customerMeasurements:[{name:'顾客A',measurements:{bust:85,waist:68,hip:92,shoulder:40,sleeve:58,length:62}}]});
assert.equal(group.status, 'recommended');
assert.deepEqual(group.customerResults, [{name:'顾客A',eligibleSizes:['M'],missingMeasurements:[]}]);
assert.deepEqual(group.eligibleSizes, ['M']);
assert.deepEqual(group.confirmationItems, []);
// 回归：规则没有 customerValue 时，顶层结论必须从分组结果汇总，不能同时声称无尺码。
const groupedSummary = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',ease:4}],customerMeasurements:[{name:'顾客A',measurements:{bust:85}}]});
assert.deepEqual(groupedSummary.customerResults, [{name:'顾客A',eligibleSizes:['M'],missingMeasurements:[]}]);
assert.deepEqual(groupedSummary.eligibleSizes, ['M']);
assert.ok(!groupedSummary.confirmationItems.includes('没有尺码满足商家给定规则'));
const mixedGroups = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',ease:4}],customerMeasurements:[{name:'顾客A',measurements:{bust:85}},{name:'顾客B',measurements:{waist:68}}]});
assert.equal(mixedGroups.status,'stopped');
assert.deepEqual(mixedGroups.eligibleSizes, []);
assert.ok(mixedGroups.missing.includes('顾客B：补充顾客测量：bust'));
const defaultAndGroups = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:85,ease:4}],customerMeasurements:[{name:'顾客A',measurements:{waist:68}}]});
assert.equal(defaultAndGroups.status, 'stopped');
assert.deepEqual(defaultAndGroups.eligibleSizes, []);
assert.ok(defaultAndGroups.missing.includes('顾客A：补充顾客测量：bust'));
const heightWeightOnlyGroup = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:85,ease:4}],customerMeasurements:[{name:'顾客A',measurements:{height:168,weight:55}}]});
assert.equal(heightWeightOnlyGroup.status, 'stopped');
assert.ok(heightWeightOnlyGroup.missing.includes('顾客A：补充顾客测量：bust'));
const partialGroup = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',ease:4}],customerMeasurements:[{name:'顾客A',measurements:{waist:68}}]});
assert.equal(partialGroup.status,'stopped');
assert.deepEqual(partialGroup.eligibleSizes, []);
assert.ok(partialGroup.missing.includes('顾客A：补充顾客测量：bust'));
const tooManyGroups = guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:90}],selectionRules:[{field:'bust',operator:'min_ease',ease:4}],customerMeasurements:Array.from({length:6},(_,i)=>({name:`顾客${i}`,measurements:{bust:85}}))});
assert.equal(tooManyGroups.status, 'stopped');
assert.ok(tooManyGroups.missing.includes('顾客测量组不得超过5组'));
assert.ok(!tooManyGroups.missing.some(item => item.includes('每组')));
for (const measurementMethod of ['商家未提供胸围测量方法','胸围量法待确认','暂无胸围测量方法','商家没有提供胸围测量方法','胸围测量方法不详','胸围请测量后填写','胸围量法商家没说','胸围围量','成衣平量','请平铺测量']) {
  const blocked=guide({unit:'cm',measurementMethod,applicableArea:'胸围',sizeChart:[{size:'M',bust:100}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}]});
  assert.equal(blocked.status,'stopped',measurementMethod);
  assert.deepEqual(blocked.eligibleSizes, [], measurementMethod);
  assert.ok(blocked.missing.some(item=>item.includes('测量方法')), measurementMethod);
}
const bodyPartOnly=guide({unit:'cm',measurementMethod:'胸围',applicableArea:'胸围',sizeChart:[{size:'M',bust:100}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}]});
assert.equal(bodyPartOnly.status,'stopped');
assert.ok(bodyPartOnly.missing.some(item=>item.includes('具体测量方法')));
for(const badInput of [
  {unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:100}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}],customerMeasurements:[{name:'顾客A',measurements:{bust:-10}}]},
  {unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:-100}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4}]},
  {unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:100}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:-10,ease:4}]}
]) assert.equal(guide(badInput).status,'stopped');
const exactInchEdge=guide({unit:'in',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:40}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:35,ease:5}]});
assert.deepEqual(exactInchEdge.eligibleSizes,['M']);
const repeatedFieldRules=guide({unit:'cm',measurementMethod:'胸围一周测量',applicableArea:'胸围',sizeChart:[{size:'M',bust:93}],selectionRules:[{field:'bust',operator:'min_ease',customerValue:80,ease:4},{field:'bust',operator:'min_ease',customerValue:90,ease:2}]});
assert.deepEqual(repeatedFieldRules.eligibleSizes,['M']);
console.log('self-test passed: full chart normalization, aligned method/area, measurement groups, mm conversion, and safe stops verified');
