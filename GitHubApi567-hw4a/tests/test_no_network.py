import unittest
from unittest.mock import patch
from src.github_api import list_repos_with_commit_counts

class NoNetwork(unittest.TestCase):
    def test_network_is_mocked(self):
        # If code tries to call requests.get for real, this will raise an error
        with patch("src.github_api.requests.get") as mock_get:
            mock_get.side_effect = RuntimeError("Network access forbidden in unit tests")
            with self.assertRaises(RuntimeError):
                list_repos_with_commit_counts("anyuser")

if __name__ == "__main__":
    unittest.main()
