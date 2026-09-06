import re
from typing import Dict, Any, List, Optional

class HierarchicalMarkdownChunkerHeadingAnchor:
    """
    Splits long Markdown documentation into RAG-optimal passages while preserving
    ancestor heading hierarchy breadcrumbs (H1 > H2 > H3) and metadata anchors.
    """
    def __init__(self, max_chunk_tokens: int = 400):
        self.max_chunk_tokens = max_chunk_tokens

    def chunk_document(self, markdown_text: str) -> Dict[str, Any]:
        lines = markdown_text.splitlines()
        chunks: List[Dict[str, Any]] = []
        
        current_h1: Optional[str] = None
        current_h2: Optional[str] = None
        current_h3: Optional[str] = None
        current_paragraphs: List[str] = []

        def flush_current_chunk():
            if not current_paragraphs:
                return
            body = "\n\n".join(current_paragraphs).strip()
            if not body:
                return
            breadcrumbs = [h for h in [current_h1, current_h2, current_h3] if h]
            breadcrumb_str = " > ".join(breadcrumbs) if breadcrumbs else "Root Document"
            approx_tokens = len(body.split()) * 1.3
            chunks.append({
                "chunk_id": f"chunk_{len(chunks) + 1:03d}",
                "heading_breadcrumbs": breadcrumbs,
                "context_header": breadcrumb_str,
                "content": f"# Context: {breadcrumb_str}\n\n{body}",
                "raw_text": body,
                "estimated_tokens": int(approx_tokens)
            })
            current_paragraphs.clear()

        for line in lines:
            h1_match = re.match(r"^#\s+(.*)$", line)
            h2_match = re.match(r"^##\s+(.*)$", line)
            h3_match = re.match(r"^###\s+(.*)$", line)

            if h1_match:
                flush_current_chunk()
                current_h1 = h1_match.group(1).strip()
                current_h2 = None
                current_h3 = None
            elif h2_match:
                flush_current_chunk()
                current_h2 = h2_match.group(1).strip()
                current_h3 = None
            elif h3_match:
                flush_current_chunk()
                current_h3 = h3_match.group(1).strip()
            else:
                if line.strip():
                    current_paragraphs.append(line.strip())

        flush_current_chunk()

        return {
            "total_chunks": len(chunks),
            "chunks": chunks
        }
