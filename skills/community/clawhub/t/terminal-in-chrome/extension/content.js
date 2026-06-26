let terminalVisible = false;
let terminalContainer = null;
let terminal = null;
let fitAddon = null;
let ws = null;
let wsUrl = 'ws://localhost:8989/terminal';
let isResizing = false;
let startY;
let startHeight;

let isFullscreen = false;
let previousHeight = 0;

let currentTheme = 'dark';
const terminalThemes = {
  dark: { 
    background: '#000000', 
    foreground: '#e6edf3', 
    cursor: '#ffffff' 
  },
  light: { 
    background: '#ffffff', 
    foreground: '#333333', 
    cursor: '#000000', 
    selectionBackground: 'rgba(0, 0, 0, 0.3)',
    // Map ANSI colors to be darker/more readable on white background
    black: '#000000',
    red: '#cd3131',
    green: '#008000',
    yellow: '#949800',
    blue: '#0451a5',
    magenta: '#bc05bc',
    cyan: '#0598bc',
    white: '#555555',
    brightBlack: '#666666',
    brightRed: '#cd3131',
    brightGreen: '#14ce14',
    brightYellow: '#b5ba00',
    brightBlue: '#0451a5',
    brightMagenta: '#bc05bc',
    brightCyan: '#0598bc',
    brightWhite: '#a5a5a5'
  }
};

function applyTheme(themeName) {
  currentTheme = themeName;
  const isLight = themeName === 'light';
  
  if (terminalContainer) {
    if (isLight) terminalContainer.classList.add('theme-light');
    else terminalContainer.classList.remove('theme-light');
  }
  
  if (bubbleContainer) {
    if (isLight) bubbleContainer.classList.add('theme-light');
    else bubbleContainer.classList.remove('theme-light');
  }
  
  if (terminal) {
    terminal.options.theme = terminalThemes[themeName] || terminalThemes.dark;
  }
}

let hasUnreadOutput = false;
let isProcessing = false;
let bubbleContainer = null;
let isFirstMessage = true;
let outputTimeout = null;


function injectBubbleHTML() {
  if (document.getElementById('web-terminal-ext-bubble')) return;
  
  bubbleContainer = document.createElement('div');
  bubbleContainer.id = 'web-terminal-ext-bubble';
  bubbleContainer.innerHTML = '>_';
  bubbleContainer.title = 'Terminal has new activity';
  
  bubbleContainer.addEventListener('click', () => {
    toggleTerminal(true);
  });
  
  document.body.appendChild(bubbleContainer);
  applyTheme(currentTheme);
}

function updateBubble() {
  if (!bubbleContainer) injectBubbleHTML();
  
  if (hasUnreadOutput && (!terminalVisible || document.hidden)) {
    bubbleContainer.classList.add('show');
    bubbleContainer.classList.add('active');
  } else {
    bubbleContainer.classList.remove('show');
    bubbleContainer.classList.remove('active');
  }
}

let originalFavicons = null;
let faviconInterval = null;
let faviconFrame = 0;

function saveFavicons() {
  if (originalFavicons !== null) return;
  originalFavicons = [];
  const links = document.querySelectorAll('link[rel~="icon"]');
  links.forEach(link => {
    originalFavicons.push({
      rel: link.rel,
      href: link.href,
      sizes: link.sizes ? link.sizes.value : '',
      type: link.type
    });
  });
  if (originalFavicons.length === 0) {
    originalFavicons.push({ rel: 'icon', href: '/favicon.ico' });
  }
}

function restoreFavicons() {
  if (originalFavicons === null) return;
  const current = document.querySelectorAll('link[rel~="icon"]');
  current.forEach(link => link.parentNode.removeChild(link));
  
  originalFavicons.forEach(icon => {
    const link = document.createElement('link');
    link.rel = icon.rel;
    link.href = icon.href;
    if (icon.sizes) link.sizes = icon.sizes;
    if (icon.type) link.type = icon.type;
    document.head.appendChild(link);
  });
  originalFavicons = null;
}

