import sys
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="Compress prompts using LLMLingua-2 to reduce token consumption.")
    parser.add_argument("--input", type=str, required=True, help="Path to input text file.")
    parser.add_argument("--ratio", type=float, default=0.5, help="Target compression ratio (e.g., 0.5 for half size).")
    parser.add_argument("--dry-run", action="store_true", help="Print diff instead of outputting compressed text.")
    parser.add_argument("--output", type=str, help="Path to save compressed text. If omitted, prints to stdout.")
    
    args = parser.parse_args()

    try:
        from llmlingua import PromptCompressor
    except ImportError:
        print("Error: llmlingua is not installed. To use this script, run 'pip install llmlingua'")
        sys.exit(1)

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            prompt = f.read()
    except Exception as e:
        print(f"Error reading {args.input}: {e}")
        sys.exit(1)

    # Initialize compressor using the smaller, faster LLMLingua-2 model
    print("Loading LLMLingua-2 model... (this may take a few seconds on first run)")
    start_load = time.time()
    try:
        # LLMLingua-2 uses an XLM-RoBERTa encoder instead of a full LLM for faster compression
        compressor = PromptCompressor(
            model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
            use_llmlingua2=True,
            device_map="cpu" # Adjust to 'cuda' or 'mps' if available and needed
        )
    except Exception as e:
        print(f"Failed to load compressor: {e}")
        sys.exit(1)
        
    print(f"Model loaded in {time.time() - start_load:.2f}s")

    print(f"Compressing at ratio {args.ratio}...")
    start_compress = time.time()
    
    # We use instructions="" as we are doing task-agnostic compression
    results = compressor.compress_prompt(
        prompt,
        rate=args.ratio,
        force_tokens=['\n', '.', '!', '?', ','], # Keep structural tokens to maintain readability
        drop_consecutive=True
    )
    
    comp_time = time.time() - start_compress
    compressed_prompt = results['compressed_prompt']
    
    print("\n--- Compression Results ---")
    print(f"Original Tokens   : {results['origin_tokens']}")
    print(f"Compressed Tokens : {results['compressed_tokens']}")
    print(f"Actual Ratio      : {results['compressed_tokens'] / results['origin_tokens']:.2f}")
    print(f"Time Taken        : {comp_time:.2f}s")
    
    if args.dry_run:
        print("\n--- Dry Run Preview (First 500 chars) ---")
        print(compressed_prompt[:500] + "...\n")
        print("Run without --dry-run and provide --output to save.")
    else:
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(compressed_prompt)
            print(f"Saved compressed prompt to {args.output}")
        else:
            print("\n--- Compressed Prompt ---")
            print(compressed_prompt)

if __name__ == "__main__":
    main()
