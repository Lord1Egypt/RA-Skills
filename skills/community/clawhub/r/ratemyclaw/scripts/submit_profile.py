"""
Submit a generated profile to RateMyClaw API.
Generates a privacy-preserving embedding locally before submission.

Embedding strategy (progressive):
    1. If sentence-transformers is installed → MiniLM (384-dim, best quality)
    2. Else if scikit-learn is installed → TF-IDF (lightweight, decent quality)
    3. Else → tags only (no embedding, still scored on maturity + tag overlap)

Usage:
    RATEMYCLAW_API_KEY=rmc_xxx python3 submit_profile.py [profile.json]
    
    If no API key is provided, the script will ask before generating one.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://ratemyclaw.com"
KEY_FILE = Path(__file__).parent.parent / ".ratemyclaw_key"
TAXONOMY_PATH = Path(__file__).parent.parent / "references" / "taxonomy.json"
MINILM_MODEL = "all-MiniLM-L6-v2"


def get_api_key() -> str:
    """Get API key from env var or saved file. Prompts before generating a new one."""
    # 1. Check env var
    env_key = os.environ.get("RATEMYCLAW_API_KEY", "")
    if env_key.startswith("rmc_"):
        return env_key
    
    # 2. Check saved key file
    if KEY_FILE.exists():
        for line in KEY_FILE.read_text().splitlines():
            if line.startswith("RATEMYCLAW_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key.startswith("rmc_"):
                    return key
    
    # 3. No key found — ask before generating
    print("  ⚠️  No API key found.")
    print(f"     This will POST to {API_BASE}/v1/keys to generate a free key")
    print(f"     and save it to {KEY_FILE}")
    print()
    
    # Support non-interactive mode via --yes flag
    if "--yes" not in sys.argv:
        answer = input("     Generate a key? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("  ❌ Aborted. Set RATEMYCLAW_API_KEY env var or pass --yes to auto-generate.")
            sys.exit(1)
    
    print("  🔑 Generating API key...")
    data = json.dumps({"label": "auto"}).encode()
    req = urllib.request.Request(
        f"{API_BASE}/v1/keys",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        key = result["api_key"]
        
        # Save it
        KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(KEY_FILE, "w") as f:
            f.write(f"RATEMYCLAW_API_KEY={key}\n")
        os.chmod(str(KEY_FILE), 0o600)
        print(f"  ✓ Key saved to {KEY_FILE}")
        return key
    except Exception as e:
        print(f"  ❌ Could not generate key: {e}")
        sys.exit(1)


def _profile_to_text(profile: dict) -> str:
    """Convert profile tags to a text string suitable for embedding."""
    parts = []
    for key in ["domains", "tools", "patterns", "integrations"]:
        vals = profile.get(key, [])
        if vals:
            parts.append(f"{key}: {', '.join(vals)}")
    
    if profile.get("skills_installed"):
        parts.append(f"installed skills: {', '.join(profile['skills_installed'])}")
    
    parts.append(f"automation level: {profile.get('automation_level', 'unknown')}")
    parts.append(f"stage: {profile.get('stage', 'unknown')}")
    
    return ". ".join(parts)


def _detect_embedding_method() -> str:
    """Detect the best available embedding method.
    
    Returns: 'minilm', 'tfidf', or 'none'
    """
    try:
        import sentence_transformers  # noqa: F401
        return "minilm"
    except ImportError:
        pass
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401
        return "tfidf"
    except ImportError:
        pass
    
    return "none"


def _generate_minilm_embedding(text: str) -> list[float]:
    """Generate a 384-dim embedding using sentence-transformers MiniLM."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MINILM_MODEL)
    embedding = model.encode(text).tolist()
    return embedding


