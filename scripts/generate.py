name: Generate and Publish M3U Files

on:
  schedule:
    - cron: '0 */6 * * *' # Runs every 6 hours
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install aiohttp

    - name: Run generate.py
      run: python scripts/generate.py

    - name: Remove untracked files
      run: git clean -f

    - name: Commit and push changes to main-m3u
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git fetch origin main-m3u || git branch main-m3u
        git checkout main-m3u
        git add .
        git commit -m 'Automated update of M3U files' || echo "No changes to commit"
        git push origin main-m3u --force

    - name: Deploy to gh-pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./ # Publish the entire repository
        publish_branch: gh-pages
        force_orphan: true
