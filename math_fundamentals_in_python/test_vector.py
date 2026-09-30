import unittest

from vector import Vector


class CosineSimilarityTests(unittest.TestCase):
    def test_known_similarity(self):
        self.assertAlmostEqual(
            Vector([1, 2, 3]).cosine_similarity(Vector([4, 5, 6])),
            0.9746318461970762,
        )

    def test_parallel_orthogonal_and_opposite_vectors(self):
        for components, expected in [([6, 0], 1), ([0, 5], 0), ([-6, 0], -1)]:
            with self.subTest(components=components):
                self.assertAlmostEqual(
                    Vector([2, 0]).cosine_similarity(Vector(components)), expected
                )

    def test_zero_vectors_raise_value_error(self):
        for left, right in [([0, 0], [1, 2]), ([1, 2], [0, 0]), ([0, 0], [0, 0])]:
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(ValueError, "zero vectors"):
                    Vector(left).cosine_similarity(Vector(right))


if __name__ == "__main__":
    unittest.main()
