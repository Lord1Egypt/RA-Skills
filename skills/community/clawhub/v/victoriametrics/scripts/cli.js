#!/usr/bin/env node

/**
 * VictoriaMetrics CLI - Query and manage VictoriaMetrics instances
 * Supports both single-node and cluster deployments
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Config file locations (priority order)
const CONFIG_PATHS = [
  process.env.VICTORIAMETRICS_CONFIG,
  path.join(process.env.HOME || '/root', '.openclaw/workspace/victoriametrics.json'),
  path.join(process.env.HOME || '/root', '.openclaw/workspace/config/victoriametrics.json'),
  './victoriametrics.json',
  path.join(process.env.HOME || '/root', '.config/victoriametrics/config.json')
].filter(Boolean);

// Parse command line args
function parseArgs(args) {
  const result = {
    command: args[0],
    query: args[1],
    flags: {},
    positional: []
  };

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      if (value !== undefined) {
        result.flags[key] = value;
      } else {
        // Check if next arg is a value (not starting with -)
        const nextArg = args[i + 1];
        if (nextArg && !nextArg.startsWith('-')) {
          result.flags[key] = nextArg;
          i++; // Skip next arg
        } else {
          result.flags[key] = true;
        }
      }
    } else if (arg.startsWith('-') && !arg.startsWith('--')) {
      const key = arg.slice(1);
      // Check if next arg is a value (not starting with -)
      const nextArg = args[i + 1];
      if (nextArg && !nextArg.startsWith('-')) {
        result.flags[key] = nextArg;
        i++; // Skip next arg
      } else {
        result.flags[key] = true;
      }
    } else if (i > 1 || result.command !== 'query') {
      result.positional.push(arg);
    }
  }

  return result;
}

// Load config
function loadConfig(configPath = null) {
  const paths = configPath ? [configPath, ...CONFIG_PATHS] : CONFIG_PATHS;
  
  for (const p of paths) {
    if (p && fs.existsSync(p)) {
      try {
        const content = fs.readFileSync(p, 'utf8');
        return { ...JSON.parse(content), _configPath: p };
      } catch (err) {
        console.error(`Warning: Failed to load config from ${p}: ${err.message}`);
      }
    }
  }
  
  return { instances: [], _configPath: null };
}

// Build URL based on deployment type
function buildUrl(instance, endpoint, params = {}) {
  const url = new URL(instance.url);
  const isCluster = instance.type === 'cluster';
  
  // Cluster deployment URL format
  if (isCluster) {
    // http://<vmselect>:8481/select/<accountID>/prometheus/api/v1/query
    const accountID = instance.accountID || instance.accountId || 0;
    const projectID = instance.projectID || instance.projectId;
    
    let tenantPath = projectID !== undefined ? `${accountID}:${projectID}` : `${accountID}`;
    
    // Insert tenant path before /prometheus
    if (!url.pathname.includes('/select/')) {
      url.pathname = `/select/${tenantPath}/prometheus${endpoint}`;
    } else {
      url.pathname = url.pathname.replace(/\/$/, '') + endpoint;
    }
  } else {
    // Single-node deployment URL format
    // http://<victoriametrics>:8428/api/v1/query
    url.pathname = endpoint;
  }
  
  // Add query parameters
  Object.keys(params).forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      url.searchParams.append(key, params[key]);
    }
  });
  
  return url.toString();
}

// Make HTTP request
function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const isHttps = parsedUrl.protocol === 'https:';
    const client = isHttps ? https : http;
    
    const requestOptions = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (isHttps ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: options.method || 'GET',
      headers: {
        'Accept': 'application/json',
        ...options.headers
      }
    };
    
    // Add basic auth if configured
    if (options.user && options.password) {
      const auth = Buffer.from(`${options.user}:${options.password}`).toString('base64');
      requestOptions.headers['Authorization'] = `Basic ${auth}`;
    }
    
    const req = client.request(requestOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch (err) {
            resolve(data);
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    req.end();
  });
}

// Query a single instance
async function queryInstance(instance, query, params = {}) {
  const url = buildUrl(instance, '/api/v1/query', { query, ...params });
  const result = await makeRequest(url, {
    user: instance.user,
    password: instance.password
  });
  
  return result;
}

// Query all instances
async function queryAllInstances(config, query, params = {}) {
  const results = await Promise.all(
    config.instances.map(async (instance) => {
      try {
        const result = await queryInstance(instance, query, params);
        return {
          instance: instance.name,
          status: 'success',
          ...result
        };
      } catch (err) {
        return {
          instance: instance.name,
          status: 'error',
          error: err.message
        };
      }
    })
  );
  
  return {
    resultType: 'vector',
    results
  };
}

// Interactive config initialization
async function initConfig() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const question = (prompt) => new Promise((resolve) => {
    rl.question(prompt, resolve);
  });
  
  console.log('\n🚀 VictoriaMetrics Configuration Wizard\n');
  
  const instances = [];
  let addMore = true;
  
  while (addMore) {
    console.log(`\n--- Instance ${instances.length + 1} ---`);
    
    const name = await question('Instance name (e.g., production, staging): ');
    const type = await question('Deployment type (single/cluster) [single]: ') || 'single';
    const url = await question('VictoriaMetrics URL (e.g., http://localhost:8428): ');
    
    const instance = { name, type, url };
    
    if (type === 'cluster') {
      const accountID = await question('Account ID (default: 0): ') || '0';
      instance.accountID = parseInt(accountID);
      
      const projectID = await question('Project ID (optional, press Enter to skip): ');
      if (projectID) instance.projectID = parseInt(projectID);
    }
    
    const hasAuth = await question('Use HTTP Basic Auth? (y/N): ');
    if (hasAuth.toLowerCase() === 'y') {
      instance.user = await question('Username: ');
      instance.password = await question('Password: ');
    }
    
    instances.push(instance);
    
    const more = await question('\nAdd another instance? (y/N): ');
    addMore = more.toLowerCase() === 'y';
  }
  
  const defaultInstance = instances.length === 1 
    ? instances[0].name 
    : await question(`\nDefault instance [${instances[0].name}]: `) || instances[0].name;
  
  rl.close();
  
  const config = {
    instances,
    default: defaultInstance
  };
  
  // Save to workspace
  const configPath = path.join(process.env.HOME || '/root', '.openclaw/workspace/victoriametrics.json');
  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  console.log(`\n✅ Configuration saved to: ${configPath}`);
  console.log('\nConfiguration:');
  console.log(JSON.stringify(config, null, 2));
}

// Commands
const commands = {
  async init() {
    await initConfig();
  },
  
  async query(parsed, config) {
    const { query, flags } = parsed;
    
    if (!query) {
      console.error('Error: Query is required');
      console.error('Usage: node cli.js query "up" [--all] [-i instance]');
      process.exit(1);
    }
    
    let result;
    
    if (flags.all) {
      result = await queryAllInstances(config, query);
    } else {
      const instanceName = flags.i || flags.instance || config.default;
      const instance = config.instances.find(i => i.name === instanceName);
      
      if (!instance) {
        console.error(`Error: Instance "${instanceName}" not found`);
        process.exit(1);
      }
      
      result = await queryInstance(instance, query);
    }
    
    console.log(JSON.stringify(result, null, 2));
  },
  
  async instances(parsed, config) {
    const result = {
      default: config.default,
      instances: config.instances.map(i => ({
        name: i.name,
        type: i.type,
        url: i.url,
        accountID: i.accountID,
        hasAuth: !!(i.user && i.password)
      }))
    };
    
    console.log(JSON.stringify(result, null, 2));
  },
  
  async metrics(parsed, config) {
    const { flags } = parsed;
    const pattern = parsed.positional[0] || '';
    
    const instanceName = flags.i || flags.instance || config.default;
    const instance = config.instances.find(i => i.name === instanceName);
    
    if (!instance) {
      console.error(`Error: Instance "${instanceName}" not found`);
      process.exit(1);
    }
    
    const url = buildUrl(instance, '/api/v1/label/__name__/values');
    const result = await makeRequest(url, {
      user: instance.user,
      password: instance.password
    });
    
    // Filter by pattern
    const metrics = result.data || [];
    const filtered = pattern 
      ? metrics.filter(m => m.includes(pattern))
      : metrics;
    
    console.log(JSON.stringify({ count: filtered.length, metrics: filtered }, null, 2));
  },
  
  async labels(parsed, config) {
    const { flags } = parsed;
    
    const instanceName = flags.i || flags.instance || config.default;
    const instance = config.instances.find(i => i.name === instanceName);
    
    if (!instance) {
      console.error(`Error: Instance "${instanceName}" not found`);
      process.exit(1);
    }
    
    const url = buildUrl(instance, '/api/v1/labels');
    const result = await makeRequest(url, {
      user: instance.user,
      password: instance.password
    });
    
    console.log(JSON.stringify(result, null, 2));
  },
  
  async 'label-values'(parsed, config) {
    const { flags } = parsed;
    const label = parsed.positional[0];
    
    if (!label) {
      console.error('Error: Label name is required');
      console.error('Usage: node cli.js label-values <label> [--all] [-i instance]');
      process.exit(1);
    }
    
    const instanceName = flags.i || flags.instance || config.default;
    const instance = config.instances.find(i => i.name === instanceName);
    
    if (!instance) {
      console.error(`Error: Instance "${instanceName}" not found`);
      process.exit(1);
    }
    
    const url = buildUrl(instance, `/api/v1/label/${label}/values`);
    const result = await makeRequest(url, {
      user: instance.user,
      password: instance.password
    });
    
    console.log(JSON.stringify(result, null, 2));
  },
  
  async series(parsed, config) {
    const { flags } = parsed;
    const match = parsed.positional[0];
    
    if (!match) {
      console.error('Error: Match selector is required');
      console.error('Usage: node cli.js series \'{__name__=~"node_.*"}\' [--all] [-i instance]');
      process.exit(1);
    }
    
    const instanceName = flags.i || flags.instance || config.default;
    const instance = config.instances.find(i => i.name === instanceName);
    
    if (!instance) {
      console.error(`Error: Instance "${instanceName}" not found`);
      process.exit(1);
    }
    
    const url = buildUrl(instance, '/api/v1/series', { 'match[]': match });
    const result = await makeRequest(url, {
      user: instance.user,
      password: instance.password
    });
    
    console.log(JSON.stringify(result, null, 2));
  },
  
  async alerts(parsed, config) {
    const { flags } = parsed;
    
    const instanceName = flags.i || flags.instance || config.default;
    const instance = config.instances.find(i => i.name === instanceName);
    
    if (!instance) {
      console.error(`Error: Instance "${instanceName}" not found`);
      process.exit(1);
    }
    
    const url = buildUrl(instance, '/api/v1/alerts');
    const result = await makeRequest(url, {
      user: instance.user,
      password: instance.password
    });
    
    console.log(JSON.stringify(result, null, 2));
  },
  
  async health(parsed, config) {
    const { flags } = parsed;
    
    const instanceName = flags.i || flags.instance || config.default;
    const instance = config.instances.find(i => i.name === instanceName);
    
    if (!instance) {
      console.error(`Error: Instance "${instanceName}" not found`);
      process.exit(1);
    }
    
    try {
      // Try health endpoint (different path for single vs cluster)
      let healthUrl;
      if (instance.type === 'cluster') {
        // Cluster mode: health is at /select/0/health or just /health
        healthUrl = instance.url.replace(/\/$/, '') + '/health';
      } else {
        healthUrl = buildUrl(instance, '/health');
      }
      
      await makeRequest(healthUrl, {
        user: instance.user,
        password: instance.password
      });
      
      console.log(JSON.stringify({
        instance: instance.name,
        status: 'healthy'
      }, null, 2));
    } catch (err) {
      console.log(JSON.stringify({
        instance: instance.name,
        status: 'unhealthy',
        error: err.message
      }, null, 2));
    }
  }
};

// Main
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
VictoriaMetrics CLI

Commands:
  init                           Interactive configuration wizard
  query <promql> [--all]         Query metrics (use --all for all instances)
  instances                      List configured instances
  metrics [pattern]              List metric names (optionally filter by pattern)
  labels                         List label names
  label-values <label>           List values for a label
  series <selector>              Find time series matching selector
  alerts                         Get active alerts
  health                         Check instance health

Flags:
  -c, --config <path>            Path to config file
  -i, --instance <name>          Target specific instance
  -a, --all                      Query all instances
  -h, --help                     Show this help

Examples:
  node cli.js init
  node cli.js query 'up'
  node cli.js query 'up' --all
  node cli.js metrics 'node_'
  node cli.js label-values instance
  node cli.js series '{__name__=~"node_cpu_.*"}'
`);
    process.exit(0);
  }
  
  const parsed = parseArgs(args);
  const configPath = parsed.flags.c || parsed.flags.config;
  const config = loadConfig(configPath);
  
  if (!commands[parsed.command]) {
    console.error(`Error: Unknown command "${parsed.command}"`);
    process.exit(1);
  }
  
  try {
    await commands[parsed.command](parsed, config);
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
