"""
Day 2 - Git practice runner

Builds a throwaway repository in a temporary folder and runs the main Day 2
scenarios, printing the Git output at each step so it can be compared with the
manual exercises. Nothing outside the temporary folder is touched.

Run:  python day2_git_practice.py
Requires: Git installed and available on the PATH.
"""

import subprocess
import tempfile
from pathlib import Path


def git(repo, *args, show=True):
    """Run a git command in the repo and return its text output."""
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    out = (result.stdout + result.stderr).strip()
    if show:
        print(f"$ git {' '.join(args)}")
        if out:
            print(out)
        print()
    return out


def write(repo, name, text):
    (Path(repo) / name).write_text(text + "\n", encoding="utf-8")


def new_repo(base):
    repo = Path(base)
    git(repo, "init", "-b", "main", show=False)
    git(repo, "config", "user.name", "Practice", show=False)
    git(repo, "config", "user.email", "practice@example.com", show=False)
    write(repo, "f.txt", "line 1")
    git(repo, "add", ".", show=False)
    git(repo, "commit", "-m", "initial", show=False)
    return repo


def title(text):
    print("=" * 60)
    print(text)
    print("=" * 60)


# 1. Merge conflict ---------------------------------------------------------
def demo_conflict():
    title("1. Merge conflict: same line edited on two branches")
    with tempfile.TemporaryDirectory() as d:
        repo = new_repo(d)
        git(repo, "switch", "-c", "a")
        write(repo, "f.txt", "hello from A")
        git(repo, "commit", "-am", "A")
        git(repo, "switch", "main")
        git(repo, "switch", "-c", "b")
        write(repo, "f.txt", "hello from B")
        git(repo, "commit", "-am", "B")
        git(repo, "merge", "a")                       # CONFLICT expected
        print("--- f.txt now contains the markers:")
        print((Path(repo) / "f.txt").read_text())
        write(repo, "f.txt", "hello from A and B")    # resolve by hand
        git(repo, "add", "f.txt")
        git(repo, "commit", "-m", "Resolve conflict")
        git(repo, "log", "--oneline", "--graph", "--all", "--decorate")


# 2. Wrong branch -----------------------------------------------------------
def demo_wrong_branch():
    title("2. Commit on the wrong branch, then move it")
    with tempfile.TemporaryDirectory() as d:
        repo = new_repo(d)
        write(repo, "f.txt", "work meant for feature")
        git(repo, "commit", "-am", "oops: committed on main")
        git(repo, "branch", "feature")
        git(repo, "reset", "--hard", "HEAD~1")
        git(repo, "log", "--oneline", "--graph", "--all", "--decorate")
        print("The commit is now only on 'feature'.\n")


# 3. Hard reset and reflog --------------------------------------------------
def demo_reflog():
    title("3. reset --hard on purpose, then recover with reflog")
    with tempfile.TemporaryDirectory() as d:
        repo = new_repo(d)
        write(repo, "f.txt", "second")
        git(repo, "commit", "-am", "second")
        write(repo, "f.txt", "third")
        git(repo, "commit", "-am", "third")
        git(repo, "reset", "--hard", "HEAD~2")
        print("Commits 'second' and 'third' appear to be gone:\n")
        git(repo, "log", "--oneline")
        reflog = git(repo, "reflog", show=True)
        # The entry for the 'third' commit is the one just before the reset.
        sha = next(line.split()[0] for line in reflog.splitlines() if "third" in line)
        git(repo, "reset", "--hard", sha)
        print("Recovered:\n")
        git(repo, "log", "--oneline")


# 4. The three reset modes --------------------------------------------------
def demo_reset_modes():
    title("4. reset --soft, --mixed and --hard compared")
    for mode in ("--soft", "--mixed", "--hard"):
        with tempfile.TemporaryDirectory() as d:
            repo = new_repo(d)
            write(repo, "f.txt", "changed")
            git(repo, "commit", "-am", "change", show=False)
            print(f"--- git reset {mode} HEAD~1")
            git(repo, "reset", mode, "HEAD~1", show=False)
            print(git(repo, "status", "--short", show=False) or "(clean)")
            print("f.txt contains:", (Path(repo) / "f.txt").read_text().strip(), "\n")


# 5. Revert -----------------------------------------------------------------
def demo_revert():
    title("5. revert adds a new commit that undoes an old one")
    with tempfile.TemporaryDirectory() as d:
        repo = new_repo(d)
        write(repo, "f.txt", "bad change")
        git(repo, "commit", "-am", "bad change")
        git(repo, "revert", "--no-edit", "HEAD")
        git(repo, "log", "--oneline")


def main():
    if subprocess.run(["git", "--version"], capture_output=True).returncode != 0:
        raise SystemExit("Git was not found. Install Git and try again.")
    demo_conflict()
    demo_wrong_branch()
    demo_reflog()
    demo_reset_modes()
    demo_revert()


if __name__ == "__main__":
    main()
