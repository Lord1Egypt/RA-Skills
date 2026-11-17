module.exports = [
  // ── Store / Get / List ─────────────────────────────────────────────────
  { name: "--store stores a secret", args: ["--store", "testkey", "testvalue"], expected: "[secrets-manager] Stored:" },
  { name: "--get retrieves masked secret", args: ["--get", "testkey"], expected: "tes****ue" },
  { name: "--list shows stored secrets", args: ["--list"], expected: "testkey" },

  // ── Delete ─────────────────────────────────────────────────────────────
  { name: "--delete removes the secret", args: ["--delete", "testkey"], expected: "[secrets-manager] Deleted:" },
  { name: "--list after deletion shows empty", args: ["--list"], expected: "No secrets stored" },

  // ── Status ─────────────────────────────────────────────────────────────
  { name: "--status shows store info", args: ["--status"], expected: "[secrets-manager] Status:" },
  { name: "No args shows status", args: [], expected: "[secrets-manager] Status:" },

  // ── Edge Cases ─────────────────────────────────────────────────────────
  { name: "--get nonexistent shows not found", args: ["--get", "ghost"], expected: "[secrets-manager] Secret not found:" },
  { name: "--store without value shows usage", args: ["--store"], expected: "Usage:" },
];
