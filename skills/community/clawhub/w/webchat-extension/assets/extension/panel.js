// panel.js —— 对话浮层（chrome-extension 页面）
// 职责：管理「上下文片段列表」、收发消息、流式渲染 AI 回复
// 上下文来源：
//   1) 「添加选中文本」按钮：读取网页选区(经 background 用 chrome.scripting.executeScript 跨 iframe 直读) + 读取系统剪切板(输入法/网页复制都在这)
//   2) 发送问题时：自动把本次内容(剪贴板或提问文本)收进上下文
// 上下文片段只读预览(10~20 字 + …)，不可直接编辑；要改就在提问框重新粘贴/输入
// 持久化：上下文片段与对话内容存 chrome.storage，刷新后自动恢复
// 浮层可拖动：标题栏按下发起点偏移，拖拽由 content.js 全屏遮罩同步接管（零往返、丝滑跟手）；双击标题栏复位
(async function () {
  const BACKEND = "http://localhost:3000";
  // 后端未启动时的「复制启动命令」内容（通用提示：先 cd 到自己的 backend 目录再 npm start）
  const BACKEND_START_CMD = "npm start   # 先 cd 到你的 backend 目录";
  let backendOnline = null; // null=检测中/未知, true=在线, false=离线

  const messagesEl = document.getElementById("messages");
  const inputEl = document.getElementById("input");
  const sendBtn = document.getElementById("sendBtn");
  const closeBtn = document.getElementById("closeBtn");
  const addSelBtn = document.getElementById("addSelBtn");
  const ctxListEl = document.getElementById("ctxList");
  const pageInfoEl = document.getElementById("pageInfo");
  const addStatusEl = document.getElementById("addStatus");
  const headerEl = document.getElementById("panelHeader");

  let pageInfo = { title: "", url: "" };
  let contexts = []; // 多个上下文片段（string，只读）
  let messages = []; // {role:'user'|'assistant', content}
  let pendingClip = ""; // 按钮 mousedown 时同步抢读的剪切板

  // ---------- 存储 ----------
  function save(key, val) {
    try {
      chrome.storage.local.set({ [key]: val });
    } catch (_) {}
  }
  function load(key, cb) {
    try {
      chrome.storage.local.get(key, (r) => cb(r ? r[key] : undefined));
    } catch (_) {
      cb(undefined);
    }
  }
  function saveContexts() {
    save("wx_contexts", contexts);
  }
  function saveMessages() {
    save("wx_messages", messages.map((m) => ({ role: m.role, content: m.content })));
  }

  // ---------- 上下文片段管理 ----------
  function renderContexts() {
    ctxListEl.innerHTML = "";
    if (contexts.length === 0) {
      const empty = document.createElement("div");
      empty.className = "ctx-empty";
      empty.textContent =
        "还没有上下文。在网页选中文字点「添加选中文本」，或复制文字后点它（会读取系统剪切板，含输入法复制）；发送问题时也会自动收进上下文。";
      ctxListEl.appendChild(empty);
      return;
    }
    contexts.forEach((txt, i) => {
      const item = document.createElement("div");
      item.className = "ctx-item";
      const preview = document.createElement("span");
      preview.className = "ctx-preview";
      // 只显示 10~20 字摘要 + 省略号，全文放在 title 悬停查看
      preview.textContent = txt.length > 20 ? txt.slice(0, 20) + "…………" : txt;
      preview.title = txt;
      const del = document.createElement("button");
      del.className = "ctx-del";
      del.textContent = "✕";
      del.title = "删除该片段";
      del.addEventListener("click", () => {
        contexts.splice(i, 1);
        renderContexts();
        saveContexts();
      });
      item.appendChild(preview);
      item.appendChild(del);
      ctxListEl.appendChild(item);
    });
  }

  // 加入上下文（去重：完全一样不重复加）。返回是否真的加进去了
  function addContext(text) {
    text = (text || "").trim();
    if (!text) return false;
    if (contexts.some((c) => c === text)) return false;
    contexts.push(text);
    renderContexts();
    saveContexts();
    return true;
  }

  function flash(text, isError) {
    addStatusEl.textContent = text;
    addStatusEl.className = "add-status" + (isError ? " err" : "");
    clearTimeout(flash._t);
    flash._t = setTimeout(() => {
      addStatusEl.textContent = "";
      addStatusEl.className = "add-status";
    }, 2800);
  }

  // ---------- 后端在线检测（离线时提示并给启动命令） ----------
  function setOfflineUI(offline) {
    const el = document.getElementById("backendOffline");
    if (el) el.hidden = !offline;
    const statusEl = document.getElementById("backendStatus");
    if (statusEl) statusEl.hidden = offline; // 在线才显示「● 后端在线 · 停止」
  }
  async function checkBackend() {
    try {
      const r = await fetch(BACKEND + "/api/health", { cache: "no-store" });
      backendOnline = !!r.ok;
    } catch (_) {
      backendOnline = false;
    }
    setOfflineUI(backendOnline === false);
    return backendOnline;
  }

  // ---------- 读取网页选区（经 background，chrome.scripting.executeScript 跨 iframe 直读） ----------
  function getSelectionText() {
    return new Promise((resolve) => {
      let done = false;
      const finish = (t) => {
        if (done) return;
        done = true;
        resolve((t || "").trim());
      };
      try {
        chrome.runtime.sendMessage({ type: "GET_SELECTION" }, (resp) => {
          finish((resp && resp.text) || "");
        });
      } catch (_) {
        finish("");
      }
      // 兜底：1.5s 内没回应就当没选到
      setTimeout(() => finish(""), 1500);
    });
  }

  // ---------- 读取系统剪切板（含输入法复制） ----------
  // 方法B（同步，趁用户手势）：传统 execCommand('paste')，需在文档聚焦+用户手势内调用
  function readClipboardSync() {
    try {
      const ta = document.createElement("textarea");
      ta.style.cssText = "position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;";
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      let v = "";
      try {
        if (document.execCommand("paste")) v = ta.value;
      } catch (_) {}
      document.body.removeChild(ta);
      return (v || "").trim();
    } catch (_) {
      return "";
    }
  }
  // 方法A（异步，现代 API，需用户手势/文档聚焦）：navigator.clipboard.readText
  async function readClipboardAsync() {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const t = (await navigator.clipboard.readText()).trim();
        if (t) return t;
      }
    } catch (_) {}
    return "";
  }
  async function readClipboard() {
    const a = await readClipboardAsync();
    if (a) return a;
    return readClipboardSync();
  }

  // ---------- 对话渲染 ----------
  function addMessage(role, content) {
    const el = document.createElement("div");
    el.className = "msg " + role;
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = content;
    el.appendChild(bubble);
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    const msg = { role: role, content: content, el: el, bubble: bubble };
    messages.push(msg);
    return msg;
  }

  function renderMessages() {
    messagesEl.innerHTML = "";
    messages.forEach((m) => {
      const el = document.createElement("div");
      el.className = "msg " + m.role;
      const bubble = document.createElement("div");
      bubble.className = "bubble";
      bubble.textContent = m.content;
      el.appendChild(bubble);
      messagesEl.appendChild(el);
    });
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function appendToMessage(msg, text) {
    msg.content += text;
    msg.bubble.textContent = msg.content;
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function send() {
    const q = inputEl.value.trim();
    if (!q) return;
    if (backendOnline === false) {
      setOfflineUI(true);
      flash("后端未启动，点上方「🚀 启动后端」即可自动拉起", true);
      return;
    }
    addMessage("user", q);
    inputEl.value = "";
    saveMessages();

    // 自动把本次内容收进上下文：优先系统剪切板（用户复制/输入法复制的素材），没有就收提问文本
    const clip = await readClipboard();
    let autoAdded = 0;
    if (clip) {
      if (addContext(clip)) autoAdded++;
    } else if (q) {
      if (addContext(q)) autoAdded++;
    }
    if (autoAdded > 0) flash("已自动把内容加入上下文");

    const assistant = addMessage("assistant", "");

    const history = messages
      .filter((m) => m.role !== "assistant" || m !== assistant)
      .map((m) => ({ role: m.role, content: m.content }));

    const body = {
      context: contexts.join("\n---\n"),
      question: q,
      history: history,
      pageTitle: pageInfo.title,
      pageUrl: pageInfo.url,
    };

    try {
      const resp = await fetch(BACKEND + "/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!resp.ok && resp.status !== 200) {
        appendToMessage(assistant, "⚠️ 后端返回错误：" + resp.status);
        saveMessages();
        return;
      }
      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        let idx;
        while ((idx = buf.indexOf("\n\n")) >= 0) {
          const raw = buf.slice(0, idx);
          buf = buf.slice(idx + 2);
          const line = raw.split("\n").find((l) => l.startsWith("data: "));
          if (!line) continue;
          let json;
          try {
            json = JSON.parse(line.slice(6));
          } catch (_) {
            continue;
          }
          if (json.type === "text") {
            appendToMessage(assistant, json.content);
          } else if (json.type === "error") {
            appendToMessage(assistant, "\n⚠️ " + json.message);
          } else if (json.type === "done") {
            // 完成
          }
        }
      }
      saveMessages();
    } catch (e) {
      appendToMessage(
        assistant,
        "⚠️ 连接后端失败：" + e.message + "\n（请确认后端已启动：cd backend && npm start）"
      );
      saveMessages();
    }
  }

  // ---------- 来自 content.js 的消息 ----------
  window.addEventListener("message", function (ev) {
    const d = ev.data;
    if (!d || !d.type) return;
    if (d.type === "INIT_PAGE") {
      pageInfo = d.info || pageInfo;
      pageInfoEl.textContent = "来自：" + (pageInfo.title || pageInfo.url || "未知网页");
      pageInfoEl.title = pageInfo.url || "";
    }
  });

  // ---------- 标题栏拖拽 ----------
  // 按下只发一次起点偏移给 content.js，后续由本页全屏遮罩同步接管（零往返、不抖动）
  if (headerEl) {
    headerEl.style.touchAction = "none";
    headerEl.addEventListener("pointerdown", (e) => {
      if (e.target.closest("#closeBtn")) return; // 点关闭按钮不触发拖拽
      e.preventDefault();
      // e.clientX/Y 是相对于面板(iframe)自身视口的偏移，content.js 会加上面板页面坐标
      window.parent.postMessage(
        { type: "DRAG_START", offsetX: e.clientX, offsetY: e.clientY },
        "*"
      );
    });
    // 双击标题栏复位到默认右上角
    headerEl.addEventListener("dblclick", (e) => {
      if (e.target.closest("#closeBtn")) return;
      window.parent.postMessage({ type: "RESET_PANEL_POS" }, "*");
    });
  }

  // ---------- 「添加选中文本」：网页选区 + 系统剪切板(含输入法复制) ----------
  // mousedown 时趁手势同步抢读剪切板（execCommand 最稳，避免 click 里 await 后手势过期）
  addSelBtn.addEventListener("mousedown", (e) => {
    e.preventDefault();
    pendingClip = readClipboardSync();
  });
  addSelBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const clip = pendingClip || (await readClipboard());
    const sel = await getSelectionText();
    let added = 0;
    if (sel) {
      if (addContext(sel)) added++;
    }
    if (clip && clip !== sel) {
      if (addContext(clip)) added++;
    }
    if (added > 0) flash("已添加 " + added + " 段内容到上下文");
    else
      flash(
        "没抓到选中文字或剪切板内容。微信读书可能屏蔽了复制/选区读取，请直接把文字粘贴或输入到下方输入框发送（发送会自动收进上下文）",
        true
      );
  });

  sendBtn.addEventListener("click", send);
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });
  closeBtn.addEventListener("click", function () {
    window.parent.postMessage({ type: "CLOSE_PANEL" }, "*");
  });

  // ---------- 后端启动：一键拉起（webchat:// 协议，无需终端） ----------
  // 后端生命周期由「扩展心跳」托管：浏览器关→心跳断→后端自退，跨浏览器通用，无需传浏览器名。
  // 这里仍顺手识别一下当前浏览器名，仅用于给用户看一眼（不影响生命周期）。
  function detectBrowserName() {
    const ua = (navigator.userAgent || "").toLowerCase();
    if (ua.includes("edg/")) return "Edge";
    if (ua.includes("quark")) return "夸克";
    if (ua.includes("qianwen") || ua.includes("qwen")) return "千问";
    if (ua.includes("opr/") || ua.includes("opera")) return "Opera";
    if (ua.includes("firefox") || ua.includes("fxios")) return "Firefox";
    if (ua.includes("brave")) return "Brave";
    if (ua.includes("chrome")) return "Chrome";
    if (ua.includes("ucbrowser")) return "UC";
    return "当前浏览器";
  }
  function launchViaProtocol() {
    try {
      // 协议跳转必须在真实网页顶层文档里触发（扩展 iframe 内的 window.open 会被浏览器静默拦截）。
      // 通过 window.parent 让 content.js（运行在真实网页上下文）注入隐藏 iframe 指向 webchat://start。
      window.parent.postMessage({ type: "LAUNCH_BACKEND" }, "*");
      const bn = detectBrowserName();
      flash("已请求启动后端（" + bn + "），正在等待本地服务就绪…");
      // 乐观复查：稍后轮询会正式隐藏横幅
      setTimeout(() => checkBackend(), 2500);
    } catch (_) {
      flash("无法自动启动，请用「复制启动命令」手动启动", true);
    }
  }

  const startBtn = document.getElementById("startBtn");
  const copyStartBtn = document.getElementById("copyStartBtn");
  const startCmdPreview = document.getElementById("startCmdPreview");
  const stopBtn = document.getElementById("stopBtn");
  if (startCmdPreview) startCmdPreview.textContent = BACKEND_START_CMD;
  if (startBtn) {
    startBtn.addEventListener("click", () => {
      startBtn.disabled = true;
      startBtn.textContent = "⏳ 正在启动…";
      launchViaProtocol();
      // 若协议未注册/被拦，3s 后恢复按钮，保留手动复制入口
      setTimeout(() => {
        if (backendOnline !== true) {
          startBtn.disabled = false;
          startBtn.textContent = "🚀 启动后端";
        }
      }, 3000);
    });
  }
  if (copyStartBtn) {
    copyStartBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(BACKEND_START_CMD);
        flash("已复制启动命令，去终端粘贴运行即可");
      } catch (_) {
        flash("复制失败，请手动复制上方命令", true);
      }
    });
  }
  // 停止后端：POST /api/stop，后端优雅退出（无需关终端/任务管理器）
  if (stopBtn) {
    stopBtn.addEventListener("click", async () => {
      try {
        await fetch(BACKEND + "/api/stop", { method: "POST" });
        flash("后端已停止");
      } catch (_) {
        // 后端可能已退出，忽略错误
        flash("后端已停止");
      }
      backendOnline = false;
      setOfflineUI(true);
    });
  }

  // ---------- 启动：恢复持久化状态 + 后端在线检测 ----------
  checkBackend();
  setInterval(() => {
    if (document.visibilityState !== "hidden") checkBackend();
  }, 12000);
  load("wx_contexts", (c) => {
    if (Array.isArray(c)) contexts = c;
    renderContexts();
  });
  load("wx_messages", (m) => {
    if (Array.isArray(m) && m.length) {
      messages = m;
      renderMessages();
    } else {
      addMessage(
        "assistant",
        "你好，我是小虾 🦐\n点开后在网页选中或复制文字，点「➕ 添加选中文本」就能带着上下文聊（会读取网页选区和系统剪切板，含输入法复制的内容）；发送问题时也会自动把内容收进上下文。标题栏可拖动浮层，双击复位。"
      );
    }
  });
})();
