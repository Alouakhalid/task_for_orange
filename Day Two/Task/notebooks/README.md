# Day 2 — Retrieval Optimization

## Overview

This notebook measures and improves retrieval quality from the Day 1 vector index using controlled experiments and real metrics.

## What This Notebook Covers

1. **`top_k` Trade-off Analysis** — Same query at k=1, k=3, k=8 to show precision vs coverage
2. **Chunk Size Ablation** — Rebuilds the index at 3 configurations (200/0, 400/50, 600/100) and compares
3. **Evaluation Test Set** — 8 curated questions with verified expected sources
4. **Precision@k Computation** — Page-level Precision@3 across all test questions

## How to Run

```bash
cd "Day One/Task/notebooks"
jupyter notebook Day2_Retrieval_Optimization.ipynb
```

Execute cells sequentially from top to bottom.

## Dependencies

Same as Day 1 — `requirements.txt` in the parent directory.
