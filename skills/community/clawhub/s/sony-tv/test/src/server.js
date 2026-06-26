const express = require('express');
const os = require('os');
const path = require('path');
const SonyTVClient = require('./SonyTVClient');

const app = express();
const PORT = process.env.PORT || 3000;

// TV configuration
const TV_HOST = process.env.TV_HOST || '192.168.50.120';
const TV_PSK = process.env.TV_PSK || '19890801';

const tvClient = new SonyTVClient(TV_HOST, TV_PSK);

app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// --- IRCC Command endpoints ---
const irccRoutes = [
  'powerOn', 'powerOff', 'togglePower',
  'up', 'down', 'left', 'right', 'confirm',
  'home', 'exit', 'options', 'back',
  'volumeUp', 'volumeDown', 'mute',
  'channelUp', 'channelDown',
  'play', 'pause', 'stop', 'rewind', 'forward',
  'hdmi1', 'hdmi2', 'hdmi3', 'hdmi4',
];

for (const route of irccRoutes) {
  app.post(`/api/${route}`, async (_req, res) => {
    try {
      const result = await tvClient[route]();
      res.json({ success: true, result });
    } catch (err) {
      res.status(500).json({ success: false, error: err.message });
    }
  });
}

// --- Generic IRCC send ---
app.post('/api/sendIRCC', (req, res) => {
  const { code } = req.body;
  if (!code) {
    return res.status(400).json({ success: false, error: 'Missing IRCC code' });
  }
  tvClient.sendIRCC(code)
    .then((result) => res.json({ success: true, result }))
    .catch((err) => res.status(500).json({ success: false, error: err.message }));
});

// --- Status endpoints ---
app.get('/api/volume', async (_req, res) => {
  try {
    const result = await tvClient.getVolume();
    res.json({ success: true, result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

app.get('/api/power', async (_req, res) => {
  try {
    const result = await tvClient.getPowerStatus();
    res.json({ success: true, result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// --- Open URL on TV ---
app.post('/api/openURL', async (req, res) => {
  const { url } = req.body;
  if (!url) {
    return res.status(400).json({ success: false, error: 'Missing URL' });
  }
  try {
    const result = await tvClient.openURL(url);
    res.json({ success: true, result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// --- Get local IP ---
app.get('/api/localIP', (_req, res) => {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal && iface.address.startsWith('192.168.')) {
        return res.json({ ip: iface.address });
      }
    }
  }
  // Fallback: return any non-internal IPv4
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return res.json({ ip: iface.address });
      }
    }
  }
  res.json({ ip: '127.0.0.1' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Sony TV Remote running on http://0.0.0.0:${PORT}`);
  console.log(`TV: ${TV_HOST}`);
});

// --- Kill/Terminate all apps on TV ---
app.post('/api/kill', async (_req, res) => {
  try {
    const result = await tvClient.terminateApps();
    res.json({ success: true, result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// --- Receive diagnostic results from TV ---
let lastDiagResults = null;

app.post('/api/diag-results', (req, res) => {
  lastDiagResults = req.body;
  res.json({ received: true });

  // Log to console
  const body = req.body;
  if (body.error) {
    console.log('\n[DIAG ERROR]', body.error);
    console.log('  UA:', body.ua);
    console.log('  Time:', body.time);
    return;
  }

  if (body.results) {
    let pass = 0, fail = 0, warn = 0;
    body.results.forEach((r) => {
      if (r.status === 'pass') pass++;
      else if (r.status === 'fail') fail++;
      else warn++;
    });
    console.log('\n[TV DIAG]', body.results.length, 'tests |', pass, 'pass,', fail, 'fail,', warn, 'warn');
    console.log('  UA:', body.ua);
    console.log('  URL:', body.url);
    console.log('  Time:', body.time);
  }
});

app.get('/api/diag-results', (_req, res) => {
  res.json(lastDiagResults || { error: 'No results yet' });
});
