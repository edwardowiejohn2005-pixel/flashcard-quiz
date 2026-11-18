import json
from pathlib import Path
import random

DEFAULT_CARDS = [
    {"question": "Which Python keyword defines a function?", "answer": "def"},
    {"question": "What is the first index of a Python list?", "answer": "0"},
    {"question": "Which type stores True or False?", "answer": "bool"},
    {"question": "Which operator performs integer floor division?", "answer": "//"},
    {"question": "What file extension is commonly used for Python scripts?", "answer": ".py"},
]


def load_cards(path=None):
    if path is None:
        return list(DEFAULT_CARDS)
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data or any(
        not isinstance(c, dict) or not isinstance(c.get("question"), str)
        or not isinstance(c.get("answer"), str) or not c["question"].strip() or not c["answer"].strip()
        for c in data
    ):
        raise ValueError("Cards must be a nonempty list of question/answer objects")
    return data


def check_answer(given, expected):
    return given.strip().casefold() == expected.strip().casefold()


def run_quiz(cards, input_fn=input, output_fn=print, shuffle=True):
    cards = list(cards)
    if shuffle:
        random.shuffle(cards)
    score = 0
    for index, card in enumerate(cards, 1):
        given = input_fn(f"{index}. {card['question']} > ")
        if check_answer(given, card["answer"]):
            score += 1
            output_fn("Correct!")
        else:
            output_fn(f"Incorrect. Answer: {card['answer']}")
    output_fn(f"Final score: {score}/{len(cards)}")
    return score


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Flashcard quiz")
    parser.add_argument("--cards", help="Optional JSON file of question/answer cards")
    args = parser.parse_args()
    try:
        run_quiz(load_cards(args.cards))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
