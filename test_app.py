import json
import tempfile
from pathlib import Path
import unittest
from app import check_answer, load_cards, run_quiz


class QuizTests(unittest.TestCase):
    def test_answer_normalized(self):
        self.assertTrue(check_answer("  DEF ", "def"))

    def test_wrong_answer(self):
        self.assertFalse(check_answer("list", "tuple"))

    def test_quiz_score(self):
        cards = [{"question": "q1", "answer": "yes"}, {"question": "q2", "answer": "no"}]
        answers = iter(["yes", "bad"])
        messages = []
        self.assertEqual(run_quiz(cards, lambda _: next(answers), messages.append, shuffle=False), 1)
        self.assertIn("Final score: 1/2", messages)

    def test_custom_cards(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "cards.json"
            path.write_text(json.dumps([{"question": "Hello?", "answer": "World"}]), encoding="utf-8")
            self.assertEqual(load_cards(path)[0]["answer"], "World")

    def test_invalid_cards(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_cards(path)


if __name__ == "__main__":
    unittest.main()
