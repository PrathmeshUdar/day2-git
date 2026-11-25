# Day 2 Study Guide: Git as a Team, and Undoing Mistakes

**Intern Study Guide: 8 Days of Software Engineering Fundamentals**
Tuesday, 24 November 2026

Companion code: [`day2_git_practice.py`](day2_git_practice.py)

---

## 1. Overview

Day 2 moves from using Git alone to using it with a team, and covers how to recover when something goes wrong. The day addresses branching and merging, sharing work through a remote, the pull request and review workflow, and the tools available for undoing mistakes.

By the end of the day the following outcomes should be met:

- Create branches, merge them, and resolve a merge conflict by hand.
- Share work through a remote (`origin`) using push, fetch and pull.
- Select the appropriate undo tool for a given mistake.
- Recover a commit that appears to be lost.
- Open a pull request and review a partner's pull request.
- Explain the four key topics in Section 7 in the learner's own words.

**Suggested schedule (about 6 to 7 hours):** setup (15 min), reading (1.5 to 2 hrs), conflict practice (30 min), wrong-branch exercise (30 min), hard reset and recovery (30 min), pull request and review (1 hr), extras (20 min), preparing the Explain answers (30 min).

---

## 2. Core Concepts

### 2.1 Branches and HEAD

A **branch** is a movable pointer to a commit. Creating one is inexpensive, because Git writes only a small reference rather than a copy of the files. **HEAD** is a pointer to the current position, normally the current branch, which in turn points at a commit. When HEAD points directly at a commit instead of a branch, the repository is in a detached HEAD state, and commits made there can be lost unless a branch is created for them.

```bash
git branch                     # list branches
git switch -c feature          # create and switch to a new branch
git switch main                # switch back
git log --oneline --graph --all
```

### 2.2 Fast-forward merge versus merge commit

| Type | When it occurs | Result |
|---|---|---|
| Fast-forward | The target branch has no new commits of its own. | Git moves the pointer forward. No new commit is created and history remains a straight line. |
| Merge commit | Both branches have new commits. | Git creates a new commit with two parents that joins the histories. |

A merge commit can be forced even when a fast-forward is possible by using `git merge --no-ff feature`. This keeps a visible record that a feature branch existed.

### 2.3 Merge conflicts and conflict markers

A conflict occurs when both branches changed the same lines, or when one branch deleted a file that the other edited, and Git cannot decide which version to keep. Git pauses the merge and writes markers into the file:

```
<<<<<<< HEAD
your version (the branch you are on)
=======
their version (the branch being merged in)
>>>>>>> feature
```

**Resolution procedure:**

1. Run `git status` to list the conflicted files.
2. Open each file and edit it to the intended final content.
3. Delete all three marker lines.
4. Run `git add <file>` to mark the file as resolved.
5. Run `git commit` to complete the merge.

If the merge needs to be abandoned, `git merge --abort` returns the repository to its state before the merge began.

### 2.4 Remotes and origin

A **remote** is another copy of the repository, usually hosted on a service such as GitHub. **origin** is the default name given to the remote that a repository was cloned from or first connected to.

| Command | Purpose |
|---|---|
| `git remote add origin <url>` | Connects the local repository to a remote. |
| `git push -u origin main` | Sends commits and sets the upstream so later pushes need only `git push`. |
| `git fetch` | Downloads new commits and updates remote-tracking branches such as `origin/main`, without changing the current branch or files. |
| `git pull` | Runs fetch, then merges (or rebases) the fetched commits into the current branch. |

### 2.5 .gitignore

A `.gitignore` file lists patterns for files that Git should not track, such as secrets, dependencies and build output.

```
.env
node_modules/
*.log
dist/
```

Note that `.gitignore` affects only untracked files. A file that is already tracked must first be removed from tracking with `git rm --cached <file>` and that change committed.

---

## 3. Pull Requests and Code Review

A **pull request (PR)** is a request on GitHub to merge one branch into another. It combines the code changes, a description and a discussion thread, and is the place where teammates review work before it is merged. **Code review** is the process in which teammates read the changes and comment, suggest improvements or approve. It raises quality, spreads knowledge across the team and catches mistakes early.

