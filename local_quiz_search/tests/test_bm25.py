import json
from pathlib import Path
import unittest

from bm25 import highlight_overlap, normalized_query_terms, search_faq


class BM25FaqTests(unittest.TestCase):
    def test_capitals_query_returns_capitals_item(self) -> None:
        base = Path(__file__).resolve().parents[1]
        data = json.loads((base / "faq.json").read_text(encoding="utf-8"))
        top = search_faq(data, "remember capitals", top_k=1)[0][0]
        self.assertEqual(top["id"], "q3")

    def test_top_k_respected(self) -> None:
        base = Path(__file__).resolve().parents[1]
        data = json.loads((base / "faq.json").read_text(encoding="utf-8"))
        results = search_faq(data, "trivia mistakes", top_k=2)
        self.assertEqual(len(results), 2)

    def test_highlight_overlap(self) -> None:
        base = Path(__file__).resolve().parents[1]
        data = json.loads((base / "faq.json").read_text(encoding="utf-8"))
        overlaps = highlight_overlap(data[0], "science trivia")
        self.assertIn("science", overlaps)

    def test_normalized_query_terms(self) -> None:
        terms = normalized_query_terms("science science trivia")
        self.assertEqual(terms, ["science", "trivia"])


if __name__ == "__main__":
    unittest.main()
