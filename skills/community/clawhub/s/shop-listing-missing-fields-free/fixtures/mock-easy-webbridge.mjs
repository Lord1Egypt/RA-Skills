#!/usr/bin/env node
import { appendFileSync, readFileSync } from 'node:fs';
if (process.argv.includes('--help')) { console.error('easy-webbridge command <browserId> <action> [args-json]'); process.exit(2); }
const [verb,browser,action,args] = process.argv.slice(2);
const mode=process.env.LISTING_TEST_MODE || 'success';
let result;
if(verb==='command'){
 const data=JSON.parse(args);if(process.env.LISTING_TEST_TRACE)appendFileSync(process.env.LISTING_TEST_TRACE,JSON.stringify({action,args:data})+'\n');
 if(action==='navigate')result={tabId:17};else if(action==='scroll')result={scrolled:true};else if(action==='list_tabs'){
  let count=0;
  if(process.env.LISTING_TEST_TRACE){try{count=readFileSync(process.env.LISTING_TEST_TRACE,'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(x=>x.action==='list_tabs').length}catch{}}
  result=mode==='mixed-session'?[{id:17,status:'complete'},{id:18,status:'complete'}]:[{id:mode==='foreign'?18:17,status:mode==='missing-status'?undefined:(mode==='loading'&&count===1?'loading':'complete')}];
 }else if(action==='evaluate'){
  const trace=process.env.LISTING_TEST_TRACE||'';let y=0;
  if(trace){try{for(const item of readFileSync(trace,'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(x=>x.action==='scroll'))y=Math.max(0,Math.min((['multi-page','virtual-stock'].includes(mode)?1500:600)-600,y+Number(item.args.y||0)));}catch{}}
  if(data.code.includes('readyState:'))result={readyState:'complete',busy:0};
  else if(data.code.includes('pageHeight:'))result={pageHeight:['multi-page','virtual-stock'].includes(mode)?1500:600,viewportHeight:600,scrollTop:0};
  else if(data.code==='location.href'){let count=0;if(trace){try{count=readFileSync(trace,'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(x=>x.action==='evaluate'&&x.args.code==='location.href').length}catch{}}result=mode==='spa-redirect'&&count>=2?'https://example.invalid/other':mode==='hash-route-redirect'&&count>=2?'https://example.invalid/edit?access_token=secret-value&signature=abc#product-2':'https://example.invalid/edit?access_token=secret-value&signature=abc#private';}
  else if(data.code==='window.scrollY'){let scroll=0;try{for(const item of readFileSync(trace,'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(x=>x.action==='scroll'))scroll=Math.max(0,Math.min((['multi-page','virtual-stock'].includes(mode)?1500:600)-600,scroll+Number(item.args.y||0)));}catch{}result=scroll;}
  else if(data.code.includes('const images')){
   const base=[['颜色','蓝色'],['尺码','M'],['库存','20'],['主图','已上传'],['详情图','三张'],['详情文案','纯棉短袖'],['运费模板','包邮模板'],['发货地','杭州'],['退货承诺','7天退货'],['售后说明','联系客服'],['材质','纯棉']].map(([label,visibleValue])=>({label,visibleValue}));
   const texts={'normal-copy':'图片加载失败说明\n买家登录后可见\n颜色：蓝色','hidden-text':'尺码：M','placeholder':'运费模板：请选择运费模板','placeholder-color':'颜色：请选择颜色','placeholder-freight':'运费模板：暂无运费模板','trailing-colon':'颜色：','empty':'颜色：','pending-control':'颜色','text-wins':'颜色：页面文本蓝色','adjacent-labels':'颜色\n库存\n请填写商品库存\n尺码：M','label-help':'库存 - 请填写商品库存\n尺码：M','controls-only':'颜色\n尺码\n库存\n主图\n详情图\n详情文案\n运费模板\n发货地\n退货承诺\n售后说明\n材质','incomplete-prompts':'规格\n库存：请填写商品库存\n图文\n主图：请上传主图\n物流\n运费模板：暂无运费模板','dynamic-sections':'规格\n款式：宽松\n卖点：棉麻\n图文\n商品视频：待上传\n卖点：三张细节图\n物流\n发货时效：24小时\n售后\n质保：一年','designing':'Designing a new product listing'};
   let text=['input-placeholder','disabled-select-placeholder','grouped-options','grouped-return','hidden-associated-label','multi-stock','custom-combo','contenteditable'].includes(mode)?'':mode==='multi-page'&&y>=600?'发货地：宁波\n退货承诺：七天无理由':mode==='custom-controls'?'颜色':(texts[mode]??'颜色：蓝色\n尺码：M\n库存：20\n主图：已上传\n详情图：三张\n详情文案：纯棉短袖\n运费模板：包邮模板\n发货地：杭州\n退货承诺：7天退货\n售后说明：联系客服\n材质：纯棉');
   let controls=base;
   if(mode==='virtual-stock')controls=y===0?[{label:'库存',category:'规格',visibleValue:''}]:y>0?[{label:'库存',category:'规格',visibleValue:'12'}]:[];else if(mode==='long-custom-field')controls=[{label:'适用于多种设备的扩展型商品规格说明',category:'规格',visibleValue:'支持多设备'}];else if(mode==='aria-grouped-options')controls=[{label:'红色',groupLabel:'颜色',option:true,category:'规格',visibleValue:'红色'}];else if(mode==='input-placeholder')controls=[{label:'颜色',visibleValue:'',pending:true}];else if(mode==='disabled-select-placeholder')controls=[{label:'运费模板',visibleValue:'',pending:true}];else if(mode==='empty')controls=[{label:'颜色',visibleValue:''}];else if(mode==='trailing-colon')controls=[{label:'颜色 ： ',visibleValue:'蓝色'}];else if(mode==='placeholder'||mode==='placeholder-color'||mode==='placeholder-freight')controls=[];else if(mode==='pending-control')controls=[{label:'颜色',visibleValue:'未确认'}];else if(mode==='text-wins')controls=[{label:'颜色',visibleValue:'internal-code'}];else if(mode==='multi-page'&&y>=600)controls=[{label:'发货地',visibleValue:'宁波'},{label:'退货承诺',visibleValue:'七天无理由'}];else if(mode==='grouped-options')controls=[{label:'蓝色',groupLabel:'颜色',option:true,category:'规格',visibleValue:'蓝色'}];else if(mode==='grouped-return')controls=[{label:'7天无理由退货',groupLabel:'退货承诺',option:true,category:'售后',visibleValue:'7天无理由退货'}];else if(mode==='hidden-associated-label')controls=[{label:'红色',visibleValue:'红色'}];else if(mode==='multi-stock')controls=[{label:'库存',fieldLabel:'库存',category:'规格',visibleValue:''},{label:'库存',fieldLabel:'库存',category:'规格',visibleValue:'12'}];else if(mode==='custom-combo')controls=[{label:'运费模板',fieldLabel:'运费模板',category:'物流',visibleValue:'顺丰包邮'}];else if(mode==='contenteditable')controls=[{label:'详情文案',fieldLabel:'详情文案',category:'图文',visibleValue:'100%纯棉'}];else if(mode==='custom-controls')controls=[{label:'颜色',visibleValue:'墨绿'}];else if(mode==='punctuated-custom-field')controls=[{label:'商品重量（kg）',fieldLabel:'商品重量（kg）',category:'规格',visibleValue:'0.5'}];else if(mode==='sensitive-label')controls=[{label:'API Token',fieldLabel:'API Token',category:'规格',visibleValue:'super-secret'}];else if(mode==='required-labels')controls=[{label:'颜色 *',fieldLabel:'颜色 *',category:'规格',visibleValue:'蓝色'},{label:'运费模板（必填）',fieldLabel:'运费模板（必填）',category:'物流',visibleValue:'顺丰包邮'}];else if(mode==='cross-category')controls=[{label:'颜色',fieldLabel:'颜色',category:'图文',visibleValue:'红色'}];else if(mode==='empty-file')controls=[{label:'主图',fieldLabel:'主图',category:'图文',visibleValue:''}];else if(['adjacent-labels','label-help','designing','hidden-text','incomplete-prompts','dynamic-sections','image-noise'].includes(mode))controls=[];
   // placeholder-freight has no control: this exercises semantic field-pair
   // parsing, rather than merely finding the marker in page-level text.
   const pairs=mode==='placeholder-freight'?[{label:'运费模板',category:'物流',visibleValue:'暂无运费模板'}]:mode==='dynamic-sections'?[{label:'款式',category:'规格',visibleValue:'宽松'},{label:'卖点',category:'规格',visibleValue:'棉麻'},{label:'商品视频',category:'图文',visibleValue:'待上传'},{label:'卖点',category:'图文',visibleValue:'三张细节图'},{label:'发货时效',category:'物流',visibleValue:'24小时'},{label:'质保',category:'售后',visibleValue:'一年'}]:[];
   const images=mode==='multi-page'&&y>=600?[{label:'主图',category:'图文',key:'img-main',visibleValue:'首图预览'},{label:'详情图',category:'图文',key:'img-detail-1',visibleValue:'详情预览'}]:mode==='saved-file-thumbnail'?[{label:'主图',category:'图文',key:'remote-main-image',visibleValue:'已保存远程主图预览'}]:mode==='image-noise'?[{label:'主图',category:'物流',key:'template-thumb',visibleValue:'模板缩略图'},{label:'详情图',category:'规格',key:'add-image-icon',visibleValue:'添加图标'}]:[];
   const categoryByLabel={'颜色':'规格','颜色 *':'规格','尺码':'规格','库存':'规格','主图':'图文','详情图':'图文','详情图片':'图文','详情文案':'图文','运费模板':'物流','发货地':'物流','退货承诺':'售后','售后说明':'售后','材质':'规格'};
   if(!['generic-section','generic-rule-fields'].includes(mode))controls=controls.map(control=>{const field=String(control.fieldLabel||control.label).trim().replace(/\s*[:：]\s*$/,'').replace(/^[*＊]\s*|\s*[*＊]\s*$/g,'').replace(/\s*[（(]必填[）)]$/,'');return {...control,category:control.category||categoryByLabel[field]};});
   // This mode mirrors explicit-control-association.html after the scanner
   // has applied only label[for]/wrapping-label/aria-labelledby association.
   // The unlabelled input is deliberately absent: a surrounding “规格” title
   // or sibling .label must never name it.
   if(mode==='explicit-control-association')controls=[{label:'颜色',category:'规格',visibleValue:'蓝色'}];
   if(mode==='placeholder-example')controls=[{label:'颜色',fieldLabel:'颜色',category:'规格',visibleValue:'',pending:true}];
   if(mode==='placeholder-dashes')controls=[{label:'运费模板',fieldLabel:'运费模板',category:'物流',visibleValue:'',pending:true}];
   if(mode==='generic-section')controls=[{label:'颜色',fieldLabel:'规格',category:'规格',visibleValue:'蓝色'}];
   if(mode==='generic-rule-fields')controls=[{label:'运费模板',fieldLabel:'运费模板',visibleValue:'包邮模板'},{label:'退货承诺',fieldLabel:'退货承诺',visibleValue:'7天无理由退货'}];
   result={text,pairs,controls,images};
  }else result={};
 }else if(action==='close_session')result={closed:1};else process.exit(1);
}else if(verb==='snapshot'){
 let snapshotCount=0;
 if(process.env.LISTING_TEST_TRACE){try{snapshotCount=readFileSync(process.env.LISTING_TEST_TRACE,'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(x=>x.action==='snapshot').length+1}catch{}}
 if(process.env.LISTING_TEST_TRACE)appendFileSync(process.env.LISTING_TEST_TRACE,JSON.stringify({action:'snapshot'})+'\n');
 const interactive=['蓝色','M','20','已上传','三张','纯棉短袖','包邮模板','杭州','7天退货','联系客服','','纯棉'].map((value,i)=>({ref:`@e${i+1}`,tag:'input',role:'textbox',text:value,value,visible:true,disabled:false}));
 result={title:'商品编辑',url:mode==='redirected-page'?'https://example.invalid/other?access_token=secret-value':'https://example.invalid/edit?access_token=secret-value&signature=abc#private',text:'颜色：蓝色\n尺码：M\n库存：20\n主图：已上传\n详情图：三张\n详情文案：纯棉短袖\n运费模板：包邮模板\n发货地：杭州\n退货承诺：7天退货\n售后说明：联系客服\n材质：纯棉',interactive};
 if(mode==='normal-copy')result.text='图片加载失败说明\n买家登录后可见\n颜色：蓝色';
 if(mode==='empty'){result.text='颜色：';result.interactive=[{ref:'@e1',tag:'input',role:'textbox',text:'颜色',value:'',visible:true,disabled:false}];}
 if(mode==='pending-control'){result.text='颜色';result.interactive=[{ref:'@e1',tag:'input',role:'textbox',text:'颜色',value:'未确认',visible:true,disabled:false}];}
 if(mode==='async-hydration'&&snapshotCount<3){result.text='商品信息正在加载';result.interactive=[];}
 if(mode==='async-hydration'&&snapshotCount>=3){result.text='颜色：蓝色';result.interactive=[{ref:'@e1',tag:'input',role:'textbox',text:'颜色',value:'蓝色',visible:true,disabled:false}];}
 if(mode==='text-wins'){result.text='颜色：页面文本蓝色';result.interactive=[{ref:'@e1',tag:'select',role:'combobox',text:'颜色',value:'internal-code',visible:true,disabled:false}];}
 if(mode==='adjacent-labels'){result.text='颜色\n库存\n请填写商品库存\n尺码：M';result.interactive=[];}
 if(mode==='label-help'){result.text='库存 - 请填写商品库存\n尺码：M';result.interactive=[];}
 if(mode==='designing'){result.text='Designing a new product listing';result.interactive=[];}
 if(mode==='hidden-text')result.text='颜色：隐藏区域里的红色\n尺码：M';
 // This is deliberately shaped like an Easy WebBridge snapshot: controls
 // expose their current visible value, not a synthetic label/name attribute.
 if(mode==='controls-only'){result.text='颜色\n尺码\n库存\n主图\n详情图\n详情文案\n运费模板\n发货地\n退货承诺\n售后说明\n材质';result.interactive=result.interactive.filter(item=>item.value!=='');}
 if(mode==='login'){result.title='账号中心 - 登录';result.text='欢迎回来';}
 if(mode==='truncated')result.textTruncated=true;
 if(mode==='malformed'){console.log(result.text);process.exit(0);}
}else process.exit(1);
console.log(JSON.stringify({ok:true,result}));
