import unittest
from gen import get_points_tally


class MyTestCase(unittest.TestCase):
    def test_get_weekly_standings(self):
        self.assertEqual(True, False)

    def test_get_points_tally(self):
        self.assertEqual(get_points_tally('liv',2021), 23)



if __name__ == '__main__':
    unittest.main()
