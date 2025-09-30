# GitHubApi567-hw4a (Mocked Version)

![CI](https://github.com/BenMoks/Homework/actions/workflows/ci.yml/badge.svg?branch=HW03a_Mocking)

This branch (**HW03a_Mocking**) uses `unittest.mock` to replace all real GitHub API calls.  
The tests run consistently without hitting the live GitHub API or being affected by rate limits.


# GitHubApi567-hw4a

**Goal:** Given a GitHub username, list each repo and its commit count.

## Usage
```bash
pip install -r requirements.txt
python -m src.github_api <github-username>
