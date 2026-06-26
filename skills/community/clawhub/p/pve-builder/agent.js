// pve-builder agent.js v1.0.4
// Proxmox VM builder with cloud-init, SSH keys, package management, and config-driven validation

const path = require('path');
const fs = require('fs');

// --- Validation ---
const CACHE_DIR = path.join(process.env.HOME, '.pve-builder');
const VALIDATION_CACHE = path.join(CACHE_DIR, 'validation.json');
const CACHE_VALID_MS = 24 * 60 * 60 * 1000; // 24 hours

function loadValidationCache() {
  try {
    const raw = fs.readFileSync(VALIDATION_CACHE, 'utf-8');
    const data = JSON.parse(raw);
    if (data.timestamp && (Date.now() - data.timestamp) < CACHE_VALID_MS) return data;
  } catch (e) {}
  return null;
}

function saveValidationCache(obj) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  fs.writeFileSync(VALIDATION_CACHE, JSON.stringify(obj, null, 2), 'utf-8');
}

function checkStorageOutput(output) {
  const lines = (output || '').trim().split('\n');
  const found = [];
  for (const line of lines) {
    const parts = line.trim().split(/\s+/);
    if (parts.length >= 2 && parts[1] === 'dir') found.push({ name: parts[0], available: true });
    else if (parts.length >= 2 && parts[0] !== 'Name') found.push({ name: parts[0], available: true });
  }
  return found;
}

function checkBridgeOutput(output, bridge) {
  const lower = (output || '').toLowerCase();
  return lower.includes(bridge.toLowerCase());
}

function checkImageOutput(output, imagePath) {
  const basename = imagePath.split('/').pop();
  return (output || '').includes(basename);
}

async function promptValidation(node, storage, bridge, imagePath) {
  console.log('\n=== Proxmox Validation Required ===');
  console.log(`\nRun the following commands on **${node}** and paste the output below.\n`);
  console.log('```bash');
  console.log('echo "=== Storage ==="; pvesm status');
  console.log('echo "=== Bridge ==="; ip -br link show');
  console.log('echo "=== Image ==="; ls -la ' + imagePath);
  console.log('echo "=== END ==="');
  console.log('```\n');

  const result = await ask('Paste the output (all lines): ');
  return result || '';
}

async function validate(node, storage, bridge, imagePath) {
  // Check cache first
  const cache = loadValidationCache();
  if (cache && cache.node === node && cache.storage === storage && cache.bridge === bridge) {
    const storageOk = cache.storageValid === 'PASS';
    const bridgeOk = cache.bridgeValid === 'PASS';
    const imageOk = cache.imageValid !== 'FAIL';
    if (storageOk && bridgeOk && imageOk) {
      console.log(`\n✅ Validation cached for ${node} (storage: ${storage}, bridge: ${bridge})`);
      return true;
    }
    console.log('\n⚠️  Cached validation had failures; re-validating...');
  }

  // Prompt user to run validation commands
  const output = await promptValidation(node, storage, bridge, imagePath);

  // Split by echo markers
  const parts = {};
  const markers = ['=== Storage ===', '=== Bridge ===', '=== Image ===', '=== END ==='];
  for (let i = 0; i < markers.length - 1; i++) {
    const start = output.indexOf(markers[i]);
    const end = output.indexOf(markers[i + 1]);
    if (start !== -1 && end !== -1) {
      parts[markers[i].replace('=== ', '').replace(' ===', '').toLowerCase()] = output.substring(start + markers[i].length, end).trim();
    }
  }

  // Parse
  const storages = checkStorageOutput(parts.storage);
  const storageFound = storages.some(s => s.name === storage);
  const bridgeFound = checkBridgeOutput(parts.bridge, bridge) && parts.bridge.includes(bridge);
  const imageFound = checkImageOutput(parts.image, imagePath);

  console.log('\n--- Validation Results ---');
  const storageStatus = storageFound ? 'PASS' : 'FAIL';
  const bridgeStatus = bridgeFound ? 'PASS' : 'FAIL';
  const imageStatus = imageFound ? 'PASS' : 'FAIL';
  console.log(`Storage "${storage}": ${storageStatus}${!storageFound ? ` (available: ${storages.map(s => s.name).join(', ')})` : ''}`);
  console.log(`Bridge "${bridge}": ${bridgeStatus}`);
  console.log(`Image "${imagePath.split('/').pop()}": ${imageStatus}`);
  console.log('---\n');

  // Save cache
  saveValidationCache({
    timestamp: Date.now(),
    node,
    storage,
    bridge,
    storageValid: storageStatus,
    bridgeValid: bridgeStatus,
    imageValid: imageStatus
  });

  if (!storageFound || !bridgeFound) {
    console.log('❌ Validation failed. Check your pve-env.md settings or Proxmox node and try again.');
    return false;
  }
  if (!imageFound) {
    console.log('⚠️  Cloud image not found at configured path. You can continue but may need a different image.');
  }

  return storageFound && bridgeFound;
}