### 3.1 Writing a good PR description

- **What** changed, in one or two sentences.
- **Why** it changed, with a link to the related issue or ticket where one exists.
- **How to test** it, with exact steps.
- **Notes for reviewers**, such as risky areas, trade-offs or open questions.
- Small, focused pull requests are reviewed more quickly.

### 3.2 Reviewing a partner's pull request

A complete review for this exercise includes three kinds of comment:

| Comment type | Example |
|---|---|
| Question | "Why was approach X chosen over Y here?" |
| Suggestion | "Could this be extracted into a helper? The same logic appears on lines 40 and 72." |
| Praise | "The test coverage on the edge case is thorough." |

Effective review comments are specific, courteous and directed at the code rather than the author.

---

## 4. Undo Toolkit

The appropriate tool depends on where the mistake is: in the working files, in the staging area, in a local commit, or in a commit that has already been pushed.

| Situation | Tool | Notes |
|---|---|---|
| Discard uncommitted edits in a file | `git restore <file>` | Permanent: the edits are lost. |
| Unstage a file but keep the edits | `git restore --staged <file>` | Safe. |
| Fix the last commit's message or contents | `git commit --amend` | Rewrites that commit; best used before pushing. |
| Shelve unfinished work temporarily | `git stash`, `git stash pop` | Useful before switching branches. |
| Undo a commit that is already shared | `git revert <sha>` | Adds a new commit that undoes the old one; history is preserved. |
| Undo local, unpushed commits | `git reset` | Moves the branch pointer back; rewrites history. |
| Find a "lost" commit | `git reflog` | Shows where HEAD has been. |

### 4.1 The three modes of git reset

Reset moves the current branch pointer to another commit. The mode determines what happens to the other two areas Git tracks: the staging area (index) and the working files. Pro Git section 7.7 describes these as the three trees: HEAD, the index and the working directory.

| Mode | Branch pointer moved | Staging area | Working files |
|---|---|---|---|
| `--soft` | Yes | Kept (changes stay staged) | Kept |
| `--mixed` (default) | Yes | Cleared (changes unstaged) | Kept |
| `--hard` | Yes | Cleared | **Discarded** |

Of the three, `--hard` is the only mode that discards uncommitted work.

### 4.2 Revert versus reset

- `git revert` is safe on shared branches because it adds history rather than removing it.
- `git reset` rewrites history, so it suits local commits that no one else has pulled. Resetting a pushed branch would require a force push, which can disrupt teammates.

### 4.3 Stash and amend quick reference

```bash
git stash                          # shelve tracked changes
git stash list                     # see what is stashed
git stash pop                      # restore the latest stash and remove it
git commit --amend -m "Better message"
git commit --amend --no-edit       # add staged changes to the last commit
```

---

## 5. Practice Exercises

The exercises are carried out in a scratch repository. The companion file `day2_git_practice.py` builds a throwaway repository and runs the main scenarios automatically, so the results can be compared with the manual steps below.

### 5.0 Setup

```bash
mkdir git-day2 && cd git-day2 && git init
echo "line 1" > f.txt && git add . && git commit -m "initial"
```

Create an empty repository on GitHub, then connect and push:

```bash
git remote add origin <url>
git push -u origin main
```

The partner is added as a collaborator for Exercise 5.4.

### 5.1 Create and resolve a merge conflict

```bash
git switch -c a
echo "hello from A" > f.txt && git add f.txt && git commit -m "A"
git switch main
git switch -c b
echo "hello from B" > f.txt && git commit -am "B"
git merge a                  # CONFLICT
# edit f.txt, remove the markers, choose the final text
git add f.txt
git commit
```

**Expected result:** `git log --oneline --graph --all` shows a merge commit with two parents, and `f.txt` contains no markers. Optional extension: repeat the conflict and use `git merge --abort` to start over.

### 5.2 Commit on the wrong branch, then move it

Scenario: the commit was made on `main` instead of `feature`, and has not been pushed.

```bash
git log --oneline --graph --all      # before
git branch feature                   # new branch at the same commit
git reset --hard HEAD~1              # remove the commit from main
git switch feature
git log --oneline --graph --all      # after: commit is on feature only
```

