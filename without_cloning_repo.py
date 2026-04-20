from pydriller import Repository
import re
REPO_URL = "https://github.com/apache/camel"
ISSUES = ["CAMEL-180", "CAMEL-321", "CAMEL-1818", "CAMEL-3214", "CAMEL-18065"]
total_commits = 0
total_files_changed = 0
total_dmm = 0.0

issue_pattern = re.compile("|".join(ISSUES))
for commit in Repository(REPO_URL).traverse_commits():

    if not issue_pattern.search(commit.msg or ""):
        continue

    total_commits += 1
    files_changed = set()
    for mod in commit.modified_files:
        if mod.new_path:
            files_changed.add(mod.new_path)
        if mod.old_path:
            files_changed.add(mod.old_path)

    total_files_changed += len(files_changed)
    unit_sizes = []
    complexities = []
    interfacing = []

    for mod in commit.modified_files:
        if mod.complexity:
            complexities.append(mod.complexity)

        size = (mod.added_lines or 0) + (mod.deleted_lines or 0)
        unit_sizes.append(size)

        interfacing.append(len(mod.changed_methods) if mod.changed_methods else 1)

    if unit_sizes and complexities and interfacing:
        dmm = (
            sum(unit_sizes)/len(unit_sizes)
            + sum(complexities)/len(complexities)
            + sum(interfacing)/len(interfacing)
        ) / 3
    else:
        dmm = 0

    total_dmm += dmm
avg_files = total_files_changed / total_commits if total_commits else 0
avg_dmm = total_dmm / total_commits if total_commits else 0

print("Total commits analyzed:", total_commits)
print("Average number of files changed:", round(avg_files, 2))
print("Average DMM metrics:", round(avg_dmm, 2))