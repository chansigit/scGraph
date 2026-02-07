# scGraph: A tool for evaluating single-cell embeddings using graph-based relationships
# Originally written by Hanchen Wang (wang.hanchen@gene.com), Leskovec, Jure and Regev, Aviv.

__version__ = "0.1.3"

# Import main classes/functions to make them available at package level
from .scgraph import scGraph

# You can add other imports here as needed
# from .other_module import OtherClass

# Define what should be imported with "from scgraph import *"
__all__ = ["scGraph"]