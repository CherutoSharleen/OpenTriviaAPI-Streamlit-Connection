# Local Quiz FAQ Search (BM25)

This mini application teaches retrieval fundamentals by searching a fictional quiz-learning FAQ corpus with BM25 ranking.

## What it does

- Loads local FAQ data from JSON.
- Scores each FAQ item with BM25 against the query.
- Returns top matches with answers.

## Concepts taught

- Tokenization and document frequency
- BM25 relevance scoring
- Ranked retrieval over local text

## Install

No external packages are required.

```bash
python --version
```

## Run

```bash
cd local_quiz_search
python cli.py
```

## Test

```bash
cd local_quiz_search
python -m unittest discover -s tests -p "test_*.py"
```

## Representative input/output

Input:

```text
remember capitals
```

Output shape:

```text
1. How can I remember world capitals for quiz games? | score=...
   Answer: ...
```

## Main components

- `bm25.py`: BM25 index and scoring logic
- `cli.py`: command-line search app
- `faq.json`: synthetic FAQ dataset
- `tests/test_bm25.py`: correctness checks

## Data note

All FAQ entries are fictional/synthetic.

## Limitations and optional exercises

- Small corpus means limited lexical coverage.
- Add typo tolerance, synonym expansion, or snippet extraction.

## Disclosure

This is a retrospective educational addition created now. Historical author/committer dates may be used for commit metadata and do not indicate the actual execution date of this work.
