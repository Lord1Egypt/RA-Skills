"""Offline captcha arithmetic regression tests; OCR and image are synthetic."""
import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import oa_utils


class CaptchaArithmeticTests(unittest.TestCase):
    def answer(self, expression):
        with patch('ddddocr.DdddOcr') as factory:
            factory.return_value.classification.return_value = expression
            with patch('builtins.eval', side_effect=AssertionError('Dynamic evaluation forbidden')):
                with contextlib.redirect_stderr(io.StringIO()):
                    return oa_utils.solve_captcha(b'not-a-real-image')

    def test_plain_arithmetic_works_without_dynamic_evaluation(self):
        for expression, expected in [('4+3-', '7'), ('9-2', '7'), ('1-4', '-3'),
                                     ('7*3', '21'), ('8/2-', '4'), ('8/3', '2'),
                                     ('0+0', '0'), ('76-', '76')]:
            with self.subTest(expression=expression):
                self.assertEqual(self.answer(expression), expected)

    def test_invalid_or_excessive_expressions_fail_closed(self):
        for expression in ['', 'not-a-number', '1/0', '9**9', '1+2+3', '1++2', '1'*40]:
            with self.subTest(expression=expression):
                self.assertIsNone(self.answer(expression))


if __name__ == '__main__':
    unittest.main()
