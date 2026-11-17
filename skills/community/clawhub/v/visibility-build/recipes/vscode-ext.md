---
id: vscode-ext
kind: asset
unlocks: [vscode-marketplace, open-vsx]
source: https://code.visualstudio.com/api/get-started/your-first-extension, https://code.visualstudio.com/api/working-with-extensions/publishing-extension, https://github.com/eclipse/openvsx/wiki/Publishing-Extensions (loaded 2026-11-08)
---
## Smallest version
One extension with one or two commands that call the product's API from the editor (e.g. "Send selection to <product>", "Look up <thing> under cursor"), with the API key stored via VS Code SecretStorage on first use. No views, webviews or language features unless that is the product.

## Scaffold
`npx --package yo@7.0.1 --package generator-code@1.12.0 -- yo code` (or `npm install --global yo@7.0.1 generator-code@1.12.0` then `yo code`); TypeScript template. Run with F5 (Extension Development Host).

## Fields the listings check
- `package.json`: `publisher` (required; the publisher ID, unchangeable once created), `name` (unique on the Marketplace), `version`, `engines.vscode` (required compatible range), `icon` (relative path to a PNG >=128x128; not SVG), `repository` (public GitHub lets vsce fix relative links), `displayName`, `description`, `categories`, `contributes.commands`.
- README/CHANGELOG image URLs must be `https`; no SVG images except trusted badge providers.
- Auth: Trusted Publishing from GitHub Actions `npx @vscode/vsce@4.1.0 publish --oidc` with `id-token: write`; or Azure DevOps PAT (All accessible organizations, Marketplace -> Manage scope; not recommended; global PATs retired 2026-12-01); or Entra ID `--azure-credential`.
- Open VSX: Eclipse account (same GitHub username), signed Publisher Agreement on open-vsx.org profile, access token, namespace = `publisher`.

## Steps
approve: run the pinned scaffold command above (it downloads packages), then scaffold with `yo code`; implement the command(s) calling the API; store the key with `context.secrets` (SecretStorage)
claude: fill package.json fields; add a 128px+ PNG icon, README with an https screenshot, CHANGELOG
claude: `vsce package` to build the .vsix
human: Marketplace publisher management page -> Create publisher (ID + Name) with a Microsoft account; set up Trusted Publishing or a PAT
human: Eclipse account, sign the Open VSX Publisher Agreement, create an Open VSX access token
approve: `vsce publish` (or `npx @vscode/vsce@4.1.0 publish --oidc` from Actions)
approve: `npx ovsx@1.4.0 create-namespace <publisher> -p <YOUR_OVSX_TOKEN>` once, then `npx ovsx@1.4.0 publish <file>.vsix -p <YOUR_OVSX_TOKEN>`

## Delegate
Command tests -> mattpocock-skills:tdd.

## Verify locally
`npm install -g @vscode/vsce@4.1.0 && vsce package` succeeds, then `code --install-extension <file>.vsix` (install flag unconfirmed on the pages loaded) or F5 and run the command against a test key.
