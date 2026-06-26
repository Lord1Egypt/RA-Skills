# Install a Pet

Use this workflow when the user asks to install a pet such as “install pet fox”.

## Steps

1. Confirm the pet id.
2. If the pet id is unclear, search the catalog API rather than scraping the website.
   - https://openpets.dev/pets/catalog.v3.json
3. Ensure the desktop app is running.
4. Install the pet:

```bash
openpets install <pet-id>
```

5. Verify available pets:

```bash
openpets pets
```

6. Optionally verify status:

```bash
openpets status
```

If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.

## Notes

- Do not hard-code current pet IDs in answers; use the live catalog API when uncertain.
- If the catalog or zip download fails, mention network access to `openpets.dev` and `zip.openpets.dev` may be required.
