import unittest,copy,json
from thermal_dose_ledger import run
DEMO={'reference_kelvin': 500, 'activation_over_R_kelvin': 5000, 'maximum_gap_s': 20, 'samples': [{'time_s': 0, 'kelvin': 500}, {'time_s': 10, 'kelvin': 500}]}
class DomainTests(unittest.TestCase):
 def test_reference_temperature(self):
  x=run(DEMO);self.assertEqual(x['known_equivalent_seconds'],10);self.assertTrue(x['complete'])
 def test_gap_is_not_cold_or_interpolated(self):
  x=run(dict(DEMO,maximum_gap_s=5));self.assertEqual(x['known_equivalent_seconds'],0);self.assertFalse(x['complete']);self.assertIsNone(x['intervals'][0]['equivalent_seconds'])
 def test_temperature_monotonic(self):
  x=copy.deepcopy(DEMO)
  for s in x['samples']:s['kelvin']=600
  self.assertGreater(run(x)['known_equivalent_seconds'],10)
