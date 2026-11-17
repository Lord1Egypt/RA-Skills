module.exports = [
  { name: "no args shows workspace status", args: [], expected: "[smart-files] Workspace status" },
  { name: "--search without dir shows usage", args: ["--search", "test"], expected: "Usage: smart-files.js --search" },
  { name: "--search with dir works", args: ["--search", "test", "--dir", "."], expected: "[smart-files] Found" },
  { name: "--dedup finds duplicates", args: ["--dedup"], expected: "[smart-files] Found" },
  { name: "--status shows workspace", args: ["--status"], expected: "[smart-files] Workspace status" },
  { name: "--info without file shows usage", args: ["--info"], expected: "Usage: smart-files.js --info" },
  { name: "--cleanup analyzes workspace", args: ["--cleanup", "."], expected: "[smart-files] Cleanup analysis" }
];
