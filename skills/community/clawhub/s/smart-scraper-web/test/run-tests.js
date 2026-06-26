module.exports = [
  { name: "no args shows status", args: [], expected: "Status:" },
  { name: "--help shows usage", args: ["--help"], expected: "Usage:" },
  { name: "invalid URL fails gracefully", args: ["--url", "not-a-url"], expected: "Error" },
  { name: "fetch with example.com", args: ["--url", "http://example.com"], expected: "extract" },
  { name: "fetch with cache flag", args: ["--url", "http://example.com", "--cache"], expected: "extract" },
  { name: "invalid flag fallback", args: ["--bogus-flag"], expected: "Status:" }
];
