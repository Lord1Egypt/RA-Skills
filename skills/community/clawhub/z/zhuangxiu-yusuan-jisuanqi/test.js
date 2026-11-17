'use strict';

const assert = require('assert');
const { calculateDecorationBudget, parseQuery, handleQuery } = require('./index.js');

// 1. 100㎡ 新房 全包 标准 → 取 100 档原区间
let r = calculateDecorationBudget({ area: 100, houseType: 'new', packageType: 'full', level: 'standard' });
assert.strictEqual(r.ok, true);
assert.deepStrictEqual(r.fullPackageTotal.range, [9.9, 12.7]);
assert.deepStrictEqual(r.halfPackage.range, [4.2, 5.2]);
assert.strictEqual(r.oldHouseExtra, null);

// 2. 90㎡ 旧房 半包
r = calculateDecorationBudget({ area: 90, houseType: 'old', packageType: 'half', level: 'standard' });
assert.deepStrictEqual(r.halfPackage.range, [3.8, 4.8]);
assert.deepStrictEqual(r.oldHouseExtra.range, [0.8, 1.5]);

// 3. 边界 80 与 150
r = calculateDecorationBudget({ area: 80 });
assert.deepStrictEqual(r.fullPackageTotal.range, [7.5, 9.9]);
r = calculateDecorationBudget({ area: 150 });
assert.deepStrictEqual(r.fullPackageTotal.range, [15.8, 20.9]);

// 4. 缺面积报错
r = calculateDecorationBudget({ area: 0 });
assert.strictEqual(r.ok, false);

// 5. handleQuery 文本解析
const parsed = parseQuery('120平旧房半包');
assert.strictEqual(parsed.area, 120);
assert.strictEqual(parsed.houseType, 'old');
assert.strictEqual(parsed.packageType, 'half');

const text = handleQuery('100平装修多少钱');
assert.ok(typeof text === 'string' && text.includes('万'));

// 6. 缺面积返回追问
const ask = handleQuery('装修要多少钱');
assert.ok(ask.includes('建筑面积'));

console.log('All tests passed');
