# scgraph-eval

Stand-alone scGraph package for evaluations. Adapted from https://github.com/Genentech/Islander . 
Originally written by Hanchen Wang (wang.hanchen@gene.com), Leskovec, Jure and Regev, Aviv.

A tool for evaluating single-cell embeddings using graph-based relationships. This package helps analyze the consistency of cell type relationships across different batches in single-cell data.

I modified the API for convenience of my use (1. pass AnnData directly, 2. specify obsm keys) following the MIT license.

## Installation

```bash
# conda create -n scgraph python=3.10 # to create another conda environment if necessary
pip install scgraph-bench
```

## Usage

### Python API

```python
from scgraph import scGraph

# Using a file path
scgraph = scGraph(
    adata_path="path/to/your/data.h5ad",   # Path to AnnData object
    batch_key="batch",                     # Column name for batch information
    label_key="cell_type",                 # Column name for cell type labels
    trim_rate=0.05,                        # Trim rate for robust mean calculation
    thres_batch=100,                       # Minimum number of cells per batch
    thres_celltype=10,                     # Minimum number of cells per cell type
)

# Run the analysis, return a pandas dataframe
results = scgraph.main()

# Save the results
results.to_csv("embedding_evaluation_results.csv")
```

You can also pass an AnnData object directly via `adata`, and use `obsm_keys` to select which embeddings to evaluate:

```python
import scanpy as sc
from scgraph import scGraph

adata = sc.read("path/to/your/data.h5ad")

# Evaluate only specific embeddings
scgraph = scGraph(
    adata=adata,                           # Pass AnnData object directly
    batch_key="batch",
    label_key="cell_type",
    obsm_keys=["X_umap", "X_scVI"],       # Only evaluate specific embeddings
)

results = scgraph.main()
```

If `obsm_keys` is not specified, all embeddings in `adata.obsm` will be evaluated.

### Command Line Interface

```bash
# Evaluate all embeddings
scgraph-bench --adata_path path/to/data.h5ad --batch_key batch --label_key cell_type --savename results

# Evaluate specific embeddings only
scgraph-bench --adata_path path/to/data.h5ad --obsm_keys X_umap X_scVI --savename results
```

## Output

The package outputs comparison metrics between different embeddings:
- Rank-PCA: Spearman correlation with PCA-based relationships
- Corr-PCA: Pearson correlation with PCA-based relationships
- Corr-Weighted: Weighted correlation considering distance-based importance (reported as scGraph scores in the paper _Limitations of cell embedding metrics assessed using drifting islands, Nature Biotechnology 2025_.)

## How It Works

1. **Build a PCA-based consensus reference**: For each batch, the top 1000 highly variable genes (HVG) are selected, and PCA (10 components) is computed on these HVGs. Trimmed-mean centroids for each cell type are calculated in this PCA space, and pairwise distances between centroids are recorded. The per-batch distance matrices are then averaged across all batches to form a consensus reference that captures robust cell-type relationships.
2. **Evaluate embeddings against the consensus**: For each embedding in `adata.obsm` (or those specified by `obsm_keys`), the same centroid and pairwise distance procedure is applied. The resulting distance matrix is compared to the PCA consensus via Spearman correlation (Rank-PCA), Pearson correlation (Corr-PCA), and distance-weighted Pearson correlation (Corr-Weighted).

Note: HVG selection and PCA are only used to build the consensus reference. The embeddings being evaluated are used as-is from `adata.obsm`.

## Requirements

- numpy
- pandas
- scanpy
- tqdm
- scipy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

## Citation

If you use this package in your research, please cite:

@article{wang2024metric,
  title={Metric mirages in cell embeddings},
  author={Wang, Hanchen and Leskovec, Jure and Regev, Aviv},
  journal={BioRxiv},
  pages={2024--04},
  year={2024},
  publisher={Cold Spring Harbor Laboratory}
}

## Contact

For questions and feedback:
- Hanchen Wang
- Email: hanchen.wang.sc@gmail.com
