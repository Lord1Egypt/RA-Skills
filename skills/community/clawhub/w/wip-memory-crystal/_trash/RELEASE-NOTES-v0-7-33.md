# Release Notes: memory-crystal v0.7.33

Related: #255

## Fix npm publish: include dist/ in package

The npm package was missing the `dist/` directory because `.gitignore` excludes it and there was no `files` array in package.json to override. The `crystal` CLI binary pointed to `dist/cli.js` which didn't exist in the published package. Every `npm install -g` installed a broken CLI.

Added `files` array to explicitly include `dist/` in the tarball. Added `prepublishOnly: npm run build` so the package is always built before publishing. The npm tarball now contains the compiled JavaScript that the CLI and MCP server need.
