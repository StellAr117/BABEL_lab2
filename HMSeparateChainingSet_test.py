import unittest
import itertools
from HMSeparateChainingSet import HMSeparateChainingSet, cons


class TestHMSeparateChainingSet(unittest.TestCase):
    def test_api(self):
        empty = HMSeparateChainingSet()
        self.assertEqual(str(cons(None, empty)), "{None}")
        l1 = cons(None, cons(1, empty))
        l2 = cons(1, cons(None, empty))
        self.assertEqual(str(empty), "{}")
        self.assertTrue(str(l1) == "{None, 1}" or str(l1) == "{1, None}")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(l1, l2)
        self.assertEqual(l1, cons(None, cons(1, l1)))

        self.assertEqual(length(empty), 0)
        self.assertEqual(length(l1), 2)
        self.assertEqual(length(l2), 2)

        self.assertEqual(str(remove(l1, None)), "{1}")
        self.assertEqual(str(remove(l1, 1)), "{None}")

        self.assertFalse(member(None, empty))
        self.assertTrue(member(None, l1))
        self.assertTrue(member(1, l1))
        self.assertFalse(member(2, l1))

        self.assertEqual(intersection(l1, l2), l1)
        self.assertEqual(intersection(l1, l2), l2)
        self.assertEqual(intersection(l1, empty), empty)
        self.assertEqual(intersection(l1, cons(None, empty)),
                         cons(None, empty))
        self.assertTrue(to_list(l1) == [None, 1] or to_list(l1) == [1, None])
        self.assertEqual(l1, from_list([None, 1]))
        self.assertEqual(l1, from_list([1, None, 1]))

        self.assertEqual(concat(l1, l2), from_list([None, 1, 1, None]))

        buf = []
        for e in l1:
            buf.append(e)
        self.assertIn(buf, map(list, itertools.permutations([1, None])))

        lst = to_list(l1) + to_list(l2)
        for e in l1:
            lst.remove(e)
        for e in l2:
            lst.remove(e)
        self.assertEqual(lst, [])

    def test_empty(self):
        empty = HMSeparateChainingSet.empty()
        self.assertEqual(str(empty), "{}")
        self.assertEqual(empty.length(), 0)

    def test_filter(self):
        l1 = HMSeparateChainingSet.from_list([None, 1])
        filtered = l1.filter(lambda x: x is not None)
        self.assertEqual(filtered.to_list(), [1])

    def test_map(self):
        l1 = HMSeparateChainingSet.from_list([1, 2])
        mapped = l1.map(lambda k, v: (k, v + 1))
        self.assertTrue(mapped.to_list() == [(1, 2), (2, 3)])

    def test_reduce(self):
        l1 = HMSeparateChainingSet.from_list([1, 2])
        result = l1.reduce(lambda acc, v: acc + v, 0)
        self.assertEqual(result, 3)


if __name__ == "__main__":
    unittest.main()