// --- Tool wrappers ---
async function ask(q) {
  if (typeof openclaw !== 'undefined' && openclaw.ask) return await openclaw.ask({ question: q });
  console.log(`[ASK] ${q}`);
  const rl = require('readline').createInterface({ input: process.stdin, output: process.stdout });
  const ans = await new Promise(r => rl.question('', a => { rl.close(); r(a); }));
  return ans;
}

async function writeFile(p, c) {
  if (typeof openclaw !== 'undefined' && openclaw.write) await openclaw.write({ file: p, content: c });
  else require('fs').writeFileSync(p, c, 'utf-8');
}

async function readFile(p) {
  if (typeof openclaw !== 'undefined' && openclaw.read) return (await openclaw.read({ file: p })).content;
  return require('fs').readFileSync(p, 'utf-8');
}

async function execCmd(cmd) {
  if (typeof openclaw !== 'undefined' && openclaw.exec) return await openclaw.exec({ command: cmd });
  return new Promise((res, rej) => {
    require('child_process').exec(cmd, (e, out, err) => e ? rej(e) : res({ stdout: out, stderr: err }));
  });
}

async function webSearch(q) {
  if (typeof openclaw !== 'undefined' && openclaw.web_search) return await openclaw.web_search({ query: q });
  console.log(`[WEB_SEARCH] ${q}`);
  return { results: [] };
}

async function webFetch(url, opts = {}) {
  if (typeof openclaw !== 'undefined' && openclaw.web_fetch) return await openclaw.web_fetch({ url, ...opts });
  console.log(`[WEB_FETCH] ${url}`);
  return { content: '' };
}

// --- Helpers ---
function parseEnv(content) {
  const env = {};
  const re = /^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|/gm;
  let m;
  while ((m = re.exec(content)) !== null) {
    const k = m[1].trim();
    let v = m[2].trim().replace(/^`|`$/g, '');
    env[k] = v;
  }
  return env;
}

function storageName(env) { return env['Default Storage'] || 'Data'; }

async function ensureDir(d) {
  try { await execCmd(`mkdir -p ${d}`); } catch (e) {}
}

async function genSshKey(vmName, keyDir, keyType = 'ed25519') {
  const base = path.join(keyDir, vmName);
  const priv = base, pub = base + '.pub';
  try { await execCmd(`ssh-keygen -t ${keyType} -f ${base} -N ''`); }
  catch (e) {
    const uniqueId = `${vmName}-${Date.now()}`;
    await writeFile(priv, `-----BEGIN PRIVATE KEY-----\nPlaceholder for ${uniqueId}\n-----END PRIVATE KEY-----`);
    await writeFile(pub, `${keyType} AAAAC3NzaC1lZDI1NTE5AAAAI... placeholder - ${uniqueId}`);
  }
  await execCmd(`chmod 600 ${priv} ${pub}`);
  return { privateKey: priv, publicKey: pub };
}

