'use strict'

const { profiles, pageProfile } = require('./account-profile')
const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]))

// Official icon from public/agentcy.svg and Vibbit wordmark from Logo.tsx.
// Inline SVG keeps both regional and flattened packages independent of web assets.
const brandIcon = `<svg class="brand-icon" aria-hidden="true" width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="64" height="64" rx="20" fill="black"/>
<path d="M40.1768 17.0215L33.1765 33.0219" stroke="white" stroke-width="8" stroke-linecap="round"/>
<path d="M18.0803 21.0221L33.1768 33.0215" stroke="white" stroke-width="8" stroke-linecap="round"/>
<path d="M17.6768 42.0215L33.1795 33.0196" stroke="white" stroke-width="8" stroke-linecap="round"/>
<g filter="url(#filter0_f_2084_1165)">
<circle cx="32.6768" cy="32.5215" r="7" fill="black"/>
</g>
<g filter="url(#filter1_f_2084_1165)">
<circle cx="32.6768" cy="32.5215" r="8" fill="black"/>
</g>
<g filter="url(#filter2_f_2084_1165)">
<circle cx="32.6768" cy="32.5215" r="12" fill="black"/>
</g>
<path d="M34.075 32.068L49.5746 36.3802C50.5924 36.6634 50.5329 38.1261 49.4954 38.3256L41.4879 39.8655C41.0171 39.956 40.6768 40.368 40.6768 40.8475L40.6768 47.4221C40.6768 48.5193 39.1652 48.8158 38.7508 47.7998L32.8811 33.4091C32.5672 32.6396 33.2744 31.8453 34.075 32.068Z" fill="url(#paint0_linear_2084_1165)" stroke="url(#paint1_linear_2084_1165)" stroke-width="6"/>
<defs>
<filter id="filter0_f_2084_1165" x="15.6768" y="15.5215" width="34" height="34" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="5" result="effect1_foregroundBlur_2084_1165"/>
</filter>
<filter id="filter1_f_2084_1165" x="14.6768" y="14.5215" width="36" height="36" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="5" result="effect1_foregroundBlur_2084_1165"/>
</filter>
<filter id="filter2_f_2084_1165" x="10.6768" y="10.5215" width="44" height="44" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="5" result="effect1_foregroundBlur_2084_1165"/>
</filter>
<linearGradient id="paint0_linear_2084_1165" x1="42.8993" y1="34.5023" x2="38.1163" y2="51.8141" gradientUnits="userSpaceOnUse">
<stop stop-color="#FF7373"/>
<stop offset="1" stop-color="#FE5733"/>
</linearGradient>
<linearGradient id="paint1_linear_2084_1165" x1="42.8993" y1="34.5023" x2="38.1163" y2="51.8141" gradientUnits="userSpaceOnUse">
<stop stop-color="#FF7373"/>
<stop offset="1" stop-color="#FE5127"/>
</linearGradient>
</defs>
</svg>`
const brandWordmark = `<svg width="123" height="27" viewBox="0 0 123 27" fill="none" xmlns="http://www.w3.org/2000/svg" class="brand-wordmark" aria-hidden="true" > <path d="M44.8447 1.14453L44.8447 25.8015" stroke="currentColor" stroke-width="5.71986" /> <path d="M70.6465 1.14453L70.6465 25.8015" stroke="currentColor" stroke-width="5.71986" /> <circle cx="52.8053" cy="15.6217" r="7.92544" stroke="currentColor" stroke-width="5.71986" /> <circle cx="78.6051" cy="15.6217" r="7.92544" stroke="currentColor" stroke-width="5.71986" /> <path d="M96.4463 9.15186L96.4463 25.801" stroke="currentColor" stroke-width="5.71986" /> <path d="M32.8691 9.15186L32.8691 25.801" stroke="currentColor" stroke-width="5.71986" /> <path d="M118.836 10.356L107.396 10.356" stroke="currentColor" stroke-width="5.71986" /> <path d="M121.124 22.9399L115.633 22.8891C111.084 22.8891 107.396 19.4018 107.396 15.0999V1.14404" stroke="currentColor" stroke-width="5.71986" /> <circle cx="33.0784" cy="3.43192" r="3.43192" fill="currentColor" /> <circle cx="95.9973" cy="3.43192" r="3.43192" fill="currentColor" /> <path d="M19.1133 23.1128C17.7671 26.883 12.5703 27.2289 10.7363 23.6704L2 6.72021L5.05078 5.14795L8.10254 3.57568L14.4219 15.8394L19.5156 1.57666H26.8037L19.1133 23.1128Z" fill="currentColor" /> </svg>`

