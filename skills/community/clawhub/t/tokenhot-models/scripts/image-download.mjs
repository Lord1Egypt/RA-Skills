import { Resolver } from 'node:dns/promises';
import { get } from 'node:https';
import { BlockList, isIP } from 'node:net';

const MAX_BYTES = 30 * 1024 * 1024;
const MAX_REDIRECTS = 3;
const DOWNLOAD_TIMEOUT = 30_000;
const nonPublic = new BlockList();
for (const [address, prefix] of [
  ['0.0.0.0', 8], ['10.0.0.0', 8], ['100.64.0.0', 10], ['127.0.0.0', 8],
  ['169.254.0.0', 16], ['172.16.0.0', 12], ['192.0.0.0', 24], ['192.0.2.0', 24],
  ['192.88.99.0', 24], ['192.168.0.0', 16], ['198.18.0.0', 15], ['198.51.100.0', 24],
  ['203.0.113.0', 24], ['224.0.0.0', 4], ['240.0.0.0', 4],
]) nonPublic.addSubnet(address, prefix);

export function imageExtension(bytes) {
  if (bytes.subarray(0, 8).equals(Buffer.from('89504e470d0a1a0a', 'hex'))) return '.png';
  if (bytes.subarray(0, 3).equals(Buffer.from('ffd8ff', 'hex'))) return '.jpg';
  const start = bytes.toString('ascii', 0, 6);
  if (start === 'GIF87a' || start === 'GIF89a') return '.gif';
  const brand = bytes.toString('ascii', 8, 12);
  if (bytes.toString('ascii', 0, 4) === 'RIFF' && brand === 'WEBP') return '.webp';
  if (bytes.toString('ascii', 4, 8) === 'ftyp' && (brand === 'avif' || brand === 'avis')) return '.avif';
  throw new Error('The result does not have a supported image signature.');
}

function parseUrl(rawUrl, previousUrl) {
  if (typeof rawUrl !== 'string' || !rawUrl.trim()) throw new Error('The image result URL is missing.');
  let url;
  try {
    url = new URL(rawUrl, previousUrl);
  } catch {
    throw new Error('The image result URL is invalid.');
  }
  if (url.protocol !== 'https:' || url.username || url.password || url.port) {
    throw new Error('The image result URL must use HTTPS without credentials or a custom port.');
  }
  return url;
}

async function resolveIPv4(hostname, signal) {
  const resolver = new Resolver({ timeout: 3000, tries: 1 });
  signal.throwIfAborted();
  const cancel = () => resolver.cancel();
  signal.addEventListener('abort', cancel, { once: true });
  try {
    return await resolver.resolve4(hostname);
  } finally {
    signal.removeEventListener('abort', cancel);
  }
}

async function publicAddress(hostname, resolve, signal) {
  const host = hostname.toLowerCase().replace(/\.$/, '');
  if (host === 'localhost' || host.endsWith('.localhost') || !host.includes('.')) {
    throw new Error('The image result host must resolve to a public IPv4 address.');
  }
  let addresses;
  try {
    addresses = isIP(host) === 4 ? [host] : await resolve(host, signal);
  } catch {
    throw new Error('The image result host could not be resolved.');
  }
  if (!addresses.length || addresses.some(address => isIP(address) !== 4 || nonPublic.check(address))) {
    throw new Error('The image result host must resolve to a public IPv4 address.');
  }
  return addresses[0];
}

function openImage(url, address, signal, request) {
  return new Promise((resolve, reject) => {
    const handle = request(url, {
      agent: false,
      family: 4,
      signal,
      // Keep the original host for TLS and pin the validated address for the socket.
      lookup: (_host, options, done) => options.all
        ? done(null, [{ address, family: 4 }])
        : done(null, address, 4),
      headers: { accept: 'image/avif,image/webp,image/png,image/jpeg,image/gif' },
    }, resolve);
    handle.once('error', reject);
  });
}

export function createImageDownloader({ resolve = resolveIPv4, request = get } = {}) {
  return async function download(rawUrl) {
    const signal = AbortSignal.timeout(DOWNLOAD_TIMEOUT);
    let url = parseUrl(rawUrl);
    for (let redirects = 0; ; redirects += 1) {
      const address = await publicAddress(url.hostname, resolve, signal);
      let response;
      try {
        response = await openImage(url, address, signal, request);
      } catch {
        throw new Error('The image result could not be downloaded.');
      }

      const status = response.statusCode;
      if ([301, 302, 303, 307, 308].includes(status)) {
        response.destroy();
        if (redirects >= MAX_REDIRECTS || !response.headers.location) {
          throw new Error('The image result exceeded the redirect limit or omitted its next location.');
        }
        url = parseUrl(response.headers.location, url);
        continue;
      }
      if (status !== 200) {
        response.destroy();
        throw new Error('The image result host did not return a complete file.');
      }
      if (Number(response.headers['content-length']) > MAX_BYTES) {
        response.destroy();
        throw new Error('The image result exceeds 30 MiB.');
      }

      const chunks = [];
      let size = 0;
      try {
        for await (const chunk of response) {
          size += chunk.length;
          if (size > MAX_BYTES) break;
          chunks.push(chunk);
        }
      } catch {
        throw new Error('The image result download was interrupted.');
      } finally {
        response.destroy();
      }
      if (size > MAX_BYTES) throw new Error('The image result exceeds 30 MiB.');
      const bytes = Buffer.concat(chunks, size);
      return { bytes, extension: imageExtension(bytes) };
    }
  };
}

export const downloadImage = createImageDownloader();
