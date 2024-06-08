import unittest
import itertools
from HMSeparateChaining import HMSeparateChainingSet, cons, length,\
    remove, member, to_list, from_list, concat, intersection,\
    empty, reduce, tmap, filter


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
        empty_set = empty()
        self.assertEqual(str(empty_set), "{}")
        self.assertIsNone(empty_set.head)

    def test_filter(self):
        l1 = from_list([None, 1])
        if l1 and hasattr(l1, 'head'):
            filtered = filter(l1.head, lambda x: x is not None)
        else:
            filtered = None
        self.assertEqual(to_list(filtered), [1])

    def test_map(self):
        l1 = from_list([1, 2])
        mapped = tmap(l1, lambda k: (k, k + 1))
        self.assertEqual(to_list(mapped), [(1, 2), (2, 3)])

    def test_reduce(self):
        l1 = from_list([1, 2])
        result = reduce(l1, lambda acc, v: acc + v, 0)
        self.assertEqual(result, 3)


if __name__ == "__main__":
    unittest.main()
