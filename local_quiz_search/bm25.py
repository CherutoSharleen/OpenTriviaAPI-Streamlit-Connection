from __future__ import annotations

import math
import re
from collections import Counter


TOKEN_PATTERN = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def build_index(documents: list[dict[str, str]]) -> tuple[list[list[str]], dict[str, int], float]:
    tokenized_docs = [tokenize(f"{doc['question']} {doc['answer']}") for doc in documents]
    df: dict[str, int] = {}
    for tokens in tokenized_docs:
        for token in set(tokens):
            df[token] = df.get(token, 0) + 1
    avg_doc_len = sum(len(tokens) for tokens in tokenized_docs) / max(1, len(tokenized_docs))
    return tokenized_docs, df, avg_doc_len


def bm25_score(
    query_tokens: list[str],
    doc_tokens: list[str],
    df: dict[str, int],
    total_docs: int,
    avg_doc_len: float,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    doc_counts = Counter(doc_tokens)
    score = 0.0
    for token in query_tokens:
        freq = doc_counts.get(token, 0)
        if freq == 0:
            continue
        doc_freq = df.get(token, 0)
        idf = math.log(1 + (total_docs - doc_freq + 0.5) / (doc_freq + 0.5))
        denom = freq + k1 * (1 - b + b * (len(doc_tokens) / max(1e-9, avg_doc_len)))
        score += idf * ((freq * (k1 + 1)) / denom)
    return score


def search_faq(documents: list[dict[str, str]], query: str, top_k: int = 3) -> list[tuple[dict[str, str], float]]:
    tokenized_docs, df, avg_len = build_index(documents)
    query_tokens = tokenize(query)
    scored: list[tuple[dict[str, str], float]] = []
    for doc, tokens in zip(documents, tokenized_docs):
        score = bm25_score(query_tokens, tokens, df, len(documents), avg_len)
        scored.append((doc, score))
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]


def highlight_overlap(item: dict[str, str], query: str) -> list[str]:
    query_tokens = set(tokenize(query))
    content_tokens = set(tokenize(f"{item['question']} {item['answer']}"))
    return sorted(query_tokens & content_tokens)


def normalized_query_terms(query: str) -> list[str]:
    return sorted(set(tokenize(query)))


def top_questions_only(documents: list[dict[str, str]], query: str, top_k: int = 3) -> list[str]:
    return [item["question"] for item, _ in search_faq(documents, query, top_k=top_k)]


def answer_preview(answer: str, max_words: int = 8) -> str:
    words = answer.split()
    if len(words) <= max_words:
        return answer
    return " ".join(words[:max_words]) + "..."