function drawFavicon(status) {
  const canvas = document.createElement('canvas');
  canvas.width = 32;
  canvas.height = 32;
  const ctx = canvas.getContext('2d');
  
  let isVisible = true;
  
  if (status === 'processing') {
    isVisible = (faviconFrame % 2) === 0;
    if (isVisible) {
      ctx.fillStyle = '#F44336'; // Red dot for recording
      ctx.beginPath();
      ctx.arc(16, 16, 12, 0, Math.PI * 2);
      ctx.fill();
    }
  } else if (status === 'done') {
    ctx.fillStyle = '#4CAF50'; // Green for done
    ctx.beginPath();
    ctx.arc(16, 16, 14, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(10, 16);
    ctx.lineTo(14, 20);
    ctx.lineTo(22, 11);
    ctx.stroke();
  }
  
  const link = document.createElement('link');
  link.rel = 'icon';
  link.href = canvas.toDataURL('image/png');
  
  const current = document.querySelectorAll('link[rel~="icon"]');
  current.forEach(l => l.parentNode.removeChild(l));
  document.head.appendChild(link);
  
  return isVisible;
}

function setFavicon(status) {
  if (status === 'clear') {
    if (faviconInterval) { clearInterval(faviconInterval); faviconInterval = null; }
    restoreFavicons();
    chrome.runtime.sendMessage({ type: 'TERMINAL_ACTIVITY', status: 'clear' }).catch(() => {});
    return;
  }
  
  saveFavicons();
  
  if (status === 'processing') {
    if (!faviconInterval) {
      const blink = drawFavicon('processing');
      chrome.runtime.sendMessage({ type: 'TERMINAL_ACTIVITY', status: 'processing', blink }).catch(() => {});
      
      faviconInterval = setInterval(() => {
        faviconFrame++;
        const blink = drawFavicon('processing');
        chrome.runtime.sendMessage({ type: 'TERMINAL_ACTIVITY', status: 'processing', blink }).catch(() => {});
      }, 500);
    }
  } else {
    if (faviconInterval) { clearInterval(faviconInterval); faviconInterval = null; }
    drawFavicon(status);
    chrome.runtime.sendMessage({ type: 'TERMINAL_ACTIVITY', status: 'done' }).catch(() => {});
  }
}

function injectTerminalHTML() {
  if (document.getElementById('web-terminal-ext-container')) return;

  const container = document.createElement('div');
  container.id = 'web-terminal-ext-container';
  
  const resizer = document.createElement('div');
  resizer.id = 'web-terminal-ext-resizer';
  
  const header = document.createElement('div');
  header.id = 'web-terminal-ext-header';
  
  const title = document.createElement('span');
  title.id = 'web-terminal-ext-title';
  title.innerText = 'Local Terminal';
  
  const closeBtn = document.createElement('button');
  closeBtn.id = 'web-terminal-ext-close';
  closeBtn.innerText = '×';
  closeBtn.addEventListener('click', () => toggleTerminal(false));
  
  header.appendChild(title);
  header.appendChild(closeBtn);
  
  const host = document.createElement('div');
  host.id = 'web-terminal-ext-host';
  
  container.appendChild(resizer);
  container.appendChild(header);
  container.appendChild(host);
  
  document.body.appendChild(container);
  terminalContainer = container;
  applyTheme(currentTheme);

  // Setup Resizer
  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    startY = e.clientY;
    startHeight = container.getBoundingClientRect().height;
    resizer.classList.add('active');
    document.body.style.cursor = 'ns-resize';
  });

  // Double click header to toggle full height
  header.addEventListener('dblclick', () => {
    if (isFullscreen) {
      // Restore previous height
      container.style.height = `${previousHeight}px`;
      isFullscreen = false;
    } else {
      // Save current height and make full screen
      previousHeight = container.getBoundingClientRect().height;
      container.style.height = '100vh';
      isFullscreen = true;
    }
    
    // Save state
    chrome.storage.local.set({ 
      terminalHeight: container.getBoundingClientRect().height,
      terminalIsFullscreen: isFullscreen,
      terminalPreviousHeight: previousHeight
    });

    if (fitAddon && ws && ws.readyState === WebSocket.OPEN) {
      setTimeout(() => {
        fitAddon.fit();
        ws.send(JSON.stringify({ type: 'resize', cols: terminal.cols, rows: terminal.rows }));
      }, 50); // Small delay to allow CSS transition if any
    }
  });

  window.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const dy = startY - e.clientY;
    container.style.height = `${startHeight + dy}px`;
    if (fitAddon) fitAddon.fit();
  });

  window.addEventListener('mouseup', () => {
    if (isResizing) {
      isResizing = false;
      resizer.classList.remove('active');
      document.body.style.cursor = '';
      
      // If manually resized, we are no longer in fullscreen mode
      isFullscreen = false;
      
      // Save height to local storage
      chrome.storage.local.set({ 
        terminalHeight: container.getBoundingClientRect().height,
        terminalIsFullscreen: false
      });

      if (fitAddon && ws && ws.readyState === WebSocket.OPEN) {
        fitAddon.fit();
        ws.send(JSON.stringify({ type: 'resize', cols: terminal.cols, rows: terminal.rows }));
      }
    }
  });

  // Restore height
  chrome.storage.local.get(['terminalHeight', 'terminalIsFullscreen', 'terminalPreviousHeight'], (result) => {
    if (result.terminalIsFullscreen !== undefined) {
      isFullscreen = result.terminalIsFullscreen;
    }
    if (result.terminalPreviousHeight) {
      previousHeight = result.terminalPreviousHeight;
    }
    if (result.terminalHeight) {
      container.style.height = `${result.terminalHeight}px`;
    }
  });
}

