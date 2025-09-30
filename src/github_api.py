from __future__ import annotations
import requests
from typing import List, Dict


class GitHubApiError(RuntimeError):
    """Raised for non-2xx GitHub API responses."""


def _get_json(url: str) -> list:
    """Fetch a single page and return JSON (list). Raise on non-2xx."""
    resp = requests.get(url, headers={"Accept": "application/vnd.github+json"}, timeout=15)
    if not resp.ok:
        raise GitHubApiError(f"GET {url} -> {resp.status_code}")
    data = resp.json()
    # Both /repos and /commits endpoints return lists for these use cases
    if not isinstance(data, list):
        # When GitHub returns an error, it’s often a dict with a 'message'
        # but we treat that as an error above already.
        return []
    return data


def _get_all_pages(url: str) -> list:
    """Follow pagination via `?page=` & `per_page=100` until empty page."""
    results = []
    page = 1
    while True:
        page_url = f"{url}?per_page=100&page={page}"
        chunk = _get_json(page_url)
        if not chunk:
            break
        results.extend(chunk)
        page += 1
    return results


def list_repos_with_commit_counts(user: str) -> List[Dict[str, int]]:
    """
    Return [{'repo': <name>, 'commits': <count>}, ...] for a GitHub user.
    Designed so HTTP can be mocked in tests.
    """
    if not user or not isinstance(user, str):
        raise ValueError("user must be a non-empty string")

    # 1) list repos
    repos_url = f"https://api.github.com/users/{user}/repos"
    repos = _get_all_pages(repos_url)

    results: List[Dict[str, int]] = []
    for r in repos:
        name = r.get("name")
        if not name:
            # skip odd entries if any
            continue
        commits_url = f"https://api.github.com/repos/{user}/{name}/commits"
        commit_list = _get_all_pages(commits_url)
        results.append({"repo": name, "commits": len(commit_list)})
    return results


if __name__ == "__main__":
    # small CLI for manual checks (avoids unit-test rate limits)
    import sys, json
    if len(sys.argv) != 2:
        print("Usage: python -m src.github_api <github-username>")
        sys.exit(2)
    user = sys.argv[1]
    try:
        print(json.dumps(list_repos_with_commit_counts(user), indent=2))
    except GitHubApiError as e:
        print(f"GitHub API error: {e}")
        sys.exit(1)
