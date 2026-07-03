import { getAddress, isAddress } from 'viem';

import { ZERO_MERKLE_ROOT } from './policy.mjs';

function normalizeBytes32(value) {
  if (!/^0x[a-fA-F0-9]{64}$/.test(value)) throw new Error('Expected bytes32 hex value.');
  return value.toLowerCase();
}

export function allowlistManifestUrl(siteUrl, root) {
  return `${siteUrl.replace(/\/$/, '')}/allowlists/${normalizeBytes32(root)}.json`;
}

export async function fetchMintAllowlistProof(siteUrl, root, address) {
  if (root.toLowerCase() === ZERO_MERKLE_ROOT) {
    return { proof: [], source: 'open phase' };
  }

  const normalizedRoot = normalizeBytes32(root);
  const normalizedAddress = getAddress(address);
  const source = allowlistManifestUrl(siteUrl, normalizedRoot);
  const response = await fetch(source, { cache: 'no-store' });
  if (response.status === 404) return null;
  if (!response.ok) throw new Error(`Allowlist proof source failed with HTTP ${response.status}.`);

  const manifest = await response.json();
  if (typeof manifest.root !== 'string' || normalizeBytes32(manifest.root) !== normalizedRoot) {
    throw new Error('Allowlist manifest root mismatch.');
  }

  const proof = findProofInManifest(manifest, normalizedAddress);
  return proof ? { proof, source } : null;
}

function findProofInManifest(manifest, address) {
  const fromLeaves = findProofInLeaves(manifest.leaves, address)
    ?? findProofInLeaves(manifest.entries, address);
  if (fromLeaves) return fromLeaves;

  if (manifest.proofs && typeof manifest.proofs === 'object' && !Array.isArray(manifest.proofs)) {
    for (const [key, value] of Object.entries(manifest.proofs)) {
      if (isAddress(key) && getAddress(key).toLowerCase() === address.toLowerCase()) {
        return parseProof(value);
      }
    }
  }
  return null;
}

function findProofInLeaves(leaves, address) {
  if (!Array.isArray(leaves)) return null;
  for (const rawLeaf of leaves) {
    if (typeof rawLeaf?.address !== 'string' || !isAddress(rawLeaf.address)) continue;
    if (getAddress(rawLeaf.address).toLowerCase() !== address.toLowerCase()) continue;
    return parseProof(rawLeaf.proof);
  }
  return null;
}

function parseProof(value) {
  if (!Array.isArray(value)) return null;
  const proof = [];
  for (const item of value) {
    if (typeof item !== 'string') return null;
    proof.push(normalizeBytes32(item));
  }
  return proof;
}