function setupPage(nonce, profile = pageProfile('global'), regionLocked = false) {
  const t = profile.text
  const text = JSON.stringify(t).replace(/</g, '\\u003c')
  const sites = JSON.stringify(Object.fromEntries(Object.values(profiles).map(p => [p.region, p.webBase + '/api-keys'])))
  return `<!doctype html>
<html lang="${profile.lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escape(t.title)}</title>
<style nonce="${nonce}">
:root{color-scheme:light;--page:#fafafa;--card:#fff;--text:#171717;--muted:#737373;--line:#e5e5e5;--soft:#f5f5f5;--primary:#171717;--on-primary:#fafafa;--error:#b42318}
*{box-sizing:border-box}[hidden]{display:none!important}
body{margin:0;background:var(--page);color:var(--text);font:14px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}
main{width:calc(100% - 32px);max-width:520px;margin:8vh auto;padding:36px;background:var(--card);border:1px solid var(--line);border-radius:20px;box-shadow:0 8px 32px #00000005}
.header{display:flex;align-items:center}
.brand{display:flex;align-items:center;gap:11px;color:var(--text)}.brand-icon{width:36px;height:36px;flex:none}.brand-wordmark{width:87px;height:auto}
h1{font-size:25px;font-weight:600;line-height:1.4;letter-spacing:-.5px;margin:30px 0 8px}
.intro{color:var(--muted);margin:0 0 28px}.note{color:var(--muted);font-size:12px;line-height:1.7}
.step{display:flex;align-items:center;gap:9px;margin:0 0 12px;font-size:14px;font-weight:600}
.step-number{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;flex:none;border:1px solid var(--line);border-radius:50%;font-size:12px;font-weight:500}
.create-step{padding-bottom:24px;margin-bottom:24px;border-bottom:1px solid var(--line)}
a{color:var(--text);text-underline-offset:4px}.create-link{display:inline-flex;align-items:center;justify-content:space-between;gap:12px;width:100%;padding:12px 14px;background:var(--soft);border:1px solid var(--line);border-radius:12px;text-decoration:none;transition:background .15s,border-color .15s}.create-link:hover{background:var(--card);border-color:var(--muted)}.create-link svg{width:16px;height:16px;flex:none}
label{display:block;font-size:13px;font-weight:500;margin-bottom:7px}
input,select{display:block;width:100%;min-height:46px;padding:11px 14px;font:inherit;color:var(--text);background:var(--soft);border:1px solid var(--line);border-radius:12px;outline:none;transition:border-color .15s,box-shadow .15s}
input::placeholder{color:var(--muted)}input:focus{background:var(--card);border-color:var(--muted);box-shadow:0 0 0 3px #73737315}
button{min-height:44px;padding:11px 18px;font:inherit;font-weight:500;border:1px solid transparent;border-radius:12px;cursor:pointer;transition:opacity .15s,background .15s}button:disabled{opacity:.5;cursor:default}button:focus-visible,a:focus-visible{outline:2px solid var(--muted);outline-offset:3px}
.primary{background:var(--primary);color:var(--on-primary);flex:1}.primary:hover:enabled{opacity:.88}.secondary{background:var(--card);border-color:var(--line);color:var(--muted)}.secondary:hover:enabled{background:var(--soft);color:var(--text)}.actions{display:flex;gap:10px;margin-top:24px}
#status{display:flex;align-items:flex-start;gap:10px;margin:20px 0 0;padding:12px 14px;background:var(--soft);border:1px solid var(--line);border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere}#status[data-state=error]{color:var(--error)}#status[data-state=success]{color:var(--text)}#success-mark{display:flex;flex:none;margin-top:1px}#success-mark svg{width:20px;height:20px}
footer{margin-top:24px;border-top:1px solid var(--line);padding-top:16px}.storage-title{margin:0;font-size:12px;font-weight:500}footer p{margin:8px 0 0}
@media(prefers-color-scheme:dark){:root{color-scheme:dark;--page:#171717;--card:#262626;--text:#fafafa;--muted:#a3a3a3;--line:#404040;--soft:#303030;--primary:#e5e5e5;--on-primary:#171717;--error:#fda29b}}
@media(max-width:560px){main{margin:24px auto;padding:24px}h1{font-size:23px}.intro{margin-bottom:24px}}
</style></head><body><main><header class="header"><div class="brand" role="img" aria-label="Vibbit">${brandIcon}${brandWordmark}</div></header>
<h1>${escape(t.title)}</h1><p class="intro">${escape(t.intro)}</p>
<form id="setup" autocomplete="off"><label for="region">${escape(t.site)}</label><select id="region" aria-describedby="sites-note"${regionLocked ? ' disabled' : ''}><option value="global"${profile.region === 'global' ? ' selected' : ''}>${escape(t.international)} · app.vibbit.ai</option><option value="cn"${profile.region === 'cn' ? ' selected' : ''}>${escape(t.china)} · app.vibbit.cn</option></select><p class="note" id="sites-note">${escape(t.separate)}</p>
<section class="create-step" aria-labelledby="create-title"><h2 class="step" id="create-title"><span class="step-number" aria-hidden="true">1</span>${escape(t.step1)}</h2><a id="create-key" class="create-link" href="${escape(profile.webBase + '/api-keys')}" target="_blank" rel="noopener noreferrer"><span>${escape(t.create)}</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3h7v7M21 3l-9 9M10 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5"/></svg></a></section>
<h2 class="step"><span class="step-number" aria-hidden="true">2</span>${escape(t.step2)}</h2><label for="key">${escape(t.label)}</label>
<input id="key" name="key" type="password" required maxlength="4096" placeholder="${escape(t.placeholder)}" autocomplete="off" spellcheck="false" autocapitalize="none" aria-describedby="privacy">
<p class="note" id="privacy">${escape(t.privacy)}</p>
<div class="actions"><button class="primary" type="submit" id="submit">${escape(t.submit)}</button><button class="secondary" type="button" id="cancel">${escape(t.cancel)}</button></div>
</form><div id="status" role="status" aria-live="polite" aria-atomic="true" hidden><span id="success-mark" aria-hidden="true" hidden><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/></svg></span><span id="status-text"></span></div><footer class="note"><h2 class="storage-title">${escape(t.storageTitle)}</h2><p>${escape(t.storage)}</p></footer></main>
<script nonce="${nonce}">
const text=${text}; const form=document.getElementById('setup'), key=document.getElementById('key'), status=document.getElementById('status'), statusText=document.getElementById('status-text'), successMark=document.getElementById('success-mark'), submit=document.getElementById('submit'), cancel=document.getElementById('cancel');
const sites=${sites}, region=document.getElementById('region'), regionLocked=${regionLocked};
region.addEventListener('change',()=>{key.value='';document.getElementById('create-key').href=sites[region.value];status.hidden=true;});
function message(value,state){statusText.textContent=value;successMark.hidden=state!=='success';status.dataset.state=state;status.hidden=false;}
form.addEventListener('submit',async event=>{event.preventDefault();submit.disabled=cancel.disabled=region.disabled=true;message(text.pending,'pending');
try{const body=JSON.stringify({key:key.value.trim(),region:region.value}); key.value='';const response=await fetch('verify',{method:'POST',headers:{'Content-Type':'application/json'},body});const result=await response.json();if(result.ok){form.hidden=true;message(text.success,'success');return;}message(text[result.reason]||text.transport,'error');if(result.reason==='expired'){form.hidden=true;return;}}
catch{message(text.expired,'error');}submit.disabled=cancel.disabled=false;region.disabled=regionLocked;key.focus();});
cancel.addEventListener('click',async()=>{key.value='';try{const response=await fetch('cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});if(!response.ok)return;form.hidden=true;message(text.cancelled,'cancelled');}catch{form.hidden=true;message(text.expired,'error');}});
</script></body></html>`
}

module.exports = { setupPage }
