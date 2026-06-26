# Clean Research Document

## Abstract

This synthesis examines current research on distributed systems resilience.
We find that consensus protocols with Byzantine fault tolerance provide
stronger guarantees than crash-fault-tolerant alternatives.

## 1. Introduction

Distributed systems require coordination mechanisms to maintain consistency.
This document surveys approaches published between 2015 and 2024.

## 2. Methodology

We reviewed 45 peer-reviewed papers from IEEE, ACM, and USENIX proceedings.
Selection criteria included systems with formal correctness proofs.

## 3. Findings

Byzantine fault tolerance (BFT) protocols incur 2-3x overhead compared
to crash-fault-tolerant (CFT) protocols but provide stronger safety guarantees.

## 4. Conclusion

For mission-critical systems, BFT protocols are recommended despite overhead.
