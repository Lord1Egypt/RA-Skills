#!/usr/bin/env node
"use strict";var K=Object.create;var A=Object.defineProperty;var _=Object.getOwnPropertyDescriptor;var L=Object.getOwnPropertyNames;var O=Object.getPrototypeOf,E=Object.prototype.hasOwnProperty;var q=(e,o,n,i)=>{if(o&&typeof o=="object"||typeof o=="function")for(let s of L(o))!E.call(e,s)&&s!==n&&A(e,s,{get:()=>o[s],enumerable:!(i=_(o,s))||i.enumerable});return e};var $=(e,o,n)=>(n=e!=null?K(O(e)):{},q(o||!e||!e.__esModule?A(n,"default",{value:e,enumerable:!0}):n,e));var p=require("fs"),h=require("path"),S=require("os"),C=require("http"),b=require("crypto"),x=(0,h.join)((0,S.homedir)(),".config","vanio"),m=(0,h.join)(x,"config.json"),v="https://api.vanio.ai",y="/v1";function u(){try{return JSON.parse((0,p.readFileSync)(m,"utf-8"))}catch{return{}}}function f(e){(0,p.mkdirSync)(x,{recursive:!0}),(0,p.writeFileSync)(m,JSON.stringify(e,null,2))}function V(){let e=process.env.VANIO_API_KEY;if(e)return e;let o=u();if(o.apiKey)return o.apiKey;console.error("Error: No API key configured."),console.error("Run: vanio login <api-key>"),console.error("Or set VANIO_API_KEY environment variable."),process.exit(1)}function N(){return process.env.VANIO_API_URL||u().baseUrl||v}async function k(e,o="GET",n){let i=`${N()}${e}`,s=V(),t=await fetch(i,{method:o,headers:{"Content-Type":"application/json","x-api-key":s},...n?{body:JSON.stringify(n)}:{}});if(!t.ok){let r=await t.json().catch(()=>({message:t.statusText}));console.error(`Error ${t.status}: ${r.message||r.error||t.statusText}`),process.exit(1)}return t.json()}async function R(e){if(e[0]&&!e[0].startsWith("--")){let a=u();a.apiKey=e[0],f(a),console.log("API key saved to ~/.config/vanio/config.json");return}let o=process.env.VANIO_API_URL||u().baseUrl||v,n=(0,b.randomBytes)(16).toString("hex"),i=(0,C.createServer)((a,c)=>{let g=new URL(a.url||"/","http://127.0.0.1");if(g.pathname==="/callback"){let I=g.searchParams.get("key"),U=g.searchParams.get("state"),T=g.searchParams.get("user")||"";if(U!==n){c.writeHead(400,{"Content-Type":"text/html"}),c.end("<h1>State mismatch \u2014 login aborted</h1><p>Close this tab and try again.</p>"),i.close(),console.error("Error: state mismatch. Possible CSRF attack. Try again."),process.exit(1);return}if(!I){c.writeHead(400,{"Content-Type":"text/html"}),c.end("<h1>No API key received</h1><p>Close this tab and try again.</p>"),i.close(),console.error("Error: no API key received from server."),process.exit(1);return}let d=u();d.apiKey=I,d.baseUrl=o,f(d),c.writeHead(200,{"Content-Type":"text/html"}),c.end(`
        <html>
          <head><title>Vanio CLI</title></head>
          <body style="font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #0a0a0a; color: #fff;">
            <div style="text-align: center;">
              <h1 style="font-size: 2rem;">\u2713 Logged in to Vanio</h1>
              <p style="color: #888;">You can close this tab and return to your terminal.</p>
            </div>
          </body>
          <script>history.replaceState(null, '', '/')</script>
        </html>
      `),console.log(`
Logged in as ${T||"unknown"}`),console.log("API key saved to ~/.config/vanio/config.json"),setTimeout(()=>{i.close(),process.exit(0)},1e3);return}c.writeHead(404),c.end()});await new Promise(a=>{i.listen(0,"127.0.0.1",()=>a())});let s=i.address().port,t=`${o}${y}/auth/cli?port=${s}&state=${n}`;console.log("Opening browser to authenticate..."),console.log(`If it doesn't open, visit: ${t}`);let{exec:r}=await import("child_process"),l=process.platform==="darwin"?`open "${t}"`:process.platform==="win32"?`start "${t}"`:`xdg-open "${t}"`;r(l),console.log("Waiting for authentication..."),setTimeout(()=>{console.error(`
Login timed out. Try again.`),i.close(),process.exit(1)},12e4)}async function w(e){let o=e.join(" ");o||(console.error("Usage: vanio ask <question>"),console.error('       vanio ask "What are my check-ins today?"'),process.exit(1));let n={query:o};for(let t=0;t<e.length;t++)e[t]==="--reservation"&&e[t+1]?n.reservationId=parseInt(e[++t],10):e[t]==="--listing"&&e[t+1]?n.listingId=parseInt(e[++t],10):e[t]==="--thread"&&e[t+1]&&(n.threadId=e[++t]);let i=e.filter((t,r)=>!(t.startsWith("--")||r>0&&e[r-1].startsWith("--")));n.query=i.join(" "),n.query||(console.error("No query provided."),process.exit(1));let s=await k(`${y}/chat`,"POST",n);if(console.log(s.answer),s.sources?.length){console.log(""),console.log("Sources:");for(let t of s.sources)console.log(`  - ${t.label} (${t.type})`)}s.usage&&console.error(`
[${s.usage.model} | ${s.usage.inputTokens+s.usage.outputTokens} tokens | $${s.usage.cost?.toFixed(4)||"?"}]`)}async function j(e){let n=(await import("readline")).createInterface({input:process.stdin,output:process.stdout}),i=`cli-${Date.now()}`,s=[];console.log('Vanio AI \u2014 interactive chat (type "exit" to quit)'),console.log("\u2500".repeat(50));let t=()=>{n.question(`
You: `,async r=>{let l=r.trim();if(!l||l==="exit"||l==="quit"){n.close();return}s.push({role:"user",content:l});let a=await k(`${y}/chat`,"POST",{query:l,threadId:i,conversationHistory:s.slice(-20)});console.log(`
Vanio: ${a.answer}`),s.push({role:"assistant",content:a.answer}),t()})};t()}async function F(){let e=await k(`${y}/chat`,"GET");console.log(`Service: ${e.service}`),console.log(`Version: ${e.version}`),console.log(`Tools:   ${e.tools}`),console.log(`Status:  ${e.status}`)}async function W(e){let o=u();if(e[0]==="set"&&e[1]&&e[2]){let n=e[1];n==="apiKey"||n==="baseUrl"?(o[n]=e[2],f(o),console.log(`Set ${n} = ${e[2]}`)):console.error(`Unknown config key: ${n}. Valid keys: apiKey, baseUrl`);return}if(e[0]==="get"&&e[1]){console.log(o[e[1]]||"(not set)");return}console.log(`API Key:  ${o.apiKey?o.apiKey.slice(0,8)+"...":"(not set)"}`),console.log(`Base URL: ${o.baseUrl||v}`),console.log(`Config:   ${m}`)}function P(){console.log(`
Vanio AI CLI \u2014 manage your vacation rental portfolio via AI

Usage:
  vanio <command> [options]

Commands:
  login                    Authenticate via browser (opens Vanio dashboard)
  login <api-key>          Authenticate with an API key directly
  logout                   Remove saved credentials
  ask <question>           Ask Vanio AI a question (single query)
  chat                     Start interactive conversation
  status                   Check API connection
  config                   Show current configuration
  config set <key> <val>   Set config value (apiKey, baseUrl)
  help                     Show this help

Ask Options:
  --reservation <id>       Scope question to a specific reservation
  --listing <id>           Scope question to a specific listing
  --thread <id>            Continue a conversation thread

Examples:
  vanio ask "What are today's check-ins?"
  vanio ask "What's the WiFi password at Alpine Lodge?" --listing 42
  vanio ask "Why was this guest charged extra?" --reservation 214303
  vanio chat
  vanio config set baseUrl https://api.vanio.ai

Environment:
  VANIO_API_KEY            API key (overrides config file)
  VANIO_API_URL            Base URL (overrides config file)
`.trim())}async function H(){let[e,...o]=process.argv.slice(2);switch(e){case"login":return R(o);case"logout":{let n=u();delete n.apiKey,f(n),console.log("Logged out. API key removed.");return}case"ask":return w(o);case"chat":return j(o);case"status":return F();case"config":return W(o);case"help":case"--help":case"-h":return P();case void 0:P();break;default:return w([e,...o])}}H().catch(e=>{console.error(e.message||e),process.exit(1)});
