# RKM Examples

`sample.md` and `keywords.yml` are a self-contained, fully fictional walkthrough.
Run them from the skill root. Set a local password first (any string of 8+ characters):

```bash
export RKM_KEY="some long local secret"        # PowerShell: $env:RKM_KEY = "some long local secret"
```

1. Preview what would be masked (writes nothing):

   ```bash
   python scripts/rkm.py scan examples/sample.md --preset cn-sensitive --keywords examples/keywords.yml
   ```

2. Mask the document and write an encrypted mapping:

   ```bash
   python scripts/rkm.py protect examples/sample.md --preset cn-sensitive \
     --keywords examples/keywords.yml --out sample.masked.md --map sample.map.json
   ```

3. Edit `sample.masked.md` with an AI model, keeping every `[[...]]` placeholder intact.

4. Verify the edited file (add `--repair --out sample.fixed.md` if placeholders were mangled):

   ```bash
   python scripts/rkm.py verify sample.masked.md --map sample.map.json
   ```

5. Restore the original keywords locally:

   ```bash
   python scripts/rkm.py restore sample.masked.md --map sample.map.json --out sample.restored.md
   ```

`sample.restored.md` should match `examples/sample.md`.

On Windows you can avoid keeping the password in an environment variable by sealing it once with DPAPI:

```bash
python scripts/rkm.py seal-password --out rkm.key
python scripts/rkm.py --dpapi-password-file rkm.key protect examples/sample.md \
  --preset cn-sensitive --out sample.masked.md --map sample.map.json
```
