// content.js —— 注入到任意网页（含 iframe，all_frames:true）
// 点工具栏图标 → 弹出对话浮层；浮层可拖动（按下标题栏发 DRAG_START，拖拽由本页全屏遮罩同步接管）
// 持久化：面板开关/位置/上下文/对话 存 chrome.storage，刷新/换页后自动重开面板
// 注意：选区读取已改由 background.js 通过 chrome.scripting.executeScript(allFrames) 完成，
//       不再走 postMessage 中继（微信读书等 iframe 阅读器下中继抓不到）
(function () {
  let panelIframe = null;
  let lastPos = null; // {left,top} 数值像素

  function setOpen(open) {
    try {
      chrome.storage.local.set({ wx_panelOpen: !!open });
    } catch (_) {}
  }
  function savePos(pos) {
    try {
      chrome.storage.local.set({ wx_panelPos: pos });
    } catch (_) {}
  }

  function closePanel() {
    if (panelIframe && panelIframe.parentNode) {
      panelIframe.parentNode.removeChild(panelIframe);
    }
    panelIframe = null;
    setOpen(false);
  }

  function openPanel() {
    const iframe = document.createElement("iframe");
    iframe.src = chrome.runtime.getURL("panel.html");
    iframe.id = "xiaoxia-panel";
    let css =
      "position:fixed;width:min(420px,92vw);height:66vh;border:0;" +
      "z-index:2147483647;box-shadow:0 8px 30px rgba(0,0,0,.3);border-radius:12px;background:#fff;";
    if (lastPos && typeof lastPos.left === "number") {
      css += "left:" + lastPos.left + "px;top:" + lastPos.top + "px;";
    } else {
      css += "top:20px;right:20px;";
    }
    iframe.style.cssText = css;
    document.body.appendChild(iframe);
    panelIframe = iframe;
    setOpen(true);
    iframe.addEventListener("load", function () {
      const rect = iframe.getBoundingClientRect();
      const info = {
        title: document.title,
        url: location.href,
        pos: { left: Math.round(rect.left), top: Math.round(rect.top) },
        viewport: { w: window.innerWidth, h: window.innerHeight },
      };
      iframe.contentWindow.postMessage({ type: "INIT_PAGE", info: info }, "*");
    });
  }

  function togglePanel() {
    if (panelIframe) closePanel();
    else openPanel();
  }

  // 与浮层（panel iframe）通信
  window.addEventListener("message", function (ev) {
    const d = ev.data;
    if (!d || !d.type) return;
    switch (d.type) {
      case "CLOSE_PANEL":
        closePanel();
        break;
      case "DRAG_START":
        // 面板只发一次起点偏移；后续拖拽由本页全屏遮罩同步接管（零往返延迟，不抖动）
        startDrag(d.offsetX || 0, d.offsetY || 0);
        break;
      case "RESET_PANEL_POS":
        resetPanelPos();
        break;
      case "LAUNCH_BACKEND":
        launchViaProtocol();
        break;
    }
  });

  // 在真实网页顶层文档注入隐藏 iframe 指向自定义协议，触发 webchat:// 处理程序。
  // 关键点：扩展 iframe 内用 window.open 自定义协议会被浏览器静默拦截；
  // 而 content.js 运行在真实网页上下文，注入 iframe 到顶层文档是浏览器认可的触发方式。
  function launchViaProtocol() {
    try {
      const f = document.createElement("iframe");
      f.style.cssText =
        "display:none;width:0;height:0;border:0;position:absolute;left:-9999px;top:-9999px;";
      f.src = "webchat://start";
      document.documentElement.appendChild(f);
      // 加载/协议调起后移除iframe（协议跳转不会真的加载资源，1.5s 兜底清理）
      setTimeout(function () {
        if (f.parentNode) f.parentNode.removeChild(f);
      }, 1500);
    } catch (_) {}
  }

  // 用全屏透明遮罩接管拖拽：pointermove 直接在本页监听、同步改样式，
  // 没有 postMessage 往返、也没有每次 getBoundingClientRect 重排 → 丝滑跟手
  let drag = null; // { grabX, grabY, overlay }
  function startDrag(offsetX, offsetY) {
    if (!panelIframe || drag) return;
    const rect = panelIframe.getBoundingClientRect();
    const grabX = rect.left + offsetX; // 指针在页面坐标系中的抓取点
    const grabY = rect.top + offsetY;
    const overlay = document.createElement("div");
    overlay.style.cssText =
      "position:fixed;inset:0;z-index:2147483647;background:transparent;cursor:grabbing;touch-action:none;";
    document.documentElement.appendChild(overlay);
    // 拖拽期间让 iframe 不拦截指针，确保遮罩收到所有 move 事件
    panelIframe.style.pointerEvents = "none";
    drag = { grabX: grabX, grabY: grabY, overlay: overlay };

    const onMove = function (e) {
      if (!drag || !panelIframe) return;
      const w = panelIframe.offsetWidth;
      const h = panelIframe.offsetHeight;
      // 关键修正：新位置 = 起始位置 + (当前指针 - 抓取点)
      // 之前少加了起始位置 rect.left/top，导致一拖就退回左上角(0,0)，
      // 连点击时的微小位移也会瞬移到左上角
      let nl = rect.left + (e.clientX - drag.grabX);
      let nt = rect.top + (e.clientY - drag.grabY);
      nl = Math.max(0, Math.min(nl, window.innerWidth - w));
      nt = Math.max(0, Math.min(nt, window.innerHeight - h));
      panelIframe.style.left = nl + "px";
      panelIframe.style.top = nt + "px";
      panelIframe.style.right = "auto";
      panelIframe.style.bottom = "auto";
      lastPos = { left: nl, top: nt };
    };
    const onUp = function () {
      if (drag) {
        drag.overlay.removeEventListener("pointermove", onMove);
        drag.overlay.removeEventListener("pointerup", onUp);
        drag.overlay.removeEventListener("pointercancel", onUp);
        if (drag.overlay.parentNode)
          drag.overlay.parentNode.removeChild(drag.overlay);
      }
      if (panelIframe) panelIframe.style.pointerEvents = "";
      savePos(lastPos);
      drag = null;
    };
    overlay.addEventListener("pointermove", onMove);
    overlay.addEventListener("pointerup", onUp);
    overlay.addEventListener("pointercancel", onUp);
  }

  function resetPanelPos() {
    if (panelIframe) {
      panelIframe.style.cssText =
        "position:fixed;top:20px;right:20px;width:min(420px,92vw);height:66vh;border:0;" +
        "z-index:2147483647;box-shadow:0 8px 30px rgba(0,0,0,.3);border-radius:12px;background:#fff;";
      lastPos = null;
      savePos(null);
    }
  }

  // 接收工具栏图标点击（来自 background service worker）
  chrome.runtime.onMessage.addListener(function (msg) {
    if (!msg || msg.type !== "TOGGLE_PANEL") return;
    // 只在顶层窗口响应，避免每个 iframe 都开一个面板
    if (window.top !== window) return;
    togglePanel();
  });

  // 页面加载时：恢复上次位置；若上次是打开状态，自动重开面板（刷新/换页不再丢）
  // 仅顶层窗口处理：all_frames 已关闭，但此处仍守卫，避免任何情况下多实例面板
  try {
    chrome.storage.local.get(["wx_panelPos", "wx_panelOpen"], function (r) {
      if (window.top !== window) return; // 只让顶层窗口创建/恢复面板
      if (r && r.wx_panelPos && typeof r.wx_panelPos.left === "number") {
        lastPos = r.wx_panelPos;
      }
      if (r && r.wx_panelOpen) openPanel();
    });
  } catch (_) {}
})();
