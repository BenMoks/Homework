# Reflection – HW4a GitHub API Assignment

## Design Perspective
When I designed this program, I tried to keep the code simple and easy to test. The main function just lists repos for a user and counts the commits in each repo. I added helper functions for making requests and handling pagination so the logic would be clear and testable.

## Tester Perspective
As a tester, I wanted to make sure the function could handle normal cases, but also errors and edge cases. I added checks for empty usernames, invalid inputs, and bad API responses. I also tested pagination since GitHub splits repos and commits across multiple pages. Mocking the requests made it possible to test everything without hitting GitHub’s rate limits.

## Challenges
Some of the challenges I faced were GitHub’s request limits, making sure pagination worked, and setting up CI. I first tried Travis CI but it needed a paid plan, so I switched to GitHub Actions which worked better and was free.

## Final Thoughts
Thinking like a tester helped me write smaller, cleaner functions that were easy to test. It also made debugging easier because the code was separated into simple pieces. Overall, I think the program is reliable and ready for CI.
