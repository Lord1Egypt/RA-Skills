export function renderHelp() {
  return `uStack — universal agent workspace compatibility and update engine

One workspace. Any agent.

Usage:
  ustack <command> [options]

Commands:
  import <github-url> [--name <id>]   Import and snapshot an upstream agent framework
  analyze <upstream-id>               Analyze latest upstream changes, produce structured report
  publish <upstream-id>               Generate website-ready update page from analysis
  update <upstream-id>                Pull latest upstream, analyze changes, and publish
  doctor                              Check workspace health and upstream state

Options:
  -h, --help     Show this help
  -v, --version  Show version

Examples:
  ustack import https://github.com/garrytan/gstack --name gstack
  ustack analyze gstack
  ustack publish gstack
  ustack update gstack
  ustack doctor

Upstream run artifacts live in:
  .ustack/upstreams/<id>/

Analysis and publish artifacts live in:
  .ustack/runs/<id>/<timestamp>/
`;
}
