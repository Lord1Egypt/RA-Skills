# Contributing to turf-skills

感谢你对 turf-skills 项目的关注！我们欢迎各种形式的贡献。

## Development Setup 开发环境设置

```bash
# Clone the repository
git clone https://github.com/zhyt1985/turf-skills.git
cd turf-skills

# Install dependencies
npm install

# Run tests
npm test

# Run coverage
npm run coverage
```

## Running Tests 运行测试

```bash
# Run all tests
npm test

# Run specific test file
node test/test.js
node test/error-handling.test.js
node test/edge-cases.test.js

# Run coverage
npm run coverage
```

## Code Style 代码风格

```bash
# Check code style
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Check formatting
npm run format:check
```

## Project Structure 项目结构

```
turf-skills/
├── index.js              # Main entry point
├── lib/                  # Core library modules
│   ├── parser.js        # Argument parsing
│   ├── measurement.js   # Measurement operations
│   ├── query.js         # Spatial query operations
│   ├── transformation.js # Transformation operations
│   ├── helpers.js       # Helper functions
│   ├── interpolation.js # Interpolation and grid operations
│   └── clustering.js    # Clustering operations
├── test/                # Test files
│   ├── test.js          # Main test suite
│   ├── error-handling.test.js # Error handling tests
│   ├── edge-cases.test.js     # Edge case tests
│   └── fixtures/        # Test data
├── SKILL.md             # Claude Code skill definition
├── README.md            # User documentation
└── package.json         # Package configuration
```

## Adding New Actions 添加新操作

1. **Add handler function** 在相应的 `lib/*.js` 文件中添加处理函数

```javascript
// Example: lib/measurement.js
module.exports = {
  // ... existing functions
  newAction(args) {
    // Your implementation
    return turf.newAction(args.input, { options: args.options });
  },
};
```

2. **Add tests** 在 `test/test.js` 中添加测试用例

```javascript
test('newAction', () => {
  const r = run('--action newAction --input ...');
  assert(r !== undefined);
});
```

3. **Update SKILL.md** 更新 SKILL.md 文档

在相应的类别下添加新操作的文档，包括：

- 操作名称
- 描述（中英文）
- 必需参数
- 可选参数

4. **Run lint and format** 运行代码检查和格式化

```bash
npm run lint:fix
npm run format
npm test
```

## Commit Guidelines 提交指南

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构
- `chore:` 构建/工具链相关

示例：

```bash
git commit -m "feat: add support for Turf.js dissolve operation"
git commit -m "fix: handle invalid GeoJSON input gracefully"
git commit -m "docs: update README with new examples"
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`npm test && npm run lint`)
5. Commit your changes
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Review Checklist

提交 PR 前，请确保：

- [ ] 所有测试通过 (`npm test`)
- [ ] 代码通过 lint 检查 (`npm run lint`)
- [ ] 代码已格式化 (`npm run format`)
- [ ] 添加了必要的测试
- [ ] 更新了相关文档（SKILL.md, README.md）
- [ ] 提交消息遵循规范

## Questions or Issues?

如果你有任何问题或建议：

- 提交 [Issue](https://github.com/zhyt1985/turf-skills/issues)
- 发起 [Discussion](https://github.com/zhyt1985/turf-skills/discussions)
- 查看 [Documentation](https://github.com/zhyt1985/turf-skills#readme)

## License

通过贡献代码，你同意你的贡献将使用与项目相同的 [MIT License](LICENSE) 进行授权。
