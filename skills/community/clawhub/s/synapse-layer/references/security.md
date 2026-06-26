# Synapse Layer Security Details

## 4-Layer Cognitive Security Pipeline

### Layer 1: Semantic Privacy Guard™

Detects and redacts sensitive information:

- **PII:** Email, phone, SSN, CPF, tax IDs
- **Credentials:** API keys, passwords, tokens
- **Financial:** Credit cards, bank accounts
- **Location:** Addresses, GPS coordinates
- **Medical:** Patient IDs, records

### Layer 2: Intelligent Intent Validation™

Categorizes memory intent:
- Information storage
- Decision recording
- Task tracking
- Alert/notification

Includes self-healing on recall.

### Layer 3: AES-256-GCM Encryption

- Algorithm: AES-256-GCM
- Key derivation: PBKDF2 (600,000 iterations)
- Auth tag: 128-bit
- Nonce: 96-bit, unique per operation

### Layer 4: Differential Privacy

Adds Gaussian noise to embeddings:
- Protects against reconstruction attacks
- Calibrated epsilon values
- Balances privacy and utility

## Trust Quotient™

Composite score (0-1) based on:

| Factor | Weight |
|--------|--------|
| Storage Confidence | 30% |
| Privacy Validation | 25% |
| Intent Validation | 20% |
| Embedding Quality | 15% |
| Source Verification | 10% |

### TQ Ranges

- **0.90-1.00**: Highly Trusted
- **0.70-0.89**: Trusted
- **0.50-0.69**: Moderately Trusted
- **0.00-0.49**: Low Trust

## Zero-Knowledge Architecture

Service provider cannot read plaintext:
- Client-side encryption before transmission
- Encrypted storage only
- Operations on encrypted data
- Client-side decryption after retrieval

## Compliance

Supports:
- **GDPR**: PII redaction, right to deletion
- **HIPAA**: Protected health information
- **SOC 2**: Security controls (planned)
- **PCI DSS**: Payment card redaction
