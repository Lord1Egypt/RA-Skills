import sys
import argparse
import os

def estimate_tokens(text: str) -> int:
    """Zero-dependency fallback: rough estimate of tokens (4 chars per token on average)."""
    return len(text) // 4

def count_tokens_tiktoken(text: str, model: str) -> int:
    import tiktoken
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base if model not found automatically
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def count_tokens_transformers(text: str, model_id: str) -> int:
    from transformers import AutoTokenizer
    # Suppress heavy warnings from transformers/huggingface
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    return len(tokenizer.encode(text))

def main():
    parser = argparse.ArgumentParser(description="Count tokens in a text file or string seamlessly.")
    parser.add_argument("--input", type=str, help="Path to input text file. If not provided, reads from stdin.")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Model name (e.g., gpt-4o, gemma, claude).")
    parser.add_argument("--diff", type=str, help="Optional second file to compare token counts.")
    parser.add_argument("--estimate", action="store_true", help="Force fast zero-dependency char/4 estimation.")
    args = parser.parse_args()

    # Read input
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading {args.input}: {e}")
            sys.exit(1)
    else:
        text = sys.stdin.read()

    def get_count(t: str, m: str, force_estimate: bool) -> int:
        if force_estimate:
            return estimate_tokens(t)
            
        mdl = m.lower()
        if "gemma" in mdl or "ollama" in mdl:
            try:
                # Use standard 7b tokenizer for Gemma metrics, highly accurate for ollama/gemma inference
                return count_tokens_transformers(t, "google/gemma-7b")
            except ImportError:
                print("[Warning] 'transformers' not installed. Falling back to --estimate for Gemma/Ollama.")
                return estimate_tokens(t)
            except Exception as e:
                print(f"[Warning] Transformers error: {e}. Falling back to --estimate.")
                return estimate_tokens(t)
                
        elif "claude" in mdl:
            try:
                # Claude uses proprietary tokenizer, tiktoken's cl100k_base is a close industry standard proxy
                return count_tokens_tiktoken(t, "cl100k_base")
            except ImportError:
                print("[Warning] 'tiktoken' not installed. Falling back to --estimate for Claude proxy.")
                return estimate_tokens(t)
                
        else:
            try:
                return count_tokens_tiktoken(t, m)
            except ImportError:
                print(f"[Warning] 'tiktoken' not installed. Falling back to --estimate for {m}.")
                return estimate_tokens(t)

    count1 = get_count(text, args.model, args.estimate)
    char_len1 = len(text)
    
    calc_method = "Estimate (char//4)" if args.estimate or count1 == (char_len1 // 4) else "Exact (Tokenizer)"
    
    print(f"--- Token Audit [{args.model}] ---")
    print(f"Method           : {calc_method}")
    print(f"Input Characters : {char_len1}")
    print(f"Input Tokens     : {count1}")
    print(f"Ratio (char/tok) : {char_len1/count1 if count1 > 0 else 0:.2f}")

    if args.diff:
        try:
            with open(args.diff, 'r', encoding='utf-8') as f:
                text2 = f.read()
            count2 = get_count(text2, args.model, args.estimate)
            char_len2 = len(text2)
            
            print(f"\n--- Compression Savings ---")
            print(f"Diff Characters  : {char_len2} ({(char_len2/char_len1)*100 if char_len1 > 0 else 0:.1f}%)")
            print(f"Diff Tokens      : {count2} ({(count2/count1)*100 if count1 > 0 else 0:.1f}%)")
            print(f"Tokens Saved     : {count1 - count2}")
        except Exception as e:
            print(f"Error reading diff file {args.diff}: {e}")

if __name__ == "__main__":
    main()