function initTerminal() {
  if (terminal) return;
  
  const host = document.getElementById('web-terminal-ext-host');
  
  terminal = new Terminal({
    cursorBlink: true,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
    fontSize: 14,
    theme: terminalThemes[currentTheme] || terminalThemes.dark
  });
  
  // Use the FitAddon constructor we exposed globally via the script injection
  fitAddon = new FitAddon.FitAddon();
  terminal.loadAddon(fitAddon);
  
  terminal.open(host);
  
  setTimeout(() => {
    fitAddon.fit();
    connectWebSocket();
  }, 10);
  
  window.addEventListener('resize', () => {
    if (terminalVisible && fitAddon) {
      fitAddon.fit();
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'resize', cols: terminal.cols, rows: terminal.rows }));
      }
    }
  });
}

function connectWebSocket() {
  // Use origin + pathname as the unique identifier for the terminal instance
  const pageUrl = encodeURIComponent(pageUrlKey);
  const connectUrl = `${wsUrl}?url=${pageUrl}&theme=${currentTheme}`;
  ws = new WebSocket(connectUrl);
  
  ws.onopen = () => {
    console.log('[WebTerminal] Connected to local server');
    isFirstMessage = true;
    ws.send(JSON.stringify({ type: 'resize', cols: terminal.cols, rows: terminal.rows }));
    
    terminal.onData(data => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });
  };
  
  ws.onmessage = (event) => {
    if (isFirstMessage) {
      isFirstMessage = false;
    } else if (!terminalVisible || document.hidden) {
      hasUnreadOutput = true;
      isProcessing = true;
      
      updateBubble();
      setFavicon('processing');
            
      
      if (bubbleContainer) {
        bubbleContainer.classList.add('processing');
        bubbleContainer.classList.remove('done');
      }
      
      clearTimeout(outputTimeout);
      outputTimeout = setTimeout(() => {
        isProcessing = false;
        if (bubbleContainer) {
          bubbleContainer.classList.remove('processing');
          bubbleContainer.classList.add('done');
        }
        setFavicon('done');
                
      }, 1000);
    }

    if (event.data instanceof Blob) {
      const reader = new FileReader();
      reader.onload = () => terminal.write(reader.result);
      reader.readAsText(event.data);
    } else {
      terminal.write(event.data);
    }
  };
  
  ws.onclose = () => {
    console.log('[WebTerminal] Disconnected');
    terminal.write(`\r\n\x1b[31m[Connection Closed] Make sure local server is running on ${wsUrl}\x1b[0m\r\n`);
    if (terminalVisible) {
      setTimeout(connectWebSocket, 3000);
    }
  };
}

