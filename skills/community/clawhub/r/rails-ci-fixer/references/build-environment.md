# Build Environment

Seeds, Node/Yarn, Tailwind, and missing system dependencies in CI.

## Seed Data

### Seeds fail on new validations
When new required columns are added, seed data creation breaks.
- **Fix**: Update `db/seeds.rb` to include the new required fields explicitly

## CI Build / Environment Failures

### Missing Node, Yarn, or npm
```text
yarn: command not found
npm: not found
node: command not found
```
- **Fix**: Add install step to `.github/workflows/ci.yml`:
  ```yaml
  - name: Setup Node
    uses: actions/setup-node@v4
    with:
      node-version: '20'
  - name: Install JS dependencies
    run: yarn install --frozen-lockfile
  ```

### Tailwind CSS not compiling in CI
- **Fix**: Ensure `yarn build:css` or equivalent runs before tests in CI workflow
- Check that `package.json` has the build script defined

### Asset precompilation failing
```text
ExecJS::RuntimeUnavailable or asset pipeline errors
```
- **Fix**: Add Node setup before asset precompile step in CI

### Missing system dependency (ImageMagick, libvips, etc.)
- **Fix**: Add an install step to the CI workflow, using the package names your
  image needs. On a self-hosted runner this step typically needs elevated
  privileges; on GitHub-hosted runners the packages are usually already present
  and the step can be skipped entirely.

  ```yaml
  - name: Install system dependencies
    run: <your package manager install command for the required libraries>
  ```

### CI workflow file location
`.github/workflows/ci.yml` — check and update this file when build steps fail, not just app code.
