"""
Additional template manager tests
"""

import pytest

from social_media_automation.core.template_manager import TemplateManager
from social_media_automation.storage.template_store import TemplateStore


@pytest.fixture
def template_store(tmp_path):
    """Create a temporary template store"""
    store = TemplateStore(str(tmp_path / "templates.db"))
    yield store


@pytest.fixture
def template_manager(template_store):
    """Create a TemplateManager instance"""
    return TemplateManager(template_store)


def test_template_with_special_characters(template_manager):
    """Test template with special characters"""
    template_manager.create_template(
        name="special",
        content="Test {{name}} with {{emoji}} 🎉",
        platform="x",
        variables=["name", "emoji"],
    )

    content = template_manager.use_template("special", {"name": "John", "emoji": "🚀"})

    assert "🚀" in content


def test_template_with_multiline(template_manager):
    """Test template with multiline content"""
    template_manager.create_template(
        name="multiline",
        content="Hello {{name}},\n\nWelcome to {{company}}!\n\nBest regards",
        platform="x",
        variables=["name", "company"],
    )

    content = template_manager.use_template("multiline", {"name": "John", "company": "Acme"})

    assert "\n\n" in content
    assert "John" in content
    assert "Acme" in content


def test_template_with_unicode(template_manager):
    """Test template with unicode characters"""
    template_manager.create_template(
        name="unicode",
        content="こんにちは {{name}}、ようこそ！",
        platform="x",
        variables=["name"],
    )

    content = template_manager.use_template("unicode", {"name": "John"})

    assert "こんにちは" in content
    assert "ようこそ" in content