def _generate_tfidf_embedding(text: str) -> list[float]:
    """Generate a fixed-dimension TF-IDF embedding using the taxonomy as vocabulary.
    
    Strategy: Build a vocabulary from all taxonomy tags, compute TF-IDF of the
    profile text against that vocabulary. This produces a consistent, fixed-dimension
    vector (one dimension per taxonomy term) that's comparable across agents.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # Load taxonomy to build vocabulary
    with open(TAXONOMY_PATH) as f:
        taxonomy = json.load(f)
    
    # Build vocabulary: all taxonomy tags as terms
    # Replace hyphens with spaces so TF-IDF tokenizer matches them
    vocab_terms = []
    for category in ["domains", "tools", "patterns", "integrations"]:
        for tag in taxonomy.get(category, []):
            vocab_terms.append(tag.replace("-", " "))
    
    # Also include the raw hyphenated forms
    for category in ["domains", "tools", "patterns", "integrations"]:
        for tag in taxonomy.get(category, []):
            if "-" in tag:
                vocab_terms.append(tag)
    
    # Deduplicate while preserving order
    seen = set()
    unique_vocab = []
    for t in vocab_terms:
        if t not in seen:
            seen.add(t)
            unique_vocab.append(t)
    
    # Use unigrams and bigrams to catch multi-word tags
    vectorizer = TfidfVectorizer(
        vocabulary=unique_vocab,
        token_pattern=r"(?u)\b[\w-]+\b",  # allow hyphens in tokens
        lowercase=True,
    )
    
    # Fit and transform just our text
    tfidf_matrix = vectorizer.fit_transform([text.replace("-", " ") + " " + text])
    embedding = tfidf_matrix.toarray()[0].tolist()
    
    return embedding


def generate_embedding(profile: dict) -> tuple[list[float] | None, str]:
    """Generate an embedding locally from the profile's tag data.
    
    Tries MiniLM first, falls back to TF-IDF, then to no embedding.
    
    Returns: (embedding_vector_or_None, method_string)
    """
    method = _detect_embedding_method()
    text = _profile_to_text(profile)
    
    if method == "minilm":
        print("  🧠 Using MiniLM (sentence-transformers) for semantic embedding...")
        embedding = _generate_minilm_embedding(text)
        print(f"  ✓ Generated {len(embedding)}-dim MiniLM embedding locally")
        return embedding, "minilm"
    
    elif method == "tfidf":
        print("  📊 Using TF-IDF for lightweight embedding (scikit-learn)...")
        embedding = _generate_tfidf_embedding(text)
        non_zero = sum(1 for v in embedding if v > 0)
        print(f"  ✓ Generated {len(embedding)}-dim TF-IDF embedding ({non_zero} active features)")
        print()
        print("  💡 For better semantic matching, install sentence-transformers:")
        print("     pip install sentence-transformers")
        print()
        return embedding, "tfidf"
    
    else:
        print("  ⚠️  scikit-learn is required for embeddings but not installed.")
        print()
        
        # Check for requirements.txt relative to this script
        req_file = Path(__file__).parent.parent / "requirements.txt"
        install_cmd = f"pip install -r {req_file}" if req_file.exists() else "pip install scikit-learn"
        
        # Support non-interactive mode via --yes flag
        if "--yes" in sys.argv:
            answer = "y"
        else:
            answer = input("     Install now? (~30MB) [Y/n] ").strip().lower()
        
        if answer in ("", "y", "yes"):
            import subprocess
            print("  📦 Installing dependencies...")
            if req_file.exists():
                cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_file)]
            else:
                cmd = [sys.executable, "-m", "pip", "install", "scikit-learn"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✓ Dependencies installed!")
                print()
                # Retry with TF-IDF now available
                from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401
                print("  📊 Using TF-IDF for lightweight embedding...")
                embedding = _generate_tfidf_embedding(text)
                non_zero = sum(1 for v in embedding if v > 0)
                print(f"  ✓ Generated {len(embedding)}-dim TF-IDF embedding ({non_zero} active features)")
                print()
                print("  💡 For better semantic matching, install sentence-transformers:")
                print("     pip install sentence-transformers")
                print()
                return embedding, "tfidf"
            else:
                print(f"  ❌ Install failed: {result.stderr.strip()}")
                print(f"     Try manually: {install_cmd}")
                sys.exit(1)
        else:
            print(f"  ❌ scikit-learn is required. Install with:")
            print(f"     {install_cmd}")
            sys.exit(1)


def submit(profile_path: str):
    api_key = get_api_key()
    
    with open(profile_path) as f:
        profile = json.load(f)
    
    print("🔐 Generating embedding locally...")
    embedding, embedding_method = generate_embedding(profile)
    
    # Build the submission payload
    payload = {
        "profile": {
            "domains": profile.get("domains", []),
            "tools": profile.get("tools", []),
            "patterns": profile.get("patterns", []),
            "integrations": profile.get("integrations", []),
            "skills_installed": profile.get("skills_installed", []),
            "automation_level": profile.get("automation_level", "manual"),
            "stage": profile.get("stage", "building"),
        },
        "embedding": embedding,  # None if no method available
        "embedding_method": embedding_method,  # "minilm", "tfidf", or "none"
        "maturity": profile.get("maturity", {}),
        "models": profile.get("models", {}),
    }
    
    print("📤 Submitting to ratemyclaw.com (tags + embedding only)...")
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{API_BASE}/v1/profile",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ API error ({e.code}): {body}")
        sys.exit(1)
    
    score_data = result.get("score", {})
    if isinstance(score_data, dict):
        overall = score_data.get("overall", "?")
    else:
        overall = score_data  # legacy: flat integer
    
    # Compute grade from score
    if isinstance(overall, (int, float)):
        if overall >= 90: grade = "S"
        elif overall >= 75: grade = "A"
        elif overall >= 60: grade = "B"
        elif overall >= 40: grade = "C"
        else: grade = "D"
    else:
        grade = "?"
    
    # Build full score URL
    profile_id = result.get("profile_id", "")
    score_url = result.get("score_url", "")
    if score_url and not score_url.startswith("http"):
        score_url = f"{API_BASE}{score_url}"
    
    print()
    print(f"  🦞 RateMyClaw Score: {overall}/100  (Grade: {grade})")
    print(f"  {'━' * 40}")
    if embedding_method != "minilm":
        print(f"  📊 Embedding: {embedding_method} (upgrade to MiniLM for better matching)")
    else:
        print(f"  📊 Embedding: MiniLM (best quality)")
    print()
    print(f"  🔗 View full breakdown: {score_url}")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        path = sys.argv[1]
    else:
        path = str(Path(__file__).parent.parent / "generated_profile.json")
    
    if not os.path.exists(path):
        print(f"❌ Profile not found: {path}")
        print("   Run profile_generator.py first")
        sys.exit(1)
    
    submit(path)
