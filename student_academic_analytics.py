"""Student Academic Analytics: NumPy, pandas, and os."""

import os
import numpy as np
import pandas as pd

SUBJECTS = ["math", "science", "english", "computer"]
PASS_MARK = 40


def read_data(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    data = pd.read_csv(filename)

    required_columns = ["student_id", "name"] + SUBJECTS
    missing_columns = [
        column for column in required_columns if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing CSV columns: " + ", ".join(missing_columns)
        )

    if data.empty:
        raise ValueError("CSV has no student records.")

    try:
        marks = data[SUBJECTS].to_numpy(dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Marks must be valid numbers in every subject."
        ) from exc

    if not np.all(np.isfinite(marks)) or np.any((marks < 0) | (marks > 100)):
        raise ValueError("Marks must be between 0 and 100.")

    return data, marks


def grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"


def report(data, marks):
    averages = np.mean(marks, axis=1)
    subject_averages = np.mean(marks, axis=0)
    at_risk = np.any(marks < PASS_MARK, axis=1)
    top_index = int(np.argmax(averages))

    print("\n" + "=" * 76)
    print("                 STUDENT ACADEMIC ANALYTICS REPORT")
    print("=" * 76)
    print(f"Students: {len(data)}")
    print(f"Class average: {np.mean(averages):.2f}%")
    print(f"Median average: {np.median(averages):.2f}%")
    print(f"Pass rate: {np.mean(~at_risk) * 100:.1f}%")
    print(f"Students needing support: {np.sum(at_risk)}")
    print(
        f"Top student: {data.iloc[top_index]['name']} "
        f"({averages[top_index]:.2f}%, Grade {grade(averages[top_index])})"
    )

    print("\nSUBJECT SUMMARY")
    print(
        f"{'Subject':<14}{'Average':>12}"
        f"{'Highest':>12}{'Lowest':>12}{'Pass rate':>14}"
    )

    for index, subject in enumerate(SUBJECTS):
        subject_marks = marks[:, index]
        pass_rate = np.mean(subject_marks >= PASS_MARK) * 100

        print(
            f"{subject.title():<14}"
            f"{subject_averages[index]:>11.2f}%"
            f"{np.max(subject_marks):>11.0f}%"
            f"{np.min(subject_marks):>11.0f}%"
            f"{pass_rate:>13.1f}%"
        )

    print("\nSTUDENT RESULTS (highest average first)")
    print(
        f"{'ID':<12}{'Name':<22}"
        f"{'Average':>10}{'Grade':>8}{'Status':>18}"
    )

    for index in np.argsort(averages)[::-1]:
        status = "Needs support" if at_risk[index] else "On track"
        student = data.iloc[index]

        print(
            f"{str(student['student_id']):<12}"
            f"{str(student['name']):<22}"
            f"{averages[index]:>9.2f}%"
            f"{grade(averages[index]):>8}"
            f"{status:>18}"
        )

    if np.any(at_risk):
        print("\nSUPPORT LIST")

        for index in np.where(at_risk)[0]:
            weak_subjects = [
                SUBJECTS[subject_index].title()
                for subject_index in np.where(marks[index] < PASS_MARK)[0]
            ]
            print(
                f"- {data.iloc[index]['name']}: "
                f"check in on {', '.join(weak_subjects)}"
            )

    print("=" * 76)


def main():
    filename = "students.csv"

    try:
        data, marks = read_data(filename)
        report(data, marks)
    except (OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()