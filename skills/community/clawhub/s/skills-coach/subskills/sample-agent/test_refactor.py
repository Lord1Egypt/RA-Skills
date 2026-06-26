#!/usr/bin/env python3
"""Test script to verify the refactored smart_task_generator."""

from smart_task_generator import SmartTaskGenerator
from pathlib import Path

def test_file_type_inference():
    """Test that file types are correctly inferred from SKILL.md."""

    # Test with skills-coach itself
    print("=" * 60)
    print("Testing with skills-coach (should NOT default to PDF)")
    print("=" * 60)

    generator = SmartTaskGenerator(
        '/Users/ranwalker/.openclaw/skills/skills-coach',
        '.'
    )

    if generator.load_and_parse_skill():
        print(f"\nSkill Name: {generator.skill_name}")
        print(f"Skill Description: {generator.skill_description}")
        print(f"Inferred File Types: {generator.inferred_file_types}")
        print(f"Input Patterns: {generator.inferred_input_patterns}")
        print(f"Output Patterns: {generator.inferred_output_patterns}")

        # Test command generation
        if generator.commands:
            print(f"\nFound {len(generator.commands)} commands")
            for i, cmd_info in enumerate(generator.commands[:3], 1):
                print(f"\n--- Command {i} ---")
                print(f"Original: {cmd_info['command']}")

                # Test realistic command generation
                if not cmd_info.get('has_required_params', True):
                    realistic = generator._generate_realistic_command(cmd_info['command'])
                    print(f"Generated: {realistic}")

                    # Verify it doesn't default to PDF unless skill is PDF-related
                    if 'pdf' not in generator.skill_description.lower() and 'pdf' not in generator.skill_name.lower():
                        if '.pdf' in realistic:
                            print("⚠ WARNING: Generated PDF file for non-PDF skill!")
                        else:
                            print("✓ Correctly avoided PDF default")

    print("\n" + "=" * 60)
    print("Test completed")
    print("=" * 60)

if __name__ == "__main__":
    test_file_type_inference()
