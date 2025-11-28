# AISTAT Anonymity Compliance Guide

## Overview
This guide helps you maintain anonymity requirements for AISTAT submissions by avoiding personal directory information in your notebook.

---

## ✅ What We Fixed

### Original Problem
The notebook contained hardcoded paths like:
```python
ROOT = Path("/home/adetayo/Documents/CSCI Forms/Adetayo Research/Cancer Screening Behavior/new_results/publication")
```

This violates anonymity by exposing:
- Your username (`adetayo`)
- Your full name or research context
- Directory structure with identifiable information

### Solution Implemented
Replaced with relative paths:
```python
# ✅ ANONYMITY-SAFE: Get repo root dynamically
ROOT = Path.cwd()  # Current working directory (where notebook is executed from)

# All subsequent paths use ROOT as base:
data_raw_path = ROOT / "data" / "raw"
data_interim_path = ROOT / "data" / "interim"
RUN_ROOT = ROOT / "new_results"
```

**Benefits:**
- ✅ No personal information in code
- ✅ Works on any machine with same directory structure
- ✅ Reproducible by reviewers
- ✅ Compliant with anonymity policies

---

## 🚀 For AISTAT Submission

### Step 1: Prepare Your Notebook
```bash
# Ensure your working directory has this structure:
project_root/
├── model.ipynb              # Your notebook
├── data/
│   ├── raw/                 # Input data files
│   └── interim/             # Intermediate files
├── new_results/
│   ├── interim/             # Temporary outputs
│   ├── processed/           # Processed data
│   └── results/
│       ├── tables/          # CSV outputs
│       └── figs/            # PNG/figure outputs
```

### Step 2: Before Submission - Audit for Personal Info

**Check for remaining hardcoded paths:**
```bash
# Search for potential privacy violations
grep -n "/home/" model.ipynb
grep -n "adetayo" model.ipynb
grep -n "/Users/" model.ipynb  # macOS users
grep -n "C:\\\Users\\\\" model.ipynb  # Windows users
```

**Common places to check:**
1. Cell comments with full paths
2. Print statements displaying file locations
3. Error messages that show full paths
4. Data loading lines with absolute paths
5. File save operations with absolute paths

### Step 3: Code Review Checklist

- [ ] Replace all `/home/` paths with `ROOT /` relative paths
- [ ] Replace all `/Users/` paths (macOS) with relative paths
- [ ] Replace all `C:\Users\` paths (Windows) with relative paths
- [ ] Check all `print()` statements - remove full paths
- [ ] Check all `.format()` or f-strings with file paths
- [ ] Check comments mentioning personal directories
- [ ] Remove author names from comments/docstrings
- [ ] Remove institution names (if anonymity requires)
- [ ] Remove contact information

### Step 4: Test Reproducibility

```bash
# Create a test directory with same structure
mkdir /tmp/test_submission
cd /tmp/test_submission

# Copy notebook and data structure
cp -r /original/path/data ./
cp /original/path/model.ipynb ./

# Run the notebook
jupyter nbconvert --to notebook --execute model.ipynb
```

---

## 📝 Example: Converting Hardcoded Paths

### ❌ BEFORE (Not Anonymity-Safe)
```python
import pandas as pd

# PROBLEM: Contains personal info
data_path = "/home/adetayo/Documents/research/data/dataset.csv"
df = pd.read_csv(data_path)

print(f"Loaded data from: {data_path}")  # Prints full path!
```

### ✅ AFTER (Anonymity-Safe)
```python
import pandas as pd
from pathlib import Path

# SOLUTION: Use relative paths
ROOT = Path.cwd()
data_path = ROOT / "data" / "dataset.csv"
df = pd.read_csv(data_path)

print(f"✓ Dataset loaded ({len(df)} rows)")  # Generic output
```

---

## 🔍 Finding All Path References

Search for these patterns in your notebook:

| Pattern | Risk | Replace With |
|---------|------|--------------|
| `/home/username/` | HIGH | `Path.cwd() /` or `ROOT /` |
| `/Users/username/` | HIGH | `Path.cwd() /` or `ROOT /` |
| `C:\Users\username\` | HIGH | `Path.cwd() /` or `ROOT /` |
| Full path in print statements | MEDIUM | Use relative/generic output |
| Full path in error messages | MEDIUM | Sanitize before display |
| Home directory `~` | LOW | Use `ROOT /` instead |

---

## 📋 Current Notebook Status

**Anonymity Updates Made:**
- ✅ Cell 1: Converted hardcoded ROOT path to `Path.cwd()`
- ✅ All subsequent path constructions use `ROOT / ...` pattern
- ✅ No changes needed to data loading/saving logic

**Remaining Checks Needed:**
- [ ] Verify all print statements don't show full paths
- [ ] Check for personal names in comments
- [ ] Ensure no contact info visible
- [ ] Test with relocated notebook

---

## 🛡️ Best Practices for Future Work

### Always Use Relative Paths
```python
# Good
data_file = Path("./data/input.csv")
output_file = Path("./results/output.csv")

# Better (with ROOT variable)
data_file = ROOT / "data" / "input.csv"
output_file = RESULTS / "output.csv"
```

### Use Generic Output Messages
```python
# Avoid showing full paths
print(f"Data loaded successfully")  # Instead of: "Data loaded from /home/adetayo/..."

# Use relative references
print(f"Output saved to: results/tables/output.csv")  # Instead of full path
```

### Document Path Structure
```python
# In README or notebook:
"""
Expected directory structure:
    project_root/
    ├── data/raw/          # Input datasets
    ├── data/interim/      # Temporary files
    └── results/           # Output files
"""
```

---

## ❓ FAQ

**Q: Can I use absolute paths if they don't contain my name?**
A: Avoid absolute paths entirely. Use relative paths from `ROOT`. This ensures reproducibility.

**Q: What if reviewers don't have the same directory structure?**
A: Using `Path.cwd()` and relative paths automatically handles this. Reviewers just need the same folder layout.

**Q: Should I remove filenames too?**
A: No, filenames are fine. Only avoid directory paths containing personal information.

**Q: What about outputs that print paths?**
A: Modify print statements to show relative paths only:
```python
# Instead of:
# print(f"Saved to: {output_path.absolute()}")

# Use:
print(f"Saved to: results/tables/output.csv")
```

---

## ✅ Pre-Submission Checklist

Before uploading to AISTAT:

- [ ] All hardcoded paths replaced with relative paths
- [ ] No personal usernames in code
- [ ] No full directory structures visible
- [ ] Print statements sanitized (no full paths)
- [ ] Author/personal info removed from comments
- [ ] Notebook runs successfully with `jupyter nbconvert --execute`
- [ ] Data structure documented in README
- [ ] Relative paths tested on clean directory

---

## 📞 Questions?

If you encounter a path reference you're unsure about:
1. Search the notebook for similar patterns
2. Replace with `ROOT / "relative" / "path"`
3. Test by running from different directory
4. Verify anonymity: no personal info should be visible

---

**Last Updated:** November 28, 2025
