# Student Academic Analytics (Python + NumPy + CSV)

A small command-line project that reads student marks from a CSV file and reports class and subject performance, individual grades, pass rates, top performer, and a support list for students who scored below the pass mark in any subject.

## Requirements
- Python 3.9+
- NumPy

## Setup
Open a terminal in this folder and install NumPy:

```bash
python -m pip install numpy
```

## Run
Use the included sample data:

```bash
python student_academic_analytics.py
```

Or provide your own CSV file:

```bash
python student_academic_analytics.py path/to/students.csv
```

## CSV format
Use these exact column headers. Marks must be numbers from 0 to 100.

```csv
student_id,name,math,science,english,computer
S001,Aarav Sharma,88,92,81,95
```

## Grade scale
- A+: 90 and above
- A: 80–89.99
- B: 70–79.99
- C: 60–69.99
- D: 50–59.99
- F: below 50

A student is listed as needing support if they score below 40 in at least one subject. Change `PASS_MARK` in the Python file to adjust this threshold.
