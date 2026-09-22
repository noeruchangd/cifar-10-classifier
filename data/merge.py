from pathlib import Path
import shutil
import csv

source_dir = Path("cifar10/train")

output_dir = Path("cifar10/train")
csv_path = output_dir / "train_labels.csv"

labels = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]

output_dir.mkdir(parents=True, exist_ok=True)

image_extensions = {
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp"
}

rows = []
sequence = 1

for label in labels:
    label_dir = source_dir / label

    if not label_dir.exists():
        print(f"Warning: missing folder: {label_dir}")
        continue

    files = sorted(
        file for file in label_dir.iterdir()
        if file.is_file() and file.suffix.lower() in image_extensions
    )

    for source_file in files:
        new_filename = f"{sequence:06d}{source_file.suffix.lower()}"
        destination_file = output_dir / new_filename

        shutil.copy2(source_file, destination_file)

        rows.append({
            "filename": new_filename,
            "label": label,
        })

        sequence += 1

with csv_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["filename", "label"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Copied {len(rows)} files to: {output_dir}")
print(f"Created CSV: {csv_path}")