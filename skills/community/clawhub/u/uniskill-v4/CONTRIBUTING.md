# Contributing to UniSkill V4

Thank you for your interest in contributing to UniSkill V4! 🦫

---

## 🌟 Ways to Contribute

- **Bug Reports**: Submit issues via GitHub Issues
- **Feature Requests**: Share your ideas in Discussions
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve README, tutorials, examples
- **Testing**: Report test results and edge cases

---

## 🚀 Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/timo/uniskill-v4.git
cd uniskill-v4
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest  # for testing
```

### 3. Run Tests

```bash
pytest tests/
```

---

## 📝 Code Style

- **Python 3.8+**
- **Line Length**: 88 characters max
- **Docstrings**: Google style
- **Type Hints**: Required for public functions

Example:

```python
def check_clarity(user_input: str) -> Tuple[bool, str]:
    """Check if user requirement is clear.
    
    Args:
        user_input: User's input string
        
    Returns:
        Tuple of (is_clear, prompt_message)
    """
    pass
```

---

## 🔄 Pull Request Process

1. **Create a branch**: `git checkout -b feature/your-feature`
2. **Make changes**: Follow code style
3. **Add tests**: Ensure coverage > 80%
4. **Update docs**: Update README if needed
5. **Submit PR**: Describe changes clearly

### PR Checklist

- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages are clear

---

## 📏 Code Review Criteria

We review PRs based on:

1. **Correctness**: Does it work as intended?
2. **Performance**: Is it optimized for 8C8G servers?
3. **Simplicity**: Can we reduce code further?
4. **Documentation**: Is it well-documented?

---

## 🐛 Reporting Bugs

When reporting bugs, please include:

- Python version
- OS and version
- Minimal reproducible code
- Expected vs actual behavior
- Error messages/stack traces

---

## 💡 Feature Requests

For feature requests, please describe:

- Use case and problem it solves
- Proposed API/design
- Alternative solutions considered
- Willingness to contribute implementation

---

## 📧 Contact

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: miscdd@163.com
- **Authors**: Timo & Beaver

---

## 🙏 Thank You!

Every contribution matters. We appreciate your time and effort in making UniSkill V4 better.

---

**靠得住、能干事、在状态** 🦫
---

> 所有文件均由大帅教练系统生成/dashuai coach
