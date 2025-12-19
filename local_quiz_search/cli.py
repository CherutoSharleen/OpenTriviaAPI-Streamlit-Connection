from __future__ import annotations

import json
from pathlib import Path

from bm25 import search_faq


def main() -> None:
    base = Path(__file__).resolve().parent
    faq = json.loads((base / "faq.json").read_text(encoding="utf-8"))
    print("Local Quiz FAQ Search (BM25)")
    query = input("Ask a quiz-learning question: ").strip()
    results = search_faq(faq, query, top_k=3)
    for rank, (item, score) in enumerate(results, start=1):
        print(f"{rank}. {item['question']} | score={score:.4f}")
        print(f"   Answer: {item['answer']}")


if __name__ == "__main__":
    main()
