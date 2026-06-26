module.exports = [
  {
    name: "No args",
    command: "node smart-scraper.js",
    expected: "Usage:"
  },
  {
    name: "--help",
    command: "node smart-scraper.js --help",
    expected: "Usage:"
  },
  {
    name: "--url http://example.com",
    command: "node smart-scraper.js --url http://example.com",
    expected: "Fetching"
  },
  {
    name: "Invalid URL",
    command: "node smart-scraper.js --url https://this-domain-does-not-exist-12345.com",
    expected: "Error"
  },
  {
    name: "--cache flag with valid URL",
    command: "node smart-scraper.js --cache --url http://example.com",
    expected: "Fetching"
  },
  {
    name: "--no-cache flag with valid URL",
    command: "node smart-scraper.js --no-cache --url http://example.com",
    expected: "Fetching"
  },
  {
    name: "--extract --table with valid URL",
    command: "node smart-scraper.js --extract --table https://httpbin.org/html",
    expected: "Tables found"
  },
  {
    name: "--extract --list with valid URL",
    command: "node smart-scraper.js --extract --list https://httpbin.org/html",
    expected: "Lists found"
  },
  {
    name: "--extract --price with valid URL",
    command: "node smart-scraper.js --extract --price https://httpbin.org/html",
    expected: "Prices found"
  },
  {
    name: "--extract --article with valid URL",
    command: "node smart-scraper.js --extract --article https://httpbin.org/html",
    expected: "Article found"
  },
  {
    name: "--extract --all with valid URL",
    command: "node smart-scraper.js --extract --all https://httpbin.org/html",
    expected: "Extracted"
  },
  {
    name: "HTTP 404 error handling",
    command: "node smart-scraper.js --url https://httpbin.org/status/404",
    expected: "Error"
  },
  {
    name: "--extract --table with HTTP 404",
    command: "node smart-scraper.js --extract --table https://httpbin.org/status/404",
    expected: "Error"
  },
  {
    name: "--extract --list with HTTP 404",
    command: "node smart-scraper.js --extract --list https://httpbin.org/status/404",
    expected: "Error"
  },
  {
    name: "--extract --price with HTTP 404",
    command: "node smart-scraper.js --extract --price https://httpbin.org/status/404",
    expected: "Error"
  },
  {
    name: "--extract --article with HTTP 404",
    command: "node smart-scraper.js --extract --article https://httpbin.org/status/404",
    expected: "Error"
  },
  {
    name: "--extract --all with HTTP 404",
    command: "node smart-scraper.js --extract --all https://httpbin.org/status/404",
    expected: "Error"
  }
];