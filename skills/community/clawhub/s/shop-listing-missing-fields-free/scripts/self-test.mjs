#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
process.env.LISTING_TEST_FAST_STABLE_WAIT = '1';
process.env.EASY_WEBBRIDGE_TOKEN = 'fixture-only-token'; // mock adapter only; never sent to a real bridge.
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const must = ['SKILL.md','manifest.yaml','agents/openai.yaml','README.md','README.en.md','LICENSE','icon-512.png','assets/promo.png','fixtures/success-page.json','fixtures/failure-page.json','fixtures/dynamic-rules.json','fixtures/dynamic-rules-no-category.json','fixtures/explicit-control-association.html'];
for (const f of must) if (!existsSync(resolve(root, f))) throw new Error(`缺少 ${f}`);
const manifest = readFileSync(resolve(root, 'manifest.yaml'), 'utf8');
if (!manifest.includes('name: shop-listing-missing-fields-free') || !manifest.includes('slug: shop-listing-missing-fields-free') || !manifest.includes('icon: icon-512.png')) throw new Error('manifest 标识或图标不正确');
const selfTestSource = readFileSync(fileURLToPath(import.meta.url), 'utf8');
if (selfTestSource.includes(['import', 'meta', 'dirname'].join('.'))) throw new Error('self_test 使用了不兼容 Node 18 的目录 API');
const checkerSource = readFileSync(resolve(root, 'scripts/check-listing.mjs'), 'utf8');
if (!checkerSource.includes("const interactiveValueSelector='input,textarea,select,[role=\"textbox\"]") || !checkerSource.includes('valueNode.matches(interactiveValueSelector)') || !checkerSource.includes('valueNode.querySelector(interactiveValueSelector)')) throw new Error('直属 value 节点本身和其子节点都必须排除交互控件，交由控件读取真实可见值');
if (!checkerSource.includes('[...el.selectedOptions]') || !checkerSource.includes("input[type=\"password\"]") || !checkerSource.includes("input:not([type=\"file\"])") || checkerSource.includes('el.files?.length') || !checkerSource.includes('sensitive(label)') || !checkerSource.includes('naturalWidth<80') || !checkerSource.includes('uniquePaths') || !checkerSource.includes('normalizeFieldLabel') || checkerSource.includes("el.getAttribute('aria-label')") || checkerSource.includes("parent.getAttribute('aria-label')") || !checkerSource.includes('label=labelFor(el)') || checkerSource.includes('label=labelFor(el)||context?.label') || !checkerSource.includes('control.option && control.groupLabel') || !checkerSource.includes('custom.${String(category') || !checkerSource.includes('aria-checked') || !checkerSource.includes('elementFromPoint') || !checkerSource.includes('node=node.parentElement') || !checkerSource.includes("browserId, 'scroll'") || !checkerSource.includes('const images=') || !checkerSource.includes("getAttribute('placeholder')") || !checkerSource.includes('samePageIdentity') || !checkerSource.includes('latest = await call') || !checkerSource.includes('shown(labelNode)') || !checkerSource.includes('shown(valueNode)') || !checkerSource.includes('[contenteditable]:not([contenteditable="false"])') || !checkerSource.includes('view(labelNode).trim()') || !checkerSource.includes('view(valueNode).trim()') || !checkerSource.includes('aria-activedescendant') || !checkerSource.includes('nodeKey') || !checkerSource.includes('assertCurrentPage') || !checkerSource.includes('stableSamples >= requiredStableSamples') || !checkerSource.includes('requiredStableSamples = testFastStabilization ? 1 : 3') || !checkerSource.includes('readiness.busy === 0') || !checkerSource.includes('pending:!hasValue&&Boolean(prompt)') || !checkerSource.includes('forbiddenPathSegments') || !checkerSource.includes('Object.hasOwn(value, key)') || !checkerSource.includes('valueNode.matches(')) throw new Error('读取必须仅使用可见标签、过滤敏感控件、保留多选值、等待稳定并安全处理字段路径');
if (!checkerSource.includes('aria-labelledby') || !checkerSource.includes('[role="radiogroup"]') || !checkerSource.includes('JSON.stringify(item.visibleValue)')) throw new Error('单选组标题须支持 ARIA 关联，跨视口采集不能覆盖复用 DOM 节点的前一 SKU');
if (checkerSource.includes('const text = snapshot.text') || checkerSource.includes('shot.text =')) throw new Error('不得把 snapshot --text-mode page 的整页文字直接作为字段证据');
const associationFixture = readFileSync(resolve(root, 'fixtures/explicit-control-association.html'), 'utf8');
if (!associationFixture.includes('<label for="fixture-colour">颜色</label>') || !associationFixture.includes('class="title">规格') || !associationFixture.includes('id="unlabelled-value"')) throw new Error('显式控件关联离线 DOM 资料模拟不完整');
if (checkerSource.includes('fieldContext') || checkerSource.includes('fieldLabel')) throw new Error('控件标签不得由祖先 .label/.title 推断，也不得使用 fieldLabel 覆盖明确关联标签');
const run = spawnSync('node', ['scripts/check-listing.mjs','--offline-page','fixtures/success-page.json','--rules','fixtures/rules.json'], { cwd: root, encoding: 'utf8' });
if (run.status !== 0) throw new Error(run.stderr);
const out = JSON.parse(run.stdout);
if (!out.rows.some(r => r.field === '库存' && r.status === '待确认') || !out.rows.some(r => r.field === '详情文案' && r.status === '待确认')) throw new Error('未读取字段必须标记为待确认');
const conflict = out.rows.find(r => r.field === '退货承诺' && r.status === '冲突');
if (out.rows.filter(r => r.field === '退货承诺').length !== 1) throw new Error('字段不得同时已见与冲突');
if (!conflict || !conflict.source.includes('离线页面资料模拟') || !conflict.source.includes('离线商家规则模拟')) throw new Error('冲突行未同时保留页面可见值与商家规则来源');
if (!conflict.manual_action.includes('设置7天无理由退货')) throw new Error('冲突行必须保留商家规则的 action');
const pendingInventory = out.rows.find(r => r.field === '库存');
if (!pendingInventory.manual_action.includes('核实') || pendingInventory.manual_action.includes('补充')) throw new Error('待确认字段只能要求核实，不得断言缺项并要求补充');
const fail = spawnSync('node', ['scripts/check-listing.mjs','--offline-page','fixtures/failure-page.json','--rules','fixtures/rules.json'], { cwd: root, encoding: 'utf8' });
if (fail.status !== 0) throw new Error('离线资料样例应可生成检查表');
const failOut = JSON.parse(fail.stdout);
if (!failOut.rows.some(r => r.field === '颜色' && r.status === '缺项') || !failOut.rows.some(r => r.field === '主图' && r.status === '缺项')) throw new Error('明确空值必须识别为缺项');
const trailingColon = JSON.parse(runBrowser('trailing-colon'));
if (trailingColon.rows.find(r => r.field === '颜色')?.visible_value !== '蓝色') throw new Error('字段标签尾部冒号不代表空值，必须采用关联控件的真实值');
const freightPlaceholder = JSON.parse(runBrowser('placeholder-freight'));
if (freightPlaceholder.rows.find(r => r.field === '运费模板')?.status !== '待确认') throw new Error('“暂无运费模板”必须保留为待确认提示，不得标成已见');
const placeholder = JSON.parse(runBrowser('placeholder'));
if (placeholder.rows.find(r => r.field === '运费模板')?.status !== '待确认') throw new Error('请选择某项的占位文案必须归为待确认');
const colorPlaceholder = JSON.parse(runBrowser('placeholder-color'));
if (colorPlaceholder.rows.find(r => r.field === '颜色')?.status !== '待确认') throw new Error('请选择颜色等带后缀的占位文案必须归为待确认');
const emptyFreight = failOut.rows.find(r => r.field === '运费模板');
const emptyReturn = failOut.rows.find(r => r.field === '退货承诺');
if (!emptyFreight?.manual_action.includes('包邮模板') || !emptyFreight.manual_action.includes('选择包邮模板') || !emptyReturn?.manual_action.includes('7天无理由退货') || !emptyReturn.manual_action.includes('设置7天无理由退货')) throw new Error('已知空字段必须保留商家规则的 expected 和 action');
const browser = spawnSync('node', ['scripts/check-listing.mjs', '--browser-id', 'fixture-browser', '--page-url', 'https://example.invalid/edit', '--rules','fixtures/dynamic-rules.json'], { cwd: root, encoding: 'utf8', env: { ...process.env, EASY_WEBBRIDGE_CLI: resolve(root, 'fixtures/mock-easy-webbridge.mjs'), LISTING_TEST_MODE: 'success' } });
if (browser.status !== 0) throw new Error(`浏览器快照分支失败：${browser.stderr}`);
const browserOut = JSON.parse(browser.stdout);
if (browserOut.rows.find(r => r.field === '颜色')?.status !== '已见' || browserOut.rows.find(r => r.field === '颜色')?.visible_value !== '蓝色') throw new Error('明确字段：值文本应写入对应字段');
if (browserOut.rows.find(r => r.field === '库存')?.visible_value !== '20' || browserOut.rows.find(r => r.field === '详情图')?.visible_value !== '三张') throw new Error('长别名字段值被短别名截断');
if (!browserOut.rows.every(r => r.source.includes('标题=商品编辑') && r.source.includes('URL=https://example.invalid/edit') && !r.source.includes('secret-value') && !r.source.includes('signature=') && !r.source.includes('#private')) || browserOut.sources.some(s => /secret-value|signature=|#private/.test(s))) throw new Error('浏览器来源未脱敏 URL 查询参数或片段');
if (browserOut.rows.find(r => r.field === '材质')?.status !== '已见' || browserOut.rows.find(r => r.field === '材质')?.visible_value !== '纯棉') throw new Error('快照中动态商家规则字段必须按真实可见标签和值映射');
const tempDir=mkdtempSync(resolve(tmpdir(),'listing-regression-'));
try {
 for(const mode of ['login','truncated','malformed','foreign','missing-status']){
  const trace=resolve(tempDir,mode+'.jsonl');
  const r=spawnSync('node',['scripts/check-listing.mjs','--browser-id','fixture-browser','--page-url','https://example.invalid/edit'],{cwd:root,encoding:'utf8',env:{...process.env,EASY_WEBBRIDGE_CLI:resolve(root,'fixtures/mock-easy-webbridge.mjs'),LISTING_TEST_MODE:mode,LISTING_TEST_TRACE:trace}});
  if(r.status===0 || r.stdout.trim())throw new Error(mode+'不得生成误导缺项表');
  const calls=readFileSync(trace,'utf8').trim().split('\n').map(JSON.parse);
  const first=calls[0],last=calls.at(-1);
  if(first.action!=='navigate'||first.args.newTab!==true||!first.args.session.startsWith('shop-listing-missing-fields-free-'))throw new Error(mode+'未使用独立任务session');
  if(mode==='foreign' && calls.some(c=>c.action==='close_session'))throw new Error('foreign tab 不属于本任务时不得关闭session');
  if(mode!=='foreign' && (last.action!=='close_session'||last.args.session!==first.args.session))throw new Error(mode+'未清理已确认归属的session');
 }
 for(const mode of ['mixed-session','redirected-page','spa-redirect','hash-route-redirect']) {
  const trace=resolve(tempDir,mode+'.jsonl');
  const r=spawnSync('node',['scripts/check-listing.mjs','--browser-id','fixture-browser','--page-url','https://example.invalid/edit'],{cwd:root,encoding:'utf8',env:{...process.env,EASY_WEBBRIDGE_CLI:resolve(root,'fixtures/mock-easy-webbridge.mjs'),LISTING_TEST_MODE:mode,LISTING_TEST_TRACE:trace}});
  if(r.status===0||r.stdout.trim())throw new Error(mode+' 必须阻止误读并停止生成');
  const calls=readFileSync(trace,'utf8').trim().split('\n').map(JSON.parse);
  if(mode==='mixed-session'&&calls.some(c=>c.action==='close_session'))throw new Error('混入其他tab时不得关闭整个session');
  if(mode==='redirected-page'&&!r.stderr.includes('最终页面与用户指定'))throw new Error('最终URL重定向到其他商品页必须拒绝读取');
  if(mode==='spa-redirect'&&!r.stderr.includes('身份发生变化'))throw new Error('页面扫描中 SPA 跳转到其他商品页必须丢弃结果');
  if(mode==='hash-route-redirect'&&!r.stderr.includes('身份发生变化'))throw new Error('同一路径的 hash 路由切换商品时必须丢弃混合结果');
 }
 const loadingTrace=resolve(tempDir,'loading.jsonl');
 const loading=spawnSync('node',['scripts/check-listing.mjs','--browser-id','fixture-browser','--page-url','https://example.invalid/edit'],{cwd:root,encoding:'utf8',env:{...process.env,EASY_WEBBRIDGE_CLI:resolve(root,'fixtures/mock-easy-webbridge.mjs'),LISTING_TEST_MODE:'loading',LISTING_TEST_TRACE:loadingTrace}});
 if(loading.status!==0)throw new Error('loading 狀态 fixture 应等待完成后读取：'+loading.stderr);
 const loadingCalls=readFileSync(loadingTrace,'utf8').trim().split('\n').map(JSON.parse).map(x=>x.action);
 const snapshotAt=loadingCalls.indexOf('snapshot'); if(snapshotAt<0||loadingCalls.slice(0,snapshotAt).filter(x=>x==='list_tabs').length<2)throw new Error('页面尚未加载完成时不得读取快照');
 const hydrationTrace=resolve(tempDir,'hydration.jsonl');
 const hydration=spawnSync('node',['scripts/check-listing.mjs','--browser-id','fixture-browser','--page-url','https://example.invalid/edit'],{cwd:root,encoding:'utf8',env:{...process.env,EASY_WEBBRIDGE_CLI:resolve(root,'fixtures/mock-easy-webbridge.mjs'),LISTING_TEST_MODE:'async-hydration',LISTING_TEST_TRACE:hydrationTrace}});
 if(hydration.status!==0)throw new Error('页面 complete 后异步回填应等待稳定再扫描：'+hydration.stderr);
 const hydrationOut=JSON.parse(hydration.stdout),hydrationCalls=readFileSync(hydrationTrace,'utf8').trim().split('\n').map(JSON.parse);
 if(hydrationOut.rows.find(r=>r.field==='颜色')?.visible_value!=='蓝色'||hydrationCalls.filter(x=>x.action==='snapshot').length<4)throw new Error('尚未回填的旧快照不得判缺项，必须等字段稳定后采用最新值');
}finally{rmSync(tempDir,{recursive:true,force:true});}
const capRules = { requirements: Array.from({ length: 105 }, (_, i) => ({ field: `extra.${i}`, label: `额外字段${i}` })) };
const capped = JSON.parse(runCheck(root, capRules));
if (capped.rows.length !== 100 || !capped.truncated || capped.total_candidate_rows !== 115 || !capped.next_batch) throw new Error('结果未强制执行 100 行上限');
if (capped.rows.some(r => r.field.startsWith('额外字段') && r.status !== '待确认')) throw new Error('不可见商家规则字段必须待确认');
const ruleMissing = JSON.parse(runCheck(root, { requirements: [{ field: 'extra.target', label: '目标字段', expected: '必须值', action: '填写必须值', source: '离线规则' }] }));
const missingTarget = ruleMissing.rows.find(r => r.field === '目标字段');
if (!missingTarget?.manual_action.includes('必须值') || !missingTarget.manual_action.includes('填写必须值')) throw new Error('未读到规则字段必须保留 expected 与 action');
const unsafeRuleDir=mkdtempSync(resolve(tmpdir(),'listing-unsafe-rule-'));
try {
 for(const field of ['constructor','__proto__.polluted','custom.prototype.value','custom.constructor.value']){
  const rulesPath=resolve(unsafeRuleDir,'rules.json');writeFileSync(rulesPath,JSON.stringify({requirements:[{field,label:'危险路径字段'}]}));
  const result=spawnSync('node',['scripts/check-listing.mjs','--offline-page','fixtures/success-page.json','--rules',rulesPath],{cwd:root,encoding:'utf8'});
  if(result.status===0||result.stdout.trim()||!result.stderr.includes('不安全的字段路径'))throw new Error(`${field} 必须在读取继承属性或写入结果前被拒绝`);
 }
}finally{rmSync(unsafeRuleDir,{recursive:true,force:true});}
const inheritedFieldDir=mkdtempSync(resolve(tmpdir(),'listing-inherited-rule-'));
try {
 const rulesPath=resolve(inheritedFieldDir,'rules.json');
 writeFileSync(rulesPath,JSON.stringify({requirements:[{label:'不应读取原型字段',expected:'任意值'}]}));
 const result=spawnSync('node',['scripts/check-listing.mjs','--offline-page','fixtures/success-page.json','--rules',rulesPath],{cwd:root,encoding:'utf8'});
 if(result.status!==0)throw new Error(result.stderr);
 if(JSON.parse(result.stdout).rows.some(row=>row.field==='不应读取原型字段'))throw new Error('未显式提供 field 的规则不得读取继承 constructor 或生成结果行');
}finally{rmSync(inheritedFieldDir,{recursive:true,force:true});}
const explicitEmpty = JSON.parse(runBrowser('empty'));
if (explicitEmpty.rows.find(r => r.field === '颜色')?.status !== '缺项') throw new Error('快照中明确空控件值必须判缺项');
const pendingValue = JSON.parse(runBrowser('pending-control'));
if (pendingValue.rows.find(r => r.field === '颜色')?.status !== '待确认') throw new Error('控件中的未确认状态不得被判为缺项');
for (const [mode,field] of [['input-placeholder','颜色'],['disabled-select-placeholder','运费模板']]) { const placeholderControl=JSON.parse(runBrowser(mode)); if(placeholderControl.rows.find(r=>r.field===field)?.status!=='待确认')throw new Error(mode+' 显示提示项时必须待确认，不能判缺项或已见'); }
for (const [mode,field] of [['placeholder-example','颜色'],['placeholder-dashes','运费模板']]) { const prompt=JSON.parse(runBrowser(mode)); const row=prompt.rows.find(r=>r.field===field); if(row?.status!=='待确认'||row.visible_value)throw new Error(mode+' 示例文本或选择占位项必须留空并待确认，不能作为已见资料'); }
const textWins = JSON.parse(runBrowser('text-wins'));
if (textWins.rows.find(r => r.field === '颜色')?.visible_value !== 'internal-code') throw new Error('关联控件值必须覆盖页面任意位置的同名文字');
const adjacent = JSON.parse(runBrowser('adjacent-labels'));
if (adjacent.rows.find(r => r.field === '颜色')?.status !== '待确认' || adjacent.rows.find(r => r.field === '库存')?.visible_value !== '' || adjacent.rows.find(r => r.field === '尺码')?.status !== '待确认') throw new Error('任意页面文字不得冒充字段值，必须等待结构化字段对或关联控件');
const labelHelp = JSON.parse(runBrowser('label-help'));
if (labelHelp.rows.find(r => r.field === '库存')?.status !== '待确认' || labelHelp.rows.find(r => r.field === '尺码')?.status !== '待确认') throw new Error('字段标签后的帮助文案不得冒充字段值');
const designText = spawnSync('node', ['scripts/check-listing.mjs','--browser-id','fixture-browser','--page-url','https://example.invalid/edit'], { cwd: root, encoding: 'utf8', env: { ...process.env, EASY_WEBBRIDGE_CLI: resolve(root, 'fixtures/mock-easy-webbridge.mjs'), LISTING_TEST_MODE: 'designing' } });
if (designText.status !== 0) throw new Error('普通文案 designing 不应被误判为登录页');
const controlsOnly = JSON.parse(runBrowser('controls-only', ['--rules','fixtures/dynamic-rules.json']));
if (controlsOnly.rows.find(r => r.field === '颜色')?.visible_value !== '蓝色' || controlsOnly.rows.find(r => r.field === '材质')?.visible_value !== '纯棉') throw new Error('关联标签的可见控件值必须映射到对应字段');
const explicitAssociation = JSON.parse(runBrowser('explicit-control-association'));
if (explicitAssociation.rows.find(r => r.field === '颜色')?.visible_value !== '蓝色' || explicitAssociation.rows.some(r => r.field === '规格' || r.visible_value === '不得采集')) throw new Error('规格分区标题不得覆盖颜色的明确关联标签；无关联控件不得采集');
const hiddenText = JSON.parse(runBrowser('hidden-text'));
if (hiddenText.rows.find(r => r.field === '颜色')?.status !== '待确认' || hiddenText.rows.find(r => r.field === '颜色')?.visible_value || hiddenText.rows.find(r => r.field === '尺码')?.status !== '待确认') throw new Error('视口外/隐藏页面文本不得成为字段证据');
const multiPage = JSON.parse(runBrowser('multi-page'));
if (!multiPage.rows.find(r => r.field === '发货地')?.visible_value.includes('宁波') || !multiPage.rows.find(r => r.field === '退货承诺')?.visible_value.includes('七天无理由') || multiPage.rows.find(r => r.field === '主图')?.visible_value !== '1张可见图片预览' || multiPage.rows.find(r => r.field === '详情图')?.visible_value !== '1张可见图片预览') throw new Error('滚动扫描必须保留重复字段的多值并采集图片预览');
const scrollDir = mkdtempSync(resolve(tmpdir(), 'listing-scroll-')), scrollTrace = resolve(scrollDir, 'trace.jsonl');
try {
 const scrollRun = spawnSync('node', ['scripts/check-listing.mjs', '--browser-id', 'fixture-browser', '--page-url', 'https://example.invalid/edit'], { cwd: root, encoding: 'utf8', env: { ...process.env, EASY_WEBBRIDGE_CLI: resolve(root, 'fixtures/mock-easy-webbridge.mjs'), LISTING_TEST_MODE: 'multi-page', LISTING_TEST_TRACE: scrollTrace } });
 if (scrollRun.status !== 0) throw new Error(scrollRun.stderr);
 const deltas = readFileSync(scrollTrace, 'utf8').trim().split('\n').map(JSON.parse).filter(call => call.action === 'scroll').map(call => call.args.y);
 if (JSON.stringify(deltas.slice(0, 3)) !== JSON.stringify([480, 420, 60]) || deltas.at(-1) !== -900) throw new Error('scroll 接口为相对滚动：分屏扫描必须按当前位置计算增量并恢复原位置');
} finally { rmSync(scrollDir, { recursive: true, force: true }); }
const customControl = JSON.parse(runBrowser('custom-controls'));
if (customControl.rows.find(r => r.field === '颜色')?.visible_value !== '墨绿') throw new Error('自定义可访问控件的显式标签和值必须采集');
const normalCopy = JSON.parse(runBrowser('normal-copy'));
if (normalCopy.rows.find(r => r.field === '颜色')?.visible_value !== '蓝色') throw new Error('普通说明中的“加载失败”“登录后可见”不能阻止合法商品页检查');
const longCustomField = JSON.parse(runBrowser('long-custom-field'));
if (longCustomField.rows.find(r => r.field === '适用于多种设备的扩展型商品规格说明')?.visible_value !== '支持多设备') throw new Error('明确可见的长自定义字段不得静默丢弃');
const ariaGrouped = JSON.parse(runBrowser('aria-grouped-options'));
if (ariaGrouped.rows.find(r => r.field === '颜色')?.visible_value !== '红色') throw new Error('ARIA radiogroup 关联标题应映射为字段名');
const punctuatedCustomField = JSON.parse(runBrowser('punctuated-custom-field'));
if (punctuatedCustomField.rows.find(r => r.field === '商品重量（kg）')?.visible_value !== '0.5') throw new Error('带括号等常见字符的自定义字段标签必须安全写入检查表');
const incompletePrompts = JSON.parse(runBrowser('incomplete-prompts'));
for (const field of ['库存','主图','运费模板']) if (incompletePrompts.rows.find(r => r.field === field)?.status !== '待确认') throw new Error(`${field} 的“请填写/请上传/暂无模板”提示必须标记待确认`);
const groupedOptions = JSON.parse(runBrowser('grouped-options'));
if (groupedOptions.rows.find(r => r.field === '颜色')?.status !== '已见' || groupedOptions.rows.find(r => r.field === '颜色')?.visible_value !== '蓝色') throw new Error('单选项文字应映射到所属字段而不是冒充字段标签');
const groupedReturn = JSON.parse(runBrowser('grouped-return'));
if (groupedReturn.rows.find(r => r.field === '退货承诺')?.visible_value !== '7天无理由退货') throw new Error('复选项文字应映射到售后所属字段');
const hiddenAssociatedLabel = JSON.parse(runBrowser('hidden-associated-label'));
if(hiddenAssociatedLabel.rows.find(r=>r.field==='颜色')?.status!=='待确认')throw new Error('隐藏标签不能成为商品字段的可见标签证据');
const multiStock = JSON.parse(runBrowser('multi-stock'));
if(multiStock.rows.find(r=>r.field==='库存')?.status!=='待确认'||JSON.stringify(multiStock.rows.find(r=>r.field==='库存')?.visible_value)!=='["","12"]')throw new Error('多个 SKU 中部分库存为空时必须保留各值并标待确认');
const virtualStock = JSON.parse(runBrowser('virtual-stock'));
if(virtualStock.rows.find(r=>r.field==='库存')?.status!=='待确认'||JSON.stringify(virtualStock.rows.find(r=>r.field==='库存')?.visible_value)!=='["","12"]')throw new Error('虚拟 SKU 复用相同 DOM 路径时，前后 SKU 的库存值必须分别保留');
const customCombo = JSON.parse(runBrowser('custom-combo'));
if(customCombo.rows.find(r=>r.field==='运费模板')?.visible_value!=='顺丰包邮')throw new Error('自定义下拉框必须读取可见选中项');
const editable = JSON.parse(runBrowser('contenteditable'));
if(editable.rows.find(r=>r.field==='详情文案')?.visible_value!=='100%纯棉')throw new Error('contenteditable 可见内容必须作为字段值');
const sensitive = JSON.parse(runBrowser('sensitive-label'));
if(sensitive.rows.some(row=>/API Token|super-secret/i.test(JSON.stringify(row)))||sensitive.sources.some(source=>/super-secret/i.test(source)))throw new Error('可见标签含访问密钥/Token 的控件不得进入输出');
const requiredLabels=JSON.parse(runBrowser('required-labels'));
if(requiredLabels.rows.find(row=>row.field==='颜色')?.visible_value!=='蓝色'||requiredLabels.rows.find(row=>row.field==='运费模板')?.visible_value!=='顺丰包邮'||requiredLabels.rows.some(row=>row.field.includes('必填')||row.field.includes('*')))throw new Error('常见必填标记必须归一化并命中已有字段');
const crossCategory=JSON.parse(runBrowser('cross-category'));
if(crossCategory.rows.find(row=>row.field==='颜色')?.status!=='待确认'||crossCategory.rows.find(row=>row.field==='颜色')?.visible_value)throw new Error('图文分区里的同名颜色不得填充规格颜色字段');
const genericSection=JSON.parse(runBrowser('generic-section'));
if(genericSection.rows.find(row=>row.field==='颜色')?.visible_value!=='蓝色'||genericSection.rows.some(row=>row.field==='规格'))throw new Error('祖先分区标题不得覆盖控件自己的明确颜色标签');
const genericRules=JSON.parse(runBrowser('generic-rule-fields',['--rules','fixtures/rules.json']));
for(const [field,value] of [['运费模板','包邮模板'],['退货承诺','7天无理由退货']])if(genericRules.rows.find(row=>row.field===field)?.visible_value!==value)throw new Error('无分区标题时，内置别名与商家规则的重复字段不能制造伪歧义');
const savedFileThumbnail=JSON.parse(runBrowser('saved-file-thumbnail'));
if(savedFileThumbnail.rows.find(row=>row.field==='主图')?.status!=='已见'||savedFileThumbnail.rows.find(row=>row.field==='主图')?.visible_value!=='1张可见图片预览')throw new Error('label[for] 内的可见远程缩略图必须作为已保存主图证据；隐藏 file 控件的 FileList 不能参与判断');
const imageNoise=JSON.parse(runBrowser('image-noise'));
if(imageNoise.rows.find(row=>row.field==='主图')?.status!=='待确认'||imageNoise.rows.find(row=>row.field==='详情图')?.status!=='待确认')throw new Error('非图文分区的缩略图或添加图标不得计为商品图片预览');
const dynamicSections = JSON.parse(runBrowser('dynamic-sections'));
for (const [field,category,status] of [['款式','规格','已见'],['商品视频','图文','待确认'],['发货时效','物流','已见'],['质保','售后','已见']]) {
 const row=dynamicSections.rows.find(item=>item.field===field);
 if(!row||row.category!==category||row.status!==status)throw new Error(`自定义${category}字段 ${field} 未进入缺项检查`);
}
const repeatedCategoryField = dynamicSections.rows.filter(item=>item.field==='卖点');
if(repeatedCategoryField.length!==2||repeatedCategoryField.find(item=>item.category==='规格')?.visible_value!=='棉麻'||repeatedCategoryField.find(item=>item.category==='图文')?.visible_value!=='三张细节图')throw new Error('不同类目下同名自定义字段必须分开保留');
const uncategorizedDynamicRule = JSON.parse(runBrowser('dynamic-sections',['--rules','fixtures/dynamic-rules-no-category.json']));
const styleRuleRow = uncategorizedDynamicRule.rows.filter(item=>item.field==='款式');
if(styleRuleRow.length!==1||styleRuleRow[0].category!=='规格'||styleRuleRow[0].visible_value!=='宽松'||styleRuleRow[0].status!=='冲突'||!styleRuleRow[0].source.includes('离线动态商家规则模拟'))throw new Error('未声明类目的唯一动态规则必须沿用匹配页面字段的真实分区、保留来源并判定冲突');
const unscopedSellingPoints=uncategorizedDynamicRule.rows.filter(item=>item.field==='卖点');
if(unscopedSellingPoints.length!==2||unscopedSellingPoints.find(item=>item.category==='规格')?.visible_value!=='棉麻'||unscopedSellingPoints.find(item=>item.category==='图文')?.visible_value!=='三张细节图'||unscopedSellingPoints.some(item=>item.category==='商家规则')||unscopedSellingPoints.some(item=>!item.source.includes('离线动态商家规则模拟')))throw new Error('无分类动态规则命中多个页面分区时必须保留两行真实分区，不能合并或归入商家规则');
const dynamicDir=mkdtempSync(resolve(tmpdir(),'listing-dynamic-'));
try {
 const pageFile=resolve(dynamicDir,'page.json'), rulesFile=resolve(dynamicDir,'rules.json');
 writeFileSync(pageFile,JSON.stringify({source:'离线页 https://shop.example/item?access_token=page-secret#private',fields:{}}));
 writeFileSync(rulesFile,JSON.stringify({requirements:[
  {field:'extra.fit',label:'版型',expected:'合身',action:'按版型表核对',source:'https://rules.example/fit?token=rule-secret#private'},
  {field:'extra.fit',label:'版型',expected:'合身',action:'核对肩宽',source:'内部规则'}
 ]}));
 const dynamic=JSON.parse(spawnSync('node',['scripts/check-listing.mjs','--offline-page',pageFile,'--rules',rulesFile],{cwd:root,encoding:'utf8'}).stdout);
 const fitRows=dynamic.rows.filter(r=>r.field==='版型');
 if(fitRows.length!==1||fitRows[0].status!=='待确认')throw new Error('同一动态字段的多条规则必须合并成一行一个状态');
 if(dynamic.sources.join('\n').includes('page-secret')||dynamic.sources.join('\n').includes('rule-secret')||dynamic.sources.join('\n').includes('#private'))throw new Error('页面或规则来源中的URL凭据必须脱敏');
 writeFileSync(pageFile,JSON.stringify({source:'商家后台资料',fields:{afterSale:{returnPolicy:'暂无退换货'}}}));
 const explicitNone=JSON.parse(spawnSync('node',['scripts/check-listing.mjs','--offline-page',pageFile],{cwd:root,encoding:'utf8'}).stdout);
 if(explicitNone.rows.find(r=>r.field==='退货承诺')?.status!=='已见'||explicitNone.rows.find(r=>r.field==='退货承诺')?.visible_value!=='暂无退换货')throw new Error('“暂无退换货”是可见规则值，不能统统视为占位提示');
 writeFileSync(rulesFile,JSON.stringify({requirements:[{field:'spec.stock',label:'库存',category:'规格',expected:'0'},{field:'spec.stock',label:'库存',category:'规格',expected:'20'}]}));
 const ruleConflict=JSON.parse(spawnSync('node',['scripts/check-listing.mjs','--offline-page','fixtures/success-page.json','--rules',rulesFile],{cwd:root,encoding:'utf8'}).stdout);
 if(ruleConflict.rows.find(r=>r.field==='库存')?.status!=='冲突')throw new Error('同字段商家规则互相矛盾时，即使页面缺项也必须显示规则冲突');
} finally { rmSync(dynamicDir,{recursive:true,force:true}); }
console.log('PASS: 关联标签控件值、快照空值、规则目标、URL 脱敏、冲突、失败清理及100行上限通过；未连接真实浏览器。');
// The fixture CLI is intentionally invoked many times; exit explicitly after
// all synchronous assertions pass so a leaked stdio handle cannot make the
// manifest self_test command appear to hang.
process.exit(0);

function runBrowser(mode, extra=[]) {
 const dir=mkdtempSync(resolve(tmpdir(),'listing-browser-')), trace=resolve(dir,'trace.jsonl');
 try {
  const r=spawnSync('node',['scripts/check-listing.mjs','--browser-id','fixture-browser','--page-url','https://example.invalid/edit',...extra],{cwd:root,encoding:'utf8',env:{...process.env,EASY_WEBBRIDGE_CLI:resolve(root,'fixtures/mock-easy-webbridge.mjs'),LISTING_TEST_MODE:mode,LISTING_TEST_TRACE:trace}});
  if(r.status!==0)throw new Error(r.stderr);
  return r.stdout;
 } finally { rmSync(dir,{recursive:true,force:true}); }
}

function runCheck(root, rules) {
  const encoded = Buffer.from(JSON.stringify(rules)).toString('base64');
  const code = `const fs=require('fs');fs.writeFileSync(process.argv[1],Buffer.from(process.argv[2],'base64'))`;
  const temp = resolve(root, '.self-test-rules.json');
  const write = spawnSync('node', ['-e', code, temp, encoded], { cwd: root, encoding: 'utf8' });
  if (write.status !== 0) throw new Error(write.stderr);
  const result = spawnSync('node', ['scripts/check-listing.mjs', '--offline-page', 'fixtures/success-page.json', '--rules', '.self-test-rules.json'], { cwd: root, encoding: 'utf8' });
  const remove = spawnSync('node', ['-e', "require('fs').unlinkSync(process.argv[1])", temp], { cwd: root, encoding: 'utf8' });
  if (remove.status !== 0 || result.status !== 0) throw new Error(result.stderr || remove.stderr);
  return result.stdout;
}
