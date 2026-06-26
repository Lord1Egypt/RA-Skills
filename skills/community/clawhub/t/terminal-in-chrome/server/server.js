const express = require('express');
const expressWs = require('express-ws');
const os = require('os');
const pty = require('node-pty');
const cors = require('cors');
const url = require('url');

const app = express();
expressWs(app);
app.use(cors()); // Allow connections from any website

let defaultShell = '/bin/bash';
if (os.platform() === 'win32') {
  defaultShell = 'powershell.exe';
} else {
  try {
    defaultShell = os.userInfo().shell || '/bin/bash';
  } catch (e) {
    defaultShell = '/bin/bash';
  }
}
const shell = process.env.SHELL || defaultShell;

// Store terminal instances by URL
// { url: { ptyProcess, history, clients: Set<ws> } }
const terminalInstances = new Map();

app.ws('/terminal', (ws, req) => {
  const query = url.parse(req.url, true).query;
  const pageUrl = query.url || 'default';
  const theme = query.theme || 'dark';
  
  console.log(`[WebSocket] Terminal client connected for URL: ${pageUrl}`);
  
  let instance = terminalInstances.get(pageUrl);
  
  if (!instance) {
    // Create new terminal instance for this URL
    const ptyProcess = pty.spawn(shell, [], {
      name: 'xterm-color',
      cols: 80,
      rows: 24,
      cwd: process.env.HOME,
      env: { ...process.env, COLORFGBG: theme === 'light' ? '15;0' : 'default' }
    });

    instance = {
      ptyProcess,
      history: '',
      clients: new Set()
    };
    
    terminalInstances.set(pageUrl, instance);

    ptyProcess.onData((data) => {
      instance.history += data;
      // Keep history from getting too large
      if (instance.history.length > 100000) {
        instance.history = instance.history.slice(instance.history.length - 100000);
      }
      
      // Broadcast to all clients on this URL
      instance.clients.forEach(clientWs => {
        if (clientWs.readyState === 1) {
          clientWs.send(data);
        }
      });
    });
  }

  // Add this client to the instance
  instance.clients.add(ws);

  // Send history to new client
  const cleanHistory = instance.history
    .replace(/\x1b\]1[01];\?(?:\x07|\x1b\\)/g, '')
    .replace(/\x1b\[[>?]*[0-9]*c/g, '')
    .replace(/\x1b\[6n/g, '');
    
  ws.send(cleanHistory);

  ws.on('message', (msg) => {
    try {
      // JSON.parse successfully parses numbers (like "1"), so we must check if it's an object
      const data = JSON.parse(msg);
      if (data && typeof data === 'object' && data.type === 'resize') {
        instance.ptyProcess.resize(data.cols, data.rows);
        return;
      }
    } catch (e) {
      // Ignore parse errors (regular terminal input)
    }
    // If we didn't return, it's terminal input
    instance.ptyProcess.write(msg);
  });

  ws.on('close', () => {
    console.log(`[WebSocket] Terminal client disconnected from URL: ${pageUrl}`);
    instance.clients.delete(ws);
    
    // We no longer kill the process here.
    // The terminal will persist even if all clients disconnect.
    // It will only be cleared when the server is restarted.
  });
});

const PORT = process.env.PORT || process.env.WEB_TERMINAL_PORT || 8989;
app.listen(PORT, () => {
  console.log(`Server listening on ws://localhost:${PORT}/terminal`);
});
