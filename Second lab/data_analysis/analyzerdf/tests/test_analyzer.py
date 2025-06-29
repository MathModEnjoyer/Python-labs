'''
Модуль тестирования работы класса анализатора временного ряда.
'''
import unittest
import pandas as pd
import numpy as np
from analyzerdf.analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer(pd.DataFrame([-1.4, 0.7, -1.8, 0, 2.5]))
        self.analyzer_with_df_size_one = Analyzer(pd.DataFrame([-1.4]))
        
    def test_get_rolling_meaning(self):
        df2 = pd.DataFrame([np.nan, np.nan, -0.833333, -0.366667, 0.233333])
        pd.testing.assert_frame_equal(self.analyzer.get_rolling_meaning(3),
                                        df2)
        
    def test_get_rolling_meaning_with_window_size_one(self):
        df2 = pd.DataFrame([-1.4, 0.7, -1.8, 0, 2.5])
        pd.testing.assert_frame_equal(self.analyzer.get_rolling_meaning(1),
                                        df2)
        
    def test_get_rolling_meaning_with_float_window_size(self):
        with self.assertRaises(ValueError):
            self.analyzer.get_rolling_meaning(2.6)
                                        
    def test_get_rolling_meaning_with_window_size_zero(self):
        with self.assertRaises(ValueError):
            self.analyzer.get_rolling_meaning(0)

    def test_get_rolling_meaning_with_negative_window_size(self):
        with self.assertRaises(ValueError):
            self.analyzer.get_rolling_meaning(-1)

    def test_get_differential(self):
        df2 = pd.DataFrame([np.nan, 2.1, -2.5, 1.8, 2.5])
        pd.testing.assert_frame_equal(self.analyzer.get_differential(),
                                        df2)

    def test_get_differential_with_df_size_one(self):
        df2 = pd.DataFrame([np.nan])
        pd.testing.assert_frame_equal(self.analyzer_with_df_size_one
                                      .get_differential(),
                                      df2)
        
    def test_get_autocorrelation(self):
        df2 = pd.DataFrame([1.000000, -0.187605, -0.165829,
                             0.146566, -0.293132])
        pd.testing.assert_frame_equal(self.analyzer.get_autocorrelation(),
                                        df2)

    def test_get_extremums(self):
        df2 = pd.DataFrame([0.7, 0], index = [1, 3])
        pd.testing.assert_frame_equal(self.analyzer.get_extremums(), df2)

if __name__ == "__main__":
    unittest.main()