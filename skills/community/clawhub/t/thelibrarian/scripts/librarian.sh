#!/bin/bash
# The Librarian - Wrapper script that handles BLAS preload automatically
# Usage: librarian build <input_dir> <output_dir> [options]
#        librarian search "query" <index_dir> [options]

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
VENV_DIR="$SKILL_DIR/venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment not found. Run:"
    echo "  cd $SKILL_DIR"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install turbovec numpy requests rank-bm25 flashrank"
    exit 1
fi

# Check if BLAS library exists
BLAS_LIB="/usr/lib/x86_64-linux-gnu/libblas.so.3"
if [ ! -f "$BLAS_LIB" ]; then
    echo "ERROR: BLAS library not found at $BLAS_LIB"
    echo "Install with: sudo apt install libblas3"
    exit 1
fi

# Function to show help
show_help() {
    echo "The Librarian - Lightweight Document Search with TurboVec"
    echo ""
    echo "Usage:"
    echo "  librarian build <input_dir> <output_dir> [options]"
    echo "  librarian search \"query\" <index_dir> [options]"
    echo ""
    echo "Commands:"
    echo "  build    Build a quantized index from documents"
    echo "  search   Search an existing index"
    echo ""
    echo "Build options:"
    echo "  --model MODEL      Embedding model (default: nomic-embed-text:v1.5)"
    echo "  --bits N           Quantization bits: 2, 3, or 4 (default: 4)"
    echo "  --chunk-size N     Chunk size in chars (default: 650)"
    echo ""
    echo "Search options:"
    echo "  --top-k N          Number of results (default: 5)"
    echo "  --expand N         Context chunks on each side (default: 0)"
    echo "  --hybrid           Use hybrid vector + BM25 search"
    echo "  --rerank           Rerank results with Flashrank"
    echo "  --vector-weight N  Weight for vector in hybrid (default: 0.5)"
    echo "  --json             Output as JSON"
    echo ""
    echo "Examples:"
    echo "  librarian build ./documents ./index"
    echo "  librarian build ./docs ./index --bits 3"
    echo "  librarian search \"habit formation\" ./index --hybrid --rerank"
    echo "  librarian search \"psychology\" ./index --top-k 10 --json"
    echo ""
    echo "Environment:"
    echo "  OLLAMA_API    Ollama API URL (default: http://host.docker.internal:11434)"
}

# No command provided
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
    build)
        if [ $# -lt 2 ]; then
            echo "ERROR: build requires input_dir and output_dir"
            echo "Usage: librarian build <input_dir> <output_dir> [options]"
            exit 1
        fi
        INPUT_DIR="$1"
        OUTPUT_DIR="$2"
        shift 2
        
        # Run build with BLAS preload
        LD_PRELOAD="$BLAS_LIB" "$VENV_DIR/bin/python3" "$SCRIPTS_DIR/build_index.py" \
            --input "$INPUT_DIR" \
            --output "$OUTPUT_DIR" \
            "$@"
        ;;
    
    search)
        if [ $# -lt 2 ]; then
            echo "ERROR: search requires query and index_dir"
            echo "Usage: librarian search \"query\" <index_dir> [options]"
            exit 1
        fi
        QUERY="$1"
        INDEX_DIR="$2"
        shift 2
        
        # Run search with BLAS preload
        LD_PRELOAD="$BLAS_LIB" "$VENV_DIR/bin/python3" "$SCRIPTS_DIR/search.py" \
            "$QUERY" \
            --index "$INDEX_DIR" \
            "$@"
        ;;
    
    help|--help|-h)
        show_help
        ;;
    
    *)
        echo "ERROR: Unknown command: $COMMAND"
        echo "Run 'librarian help' for usage information"
        exit 1
        ;;
esac