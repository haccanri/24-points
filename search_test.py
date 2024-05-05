import unittest
import operator

from search import get_valid_ops

class TestGetValidOps(unittest.TestCase):

    def test_get_valid_ops(self):
        self.assertEqual(get_valid_ops(2, 3), [[3, 2, operator.add], [3, 2, operator.sub], [3, 2, operator.mul]])
        self.assertEqual(get_valid_ops(5, 6), [[6, 5, operator.add], [6, 5, operator.sub], [6, 5, operator.mul]])
        self.assertEqual(get_valid_ops(3, 6), [[6, 3, operator.add], [6, 3, operator.sub], [6, 3, operator.mul], [6, 3, operator.truediv]])


if __name__ == '__main__':
    unittest.main()