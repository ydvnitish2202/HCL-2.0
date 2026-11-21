"""Student Academic Analytics: CSV + NumPy + Matplotlib."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

SUBJECTS = ("math", "science", "english", "computer")
PASS_MARK = 40


def read_data(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"student_id", "name", *SUBJECTS}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
        students = list(reader)
    if not students:
        raise ValueError("CSV has no student records.")
    try:
        marks = np.array([[float(row[s]) for s in SUBJECTS] for row in students], dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Marks must be valid numbers in every subject.") from exc
    if not np.all(np.isfinite(marks)) or np.any((marks < 0) | (marks > 100)):
        raise ValueError("Marks must be between 0 and 100.")
    return students, marks


def grade(avg):
    return "A+" if avg >= 90 else "A" if avg >= 80 else "B" if avg >= 70 else "C" if avg >= 60 else "D" if avg >= 50 else "F"


def make_charts(students, marks, show=True, save=True):
    averages = marks.mean(axis=1)
    subject_means = marks.mean(axis=0)
    risks = np.any(marks < PASS_MARK, axis=1)
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("Student Academic Performance Dashboard", fontsize=17, fontweight="bold")

    ax = axes[0, 0]
    bars = ax.bar([s.title() for s in SUBJECTS], subject_means, color="#4f86f7")
    ax.set_title("Average Marks by Subject"); ax.set_ylabel("Average (%)"); ax.set_ylim(0, 110); ax.grid(axis="y", alpha=.2)
    ax.bar_label(bars, fmt="%.1f")

    ax = axes[0, 1]
    order = np.argsort(averages)
    colors = ["#e76f51" if risks[i] else "#2a9d8f" for i in order]
    bars = ax.barh([students[i]["name"] for i in order], averages[order], color=colors)
    ax.set_title("Student Average Scores"); ax.set_xlabel("Average (%)"); ax.set_xlim(0, 110); ax.grid(axis="x", alpha=.2)
    ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8)

    ax = axes[1, 0]
    ax.boxplot([marks[:, j] for j in range(len(SUBJECTS))], tick_labels=[s.title() for s in SUBJECTS], patch_artist=True,
               boxprops={"facecolor": "#b8d8f8"})
    ax.set_title("Marks Spread by Subject"); ax.set_ylabel("Marks (%)"); ax.set_ylim(0, 105); ax.grid(axis="y", alpha=.2)

    ax = axes[1, 1]
    on_track = int(np.sum(~risks)); needs_support = int(np.sum(risks))
    ax.pie([on_track, needs_support], labels=[f"On track ({on_track})", f"Needs support ({needs_support})"],
           colors=["#2a9d8f", "#e76f51"], autopct="%1.0f%%", startangle=90, wedgeprops={"width": .42})
    ax.set_title(f"Class Status (pass mark: {PASS_MARK})")
    fig.tight_layout(rect=[0, 0, 1, .95])
    if save:
        image_path = Path(__file__).with_name("performance_dashboard.png")
        fig.savefig(image_path, dpi=160, bbox_inches="tight")
        print(f"\nGraph saved: {image_path}")
    if show:
        plt.show()
    else:
        plt.close(fig)


def report(students, marks):
    averages = marks.mean(axis=1)
    subject_means = marks.mean(axis=0)
    at_risk = np.any(marks < PASS_MARK, axis=1)
    top = int(np.argmax(averages))
    print("\n" + "=" * 76)
    print("                 STUDENT ACADEMIC ANALYTICS REPORT")
    print("=" * 76)
    print(f"Students: {len(students)} | Class average: {averages.mean():.2f}% | Median: {np.median(averages):.2f}%")
    print(f"Pass rate (all subjects >= {PASS_MARK}): {np.mean(~at_risk)*100:.1f}% | Need support: {at_risk.sum()}")
    print(f"Top student: {students[top]['name']} ({averages[top]:.2f}%, Grade {grade(averages[top])})")
    print("\nSUBJECT SUMMARY")
    print(f"{'Subject':<14}{'Average':>12}{'Highest':>12}{'Lowest':>12}{'Pass rate':>14}")
    for j, subject in enumerate(SUBJECTS):
        print(f"{subject.title():<14}{subject_means[j]:>11.2f}%{marks[:,j].max():>11.0f}%{marks[:,j].min():>11.0f}%{np.mean(marks[:,j]>=PASS_MARK)*100:>13.1f}%")
    print("\nSTUDENT RESULTS (highest average first)")
    print(f"{'ID':<9}{'Name':<22}{'Average':>10}{'Grade':>8}{'Status':>18}")
    for i in np.argsort(averages)[::-1]:
        status = "Needs support" if at_risk[i] else "On track"
        print(f"{students[i]['student_id']:<9}{students[i]['name']:<22}{averages[i]:>9.2f}%{grade(averages[i]):>8}{status:>18}")
    if np.any(at_risk):
        print("\nSUPPORT LIST")
        for i in np.where(at_risk)[0]:
            weak = ", ".join(SUBJECTS[j].title() for j in np.where(marks[i] < PASS_MARK)[0])
            print(f"- {students[i]['name']}: check in on {weak}")
    print("=" * 76)


def main():
    parser = argparse.ArgumentParser(description="Analyze student scores and display/save performance graphs.")
    parser.add_argument("csv_file", nargs="?", type=Path, default=Path(__file__).with_name("students.csv"))
    parser.add_argument("--no-graph", action="store_true", help="Print report without opening graph window")
    args = parser.parse_args()
    try:
        students, marks = read_data(args.csv_file)
        report(students, marks)
        make_charts(students, marks, show=not args.no_graph)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

if __name__ == "__main__":
    main()
