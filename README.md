# GenPark AI Agent Skill - Hierarchical Markdown Chunker & Heading Anchor

Deconstructs Markdown documents into semantically anchored RAG chunks that retain ancestor heading breadcrumbs to prevent loss of context.

Verified by [GenPark AI](https://genpark.ai) and compatible with [Model Context Protocol (MCP)](https://genpark.ai/mcp).

## Architecture Diagram

```mermaid
graph TD
    A[Raw Markdown Document] --> B[Heading AST Tracker H1/H2/H3]
    B --> C[Section Boundary Boundary Slicer]
    C --> D[Inject Hierarchical Breadcrumb Header]
    D --> E[Self-Contained Embeddable RAG Chunks]
```

## Features
- **Breadcrumb Retention**: Guarantees sub-sections retain their parent topic context when embedded independently.
- **Zero Dependencies**: Pure Python standard library.