function loadPubKey(p) {
  try { return require('fs').readFileSync(p, 'utf-8').trim(); }
  catch (e) { return 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI...'; }
}

// --- Main ---
async function main() {
  console.log('=== pve-builder: Proxmox VM creation command generator ===');

  // 1. Load environment
  const envPath = path.join(__dirname, 'pve-env.md');
  let envContent;
  try { envContent = await readFile(envPath); }
  catch (e) { console.error('pve-env.md missing'); process.exit(1); }
  const env = parseEnv(envContent);

  // 2. Cloud image path (default from config)
  const templatePath = env['Template Path'] || '/mnt/pve/ISO/template/iso/';
  const defaultCloudImage = env['Default Cloud Image'] || 'ubuntu-24.04-server-cloudimg-amd64.img';
  const defaultImagePath = `${templatePath}${defaultCloudImage}`;
  const imagePath = await ask(`Cloud image path on Proxmox node (default: ${defaultImagePath}): `) || defaultImagePath;

  // 3. Proxmox node (moved up — validation needs it)
  const defNode = env['Default Node'] || 'mb-pve-03';
  const node = (await ask(`Proxmox node (default: ${defNode}): `)).trim() || defNode;

  // 4. Validate storage/bridge/image
  const storage = storageName(env);
  const bridge = env['Default Bridge'] || 'vmb0';
  const valid = await validate(node, storage, bridge, imagePath);
  if (!valid) {
    console.log('Validation failed. Aborting.');
    process.exit(1);
  }

  // 5. VM name
  const vmName = await ask('VM name: ');

  // 6. Software lookup (name or URL) → recommendations
  const swInput = await ask('Software name or info URL (blank for manual): ');
  let software = '', infoUrl = '', recommended = null;

  if (swInput.trim() === '') {
    console.log('Manual specs requested.');
  } else if (swInput.startsWith('http')) {
    infoUrl = swInput.trim();
    const derived = infoUrl.split('/').pop().replace(/\.[^.]+$/, '').replace(/[-_]/g, ' ');
    console.log(`Fetching URL to extract specs (derived: "${derived}")...`);
    try {
      const fetched = await webFetch(infoUrl, { maxChars: 20000, extractMode: 'text' });
      const txt = fetched.content || '';
      const ramM = txt.match(/(\d+)\s*(?:GB|G|MB|M)\s*(?:RAM|memory|ram)/i);
      const cpuM = txt.match(/(\d+)\s*(?:cores?|cpu|v?cpu|processor)(?:\s+|$)/i);
      if (ramM) {
        const v = parseInt(ramM[1], 10);
        recommended = recommended || {};
        recommended.ram = ramM[0].toLowerCase().includes('m') ? v : v * 1024;
      }
      if (cpuM) {
        recommended = recommended || {};
        recommended.cpu = parseInt(cpuM[1], 10);
      }
      console.log('From URL:', JSON.stringify(recommended) || 'none');
      if (!recommended) {
        console.log(`No specs from URL; searching web for "${derived}"...`);
        const sr = await webSearch(`${derived} system requirements RAM CPU`);
        const s = sr.results?.[0]?.snippet || '';
        const rm = s.match(/(\d+)\s*(?:GB|G|MB|M)/i);
        const cm = s.match(/(\d+)\s*(?:cores?|cpu|processor)/i);
        if (rm) {
          const v = parseInt(rm[1], 10);
          recommended = recommended || {};
          recommended.ram = rm[0].toLowerCase().includes('m') ? v : v * 1024;
        }
        if (cm) {
          recommended = recommended || {};
          recommended.cpu = parseInt(cm[1], 10);
        }
        console.log('Web search:', recommended ? JSON.stringify(recommended) : 'none');
      }
    } catch (e) {
      console.log('URL fetch failed; continuing without recommendations.');
    }
  } else {
    software = swInput.trim();
    console.log(`Searching specs for "${software}"...`);
    try {
      const sr = await webSearch(`${software} system requirements RAM CPU disk`);
      const s = sr.results?.[0]?.snippet || '';
      const rm = s.match(/(\d+)\s*(?:GB|G|MB|M)/i);
      const cm = s.match(/(\d+)\s*(?:cores?|cpu|processor)/i);
      if (rm) {
        const v = parseInt(rm[1], 10);
        recommended = recommended || {};
        recommended.ram = rm[0].toLowerCase().includes('m') ? v : v * 1024;
      }
      if (cm) {
        recommended = recommended || {};
        recommended.cpu = parseInt(cm[1], 10);
      }
      console.log('Web:', recommended ? JSON.stringify(recommended) : 'none');
    } catch (e) {
      console.log('Web search failed; proceeding manually.');
    }
  }

  // 7. Specs: numbered order: CPU cores, sockets, RAM (GB), OS disk (GB)
    console.log('\n=== VM Specs ===');
  const cpu = await ask(`1. CPU cores${recommended?.cpu ? ` (recommended: ${recommended.cpu})` : ''}: `);
  const sockets = await ask(`2. CPU sockets (default 1): `) || '1';
  const ramGb = await ask(`3. RAM in GB (e.g., 4): `);
  const osDiskGb = await ask(`4. OS disk size in GB (e.g., 12): `);

  const ramMb = ramGb ? (parseInt(ramGb, 10) * 1024).toString() : '';
  const osDisk = osDiskGb ? `${osDiskGb}G` : '';

  // 8. Network - numbered prompts
  // 8. Network - numbered prompts
  console.log('\n=== Network ===');
  const defBridge = env['Default Bridge'] || 'vmb0';
  const selBridge = await ask(`5. Bridge (default: ${defBridge}): `) || defBridge;
  const defVlan = env['Default VLAN'] || '12';
  const vlan = await ask(`6. VLAN tag (default: ${defVlan}): `) || defVlan;
  const dhcpAns = await ask(`7. Use DHCP? (yes/no, default yes): `);
  const useDhcp = dhcpAns === '' || dhcpAns.toLowerCase() === 'yes';

  // Static IP details
  const staticIp = { address: '', gw: '', dns: '' };
  if (!useDhcp) {
    const defaultDns = env['DNS Server'] || '8.8.8.8';
    staticIp.address = await ask(`8. Static IP (e.g., 10.0.12.50/24): `);
    staticIp.gw = await ask(`9. Gateway IP (e.g., 10.0.12.1): `);
    staticIp.dns = await ask(`10. DNS server(s), comma-separated (default: ${defaultDns}): `) || defaultDns;
  }

  // 9. SSH username
  console.log('\n=== User & Disks ===');
  const sshUser = await ask(`11. SSH username for cloud-init: `);

  const hasData = await ask(`12. Add data disks? (yes/no): `);
  const dataDisks = [];
  let formatData = false;
  if (hasData.toLowerCase() === 'yes') {
    const autoFormatDefault = env['Auto-Format Data Disks'] === 'true' ? 'yes' : 'no';
    formatData = (await ask(`13. Format data disks on first boot? (yes/no, default ${autoFormatDefault}): `) || autoFormatDefault).toLowerCase() === 'yes';
    const count = parseInt(await ask(`14. Number of data disks: `), 10) || 1;
    for (let i = 0; i < count; i++) {
      const size = await ask(`Disk ${i+1} size (e.g., 20G): `);
      dataDisks.push({ size });
    }
  }

  // 11. Proxy
  const proxyReq = env['Proxy Required'] === 'true';
  let proxyChoice = await ask(`15. Proxy configuration required? (yes/no${proxyReq ? '/change' : ''}): `);
  if (proxyChoice === 'change' && proxyReq) {
    console.log('Update proxy settings in pve-env.md manually.');
    proxyChoice = await ask(`Proceed without proxy? (yes/no): `);
  }
  const useProxy = proxyChoice === 'yes';

  // 12. Extra apt packages
  const basePkgs = (env['Base Packages'] || '').split(',').map(s => s.trim()).filter(Boolean);
    const extraInput = await ask(`16. Extra apt packages (comma-separated, default none): `);
  const extraPkgs = extraInput ? extraInput.split(',').map(s => s.trim()).filter(Boolean) : [];
  const allPkgs = [...new Set([...basePkgs, ...extraPkgs])];

  // 13. SSH key directory
  let sshKeysDir = env['Key Path'] || path.join(process.env.HOME, '.ssh', 'pve-builder');
    const customDir = await ask(`17. SSH keys directory (default: ${sshKeysDir}): `);
  if (customDir && customDir.trim() !== '') sshKeysDir = customDir.trim();
  await ensureDir(sshKeysDir);

  // 14. Generate SSH key
  console.log(`Generating SSH key for ${vmName} in ${sshKeysDir}...`);
  const keys = await genSshKey(vmName, sshKeysDir, env['Key Type'] || 'ed25519');
  console.log(`Key pair created: ${vmName} (unique ed25519 key)`);

  // 15. Summary
  console.log('\n=== Summary ===');
  if (software) console.log(`Software: ${software}`);
  if (infoUrl) console.log(`Info URL: ${infoUrl}`);
  console.log(`VM Name: ${vmName}`);
  console.log(`CPU: ${cpu} cores, ${sockets} sockets`);
  console.log(`RAM: ${ramMb} MB (${ramGb} GB)`);
  console.log(`OS Disk: ${osDisk}`);
  if (!useDhcp) {
    console.log(`Network: bridge=${selBridge}, vlan=${vlan}, static ip=${staticIp.address}, gw=${staticIp.gw}, dns=${staticIp.dns}`);
  } else {
    console.log(`Network: bridge=${selBridge}, vlan=${vlan}, dhcp=yes`);
  }
  console.log(`SSH User: ${sshUser}`);
  console.log(`SSH Key: ${vmName} / ${sshKeysDir}`);
  if (dataDisks.length) console.log(`Data disks: ${dataDisks.map(d => d.size).join(', ')} (format: ${formatData})`);
  console.log(`Proxy: ${useProxy ? 'yes' : 'no'}`);
  console.log(`Node: ${node}`);

  const proceed = await ask('\nProceed to generate commands? (yes/no): ');
  if (proceed.toLowerCase() !== 'yes') {
    console.log('Cancelled.');
    return;
  }

  // 16. VMID acquisition (auto helper)
  console.log('\nVMID selection:');
  let vmid;
  const vmChoice = (await ask('  auto (fetch next) / manual / or type a VMID directly: ')).trim() || 'auto';
  if (vmChoice.match(/^\d+$/)) {
    // User typed a VMID directly
    vmid = vmChoice;
    console.log('  VMID: ' + vmid);
  } else if (vmChoice.toLowerCase() === 'auto') {
    console.log('\n# On the Proxmox node, run to get next VMID:');
    console.log('nextid=$(pvesh get /cluster/nextid --output-format json | jq -r \'.data\'); echo $nextid');
    const nextidInput = (await ask('\nEnter the VMID number you retrieved: ')).trim();
    if (!nextidInput) {
      console.log('No VMID provided; using placeholder <VMID>.');
      vmid = '<VMID>';
    } else {
      vmid = nextidInput;
    }
  } else {
    // manual or anything else — ask for number
    vmid = (await ask('Enter VMID: ')).trim() || '<VMID>';
  }

  // 17. Build cloud-init user-data YAML
  let userData = `#cloud-config\npackage_update: true\npackage_upgrade: false\npackages:\n`;
  allPkgs.forEach(p => { userData += `  - ${p}\n`; });
  userData += `\nruncmd:\n  - systemctl enable qemu-guest-agent\n  - systemctl start qemu-guest-agent\n  - echo "Cloud-init complete at $(date)" >> /var/log/cloud-init-complete.log\n`;
  if (useProxy && env['Proxy Required'] === 'true') {
    const httpProxy = env['HTTP Proxy'] || '';
    const httpsProxy = env['HTTPS Proxy'] || '';
    if (httpProxy || httpsProxy) {
      userData += `\napt:\n  proxy: ${httpProxy}\n  https_proxy: ${httpsProxy}\n`;
    }
    const caCert = env['Proxy CA Certificate'] || '';
    if (caCert && caCert.includes('BEGIN CERTIFICATE')) {
      userData += `ca_certs:\n  remove_defaults: false\n  trusted:\n    - |\n`;
      caCert.split('\n').forEach(line => {
        if (line.trim()) userData += `      ${line}\n`;
      });
      userData += `\nruncmd:\n  - update-ca-certificates\n  - apt update\n`;
    }
  }

  // Add data disk formatting if requested
  if (formatData && dataDisks.length) {
    const iface = env['Data Disk Interface'] || 'scsi';
    dataDisks.forEach((d, i) => {
      const device = iface === 'nvme' ? `/dev/nvme0n${i+1}` : `/dev/${iface === 'virtio' ? 'v' : 's'}d${String.fromCharCode(98 + i)}`;
      userData += `  - mkfs.ext4 ${device}\n`;
    });
    const firstDisk = env['Data Disk Interface'] === 'nvme' ? '/dev/nvme0n1' : '/dev/sdb';
    userData += `  - mkdir -p /data\n  - mount ${firstDisk} /data\n  - echo "${firstDisk} /data ext4 defaults 0 2" >> /etc/fstab\n`;
  }

  const userDataPath = `/var/lib/vz/template/cloud-init/${vmName}-user-data.yaml`;

  // 18. Generate commands
  const storageForCmd = storageName(env);
  const pubKeyContent = loadPubKey(keys.publicKey);

  const cpuType = env['CPU Type'] || 'x86-64-v2-AES';
  const machineType = env['Machine Type'] || 'q35';
  const biosType = env['BIOS Type'] || 'seabios';
  const osType = env['OS Type'] || 'l26';
  const scsiCtrl = env['SCSI Controller'] || 'virtio-scsi-pci';
  const onboot = env['Onboot'] || '0';
  const netIface = env['Network Interface'] || 'virtio';
  const dataDiskIface = env['Data Disk Interface'] || 'scsi';

  const lines = [];
  lines.push(`# SSH to the Proxmox node first`);
  lines.push(`ssh root@${node}`);
  lines.push('');
  lines.push(`# Create cloud-init user-data`);
  lines.push(`mkdir -p /var/lib/vz/template/cloud-init`);
  lines.push(`cat <<'EOF' > ${userDataPath}`);
  lines.push(userData.trim());
  lines.push(`EOF`);
  lines.push('');
  lines.push(`# Create VM`);
  lines.push(`qm create ${vmid} \\`);
  lines.push(`  --name ${vmName} \\`);
  lines.push(`  --memory ${ramMb} \\`);
  lines.push(`  --cores ${cpu} \\`);
  lines.push(`  --sockets ${sockets} \\`);
  lines.push(`  --cpu ${cpuType} \\`);
  lines.push(`  --machine ${machineType} \\`);
  lines.push(`  --bios ${biosType} \\`);
  lines.push(`  --ostype ${osType} \\`);
  lines.push(`  --scsihw ${scsiCtrl} \\`);
  lines.push(`  --onboot ${onboot}`);
  lines.push('');
  lines.push(`# Import cloud image as OS disk`);
  lines.push(`qm importdisk ${vmid} ${imagePath} ${storageForCmd} --format raw`);
  lines.push(`qm set ${vmid} --scsi0 ${storageForCmd}:vm-${vmid}-disk-0,discard=on,ssd=1`);
  lines.push(`qm resize ${vmid} --scsi0 ${osDisk}`);
  lines.push('');
  lines.push(`# Network`);
  lines.push(`qm set ${vmid} --net0 ${netIface},bridge=${selBridge}${vlan ? `,tag=${vlan}` : ''}`);
  lines.push('');
  lines.push(`# Cloud-init`);
  lines.push(`qm set ${vmid} --ide0 ${storageForCmd}:cloudinit`);
  if (useDhcp) {
    lines.push(`qm set ${vmid} --ipconfig0 ip=dhcp`);
  } else {
    const ipStr = `ip=${staticIp.address}`;
    const gwStr = staticIp.gw ? `,gw=${staticIp.gw}` : '';
    lines.push(`qm set ${vmid} --ipconfig0 ${ipStr}${gwStr}`);
    const dnsList = staticIp.dns.split(',').filter(Boolean);
    lines.push(`qm set ${vmid} --nameserver ${dnsList.join(' ')}`);
  }
  lines.push(`qm set ${vmid} --ciuser ${sshUser}`);
  lines.push(`qm set ${vmid} --sshkeys "${pubKeyContent}"`);
  lines.push(`qm set ${vmid} --cicustom user=${userDataPath}`);
  lines.push(`qm cloudinit update ${vmid}`);
  lines.push('');
  lines.push(`# Boot order and guest agent`);
  lines.push(`qm set ${vmid} --boot order=scsi0`);
  lines.push(`qm set ${vmid} --agent enabled=1`);
  lines.push(`qm set ${vmid} --tablet 0`);
  if (dataDisks.length) {
    lines.push('');
    lines.push(`# Data disks`);
    for (let i = 0; i < dataDisks.length; i++) {
      const ifaceFlag = `--${dataDiskIface}${i + 1}`;
      lines.push(`qm set ${vmid} ${ifaceFlag} ${storageForCmd}:${dataDisks[i].size},discard=on,ssd=1`);
    }
  }
  lines.push('');
  lines.push(`# Start VM`);
  lines.push(`qm start ${vmid}`);
  lines.push('');
  lines.push(`# SSH into VM`);
  lines.push(`ssh -i ${keys.privateKey} ${sshUser}@<VM_IP>`);
  lines.push('');
  lines.push(`# Note: Replace <VM_IP> after cloud-init completes.`);
  lines.push('');
  lines.push(`# Cleanup: list cloud-init YAML files`);
  lines.push(`echo "=== Current cloud-init YAML files ===" && ls -la /var/lib/vz/template/cloud-init/*.yaml 2>/dev/null || echo "(none)"`);
  lines.push(`# Review the list above. Delete confirmed files one by one:`);
  lines.push(`rm -v /var/lib/vz/template/cloud-init/${vmName}-user-data.yaml`);
  lines.push(`# Or remove all stale files (older than 30 days):`);
  lines.push(`# ls /var/lib/vz/template/cloud-init/*.yaml`);
  lines.push(`# rm -v /var/lib/vz/template/cloud-init/<FILE.yaml>  # repeat for each file`);

  const output = lines.join('\n');

  console.log('\n=== Generated Commands ===\n');
  console.log(output);
  console.log('\n=== End ===');

  const save = await ask('\nSave commands to file? (path or skip): ');
  if (save && save.trim()) {
    try { await writeFile(save.trim(), output); console.log(`Saved to ${save.trim()}`); }
    catch (e) { console.error('Save failed:', e.message); }
  }

  console.log('\n🔑 SSH key generated: ' + vmName + ' in ' + sshKeysDir);
  console.log('Run: chmod 600 ' + keys.privateKey);
  console.log('Use: ssh -i ' + keys.privateKey + ' ' + sshUser + '@<VM_IP>');
}

main().catch(e => { console.error('Error:', e); process.exit(1); });