let pageUrlKey = window.location.origin + window.location.pathname;

function toggleTerminal(show) {
  if (!terminalContainer) injectTerminalHTML();
  
  terminalVisible = show !== undefined ? show : !terminalVisible;
  
  // Save visibility state specifically for this URL
  chrome.storage.local.set({ [`terminalVisible_${pageUrlKey}`]: terminalVisible });
  
  if (terminalVisible) {
    if (!document.hidden) {
      hasUnreadOutput = false;
      isProcessing = false;
      clearTimeout(outputTimeout);
      
      if (bubbleContainer) {
        bubbleContainer.classList.remove('processing');
        bubbleContainer.classList.remove('done');
      }
      
      updateBubble();
      setFavicon('clear');
            
    }
    
    terminalContainer.classList.add('show');
    if (!terminal) {
      initTerminal();
    } else {
      setTimeout(() => {
        fitAddon.fit();
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'resize', cols: terminal.cols, rows: terminal.rows }));
        }
        terminal.focus();
      }, 50);
    }
  } else {
    terminalContainer.classList.remove('show');
  }
}

let isSiteBlocked = false;

// Check if current site is blocked
chrome.storage.local.get(null, (result) => {
  if (result.sharedPaths && Array.isArray(result.sharedPaths)) {
    const currentHref = window.location.href;
    const currentHostPath = window.location.host + window.location.pathname;
    let bestMatch = '';
    for (const p of result.sharedPaths) {
      if (currentHref.startsWith(p) || currentHostPath.startsWith(p)) {
        if (p.length > bestMatch.length) {
          bestMatch = p;
        }
      }
    }
    if (bestMatch) {
      pageUrlKey = 'shared_' + bestMatch;
    }
  }
  if (result.blockedSites && Array.isArray(result.blockedSites)) {
    const origin = window.location.origin;
    const hostname = window.location.hostname;
    
    isSiteBlocked = result.blockedSites.some(site => {
      // Check if site includes protocol/port (e.g. http://localhost:18080)
      if (site.startsWith('http://') || site.startsWith('https://')) {
        // Match exact origin, or origin + trailing slash, or origin + path prefix
        return origin === site || origin + '/' === site || window.location.href.startsWith(site);
      }
      
      // If no protocol/port, fallback to hostname matching (e.g. google.com)
      return hostname === site || hostname.endsWith(`.${site}`);
    });
  }
  
  if (isSiteBlocked) return;
  
  if (result.terminalTheme) {
    applyTheme(result.terminalTheme);
  }
  if (result.terminalPort) {
    wsUrl = `ws://localhost:${result.terminalPort}/terminal`;
  }
  if (result[`terminalVisible_${pageUrlKey}`]) {
    toggleTerminal(true);
  }
});

// Listen for keyboard shortcuts (Ctrl+` or Cmd+j)
document.addEventListener('keydown', (e) => {
  if (isSiteBlocked) return;
  
  if ((e.ctrlKey && e.key === '`') || (e.metaKey && e.key === 'j')) {
    e.preventDefault();
    toggleTerminal();
  }
});

// Listen for messages from background script or popup to update port
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if ((message.type === 'UPDATE_PORT' || message.type === 'UPDATE_SETTINGS') && message.port) {
    if (message.theme) {
      applyTheme(message.theme);
    }
    const newWsUrl = `ws://localhost:${message.port}/terminal`;
    if (wsUrl !== newWsUrl) {
      wsUrl = newWsUrl;
      if (ws) {
        ws.close(); // Will auto-reconnect via onclose handler
      }
    }
  }
});


document.addEventListener('visibilitychange', () => {
  if (!document.hidden && terminalVisible) {
    hasUnreadOutput = false;
    isProcessing = false;
    clearTimeout(outputTimeout);
    
    if (bubbleContainer) {
      bubbleContainer.classList.remove('processing');
      bubbleContainer.classList.remove('done');
    }
    
    updateBubble();
    setFavicon('clear');
        
  }
});
