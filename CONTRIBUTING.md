# Contributing to ShortsShield

Thank you for your interest in contributing to ShortsShield! This guide will help you get started.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Support other contributors

## Getting Started

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shortsshield.git
cd shortsshield
```

2. Install development dependencies:
```bash
./install.sh
pip3 install --user pytest pytest-cov pylint black
```

3. Run the application:
```bash
python3 shorts-facts.py
```

### Project Structure

```
shortsshield/
├── shorts-facts.py          # Main GUI application
├── shortsshield-cli.py      # CLI utility
├── install.sh               # Installation script
├── README.md                # User documentation
├── CONTRIBUTING.md          # This file
├── LICENSE                  # MIT License
├── sample_facts.json        # Sample fact database
├── requirements.txt         # Python dependencies
└── docs/
    ├── architecture.md      # System design
    ├── database.md          # Database schema
    └── development.md       # Developer guide
```

## Development Guidelines

### Code Style

Follow PEP 8 with these guidelines:

```python
# Good: Clear, descriptive names
def get_random_fact(self) -> Optional[FunFact]:
    """Get a random fun fact from the database."""
    pass

# Bad: Unclear abbreviations
def grf(self):
    pass
```

### Type Hints

Use type hints for better code clarity:

```python
# Good
def add_fact(self, text: str, category: str = "general") -> bool:
    pass

# Avoid
def add_fact(self, text, category="general"):
    pass
```

### Documentation

Write clear docstrings for all classes and methods:

```python
def get_random_fact(self) -> Optional[FunFact]:
    """
    Retrieve a random fun fact from the database.
    
    Prefers facts that haven't been displayed recently to avoid
    repetition. If all recent facts are exhausted, returns any random fact.
    
    Returns:
        FunFact: A random fact object, or None if database is empty.
        
    Raises:
        sqlite3.Error: If database query fails.
    """
    pass
```

### Testing

Write tests for new features:

```python
# test_shorts_facts.py
import pytest
from shorts_facts import FunFactDatabase

def test_add_fact():
    db = FunFactDatabase(":memory:")
    result = db.add_fact("Test fact", "test")
    assert result == True
    
def test_get_random_fact():
    db = FunFactDatabase(":memory:")
    db.add_fact("Fact 1", "test")
    fact = db.get_random_fact()
    assert fact is not None
    assert fact.text == "Fact 1"
```

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=shorts_facts
```

## Areas for Contribution

### 1. Fun Facts

Help expand our database! Submit new facts via:
- Pull request with updated `sample_facts.json`
- GitHub issue with fact suggestions
- Format: `{"text": "...", "category": "...", "source": "..."}`

**Categories**: science, history, animals, nature, technology, geography, biology, physics, chemistry, astronomy, etc.

### 2. Features

Popular feature requests:
- **Browser Extension**: Integrate directly with YouTube
- **API Backend**: Support syncing custom facts
- **Advanced Search**: Filter and search facts
- **Statistics**: Track learning progress
- **Internationalization**: Support multiple languages
- **Themes**: Additional color schemes and layouts
- **Text-to-Speech**: Audio fact playback

### 3. Documentation

- Improve README clarity
- Add tutorials and guides
- Document API endpoints
- Create video tutorials
- Translate documentation

### 4. Code Quality

- Fix bugs reported in issues
- Optimize performance
- Improve error handling
- Add edge case tests
- Refactor technical debt

### 5. Platform Support

- Test on different Linux distributions
- Create flatpak packaging
- Build snap package
- Create AppImage
- Windows/macOS ports

## Bug Reporting

Found a bug? Please report it:

1. **Check existing issues** to avoid duplicates
2. **Title**: Clear, concise description
3. **Environment**:
   ```
   - OS: Ubuntu 22.04
   - Python: 3.10
   - Installation: Using install.sh
   ```
4. **Steps to reproduce**: Detailed steps
5. **Expected behavior**: What should happen
6. **Actual behavior**: What actually happens
7. **Screenshots**: If applicable

## Feature Requests

Have an idea? Share it:

1. **Title**: Clear feature description
2. **Use case**: Why is this needed?
3. **Suggested implementation**: How would it work?
4. **Additional context**: Related issues or references

## Pull Request Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/shortsshield.git
   cd shortsshield
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test thoroughly**
   ```bash
   python3 shorts-facts.py  # Test GUI
   python3 shortsshield-cli.py --help  # Test CLI
   pytest tests/  # Run unit tests
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: Add amazing feature

   - Detail about implementation
   - Additional context
   - Fixes #123"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/my-feature
   ```

6. **Create Pull Request**
   - Link related issues
   - Describe changes clearly
   - Include screenshots if UI changes

## Commit Message Guidelines

Use conventional commits format:

```
feat: Add new feature
fix: Fix a bug
docs: Documentation updates
style: Code style improvements (no functionality change)
refactor: Refactor code (no functionality change)
perf: Performance improvements
test: Add or update tests
chore: Build, CI, or dependency updates
```

Examples:
```
feat: Add fact search functionality
fix: Correct database connection timeout
docs: Update installation instructions
style: Format code to PEP 8 standards
```

## Code Review

When submitting a PR, expect review feedback. Please:
- Respond to all comments
- Make requested changes
- Push updates to the same branch
- Request re-review when done

## Release Process

1. Update version in code
2. Update CHANGELOG.md
3. Create release tag
4. Update package managers (snap, flatpak)

## Development Tools

Recommended tools:
- **IDE**: VS Code, PyCharm, Vim
- **Linting**: pylint, flake8
- **Formatting**: black, autopep8
- **Testing**: pytest, pytest-cov
- **Version Control**: git, gitk
- **Documentation**: Sphinx, markdown

## Performance Considerations

When contributing code:
- Keep startup time < 500ms
- Database queries < 5ms
- Memory usage < 100MB
- UI responsive during long operations
- Use threading for blocking operations

## Security

- Never commit API keys or secrets
- Validate all user input
- Use parameterized database queries (never string concatenation)
- Keep dependencies updated
- Report security issues privately

## Getting Help

- **Documentation**: Check README.md and docs/
- **Issues**: Search existing issues
- **Discussions**: Start a discussion on GitHub
- **Email**: Contact maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors list

Thank you for contributing! 🎉
