import unittest
from text_tools import format_text, summarize_text

class TextToolsTests(unittest.TestCase):
    def test_formatting(self):
        self.assertEqual(format_text('Hola  ,mundo!  Buen día.'), 'Hola, mundo! Buen día.')

    def test_short_text_not_summarized(self):
        self.assertIsNone(summarize_text('Una sola oración.'))

    def test_summary_is_extractive(self):
        text = ('La lectura ayuda a aprender. '
                'Leer textos permite conocer ideas nuevas. '
                'La práctica diaria fortalece el aprendizaje. '
                'El descanso también es importante.')
        summary = summarize_text(text)
        self.assertIsNotNone(summary)
        self.assertTrue(len(summary) < len(text))
        self.assertTrue(any(sentence in text for sentence in summary.split('. ') if sentence))

if __name__ == '__main__':
    unittest.main()
