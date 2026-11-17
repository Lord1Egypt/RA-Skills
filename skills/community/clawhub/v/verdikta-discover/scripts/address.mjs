import { keccak_256 } from '@noble/hashes/sha3';
import { bytesToHex } from '@noble/hashes/utils';

// EIP-55 checksum only; no wallet, provider or signing dependency.
export function supplierAddress(value) {
  if (typeof value !== 'string' || !/^0x[0-9a-fA-F]{40}$/.test(value) || /^0x0{40}$/i.test(value)) return null;
  const raw = value.slice(2), lower = raw.toLowerCase();
  const hash = bytesToHex(keccak_256(new TextEncoder().encode(lower)));
  const checked = [...lower].map((c, i) => parseInt(hash[i], 16) >= 8 ? c.toUpperCase() : c).join('');
  if (raw !== lower && raw !== raw.toUpperCase() && raw !== checked) return null;
  return `0x${checked}`;
}
