# TurboVec Quantization Explained

## What is Quantized Vector Search?

Traditional vector search stores each dimension as a 32-bit float. A 768-dimensional embedding (like nomic-embed-text) requires 768 × 4 bytes = 3KB per vector.

TurboVec compresses vectors to 2-4 bits per dimension:

| Bit Width | Bits/Dim | Bytes/Vector | Compression | Accuracy Loss |
|-----------|----------|--------------|--------------|---------------|
| 4-bit | 4 | 384 | 8x | ~2-3% |
| 3-bit | 3 | 288 | 10.7x | ~4-5% |
| 2-bit | 2 | 192 | 16x | ~6-8% |

For a library with 73,290 chunks at 768 dimensions:

| Engine | Index Size | Accuracy | Search Time |
|--------|-----------|----------|-------------|
| FAISS Flat | ~225MB | 100% | ~10ms |
| FAISS IVF | ~230MB | ~95% | ~5ms |
| TurboVec 4-bit | ~28MB | ~97% | ~10-15ms |
| TurboVec 2-bit | ~15MB | ~93% | ~10-15ms |

## How It Works

TurboVec uses product quantization with SIMD-optimized search:

1. **Rotation**: Applies random rotation to vectors (improves quantization quality)
2. **Quantization**: Maps each float to 2-4 bit code using Lloyd-Max centroids
3. **SIMD Search**: Uses CPU vector instructions for fast distance computation

The accuracy loss is surprisingly small because:
- Semantic similarity is robust to small perturbations
- The rotation step preserves approximate distances
- Higher bits (3-4) capture most of the information

## When to Use TurboVec

### Good Use Cases

- **Resource-constrained hardware**: Raspberry Pi, small VMs, laptops
- **Large document libraries**: 100K+ chunks where memory matters
- **Offline deployment**: No cloud, no GPU, minimal dependencies
- **Development/testing**: Quick iteration without infrastructure

### Less Ideal Use Cases

- **Maximum accuracy required**: Legal, medical, financial where recall is critical
- **Millions of vectors**: Consider FAISS IVF-PQ or dedicated vector DB
- **Real-time streaming**: Quantization adds overhead to new vectors
- **Need incremental updates**: TurboVec requires rebuilding for new documents

## Choosing Bit Width

| Bit Width | Use Case |
|-----------|----------|
| 4-bit | Default choice, best balance |
| 3-bit | Tight memory, slight accuracy tradeoff |
| 2-bit | Extreme compression, acceptable for rough search |

Start with 4-bit. Test recall with known queries. If accuracy is sufficient, try 3-bit or 2-bit.

## Technical Details

### Preprocessing

```python
# Vectors are normalized before quantization
vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

# Random rotation improves quantization quality
rotation = np.random.randn(dim, dim)
rotation, _ = np.linalg.qr(rotation)  # Orthogonal
vectors = vectors @ rotation
```

### Quantization

```python
# Lloyd-Max quantization maps floats to integer codes
# Each code represents a centroid in that dimension's distribution
# 4-bit = 16 centroids, 3-bit = 8 centroids, 2-bit = 4 centroids

index = TurboQuantIndex(dim, bit_width)
index.add(vectors)
index.prepare()  # Compute rotation and centroids
```

### Search

```python
# Query is quantized using the same rotation/centroids
query_embedding = get_embedding(query_text)
query_vec = np.array([query_embedding], dtype=np.float32)

# SIMD-optimized distance computation
distances, indices = index.search(query_vec, k=5)
```

## Comparison with Alternatives

| Solution | Memory | Accuracy | Latency | Complexity |
|----------|--------|----------|---------|------------|
| TurboVec | Minimal | Good | Low | Very Low |
| FAISS Flat | High | Perfect | Low | Low |
| FAISS IVF-PQ | Medium | Good | Low | Medium |
| Pinecone/Weaviate | Cloud | Perfect | Network | High |

## Best Practices

1. **Normalize embeddings**: Some models output unnormalized vectors
2. **Use same model for index and query**: Mismatched models break search
3. **Test recall with known queries**: Validate accuracy for your use case
4. **Consider expand=1**: Chunk truncation hurts recall; expand for context
5. **Batch builds**: Adding documents requires rebuild; batch them