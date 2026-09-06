import json
from client import HierarchicalMarkdownChunkerHeadingAnchor

def main():
    chunker = HierarchicalMarkdownChunkerHeadingAnchor()
    doc = """# Cloud Architecture Overview
This document outlines our multi-region cloud deployment.

## Storage Services
We utilize distributed object storage for media and artifacts.

### Hot Storage Tier
Hot storage maintains sub-10ms TTFB across all edge nodes.

### Cold Archive Tier
Cold archive reduces cost by 78% for logs older than 90 days.
"""
    result = chunker.chunk_document(doc)
    print("Hierarchical Chunks:")
    print(json.dumps(result, indent=2))
    assert result["total_chunks"] >= 4
    # Index 0: Root document under H1
    # Index 1: Storage Services under H2
    # Index 2: Hot Storage Tier under H3
    assert result["chunks"][1]["context_header"] == "Cloud Architecture Overview > Storage Services"
    assert result["chunks"][2]["context_header"] == "Cloud Architecture Overview > Storage Services > Hot Storage Tier"
    print("Hierarchical chunker verification complete: PASS")

if __name__ == "__main__":
    main()
