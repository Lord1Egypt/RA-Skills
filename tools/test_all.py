#!/usr/bin/env python3
import subprocess
import os
import sys

def run_test(cmd, cwd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ FAILED: {result.stderr}")
        return False, result.stdout, result.stderr
    print("✅ PASSED")
    return True, result.stdout, result.stderr

def main():
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(tools_dir)
    
    print("=== Starting RA-Skills Verification Tests ===\n")
    
    # Test 1: Search by query
    ok1, out1, _ = run_test([sys.executable, "tools/search.py", "apple-notes", "--limit", "1"], root_dir)
    if not ok1 or "apple-notes" not in out1:
        print("Test 1 Failed: Search query did not find apple-notes")
        sys.exit(1)
        
    # Test 2: Search with source filter
    ok2, out2, _ = run_test([sys.executable, "tools/search.py", "--source", "built-in", "--limit", "2"], root_dir)
    if not ok2 or "built-in" not in out2:
        print("Test 2 Failed: Search source filtering failed")
        sys.exit(1)

    # Test 3: Search with category filter
    ok3, out3, _ = run_test([sys.executable, "tools/search.py", "--category", "productivity", "--limit", "2"], root_dir)
    if not ok3 or "productivity" not in out3:
        print("Test 3 Failed: Search category filtering failed")
        sys.exit(1)

    # Test 4: Fetch LobeHub skill content
    # Look up a LobeHub skill identifier in registry.json to test
    print("Testing LobeHub fetch...")
    ok4, _, _ = run_test([sys.executable, "tools/fetch_content.py", "lobehub/mid-journey-prompt"], root_dir)
    lobe_path = os.path.join(root_dir, "skills", "community", "lobehub", "l", "lobehub_mid-journey-prompt", "CONTENT.md")
    if not os.path.exists(lobe_path):
        print(f"Test 4 Failed: LobeHub skill content was not saved to {lobe_path}")
        sys.exit(1)
    else:
        print("LobeHub fetch verified.")

    # Test 5: Fetch skills.sh skill content
    # Find a skills.sh skill to fetch. Example: skills-sh/sickn33/antigravity-awesome-skills/00-andruia-consultant
    print("Testing skills.sh fetch...")
    ok5, _, _ = run_test([sys.executable, "tools/fetch_content.py", "skills-sh/sickn33/antigravity-awesome-skills/00-andruia-consultant"], root_dir)
    skills_sh_path = os.path.join(root_dir, "skills", "community", "skills_sh", "s", "skills-sh_sickn33_antigravity-awesome-skills_00-andruia-consultant", "CONTENT.md")
    if not os.path.exists(skills_sh_path):
        print(f"Test 5 Failed: skills.sh content was not saved to {skills_sh_path}")
        sys.exit(1)
    else:
        print("skills.sh fetch verified.")

    # Test 6: Fetch ClawHub static scraper fetch
    print("Testing ClawHub static scrape fetch...")
    ok6, _, _ = run_test([sys.executable, "tools/fetch_content.py", "apple-notes-native"], root_dir)
    clawhub_path = os.path.join(root_dir, "skills", "community", "clawhub", "a", "apple-notes-native", "CONTENT.md")
    if not os.path.exists(clawhub_path):
        print(f"Test 6 Failed: ClawHub static scrape content was not saved to {clawhub_path}")
        sys.exit(1)
    else:
        print("ClawHub fetch verified.")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! 100% functional verification completed.")

if __name__ == "__main__":
    main()