If `feature` already exists, use cherry-pick instead:

```bash
git switch feature
git cherry-pick <sha>
git switch main
git reset --hard HEAD~1
```

### 5.3 Reset --hard on purpose, then recover with reflog

```bash
# make 2 or 3 commits first
git reset --hard HEAD~2              # the commits appear to vanish
git reflog                           # find the entry from before the reset
git reset --hard <sha>               # or: git branch rescue <sha>
```

The exercise can be repeated with `--soft` and `--mixed` on a fresh commit, running `git status` after each to see how the staging area and files differ.

### 5.4 Open a PR and review a partner's PR

1. Create a branch, commit a small change and run `git push -u origin <branch>`.
2. On GitHub, open a pull request with a description covering what, why and how to test.
3. Review the partner's pull request with three comments: one question, one suggestion and one praise.
4. Where no partner is available, swap with a peer or use a second GitHub account.

### 5.5 Extras

- Use `git stash` and `git stash pop` with an uncommitted edit.
- Use `git commit --amend` to correct a commit message.
- Use `git revert <sha>` and inspect the new commit it creates.
- Add `.env` and `node_modules/` to `.gitignore` and confirm that Git ignores them.

---

## 6. Reading and Search List

**Read**

- Pro Git book, chapter 3 (Branching). The section "Basic Branching and Merging" is the main focus.
- Pro Git, section 7.7 "Reset Demystified". The three-trees model explains the reset modes.
- GitHub Docs, "About pull requests".

**Search terms**

- git merge conflict how to resolve
- git fetch vs pull
- git revert vs reset
- git reset soft mixed hard
- git reflog recover lost commit
- how to write a good pull request description
- committed API key to github what to do

---

## 7. Explain: Model Answers

The following reference answers cover the four topics to be explained.

### 7.1 Fetch versus pull

`git fetch` downloads new commits from the remote and updates remote-tracking branches such as `origin/main`, but never changes the current branch or working files. The incoming work can be inspected before any decision is made. `git pull` runs fetch and then merges (or rebases) the fetched commits into the current branch, so it can change files immediately and can cause conflicts.

### 7.2 Revert versus reset

`git revert` creates a new commit that reverses an earlier commit and leaves history intact, which makes it safe on shared branches. `git reset` moves the branch pointer backwards and so rewrites history; it is intended for local, unpushed work. Revert is used when others may already have the commit, and reset when the commit exists only on the local machine.

### 7.3 Recovering after a hard reset

A hard reset moves the branch pointer, but the old commits remain in Git's database; they are simply no longer reachable from a branch. Running `git reflog` lists where HEAD has been. After finding the entry from just before the reset, `git reset --hard <sha>` moves the branch back, or `git branch rescue <sha>` keeps the commit on a new branch. Recovery applies only to **committed** work, because uncommitted changes removed by `--hard` are gone, and reflog entries expire after roughly 90 days by default.

### 7.4 Why a leaked secret is rotated first and removed from history second

Once a secret has been pushed, it must be assumed to be copied. Automated bots scan public repositories within minutes, and forks, clones and caches may already hold it. Deleting it from history does not reverse the leak. Rotating the secret, meaning revoking it and issuing a new one, makes every copy worthless and takes effect immediately. Cleaning history with `git filter-repo` or BFG, force-pushing and asking collaborators to re-clone is slow and cannot reach copies outside the team's control. The order is therefore: rotate first, remove from history second, and add the file to `.gitignore` to prevent a repeat. The provider's logs should also be checked for any misuse.

---

## 8. Learning Outcomes

- A merge conflict has been resolved by hand.
- A commit has been moved from the wrong branch to the right one.
- A commit lost to `git reset --hard` has been recovered with `git reflog`.
- The `--soft`, `--mixed` and `--hard` modes have been compared.
- A pull request has been opened with a clear description.
- A partner's pull request has been reviewed with a question, a suggestion and a praise.
- Stash, amend, revert and `.gitignore` have been tried.
- The four Explain topics can be described without notes.
