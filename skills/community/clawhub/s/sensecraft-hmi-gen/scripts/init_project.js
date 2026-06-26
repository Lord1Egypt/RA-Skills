#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const crypto = require('crypto');

const SCRIPT_DIR = __dirname;
const SKILL_DIR = path.dirname(SCRIPT_DIR);
const PROJECT_DIR = path.join(SKILL_DIR, 'data');

console.log('🎨 Initializing SenseCraft HMI project...');

// Create project directory
if (!fs.existsSync(PROJECT_DIR)) {
    fs.mkdirSync(PROJECT_DIR, { recursive: true });
}

// Initialize npm if needed
const packageJsonPath = path.join(PROJECT_DIR, 'package.json');
if (!fs.existsSync(packageJsonPath)) {
    const originalDir = process.cwd();
    process.chdir(PROJECT_DIR);
    try {
        execSync('npm init -y', { stdio: 'inherit' });
        execSync('npm install express', { stdio: 'inherit' });
    } catch (error) {
        console.error('Failed to initialize npm or install dependencies:', error);
    }
    process.chdir(originalDir);
}

// Copy server.js if not exists
const serverJsPath = path.join(PROJECT_DIR, 'server.js');
if (!fs.existsSync(serverJsPath)) {
    const serverJsContent = `#!/usr/bin/env node
const express = require('express');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 19527;
const CONTENT_DIR = __dirname;
const TOKEN_FILE = path.join(CONTENT_DIR, '.token');
const HTML_FILE = path.join(CONTENT_DIR, 'index.html');

let ACCESS_TOKEN;
if (fs.existsSync(TOKEN_FILE)) {
  ACCESS_TOKEN = fs.readFileSync(TOKEN_FILE, 'utf8').trim();
} else {
  ACCESS_TOKEN = crypto.randomBytes(32).toString('hex');
  fs.writeFileSync(TOKEN_FILE, ACCESS_TOKEN);
  console.log('Generated new access token:', ACCESS_TOKEN);
}

function requireToken(req, res, next) {
  const token = req.query.token;
  if (token === ACCESS_TOKEN) {
    next();
  } else {
    res.status(403).send('Forbidden: Invalid or missing token');
  }
}

app.use('/static', requireToken, express.static(path.join(CONTENT_DIR, 'public')));

app.get('/', requireToken, (req, res) => {
  if (fs.existsSync(HTML_FILE)) {
    res.sendFile(HTML_FILE);
  } else {
    res.send('<html><body><h1>No content yet</h1><p>Run wizard to create your first page.</p></body></html>');
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.use((req, res) => {
  res.status(404).send('Not Found');
});

app.listen(PORT, () => {
  console.log(\`SenseCraft HMI server running on http://localhost:\${PORT}\`);
  console.log(\`Access token: \${ACCESS_TOKEN}\`);
  console.log(\`URL with token: http://localhost:\${PORT}/?token=\${ACCESS_TOKEN}\`);
});
`;
    fs.writeFileSync(serverJsPath, serverJsContent);
    if (process.platform !== 'win32') {
        fs.chmodSync(serverJsPath, '755');
    }
}

// Create directories
const publicImagesPath = path.join(PROJECT_DIR, 'public', 'images');
const publicCssPath = path.join(PROJECT_DIR, 'public', 'css');

if (!fs.existsSync(publicImagesPath)) {
    fs.mkdirSync(publicImagesPath, { recursive: true });
}
if (!fs.existsSync(publicCssPath)) {
    fs.mkdirSync(publicCssPath, { recursive: true });
}

// Make scripts executable if not on Windows
if (process.platform !== 'win32') {
    const files = fs.readdirSync(SCRIPT_DIR);
    for (const file of files) {
        if (file.endsWith('.js') || file.endsWith('.sh')) {
            const filePath = path.join(SCRIPT_DIR, file);
            try {
                fs.chmodSync(filePath, '755');
            } catch (err) {
                console.warn(`Could not make ${file} executable.`, err.message);
            }
        }
    }
}

console.log(`\n✓ Project initialized at ${PROJECT_DIR}`);
