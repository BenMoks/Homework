import unittest
from unittest.mock import patch, Mock
from src.github_api import list_repos_with_commit_counts, GitHubApiError


def _mk_resp(ok=True, json_data=None, status=200):
    m = Mock()
    m.ok = ok
    m.status_code = status
    m.json.return_value = json_data
    return m


class GitHubApiTests(unittest.TestCase):

    @patch("src.github_api.requests.get")
    def test_happy_path_single_repo_single_page(self, mock_get):
        # Page 1 repos
        mock_get.side_effect = [
            _mk_resp(json_data=[{"name": "Triangle567"}]),  # repos?page=1
            _mk_resp(json_data=[]),                         # repos?page=2 -> stop
            _mk_resp(json_data=[{"sha": "a"}, {"sha": "b"}]),  # commits?page=1
            _mk_resp(json_data=[]),                            # commits?page=2 -> stop
        ]
        out = list_repos_with_commit_counts("John567")
        self.assertEqual(out, [{"repo": "Triangle567", "commits": 2}])

    @patch("src.github_api.requests.get")
    def test_pagination_multiple_pages(self, mock_get):
        # Repos over two pages
        mock_get.side_effect = [
            _mk_resp(json_data=[{"name": "A"}, {"name": "B"}]),  # repos p1
            _mk_resp(json_data=[{"name": "C"}]),                  # repos p2
            _mk_resp(json_data=[]),                               # repos p3 -> stop
            # commits for A
            _mk_resp(json_data=[{"sha": "1"}]), _mk_resp(json_data=[]),
            # commits for B
            _mk_resp(json_data=[{"sha": "2"}, {"sha": "3"}]), _mk_resp(json_data=[]),
            # commits for C
            _mk_resp(json_data=[]),  # no commits
        ]
        out = list_repos_with_commit_counts("someone")
        self.assertEqual(
            sorted(out, key=lambda x: x["repo"]),
            [{"repo": "A", "commits": 1},
             {"repo": "B", "commits": 2},
             {"repo": "C", "commits": 0}]
        )

    @patch("src.github_api.requests.get")
    def test_non_2xx_raises(self, mock_get):
        mock_get.return_value = _mk_resp(ok=False, json_data={"message": "Not Found"}, status=404)
        with self.assertRaises(GitHubApiError):
            list_repos_with_commit_counts("nope")

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            list_repos_with_commit_counts("")

        with self.assertRaises(ValueError):
            list_repos_with_commit_counts(None)  # type: ignore


if __name__ == "__main__":
    unittest.main()
