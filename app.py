# Smart Download Manager – File Assistant (Updated)
# Skills: functions, loops, conditionals, file I/O, automation

# ---------------- FUNCTIONS ----------------

def load_data():
    """Load previous file records from downloads.txt"""
    downloads = []
    with open("downloads.txt") as file:
        for line in file:
            name, category = line.strip().split(",")
            downloads.append((name, category))
    return downloads


def save_data(downloads):
    """Save all records back to downloads.txt"""
    with open("downloads.txt", "w") as file:
        for name, category in downloads:
            file.write(f"{name},{category}\n")


def detect_category(filename):
    """Automatically decide file category from its extension"""
    if filename.endswith((".jpg", ".png", ".jpeg")):
        return "Image"
    elif filename.endswith((".mp3", ".wav")):
        return "Music"
    elif filename.endswith((".mp4", ".avi", ".mov")):
        return "Video"
    elif filename.endswith((".pdf", ".docx", ".txt")):
        return "Document"
    else:
        return "Other"


def add_file(downloads):
    """Add new file with auto category and duplicate detection"""
    name = input("Enter file name: ").strip()

    # Duplicate check
    for file, _ in downloads:
        if file == name:
            print("This file already exists in the log. Skipped.")
            return downloads

    category = detect_category(name)
    downloads.append((name, category))
    print(f"{name} added as {category}.")
    check_cleanup_suggestion(downloads, category)
    return downloads


def edit_file(downloads):
    """Edit an existing file name"""
    view_files(downloads)
    target = input("Enter the name of the file you want to edit: ").strip()
    found = False

    for i, (name, category) in enumerate(downloads):
        if name == target:
            new_name = input("Enter new file name: ").strip()
            new_category = detect_category(new_name)
            downloads[i] = (new_name, new_category)
            print(f"File '{target}' updated to '{new_name}' ({new_category}).")
            found = True
            break

    if not found:
        print("File not found.")
    return downloads


def delete_file(downloads):
    """Delete a file from the list"""
    view_files(downloads)
    target = input("Enter the name of the file to delete: ").strip()
    new_list = []
    deleted = False

    for name, category in downloads:
        if name != target:
            new_list.append((name, category))
        else:
            deleted = True

    if deleted:
        print(f"File '{target}' deleted.")
    else:
        print("File not found.")

    return new_list


def view_files(downloads):
    """Show all stored files"""
    if not downloads:
        print("No files logged yet.")
    else:
        print("\n--- FILE LIST ---")
        for i, (name, category) in enumerate(downloads, start=1):
            print(f"{i}. {name} ({category})")
        print("-----------------")


def count_categories(downloads):
    """Return a dictionary of category counts"""
    counts = {}
    for _, category in downloads:
        counts[category] = counts.get(category, 0) + 1
    return counts


def check_cleanup_suggestion(downloads, category):
    """Warn user when too many files of one category"""
    counts = count_categories(downloads)
    if counts[category] >= 5:
        print(f"⚠️ You now have {counts[category]} {category.lower()} files. "
              f"Consider cleaning or organizing them!")


def search_files(downloads):
    """Search for files by keyword or category"""
    keyword = input("Enter a keyword or file type to search: ").strip().lower()
    results = []

    for name, category in downloads:
        if keyword in name.lower() or keyword == category.lower():
            results.append((name, category))

    if results:
        print(f"Found {len(results)} matching files:")
        for name, category in results:
            print(f"- {name} ({category})")
    else:
        print("No matches found.")


def generate_summary(downloads):
    """Create summary report automatically"""
    counts = count_categories(downloads)
    total = len(downloads)
    top_type = max(counts, key=counts.get) if counts else "None"

    with open("summary.txt", "w") as file:
        file.write("=== DAILY SUMMARY REPORT ===\n")
        file.write(f"Total files logged: {total}\n")
        for c, n in counts.items():
            file.write(f"{c}: {n}\n")
        file.write(f"Most frequent type: {top_type}\n")
    print("Summary report generated (summary.txt).")


# ---------------- MAIN PROGRAM ----------------

def main():
    downloads = load_data()
    print("Welcome to Smart Download Manager – File Assistant")

    while True:
        print("\n1. Add File")
        print("2. View All Files")
        print("3. Edit File")
        print("4. Delete File")
        print("5. Search Files")
        print("6. Generate Summary")
        print("7. Exit (Auto Save + Backup)")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            downloads = add_file(downloads)
        elif choice == "2":
            view_files(downloads)
        elif choice == "3":
            downloads = edit_file(downloads)
        elif choice == "4":
            downloads = delete_file(downloads)
        elif choice == "5":
            search_files(downloads)
        elif choice == "6":
            generate_summary(downloads)
        elif choice == "7":
            save_data(downloads)
            generate_summary(downloads)
            with open("backup.txt", "w") as backup:
                for name, category in downloads:
                    backup.write(f"{name},{category}\n")
            print("All data saved and backup created. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")



main()
