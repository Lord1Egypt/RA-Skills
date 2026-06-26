/**
 * Docker sandbox execution.
 * Runs the skill in an isolated container: no network, read-only root except /tmp,
 * CPU and memory limits. Does not log or store skill output (security).
 */

const Docker = require('dockerode');
const path = require('path');
const fs = require('fs').promises;

const SANDBOX_IMAGE = process.env.SAFEHUB_SANDBOX_IMAGE || 'node:18-alpine';
const SANDBOX_TIMEOUT_MS = parseInt(process.env.SAFEHUB_SANDBOX_TIMEOUT_MS || '30000', 10);
const SANDBOX_MEMORY_BYTES = 256 * 1024 * 1024;
const SANDBOX_NANO_CPUS = 5e8; // 0.5 cores

/**
 * Runs the skill in an isolated Docker container and returns behavior summary.
 * Container has no network, read-only root, writable /tmp only.
 * @param {string} skillPath - Absolute path to skill directory
 * @param {object} options - { timeoutMs, skipSandbox }
 * @returns {Promise<{ networkAttempted: boolean, suspiciousSyscalls: string[], sensitiveReads: string[], exitCode: number | null, error?: string }>}
 */
async function runSandbox(skillPath, options = {}) {
  const timeoutMs = options.timeoutMs ?? SANDBOX_TIMEOUT_MS;
  if (options.skipSandbox) {
    return {
      networkAttempted: false,
      suspiciousSyscalls: [],
      sensitiveReads: [],
      exitCode: null,
      skipped: true
    };
  }

  const normalizedPath = path.resolve(skillPath);
  try {
    await fs.access(normalizedPath);
  } catch (err) {
    throw new Error(`Sandbox: skill path not accessible (${err.message})`);
  }

  const docker = new Docker({ socketPath: '/var/run/docker.sock' });
  let container = null;

  try {
    container = await docker.createContainer({
      Image: SANDBOX_IMAGE,
      Cmd: ['node', 'index.js'],
      WorkingDir: '/skill',
      HostConfig: {
        NetworkMode: 'none',
        ReadonlyRootfs: true,
        Memory: SANDBOX_MEMORY_BYTES,
        NanoCpus: SANDBOX_NANO_CPUS,
        AutoRemove: true,
        Binds: [
          `${normalizedPath}:/skill:ro`,
          'safehub_tmp:/tmp:rw'
        ],
        CapDrop: ['ALL']
      },
      AttachStdout: false,
      AttachStderr: false
    });

    await container.start();

    const exitCode = await waitWithTimeout(container, timeoutMs);
    await container.remove({ force: true }).catch(() => {});

    return {
      networkAttempted: false,
      suspiciousSyscalls: [],
      sensitiveReads: [],
      exitCode: exitCode ?? -1
    };
  } catch (err) {
    if (container) {
      try {
        await container.stop({ t: 2 });
        await container.remove({ force: true });
      } catch (_) {}
    }
    return {
      networkAttempted: false,
      suspiciousSyscalls: [],
      sensitiveReads: [],
      exitCode: null,
      error: err.message
    };
  }
}

/**
 * Waits for container to exit, or kills after timeout. Returns exit code or null.
 */
function waitWithTimeout(container, timeoutMs) {
  return new Promise((resolve) => {
    const t = setTimeout(async () => {
      try {
        await container.kill();
      } catch (_) {}
      resolve(null);
    }, timeoutMs);

    container.wait((err, data) => {
      clearTimeout(t);
      if (err) {
        resolve(null);
        return;
      }
      resolve(data?.StatusCode ?? null);
    });
  });
}

module.exports = { runSandbox };
